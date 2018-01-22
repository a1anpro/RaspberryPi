#将摄像头的视频流用另一个线程来执行。主线程只做处理部分
from threading import Thread
import cv2
import sys
#注：动词加ed是bool变量

class WebcamStream:
    def __init__(self, src = 0):#默认是打开0号摄像头
        self.stream =  cv2.VideoCapture(src)
        print("[调试] 打开",src, "视频流")
        (self.grabbed, self.frame) = self.stream.read()#读取第一帧
        if not self.grabbed:#如果第一帧没有读到说明视频流没有打开
            print("未读到第一帧")
            sys.exit(-1)#先这样处理，之后用异常来让用户选择
        self.stopped = False#是否暂停视频流

    # 读取当前帧
    def read(self):
        return self.frame

    def start(self):
        # 把update函数运行的内容新建一个线程
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        while True:#持续读视频流
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    # 停止继续读视频流，但是资源并没有释放
    def stop(self):
        self.stopped = True
