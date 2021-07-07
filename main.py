'''
Date: 2021-07-07 12:19:16
LastEditors: Jiang Hankun
LastEditTime: 2021-07-07 17:43:42
'''
# -*- coding:utf-8 -*-
from lib import OLED, BH1750FVI, DTH22, BMP180_2
from lib.global_var import globalvar as gl
gl._init()

if __name__ == "__main__":
    # 实例化对象
    sensor_DTH22 = DTH22(pin=5)
    sensor_BH1750 = BH1750FVI()
    sensor_BMP180_2 = BMP180_2()
    oled = OLED()
    
    # 开始多线程运行
    sensor_DTH22.start()
    sensor_BH1750.start()
    sensor_BMP180_2.start()
    oled.start()
    

