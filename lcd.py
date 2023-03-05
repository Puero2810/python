import I2C_LCD_driver
from time import *

def nombre(nombre):
    mylcd = I2C_LCD_driver.lcd()
    mylcd.lcd_display_string(nombre, 1)
    sleep(10)