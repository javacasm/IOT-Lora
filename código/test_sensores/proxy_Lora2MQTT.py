from time import sleep
from ulora import LoRa, ModemConfig
from test_board import show_text_oled, clear_oled, set_led, test_led, show
from config_lora import *
from test_lora import *
import umqttsimple
import ubinascii
import machine
import time
import json
from test_wifi import init_wifi

v = '0.9.2'

print(f'Proxy Lora2MQTT v{v}')

datos_recibidos = None
data_log = DATA_LOG
def save_data(data,filename):
    print(f'save2{filename}')
    with open(filename,"at") as f:
        f.write(data)

client_id = ubinascii.hexlify(machine.unique_id())

client = None

def init_MQTT():
    global client
    if client == None:
        client = umqttsimple.MQTTClient(client_id, BROKER_MQTT, port = PUERTO_MQTT)
        #client.set_callback(comprueba_mensajes)
        try:
            client.connect()  # conectamos con el servidor

        except umqttsimple.MQTTException as me: # https://www.vtscada.com/help/Content/D_Tags/D_MQTT_ErrMsg.htm
            print(get_error_MQTT(me))
            #print('Reseteando dispositivo en 10 segundos. Ctrl+C para detener')
            #time.sleep(10)
            #machine.reset()
        except Exception as e:
            print(f'Error conectando (ex): {e}')
            #print('Reseteando dispositivo en 10 segundos. Ctrl+C para detener')     
            #time.sleep(10)
            #machine.reset()
            


def publish_MQTT(base_topic,medidas):
    init_MQTT()
    
    try:
        y=0
        clear_oled()
        #show(msgTime)
        #y += 9
        for magnitud,medida in medidas.items():
            topic = base_topic + magnitud
            client.publish(topic, str(medida))
            show( f'pub {magnitud} - {medida}',y)
            y += 9 # pasamos a la siguiente línea
    except Exception as e:
        print(f'Error publicando: {e}')

# Cuando se reciben datos lora se llama a esta función automáticamente 
def procesa_paquetes_lora(payload):
    global datos_recibidos
    set_led(True)
    clear_oled()
    datos_recibidos = payload
    show(f"From:{payload.header_from} To:{payload.header_to}", y=9)
    show(f"<{payload.message}", y=18)
    try:
        datos_sensores = json.loads(payload.message)
        CLIENT_ID_STR = 'CLIENTE_'+str(payload.header_from)
        base_topic = b'/'+CLIENT_ID_STR+'/'  # topic base

        publish_MQTT(base_topic, datos_sensores)
    except Exception as e:
        print(f'Error {e} de formato: {payload.message}')
    if data_log != None:
        msg=f'{payload.header_to},{payload.header_from},{payload.header_id},"{payload.message}",{payload.rssi},{payload.snr},{payload.header_flags}\n'
        save_data(msg,data_log)
    set_led(False)
    

def proxy(direccion,data_file=None):
    global data_log
    data_log = data_file
#    init_lora(address)
    activa_servidor(procesa_paquetes_lora,direccion_servidor = direccion)
    contador = 0
    # loop and wait for data
    while True:
        try:

            if contador%10 == 0:
                if datos_recibidos == None:
                    clear_oled()                
                show(f'Listening {contador}')
            contador += 1
            sleep(1)        
        except Exception as e:
            show(str(e))
            exit()

