# test_sensores
from machine import Pin, SoftI2C
from dht import DHT11
from BME280 import BME280
from time import sleep
from test_board import show, clear_oled
from config_lora import DHT_PIN,BME_I2C_SCL,BME_I2C_SDA,BME_ADDRESS,SERVER_ADDRESS
from test_lora import envia_mensaje_lora
import json

v = '0.9.2'
print(f'test_sensores v{v}')

sensorDHT = None
sensorBME280 = None
i2c_BME = None

def init_DHT():
    global sensorDHT
    if sensorDHT == None:
        sensorDHT = DHT11(Pin(DHT_PIN)) # configuración

def lee_sensor_DHT():
    init_DHT()
    sensorDHT.measure()
    temperatura_medida = sensorDHT.temperature()
    humedad_medida = sensorDHT.humidity()
    return {'T_dht':temperatura_medida, 'H_dht':humedad_medida}

def init_BME280():
    global i2c_BME, sensorBME280
    if i2c_BME == None:
        i2c_BME = SoftI2C(scl=Pin(BME_I2C_SCL), sda=Pin(BME_I2C_SDA))
        dispositivos_I2C_BME =i2c_BME.scan() 
        print('i2c_BME.scan:',dispositivos_I2C_BME)
        if BME_ADDRESS not in dispositivos_I2C_BME:
            print(f'ERROR: no se encuentra el dispositivo con dirección {BME_ADDRESS}')
    if sensorBME280 == None:
        sensorBME280 = BME280(i2c=i2c_BME,address=BME_ADDRESS)

def lee_sensor_bme280():
    init_BME280()
    temp = sensorBME280.temperature_number
    hum = sensorBME280.humidity_number
    pres = sensorBME280.pressure_number        
    return {'T_bme':temp,'H_bme':hum,'P_bme':pres}

def lee_sensor_prueba():
    from random import randint
    return {'T_prueba':randint(15,30),'H_prueba':randint(45,80),'P_prueba':randint(950,1100)}

def get_medidas_sensores():
        medidas = {}
        
        try:
            medidas_sensor_bme = lee_sensor_bme280()
            medidas.update(medidas_sensor_bme) # añade las medidas
        except :
            print('ERROR sensor BME')
        '''
        try:
            medidas_sensor_dht = lee_sensor_DHT()
            medidas.update(medidas_sensor_dht) # añade las medidas
        except :
            print('ERROR sensor DHT')
        '''
        return medidas

def envia_medidas_lora(medidas):
        msg_lora = ''
        y = 0
        clear_oled()
        for magnitud,medida in medidas.items():
            mensaje = f'{magnitud}:{medida}'
        
            show(mensaje,y)
            y += 9 # pasamos a la siguiente línea
            msg_lora+=mensaje +' '
        envia_mensaje_lora(json.dumps(medidas),y=y)    

def test_sensores(espera = 10):

    while True:
        try:
            medidas = get_medidas_sensores()
            envia_medidas_lora(medidas)
        except  Exception as e:
            show(f'Error {e}')
        sleep(espera)  
