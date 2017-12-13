from utils.process import axe
import cv2
import time
pic = cv2.imread("C:/Users/women/Pictures/wp-1493431453196.jpeg")

choice = 2
if choice==1:
    rec2 = (80, 80, 200, 200)
    rec1 = (50, 50, 250, 250)
else:
    rec1 = cv2.selectROI(pic, False)# 得到的是长宽不是右下坐标
    rec2 = cv2.selectROI(pic, False)
    # 左上、右下
    rec1 = (rec1[0], rec1[1], rec1[0] + rec1[2], rec1[1] + rec1[3])
    rec2 = (rec2[0], rec2[1], rec2[0] + rec2[2], rec2[1] + rec2[3])

p11 = (rec1[0], rec1[1])
p12 = (rec1[2], rec1[3])
p21 = (rec2[0], rec2[1])
p22 = (rec2[2], rec2[3])

print("矩形标准坐标：", rec1, rec2)
print("相交面积：", axe.intersectedArea(rec1, rec2))

cv2.rectangle(pic, p11,p12, (60, 20, 255), 2, 2)
cv2.rectangle(pic, p21,p22, (200,200,200), 2, 2)

if axe.isSameObject(rec1, rec2):
    print("同一个矩形")

cv2.imshow("pic", pic)
cv2.waitKey(1)
time.sleep(10.0)
cv2.destroyAllWindows()

