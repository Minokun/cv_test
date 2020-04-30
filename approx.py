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

src = cv2.imread('id-4.jpg')

src_copy = src.copy()
src_y, src_x = src.shape[0:2]

# 获取图像中心点
center_point_x = ceil(src_x/2)
center_point_y = ceil(src_y/2)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
gray_src = cv2.bitwise_not(gray)

kernel = np.ones((5, 5), np.uint8)
dilation = cv2.dilate(gray, kernel, iterations=6)

# ***************** 提取货车车厢部分 *****************
# 二值化
ret, gray_binary = cv2.threshold(dilation, 0, 200, cv2.THRESH_BINARY)

lower = np.array([0, 0])
uper = np.array([180, 180])
mask = cv2.inRange(dilation, 0, 180)

# 边缘检测最大面积区域
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(src_copy, contours, -1, (0, 0, 255), 3)

# 求面积 循环记录最大面积的轮廓index
area_max_index = 0
area_max = 0
area_list = []
n = 0
for i in contours:
    area = cv2.contourArea(i)
    area_list.append(i)
    if area > area_max:
        area_max = area
        area_max_index = n
    n += 1

# 多边形拟合
cnt = contours[area_max_index]
approx = cv2.approxPolyDP(cnt, 3, True)

# 画出多边形
# image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.polylines(src, [approx], True, (0, 255, 0), 2)

# 将轮廓外部变成透明背景
from time import *
begin_time = time()

src_a = cv2.cvtColor(src, cv2.COLOR_RGB2BGRA)
for x in range(src_x):
    for y in range(src_y):
        flag = cv2.pointPolygonTest(cnt, (x, y), False)
        if flag < 0:
            src_a[y][x] = (255, 255, 255, 0)
end_time = time()
run_time = end_time-begin_time
print ('该循环程序运行时间：',run_time)

cv2.imwrite('2.png', src_a)
# showImageList([dilation, mask])