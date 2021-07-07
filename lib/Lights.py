from RPi import GPIO

class LEDs(object):
	def __init__(self, pin_LED_1=17, pin_LED_2=27, pin_LED_3=22) -> None:
		super().__init__()
		self.pin_LED_1 = pin_LED_1
		self.pin_LED_2 = pin_LED_2
		self.pin_LED_3 = pin_LED_3

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin_LED_1,GPIO.OUT)
		GPIO.setup(self.pin_LED_2, GPIO.OUT)
		GPIO.setup(self.pin_LED_3, GPIO.OUT)

		GPIO.output(self.pin_LED_1,GPIO.HIGH)
		GPIO.output(self.pin_LED_2, GPIO.HIGH)
		GPIO.output(self.pin_LED_3, GPIO.HIGH)
