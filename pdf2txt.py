# -*- coding: UTF-8 -*-
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

# 设置Tesseract OCR路径（如果需要）
pytesseract.pytesseract.tesseract_cmd = r'D:/Tesseract-OCR/tesseract.exe'


# 将PDF转换为图像
def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images


# 对图像进行OCR处理
def ocr_images(images):
    text = ""
    for image in images:
        image.show()
        image_text = pytesseract.image_to_string(image, lang='chi_sim')
        text += image_text
    return text


# 提取文本中的特定信息（示例）
def extract_information(text):
    # 这里可以使用正则表达式或其他方法来提取特定信息
    # 例如，提取所有以"Hello"开头的行
    lines = text.split('\n')
    hello_lines = [line for line in lines if line.startswith('Hello')]
    print(hello_lines)
    return hello_lines


# 主函数
def process_pdf(pdf_path):
    images = convert_pdf_to_images(pdf_path)
    text = ocr_images(images)
    information = extract_information(text)
    return information


# 示例用法
pdf_file = './pdf2txt/GBT2900.20-2016.pdf'
extracted_info = process_pdf(pdf_file)
# for info in extracted_info:
#     print(info)
# text = pytesseract.image_to_string('./pdf2txt/test.jpg', lang='chi_sim')
# information = extract_information(text)
# print(text)
