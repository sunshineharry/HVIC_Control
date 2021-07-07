import RPi.GPIO as GPIO
import time

"""
步进电机，用于控制窗帘
"""

# delay=2 #delay 2ms

# 控制步进电机的引脚
# pin_phase_1 = 6
# pin_phase_2 = 13
# pin_phase_3 = 19
# pin_phase_4 = 26

class ULN2003(object):
    def __init__(self, pin_phase_1 = 6, pin_phase_2 = 13, pin_phase_3 = 19, pin_phase_4 = 26) -> None:
        super().__init__()
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

    def _setStep(self, w1, w2, w3, w4):
        GPIO.output(self.pin_phase_1, w1)
        GPIO.output(self.pin_phase_2, w2)
        GPIO.output(self.pin_phase_3, w3)
        GPIO.output(self.pin_phase_4, w4)

    def forward(self, delay):
        delay = delay/1000.0
        self._setStep(1, 0, 0, 0)
        time.sleep(delay)
        self._setStep(0, 1, 0, 0)
        time.sleep(delay)
        self._setStep(0, 0, 1, 0)
        time.sleep(delay)
        self._setStep(0, 0, 0, 1)
        time.sleep(delay)


if __name__ == "__main__":
    motor_ULN2003 = ULN2003()
    while True:
        motor_ULN2003.forward(2)
