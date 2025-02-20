import machine
_REG_VERSION = 0x42
_BUFFER = bytearray(1)
buf = _BUFFER
_cs = machine.Pin(18, machine.Pin.OUT, value=1)
_rst = machine.Pin(14, machine.Pin.OUT, value=1)
_device = machine.SoftSPI(baudrate=4000000, polarity=0, phase=0, bits=8, firstbit=0, sck=machine.Pin(5), mosi=machine.Pin(27), miso=machine.Pin(19))
address = _REG_VERSION
# MSB set to 0 for SPI read
# 0x7F = 01111111 used as a mask using &
_BUFFER[0] = address & 0x7F
_cs.off()
_device.write(_BUFFER[0:1])
_device.readinto(buf)
_cs.on()
print(_BUFFER[0])