#一个统一的接口，到时候需要把树莓派的视频流接入
from utils.video.fps import FPS
from utils.video.webcamstream import WebcamStream
class VideoStream:
    def __init__(self, src = 0, usePicamera = False):
        if usePicamera:#如果使用pi的摄像头的话就调用这个代码块
            pass
        else:
            self.stream = WebcamStream(src)

    def start(self):
        return self.stream.start()
    def update(self):
        return self.stream.update()
    def read(self):
        return self.stream.read()
    def stop(self):
        return self.stream.stop()
