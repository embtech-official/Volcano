import spidev

# /dev/spidev<bus>.<device>
#/dev/spidev2.0

bus = 2
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
to_send = [0x01, 0x02, 0x03]
spi.writebytes(to_send)
spi.close()
