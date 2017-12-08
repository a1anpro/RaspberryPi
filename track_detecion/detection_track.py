# 跟踪与检测 综合
import cv2
import numpy as np
from utils.videostream import VideoStream
import time
from utils.video.fps import FPS
import utils.process.axe as tools
import datetime

# 配置信息
PROTOTXT_PATH = "models\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = "models\MobileNetSSD_deploy.caffemodel"
DEFAULT_CONFIDENCE = 0.3
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

vs = VideoStream(src="videos\trackCar.mp4").start()
frame = vs.get_firstFrame()

# 加载模型
print("[初始化] 加载模型...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

(h, w) = frame.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

print("[计算] 目标检测...")
net.setInput(blob)
detections = net.forward()

bbox = None
for i in np.arange(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > DEFAULT_CONFIDENCE:
        idx = int(detections[0, 0, i, 1])
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        if CLASSES[idx] == 'person':
            bbox = (startX, startY, endX, endY)
            print('[调试] 目标物的坐标:', startX, startY, endX, endY)
            break #找到person就可以退出了

# 创建KCF跟踪对象
tracker = cv2.TrackerKCF_create()
# 初始化跟踪的第一帧，bbox是检测出来的第一个person的位置
ok = tracker.init(frame, bbox)

while True:
    frame = vs.read()
    # 开始计时器
    timer = cv2.getTickCount()
    # 更新跟踪帧
    ok, bbox = tracker.update(frame)
    # 计算FPS
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    # 画出边框
    if ok:
        # 跟踪成功
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (60, 20, 255), 2, 2)
    else:
        # 跟踪失败
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # 显示跟踪信息到frame
    cv2.putText(frame, "KCF Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
    # 显示FPS到frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    frame = tools.resize(frame, height=500)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # 将blob传给神经网络 获得检测和预测
    net.setInput(blob)
    # 这一步检测是最费时的#####
    detections = net.forward()

    # 处理检测到的物体
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > DEFAULT_CONFIDENCE:
            index = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{}: {:.2f}%".format(CLASSES[index],
                                         confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          COLORS[index], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[index], 2)
            # # 在显式中打时间戳
            # timestamp = datetime.datetime.now()
            # ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            # cv2.putText(frame, ts, (40, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)

    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        vs.stop()
        break

cv2.destroyAllWindows()
vs.stop()
# 释放视频流资源
vs.release()
