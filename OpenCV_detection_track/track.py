import cv2
import sys
from utils.videostream import VideoStream
import numpy as np
import time
PROTOTXT_PATH = "models\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = "models\MobileNetSSD_deploy.caffemodel"
DEFAULT_CONFIDENCE = 0.95

if __name__ == '__main__':
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    # 加载模型
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

    found = False #是否找到目标物


    bbox = None
    count = 1
    video = cv2.VideoCapture("Car.mp4")

    while not found:
        ok, frame = video.read()
        if not ok:
            print("视频读取失败")
            sys.exit(-1)

        # cv2.imshow("car", frame)
        print("frame:", count)
        count += 1

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        print("[INFO] computing object detections...")
        net.setInput(blob)
        detections = net.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > DEFAULT_CONFIDENCE:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                if CLASSES[idx] == 'car':
                    label = "{}: {:.2f}%".format("car",
                                                 confidence * 100)
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  (255,0,0), 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                    bbox = (startX, startY, endX, endY)
                    print('[DEBUG]the car coordinate:', startX, startY, endX, endY)
                    print('[DEBUG] confidence: ', confidence)
                    found = True
                    break# 找到了就可以结束循环了.我们只需要坐标

    time.sleep(3.0)

    ##################################

    print('[DEBUG] 进入跟踪...')
    _, frame = video.read()
    # bbox = cv2.selectROI(frame, False)
    # 创建KCF跟踪对象
    tracker = cv2.TrackerKCF_create()
    # 初始化跟踪的第一帧，bbox是检测出来的第一个person的位置
    ok = tracker.init(frame, bbox)

    while True:
        # 取vs得到的帧，线程一直在运行，不需要update()
        # frame = vs.read()
        _, frame = video.read()
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
        cv2.imshow("Tracking", frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            # vs.stop()
            break

    video.release()
    cv2.destroyAllWindows()
    # 释放视频流资源
    # vs.release()