# encoding=utf-8

import os
import time
import cv2
import turtle
import numpy as np
import pylab
import pygame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mathtext as mathtext
import matplotlib
try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    import Image, ImageDraw, ImageFilter, ImageFont


def cal_time(func):  
    def run_time():  
        start=time.clock()
        func()  
        stop=time.clock()
        print(stop-start)  
    return run_time  

# 1.用Image生成图片
def draw_line1(name):
    image = Image.new("RGB", (300, 50), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 20)
    draw.text((10, 5), u'test1', font=font, fill="#000000")
    image.save(name)

    return

# 2.用pygame来生成图片
def draw_line2():
    pygame.init()
    font = pygame.font.Font("/System/Library/Fonts/Hiragino Sans GB.ttc", 20)
    rtext = font.render('line2', True, (0, 0, 0), (255,255,255))
    pygame.image.save(rtext, "line22.jpg")
    im = Image.open('line2.jpg')

    return

# 3.np+Image生成图片
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

# 4.np+opencv生成图片
def draw_line4():
    font = cv2.FONT_HERSHEY_SIMPLEX
    im = np.zeros((50,300,3), np.uint8)
    cv2.putText(im,u"Hello World!", (10, 10), font, 0.5, (255, 255, 255), 2) #Draw the text
    cv2.imwrite('line4.png', im)

    return

# 5.np+pylab生成图片
def draw_line5():
    image = np.zeros((50,300,3), np.uint8)
    pylab.text(20, 20, '123', color = 'b', size='large')
    pylab.axis('off')
    pylab.imshow(image)
    pylab.savefig('line5.jpg')

    return

# 6.matplotlib.pyplot生成图片
def draw_line6():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.text(3, 2, u'line6 text')
    ax.axis([0, 10, 0, 10])
    ax.axis('off')
    plt.savefig('line6.jpg')

    return

# 7.matplotlib.mathtext生成图片
def draw_line7():
    parser = mathtext.MathTextParser("Bitmap")
    parser.to_png('line7.png', '123', color='red', fontsize=20, dpi=100)

    return

# 图片拼接
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


if __name__ == "__main__":
    draw_line1('line1.jpg')

    draw_line1('line2.jpg')

    # draw_line2()

    # draw_line3()

    # draw_line4()

    # draw_line5()

    # draw_line6()

    # draw_line7()

    join_pic()
