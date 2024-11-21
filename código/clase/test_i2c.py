from machine import Pin, SoftI2C
import ssd1306

v = 0.4

print('test_i2c version:',v)

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

lista_dispositivos_i2c = i2c.scan()

print('dispositivos i2c:', lista_dispositivos_i2c)

if 60 in lista_dispositivos_i2c: # 60 es la dirección de la pantalla
    pantalla = ssd1306.SSD1306_I2C(128, 64, i2c) # ancho y alto
    pantalla.fill(0)
    pantalla.text('hola OLED',0,0,1) # texto,columna 0,fila 0,color 
    pantalla.text('version: ' + str(v), 0, 9, 1) # columna 0, fila 1 
    pantalla.show()
else:
    print('No se ha encontrado la pantalla')
