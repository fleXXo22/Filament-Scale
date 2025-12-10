import hx711, digitalio, adafruit_pn532
import machine
import network as nw
import requests as rq
from time import sleep




#Pins
#Buttons
Button1 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
Button2 = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

#NFC_Reader
I2C_scl = machine.Pin(22)
I2C_sda = machine.Pin(21)

#Scale
SPI_clk = machine.Pin(4, Pin.IN, pull=machine.Pin.PULL_DOWN)
SPI_data = machine.Pin(16, machine.Pin.OUT)

#general info
#Spoolman info
SURL = "192.168.100.45:"

#WIFI info
SSID = "SSID"
PASSWORD = "Password"

#initialize variables
wlan = nw.WLAN()


def interrupt():
    machine.soft_reset()

def connect_to_wifi():
    wlan = nw.WLAN()
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

def mode_updateWeight():

    pass

def mode_addSpool():
    pass

def mode_read_NFC():
    pass

def main_loop():
    while True:
        if not wlan.isconnected():
            connect_to_wifi()
        if Button1.value() == 1:
            mode_updateWeight()
        elif Button2.value() == 1:
            mode_addSpool()
        else:
            pass



#machine interrupts
Button1.irq(trigger=machine.Pin.IRQ_Falling, handler=interrupt)
Button2.irq(trigger=machine.Pin.IRQ_Falling, handler=interrupt)

main_loop()