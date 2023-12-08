# I2C:

For this project you will need a Docker container with the following requirements:

- python3.
- python3-pip.
- smbus2 ( python library).
- You also need to create and add the user  to i2cdev group.

In `../../Docker/i2c/`, there is a Dockerfile to use as example.

## List the available i2c interfaces:

```bash
ls  /dev/i2c-*
```

You can also use :

```bash
i2cdetect -l
```

Detect devices on i2c-3 : 

```bash
i2cdetect -y -r 3
```

Possible output: 

```bash
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- UU -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- 49 -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

UU denotes a device which is used by a kernel driver and thus is usually not touched. 49 denotes the temperature sensor, in that case.

## Running Docker Container:

Custom container build from Dockerfile:

```bash
docker run --rm   --device=/dev/i2c-3:/dev/i2c-3  --group-add 51  <username>/<name-of-image>
```

## I2C with Python :

In this repository has a .py file called i2c, which has a implementation of how to use a i2c  with python.

First we need to import smbus library  :

```python
import smbus2
```

Declare our bus interface:

```python
bus = smbus2.SMBus('/dev/i2c-3')
```

Read a block of 2 bytes from address 0x49 and  offset 0: 

```python
data = bus.read_i2c_block_data(0x49, 0x00, 2, force=True)
```

Handle data, where cTemp storage Temperature in Celsius:

```python
temp = (data[0]<< 8 | data[1]) >> 5
cTemp = temp * 0.125
```

Print message in console:

```python
print(f"{ctemp}°C")
```

## References :

1. https://developer.toradex.com/torizon/application-development/use-cases/peripheral-access/how-to-use-i2c-on-torizon/

2. https://developer.toradex.com/linux-bsp/application-development/peripheral-access/i2c-linux/
