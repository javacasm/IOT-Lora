from machine import Pin, SoftI2C
from time import sleep
from BME280 import BME280
import ssd1306

i2c = SoftI2C(scl=Pin(15), sda=Pin(4))
print(i2c.scan())
pantalla = ssd1306.SSD1306_I2C(128,64,i2c)
bme = BME280(i2c=i2c,address=0x77)
while True:

    try:    
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        pantalla.fill(0) #borramos la pantalla
        print('Temperatura: ', temp)
        pantalla.text('T:',0,0,1) 
        pantalla.text(temp,20,0,1)
        print('Humedad: ', hum)
        pantalla.text('H:',0,9,1)
        pantalla.text(hum,20,9,1)
        print('Presión: ', pres)
        pantalla.text('P:',0,18,1)
        pantalla.text(pres,20,18,1)
        pantalla.show()
    except:
        print('Se ha producido un error de conexion')
    sleep(1)
