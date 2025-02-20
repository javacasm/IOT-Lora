from test_wifi import init_wifi
from test_board import show, test_led, clear_oled, init_SD
from server import listen
#from client import test_Lora_client
from config_lora import *
data_log = DATA_LOG
try:
    show('Init sd',0)
    init_SD(SD)
    data_log = SD+"/" + DATA_LOG
    clear_oled()
    show('SD Ok',0)
except Exception as e:
    clear_oled()
    show("SD error")
    print(e)
    
show(f'wifi:{SSID}',y=9)
show(f'IP:{init_wifi(SSID,WIFI_PASSWD)}',y=18)
test_led()
listen(SERVER_ADDRESS,data_log)
#test_Lora_client(CLIENT_ADDRESS + 1,SERVER_ADDRESS,espera=1)