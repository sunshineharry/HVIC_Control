'''
Date: 2021-07-07 12:19:16
LastEditors: Jiang Hankun
LastEditTime: 2021-07-20 09:59:55
'''

# 导入并初始化全集变量库
from serial.serialutil import Timeout
from lib.Fan import FAN
from lib.global_var import globalvar as gl
gl._init()

# 导入系统库
import threading, time, math, serial

# 导入其他模块
from lib import OLED, BH1750FVI, DTH22, BMP180_2, LEDs, ULN2003

lock = threading.RLock()

class GlobalLogicCtrl(threading.Thread):
    """全局逻辑控制"""
    def __init__(self) -> None:
        super().__init__()
        self.illuminance = gl.get_value('illuminance')  # 光照度
        self.humidity = gl.get_value('humidity')        # 湿度
        self.temperature = gl.get_value('temperature')  # 温度
        self.preasure_in = gl.get_value('preasure_1')   # 车厢内气压
        self.preasure_out = gl.get_value('preasure_2')  # 车厢外气压
        self.is_window_open = False
        self.leds = LEDs()
        self.uln2003 = ULN2003()
        self.fan = FAN()
        self.ser = serial.Serial("/dev/ttyS0", 9600 ,timeout=0.5)


    def __var_update(self):
        """更新成员变量"""
        print('开始更新变量：__var_update()')
        self.ser.write('开始更新变量：\n'.encode('gbk'))
        self.illuminance = gl.get_value('illuminance')  # 光照度
        self.humidity = gl.get_value('humidity')        # 湿度
        self.temperature = gl.get_value('temperature')  # 温度
        self.preasure_in = gl.get_value('preasure_1')   # 车厢内气压
        self.preasure_out = gl.get_value('preasure_2')  # 车厢外气压
        print("\tilluminance:",self.illuminance)
        self.ser.write(("\tilluminance:"+str(self.illuminance)+"\n").encode('gbk'))
        print("\thumidity:",self.humidity)
        self.ser.write(("\thumidity:"+str(self.humidity)+"\n").encode('gbk'))
        print("\ttemperature:",self.temperature)
        self.ser.write(("\ttemperature:"+str(self.temperature)+"\n").encode('gbk'))
        print("\tpreasure_in:",self.preasure_in)
        self.ser.write(("\tpreasure_in:"+str(self.preasure_in)+"\n").encode('gbk'))
        print("\tpreasure_out:",self.preasure_out)
        self.ser.write(("\tpreasure_out:"+str(self.preasure_out)+"\n").encode('gbk'))
        print('')
        self.ser.write("\n".encode('gbk'))

    def __fan_ctrl(self):
        """风扇控制
        1. 当体感温度高于31摄氏度时，打开风扇
        2. 当体感温度低于30摄氏度时，关闭风扇（两个地方阈值不一样，避免由于传感器的波动导致风扇频繁启停）
        """
        # TODO 由串口控制风扇的开启关闭

        print("风扇控制：\n")
        self.ser.write("风扇控制：\n".encode('gbk'))
        # 计算体感温度
        e = (self.humidity/100)*6.105*math.exp((17.27*self.temperature)/(237.7+self.temperature))
        apparent_temperature = 1.07*self.temperature + 0.2*e -2.7
        print("\t体感温度:",apparent_temperature)
        self.ser.write(("\t体感温度:"+str(apparent_temperature)+"\n").encode('gbk'))

        if apparent_temperature > 30:
            print('\tFan on')
            self.ser.write('\tFan on\n'.encode('gbk'))
            self.fan.on() 

        if apparent_temperature < 29.8:
            print('\tFan off')
            self.ser.write('\tFan off\n'.encode('gbk'))
            self.fan.off()

        print('')
        self.ser.write('\n'.encode('gbk'))

    def __lighting_crtl(self):
        """灯光控制
        1. 在光照不足（如进入隧道时，日落后）进行补光
        2. 在光照过强时关闭窗帘
        """
        # TODO 增加串口对光照的控制

        # 获取当前时间
        # hour = time.localtime(time.time()).tm_hour

        print("照明控制: ")
        self.ser.write('照明控制: \n'.encode('gbk'))
        print("\t窗户状态: ",self.is_window_open)
        self.ser.write(('\t窗户状态: '+str(self.is_window_open)+'\n').encode('gbk'))
        # 白天的控制逻辑
        if (self.illuminance < 90) and (self.is_window_open is False):
            print('\t开灯开窗')
            self.ser.write('\t开灯开窗\n'.encode('gbk'))
            self.leds.on()
            self.leds.on()
            gl.set_value('method', 'forward')
            # self.uln2003.set_methrd('forward')
            # self.uln2003.start()
            # self.uln2003.join()
            self.uln2003.forward()
            print('\t开灯开窗完成')
            self.ser.write('\t开灯开窗完成\n'.encode('gbk'))
            self.is_window_open = True

        if self.illuminance > 100 and self.is_window_open:
            print('\t关灯关窗')
            self.ser.write('\t关灯关窗\n'.encode('gbk'))
            self.leds.off()
            self.leds.off()
            gl.set_value('method', 'backward')
            # time.sleep(1)
            # lock.acquire()
            # self.uln2003.set_methrd('backward')
            # self.uln2003.start()
            # self.uln2003.join()
            # lock.release()
            self.uln2003.backward()
            print('\t关灯关窗完成')
            self.ser.write('\t关灯关窗完成\n'.encode('gbk'))
            self.is_window_open = False


    def run(self):
        while True:
            self.ser.write("\n".encode('gbk'))
            self.__var_update()
            if self.humidity is not None and self.illuminance is not None:
                self.__fan_ctrl()
                self.__lighting_crtl()
            time.sleep(2)


    def __del__(self):
        print('success')






if __name__ == "__main__":
    from RPi import GPIO
    # import msvcrt
    import sys
    GPIO.cleanup()
    # 实例化对象
    sensor_DTH22 = DTH22(pin=5)
    sensor_BH1750 = BH1750FVI()
    sensor_BMP180_2 = BMP180_2()
    oled = OLED()
    global_logic_ctrl = GlobalLogicCtrl()
    
    # 开始多线程运行
    
    sensor_DTH22.setDaemon(True)
    sensor_DTH22.start()
    
    sensor_BH1750.setDaemon(True)
    sensor_BH1750.start()
    
    sensor_BMP180_2.setDaemon(True)
    sensor_BMP180_2.start()
    
    oled.setDaemon(True)
    oled.start()
    
    global_logic_ctrl.setDaemon(True)
    global_logic_ctrl.start()

    while True:
        pass
