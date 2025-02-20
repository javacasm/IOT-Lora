from utime import sleep
from network import WLAN,STA_IF


def init_wifi(ssid,wifi_passwd):
    
    w = WLAN(STA_IF)

    if not w.active():
        w.active(True)

    w.connect(ssid, wifi_passwd)
    while not w.isconnected():
        print('.',end='')
        sleep(1)
        
    return w.ifconfig()[0]
