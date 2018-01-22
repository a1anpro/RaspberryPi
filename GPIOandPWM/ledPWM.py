#coding:utf-8

import time
import RPi.GPIO as GPIO

LED=10

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

GPIO.setwarnings(False)

pwm = GPIO.PWM(LED, 70)  # 通道为 12 频率为 50Hz

pwm.start(0)
time.sleep(2)
try:
    while True:
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()