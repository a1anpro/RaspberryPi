# RaspberryPi
object detection and tracking the person we want, warning him/her duly

## Environment:
Often use: Windows10 + Python3.6 + OpenCV3.3.0 + Tensorflow1.2.1
Occasionally use: Ubuntu14.04 + ...(same as above)

## File description:
---
### Fisrt try:
  
  object_detection.py - this is the google object detection api demo
  
  opencv_Track.py - opencv contrib track api demo(my environment:opencv3.3.1 python3.6. [opencv and contrib resource website](https://www.lfd.uci.edu/~gohlke/pythonlibs/) ps:you can download [linux-edition](https://pypi.python.org/pypi/opencv-python))
  
  track_detection.py - i integrated them in this file and the performance is terrible

---
### Second try:[didn't finish] optimize:use multithreading
  
  detection_func.py - package the google object detection api to a funtion

---
### Third try:[referenced from *www.pyimagesearch.com*, and thanks Adrian Rosebrock's blog for help]

I quit the second idea i raised, it's too slow to run on my laptop.So, i read many many blogs to look for a better solution:In short, we first need to choose which architecture and model to use.I chose to Combine MobileNets and Single Shot Detectors(ssd).

**MobileNets**(Howard another paper by Google researchers, 2017): We call these networks “MobileNets” because they are designed for resource constrained devices such as your smartphone. MobileNets differ from traditional CNNs through the usage of depthwise separable convolution. It has an amazing efficency, though it sacrifice accuracy.

**Single Shot Detectors(SSDs)**:SSDs was developed by Google, are a balance between Faster R-CNNs(hard to understand, hard to implement and challenge to train) an YOLO(leave much accuracy to be desired). The algorithm is more straightforward (and I would argue better explained in the original seminal paper) than Faster R-CNNs.



  models[dir]:
  
    MobileNetSSD_deploy.caffemodel - model we use
    MobileNetSSD_deploy.prototxt.txt - prototxt, configurations

  
  utils[dir]:
    
    video[dir]:
      fps.py - a module to calculate the fps from video
      webcamstream.py - create a new thread to get webcam, since the video stream may block the main thread to process data, I/O operation is much slower than cpu.
    videostream.py - a unified file with fps and webcamstream
  process[dir]:
  
      axe.py - rotate, resize and so on..., it process image just as axe to trees, hhh...

  Car.mp4 - a video to use
  
  detection_track.py - detection and track all from OpenCV.I integrated them together.
  
  real-time-detection.py - detection
  
  track_thread.py - i used to want to put the track function into a thread module, but i didn't know how to share variable, so i quit...(i will finish it sometime to check if it can speed up)



i will post a tutorial to my [blog](http://www.alanpro.win)