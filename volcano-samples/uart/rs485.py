import serial
from serial import rs485

try:
    rs485Port = serial.Serial('/dev/ttymxc1', baudrate = 115200)
    rs485Port.rs485_mode = serial.rs485.RS485Settings()
except:
    print("Serial port RS-485 not working")

def rsend(arg1):
    print(f'\n{arg1}')
    try:
        rs485Port.write(bytes(f'\r{arg1}\n','UTF-8'))
    except:
        print("Rsend except")

def rsrecive():
    while True:
           rs485Port.flushInput()
           line = rs485Port.read_until(b'\r')
           user_input = line.decode("utf-8").replace("\r","")
