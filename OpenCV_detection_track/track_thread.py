#跟踪模块由另一个线程执行
from threading import Thread
import cv2

class Tracker:
    def __init__(self, firstFrame, firstBox):
        # KCF的跟踪对象
        self.tracker = cv2.TrackerKCF_create()
        # 由第一帧图和坐标初始化Tracker对象
        self.tracker.init(firstFrame, firstBox)

    def start(self, frame):
        Thread(target=self.update, args=(frame)).start()

    def update(self, frame):
        timer = cv2.getTickCount()
        # 根据穿进来的图，更新跟踪帧
        ok, bbox = self.tracker.update(frame)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        if ok:
            # 跟踪成功
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (60, 20, 255), 2, 2)
        else:
            # 跟踪失败
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # 把跟踪信息画到frame
        cv2.putText(frame, "KCF Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        # 把FPS画到frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        return frame