import cv2
import sys
from utils.videostream import VideoStream
import numpy as np

PROTOTXT_PATH = "models\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = "models\MobileNetSSD_deploy.caffemodel"
DEFAULT_CONFIDENCE = 0.3

if __name__ == '__main__':
    # 创建线程的同时
    vs = VideoStream(src=0).start()
    frame = vs.get_firstFrame()

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # 加载模型
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    bbox = None
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > DEFAULT_CONFIDENCE:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            if CLASSES[idx] == 'person':
                bbox = (startX, startY, endX, endY)
                print('[DEBUG]the person coordinate:', startX, startY, endX, endY)

            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    # 输出检测到的各物体位置
    cv2.imshow("Output", frame)
    cv2.waitKey(0)
    # 关闭窗口
    cv2.destroyAllWindows()

    ##################################
    video = cv2.VideoCapture(0)
    _, frame = video.read()
    bbox = cv2.selectROI(frame, False)
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
            vs.stop()
            break

    # 释放视频流资源
    vs.release()