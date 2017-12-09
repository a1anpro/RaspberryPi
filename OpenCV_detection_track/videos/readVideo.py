import cv2
import sys

video = cv2.VideoCapture("Car.mp4")
if video.isOpened():
	print("video has been opened")
else:
	print("failed to open the video")
	video.release()
	sys.exit()
ok, frame = video.read()
bbox = cv2.selectROI(frame, False)#select area by user
while True:
	ok, frame = video.read()
	if not ok:
		print('[调试] 读取帧失败')
		video.release()
		sys.exit()
	cv2.imshow("frame", frame)

video.release()
cv2.destroyAllWindows()