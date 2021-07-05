'''
Date: 2021-07-06 00:57:05
LastEditors: Jiang Hankun
LastEditTime: 2021-07-06 01:02:42
'''

import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import time

# def setup():
#     print '\n Barometer begins...'

# def loop():
#     while True:
#         sensor = BMP085.BMP085()
#         temp = sensor.read_temperature()    # Read temperature to veriable temp
#         pressure = sensor.read_pressure()   # Read pressure to veriable pressure

#         print ''
#         print '      Temperature = {0:0.2f} C'.format(temp)     # Print temperature保留小数点后两位
#         print '      Pressure = {0:0.2f} Pa'.format(pressure)   # Print pressure
#         #字符串中大括号和其中的字符会被替换成传入 str.format() 的参数。
#         #字段名后允许可选的 ':' 和格式指令。{0:0.2f}保留小数点后两位
#         time.sleep(1)           
#         print ''

# def destory():
#     GPIO.cleanup()              # Release resource

# if __name__ == '__main__':      # Program start from here
#     setup()
#     try:
#         loop()
#     except KeyboardInterrupt:   # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
#         destory()