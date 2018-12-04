Java 鉴权和验权模块设计
<br />
权限模块首先需要了解过滤器和拦截器这两部分的内容：<br />
过滤器和拦截器都属于AOP（面向切面编程）思想的具体实现，系统层面上的问题类似权限，日志，事务等都可以通过AOP的思想来解决。

过滤器依赖servlet容器，而且不由Web服务器执行，是在容器回调用完成，可以修改request和response，所以CORS(后续补充文章介绍CORS)是在过滤器中设计完成。
拦截器首先是属于Web应用的，拦截器可以通过DI来使用工厂中的其他实例实现拦截器的逻辑(这里又有一大坨思想的理解与介绍，大致方向为：单例->DI->IOC->23种设计模式 ~>.<~，后续慢慢补充自己的理解，这里其实是最基础也是最重要的关于我们用的东西到底是如何产生的)
总结就是进入Web服务器之前，可以称为Filter,进入Web服务器之后，称为Interceptor.

回归正题，权限模块主要用到拦截器
大体思路如下：<br />
  涉及到权限到时候，最重要到一步就是表结构设计，User表，Permission表，Role表，User_role表，Role_Permission表。具体表结构参考上传的代码。
大体流程如下：<br />
  0.在数据库中配置好所有的权限信息，给用户分配角色，给角色分配权限，通过这样的关联关系，能够通过用户来获取对应的权限信息。<br />
  1.用户登录之后，将用户信息和用户相关的权限信息存入Redis中，以User_Id 通过Hash加密算法(SHA-256,加密算法后续继续总结)得到SessioID作为Key，相关信息作为Value，然后在利用JWT将SessionID封装为Token。<br />
  2.登录之后将Token返给前端，前端每次发起新的请求的时候，在request head里面都需要将Token带着传递到后台。<br />
  3.JWT拦截器获取到Head里面到Token，解析Token取出登录时存入Redis的相关信息，封装成对应User对象传递给权限拦截器。<br />
  4.Permission拦截器获取到用户相关信息之后，循环对比request的method和URL，如果匹配成功，说明该用户的这个操作，之前在数据库中就被允许，也就是该用户有权限这么做；如果没有匹配，则抛出该用户没有此操作权限的异常。<br />

登录封装Token代码：
 ```    
        String token = JwtUtil.createToken(sessionId, jwtSceret, jwtExpiredTime);
        String refreshToken = JwtUtil.getRefreshToken(sessionId, jwtSceret, jwtExpiredWeekTime);
 ```
 createToken具体实现：
 ```
 Jwts.builder().setSubject(sessionId.toString())
               .claim("sessionId", sessionId.toString())
               .setIssuedAt(new Date()).setExpiration(new Date(System.currentTimeMillis() + expiredTime))
               .signWith(SignatureAlgorithm.HS256, jwtSceret).compact())
 ```
