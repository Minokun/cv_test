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

src = cv2.imread('id-2.jpg')
src_copy = src.copy()
src_y, src_x = src.shape[0:2]
# 获取图像中心点
center_point_x = ceil(src_x/2)
center_point_y = ceil(src_y/2)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
gray_src = cv2.bitwise_not(gray)

kernel = np.ones((5, 5), np.uint8)
dilation = cv2.dilate(gray, kernel, iterations=6)

# 提取货车车厢部分

# 二值化
ret, gray_binary = cv2.threshold(dilation, 0, 200, cv2.THRESH_BINARY)

lower = np.array([0, 0])
uper = np.array([180, 180])
mask = cv2.inRange(dilation, 0, 180)

# 边缘检测最大面积区域
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(src, contours, -1, (0, 0, 255), 3)

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

# 绘制最大面积区域
cv2.drawContours(src, area_list[area_max_index], -1, (0, 0, 255), 2)

# p = 0
# point_dict = {}
# distance_list = []
# font=cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(src, str('center'), (center_point_x-10,center_point_y+10), font, 1, (0, 0, 255), 2)
# for i in contours:
#     #将轮廓分解为识别对象的左上角坐标和宽、高
#     x, y, w, h = cv2.boundingRect(i)
#     #在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
#     cv2.rectangle(src, (x, y), (x+w, y+h), (0, 255,), 3)
#     #加减10是调整字符位置
#     cv2.putText(src, str(p), (x-10, y+10), font, 1, (0, 0, 255), 2)
#     # 获取每个矩形到中心点的距离
#     distance = sqrt(pow(center_point_x - x, 2) + pow(center_point_y - y, 2))
#     distance_list.append(distance)
#     point_dict[distance] = (y, y+h, x, x+w)
#     p += 1

showImage(src)
# showImageList([dilation, mask])
