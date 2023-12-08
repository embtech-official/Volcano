# Audio:

If you have any doubts about how to connect a Speaker box on Volcano Board, consult Volcano Manual.

For this project you will need a Docker container with the following requirements:

- libasound2.
- libasound2-dev.
- alsa-utils.
- libsndfile1-dev.
- python3.
- You also need to give the user access to audio group.

In `../../Docker/audio/`,  there is a Dockerfile to use as example.

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

#### Create a Branch:

```bash
$ torizoncore-builder union custom-branch
```

#### Deploying The Image:

Directly on the board through [SSH](https://developer.toradex.com/software/development-resources/ssh), with the `deploy` command, passing the device IP address, username, and password as arguments:

```bash
torizoncore-builder deploy --remote-host <ip or host> --remote-username torizon --remote-password torizon --reboot custom-branch
```

## List the available audio devices:

```bash
 cat /proc/asound/cards
```

Possible Output: 

```bash
 0 [imx8mmwm8904   ]: simple-card - imx8mm-wm8904
                      imx8mm-wm8904
```

## Running Docker Container:

Custom container build from Dockerfile:

```bash
docker run --rm -e ALSA_CARD=imx8mmwm8904 --group-add audio --device=/dev/snd:/dev/snd <username>/<name-of-image>
```

## Running audio:

To run the audio on your board, use the below command: 

```bash
aplay coolSong.wav
```

If you want to give a timeout for the sound, use this command: 

```bash
timeout --k 8 8 aplay coolSong.wav
```

This will give a 8 seconds duration for the audio.

## References:

1. https://developer.toradex.com/linux-bsp/application-development/multimedia/audio-linux/

2. https://developer.toradex.com/torizon/application-development/use-cases/multimedia/how-to-play-audio-on-torizoncore-using-alsa-and-ccpp/

3. https://developer.toradex.com/torizon/os-customization/use-cases/device-tree-overlays-on-torizon/

4. https://developer.toradex.com/linux-bsp/os-development/build-yocto/device-tree-overlays-linux/
