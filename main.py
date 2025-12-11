import hx711, digitalio
import machine,json, time
import network as nw
import requests as rq
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
SCALE_SCALE = 425 #adjust to fit your scale

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
Scale = hx711.HX711(SPI_clk, SPI_data)


def interrupt():
    machine.soft_reset()

def connect_to_wifi():
    wlan = nw.WLAN()
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

def mode_updateWeight():
    nfc_id = get_NFC_id()
    try:
        spool_id = get_Spool_id(nfc_id)
        weight = get_remaining_weight(spool_id)
        set_spool_weight(weight, spool_id)

    except:
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


def get_weight():

    new_value = 10000
    old_value = 20000
    while (new_value/old_value < 0.999) or (new_value/old_value > 1.001):
        old_value = new_value
        new_value = Scale.get_units()
    return new_value

def get_remaining_weight(spool_id, measured_weight):
    spool_weight = do_API_get_call(f"/spool/{spool_id}")
    spool_weight.json()
    spool_weight = spool_weight[0]["spool_weight"]
    remaining_weight = measured_weight - spool_weight
    return remaining_weight

def prepare_scale():
    Scale.set_scale(SCALE_SCALE)
    time.sleep(5)
    Scale.tare(5)

def get_Spool_id(nfc_id):
    self.nfc_id = nfc_id
    spool_id = do_API_get_call(f"/spool?lot_nr={nfc_id}")
    return spool_id

def set_Spool_weight(spool_id, weight):
    patch = {"remaining_weight":weight}
    do_API_patch_call(f"/spool/{spool_id}", patch_argument)

## Spoolman API Interaction

def do_API_get_call(argument):
    api_call = f"{SURL}/api/v1{argument}"
    response = rq.get(api_call)
    return response.json()
def do_API_patch_call(argument, patch_argument):
    api_call = f"{SURL}{argument}"
    response = requests.patch(api_call, json=patch_argument)
    return response.json()
    




#machine interrupts
Button1.irq(trigger=machine.Pin.IRQ_Falling, handler=interrupt)
Button2.irq(trigger=machine.Pin.IRQ_Falling, handler=interrupt)


pn532.SAM_configuration()
prepare_scale()
main_loop()