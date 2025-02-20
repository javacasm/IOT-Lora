from test_wifi import init_wifi
from test_board import show,test_led
#from server import listen
from client import test_Lora_client
from config_lora import *

show(f'IP:{init_wifi(SSID,WIFI_PASSWD)}')
test_led()

#listen(SERVER_ADDRESS)
test_Lora_client(CLIENT_ADDRESS + 1,SERVER_ADDRESS,espera=15)