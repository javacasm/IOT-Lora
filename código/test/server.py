from time import sleep
from ulora import LoRa, ModemConfig
from test_board import show_text_oled, clear_oled
from config_lora import *

datos_recibidos = None

# This is our callback function that runs when a message is received
def on_recv(payload):
    global datos_recibidos
    clear_oled()
    datos_recibidos = payload
    show(f"From:{payload.header_from}",y=9)
    show(f"<{payload.message}",y=18)
    show(f"RSSI: {payload.rssi}",y=27)
    show(f"SNR: {payload.snr}",y=35)

# initialise radio
# Lora(spi_sck, spi_mosi, spi_miso, interrupt, this_address, cs_pin, reset_pin=None, freq=868.0, tx_power=14,
#   modem_config=ModemConfig.Bw125Cr45Sf128, receive_all=False, acks=False, crypto=None)
lora = LoRa(RFM95_SPI_SCK,RFM95_SPI_MOSI,RFM95_SPI_MISO, RFM95_IRQ, SERVER_ADDRESS, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True, receive_all=True)

# set callback
lora.on_recv = on_recv

# set to listen continuously
lora.set_mode_rx()

def show(text,y=0):
    print(text)
    show_text_oled(text,0,y)

contador = 0
# loop and wait for data
while True:
    try:
        if datos_recibidos == None:
            clear_oled()
        show(f'Listening {contador}')
        contador += 1
        sleep(1)        
    except Exception as e:
        show(str(e))
        exit()