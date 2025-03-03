# test_sensores
from machine import Pin, SoftI2C
from dht import DHT11
from BME280 import BME280
from time import sleep
from test_board import show, clear_oled
from config_lora import DHT_PIN,BME_I2C_SCL,BME_I2C_SDA,SERVER_ADDRESS
from test_lora import envia_mensaje_lora


v = '0.9'
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
        print('i2c_BME.scan:',i2c_BME.scan())
    if sensorBME280 == None:
        sensorBME280 = BME280(i2c=i2c_BME,address=BME_ADDRESS)

def lee_sensor_bme280():
    init_BME280()
    temp = sensorBME280.temperature
    hum = sensorBME280.humidity
    pres = sensorBME280.pressure        
    return {'T_bme':temp,'H_bme':hum,'P_bme':pres}

def lee_sensor_prueba():
    from random import randint
    return {'T_prueba':randint(15,30),'H_prueba':randint(45,80),'P_prueba':randint(950,1100)}

def get_medidas_sensores():
        medidas = {}
        try:
            medidas_sensor_bme = lee_sensor_bme280()
            medidas.update(medidas_sensor_bme) # añade las medidas
        except Exception e:
            print(f'Error sensor bme: {e}')
        try:
            medidas_sensor_dht = lee_sensor_DHT()
            medidas.update(medidas_sensor_dht) # añade las medidas
        except Exception e:
            print(f'Error sensor dht: {e}')
    return medidas

def envia_medidas_lora(medidas):
        msg_lora = ''
        y = 0
        clear_oled()
        for magnitud,medida in medidas.items():
            mensaje = f'{magnitud}:{medida}'
            show(mensaje,y)
            msg_lora+=mensaje +' '
            y += 9 # pasamos a la siguiente línea
        envia_mensaje_lora(msg_lora,y=y)    

def test_sensores(espera = 10):

    while True:
        try:
            medidas = get_medidas_sensores()
            envia_medidas_lora(medidas)
        except  Exception as e:
            show(f'Error {e}')
        sleep(espera)  
