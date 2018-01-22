#coding:utf-8
#Python中声明文件编码的注释，编码格式指定为utf-8

import RPi.GPIO as GPIO
import time

########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)




def stop():
	print('motor 停机')
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)	



if __name__ == '__main__':
	stop()