refreshToken是先判断当前Token是否过期，过期就重新再次生成新的Token。
 
 这里封装Token使用的是JWT模块，用于Json对象在传输信息时的一种规范，这里的Token是可以被验证和信任，官方原话如下：JSON Web Tokens are an open, industry standard RFC 7519 method for representing claims securely between two parties.
 具体JWT结构以及用法可以参考[JWT官网](https://jwt.io/)。
 
 前端接受登录返回到Token信息之后，需要在每次请求的head中，带上这个令牌传给后端。请求进入拦截器。
 拦截器的实现方式其实很简单，可以自己定义一个Interceptor类继承[HandlerInterceptor](https://docs.spring.io/spring/docs/5.0.4.BUILD-SNAPSHOT/javadoc-api/org/springframework/web/servlet/HandlerInterceptor.html)/[WebRequestInterceptor](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/context/request/WebRequestInterceptor.html)接口类，或者它实现类HandlerInterceptor/WebRequestInterceptor接口方法(通常直接使用这种，简单便捷)。最后在对应的Config中实例化拦截器，然后在addInterceptors中将其添加到对应到拦截器链中。<br />
 <br />
 添加到拦截器链中：
  ```
 @Override
  public void addInterceptors(InterceptorRegistry registry) {
      registry.addInterceptor(jwtInterceptor())
              .addPathPatterns("/**");
      registry.addInterceptor(permissionInterceptor())
              .addPathPatterns("/**")
              .excludePathPatterns("/xxx/**");
      super.addInterceptors(registry);
  }
  ```
  <br />
  拦截器jwtInterceptor功能代码如下：
  
  ```
  @Override
  public boolean preHandle(HttpServletRequest request, HttpServletResponse reponse, Object handle) throws Exception {
      if ("OPTIONS".equals(request.getMethod().toUpperCase())) {
          return true;
      }
      logger.debug("拦截器1执行-----preHandle");
      String authHeader = request.getHeader(JWT_TOKEN_KEY);
      if (Strings.isNullOrEmpty(authHeader) || !authHeader.startsWith(JWT_HEADER_PREFIX)) {
          throw new UnauthorizedException();
      }
      String token = authHeader.substring(JWT_HEADER_PREFIX.length() + 1);
      if (!JwtUtil.validateToken(token, JWT_SECRET)) {
          throw new UnauthorizedException("token 过期");
      }
      String sessionId = JwtUtil.getSessionId(token, JWT_SECRET);
      UserAuthDTO userAuth = (UserAuthDTO) redisTemplate.opsForValue().get(sessionId);
      if (userAuth == null) {
          redisTemplate.delete(sessionId);
          throw new UnauthorizedException("token 过期");
      }
      request.setAttribute(ReqAttrKey.REQ_USER_AUTH_KEY, userAuth);
      return true;
  }
  ```
  
  拦截器PermissionInterceptor功能代码如下：
  ```
  @Override
  public boolean preHandle(HttpServletRequest request, HttpServletResponse reponse, Object handle) throws Exception {
      if ("OPTIONS".equals(request.getMethod().toUpperCase())) {
          return true;
      }
      String path = request.getServletPath();
      UserAuthDTO userAuthDTO = (UserAuthDTO) request.getAttribute(ReqAttrKey.REQ_USER_AUTH_KEY);
      PathContainer pathContainer = PathContainer.parsePath(path);
      PathPatternParser ppp = new PathPatternParser();
      long matchCount = userAuthDTO.getPermissionList()
              .stream()
              .filter(permission -> ppp.parse(permission.getResource()).matches(pathContainer) &&
                     getPermissionAction(path, request.getMethod()) == permission.getAction())
              .count();
      if (matchCount == 0) {
          throw new AccessForbiddenException();
      }
      return true;
  }
  ```
  
  最后，当token过期的时候，为了避免用户重新登录，这里设置了一个refreshToken，前端只需调用对应的refresh接口获取新的token即可：
refresh接口代码如下：

  ```
  @ApiOperation(value="刷新Token", notes="刷新Token")
  @RequestMapping(value="/xxx/token/refresh", method=RequestMethod.GET, produces=MediaType.APPLICATION_JSON_VALUE)
  public Reply<TokenRespDTO> refreshtoken(
          @ApiParam @RequestParam("refreshToken") final String refreshToken) throws Exception {
      String newToken = JwtUtil.refreshToken(refreshToken, jwtSceret, jwtExpiredTime);
      if (Strings.isNullOrEmpty(newToken)) {
          throw new UnauthorizedException("token 过期，请重新登录");
      }
      String sessionId = JwtUtil.getSessionId(newToken, jwtSceret);
      redisTemplate.expire(sessionId, jwtExpiredTime, TimeUnit.MILLISECONDS);
      return new Reply<>(ReplyBizStatus.OK, "success", new TokenRespDTO(newToken, refreshToken, jwtExpiredTime/1000));
  }
  ```
  
  在用户登录成功之后，首先会访问的接口是该用户所属权限下的模块（菜单信息）接口，前端再根据对应的返回数据，展示出只属于该用户的菜单模块。
  菜单模块接口如下：
  ```
  @ApiOperation(value="模块列表", notes="模块列表")
  @RequestMapping(value="/moudle/list", method=RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
  public Reply<List<MoudleDTO>> moudleList(
          @RequestAttribute(ReqAttrKey.REQ_USER_AUTH_KEY) UserAuthDTO userAuth) throws Exception {

          List<PermissionDTO> permissionDTOList = userAuth.getPermissionList();
          // permissionDTOList.stream().map(tp -> tp.toConvertTemp()).cocat(entityPermissionDTOList.stream().map(tp -> tp.toConvertTemp()));
          List<PermissionDTO> tmpPermissionAllList = new ArrayList<>();
          if (permissionDTOList != null){
              tmpPermissionAllList.addAll(permissionDTOList);
          }
          List<MoudleDTO> result = new ArrayList<>();

          for (PermissionDTO tmpPermissionAll : tmpPermissionAllList){
              MoudleDTO moudleDto = moudleService.getById(tmpPermissionAll.getMid());
              if (!result.contains(moudleDto)){
                  result.add(moudleDto);
              }
          }
          List<MoudleDTO> finalResult = moudleService.getPidMoudle(result);
          return new Reply<>(ReplyBizStatus.OK, "success", finalResult);
      }
  }
  ```
  首先在菜单是一个树形结构，且菜单的叶子节点对应的就是权限表里面对应的数据，所以这里获取菜单的操作可以理解为根据叶子节点获取整颗树的操作。上述代码中原本有一个用户登录系统的权限，还有一个具体业务的权限，然后具体业务的权限这里就直接Pass掉，原理其实一样。于是想着给系统添加一套处理树的工具类，方便之后类似 部门，菜单，地区等等这些树形结构的处理：
   工具类中一些简单的处理方法就直接Pass掉，这里主要来理清一下深度优先遍历和广度优先遍历这两种对树的子节点遍历方法。
   
   
   深度优先遍历的算法大致如下：
        1.首先会使用到Stack栈这种数据类型，特点是数据先进后出；
        2.首先第一个节点需要入栈；再出栈，将第一节点的子节点入栈
   
   ```
   public class DeepWalkTree<T extends BaseNode> extends Tree<T> {

        public DeepWalkTree(List<T> nodes){
          super(nodes);
        }

        @Override
        public List<T> findAllChildren(T node) {
          Stack <T> treeStack = new Stack<>();
          List<T> childrenNodes = new ArrayList<>();
          treeStack.add(node);
          while (!treeStack.isEmpty()) {
              T tmpNode = treeStack.pop();
              List<T> snodes = findChildren(tmpNode);
              if (!snodes.isEmpty()){
                  childrenNodes.addAll(snodes);
              }
              for (T snode : snodes){
                  treeStack.add(snode);
              }
          }
          return childrenNodes;
      }
   }
   ```
   
 
  


 这里的菜单模块接口，给权限控制系统第一层保证，能够现在在前端页面该用户能够发送请求的范围，这也是权限在前端页面的具体体现；然后后台系统中也有完整的鉴权验权机制，权限控制设计的思路大致为上面的一系列介绍，如果有什么缺陷和遗漏的地方，还希望大家多多提点提点。
 
 
 
 
 
 
 参考文档：
    https://www.jianshu.com/p/4339eea38c81
    
 
 
   
