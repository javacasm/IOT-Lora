# import machine
from machine import Pin , PWM
from time import sleep_ms, sleep 

#led =machine.Pin(25, machine.Pin.OUT)
led = Pin(25,Pin.OUT)

led_pwm = PWM(led)
led_pwm.freq(500) # cambio la frecuencia PWM a 500
print('Frecuencia del PWM:',led_pwm.freq())

for brillo in range(0,1024,4): # entre 0 y 1023
    led_pwm.duty(brillo)
    sleep_ms(5)
    
for brillo in range(1022,0,-4): # entre 1023 y 0
    led_pwm.duty(brillo)
    sleep_ms(5)
led_pwm.duty(0)