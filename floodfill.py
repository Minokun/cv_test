import cv2
import numpy as np
from math import sqrt, ceil

def showImage(image, name='test'):
    # 图像窗口显示
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, image)
    cv2.waitKey()


def showImageList(image_list, name='test'):
    # 图像窗口显示
    image = np.hstack(image_list)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, image)
    cv2.waitKey()

src = cv2.imread('id-1.jpg')
src_y, src_x = src.shape[0:2]

flood_mask = np.zeros([src_y+2, src_x+2], np.uint8)
cv2.floodFill(src, flood_mask, (0, 100), (0, 100, 255), (100, 100, 50), (50, 50, 50), cv2.FLOODFILL_FIXED_RANGE)

showImage(src)