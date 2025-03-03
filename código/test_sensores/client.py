# client
from time import sleep
from ulora import LoRa, ModemConfig
from test_board import show_text_oled, clear_oled, set_led, show
from config_lora import *
from test_lora import envia_mensaje_lora, init_lora

v = 0.9

print(f'Lora client Test v{v}')


def test_Lora_client(direccion_cliente,direccion_servidor=SERVER_ADDRESS, espera=10):
    init_lora(direccion = direccion_cliente)
    contador = 0
    # loop and send data
    while True:
        mensaje = f'Test {contador}'
        set_led(True) # enciendo el led de la placa
        clear_oled() # borro la pantalla
        envia_mensaje_lora(mensaje, direccion_servidor)
        contador += 1
        set_led(False) # apago el led de la placa
        sleep(espera)
