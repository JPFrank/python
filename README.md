# python 画图的几种方法总结
画图初衷：
   最初的需求是将两张Icon按照要求整合为一个Icon，原本是一个拼接图片的工作，用到的为Python的PIL包，Python里面最重要的两个包还是Np和Pandas，但是PIL包还是挺有意思的，值得去多看下。
   [拼接用到的方法](https://pillow.readthedocs.io/en/latest/_modules/PIL/Image.html#Image.paste)，拼接方法代码如下:
   
      def join_pic():
          unit_size = 50
          width = 300
          image_path = ['line1.jpg', 'line2.jpg']
          left = 0
          right = 50
          target = Image.new('RGB', (width, unit_size*2))
          for i in image_path:
              target.paste(Image.open(i), (0, left, width, right))
              left = left + unit_size
              right = right + unit_size
              quality_value = 100
              target.save('result.jpg', quality=quality_value)
          image_path_2 = ['icon.jpg', 'result.jpg']
          j = 0
          target2 = Image.new('RGB', (480, 100), (255, 255, 255))
          left = 100
          right = 80
          for i in image_path_2:
              target2.paste(Image.open(i), (left, 0))
              left = left + 80
              quality_value = 100
              target2.save('last.jpg', quality=quality_value)
          return
    
## 1.
## 2.
## 3.
## 4.
## 5.
## 6.
## 7.
## 8.
## 9.
