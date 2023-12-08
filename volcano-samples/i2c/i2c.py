import smbus2

try:
    bus = smbus2.SMBus('/dev/i2c-3')
    data = bus.read_i2c_block_data(0x49, 0x00, 2, force=True)
    temp = (data[0]<< 8 | data[1]) >> 5
    cTemp = temp * 0.125
    print(f"{ctemp}°C")
except:
    print("Sensor not working")
