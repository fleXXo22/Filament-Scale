import hx711, digitalio
import machine
import network as nw
import requests as rq
from time import sleep
from pn532_i2c import PN532_I2C

# Initialize I2C
i2c = I2C(1, scl=Pin(22), sda=Pin(21))
pn532 = PN532_I2C(i2c, debug=False)

pn532.SAM_configuration()




#Pins
#Buttons
Button1 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
Button2 = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

#NFC_Reader
I2C_scl = machine.Pin(22)
I2C_sda = machine.Pin(21)
i2c = machine.I2C(1, I2C_scl, I2C_sda)


#Scale
SPI_clk = machine.Pin(4, Pin.IN, pull=machine.Pin.PULL_DOWN)
SPI_data = machine.Pin(16, machine.Pin.OUT)

#general info
#User Settings
READ_NFC_TIMEOUT = 30 #timeout for NFC detection


#Spoolman info
SURL = "192.168.100.45:"

#WIFI info
SSID = "SSID"
PASSWORD = "Password"

#initialize variables
wlan = nw.WLAN()
pn532 = PN532_I2C(i2c, debug=False)


def interrupt():
    machine.soft_reset()

def connect_to_wifi():
    wlan = nw.WLAN()
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

def mode_updateWeight():
    nfc_id = get_NFC_id()
    if nfc_id != False:

        pass



def get_NFC_id():
    try:
        nfc_id = pn532.read_passive_target(timeout=READ_NFC_TIMEOUT) #read the NFC ID
        if nfc_id:
            print("Found NFC tag with UID:", [hex(i) for i in nfc_id])
            print(nfc_id.hex())
            return nfc_id.hex()
    except:
        return False




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


## Spoolman functions

def do_API_get_call(argument):
    api_call = f"{SURL}{argument}"
    response = requests.get(api_call)
    return response.json()
    

def get_Spool_id(nfc_id):
    self.nfc_id = nfc_id
    spool_id = do_API_call(f"/spool?lot_nr={nfc_id}")

#machine interrupts
Button1.irq(trigger=machine.Pin.IRQ_Falling, handler=interrupt)
Button2.irq(trigger=machine.Pin.IRQ_Falling, handler=interrupt)


pn532.SAM_configuration()
main_loop()