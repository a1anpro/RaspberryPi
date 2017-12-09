import cv2
import numpy as np
from utils.videostream import VideoStream
import time
from utils.video.fps import FPS
import utils.process.axe as tools
import datetime

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

PROTOTXT_PATH = "models\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = "models\MobileNetSSD_deploy.caffemodel"
DEFAULT_CONFIDENCE = 0.3

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

# initialize the video stream, allow the camera sensor to warmup
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

# loop over the frames from the video stream
while True:
	frame = vs.read()
	frame = tools.resize(frame,height=700)

	# grab the frame dimensions and convert it to a blob
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300,300)), 0.007843, (300,300), 127.5)

	#pass the blob through the network the network and obtain the detections and predictions
	net.setInput(blob)
	detections = net.forward()

	#loop over the detections
	for i in np.arange(0, detections.shape[2]):
		confidence = detections[0,0,i,2]

		if confidence > DEFAULT_CONFIDENCE:
			index = int(detections[0,0,i,1])
			box = detections[0,0,i,3:7]*np.array([w,h,w,h])
			(startX, startY, endX, endY) = box.astype("int")

			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[index],
										 confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
						  COLORS[index], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[index], 2)
			#在显式中打时间戳
			timestamp = datetime.datetime.now()
			ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
			cv2.putText(frame, ts, (40, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

	fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
