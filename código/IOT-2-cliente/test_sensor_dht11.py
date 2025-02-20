from machine import Pin
from dht import DHT11
from time import sleep
sensor = DHT11(Pin(14)) # configuración

def mide_humedad_temperatura():
    sensor.measure()
    temperatura_medida = sensor.temperature()
    humedad_medida = sensor.humidity()
    return temperatura_medida, humedad_medida
while True:
    temperatura,humedad = mide_humedad_temperatura()
    print('Humedad: ', humedad)
    print('Temperatura: ',temperatura)
    sleep(2)  # 2 segundos