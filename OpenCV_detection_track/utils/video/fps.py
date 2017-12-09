#该模块用来计算视频流的fps
import datetime
class FPS:
    #相当于是计时器，考虑是否可以用装饰器来完成
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        self._end = datetime.datetime.now()

    def update(self):
        self._numFrames += 1#随着视频流的更新来更新帧数

    def elapsed(self):
        return (self._end - self._start).total_seconds()

    def fps(self):
        return self._numFrames/self.elapsed()

