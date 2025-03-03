from time import sleep
from ulora import LoRa, ModemConfig
from test_board import show_text_oled, clear_oled, set_led, test_led, show
from config_lora import *
from test_lora import *

v = '0.9'

print(f'Lora server v{v}')

datos_recibidos = None
data_log = DATA_LOG
def save_data(data,filename):
    print(f'save2{filename}')
    with open(filename,"at") as f:
        f.write(data)

# Cuando se reciben datos lora se llama a esta función automáticamente 
def procesa_datos_recibidos(payload):
    global datos_recibidos
    set_led(True)
    clear_oled()
    datos_recibidos = payload
    show(f"From:{payload.header_from} To:{payload.header_to}", y=9)
    show(f"<{payload.message}", y=18)
    show(f"RSSI: {payload.rssi}", y=27)
    show(f"SNR: {payload.snr}", y=36)
    show(f"id:{payload.header_id}",y=45)
    show(f"flag:{payload.header_flags}",y=54)
    if data_log != None:
        msg=f'{payload.header_to},{payload.header_from},{payload.header_id},"{payload.message}",{payload.rssi},{payload.snr},{payload.header_flags}\n'
        save_data(msg,data_log)
    set_led(False)
    
def init_lora(address):
    # initialise radio
    # Lora(spi_sck, spi_mosi, spi_miso, interrupt, this_address, cs_pin, reset_pin=None, freq=868.0, tx_power=14,
    #   modem_config=ModemConfig.Bw125Cr45Sf128, receive_all=False, acks=False, crypto=None)
    lora = LoRa(RFM95_SPI_SCK,RFM95_SPI_MOSI,RFM95_SPI_MISO, RFM95_IRQ, address, RFM95_CS, reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True, receive_all=True)

    # set callback
    lora.on_recv = procesa_datos_recibidos

    # set to listen continuously
    lora.set_mode_rx()


def listen(direccion,data_file=None):
    global data_log
    data_log = data_file
#    init_lora(address)
    activa_servidor(procesa_datos_recibidos,direccion_servidor = direccion)
    contador = 0
    # loop and wait for data
    while True:
        try:

            if contador%50 == 0:
                if datos_recibidos == None:
                    clear_oled()                
                show(f'Listening {contador}')
            contador += 1
            sleep(10)        
        except Exception as e:
            show(str(e))
            exit()

