from sx127x import SX127x
import time
import ubinascii

class LoRa:
    LORAWAN = 1
    EU868 = 1

    def __init__(self, sx127x):
        self.sx127x = sx127x
        self.dev_addr = None
        self.nwk_skey = None
        self.app_skey = None

    def init(self, mode, region, device_address, network_key, app_key):
        if mode != self.LORAWAN or region != self.EU868:
            raise Exception("Solo se soporta LoRaWAN en EU868 por ahora")
        self.dev_addr = device_address
        self.nwk_skey = network_key
        self.app_skey = app_key

    def send(self, payload, fcnt, port=1):
        # Construir trama LoRaWAN básica (MHDR + DevAddr + FCtrl + FCnt + Port + Payload)
        mhdr = bytes([0x40])  # Unconfirmed Data Up
        fctrl = bytes([0x00])  # Sin opciones adicionales
        fcnt_bytes = fcnt.to_bytes(2, 'little')  # Contador de 16 bits

        frame = mhdr + self.dev_addr + fctrl + fcnt_bytes + bytes([port]) + payload

        # Calcular MIC (simplificado para ABP con Frame Counter Checks desactivado)
        mic = self._calculate_mic(frame)
        frame += mic

        # Enviar la trama
        self.sx127x.send(frame)

    def _calculate_mic(self, frame):
        # Simplificación: MIC dummy, ajustar con AES-CMAC si es necesario
        return bytes([0x00, 0x00, 0x00, 0x00])