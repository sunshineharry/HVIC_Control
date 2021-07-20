'''
Date: 2021-07-07 12:19:16
LastEditors: Jiang Hankun
LastEditTime: 2021-07-09 16:46:26
'''
# -*- coding:utf-8 -*-

import time
import datetime
import threading
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

from .global_var import globalvar as gl




class OLED(threading.Thread):
    def __init__(self, pin=27) -> None:
        super().__init__()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        width = 128
        height = 64

        # First define some constants to allow easy resizing of shapes.
        padding = 0
        self.top = padding
        self.bottom = height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0

        serial = i2c(port=1, address=0x3c)
        self.device = ssd1306(serial, rotate=2)  # sh1106
      
    
    def run(self):
        while True:
            # print(gl.get_value('illuminance'))
            now = datetime.datetime.now()
            today_date = now.strftime("%Y/%m/%d")
            today_time = now.strftime("%H:%M:%S")

            with canvas(self.device) as draw:
                draw.text((self.x, self.top), today_date, fill=255)
                draw.text((self.x+75, self.top), today_time, fill=255)

                # device.clear()
                draw.text((self.x, self.top + 13), "illumin: " +
                        f"{gl.get_value('illuminance'):.2f}" + " Lx", fill=255)
                draw.text((self.x, self.top+23), "humid:   " +
                        f"{gl.get_value('humidity'):.2f}" + " %", fill=255)
                draw.text((self.x, self.top+33), "tempera: " +
                        f"{gl.get_value('temperature'):.2f}" + " °C", fill=255)
                draw.text((self.x, self.top+43), "prea_in: " +
                        f"{int(gl.get_value('preasure_1')):.2f}" + " Pa", fill=255)
                draw.text((self.x, self.top+53), "prea_out:" +
                        f"{int(gl.get_value('preasure_2')):.2f}" + " Pa", fill=255)                        
                # print('pressure_1 = ',gl.get_value('pressure_1'))
                # print('temperature = ',gl.get_value('temperature'))
                # draw.text((self.x, self.top+65), "prea_2: " +
                #         f"{gl.get_value('preasure_2'):.2f}" + " Pa", fill=255)

            time.sleep(0.1)


if __name__ == "__main__":
    oled = OLED()
    oled.start()
