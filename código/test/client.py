from time import sleep
from ulora import LoRa, ModemConfig
from test_board import show_text_oled, clear_oled
from config_lora import *

# Lora(spi_sck, spi_mosi, spi_miso, interrupt, this_address, cs_pin, reset_pin=None, freq=868.0, tx_power=14,
#   modem_config=ModemConfig.Bw125Cr45Sf128, receive_all=False, acks=False, crypto=None)
lora = LoRa(RFM95_SPI_SCK,RFM95_SPI_MOSI,RFM95_SPI_MISO, RFM95_IRQ, CLIENT_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True, receive_all=True)

def show(text):
    print(text)
    show_text_oled(text,0,0)

contador = 0
# loop and send data
while True:
    msg = f'Test {contador}'
    lora.send_to_wait(msg, SERVER_ADDRESS)
    clear_oled()
    show(f'"{msg}">{SERVER_ADDRESS}')
    contador += 1
    sleep(10)
