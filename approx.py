import cv2
import numpy as np

def getSplitPic(pic, type=1):
    '''
    图像自动切图
    :param pic:
    :param type: 1， 返回灰度图 2 返回原始图 3，返回透明背景图
    :return:
    '''
    # 读取图片
    src = cv2.imread(pic)

    src_copy = src.copy()
    src_y, src_x = src.shape[0:2]

    # 灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 膨胀
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(gray, kernel, iterations=1)

    # ***************** 提取货车车厢部分 *****************
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
    cv2.polylines(src, [approx], True, (0, 255, 0), 2)

    # 将轮廓外部变成透明背景
    if type == 1:
        for x in range(src_x):
            for y in range(src_y):
                flag = cv2.pointPolygonTest(cnt, (x, y), False)
                if flag < 0:
                    gray[y][x] = 0
        return gray
    elif type == 2:
        for x in range(src_x):
            for y in range(src_y):
                flag = cv2.pointPolygonTest(cnt, (x, y), False)
                if flag < 0:
                    src[y][x] = (0, 0, 0)
        return src
    else:
        src_a = cv2.cvtColor(src, cv2.COLOR_RGB2BGRA)
        for x in range(src_x):
            for y in range(src_y):
                flag = cv2.pointPolygonTest(cnt, (x, y), False)
                if flag < 0:
                    src_a[y][x] = (255, 255, 255, 0)
        return src_a