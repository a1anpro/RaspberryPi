# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
ENA = 13        #//L298使能A
ENB = 20        #//L298使能B
IN1 = 19        #//电机接口1
IN2 = 16        #//电机接口2
IN3 = 21        #//电机接口3
IN4 = 26        #//电机接口4

class Car():
    def __init__(self, left_in1, left_in2, left_ena, right_in3, right_in4, right_enb, low_electrical_level,
                 hight_electrical_level):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.left_in1 = left_in1
        self.left_in2 = left_in2
        self.left_ena = left_ena
        if self.left_ena > 0:
            GPIO.setup(self.left_ena, GPIO.OUT)

        GPIO.setup(self.left_in1, GPIO.OUT)
        GPIO.setup(self.left_in2, GPIO.OUT)

        self.right_in3 = right_in3
        self.right_in4 = right_in4
        self.right_enb = right_enb

        GPIO.setup(self.right_in3, GPIO.OUT)
        GPIO.setup(self.right_in4, GPIO.OUT)
        if self.right_enb > 0:
            GPIO.setup(self.right_enb, GPIO.OUT)

        self.hight_electrical_level = hight_electrical_level
        self.low_electrical_level = low_electrical_level

    def rFoward(self):
        GPIO.output(self.right_in3, self.hight_electrical_level)
        GPIO.output(self.right_in4, self.low_electrical_level)
        if self.right_enb > 0:
            GPIO.output(self.right_enb, self.hight_electrical_level)

    def lFoward(self):
        GPIO.output(self.left_in1, self.hight_electrical_level)
        GPIO.output(self.left_in2, self.low_electrical_level)
        if self.left_ena > 0:
            GPIO.output(self.left_ena, self.hight_electrical_level)

    def rBackward(self):
        GPIO.output(self.right_in3, self.low_electrical_level)
        GPIO.output(self.right_in4, self.hight_electrical_level)
        if self.right_enb > 0:
            GPIO.output(self.right_enb, self.hight_electrical_level)

    def lBackward(self):
        GPIO.output(self.left_in1, self.low_electrical_level)
        GPIO.output(self.left_in2, self.hight_electrical_level)
        if self.left_ena > 0:
            GPIO.output(self.left_ena, self.hight_electrical_level)

    def lStop(self):
        if self.left_ena > 0:
            GPIO.output(self.left_ena, self.low_electrical_level)
        else:
            GPIO.output(self.left_in2, self.low_electrical_level)
            GPIO.output(self.left_in1, self.low_electrical_level)

    def rStop(self):
        if self.right_enb > 0:
            GPIO.output(self.right_enb, self.low_electrical_level)
        else:
            GPIO.output(self.right_in3, self.low_electrical_level)
            GPIO.output(self.right_in4, self.low_electrical_level)

    def moveForward(self):
        self.lFoward()
        self.rFoward()

    def moveBackground(self):
        self.lBackward()
        self.rBackward()

    def spinRight(self):
        self.rFoward()
        self.lBackward()

    def spinLeft(self):
        self.rBackward()
        self.lFoward()

    def stop(self):
        self.lStop()
        self.rStop()

    def cleanup(self):
        GPIO.cleanup()



if __name__ == '__main__':
    car = Car(IN3, IN4, ENB, IN1, IN2, ENA, 0, 1)
    car.moveForward()
