# test_lora
from ulora import LoRa, ModemConfig
from config_lora import *
from test_board import show, set_led

v = 0.9

print(f'Lora client Test v{v}')

lora = None
mi_direccion = -1 
def init_lora(direccion = CLIENT_ADDRESS):
    global lora, mi_direccion
    mi_direccion = direccion
    if lora == None:
         lora = LoRa(RFM95_SPI_SCK,RFM95_SPI_MOSI,RFM95_SPI_MISO, RFM95_IRQ, mi_direccion, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True, receive_all=False)

def envia_mensaje_lora(mensaje, destino=SERVER_ADDRESS,y=0):
    global lora
    set_led(True)
    if lora == None:
        init_lora()
    lora.send_to_wait(mensaje, destino)
    show(f'{mi_direccion}>"{mensaje}">{destino}',y)
    set_led(False)
    
def activa_servidor(funcion_para_procesar_datos_recibidos,direccion_servidor = SERVER_ADDRESS):
    global lora
    if lora == None:
        init_lora(direccion=direccion_servidor)
    lora.on_recv = funcion_para_procesar_datos_recibidos
    lora.set_mode_rx() # se activa la escucha