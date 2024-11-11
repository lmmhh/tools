# -*- coding: UTF-8 -*-
import os
import cv2
import numpy as np


def preprocess(img):
    # 转换为灰度图
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # 膨胀
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    # 腐蚀
    img = cv2.erode(img, kernel, iterations=1)
    return img


def preprocess_adaptive(img):
    # 高斯模糊
    # blurred = cv2.GaussianBlur(img, (1, 1), 0)

    # 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 自适应阈值化
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # 腐蚀和膨胀操作去除噪点
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(thresholded, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)
    return dilated


def find_corners(img):
    """
    Finds the 4 extreme corners of the largest contour in the image.
    """
    # OpenCV版本问题，cv2.findContours 版本3返回值有3个，版本4只有2个
    opencv_version = cv2.__version__.split('.')[0]
    if opencv_version == '3':
        _, contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    # 找到最大的轮廓
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = contours[0]

    # bottom-right point has the largest (x + y) value
    # top-left has point smallest (x + y) value
    # bottom-left point has smallest (x - y) value
    # top-right point has largest (x - y) value

    # 初始化
    val_br = polygon[0][0][0] + polygon[0][0][1]
    val_tl = polygon[0][0][0] + polygon[0][0][1]
    val_bl = polygon[0][0][0] - polygon[0][0][1]
    val_tr = polygon[0][0][0] - polygon[0][0][1]
    bottom_right = polygon[0][0]
    top_left = polygon[0][0]
    bottom_left = polygon[0][0]
    top_right = polygon[0][0]

    # 寻找最大轮廓的4个边界点坐标
    for i in range(1, len(polygon)):
        val_add = polygon[i][0][0] + polygon[i][0][1]
        val_minus = polygon[i][0][0] - polygon[i][0][1]
        if val_add > val_br:
            val_br = val_add
            bottom_right = polygon[i][0]
        if val_add < val_tl:
            val_tl = val_add
            top_left = polygon[i][0]
        if val_minus < val_bl:
            val_bl = val_minus
            bottom_left = polygon[i][0]
        if val_minus > val_tr:
            val_tr = val_minus
            top_right = polygon[i][0]
    # 返回4个边界点坐标
    return [top_left, top_right, bottom_right, bottom_left]


# 得到PPT图片的4个边界点坐标
def crop_and_warp(img, crop_rect):
    """
    Crops and warps a rectangular section from an image into a square of similar size.
    """
    # 4个边界点坐标
    top_left, top_right, bottom_right, bottom_left = \
        crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]

    # Explicitly set the data type to float32 or 'getPerspectiveTransform' will throw an error
    # 原始坐标
    src = np.array([top_left, top_right, bottom_right, bottom_left], dtype='float32')

    width, height = 800, 600  # 设置矫正后的图像尺寸
    dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1], ], dtype=np.float32)

    # Gets the transformation matrix for skewing the image to fit a square by comparing the 4 before and after points
    matrix = cv2.getPerspectiveTransform(src, dst)

    # Performs the transformation on the original image
    img = cv2.warpPerspective(img, matrix, (width, height))
    return img


def calculate_distance(point1, point2, debug=False, threshold=50):
    dis = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    if debug:
        return point1 if dis > threshold else [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]
    return dis


