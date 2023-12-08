## SPI :

For this project you will need a Docker container with the following requirements:

- python3.
- python3-pip.
- spidev ( python library).
- You also need to give the user access to spidev group.

In `../../Docker/spi/`, there is a Dockerfile to use as example.

## Enable SPI and Bind SPIDEV

1. Check that there are no pre-enabled SPI devices.

```bash
ls -al /dev/spi*
```

2. Check the SPI devices under `/sys/bus`.

```bash
ls /sys/bus/spi/devices 
```

Possible Output:

```bash
spi2.0
```

Enter in root mode with this command: 

```bash
sudo su
```

##### IMPORTANT: When executed the following commands, you will disable the CAN connection for Verdin IMX8 Mini, this occur because IMX8 Mini doesn't have a native CAN connection,  so its uses SPI to communicate with the MCP, wich is a SPI-CAN converter.

3. Unbind the device from the mcp251x driver.

```bash
echo spi2.0 > /sys/bus/spi/drivers/mcp251xfd/unbind
```

4. Allow the device to take spidev driver.

```bash
echo spidev > /sys/bus/spi/devices/spi2.0/driver_override
```

5. Bind it to the spidev driver.

```bash
echo spi2.0 > /sys/bus/spi/drivers/spidev/bind
```

6. exit root mode with this command: 

```bash
exit
```

7. Check if the process worked by listing the `/dev` directory.

```bash
ls -al /dev/spi*
```

Possible output: 

```bash
crw-rw-r-- 1 root spidev 153, 0 Sep 12 11:54 /dev/spidev2.0
```

## Running Docker Container:

Custom container build from Dockerfile:

```bash
docker run --rm -t -i --user torizon -w /home/torizon --group-add spidev --device /dev/spidev2.0:/dev/spidev2.0  <username>/<name-of-image> 
```

## Python with SPI:

In this repository has a .py file called spi, which has a implementation of how to use a spi with python.

We need to import the spidev library inside ours .py file with the follwing line

```python
import spidev
```

Now we need to define bus and device variable, the pattern is ` /dev/spidev<bus>.<device>`, so in our case ,`/dev/spidev2.0`  , the variable wil be like that:

```python
bus = 2
device = 0
```

Enable Spi:

```python
spi = spidev.SpiDev()
```

Open a connection to a specific bus and device (chip select pin):

```python
spi.open(bus, device)
```

Read n bytes from SPI device:

```python
spi.readbytes(n)
```

Writes a list of values to SPI device:

```python
spi.writebytes(list of values)
```

Disconnects from the SPI device:

```python
spi.close()
```

## References:

1. https://developer.toradex.com/torizon/application-development/use-cases/peripheral-access/how-to-use-spi-on-torizon/

2. https://developer.toradex.com/linux-bsp/application-development/peripheral-access/spi-linux/

3. [spidev · PyPI](https://pypi.org/project/spidev/)
