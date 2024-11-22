'''
Programa para gestionar la lista de la compra y que se muestre en la pantalla OLED
'''
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

pantalla = SSD1306_I2C(128, 64, i2c) # ancho, algo, conexión i2c
pantalla.fill(0) # borro la pantalla

lista_compra = ['cafe','patata','cerveza','papel higienico']

def mostrar_lista_compra(): #definición de la función
    for i in lista_compra:
        print(i)

def mostrar_lista_compra_oled(): #definición de la función
    y = 0
    for i in lista_compra:
        pantalla.text(i,0,y,1)
        y = y + 9 # 8 pixel de cada letra + 1 pixel de espacio
    pantalla.show()     
                                 
mostrar_lista_compra() # ejecuto la función
while True:
    compra = input("¿Quieres comprar algo más? ('no' para terminar) ")
    if compra != 'no':
        lista_compra.append(compra)
    else:
        break 
mostrar_lista_compra() # ejecuto la función
mostrar_lista_compra_oled()