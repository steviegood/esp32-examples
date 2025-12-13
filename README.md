# ESP32 Examples

## Arduino Examples
These are a series of examples made using sketches in the Arduino IDE

### blinking_led

- Initial project: Getting Started With ESP32 on a Mac: Blink and LED
- URL: https://www.instructables.com/Getting-Started-With-ESP32-on-a-Mac-Blink-and-LED/


## Micropython Examples

### esptool
This involves installing the required MicroPython firmware to the esp32. We first need to download the esptool Python package, having created a virtual environment:

```
% cd working-dir
% python -m venv venv
% source venv/bin/activate
% pip install esptool
```

### Micropython firmware

Next we must download the relevant Micropython firmware. We use the version here:

- https://micropython.org/resources/firmware/ESP32_GENERIC-20250911-v1.26.1.bin

Now we identify the correct device for interacting with the esp32:

```
% ls /dev/cu*usb*
/dev/cu.usbserial-1420
```

Finally, we first erase the current firmware, then install the one downloaded above:

```
% esptool erase_flash
esptool v5.1.0
Connected to ESP32 on /dev/cu.usbserial-1420:
Chip type:          ESP32-D0WD-V3 (revision v3.1)
Features:           Wi-Fi, BT, Dual Core + LP Core, 240MHz, Vref calibration in eFuse, Coding Scheme None
Crystal frequency:  40MHz
MAC:                88:57:21:b6:83:9c

Stub flasher running.

Flash memory erased successfully in 6.4 seconds.

Hard resetting via RTS pin...
```

```
% esptool --port /dev/cu.usbserial-1420 --baud 460800 write-flash 0x1000 firmware/ESP32_GENERIC-20250911-v1.26.1.bin 
esptool v5.1.0
Connected to ESP32 on /dev/cu.usbserial-1420:
Chip type:          ESP32-D0WD-V3 (revision v3.1)
Features:           Wi-Fi, BT, Dual Core + LP Core, 240MHz, Vref calibration in eFuse, Coding Scheme None
Crystal frequency:  40MHz
MAC:                88:57:21:b6:83:9c

Stub flasher running.
Changing baud rate to 460800...
Changed.

Configuring flash size...
Flash will be erased from 0x00001000 to 0x001a8fff...
Wrote 1734416 bytes (1137589 compressed) at 0x00001000 in 30.1 seconds (460.2 kbit/s).
Hash of data verified.

Hard resetting via RTS pin...
```

### rshell
We will use rshell to communicate with the esp32 board. Install it as below:

```
% pip install rshell
```

### mpy-cross
This is a cross-compiler that can convert traditional .py scripts into binaries, which saves space on esp32 boards:

```
% pip install mpy-cross
Collecting mpy-cross
  Downloading mpy_cross-1.26.1.post2-py2.py3-none-macosx_11_0_universal2.whl.metadata (3.8 kB)
Downloading mpy_cross-1.26.1.post2-py2.py3-none-macosx_11_0_universal2.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 6.1 MB/s  0:00:00
Installing collected packages: mpy-cross
Successfully installed mpy-cross-1.26.1.post2
```

### Connecting to the esp32
```
sudo rshell -b 115200 -p /dev/cu.usbserial-1420 -d -a
```

### Reading and Writing Files to esp32
When using rshell, the contents of the esp32 are in a special directory called /pyboard. This means you can use rshell to read and copy files:

```
# Copy file onto esp32 from local directory
cp myfile.py /pyboard
# List files on esp32
ls /pyboard
# Copy file from esp32 to local directory
cp /pyboard/boot.py .
```

### Examples for Blinking LEDs
- https://www.instructables.com/Getting-Started-With-Python-for-ESP8266-ESP32/
- https://techexplorations.com/guides/esp32/micropython-with-the-esp32/13-micropython-shell/
- https://randomnerdtutorials.com/micropython-esp32-deep-sleep-wake-up-sources/


