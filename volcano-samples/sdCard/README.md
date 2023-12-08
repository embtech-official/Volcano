## SD Card:

If you have any doubts about how to connect SD Card on Volcano Board, consult Volcano Manual.

TorizonCore have a auto mount for SD Cards.

Use the command `lsblk`  to list block devices:

```bash
 lsblk
```

Possible Output: 

```bash
NAME         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
mmcblk0      179:0    0 14.8G  0 disk
`-mmcblk0p1  179:1    0 14.8G  0 part /var
                                      /usr
                                      /boot
                                      /
                                      /sysroot
mmcblk0boot0 179:32   0 31.5M  1 disk
mmcblk0boot1 179:64   0 31.5M  1 disk
mmcblk1      179:96   0  7.4G  0 disk
`-mmcblk1p1  179:97   0  7.4G  0 part /var/rootdirs/media/SDHC
zram0        253:0    0    0B  0 disk
```

You can see the device `mmcblk1` , SD CARD, it's mounted on /var/rootdirs/media/SDHC

You can enter on SD Card with:

```bash
cd /var/rootdirs/media/<NAME>
```

Or  just :

```bash
cd /media/<NAME>
```

Now, after enter in mount path , you can manipulate the SD Card as you want.

## Explanation of Auto mount

Auto mount occurs because of  a rule in `etc/udev/rules.d` called `bootpart-automount.rules`, that runs a script in `etc/udev/scripts/` called `toradex-mount-bootpart.sh`

## Custom  Auto Mount:

The fstab file can be used to define how disk partitions, various other block 
devices, or remote file systems should be mounted into the file system.

Each file system is described in a separate line. These definitions will be converted into systemd mount units dynamically at boot, and when the configuration of the system manager is reloaded.

```bash
cat /etc/fstab
```

Possible Output: 

```bash
# stock fstab - you probably want to override this with a machine specific one

/dev/root            /                    auto       defaults              1  1
proc                 /proc                proc       defaults              0  0
devpts               /dev/pts             devpts     mode=0620,ptmxmode=0666,gid=5      0  0
tmpfs                /run                 tmpfs      mode=0755,nodev,nosuid,strictatime 0  0
tmpfs                /var/volatile        tmpfs      defaults              0  0

# uncomment this if your device has a SD/MMC/Transflash slot
#/dev/mmcblk0p1       /media/card          auto       defaults,sync,noauto  0  0
```

Caption:

<file system>  <mount point>  <type>  <options>  <dump>  <pass>

- `<device>` describes the block special device or remote file system to be mounted; see [#Identifying file systems](https://wiki.archlinux.org/title/fstab#Identifying_file_systems).
- `<dir>` describes the [mount](https://wiki.archlinux.org/title/Mount "Mount") directory.
- `<type>` the [file system](https://wiki.archlinux.org/title/File_system "File system") type.
- `<options>` the associated mount options; see [mount(8) § FILESYSTEM-INDEPENDENT MOUNT OPTIONS](https://man.archlinux.org/man/mount.8#FILESYSTEM-INDEPENDENT_MOUNT_OPTIONS) and [ext4(5) § Mount options for ext4](https://man.archlinux.org/man/ext4.5#Mount_options_for_ext4).
- `<dump>` is checked by the [dump(8)](https://linux.die.net/man/8/dump) utility. This field is usually set to `0`, which disables the check.
- `<fsck>` sets the order for file system checks at boot time; see [fsck(8)](https://man.archlinux.org/man/fsck.8). For the root device it should be `1`. For other partitions it should be `2`, or `0` to disable checking.

## References:

1. [fstab - ArchWiki](https://wiki.archlinux.org/title/fstab)
