import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
import cv2

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# ## Object detection imports
# Here are the imports from the object detection module.

from utils import label_map_util
from utils import visualization_utils as vis_util

# # Model preparation 
# ## Variables
# 
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.  
# 
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = os.path.join('ssd_mobilenet_v1_coco_11_06_2017', 'frozen_inference_graph.pb')
# PATH_TO_CKPT = os.path.join('ssd_mobilenet_v1_coco_2017_11_17', 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')


NUM_CLASSES = 90

# ## Load a (frozen) Tensorflow model into memory.

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, 
# we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# ## Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# tracker:
tracker = cv2.TrackerKCF_create()
#video = cv2.VideoCapture("videos/trackCar.mp4")
cap = cv2.VideoCapture("videos/trackCar.mp4")
# cap = cv2.VideoCapture(0)
# Exit if video not opened.
if not cap.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame.
ok, frame = cap.read()#frame is the first frame
if not ok:
    print('Cannot read video file')
    sys.exit()

# Define an initial bounding box
bbox = (287, 23, 86, 320)

# Uncomment the line below to select a different bounding box
bbox = cv2.selectROI(frame, False)#select area by user

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)

isDetec = False
start_time = time.time()*1000

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    while True:
      if isDetec:
        isDetec = False
        start_time = time.time()*1000#if isDetec is updated, start_time will update

      # Read a new Frames
      ok, frame = cap.read()  
      if not ok:
          print('video break!')
          break
      #while True:
      # break-time:
      #btime = time.time()*1000

      # Start timer
      timer = cv2.getTickCount()
      # Update tracker
      ok, bbox = tracker.update(frame)
      # Calculate Frames per second (FPS)
      fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
      # Draw bounding box
      if ok:
          # Tracking success
          p1 = (int(bbox[0]), int(bbox[1]))
          p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
          cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
      else :
          # Tracking failure
          cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
      # Display tracker type on frame
      cv2.putText(frame, "KCF" + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
      # Display FPS on frame
      cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
      
      #endtime = time.time()*1000
      #if (btime-endtime) > 2000:
       # break
      # Display result
      #cv2.imshow("Tracking", frame)

      # Exit if ESC pressed
      # k = cv2.waitKey(1) & 0xff
      # if k == 27 : break

      # Definite input and output Tensors for detection_graph
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
      detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')

      # ret, image_np = cap.read()
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      frame_np_expanded = np.expand_dims(frame, axis=0)
      
      if time.time()*1000-start_time >= 0:
        isDetec=True
        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_np_expanded})
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8)

      #print(image_np)
      cv2.imshow("object detection", frame)
      # print(time.time()-start_time)
      if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break




