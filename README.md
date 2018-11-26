# python 画图的几种方法总结
画图初衷：
   最初的需求是将两张Icon按照要求整合为一个Icon，原本是一个拼接图片的工作，用到的为Python的PIL包，Python里面最重要的两个包还是Np和Pandas，但是PIL包还是挺有意思的，值得去多看下。画图方法--》新包--》学习更多的包！
   拼接图片有很多种思路，主要是要先选择好了思路，再去找对应的实现方法，[本文中拼接用到的方法为Image.paste](https://pillow.readthedocs.io/en/latest/_modules/PIL/Image.html#Image.paste)，拼接方法代码如下:
   
      def join_pic():
          left = 0
          right = 50
          image_path = ['line1.jpg', 'line2.jpg']
          target = Image.new('RGB', (300, 100))
          for i in image_path:
              target.paste(Image.open(i), (0, left, width, right))
              left = left + unit_size
              right = right + unit_size
              quality_value = 100
              target.save('result.jpg', quality=quality_value)
          
          left = 100
          right = 80
          image_path_2 = ['icon.jpg', 'result.jpg']
          target2 = Image.new('RGB', (480, 100), (255, 255, 255))
          for i in image_path_2:
              target2.paste(Image.open(i), (left, 0))
              left = left + 80
              quality_value = 100
              target2.save('last.jpg', quality=quality_value)
          return
     
   本文的重点为多种方式来实现画图的，目前脑海里能想到用Python画图的暂时只有7种，日后再慢慢总结新的方法
    
### 1. 根据Image来生成图片

      def draw_line1(name):
          image = Image.new("RGB", (300, 50), (255, 255, 255))
          draw = ImageDraw.Draw(image)
          font = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 20)
          draw.text((10, 5), u'test1', font=font, fill="#000000")
          image.save(name)

          return

### 2. 根据pygame来生成图片

      def draw_line2():
          pygame.init()
          font = pygame.font.Font("/System/Library/Fonts/Hiragino Sans GB.ttc", 20)
          rtext = font.render('line2', True, (0, 0, 0), (255,255,255))
          pygame.image.save(rtext, "line22.jpg")
          im = Image.open('line2.jpg')

          return
          
## 3. 根据np+Image来生成图片

      def draw_line3():
          array = np.ndarray((50, 300, 3), np.uint8)
          array[:, :, 0] = 0  
          array[:, :, 1] = 0  
          array[:, :, 2] = 100  
          image = Image.fromarray(array)
          draw = ImageDraw.Draw(image)  
          font = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 40, encoding="unic")
          draw.text((10, 5), 'line3', font=font, fill="#000000") 
          # image.show()
          image.save("line3.jpg") 

          return
          
## 4. 根据np+opencv来生成图片

      def draw_line4():
          font = cv2.FONT_HERSHEY_SIMPLEX
          im = np.zeros((50,300,3), np.uint8)
          cv2.putText(im,u"Hello World!", (10, 10), font, 0.5, (255, 255, 255), 2) #Draw the text
          cv2.imwrite('line4.png', im)

          return
          
## 5. 根据np+pylab来生成图片

      def draw_line5():
          image = np.zeros((50,300,3), np.uint8)
          pylab.text(20, 20, '123', color = 'b', size='large')
          pylab.axis('off')
          pylab.imshow(image)
          pylab.savefig('line5.jpg')

          return
          
## 6. 根据matplotlib.pyplot生成图片

      def draw_line6():
          fig = plt.figure()
          ax = fig.add_subplot(111)
          ax.text(3, 2, u'line6 text')
          ax.axis([0, 10, 0, 10])
          ax.axis('off')
          plt.savefig('line6.jpg')

          return
          
## 7. 根据matplotlib.mathtext生成图片

      def draw_line7():
          parser = mathtext.MathTextParser("Bitmap")
          parser.to_png('line7.png', '123', color='red', fontsize=20, dpi=100)

          return
          


