## RTC (Real Time clock):

Two clocks are important in Linux: a `hardware clock`, also known as RTC, CMOS or BIOS clock. This is the battery-backed clock that keeps time even when the system is shut down. The second clock is called the `system clock/tick` or `kernel clock`
 and is maintained by the operating system. At boot time, the hardware clock is read and used to set the system clock. From that point onward the system clock is used to track time.

## Manipulation of RTC:

## hwclock command:

#### Description:

`hwclock` is an administration tool for the time clocks. It can: display the Hardware Clock time;  set the Hardware Clock to a specified time; set the Hardware Clock from the System Clock; set the System Clock from the Hardware Clock; compensate for Hardware Clock drift; correct the  System Clock timescale; set the kernel’s timezone, NTP timescale, and epoch (Alpha only); and  predict future Hardware Clock values based on its drift rate.

#### Basic commands:

###### Display Real-Time Clock (RTC):

```bash
sudo hwclock -r
```

Or:

```bash
sudo hwclock --show
```

###### Set RTC:

```bash
 sudo hwclock --set --date="09/14/23 12:48:08"
```

###### Set Hardware Clock to the Current system Time:

```bash
sudo hwclock -w 
```

###### Adjust Hardware Clock:

To control the adjustment of RTC when your system starts, use the “adjust” command:

```bash
sudo hwclock -adjust
```

## date command:

#### Description:

Display the current time in the given FORMAT, or set the system date.

```bash
date
```

Example : 

```bash
Thu Sep 14 12:14:25 UTC 2023
```

Set date :

```bash
date --set="STRING"
```

For Example: 

```bash
date --set="2023-09-15 18:20:40"
```

Or use just `-s`: 

```bash
date -s "2023-09-15 18:20:40"
```

###### These are the most common formatting characters for the **`date`** command:

- - **`%D`** – Display date as mm/dd/yy
  - **`%Y`** – Year (e.g., 2020)
  - **`%m`** – Month (01-12)
  - `%d` - Day of month (e.g., 01)
  - `%F` -  Full date; like %+4Y-%m-%d
  - **`%B`** – Long month name (e.g., November)
  - **`%b`** – Short month name (e.g., Nov)
  - **`%j`** – Day of year (001-366)
  - **`%u`** – Day of week (1-7)
  - **`%A`** – Full weekday name (e.g., Friday)
  - **`%a`** – Short weekday name (e.g., Fri)
  - **`%H`** – Hour (00-23)
  - **`%I`** – Hour (01-12)
  - **`%M`** – Minute (00-59)
  - **`%S`** – Second (00-60)

## timedatectl command:

#### Description:

The **timedatectl** allows displaying the current time, both, the system clock and the hardware clock. Furthermore, it also displays the currently configured time zone of the system (which is UTC by default in torizon images).

```bash
timedatectl 
```

Example of Output: 

```bash
               Local time: Thu 2023-09-14 12:21:51 UTC
           Universal time: Thu 2023-09-14 12:21:51 UTC
                 RTC time: Thu 2023-09-14 12:21:51
                Time zone: Universal (UTC, +0000)
System clock synchronized: no
              NTP service: active
          RTC in local TZ: no
```

If an Internet connection is provided, the **systemd-timesyncd** service will automatically synchronize the local system clock with a remote Network Time Protocol server and the **systemd-timedated** service will make sure the new system clock is synchronized with the hardware clock (RTC) immediately.

If no Internet connection is provided, **timedatectl** can be used to set the date or time and the **systemd-timedated** service will make sure the new system clock is synchronized with the hardware clock (RTC) immediately:

```bash
timedatectl set-ntp false
```

```bash
timedatectl set-time "2023-09-15 18:20:40"
```

For more information refer to the timedatectl [manual page at freedesktop.org](http://www.freedesktop.org/software/systemd/man/timedatectl.html "http://www.freedesktop.org/software/systemd/man/timedatectl.html").

## Change the Timezone in a Docker Container:

#### Setting the Timezone During Container Creation

You can set a specific timezone while creating a Docker container by passing the desired timezone as an environment variable using the **-e** flag:

```bash
-e TZ=America/Sao_Paulo 
```

#### Dockerfile Approach:

Include the following line in your Dockerfile:

```bash
ENV TZ=America/Sao_Paulo 
```

## References :

1. GNU man of hwclock
2. https://developer.toradex.com/software/linux-resources/linux-features/real-time-clock-rtc-linux/
