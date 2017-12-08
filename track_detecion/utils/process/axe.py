#这是一个通用的工具集合：图片旋转，改变大小等。。
import cv2
#按比例改变大小
def resize(image, height):
    ratio = height / image.shape[1]
    dim = (height, int(image.shape[0]*ratio))

    resized = cv2.resize(image,dim, interpolation=cv2.INTER_AREA)
    return resized