from time import sleep
from ulora import LoRa, ModemConfig
from test_board import show_text_oled, clear_oled, set_led, show
from config_lora import *

v = 0.8

print(f'Lora client Test v{v}')


def test_Lora_client(address,server_address=SERVER_ADDRESS, espera=10):
    # Lora(spi_sck, spi_mosi, spi_miso, interrupt, this_address, cs_pin, reset_pin=None, freq=868.0, tx_power=14,
    #   modem_config=ModemConfig.Bw125Cr45Sf128, receive_all=False, acks=False, crypto=None)
    lora = LoRa(RFM95_SPI_SCK,RFM95_SPI_MOSI,RFM95_SPI_MISO, RFM95_IRQ, address, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True, receive_all=True)
    
    contador = 0
    # loop and send data
    while True:
        msg = f'Test {contador}'
        set_led(True)
        lora.send_to_wait(msg, server_address)
        clear_oled()
        show(f'{address}>"{msg}">{server_address}')
        contador += 1
        set_led(False)
        sleep(espera)
