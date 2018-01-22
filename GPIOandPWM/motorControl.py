#coding:utf-8
#Python中声明文件编码的注释，编码格式指定为utf-8
import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
'''
电机组A：IN1是GPIO19， IN2是GPIO16， ENA是GPIO13。
电机组B：IN3是GPIO21， IN4是GPIO26， ENB是GPIO20
'''

def func(pos, forward=True):
	if pos == ENA:
		GPIO.output(ENA, True)
		if forward:
			GPIO.output(IN1, True)
			GPIO.output(IN2, False)
		else:
			GPIO.output(IN1, False)
			GPIO.output(IN2, True)
	elif pos == ENB:
		GPIO.output(ENB, True)
		if forward:
			GPIO.output(IN3, True)
			GPIO.output(IN4, False)
		else:
			GPIO.output(IN3, False)
			GPIO.output(IN4, True)

lpwm = GPIO.PWM(ENA, 50)  # 左转 使能信号的pwm
rpwm = GPIO.PWM(ENB, 50)  # 右转 使能信号的pwm
lpwm.start(0)
rpwm.start(0)


# def turnLeft(rate=0.5):
# 	openRightWheel()
# 	openLeftWheel()

# 	lpower = 80  # 左转力量
# 	rpower = (1-rate)*lpower  # 右转力量

# 	lpwm.ChangeDutyCycle(lpower)
# 	rpwm.ChangeDutyCycle(rpower)


# def turnRight(rate=0.5):
# 	openRightWheel()
# 	openLeftWheel()

# 	rpower = 80  # 左转力量
# 	lpower = (1-rate)*rpower  # 右转力量

# 	rpwm.ChangeDutyCycle(rpower)
# 	lpwm.ChangeDutyCycle(lpower)


def turnLeft_back():
	GPIO.output(ENA, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(ENB, True)
	GPIO.output(IN3, True)
	GPIO.output(IN4, False)
	
	lpwm.ChangeDutyCycle(60)
	rpwm.ChangeDutyCycle(30)


def turnRight_back():
	GPIO.output(ENA, True)
	GPIO.output(IN1, True)
	GPIO.output(IN2, False)
	GPIO.output(ENB, True)
	GPIO.output(IN3, True)
	GPIO.output(IN4, False)
	
	lpwm.ChangeDutyCycle(30)
	rpwm.ChangeDutyCycle(60)


def openRightWheel():
	GPIO.output(ENA, True)
	GPIO.output(IN1, False)
	GPIO.output(IN2, True)


def openLeftWheel():
	GPIO.output(ENB, True)
	GPIO.output(IN3, False)
	GPIO.output(IN4, True)


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

def changeDirection(state, continue_time = 2.0):
	openRightWheel()
	openLeftWheel()
	
	if state == TURNLEFT:
		print('左转')
		lpwm.ChangeDutyCycle(60)
		rpwm.ChangeDutyCycle(30)
	elif state == TURNRIGHT:
		print('右转')
		lpwm.ChangeDutyCycle(30)
		rpwm.ChangeDutyCycle(60)
	elif state == TURNLEFT_BACK:
		print('左转_回程')
		turnLeft_back()
	elif state == TURNRIGHT_BACK:
		print('右转_回程')
		turnRight_back()

	time.sleep(continue_time)
		

def forward(state = AVERAGE, continue_time = 2.0):
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

	rpwm.ChangeDutyCycle(speed)
	lpwm.ChangeDutyCycle(speed)
	time.sleep(continue_time)  # 持续时间

def back():
	"""
	后退
	"""
	rpwm.ChangeDutyCycle(30)
	lpwm.ChangeDutyCycle(30)

	GPIO.output(ENA,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)

	GPIO.output(ENB,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)


def stop():
	# print('motor 停机')
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)

	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)

	lpwm.stop()
	rpwm.stop()

	GPIO.cleanup()


def test_turnLeft():
	print('左转')
	turnLeft()
	time.sleep(3.0)

def test_turnRight():
	print('右转')
	turnRight()
	time.sleep(3.0)

def test_turnLeftBack():
	print('左转_回程')
	turnLeft_back()
	time.sleep(3.0)

def test_turnRightBack():
	print('右转_回程')
	turnRight_back()
	time.sleep(3.0)

def test_LeftRight():
	test_turnLeft()
	test_turnLeftBack()
	test_turnRight()
	test_turnRightBack()

def getRandom():
	return random.randint(1,3)*1.0+random.randint(0,10)*0.1

def test_StateChange():
	"""
	三种状态测试:匀速、加速、减速
	"""

	state_list = [{
		'state': AVERAGE, 
		'time': getRandom(),
	}, {
		'state': SPEEDUP, 
		'time': getRandom(),
	}, {
		'state': SLOWDOWN, 
		'time': getRandom(),
	}, {
		'state': STOP, 
		'time': getRandom(),
	}, {
		'state': TURNLEFT, 
		'time': getRandom(),
	}, {
		'state': TURNRIGHT, 
		'time': getRandom(),
	}, {
		'state': AVERAGE, 
		'time': getRandom(),
	}, {
		'state': STOP, 
		'time': getRandom(),
	},  
	]
	for state in state_list:
		s = state['state']
		t = state['time']
		print(s, t)
		if state['state'] < 10:
			forward(s, t)
		else :
			changeDirection(s, t)

def test_Direction():
	state_list = [{
		'state': TURNLEFT, 
		'time': getRandom(),
	}, 
	{
		'state': TURNLEFT_BACK, 
		'time': getRandom(),
	}, 
	{
		'state': TURNRIGHT, 
		'time': getRandom(),
	},
	{
		'state': TURNRIGHT_BACK, 
		'time': getRandom(),
	},
	]
	for state in state_list:
		s = state['state']
		t = state['time']
		print(s, t)
		changeDirection(s, t)

if __name__ == '__main__':
	test_StateChange()
	# test_Direction()
	stop()
