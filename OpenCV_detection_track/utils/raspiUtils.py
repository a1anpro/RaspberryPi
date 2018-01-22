# coding:utf-8
# Python中声明文件编码的注释，编码格式指定为utf-8

import time

# 小车转向状态
TURNLEFT = 10
TURNRIGHT = 20
TURNLEFT_BACK = 30
TURNRIGHT_BACK = 40

# 小车前进状态
AVERAGE = 1
SLOWDOWN = 2
SPEEDUP = 3
STOP = 4

def turnLeft_back():
    print('左转-回程')


def turnRight_back():
    print('右转-回程')


def openRightWheel():
    pass


def openLeftWheel():
    pass


def changeDirection(state):
    openRightWheel()
    openLeftWheel()

    if state == TURNLEFT:
        print('左转')
    elif state == TURNRIGHT:
        print('右转')
    elif state == TURNLEFT_BACK:
        print('左转_回程')
    elif state == TURNRIGHT_BACK:
        print('右转_回程')


def forward(state=AVERAGE):
    """
    前进，有三种状态，匀速、减速、加速

    """
    openRightWheel()
    openLeftWheel()

    speed = 50
    if state == SLOWDOWN:
        print('减速')
        speed -= 20
    elif state == SPEEDUP:
        print('加速')
        speed += 20
    elif state == STOP:
        print('停止')
        speed = 0


def back():
    """
    后退
    """
    print('后退')


def stop():
    # print('motor 停机')
    pass


def test_StateChange():
    """
    三种状态测试:匀速、加速、减速
    """
    state_list = [AVERAGE, SPEEDUP, TURNLEFT, TURNRIGHT, SLOWDOWN, STOP, AVERAGE, SPEEDUP, AVERAGE]
    for state in state_list:
        if state < 10:
            forward(state)
        else:
            changeDirection(state)

        time.sleep(2.0)


def test_Direction():
    state_list = [TURNLEFT, TURNLEFT_BACK, TURNRIGHT, TURNRIGHT_BACK]
    for state in state_list:
        changeDirection(state)
        time.sleep(2.0)


if __name__ == '__main__':
    test_StateChange()
    # test_Direction()
    stop()
