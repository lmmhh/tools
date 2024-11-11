from PIL import Image

# 打开图像文件
image = Image.open('jxj2018.jpg')
#
# 降低图像质量
# image.save('by_low_quality.jpg', quality=80)



# 调整图像尺寸
new_size = (image.size[0]//2, image.size[1]//2)
resized_image = image.resize(new_size)

# 保存图像
# resized_image.save('resized_image.jpg')


# 使用压缩算法保存图像
resized_image.save('jxj2018_compressed_image.jpg', optimize=True, compress_level=5)