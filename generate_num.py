from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np
from approx import *

def generateNumPic(n):
    """
    随机生成n个数字图片
    :param n: 数量
    :return:
    """
    # 设置黑色背景
    background = Image.new('RGBA', (80, 150), (0, 0, 0))
    # 初始画布
    draw = ImageDraw.Draw(background)
    # # 设置字体
    font_path = 'AllertaStencil-Regular-VTT.ttf'
    font = ImageFont.truetype(font_path, 120)
    # # 写上数字
    draw.text((5, 20), '8', font=font, fill=(255, 255, 255))


# generateNumPic(7000)
import os
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name.endswith('.jpg'):
            pic = getSplitPic(name)
            cv2.imwrite('gray' + name, pic)