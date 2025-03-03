from machine import Pin, SPI
import time

class SX127x:
    # Registro de direcciones del SX127x
    REG_FIFO = 0x00
    REG_OP_MODE = 0x01
    REG_FRF_MSB = 0x06
    REG_FRF_MID = 0x07
    REG_FRF_LSB = 0x08
    REG_PA_CONFIG = 0x09
    REG_LNA = 0x0C
    REG_FIFO_ADDR_PTR = 0x0D
    REG_FIFO_TX_BASE_ADDR = 0x0E
    REG_FIFO_RX_BASE_ADDR = 0x0F
    REG_FIFO_RX_CURRENT_ADDR = 0x10
    REG_IRQ_FLAGS = 0x12
    REG_RX_NB_BYTES = 0x13
    REG_PKT_SNR_VALUE = 0x19
    REG_PKT_RSSI_VALUE = 0x1A
    REG_MODEM_CONFIG_1 = 0x1D
    REG_MODEM_CONFIG_2 = 0x1E
    REG_PAYLOAD_LENGTH = 0x22
    REG_MAX_PAYLOAD_LENGTH = 0x23
    REG_MODEM_CONFIG_3 = 0x26
    REG_VERSION = 0x42

    # Modos
    MODE_LONG_RANGE_MODE = 0x80
    MODE_SLEEP = 0x00
    MODE_STDBY = 0x01
    MODE_TX = 0x03
    MODE_RX_CONTINUOUS = 0x05

    def __init__(self, freq=868.0):
        # Configuración específica para TTGO LoRa V1.6
        self.spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(27), miso=Pin(19))
        self.cs = Pin(18, Pin.OUT)  # NSS
        self.reset = Pin(23, Pin.OUT)  # RST en TTGO LoRa V1.6
        self.dio0 = Pin(26, Pin.IN)   # DIO0
        self.freq = freq

        # Inicializar pines
        self.cs.value(1)
        self.reset.value(1)
        
        # Reset del módulo
        self.reset.value(0)
        time.sleep(0.01)
        self.reset.value(1)
        time.sleep(0.01)

        # Verificar versión del chip
        version = self.read_register(self.REG_VERSION)
        if version != 0x12:
            raise Exception("Versión del chip SX127x no detectada")

        # Configurar modo LoRa
        self.write_register(self.REG_OP_MODE, self.MODE_LONG_RANGE_MODE | self.MODE_SLEEP)
        time.sleep(0.01)

        # Configurar frecuencia
        frf = int((freq * 1000000.0) / 61.03515625)
        self.write_register(self.REG_FRF_MSB, (frf >> 16) & 0xFF)
        self.write_register(self.REG_FRF_MID, (frf >> 8) & 0xFF)
        self.write_register(self.REG_FRF_LSB, frf & 0xFF)

        # Configurar potencia y ancho de banda
        self.write_register(self.REG_PA_CONFIG, 0x8F)  # Máxima potencia
        self.write_register(self.REG_MODEM_CONFIG_1, 0x72)  # BW=125kHz, CR=4/5
        self.write_register(self.REG_MODEM_CONFIG_2, 0x74)  # SF=7, CRC activado
        self.write_register(self.REG_MODEM_CONFIG_3, 0x04)  # LNA automática

        # Configurar buffers
        self.write_register(self.REG_FIFO_TX_BASE_ADDR, 0x00)
        self.write_register(self.REG_FIFO_RX_BASE_ADDR, 0x00)

        # Poner en standby
        self.write_register(self.REG_OP_MODE, self.MODE_LONG_RANGE_MODE | self.MODE_STDBY)

    def write_register(self, reg, value):
        self.cs.value(0)
        self.spi.write(bytes([reg | 0x80]))  # Escritura
        self.spi.write(bytes([value]))
        self.cs.value(1)

    def read_register(self, reg):
        self.cs.value(0)
        self.spi.write(bytes([reg & 0x7F]))  # Lectura
        value = self.spi.read(1)[0]
        self.cs.value(1)
        return value

    def send(self, data):
        self.write_register(self.REG_OP_MODE, self.MODE_LONG_RANGE_MODE | self.MODE_STDBY)
        self.write_register(self.REG_FIFO_ADDR_PTR, 0x00)
        self.write_register(self.REG_PAYLOAD_LENGTH, len(data))

        # Escribir datos en el FIFO
        self.cs.value(0)
        self.spi.write(bytes([self.REG_FIFO | 0x80]))
        self.spi.write(data)
        self.cs.value(1)

        # Iniciar transmisión
        self.write_register(self.REG_OP_MODE, self.MODE_LONG_RANGE_MODE | self.MODE_TX)
        while self.read_register(self.REG_IRQ_FLAGS) & 0x08 == 0:  # Esperar TxDone
            time.sleep(0.001)
        self.write_register(self.REG_IRQ_FLAGS, 0x08)  # Limpiar bandera
        self.write_register(self.REG_OP_MODE, self.MODE_LONG_RANGE_MODE | self.MODE_STDBY)