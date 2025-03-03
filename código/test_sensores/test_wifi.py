# test_wifi

from utime import sleep
from network import WLAN,STA_IF
from machine import reset

v = 0.9

print(f'test_wifi v{v}')

def init_wifi(ssid,wifi_passwd):
    
    w = WLAN(STA_IF)

    if not w.active():
        w.active(True)
    try:
        print('Conectando a',ssid)
        w.connect(ssid, wifi_passwd)
    except OSError as oes:
        print('Error interno:',oes)
        print('El dispositivo se reseteará en 5 segundos')
        sleep(5)
        print('Reseteando!!')
        reset()
        
    while not w.isconnected():
        print('.',end='')
        sleep(1)
        
    return w.ifconfig()[0]

