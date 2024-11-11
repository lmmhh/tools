# -*- coding: UTF-8 -*-
import cv2
import numpy as np
"""
Created on common image process
@author: <LMM>
"""
from folder_tool import FolderTool
from PIL import Image


class ImageTool:
    def __init__(self, folder_src, folder_dst, src_format="jpg"):
        self.folder_src = folder_src
        self.folder_dst = folder_dst
        self.image_list = FolderTool(self.folder_src, src_format, subfolders=True).file_list

    def read(self, file_path):

        try:
            image = cv2.imread(file_path)
            # print("图像读取成功！")
            return image
        except IOError:
            print("无法读取图像，请检查路径!")

    def reshape2pdf(self, out_path, new_shape=(2000, 1500)):

        count = 0
        for file in self.image_list:
            image = Image.open(file)
            image = image.resize(new_shape)
            image.save(out_path + str(count) + '.pdf', "PDF", resolution=100.0)
            print(f"save {image} as pdf, count={count}")
            count += 1

    def color2space(self, src_image, color_space='RGB'):

        if color_space == 'RGB':
            dst_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
        elif color_space == 'GRAY':
            dst_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
        elif color_space == 'HSV':
            dst_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2HSV)
        elif color_space == 'Lab':
            dst_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2Lab)
        elif color_space == 'YUV':
            dst_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2YUV)
        else:
            raise Exception('color space format not supported')

        return dst_image

    def preprocess(self, src_image):
        # 二值化
        dst_image = cv2.threshold(src_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # 膨胀
        kernel = np.ones((3, 3), np.uint8)
        dst_image = cv2.dilate(dst_image, kernel, iterations=1)
        # 腐蚀
        dst_image = cv2.erode(dst_image, kernel, iterations=1)

        return dst_image

    def preprocess_adaptive(self, src_image):
        # 高斯模糊
        # blurred = cv2.GaussianBlur(img, (1, 1), 0)
        # 灰度化
        gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
        # 自适应阈值化
        thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)
        # 腐蚀和膨胀操作去除噪点
        kernel = np.ones((3, 3), np.uint8)
        eroded = cv2.erode(thresholded, kernel, iterations=1)
        dilated = cv2.dilate(eroded, kernel, iterations=1)

        return dilated