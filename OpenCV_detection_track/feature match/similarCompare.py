import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

# 最简单的以 灰度直方图作为相似比较：
def classify_gray_compare(img1, img2, size=(256,256)):
    start_time = time.time()
    # 计算直方图
    img1 = cv2.resize(img1, size)
    img2 = cv2.resize(img2, size)

    hist1 = cv2.calcHist([img1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0.0, 255.0])

    # 可以比较下直方图
    # plt.plot(range(256), hist1, 'r')
    # plt.plot(range(256), hist2, 'b')
    # plt.show()

    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    print("spent:", time.time() - start_time)
    degree = degree / len(hist1)
    return degree

    # cv2.imshow("img1", img1)
    # cv2.imshow("img2", img2)
    # k = cv2.waitKey(0)
    # if k&0xff==ord('q'):
    #     cv2.destroyAllWindows()

img1 = cv2.imread("img1.png")
img2 = cv2.imread("img2.png")

print("重合度：",classify_gray_compare(img1, img2))