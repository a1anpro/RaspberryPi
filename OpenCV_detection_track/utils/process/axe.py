# 这是一个通用的工具集合：图片旋转，改变大小等。。
# 通用工具中加入：判断矩形是否相交，计算相交矩形的公共面积
import cv2
import math
# 按比例改变大小：
def resize(image, height):
    ratio = height / image.shape[1]
    dim = (height, int(image.shape[0]*ratio))

    resized = cv2.resize(image,dim, interpolation=cv2.INTER_AREA)
    return resized

# 判断矩形是否特殊情况：
def isCoincident(rec1, rec2):
    if rec1[0] > rec2[0] and rec1[1] > rec2[1] and rec1[2] < rec2[2] and rec1[3] < rec2[3]:
        return True
    return False

# 判断两个矩形是否相交：
# 两个矩形如果不相交，则有4 中位置关系：A在中间，B在上、下、左、右
def isIntersected(rec1, rec2):# rec是一个tuple,包含四个值，分别是：左上x，左上y，右下x，右下y
    notintersected = False
    # rec2在rec1之上：
    notintersected = rec2[3] < rec1[1]
    # 之下：
    notintersected = rec2[1] > rec1[3]
    # 之左：
    notintersected = rec2[2] < rec1[0]
    # 之右：
    notintersected = rec2[0] > rec1[2]

    return not notintersected

# 计算相交区域面积
def intersectedArea(rec1, rec2):
    # 根据归纳，利用两个矩形的左下和右上坐标计算相交面积
    r1 = (rec1[0], rec1[3], rec1[2], rec1[1])
    r2 = (rec2[0], rec2[3], rec2[2], rec2[1])

    # 根据关系计算实际要计算的坐标，初始化都为0
    leftDownX = leftDownY = 0
    rightUpX = rightUpY = 0

    # 交叉面积规律
    leftDownX = max(r1[0], r2[0])
    leftDownY = min(r1[1], r2[1])
    rightUpX = min(r1[2], r2[2])
    rightUpY = max(r1[3], r2[3])

    # print("左下角坐标：", (leftDownX,leftDownY))
    # print("右上角坐标：", (rightUpX, rightUpY))

    retarea = (rightUpX - leftDownX) * (rightUpY - leftDownY)
    if retarea > 0:
        retarea = retarea
    else:
        retarea = -retarea
    return retarea

# 计算矩形面积，左上和右下坐标
def recArea(rec):
    return (rec[3]-rec[1])*(rec[2]-rec[0])

# 相交面积与相并面积比值
def intersectedRate(rec1, rec2):
    rate = 0.0
    if isIntersected(rec1, rec2):
        # print("矩形相交")
        iArea = intersectedArea(rec1, rec2)
        totalArea = recArea(rec1) + recArea(rec2) - iArea
        rate = iArea / totalArea
        # print("置信率:", rate)
    return rate

# 如果相交且相交区域比例较大则说明是同一个检测对象
def isSameObject(rec1, rec2):
    issame = False
    if isIntersected(rec1, rec2):
        # print("矩形相交")
        iArea = intersectedArea(rec1, rec2)

        if isCoincident(rec1, rec2):
            rate = 1.0
        else:
            rate = iArea / recArea(rec2)
        # print("重合率：", rate)
        issame = rate > 0.9

    return issame

# 计算中心点，来保证矩形位置偏移度很小
def calcCenterPoint(rec):
    return ((rec[0]+rec[2])/2, (rec[1]+rec[3])/2)

# 计算两个矩形中心点距离
def calcCenterLength(rec1, rec2):
    p1 = calcCenterPoint(rec1)
    p2 = calcCenterPoint(rec2)

    return math.sqrt(math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2))

# 判断是否更新
def shouldUpdate(normal_rec, maxCoincidentBox, minDriftageBox):
    isUpdate = False
    if calcCenterLength(normal_rec, maxCoincidentBox) <= calcCenterLength(normal_rec, minDriftageBox):
        isUpdate = True
    return isUpdate

