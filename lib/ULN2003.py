'''
Date: 2021-07-07 23:57:38
LastEditors: Jiang Hankun
LastEditTime: 2021-07-18 16:36:46
'''
import RPi.GPIO as GPIO
import time
import threading
from .global_var import globalvar as gl

"""
步进电机，用于控制窗帘
"""

# delay=2 #delay 2ms

# 控制步进电机的引脚
# pin_phase_1 = 6
# pin_phase_2 = 13
# pin_phase_3 = 19
# pin_phase_4 = 26

class ULN2003(threading.Thread):
    def __init__(self, pin_phase_1 = 6, pin_phase_2 = 13, pin_phase_3 = 19, pin_phase_4 = 26) -> None:
        super().__init__()
        self.event = threading.Event()
        self.method = None
        self.pin_phase_1 = pin_phase_1
        self.pin_phase_2 = pin_phase_2
        self.pin_phase_3 = pin_phase_3
        self.pin_phase_4 = pin_phase_4

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # 设置引脚的编码方式
        GPIO.setup(pin_phase_1, GPIO.OUT)
        GPIO.setup(pin_phase_2, GPIO.OUT)
        GPIO.setup(pin_phase_3, GPIO.OUT)
        GPIO.setup(pin_phase_4, GPIO.OUT)

    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.pin_phase_1, w1)
        GPIO.output(self.pin_phase_2, w2)
        GPIO.output(self.pin_phase_3, w3)
        GPIO.output(self.pin_phase_4, w4)

    def __forward_step(self, delay):
        delay = delay/1000.0
        self.setStep(1, 0, 0, 0)
        self.event.wait(delay)
        self.setStep(0, 1, 0, 0)
        self.event.wait(delay)
        self.setStep(0, 0, 1, 0)
        self.event.wait(delay)
        self.setStep(0, 0, 0, 1)
        self.event.wait(delay)

    def __backward_step(self, delay):
        delay = delay/1000.0
        self.setStep(0, 0, 0, 1)
        self.event.wait(delay)
        self.setStep(0, 0, 1, 0)
        self.event.wait(delay)
        self.setStep(0, 1, 0, 0)
        self.event.wait(delay)
        self.setStep(1, 0, 0, 0)
        self.event.wait(delay)

    def forward(self, circle_time = 600, delay = 4):
        for i in range(circle_time):
            # print("\n------\ni= ",i)
            self.__forward_step(delay) 

    def backward(self, circle_time = 600, delay = 4):
        for i in range(circle_time):
            # print("\n------\ni= ",i)
            self.__backward_step(delay)
    
    # def run(self):
    #     self.method = gl.get_value('method')
    #     if self.method=='forward':
    #         self.__forward()
    #         self.method = None
    #     if self.method=="backward":
    #         self.__backward()
    #         self.method = None