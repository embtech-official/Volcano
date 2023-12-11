# Can:

If you have any doubts about how to connect a CAN cable on Volcano Board, consult the Volcano Manual.

For this project, you will need a Docker container with the following requirements:

- can-utils.

- net-tools.

- iproute2.

- python3-pip.

- python3.

In `../../Docker/can/`, there is a Dockerfile to use as example.

## Prerequisites:

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

##### Changing Device-tree for  the Verdin IMX8M Mini:

```bash
torizoncore-builder dt apply --include-dir linux/include --include-dir linux/arch/arm64/boot/dts/freescale/ linux/arch/arm64/boot/dts/freescale/imx8mm-verdin-wifi-dahlia.dts
```

##### Changing Device-tree for  the Verdin IMX8M Plus:

```bash
torizoncore-builder dt apply --include-dir linux/include --include-dir linux/arch/arm64/boot/dts/freescale/ linux/arch/arm64/boot/dts/freescale/imx8mp-verdin-wifi-dahlia.dts
```

In a Verdin IMX8M Plus the CAN connection is already enable by default.

##### Removing Overlay:

We also need to remove the overlay that disabled CAN connection: 

```bash
torizoncore-builder dto remove verdin-imx8mm_disable_can1.dtbo
```

##### Applying Overlay:

In `../../device-trees/`, there is file called `verdin-imx8mm_20mhz_can1.dts`. Which contain an overlay that enabled CAN in Verdin IMX8 Mini.

```bash
torizoncore-builder dto apply --include-dir linux/include --include-dir linux/arch/arm64/boot/dts/freescale/ --device-tree imx8mm-verdin-wifi-dahlia.dtb verdin-imx8mm_20mhz_can1.dts
```

#### Create a Branch:

```bash
$ torizoncore-builder union custom-branch
```

#### Deploying The Image:

Directly on the board through [SSH](https://developer.toradex.com/software/development-resources/ssh), with the `deploy` command, passing the device IP address, username, and password as arguments:

```bash
torizoncore-builder deploy --remote-host <ip or host> --remote-username torizon --remote-password torizon --reboot custom-branch## Environment requirements:
```

From the command-line in your board, type the following commands : 

```bash
ip link show can0
```

Possible output: 

```bash
4: can0: <NOARP,ECHO> mtu 16 qdisc pfifo_fast state DOWN mode DEFAULT group default qlen 10
    link/can
```

You can observe the can0 is in DOWN mode, let's bring it to UP mode with  the following commands .

First we need to define a bitrate of 500000 bps:

```bash
ip link set can0 type can bitrate 500000
```

Bring the interface up:

```bash
ip link set can0 up
```

Now, if you type the  `ip link show can0` again, you can see the can interface is in UP mode.

Possible output:

```bash
4: can0: <NOARP,UP,LOWER_UP,ECHO> mtu 16 qdisc pfifo_fast state UP mode DEFAULT group default qlen 10
    link/can
```

## Running Docker Container:

Custom container built from Dockerfile:

```bash
docker run -it --rm  --name=can-test --net=host --cap-add="NET_ADMIN" \         -v /dev:/dev -v /tmp:/tmp -v /run/udev/:/run/udev/ \        <username>/<name-of-image>
```

- --net=host : This will make Docker to uses the host's network stack for the container.
- --cap-add=NET_ADMIN : For interacting with the network stack, this allow to modify the network interfaces.

## Simple testing with can-utils

Now, inside your Docker Container : 

One way to test if everything is OK with your CAN communication is to do the following:

1. Use the `cansend <interface> <message>` to send CAN messages on a given interface. Like for example:
   
   ```
   cansend can0 123#deadbeef
   ```

2. Use the `candump <interface>` command to start listening to incoming CAN messages on a given  interface. 

```bash
candump can0
```

You can read more about can-utils on its `https://github.com/linux-can/can-utils/blob/master/README.md`.

## Can with Python:

In this repository has a .py file called can, which has a implementation of how to use a can  with python.

First we need to import the can library  :

```python
import can
```

Declare our can  interface:

```python
with can.Bus(interface='socketcan',
          channel='can0',
          bitrate=500000) as busCan:
```

Define a id message and data:

```python
message = can.Message(arbitration_id=123, is_extended_id=True,
                         data=[0x11, 0x22, 0x33]) 
```

```python
 busCan.send(message)
```

Receive message:

```python
# iterate over received messages
   for msg in bus:
       print(f"{msg.arbitration_id:X}: {msg.data}")
```

Example taken from library documentation : [python-can · PyPI](https://pypi.org/project/python-can/).

## Automatically bring up a SocketCAN interface on boot:

From the command-line in your board, type the following commands :

With your favorite cli text editor,  open this file 

`/etc/systemd/network/80-can.network` with sudo, and add the following lines to it :

```bash
[Match]
Name=can0
[CAN]
BitRate=500K
RestartSec=100ms
```

Once done, save the file and exit.

To enable this configuration file for our `can0` SocketCAN network interface, we just need to restart the *systemd-networkd* service:

```bash
sudo systemctl restart systemd-networkd
```

## References:

1. https://developer.toradex.com/torizon/application-development/peripheral-access/how-to-use-can-on-torizoncore/
2. [Automatically bring up a SocketCAN interface on boot - PragmaticLinux](https://www.pragmaticlinux.com/2021/07/automatically-bring-up-a-socketcan-interface-on-boot/)
3. [python-can · PyPI](https://pypi.org/project/python-can/)
4. https://developer.toradex.com/torizon/os-customization/use-cases/device-tree-overlays-on-torizon/
5. https://developer.toradex.com/linux-bsp/os-development/build-yocto/device-tree-overlays-linux/
