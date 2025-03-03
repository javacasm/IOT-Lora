[Tutorial LoraWan](https://lemariva.com/blog/2020/02/tutorial-micropython-esp32-sends-data-over-lorawan)

[Código del ejemplo](https://github.com/lemariva/uPyLoRaWAN/tree/LoRaWAN)

Veamos un tutorial detallado y paso a paso sobre cómo utilizar The Things Network (TTN) con LoRaWAN desde MicroPython en una placa ESP32 equipada con un módulo LoRa RFM95. Este tutorial incluye ejemplos prácticos y explicaciones claras para que puedas implementarlo incluso si eres principiante. Vamos a configurar un nodo LoRaWAN que envíe datos a TTN utilizando el método de activación ABP (Activation By Personalization), ya que es más sencillo para empezar.

---

Tutorial: Conectar ESP32 con RFM95 a TTN usando MicroPython

Requisitos previos

1. Hardware:
    - Placa ESP32 (como la Wemos TTGO LoRa32 o cualquier ESP32 genérico).    
    - Módulo LoRa RFM95 (compatible con SX1276).
    - Antena adecuada para la frecuencia de tu región (868 MHz para Europa, 915 MHz para América del Norte, etc.).
    - Cables para conexiones si usas un módulo RFM95 separado.
    - Computadora con puerto USB.
        
2. Software:
    - MicroPython instalado en tu ESP32 (puedes descargarlo desde micropython.org y flashearlo con herramientas como esptool.py).
    - Un IDE como Thonny o uPyCraft para cargar código al ESP32.
    - Cuenta en The Things Network (TTN) creada en console.thethingsnetwork.org.
        
3. Conocimientos básicos:
    - Familiaridad con MicroPython y conexiones SPI.
    - Acceso a un gateway LoRaWAN cercano registrado en TTN o tu propio gateway.

---

Paso 1: Conectar el RFM95 al ESP32

El módulo RFM95 utiliza SPI para comunicarse con el ESP32. Asegúrate de conectar los pines correctamente. Aquí tienes una configuración típica:

| Pin RFM95 | Pin ESP32 (ejemplo) | Descripción  |
| --------- | ------------------- | ------------ |
| VCC       | 3.3V                | Alimentación |
| GND       | GND                 | Tierra       |
| MOSI      | GPIO 27             | SPI MOSI     |
| MISO      | GPIO 19             | SPI MISO     |
| SCK       | GPIO 5              | SPI Clock    |
| NSS (CS)  | GPIO 18             | Chip Select  |
| DIO0      | GPIO 26             | Interrupción |
| RST       | GPIO 14             | Reset        |

Nota: Antes de encender el ESP32, conecta la antena al RFM95 para evitar daños al módulo.

---

Paso 2: Configurar TTN

1. Inicia sesión en TTN:    
    - Ve a console.thethingsnetwork.org y accede con tu cuenta.
2. Crea una aplicación:
    - Haz clic en "Applications" y luego en "Add Application".
    - Rellena los campos:
        - Application ID: Un nombre único ( Ejemplo: mi-app-lora).
        - Description: Opcional ( Ejemplo: "Aplicación de prueba con ESP32").
        - Handler: Selecciona tu región ( Ejemplo: eu1 para Europa).
    - Haz clic en "Add Application".
        
3. Registra un dispositivo:
    - En la pestaña de tu aplicación, ve a "Devices" y haz clic en "Register Device".
    - Rellena:
        - Device ID: Un nombre único ( Ejemplo: esp32-lora-01).
        - Device EUI: Genera uno automáticamente haciendo clic en el ícono de mezcla o usa uno personalizado.
    - Haz clic en "Register".
4. Configura ABP:
    - En la pestaña del dispositivo, ve a "Settings".
    - Cambia "Activation Method" a ABP.
    - Desactiva "Frame Counter Checks" (opcional, pero recomendado para pruebas).
    - Copia los siguientes valores generados:
        - Device Address (DevAddr).
        - Network Session Key (NwkSKey).
        - App Session Key (AppSKey).
    - Guárdalos, los usarás en el código.
        

---

Paso 3: Instalar las librerías en MicroPython

Necesitamos una implementación de LoRaWAN para MicroPython. Usaremos una versión simplificada basada en proyectos como uLoRaWAN o el driver de SX127x. Aquí te doy un ejemplo funcional:

1. Descarga el driver SX127x:    
    - Puedes encontrar una implementación en GitHub (como la de LeMaRiva o aizukanne). Por simplicidad, asumimos que tienes un archivo sx127x.py y lora.py.
    - Sube estos archivos al ESP32 usando Thonny (arrastrándolos a la raíz del sistema de archivos).

2. Estructura de archivos en el ESP32:    
    - sx127x.py: Driver del módulo RFM95.
    - lora.py: Clase para manejar LoRaWAN.
    - main.py: Tu script principal.
        

---

Paso 4: Código de ejemplo

A continuación, te doy un ejemplo funcional para enviar un mensaje simple a TTN usando ABP desde MicroPython.

python

```python
from sx127x import SX127x
from lora import LoRa
from machine import Pin, SPI
import time
import ubinascii

# Configuración de pines SPI
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(27), miso=Pin(19))
cs = Pin(18, Pin.OUT)  # NSS
rst = Pin(14, Pin.OUT)  # Reset
irq = Pin(26, Pin.IN)   # DIO0

# Inicializar el módulo RFM95
lora = SX127x(spi, cs, rst, irq, freq=868.0)  # Frecuencia para Europa, cambia a 915.0 si es necesario

# Configuración LoRaWAN
dev_addr = ubinascii.unhexlify('260B1234')  # Reemplaza con tu Device Address de TTN
nwk_skey = ubinascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # Reemplaza con tu Network Session Key
app_skey = ubinascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')  # Reemplaza con tu App Session Key

# Inicializar LoRaWAN en modo ABP
lora.init(mode=LoRa.LORAWAN, region=LoRa.EU868, device_address=dev_addr, network_key=nwk_skey, app_key=app_skey)

# Contador de tramas (Frame Counter)
fcnt = 0

# Función para enviar datos
def send_data(payload):
    global fcnt
    lora.send(payload, fcnt, port=1)  # Puerto 1 por defecto
    fcnt += 1
    print("Datos enviados:", payload)

# Bucle principal
while True:
    payload = "Hola TTN desde ESP32!"
    send_data(payload.encode())
    time.sleep(60)  # Espera 60 segundos entre envíos
```

Notas sobre el código:

- Reemplaza dev_addr, nwk_skey y app_skey con los valores obtenidos de TTN.
- Ajusta la frecuencia (freq=868.0) según tu región.
- El módulo sx127x.py y lora.py deben estar adaptados para soportar ABP y tu región específica. Si no los tienes, busca implementaciones como las de LeMaRiva o adapta una desde Arduino LMIC.

---

Paso 5: Cargar y ejecutar el código

1. Conecta tu ESP32 a la computadora vía USB.
2. Abre Thonny y sube los archivos sx127x.py, lora.py y main.py al ESP32.
3. Ejecuta main.py desde Thonny o reinicia el ESP32 para que se ejecute automáticamente.

Si todo está configurado correctamente, verás mensajes en la consola indicando que los datos se están enviando.

---

Paso 6: Verificar en TTN

1. Ve a la pestaña "Live Data" de tu dispositivo en TTN.
2. Si el envío funciona, verás los payloads recibidos. Por ejemplo:
    ```text
    {
      "port": 1,
      "payload_raw": "SG9sYSBUVE4gZGVzZGUgRVNQMzIh"
    }
    ```
    
    - Usa la pestaña "Payload Formats" en TTN para decodificar el payload de base64 a texto si es necesario.
        

---

Paso 7: Depuración y mejoras

- Problemas comunes:
    
    - Si no ves datos en TTN, verifica:
        
        - La frecuencia coincide con tu gateway y región.
            
        - El gateway está activo y conectado a TTN.
            
        - Los pines SPI están correctamente conectados.
            
    - Aumenta el intervalo entre envíos (time.sleep) para cumplir con las restricciones de duty cycle de LoRaWAN.
        
- Mejoras:
    
    - Agrega sensores (como temperatura con un DHT11) y envía datos reales.
        
    - Implementa OTAA (Over-the-Air Activation) para una configuración más segura (requiere más código y soporte en la librería).
        

---

Ejemplo con sensor

Aquí tienes un ejemplo extendido que envía la temperatura usando un sensor DHT11:

python

```python
from sx127x import SX127x
from lora import LoRa
from machine import Pin, SPI
import time
import ubinascii
import dht

# Configuración de pines SPI
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(27), miso=Pin(19))
cs = Pin(18, Pin.OUT)
rst = Pin(14, Pin.OUT)
irq = Pin(26, Pin.IN)

# Sensor DHT11
sensor = dht.DHT11(Pin(4))

# Inicializar RFM95
lora = SX127x(spi, cs, rst, irq, freq=868.0)

# Configuración LoRaWAN
dev_addr = ubinascii.unhexlify('260B1234')
nwk_skey = ubinascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
app_skey = ubinascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

lora.init(mode=LoRa.LORAWAN, region=LoRa.EU868, device_address=dev_addr, network_key=nwk_skey, app_key=app_skey)

fcnt = 0

def send_data(payload):
    global fcnt
    lora.send(payload, fcnt, port=1)
    fcnt += 1
    print("Datos enviados:", payload)

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    payload = "Temp: {}C, Hum: {}%".format(temp, hum)
    send_data(payload.encode())
    time.sleep(60)
```

---

Conclusión

Con este tutorial, has configurado un ESP32 con RFM95 para enviar datos a TTN usando MicroPython. Este es un punto de partida que puedes expandir con más sensores, optimizaciones de energía (como deep sleep) o soporte para OTAA. Si tienes problemas, asegúrate de verificar las conexiones, la cobertura del gateway y la compatibilidad de las librerías. ¡Disfruta explorando LoRaWAN!


