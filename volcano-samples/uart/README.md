## UART :

If you have any doubts about how to connect a Serial cable on Volcano Board, consult Volcano Manual.

For this project you will need a Docker container with the following requirements:

- python3.
- python3-pip.
- pyserial ( python library).
- You also need to give the user access to dialout group.

In `../../Docker/uart/`, there is a Dockerfile to use as example.

## Python Comunication:

#### RS-485

RS-485 is a communication protocol running on top of the UART stack. The same steps provided in the more generic article [UART (Linux): RS-485](https://developer.toradex.com/linux-bsp/application-development/peripheral-access/uart-linux#rs-485) apply to TorizonCore.

#### Python :

In this repository has a .py file called rs485, which has a implementation of how to use a can with python.

We need to import the serial library inside ours .py file with the follwing lines.

```python
import serial
```

Now we need to declare the serial port which we are using: 

```python
rs485Port = serial.Serial('/dev/ttymxc1', baudrate = 115200)
```

If you are using a RS-485 port, add this line of code: 

```python
 rs485Port.rs485_mode = serial.rs485.RS485Settings()
```

You also need to add this import, if you are using a RS-485 port:

```python
from serial import rs485
```

Send message: 

```python
rs485Port.write(bytes(f'\r{arg1}\n','UTF-8'))
```

Recive message:

```python
rs485Port.flushInput()
line = rs485Port.read_until(b'\r')
user_input = line.decode("utf-8").replace("\r","")
```

## Send a message From PC:

To send a command in GNU/LINUX, use echo command with option -e, and add a \\r to it.

Example: 

```bash
echo -e  'hello World\r' > /dev/ttyUSB0
```

In Windows Applications, like Hercules, the \\r, already included.

##### The ascii character `\r`  is commonly known as '**Carriage Return**'.

## Best Practices for Production

#### Specify Accessible Devices within the Container

It is recommended to only share the required devices with the container using the `--device` flag when in production. For example:

```bash
docker run --rm -it --device /dev/ttymxc1 <yourDockerHubUsername>/<DockerHubRepository>
```

## References:

1. https://developer.toradex.com/torizon/application-development/peripheral-access/how-to-use-uart-on-torizoncore/
