'''
Date: 2021-07-09 15:39:46
LastEditors: Jiang Hankun
LastEditTime: 2021-07-09 16:43:00
'''
from RPi import GPIO


class LEDs(object):

    def __init__(self, pin_LED=22) -> None:
        super().__init__()
        self.pin_LED = pin_LED

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_LED, GPIO.OUT)

        # GPIO.output(self.pin_LED, GPIO.HIGH)
        self.off()

    def off(self):
        GPIO.output(self.pin_LED, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin_LED, GPIO.HIGH)

    def __del__(self):
        self.off()


if __name__ == "__main__":
    import time
    leds = LEDs()
    while True:
        leds.off()
        time.sleep(1)
        leds.on()
        time.sleep(1)

