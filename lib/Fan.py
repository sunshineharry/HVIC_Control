'''
Date: 2021-07-11 10:55:44
LastEditors: Jiang Hankun
LastEditTime: 2021-07-18 16:38:07
'''

from RPi import GPIO

class FAN(object):
    def __init__(self) -> None:
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([21,20], GPIO.OUT)
        GPIO.output(20,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)

    def on(self):
        GPIO.output(21,GPIO.HIGH)

    def off(self):
        GPIO.output(21,GPIO.LOW)

    def __del__(self):
        self.off()


if __name__ == "__main__":
    fan = FAN()
    import time
    while True:
        fan.on()
        time.sleep(5)
        fan.off()
        time.sleep(5)
