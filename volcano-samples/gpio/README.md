# GPIO access :

For this project you will need a Docker container with the following requirements:

- python3.

- python3-pip.

- libgpiod2.

- gpiod.

- gpiod (Python library to use gpio).

- You also need to give the user access to gpio group.

In `../../Docker/gpio/`, there is a Dockerfile to use as example.

Prerequisites:

1. A SoM with [TorizonCore](https://developer.toradex.com/torizon) installed.

2. Have already completed [Quickstart Guide - Toradex](https://developer-archives.toradex.com/getting-started).

3. Knowledge of [Device Tree Overlay on Torizon](https://developer.toradex.com/torizon/os-customization/use-cases/device-tree-overlays-on-torizon).

## Changing Device-Tree:

#### Getting Source Code:

To get the source code of the Toradex-supplied device tree files (including overlays), you need to clone two repositories:

- **Linux kernel**:
   it contains the device trees and headers that both device trees and 
  overlays might reference. For i.MX 6/6ULL/7, we use the upstream kernel 
  directly from kernel.org, and for i.MX 8/8X/8M Mini/8M Plus we provide 
  our own fork based on the NXP downstream kernel.
- **Device tree overlays**:
   this is a repository with overlays provided by Toradex. You need to use
   a specific branch and commit depending on the TorizonCore version and 
  whether it uses the upstream kernel or our fork based on the NXP 
  downstream.

##### Info:

The device trees and overlays workflow is being reviewed. The `torizoncore-builder dt checkout` command is not available for TorizonCore 6 at the moment, and it may 
change or be deprecated. For TorizonCore 5, go to the corresponding 
version docs.

###### Not available for TorizonCore 6

```bash
$ torizoncore-builder dt checkout 
```

###### Torizoncore version above 6 :

###### Cloning the `linux` or `linux-toradex` repositories may take a while.

For i.MX 6/6ULL/7 :

```bash
git clone -b linux-6.0.y git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
```

```bash
git clone -b master git://git.toradex.com/device-tree-overlays.git device-trees
```

For i.MX 8/8X/8M Mini/8M Plus:

```bash
git clone -b toradex_5.15-2.1.x-imx git://git.toradex.com/linux-toradex.git linux
```

```bash
git clone -b toradex_5.15-2.1.x-imx git://git.toradex.com/device-tree-overlays.git device-trees
```

You will end up with `linux` and `device-trees` directories.

To see the available device trees and select the appropriate one for your device, run the command below, passing the parameter `-name` accordingly to your device:

Verdin IMX8M Mini:

```bash
find linux -name "*imx8mm-verdin*.dts"
```

Output:

```bash
linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-nonwifi-dev.dts
linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-wifi-dahlia.dts
linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-nonwifi-yavia.dts
linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-wifi-dev.dts
linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-wifi-yavia.dts
linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-nonwifi-dahlia.dts
```

Verdin IMX8M Plus:

```bash
find linux -name "*imx8mp-verdin*.dts"
```

Output:

```bash
linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-wifi-yavia.dts
linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-nonwifi-dev.dts
linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-nonwifi-yavia.dts
linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-wifi-dahlia.dts
linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-nonwifi-dahlia.dts
linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-wifi-dev.dts
```

##### Changing Device-tree for  Verdin IMX8M Mini:

```bash
torizoncore-builder dt apply --include-dir linux/include --include-dir linux/arch/arm64/boot/dts/freescale/ linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-wifi-dahlia.dts
```

##### Changing Device-tree for  Verdin IMX8M Plus:

```bash
torizoncore-builder dt apply --include-dir linux/include --include-dir linux/arch/arm64/boot/dts/freescale/ linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-wifi-dahlia.dts
```

#### Applying Overlay:

In `../../device-trees/`, has a  file called `verdin-imx8mm_gpio.dts`,  which contain an overlay that enabled gpio in Verdin IMX8 Mini.  And in the same folder has a file called `verdin-imx8mp_gpio.dts`, which contain an overlay that enabled gpio in Verdin IMX8 Plus.

Example for Verdin IMX8 Mini: 

```bash
torizoncore-builder dto apply --include-dir linux/include --include-dir linux/arch/arm64/boot/dts/freescale/ --device-tree imx8mm-verdin-wifi-dahlia.dtb verdin-imx8mm_gpio.dts
```

#### Create a Branch:

```bash
$ torizoncore-builder union custom-branch
```

#### Deploying The Image:

Directly on the board through [SSH](https://developer.toradex.com/software/development-resources/ssh), with the `deploy` command, passing the device IP address, username, and password as arguments:

```bash
torizoncore-builder deploy --remote-host <ip or host> --remote-username torizon --remote-password torizon --reboot custom-branch
```

## Running Docker Container:

Custom container build from Dockerfile:

```bash
docker run --rm -it  --user torizon -w /home/torizon  -v /dev:/dev --device-cgroup-rule='c 254:* rmw' <username>/<name-of-image>
```

Toradex Container : 

```bash
docker run --rm -it -v /dev:/dev --device-cgroup-rule='c 254:* rmw' torizonextras/arm64v8-gpiod
```

## Finding Avaliable GPIO PINS:

To find the avaliable gpio pins, first we need to find the gpio banks.  A gpio bank it's like a database of your gpio pins, and inside each bank have colums and rows like any another database. In the case of gpio bank, has a imaginary column called `line` , that linked the gpio pin. Use the following command inside your container to see all gpio banks: 

```bash
ls /dev/gpiochip*
```

Output: 

```bash
/dev/gpiochip0  /dev/gpiochip1  /dev/gpiochip2  /dev/gpiochip3  /dev/gpiochip4
```

Use the following command to see all gpio banks and their lines:

```bash
gpioinfo
```

Possible output: 

```bash
...
 gpiochip2 - 32 lines:
    line   0:  "SODIMM_52"       unused  output  active-high
    line   1:  "SODIMM_54"       unused   input  active-high
    line   2:  "SODIMM_64"       unused   input  active-high
    line   3:  "SODIMM_21"       unused   input  active-high
    line   4: "SODIMM_206"       unused   input  active-high
    line   5:  "SODIMM_76" "regulator-usdhc2" output active-high [used]
    line   6:  "SODIMM_56"       unused   input  active-high
    line   7:  "SODIMM_58"       unused   input  active-high
    line   8:  "SODIMM_60"       unused   input  active-high
    line   9:  "SODIMM_62"       unused   input  active-high
    line  10:      unnamed       unused   input  active-high
    line  11:      unnamed       unused   input  active-high
    line  12:      unnamed       unused   input  active-high
    line  13:      unnamed       unused   input  active-high
    line  14:  "SODIMM_66"       unused   input  active-high
    line  15:  "SODIMM_17"       unused   input  active-high
    line  16:      unnamed       unused   input  active-high
    line  17:      unnamed       unused   input  active-high
    line  18:      unnamed       unused   input  active-high
    line  19: "SODIMM_244"       unused  output  active-high
    line  20:      unnamed       unused   input  active-high
    line  21:  "SODIMM_48"       unused   input  active-high
    line  22:  "SODIMM_44"       unused   input  active-high
    line  23:  "SODIMM_42"       unused   input  active-high
    line  24:  "SODIMM_46"       unused   input  active-high
    line  25:      unnamed "regulator-wifi-en" output active-high [used]
    line  26:      unnamed       unused   input  active-high
    line  27:      unnamed       unused   input  active-high
    line  28:      unnamed       unused   input  active-high
    line  29:      unnamed       unused   input  active-high
    line  30:      unnamed       unused   input  active-high
    line  31:      unnamed       unused   input  active-high
...
```

With the  above output you can see which `SODIMM` corresponds with the correct line.

#### Volcano Board

In case of you are using the Volcano Board and Verdin Mini Module, the gpio pins of Led User and Button user are: 

```bash
 gpiochip2 - 32 lines:
    line   0:  "SODIMM_52"       unused  output  active-high
    line   1:  "SODIMM_54"       unused   input  active-high
```

Where the line 0 corresponds to the led and line 1 corresponds the user button.

You can check this in the Volcano datasheet. Be careful,  the bank and the line may vary according to the module.

## Toggle the GPIO Pin

Change the logic level of the pin and verify if it works as expected.

```bash
gpioset <bank> <line>=<logic_level>
```

For example, we could turn the LED on by running the following command.

```bash
gpioset gpiochip2 0=1
```

You can also omit the 'gpiochip' name below as:

```bash
gpioset 2 0=1
```

To turn the led off use the following command: 

```bash
gpioset 2 0=0
```

Now, to check with the button it's working properly use the monitor command:

```bash
gpiomon 2 1
```

When you press the button the follow output will apper in the terminal: 

```bash
event: FALLING EDGE offset: 1 timestamp: [   10924.788970750]
event:  RISING EDGE offset: 1 timestamp: [   10924.941961250]
```

Press Ctrl + C to exit.

## Python blink Led :

To create a script in python to intereact with the gpio we will use the [gpiod]([gpiod · PyPI](https://pypi.org/project/gpiod/)) library:

In this repository has a .py file called blinkLed, which have a implementation of how to use a gpio pins with python.

We need to import the gpiod library inside ours .py file with the following line:

```python
import gpiod
```

Now, we will declare a variable to store which gpio bank we are using:

```python
gpiochip = gpiod.chip('gpiochip2')
```

To configure which is the type of the pin we are using:

```python
config_output = gpiod.line_request()
config_output.request_type = gpiod.line_request.DIRECTION_OUTPUT
```

If you are using  a Input peripheral, like a button, change the second line to :

```python
config_output.request_type = gpiod.line_request.DIRECTION_INPUT
```

Now, we need to declare which line (pin) we are using, the line that corresponds to the led is 0, so we will declare the led variable like this:

```python
led = gpiochip.get_line(0)
```

and pass our configuration to led : 

```python
led.request(config_output)
```

To turn the led on we will use the follwing line: 

```python
led.set_value(1)
```

And, to turn it off : 

```python
led.set_value(0)
```

Now, to create a blink application we just need to put it into a while loop, like this:

```python
while true :
    print("LED ON")
    led.set_value(1)
    time.sleep(1)
    print("LED OFF")
    led.set_value(0)
    time.sleep(1)
```

Don't forget to import time library, using `import time`.

## Python Button :

In this repository has a .py file called button, which has a implementation of how to use a gpio button with python.

The first steps are the same as for the led:

```python
 gpiochip = gpiod.chip('gpiochip2')
 config_input = gpiod.line_request()
```

But, now you need to declare as a INPUT gpio, like that: 

```python
config_input.request_type = gpiod.line_request.DIRECTION_INPUT
```

Now, we need to declare which line (pin) we are using, the line that corresponds to the button is 1, so we will declare the btn variable like this:

```python
 btn = gpiochip.get_line(1)
 btn.request(config_input)
```

To check if the button was pressed, you will use this if statement: 

```python
if(btn.get_value() == 0) :
```

If it returns true, so the button was pressed.

In the file `button.py` has an implementation that when the button is pressed the led will turn on.

## Best Practices for Production

### Specify Accessible Devices within the Container

To test the GPIO pin, we provided container access to all GPIO banks using the `--device-cgroup-rule='c 254:* rmw'` flag. However, it is recommended to only share the required banks with the container using the `--device` flag when in production. For example:

```
# docker run --rm -it --device /dev/gpiochip2 <yourDockerHubUsername>/<DockerHubRepository>
```

## References

1. https://developer.toradex.com/torizon/application-development/peripheral-access/how-to-use-gpio-on-torizoncore/
2. https://developer.toradex.com/torizon/os-customization/use-cases/device-tree-overlays-on-torizon/
3. https://developer.toradex.com/linux-bsp/os-development/build-yocto/device-tree-overlays-linux/
