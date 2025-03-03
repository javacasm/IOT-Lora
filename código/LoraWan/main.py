from sx127x import SX127x
from lora import LoRa
import time
import ubinascii
from config_ttn import *

# Inicializar el módulo RFM95 en TTGO LoRa V1.6
lora_module = SX127x(freq=868.0)  # Frecuencia para Europa

# Configuración LoRaWAN (reemplaza con tus claves de TTN)
dev_addr = ubinascii.unhexlify(DEV_ADDRESS)  # Device Address
nwk_skey = ubinascii.unhexlify(NWKSKEY)  # Network Session Key
app_skey = ubinascii.unhexlify(APPSKEY)  # App Session Key

# Inicializar LoRaWAN
lora = LoRa(lora_module)
lora.init(mode=LoRa.LORAWAN, region=LoRa.EU868, device_address=dev_addr, network_key=nwk_skey, app_key=app_skey)

# Contador de tramas
fcnt = 0

# Función para enviar datos
def send_data(payload):
    global fcnt
    lora.send(payload, fcnt, port=1)
    fcnt += 1
    print("Datos enviados:", payload)

# Bucle principal
while True:
    payload = "Hola TTN desde TTGO LoRa V1.6!"
    send_data(payload.encode())
    time.sleep(20)  # Espera 60 segundos entre envíos