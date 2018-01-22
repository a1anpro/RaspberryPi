# 跟踪与检测 综合
import cv2
import numpy as np
from utils.videostream import VideoStream
import time
import math
import utils.process.axe as tools


# 配置信息
PROTOTXT_PATH = "models\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = "models\MobileNetSSD_deploy.caffemodel"
DEFAULT_CONFIDENCE = 0.5
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# 加载模型
print("[初始化] 加载模型...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)

vs = VideoStream().start()

found = False  # 初始化 未发现目标
count = 1
firstBox = None
lastPersonBox = None


while not found:
    frame = vs.read()
    # 一致化 frame大小，否则得到的目标物坐标系不一致
    frame = tools.resize(frame, height=500)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    print("[计算] 目标检测:", count)
    count += 1
    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.95:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # lastPersonBox用来修正跟踪对象的矩形框大小
            lastPersonBox = (startX, startY, endX, endY)
            found = True
            if CLASSES[idx] == 'person':
                print('[调试] 第一帧目标物坐标:', lastPersonBox)
                break  # 找到了就可以结束循环了.我们只需要坐标

# 1：找到多个检测对象中的 目标物，通过与lastPersonBox矩形的(相交/相并)匹配度来确认目标物
# 2：中心点的偏移

# 保存目标物距离的队列，用来判断目标物 是前进还是后退
move_direction = []
MOVE_NUM = 5  # 判断移动方向的次数
STEP_LEN = 2  # 靠近还是远离的误差值
for i in range(0, MOVE_NUM):
    move_direction.append(i)

while True:
    start_time = time.time()

    frame = vs.read()
    # 一致化
    frame = tools.resize(frame, height=500)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # 将blob传给神经网络 获得检测和预测
    net.setInput(blob)

    # 这一步检测是最费时的
    #####
    detections = net.forward()
    #####

    # 初始化
    maxCoincidentRate = -1.0  # 最大相交率
    minDriftageLength = 0xFF  # 中心点的偏移距离

    maxCoincidentBox = lastPersonBox
    minDriftageBox = lastPersonBox

    # 处理检测到的物体
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > DEFAULT_CONFIDENCE:
            index = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # 如果检测结果是person则与lastPersonBox比较，位移差别较小则是目标。
            # 用相交面积与相并面积的比值最大来确定目标。
            if (CLASSES[index] == 'person'):
                coincident_rate = tools.intersectedRate(lastPersonBox, (startX, startY, endX, endY))  # 计算当前person和目标物的相交比例
                driftage_len = tools.calcCenterLength(lastPersonBox, (startX, startY, endX, endY))  # 当前person和目标物的中心点距离
                if coincident_rate > maxCoincidentRate:
                    maxCoincidentBox = (startX, startY, endX, endY)
                    maxCoincidentRate = coincident_rate
                if driftage_len < minDriftageLength:
                    minDriftageBox = (startX, startY, endX, endY)
                    minDriftageLength = driftage_len

            label = "{}: {:.2f}%".format(CLASSES[index],
                                         confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          COLORS[index], 4)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[index], 2)  # 打标签

    # 如果最大比值的那个框大于设定值，则确定是目标物
    if maxCoincidentRate > 0.5 and tools.shouldUpdate(lastPersonBox, maxCoincidentBox, minDriftageBox):
        # 蓝色是上一帧目标物颜色
        # cv2.rectangle(frame, (lastPersonBox[0], lastPersonBox[1]), (lastPersonBox[2], lastPersonBox[3]), (0, 255, 0), 2, 2)
        # 红色是当前确定的目标物颜色
        #给目标物做出标记 提示
        lable = "  target"
        lable_pos = maxCoincidentBox[1] + 15
        cv2.putText(frame, lable, (maxCoincidentBox[0], lable_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # 设置目标物的标签
        cv2.rectangle(frame, (maxCoincidentBox[0], maxCoincidentBox[1]), (maxCoincidentBox[2], maxCoincidentBox[3]), (0, 255, 0), 2, 2)
        lastPersonBox = maxCoincidentBox

        # 距离计算：
        mid_x = (maxCoincidentBox[0] + maxCoincidentBox[2]) / 2
        mid_y = (maxCoincidentBox[1] + maxCoincidentBox[3]) / 2
        apx_distance = maxCoincidentBox[3] - maxCoincidentBox[1]

        move_direction.pop(0)
        move_direction.append(apx_distance)  # 把当前目标物的距离入队列
        print(move_direction)

        cv2.putText(frame, '{}'.format(apx_distance), (int(mid_x), int(mid_y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        # 靠近还是远离判断
        near_cnt = 0  # 靠近计数器
        far_cnt = 0  # 远离计数器

        for i in range(1, MOVE_NUM):
            difference = move_direction[i] - move_direction[i-1]
            if difference > STEP_LEN:
                near_cnt += 1
            elif difference < -STEP_LEN:
                far_cnt += 1
        if near_cnt >= MOVE_NUM - 2:
            cv2.putText(frame, 'near', (int(mid_x), int(mid_y+20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        elif far_cnt >= MOVE_NUM - 2:
            cv2.putText(frame, 'far', (int(mid_x), int(mid_y + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'keep', (int(mid_x), int(mid_y + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


    cv2.imshow("Tracking", frame)

    print('spent:', time.time() - start_time)

    if cv2.waitKey(1) & 0xff == ord('q'):
        vs.stop()
        break

cv2.destroyAllWindows()
vs.stop()