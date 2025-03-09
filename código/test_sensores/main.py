# main
from test_wifi import init_wifi
from test_board import show,test_led
#from server import listen
from client import test_Lora_client
from config_lora import *
from test_sensores import test_sensores
from test_mqtt import *
v = '0.9.2'

print(f'main v{v}')

show(f'IP:{init_wifi(SSID,WIFI_PASSWD)}')

#test_led()
#listen(SERVER_ADDRESS,'data.csv') # descomenta para que actúe como server
#test_Lora_client(CLIENT_ADDRESS,SERVER_ADDRESS,espera=2,payload_oversize=150) # descomenta para que sea cliente
test_sensores(espera = 5) # descomenta para prueba de sensores
#publish_forever()