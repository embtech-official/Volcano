## ADC (Analog-to-Digital Converter):

Analog input, also known as Analog to Digital Converter (ADC), is a hardware peripheral that can read an analog voltage value and convert it to a digital value that can be used by the processo.

The ADC Linux drivers usually support two modes of performing conversations:

- **One-shot conversions** performed by reading the ADC files for your specific board. For example: `/dev/verdin-adc*`
- **Continuous conversions** of a single channel at a time using the /dev/iio:device0 character device file.

When the ADC sequencer finishes cycling through all the enabled channels, the user can decide if the sequencer should stop (one-shot mode), or loop back and schedule again (continuous mode).

### One-shot Mode

To read a single ADC output from a particular channel, Toradex provides useful symlinks for each SoM family. This also helps you to write software that is compatible across SoMs within a family.

#### Verdin Family :

```bash
ls -l /dev/verdin-adc*
```

Possible Output: 

```bash
lrwxrwxrwx 1 root root 94 Sep 14 11:19 /dev/verdin-adc1 -> /sys/devices/platform/soc@0/30800000.bus/30a20000.i2c/i2c-0/0-0049/iio:device0/in_voltage3_raw
lrwxrwxrwx 1 root root 94 Sep 14 11:19 /dev/verdin-adc2 -> /sys/devices/platform/soc@0/30800000.bus/30a20000.i2c/i2c-0/0-0049/iio:device0/in_voltage2_raw
lrwxrwxrwx 1 root root 94 Sep 14 11:19 /dev/verdin-adc3 -> /sys/devices/platform/soc@0/30800000.bus/30a20000.i2c/i2c-0/0-0049/iio:device0/in_voltage1_raw
lrwxrwxrwx 1 root root 94 Sep 14 11:19 /dev/verdin-adc4 -> /sys/devices/platform/soc@0/30800000.bus/30a20000.i2c/i2c-0/0-0049/iio:device0/in_voltage0_raw
```

| Toradex Name | Device           |
| ------------ | ---------------- |
| ADC_1        | /dev/verdin-adc1 |
| ADC_2        | /dev/verdin-adc2 |
| ADC_3        | /dev/verdin-adc3 |
| ADC_4        | /dev/verdin-adc4 |

It will display the available Verdin pin-compatible ADCs and display the corresponding names used by the BSP. Those corresponding names are important because the Linux kernel logs will print the real device names 

(e.g. `/sys/devices/platform/soc@0/30800000.bus/30a20000.i2c/i2c-0/0-0049/iio:device0/in_voltage3_raw`), not the Verdin symlinks (e.g. `/dev/verdin-adc1`).

To get a one-shot conversion, just read the file contents:

```bash
cat /dev/verdin-adc1
```

Example of output :

```bash
286
```

### Continuous Mode

The single-channel continuous conversion mode converts a single channel continuously and indefinitely in regular channel conversion.

The continuous mode feature allows the ADC to work in the background.

The ADC converts the channels continuously without any intervention from the CPU. Additionally, the DMA can be used in circular mode, thus reducing the CPU load.    

Important folders in the **iio:deviceX** directory are:

- **buffer** directory.
- data_available: a read-only value indicating the bytes of data available in the buffer.
- enable: get and set the state of the value buffer.
- length: get and set the length of the value buffer.
- watermark: a single positive integer specifying the maximum number of scan elements to wait for.
- **scan_elements** directory contains interfaces for elements that will be captured for a single sample set in the buffer:

```bash
ls -al /sys/bus/iio/devices/iio\:device0/scan_elements/
```

Possible Output: 

```bash
total 0
drwxr-xr-x 2 root root    0 Sep 14 16:54 .
drwxr-xr-x 8 root root    0 Sep 14 11:19 ..
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_timestamp_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_timestamp_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_timestamp_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0-voltage1_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0-voltage1_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0-voltage1_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0-voltage3_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0-voltage3_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0-voltage3_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage0_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage1-voltage3_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage1-voltage3_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage1-voltage3_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage1_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage1_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage1_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage2-voltage3_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage2-voltage3_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage2-voltage3_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage2_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage2_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage2_type
-rw-r--r-- 1 root root 4096 Sep 14 17:25 in_voltage3_en
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage3_index
-r--r--r-- 1 root root 4096 Sep 14 17:25 in_voltage3_type
```

**scan_elements** exposes 3 files per channel:

- **in_voltageX_en**: is this channel enabled for capturing?
- **in_voltageX_index**: index of this channel in the buffer's chunks
- **in_voltageX_type**: How the ADC stores its data. Reading this file should return you a string something like `le:u12/16>>0`

Set up the channels in use (you can enable any combination of the channels you want):

```bash
sudo echo 1 > /sys/bus/iio/devices/iio\:device0/scan_elements/in_voltage0_en
```

Set up the buffer length:

```bash
sudo echo 100 > /sys/bus/iio/devices/iio\:device0/buffer/length
```

Enable the capture:

```bash
sudo echo 1 > /sys/bus/iio/devices/iio\:device0/buffer/enable
```

###### Notice:

For some ADCs the continuous conversion mode of  the ADC driver can only enable one channel at one time or is not even supported at all.

## References:

1. https://developer.toradex.com/torizon/application-development/use-cases/peripheral-access/how-to-use-adc-on-torizoncore/

2. https://developer.toradex.com/linux-bsp/application-development/peripheral-access/adc-linux/
