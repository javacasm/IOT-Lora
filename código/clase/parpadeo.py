import machine
import time
import random
import ssd1306
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)  # SCL y SDA son GPIO22 y GPIO21 respectivamente
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Limpiar la pantalla antes de dibujar
oled.fill(0)

# Escribir texto en la pantalla
oled.text("Hola desde ESP32", 0, 0)  # Escribir en la posición (0, 0)
oled.text("MicroPython!", 0, 10) 
led = machine.Pin(25, machine.Pin.OUT)
while True:
    led.on()
    print("on")
    time.sleep_ms(random.randint(50, 500))
    led.off()
    print("off")
    time.sleep_ms(random.randint(50, 500))