# import machine
from machine import Pin 
from time import sleep_ms, sleep 

#led =machine.Pin(25, machine.Pin.OUT)
led = Pin(25,Pin.OUT)

while True: # bucle infinito o el loop de arduino
    led.on()
    sleep_ms(50)
    led.off()
    sleep_ms(210)