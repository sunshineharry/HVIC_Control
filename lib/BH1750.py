'''
Date: 2021-07-06 00:45:47
LastEditors: Jiang Hankun
LastEditTime: 2021-07-09 15:59:48
'''

"""
    注意事项：需要开启I2C，安装python-smbus
"""

import smbus
import time
import threading
from .global_var import globalvar as gl

class BH1750FVI(threading.Thread):
    """环境光照度传感器BH1750FVI"""

    def __init__(self) -> None:
        super().__init__()

        #BH1750地址
        self.__DEV_ADDR=0x23

        #控制字
        self.__CMD_PWR_OFF=0x00  #关机
        self.__CMD_PWR_ON=0x01   #开机
        self.__CMD_RESET=0x07    #重置
        self.__CMD_CHRES=0x10    #持续高分辨率检测
        self.__CMD_CHRES2=0x11   #持续高分辨率模式2检测
        self.__CMD_CLHRES=0x13   #持续低分辨率检测
        self.__CMD_THRES=0x20    #一次高分辨率
        self.__CMD_THRES2=0x21   #一次高分辨率模式2
        self.__CMD_TLRES=0x23    #一次分辨率
        self.__CMD_SEN100H=0x42  #灵敏度100%,高位
        self.__CMD_SEN100L=0X65  #灵敏度100%，低位
        self.__CMD_SEN50H=0x44   #50%
        self.__CMD_SEN50L=0x6A   #50%
        self.__CMD_SEN200H=0x41  #200%
        self.__CMD_SEN200L=0x73  #200%

        # 初始化
        self.bus=smbus.SMBus(0)
        self.bus.write_byte(self.__DEV_ADDR,self.__CMD_PWR_ON)
        self.bus.write_byte(self.__DEV_ADDR,self.__CMD_RESET)
        self.bus.write_byte(self.__DEV_ADDR,self.__CMD_SEN100H)
        self.bus.write_byte(self.__DEV_ADDR,self.__CMD_SEN100L)
        self.bus.write_byte(self.__DEV_ADDR,self.__CMD_PWR_OFF)


    def read_data(self) -> int:
        self.bus.write_byte(self.__DEV_ADDR,self.__CMD_PWR_ON)
        self.bus.write_byte(self.__DEV_ADDR,self.__CMD_THRES2)
        time.sleep(0.2)
        res = self.bus.read_word_data(self.__DEV_ADDR,0)
        # read_word_data
        res=((res>>8)&0xff)|(res<<8)&0xff00
        res=round(res/(2*1.2),2)
        return res

    def run(self) -> None:
        while True:
            gl.set_value('illuminance', self.read_data())
            # print(gl.get_value('illuminance'))
            time.sleep(3.1)



if __name__ == "__main__":
    sensor_BH1750FVI = BH1750FVI()
    sensor_BH1750FVI.start()