# test_lora
from ulora import LoRa, ModemConfig
from config_lora import *

v = 0.8

print(f'Lora client Test v{v}')

lora = None
mi_direccion = -1 
def init_lora(direccion_cliente = CLIENT_ADDRESS):
    global lora
    mi_direccion = direccion_cliente
    if lora == None:
         lora = LoRa(RFM95_SPI_SCK,RFM95_SPI_MOSI,RFM95_SPI_MISO, RFM95_IRQ, direccion_cliente, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True, receive_all=False)

def envia_lora(mensaje, destino=SERVER_ADDRESS,y=0):
    lora.send_to_wait(mensaje, destino)
    show(f'{mi_direccion}>"{mensaje}">{destino}',y)