'''
Date: 2021-07-06 00:26:47
LastEditors: Jiang Hankun
LastEditTime: 2021-07-06 00:31:42
'''

"""
注意事项：
    需要安装Adafruit_DHT（参考https://blog.csdn.net/qq_19961917/article/details/82888111）
"""

import Adafruit_DHT

class DTH22(object):
    """DTH22温湿度检测模块"""

    def __init__(self, pin=27) -> None:
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
            return (hu,temp)
            #循环延迟设为3秒
        except RuntimeError as e:
            print("error\n{0}".format(e))
            return None
        except:
            print("error\nFailed to read sensor data!")
            return None