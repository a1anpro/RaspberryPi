from webcamstream import WebcamStream
import cv2
import time

vs = WebcamStream(src = "Car.mp4")
frame = vs.get_firstFrame()
cv2.imshow("frame", frame)
time.sleep(3.0)
print(frame.shape)
print("[调试] 结束...")