def merge_crop_rect(crop_rect, crop_rect_adaptive, threshold=50):
    """
    合并两种方法得到的边界点坐标，排除异常值
    """
    crop_rect_final = []

    for i in range(4):
        if calculate_distance(crop_rect[i], crop_rect_adaptive[i], threshold=threshold) < threshold:
            crop_rect_final.append((crop_rect[i] + crop_rect_adaptive[i]) / 2)
    if len(crop_rect_final) == 4:
        return np.array(crop_rect_final, dtype='float32')
    elif len(crop_rect_final) == 3:
        crop_rect_final = []
        x1, y1, x2, y2 = crop_rect[0][0], crop_rect[0][1], crop_rect[1][0], crop_rect[1][1]
        x3, y3, x4, y4 = crop_rect[2][0], crop_rect[2][1], crop_rect[3][0], crop_rect[3][1]
        x1_adp, y1_adp, x2_adp, y2_adp = crop_rect_adaptive[0][0], crop_rect_adaptive[0][1], crop_rect_adaptive[1][0], \
        crop_rect_adaptive[1][1]
        x3_adp, y3_adp, x4_adp, y4_adp = crop_rect_adaptive[2][0], crop_rect_adaptive[2][1], crop_rect_adaptive[3][0], \
        crop_rect_adaptive[3][1]

        dis_ab1 = calculate_distance((x1, y1), (x2, y2), threshold=threshold)
        dis_ab2 = calculate_distance((x1_adp, y1_adp), (x2_adp, y2_adp), threshold=threshold)
        dis_cd1 = calculate_distance((x3, y3), (x4, y4), threshold=threshold)
        dis_cd2 = calculate_distance((x3_adp, y3_adp), (x4_adp, y4_adp), threshold=threshold)

        if abs(dis_ab1 - dis_ab2) < threshold:
            crop_rect_final.append([(x1 + x1_adp) / 2, (y1 + y1_adp) / 2])
            crop_rect_final.append([(x2 + x2_adp) / 2, (y2 + y2_adp) / 2])
            basic_dis = (dis_ab1 + dis_ab2) / 2
            if abs(dis_cd1 - basic_dis) < threshold:
                crop_rect_final.append(calculate_distance((x3, y3), (x3_adp, y3_adp), debug=True, threshold=threshold))
                crop_rect_final.append(calculate_distance((x4, y4), (x4_adp, y4_adp), debug=True, threshold=threshold))
            elif abs(dis_cd2 - basic_dis) < threshold:
                crop_rect_final.append(calculate_distance((x3_adp, y3_adp), (x3, y3), debug=True, threshold=threshold))
                crop_rect_final.append(calculate_distance((x4_adp, y4_adp), (x4, y4), debug=True, threshold=threshold))
        elif abs(dis_cd1 - dis_cd2) < threshold:
            basic_dis = (dis_cd1 + dis_cd2) / 2
            if abs(dis_ab1 - basic_dis) < threshold:
                crop_rect_final.append(calculate_distance((x1, y1), (x1_adp, y1_adp), debug=True, threshold=threshold))
                crop_rect_final.append(calculate_distance((x2, y2), (x2_adp, y2_adp), debug=True, threshold=threshold))
            elif abs(dis_ab2 - basic_dis) < threshold:
                crop_rect_final.append(calculate_distance((x1_adp, y1_adp), (x1, y1), debug=True, threshold=threshold))
                crop_rect_final.append(calculate_distance((x2_adp, y2_adp), (x2, y2), debug=True, threshold=threshold))

            crop_rect_final.append([(x3 + x3_adp) / 2, (y3 + y3_adp) / 2])
            crop_rect_final.append([(x4 + x4_adp) / 2, (y4 + y4_adp) / 2])

    if len(crop_rect_final) == 4:
        return np.array(crop_rect_final, dtype='float32')
    else:
        for i in range(4):
            if 0 in crop_rect_adaptive[i]:
                return crop_rect
        return crop_rect_adaptive


if __name__ == '__main__':
    file_src = 'src/'
    file_dst = 'dst/'
    files = os.listdir(file_src)
    for file in files:
        # 读取图片
        img_origin = cv2.imread(file_src + file)
        # img_origin = cv2.imread('static/src/test(5).jpg')
        # 预处理
        img = preprocess(img_origin)
        adaptive = preprocess_adaptive(img_origin)
        # 得到PPT图片的4个边界点坐标
        crop_rect = find_corners(img)
        crop_rect_adaptive = find_corners(adaptive)

        # 合并两种方法得到的边界点坐标，排除异常值
        height, width = img.shape[:2]
        crop_rect_final = merge_crop_rect(crop_rect, crop_rect_adaptive, threshold=width / 20)

        # 矫正
        img = crop_and_warp(img_origin, crop_rect_final)

        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite(file_dst + file, img)