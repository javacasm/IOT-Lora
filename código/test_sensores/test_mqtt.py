import umqttsimple
import ubinascii
import machine
import time
from test_wifi import init_wifi
from test_board import set_led, show,clear_oled 
from test_sensores import get_medidas_sensores
from config_lora import CLIENT_ADDRESS, SSID, WIFI_PASSWD

v = '0.9.1'
print(f'test_MQTT v{v}')

BROKER_MQTT = '192.168.1.140' # raspy5.local
PUERTO_MQTT = 1883

show(f'IP:{init_wifi(SSID,WIFI_PASSWD)}')

client_id = ubinascii.hexlify(machine.unique_id())
CLIENT_ID_STR = 'CLIENTE_'+str(CLIENT_ADDRESS)
base_topic = b'/'+CLIENT_ID_STR+'/'  # topic base
topic_LED = b'/'+CLIENT_ID_STR+'/LED'
topic_errors = b'/errors'



def comprueba_mensajes(topic, msg):
    print(f'Topic:{topic} msg:{msg}')
    if topic == topic_LED:     # Check for Led Topic
        if msg == b'On':
            set_led(True)
            print('Led:On')
        elif msg == b'Off':
            set_led(False)
            print('Led:Off')
        else:
            print('Led mensaje desconocido: {msg}')
            
def getLocalTimeHumanFormat():
    strLocalTime = "{0}/{1:02}/{2:02} {3:02}:{4:02}:{5:02}".format(*time.localtime(time.time())[0:6])
    return strLocalTime

def get_error_MQTT(me):
    value = f'{me}'
    msg_error = f'Error conectando: {me}'
    if value == '5':
        msg_error =  'Error de autorizacion: {me} '
    elif value == '4':
        msg_error = 'Login error: {me}'
    return msg_error  

def publish_MQTT_forever(tiempo = 10):
    client = umqttsimple.MQTTClient(client_id, BROKER_MQTT, port = PUERTO_MQTT)
    client.set_callback(comprueba_mensajes)
    try:
        client.connect()  # conectamos con el servidor
        client.subscribe(topic_errors)
        print(f'Suscrito a {topic_errors}')
        client.subscribe(topic_LED)
        print(f'Suscrito a {topic_LED}')
    except umqttsimple.MQTTException as me: # https://www.vtscada.com/help/Content/D_Tags/D_MQTT_ErrMsg.htm
        print(get_error_MQTT(me))
        print('Reseteando dispositivo en 10 segundos. Ctrl+C para detener')
        time.sleep(10)
        machine.reset()
    except Exception as e:
        print(f'Error conectando (ex): {e}')
        print('Reseteando dispositivo en 10 segundos. Ctrl+C para detener')     
        time.sleep(10)
        machine.reset()

    tiempo_ultima_vez = 0 # utime.ticks_ms()
    while True :

        ahora = time.ticks_ms()
        diferencia_ms = time.ticks_diff(ahora, tiempo_ultima_vez)
        client.check_msg() # comprobamos si hay mensajes para nosotros
        
        if diferencia_ms > (tiempo * 1000):
            tiempo_ultima_vez = ahora
            msgTime = getLocalTimeHumanFormat()
            try:
                medidas = get_medidas_sensores()
                y=0
                clear_oled()
                show(msgTime)
                y += 9
                for magnitud,medida in medidas.items():
                    topic = base_topic + magnitud
                    client.publish(topic, str(medida))
                    show( f'pub {magnitud} - {medida}',y)
                    y += 9 # pasamos a la siguiente línea
            except Exception as e:
                print(f'Error publicando: {e}')
            
        time.sleep_ms(10)

