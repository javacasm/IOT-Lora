from machine import Pin,SoftI2C
from time import sleep
from ssd1306 import SSD1306_I2C

v = 0.5

OLED_RESET = 16

OLED_SCL = 15
OLED_SDA = 4

OLED_ADDRESS = 0x3c

OLED_WITDH = 128
OLED_HEIGHT = 64

LED_BUILTIN = 2

def test_led():
    led = Pin(LED_BUILTIN,Pin.OUT)
    espera = 0.5
    for i in range(10):
        led.on()
        sleep(espera)
        led.off()
        sleep(espera)
        espera /= 1.5

oled = None
i2c = None
oled_rst = None
def init_i2c():
    global i2c
    print('Init i2c')
    i2c = SoftI2C(scl=Pin(OLED_SCL),sda=Pin(OLED_SDA))

def init_oled():
    global oled, oled_rst
    print('init oled')
    if i2c == None:
        init_i2c()
        
    oled_rst = Pin(OLED_RESET,Pin.OUT)        
    oled_rst.off()
    print(f'oled reset off: {i2c.scan()}')

    oled_rst.on()
    print(f'oled reset on: {i2c.scan()}')        
    oled = SSD1306_I2C(OLED_WITDH,OLED_HEIGHT,i2c,addr=OLED_ADDRESS)    
    
def show_text_oled(texto,x,y):
    global oled
    if oled == None:
        init_oled()
    # print(f'show_text({texto})')
    oled.text(texto,x,y)
    oled.show()

def clear_oled():
    global oled
    if oled == None:
        init_oled()
    oled.fill(0)
    oled.show()

def test_oled():
    global oled, i2c

    show_text('hola',0,0)
    sleep(1)
    
    show_text('lora',0,9)
    sleep(1)
    
    print('reset off')
    oled_rst.off()

    sleep(1)
    
    print('reset on')
    oled_rst.on()