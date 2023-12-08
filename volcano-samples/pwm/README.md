# PWM:

For this project you will need a Docker container with the following requirements:

- python3.
- python3-pip.
- pathlib ( python library).
- You also need to give the user access to pwm group.

In `../../Docker/pwm/`, there is a Dockerfile to use as example.

## Running Docker Container:

Custom container build from Dockerfile:

```bash
docker run --rm -v /sys/class/pwm/pwmchip0:/sys/class/pwm/pwmchip0 --group-add 54  --user torizon -w /home/torizon  <username>/<name-of-image>
```

## List avaliable PWMs:

PWM can either be controlled by your application, or by a device driver. If a device driver uses a PWM, you will not be able to control it from your application, therefore you must first list the available PWMs.

Use the following command to list the avaliable PWMs: 

```bash
sudo cat /sys/kernel/debug/pwm
```

- Those shown as `null` are either not exported or in use by a driver. Try to export them as explained on [PWM (Linux)](https://developer.toradex.com/linux-bsp/application-development/peripheral-access/pwm-linux); if successful, you will be able to use them.
- Those shown as `sysfs` are exported to userspace control and ready-to-use.

## Python with the Pwmchip interface:

In this repository has a .py file called pwm, which has a implementation of how to use a pwm with python.

We need to import the pathlib and time library inside ours .py file with the follwing lines:

```python
from pathlib import Path
import time
```

Define de pwmchip and pwm0 dir: 

```python
pwmchip0_dir = Path('/sys/class/pwm/pwmchip0')
pww0_dir = pwmchip0_dir / 'pwm0'
```

Write 0 in file export: 

```python
if not pww0_dir.exists():
    export = open((pwmchip0_dir / 'export'), 'w' ,buffering=1)
    export.write('0\n')
    export.flush()
    export.close()

    if not pwmchip0_dir.exists():
        print("Couldn\t export pwmchip0")
        exit()
```

Define duty cycle, period and enable files: 

```python
duty_cycle = pww0_dir / 'duty_cycle'
period = pww0_dir / 'period'
enable = pww0_dir / 'enable'
```

Open this files: 

```python
with open(duty_cycle, 'w', buffering=1) as pwm_duty_cycle,\
    open(enable,'w',buffering=1) as pwm_enable,\
    open(period,'w',buffering=1) as pwm_period:
```

Select the period of the PWM signal. Value is in nanoseconds.

```python
 pwm_period.write("2000000\n")
```

Select the duty cycle. Value is in nanoseconds and must be less than the period.

```python
pwm_duty_cycle.write("1000000\n")
```

Enable/disable the PWM signal, use 1 or 0 respectively:

```python
 pwm_enable.write("1\n")
```

Sleep  application for 1 second: 

```python
time.sleep(1)
```

Change period and duty cycle, and after that, wait 1 second:

```python
pwm_period.write("1000000\n")
    pwm_duty_cycle.write("500000\n")

    time.sleep(1)
```

Change period and duty cycle, wait 1 second and disable pwm: 

```python
pwm_period.write("3000000\n")
    pwm_duty_cycle.write("1500000\n")

    time.sleep(1)

    pwm_enable.write("0\n")
```

## References:

1. https://developer.toradex.com/torizon/application-development/use-cases/peripheral-access/how-to-use-pwm-on-torizoncore/

2. https://developer.toradex.com/linux-bsp/application-development/peripheral-access/pwm-linux/
