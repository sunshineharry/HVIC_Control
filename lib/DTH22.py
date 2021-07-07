'''
Date: 2021-07-06 00:26:47
LastEditors: Jiang Hankun
LastEditTime: 2021-07-07 15:22:10
'''


"""
注意事项：
    需要安装Adafruit_DHT（参考：https://blog.csdn.net/qq_19961917/article/details/82888111）
    这个库不识别4B+，需要改驱动代码（参考：https://blog.csdn.net/Elleryer/article/details/108482087）
        1. 安装Adafruit_DHT==1.3.4
        2. cd /home/pi/.local/lib/python3.7/site-packages/Adafruit_DHT/
        3. 打开 platform_detect.py 文件
        4. 参考教程补充代码
"""

import time
import threading
import Adafruit_DHT
from .global_var import globalvar as gl

class DTH22(threading.Thread):
    """DTH22温湿度检测模块"""
    # 注意，两次获取温湿度值之前间隔3s

    def __init__(self, pin=5) -> None:
        super().__init__()
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin

    def read_data(self) -> tuple:
        """读取温湿度数据

        Returns
        -------
        tuple
            返回值为（湿度，温度）
        """
        try:
            #读取温湿度数据到temp和hu两个变量中
            hu, temp = Adafruit_DHT.read_retry(self.sensor, self.pin)
            #打印出结果
            return hu, temp
        except RuntimeError as e:
            print("error\n{0}".format(e))
            return None
        except:
            print("error\nFailed to read sensor data!")
            return None

    def run(self):
        while True:
            humidity,temperature = self.read_data()
            gl.set_value('humidity', humidity)
            gl.set_value('temperature', temperature)
            # print('humidity = ',humidity,' %\ttemperature = ',temperature,' °C')
            time.sleep(1)


if __name__ == "__main__":
    sensor_DTH22 = DTH22(pin=5)
    sensor_DTH22.start()