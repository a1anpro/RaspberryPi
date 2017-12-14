import cv2
import time

# 创建surf特征匹配对象
surf = cv2.xfeatures2d.SURF_create(100)

img1 = cv2.imread("img1.png")
img2 = cv2.imread("img2.png")

# img1 = cv2.cvtColor(cv2.imread("img1.png"), cv2.COLOR_BGR2GRAY)
# img2 = cv2.cvtColor(cv2.imread("img2.png"), cv2.COLOR_BGR2GRAY)
start_time = time.time()
keypoints = surf.detect(img1, None)

# print(dir(keypoints))
print("time:", time.time() - start_time)

# print("list1:", keypoints)

# img = cv2.drawKeypoints(img1, list1, img1)
# cv2.imshow("keypoints_img", img1)
# k = cv2.waitKey(0)
# if k & 0xff == ord('q'):
    # cv2.destroyAllWindows()