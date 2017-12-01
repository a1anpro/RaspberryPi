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

from utils import label_map_util
from utils import visualization_utils as vis_util

category_index = None
detection_graph = None
sess = None

def prepare():
  #修改全局变量
  global category_index
  global detection_graph

  PATH_TO_CKPT = os.path.join('ssd_mobilenet_v1_coco_11_06_2017', 'frozen_inference_graph.pb')
  PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

  NUM_CLASSES = 150

  # ## Load a (frozen) Tensorflow model into memory.
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')

  # ## Loading label map
  label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
  category_index = label_map_util.create_category_index(categories)

  # return detection_graph

# ## Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)  
      

def detection_pic(image_np):
  start_time = time.time()

  image_np_expanded = np.expand_dims(image_np, axis=0)

  image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
  detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
  detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
  detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
  num_detections = detection_graph.get_tensor_by_name('num_detections:0')

  # Actual detection.
  (boxes, scores, classes, num) = sess.run(
      [detection_boxes, detection_scores, detection_classes, num_detections],
      feed_dict={image_tensor: image_np_expanded})
  # Visualization of the results of a detection.
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      np.squeeze(boxes),
      np.squeeze(classes).astype(np.int32),
      np.squeeze(scores),
      category_index,
      use_normalized_coordinates=True,
      line_thickness=10)

  #print(image_np)
  #cv2.imshow("object detection", image_np)
  print("spent:", time.time()-start_time)
  #cv2.destroyAllWindows()

if __name__ == '__main__':
  prepare()
  # detection_graph = detection_graph.as_default()
  print(detection_graph)
  sess = tf.Session(graph=detection_graph)

  PATH_TO_TEST_IMAGES_DIR = 'test_images'
  TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1,4) ]

  for image_path in TEST_IMAGE_PATHS:
    PIL_img = Image.open(image_path)
    image_np = load_image_into_numpy_array(PIL_img)
    detection_pic(image_np)

  sess.close()  

