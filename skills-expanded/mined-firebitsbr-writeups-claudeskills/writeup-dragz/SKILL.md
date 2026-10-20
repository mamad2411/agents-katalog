<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dragz
description: CTF writeups and security challenges by dragz.
---

# Writeups by dragz

Source repository: `/repos/dragz`

## Repository Index

- explorationsincarhacking/README.md
- explorationsincarhacking/articles/obdb_and_udsoncan.md
- explorationsincarhacking/articles/rpiandelm327onbt.md
- explorationsincarhacking/sources/obdbudsoncan/README.md
- explorationsincarhacking/articles/getting_past_the_secure_gateway/getting_past_the_secure_gateway.md

## Writeup Content


### File: explorationsincarhacking/README.md

### Useful tips and tricks for hacking your car.

These short writeups have two intentions:

1. Help myself remember what I achieved and how I did it.
2. Share my findings with others.

_I hope this is useful for others. At this time I'm only a newbie at car hacking as I've only been doing this for a couple of weeks (writing this in Jan 2025)._

### Articles

[Connect Raspberry Pi to an OBDII module with bluetooth](./articles/rpiandelm327onbt.md)

[Combine OBDb and Udsoncan to query and intrepret data](./articles/obdb_and_udsoncan.md)

[Getting past the secure gateway](./articles/getting_past_the_secure_gateway/getting_past_the_secure_gateway.md)


### File: explorationsincarhacking/sources/obdbudsoncan/README.md

# OBDb Python Examples

This directory contains Python scripts demonstrating how to work with OBDb signalset data and communicate with vehicles via CAN bus.

The most important scripts are `query_signalset.py` and `query_signal.py`. The others are mostly for testing the communication.

All scripts are created with heavy use of Claude Sonnet 4 and are therefore a bit overengineered...

## Prerequisites
A working canbus setup on a Linux pc, for instance as described in https://github.com/dragz/explorationsincarhacking/

### OBDb repos


Clone '.schemas' and your vehicle repositories in https://github.com/OBDb/.

```bash
mkdir OBDb
cd OBDb
git clone https://github.com/OBDb/.schemas
git clone https://github.com/OBDb/Hyundai-IONIQ-5
```


### Python Dependencies:
```bash
# Install all dependencies
pip install python-can udsoncan can-isotp

# Verify installations
python3 -c "import can; import udsoncan; import isotp; print('OK')"
```

## Configuration

You can change `config.txt` file to set default values and avoid specifying them in every command.


**Benefits:**
- Run `query_signal.py` and `query_signalset.py` without specifying `--signalset` every time
- Command-line arguments always override config defaults
- Makes scripts more convenient for regular use

## Scripts

### 1. query_vin.py
Query vehicle VIN (Vehicle Identification Number) via CAN bus using UDS protocol.

**Features:**
- UDS Service 0x22 (ReadDataByIdentifier)
- ISO-TP transport layer with automatic 8-byte padding
- Automatic response-id calculation (request-id + 8)
- Scan mode to try multiple common ECU addresses
- VIN decoding with proper filtering

**Usage:**
```bash
# Query VIN from specific ECU
python3 query_vin.py --request-id 0x7C7

# Query with custom response ID
python3 query_vin.py --request-id 0x7C7 --response-id 0x7CF

# Scan multiple ECUs for VIN
python3 query_vin.py --scan

# Query specific DID
python3 query_vin.py --request-id 0x7C7 --did 0xF190
```

**Dependencies:**
```bash
pip install python-can udsoncan can-isotp
```

---

### 2. query_did.py
Query any DID (Data Identifier) from the vehicle and display as hex string.

**Features:**
- Generic DID querying (not limited to VIN)
- Raw hex output display
- Optional ASCII decoding for text data
- Same reliable UDS/ISO-TP setup as query_vin.py

**Usage:**
```bash
# Query VIN (outputs as hex)
python3 query_did.py --did 0xF190 --request-id 0x7C7

# Query ECU serial number
python3 query_did.py --did 0xF18C --request-id 0x7C7

# Try ASCII decoding
python3 query_did.py --did 0xF190 --request-id 0x7C7 --ascii

# Increase timeout for slow ECUs
python3 query_did.py --did 0x0100 --request-id 0x7C7 --timeout 5.0
```

**Common DIDs:**
- `0xF190` - VIN (Vehicle Identification Number)
- `0xF187` - Vehicle Manufacturer Spare Part Number
- `0xF18A` - Vehicle Manufacturer ECU Software Number
- `0xF18C` - ECU Serial Number
- `0xF191` - ECU Hardware Version Number
- `0xF19E` - System Supplier ECU Software Number

---

### 3. query_signalset.py
Search and parse OBDb signalset JSON files to discover available commands and signals.

**Features:**
- Load and parse signalset JSON files
- Search commands by service type, PID, or CAN ID
- Display detailed signal information (format, range, units)
- List all available signals grouped by path
- Decode example responses

**Usage:**
```bash
# View signalset summary (uses config.txt default if configured)
python3 query_signalset.py

# Or specify signalset explicitly
python3 query_signalset.py -s ../Hyundai-IONIQ-5/signalsets/v3/default.json

# Search by service 0x22
python3 query_signalset.py --service 0x22

# Search by specific PID
python3 query_signalset.py -s ../Hyundai-IONIQ-5/signalsets/v3/default.json --service 0x22 --pid 0xE001

# Search by CAN ID
python3 query_signalset.py -s ../Hyundai-IONIQ-5/signalsets/v3/default.json --can-id 0x74C

# List all signals
python3 query_signalset.py -s ../Hyundai-IONIQ-5/signalsets/v3/default.json --list-signals

# Show verbose signal details
python3 query_signalset.py -s ../Hyundai-IONIQ-5/signalsets/v3/default.json --service 0x22 --pid 0xE001 --verbose
```

**Dependencies:**
Uses the OBDb Python modules from `.schemas/python`:
- `can.signals` - SignalSet, Command, Signal parsing
- `can.command_registry` - Command registry and decoding
- `signalsets.loader` - Signalset file loading utilities

---

### 4. query_signal.py
Query a specific signal from the vehicle by signal ID.

**Features:**
- Automatically finds signal in signalset
- Determines which command contains the signal
- Queries vehicle via UDS using the correct service/PID
- Decodes and displays just the requested signal value
- Auto-detects CAN IDs from signalset
- Info mode to show signal details without querying
uses config.txt default if configured)

**Usage:**
```
python3 query_signal.py --signal IONIQ5_HVBAT_HV_BATTERY_VOLTAGE

# Or specify signalset explicitly
python3 query_signal.py --signal IONIQ5_HVBAT_HV_BATTERY_VOLTAGE \
    --signalset ../Hyundai-IONIQ-5/signalsets/v3/default.json

# Query state of charge with explicit request ID
python3 query_signal.py --signal IONIQ5_HVBAT_SOC_VCMSuery state of charge with explicit request ID
python3 query_signal.py --signal IONIQ5_HVBAT_SOC_VCMS \
    --signalset ../Hyundai-IONIQ-5/signalsets/v3/

# Show signal information without querying
python3 query_signal.py --signal IONIQ5_VSS_HD

# Show signal information without querying
python3 query_signal.py --signal IONIQ5_VSS_HD \
    --signalset ../Hyundai-IONIQ-5/signalsets/v3/default.json --info

# Query with custom timeout
python3 query_signal.py --signal IONIQ5_ODO_KM \
    --signalset ../Hyundai-IONIQ-5/signalsets/v--timeout 5.0
```

**Note:** Both `query_signal.py` and `query_signalset.py` support `config.txt` for default signalset paths.
**How it works:**
1. Loads the signalset JSON file
2. Searches for the signal by ID
3. Extracts the command (service/PID/CAN IDs)
4. Connects to CAN bus via udsoncan
5. Queries the ECU with the appropriate UDS command
6. Decodes only the requested signal from the response
7. Displays the value with units

**Dependencies:**
```bash
pip install python-can udsoncan can-isotp
```

---

## CAN Interface Setup

All scripts require a configured CAN interface (typically `can0`).

### Setup SocketCAN:
```bash
# Bring up CAN interface with 500kbps bitrate
sudo ip link set can0 up type can bitrate 500000

# Verify interface is active
ip link show can0

# Monitor CAN traffic
candump can0
```

### Common CAN bitrates:
- 500000 (500 kbps) - Most common for automotive
- 250000 (250 kbps)
- 125000 (125 kbps)

---

## OBDb Python API

The `.schemas/python` directory contains the core OBDb Python modules:

### Core Modules:
- **`can/signals.py`** - Signal, Command, SignalSet classes with JSON parsing
- **`can/command_registry.py`** - CommandRegistry for searching and decoding
- **`can/can_frame.py`** - CAN frame handling
- **`signalsets/loader.py`** - Load signalsets by model year or path
- **`overlapping_signals.py`** - Signal validation utilities
- **`json_formatter.py`** - JSON formatting and validation

### Example API Usage:
```python
from can.signals import SignalSet
from can.command_registry import CommandRegistry

# Load signalset from JSON
with open('path/to/signalset.json', 'r') as f:
    signalset = SignalSet.from_json(f.read())

# Search for commands
for cmd in signalset.commands:
    if cmd.header == 0x74C:
        print(f"Found: {cmd.id}")
        for signal in cmd.signals:
            print(f"  - {signal.name}")
```

---

## Vehicle-Specific Notes

### Hyundai IONIQ 5
- VIN available at: `0x7C7 → 0x7CF`, DID `0xF190`
- Battery info at: `0x744 → 0x74C`, various PIDs (`0xE001`, `0xE002`, `0xE003`)
- Motor info at: `0x7E3 → 0x7EB`, DID `0xE001`

---

## Troubleshooting

### CAN Interface Issues:
```bash
# Check if interface exists
ip link show can0

# Check for errors
ip -details -statistics link show can0

# Restart interface
sudo ip link set can0 down
sudo ip link set can0 up type can bitrate 500000
```

### Permission Errors:
Run with `sudo` or add user to appropriate groups:
```bash
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

### No Response from ECU:
- Verify vehicle ignition is ON
- Check CAN bitrate matches vehicle (usually 500kbps)
- Try different request/response IDs
- Increase timeout: `--timeout 5.0`
- Use `candump can0` to verify traffic

---

## Additional Resources

- **OBDb Repository**: https://github.com/OBDb
- **UDS Specification**: ISO 14229
- **ISO-TP Protocol**: ISO 15765-2
- **SocketCAN Documentation**: https://www.kernel.org/doc/html/latest/networking/can.html



### File: explorationsincarhacking/articles/getting_past_the_secure_gateway/getting_past_the_secure_gateway.md

# Getting past the secure gateway.

## Background
Most modern cars has a security gateway (SGW) that filters traffic so that one cannot read canbus traffic or send commands through the OBDII port. To get to the canbus(es) one have to physically connect to the can wiring in the car.
For an introduction to CANBUS technology see 
[this excellent article](https://www.csselectronics.com/pages/can-bus-simple-intro-tutorial).


This writeup is about connecting into the canbus behind the SGW of a fairly modern car, the Hyundai Ioniq 5 model year 2022, without harming any wiring. Beware, this is not for the faint hearted and you can void your warranty by doing this.

## The SGW

The SGW in the Ioniq 5 is named ICU, Integrated Controller Unit (not to be confused with the infamous ICCU that still is the bane of these cars). The ICU is placed under the dash on the driver side right behind the OBDII port and can be dismounted fairly easily after removing a couple of panels.

Get hold of a service manual by searching r/ioniq5 on reddit and look for how to remove "Crash pad lower panel".
![ICU placement](iculocation.png)

## Wiring layouts
By looking through the wiring harness layouts and schematics in the repair shop manuals one can see that the car has 10 different CAN-buses. Where 8 of them are coming together in one connector on the back of the ICU which acts as a network hub/gateway between them.

![ICU connector](icu-junction-block.png)

## Getting a harness

It turns out that the connector above is a nearly standard 32-pin connector used in other cars and extension harnesses can be found on aliexpress: https://www.aliexpress.com/item/1005007839039821.html

Many thanks to the friendly folks at r/CarHacking for guiding me in the right direction here, https://www.reddit.com/r/CarHacking/comments/1kdcalf/connector_type/

Remark, one needs to remove some plastic from the harness plugs to fit into the ICU-connectors:

![ICU Connector](./icuconnector1.jpg)
![ICU Connector](./icuconnector2.jpg)
(Unmodified connector on the left.)

Care is recommended as the pins are fragile and bend easily. Buy two or more in case something breaks. Use a fine woodworking tool to cut/scrape away the excess plastic.

## Tapping into the CAN-buses

Patching into the wiring on the harness is straight forward using T-taps.
Original extension harness from aliexpress:
![alt text](origharness.png)

Harness with T-taps for all canbuses listed in the ICU-H schematics:
![alt text](harnesswithtaps.png)
Remember to also tap into ground on connector 16 to get good quality signals. It is also recommended to use connectors that only fits one way on the tap ends so one do not swap can high and can low. 

The full setup from laptop to harness:
![alt text](laptoptoharness.png)

In car:
![alt text](harnessbehindicu.png)
![alt text](icuinplacewithcabling.png)
![alt text](laptopconnectedincar.png)

## Closing remarks.

### Fitting the connectors

The connector, ICU-H, is on the back side of the ICU and the easiest way to ensure that the harness with the modified plugs fits well is to entirely dismount the ICU and test the connectors.
![alt text](icubackside.jpg)




### File: explorationsincarhacking/articles/obdb_and_udsoncan.md

# Combining OBDb and Udsoncan to query car data

## Introduction

The OBDb database (https://github.com/OBDb/) contains a lot of schemas to 
interpret UDS data for a wide variety of cars and Udsoncan 
(https://udsoncan.readthedocs.io/en/latest/index.html) provides an industrial strenght python module for communicating with a cars UDS interface.  However, 
it can be a challenge to get all the bits together to get the communication 
flowing and interpreting the data correctly.

## Source code examples

The python scripts in [../sources/obdbudsoncan/](../sources/obdbudsoncan/) has some complete examples on how to use Udsoncan for the communication and OBDb for interpreting the results.



### File: explorationsincarhacking/articles/rpiandelm327onbt.md

## Table of Contents

- [Introduction](#introduction)
- [Hardware setup](#hardware-setup)
- [Software setup](#software-setup)
  - [Installing the can327 kernel module](#installing-the-can327-kernel-module)
  - [Installing the CANBUS tools](#installing-the-canbus-tools)
- [Setting up the Bluetooth connection](#setting-up-the-bluetooth-connection)
- [Setting up the CANBUS](#setting-up-the-canbus)
- [Testing the setup](#testing-the-setup)
- [Closing the connection](#closing-the-connection)
- [Troubleshooting](#troubleshooting)
  - [Checking that the OBDII device is working](#checking-that-the-obdii-device-is-working)
  - [Monitoring the bluetooth traffic](#monitoring-the-bluetooth-traffic)
  - [Watch the kernel messages](#watch-the-kernel-messages)

## Introduction

This is a short writeup of the steps needed to connect an OBDII
bluetooth adapter to a Raspberry Pi4. The process should be very
similar on a regular PC running Linux as long as it has a working
bluetooth module.

_NOTE1_: This writeup only concerns the process of getting the hardware
communication going. It is not a comprehensive guide to CANBUS nor
how to hack a car.

_NOTE2_: Modern cars do not send the CANBUS traffic to the diagnostic port, so it is in most cases not possible to sniff the bus traffic using this interface. One can use UDS (Unified Diagnostic Services) to talk to the car through the OBDII interface. A good starting point is the introductory material at [CarHacking on Reddit](https://www.reddit.com/r/CarHacking/) (and to join the friendly community there).

## Hardware setup

- A Raspberry Pi running Raspbian (Based on Debian 12 Bookworm).
- A OBDII bluetooth adapter (I'm using a VGATE Pro).
- A car with an OBDII port.

## Software setup

The kernel module `can327` needed for CAN communication to the ELM327 is not
included in the Raspbian Linux release and need to be compiled
separately. Using `dkms` one can automate this process and have the
module recompiled every time the kernel is upgraded.

### Installing the `can327` kernel module

To install a kernel module one needs the kernel headers and dkms:

```
sudo apt update
sudo apt install build-essential linux-headers-$(uname -r) dkms

```

Fetch `can327.c` from the kernel source tree. (it doesn't seem to change much so any recent version of the kernel source should do)

```
https://github.com/torvalds/linux/blob/master/drivers/net/can/can327.c
```

Copy it to the right place and create a dkms setup

```
sudo mkdir -p /usr/src/can327-1.0/
sudo cp can327.c /usr/src/can327-1.0/
```

Create the dkms config and Makefile in the above directory

`/usr/src/can327-1.0/Makefile`:

```
obj-m += can327.o

all:
        make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
        make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

(remember the tabs in the Makefile if you're copying this)

`/usr/src/can327-1.0/dkms.conf`:

```
PACKAGE_NAME="can327"
PACKAGE_VERSION="1.0"
BUILT_MODULE_NAME[0]="can327"
DEST_MODULE_LOCATION[0]="/kernel/drivers/net/can/"
AUTOINSTALL="yes"
```

Register the module with dkms, build and install it:

```
sudo dkms add -m can327 -v 1.0
sudo dkms build -m can327 -v 1.0
sudo dkms install -m can327 -v 1.0
```

If everything is correct you should now see something like

```
sudo dkms status
can327/1.0, 6.6.62+rpt-rpi-v8, aarch64: installed

```

and

```
modinfo can327
filename:       /lib/modules/6.6.62+rpt-rpi-v8/updates/dkms/can327.ko.xz
author:         Max Staudt <max@enpas.org>
license:        GPL
description:    ELM327 based CAN interface
alias:          tty-ldisc-30
srcversion:     7F50115BF9D717366AF765F
depends:        can-dev
name:           can327
vermagic:       6.6.62+rpt-rpi-v8 SMP preempt mod_unload modversions aarch64
sig_id:         PKCS#7
signer:         DKMS module signing key
sig_key:        51:9A:4B:23:34:63:5B:AE:0A:79:11:DF:7E:C0:AD:2E:D6:38:25:B5
sig_hashalgo:   sha512
signature:      08:60:D3:B3:93:7C:2D:BB:75:D1:FA:08:EC:E5:E7:5E:76:2F:1C:90:
                E6:9F:BE:33:55:E3:2F:C6:A8:68:8F:FF:BF:84:81:AB:52:0C:3B:2A:
                FA:1F:F3:62:A4:68:07:7B:B7:6A:DD:3E:F0:83:7A:79:4C:F0:15:6F:
                91:D6:56:64:C7:4D:C7:18:A4:0A:BC:0F:C8:53:E9:B0:AB:72:70:23:
                BC:3A:E2:45:41:8E:8D:33:C8:5F:6D:73:8F:97:93:EA:9F:C1:D3:78:
                6D:7E:1E:B0:BA:29:E6:9C:93:77:2F:F6:62:AA:B1:D0:C4:59:96:BA:
                B9:1A:DD:BE:97:02:48:D1:D2:B4:FC:63:A7:01:1C:AD:2F:BF:6A:D2:
                03:17:D8:B7:E3:FE:42:39:7C:5F:1E:F5:43:2A:33:C5:ED:4A:2D:11:
                B0:3B:9D:27:EB:4B:64:8E:92:97:BD:3C:9C:78:DE:46:62:B7:EC:95:
                5B:7E:F7:BD:54:EF:94:00:DB:89:87:AD:2C:B2:00:6D:B4:CE:99:4E:
                A0:55:AB:C6:18:F8:EA:E3:66:D3:CA:E1:0A:39:72:4A:05:C9:4B:27:
                30:07:85:A8:C9:3F:46:5F:39:97:BF:36:83:40:A1:15:2C:C1:E5:07:
                A9:9A:4E:2B:F6:78:52:80:79:C1:6E:A0:2C:5E:6D:93
```

### Installing the CANBUS tools

The kernel now has the neccessary modules for the CANBUS communication and we only need the userspace utils:

```
sudo apt install can-utils
```

## Setting up the Bluetooth connection

Raspbian includes all the tools needed for bluetooth connection so this is smooth sailing. Put the OBDII device into the diagnostic port in the car. (Many devices has an idle timeout to save power so you might have to reseat it if it has been sitting idle for a while)

Start scanning

```
$ bluetoothctl power on
Changing power on succeeded
$ bluetoothctl --timeout 5 scan on
Discovery started
[CHG] Controller DC:A6:32:34:62:E5 Discovering: yes
[NEW] Device 78:21:84:CF:ED:4A ZAP097907
[NEW] Device CB:EA:EF:A7:30:4F CB-EA-EF-A7-30-4F
[NEW] Device DE:52:BE:9C:16:2D TT214H BlueFrog
[NEW] Device 8C:79:F5:89:3F:EF 8C-79-F5-89-3F-EF
[NEW] Device C4:DE:E2:E1:E1:92 CAF-P583S-KEU
[NEW] Device 50:54:7B:81:2D:6F BM6
[NEW] Device D2:E0:2F:8D:53:6C IOS-Vlink
[NEW] Device 74:46:B3:54:5F:BD S6b01d8bf167b1aafC
```

In this case the device of interest is the one named IOS-Vlink.

```
$ bluetoothctl trust D2:E0:2F:8D:53:6C
$ bluetoothctl connect D2:E0:2F:8D:53:6C
```

It might ask for a PIN, usually it is 0000 or 1234. It should be documented in the setup guide.

If the connection is successful one must bind the device to a pty.

```
sudo /usr/bin/rfcomm bind rfcomm0 D2:E0:2F:8D:53:6C
```

## Setting up the CANBUS

The SocketCAN kernel interface is a standard way to communicate over the CANBUS and makes
programming communication very easy. It is included in the Raspbian build and works out of the box.

Connect the pty attached to `rfcomm0` to a line discipline

```
sudo ldattach --debug --speed 38400 --eightbits --noparity --onestopbit 30 /dev/rfcomm0
```

Now you have something that looks like a network device, `can0`. It needs to be configured before
you can talk to it

```
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 500000  listen-only off
sudo ip link set can0 up
```

## Testing the setup

Create to terminals: Run `candump can0` on the first and then the command

```
cansend can0 '7DF#0201010000000000'
```

on the second terminal. You should now see something like this on the first terminal running `candump`:

```
$ candump can0
  can0  7DF   [8]  02 01 01 00 00 00 00 00
  can0  7EE   [8]  06 41 01 00 04 00 00 AA
  can0  7EC   [8]  06 41 01 00 00 00 00 AA
  can0  5EA   [8]  06 41 01 00 04 00 00 AA
  can0  7EB   [8]  06 41 01 00 04 00 00 AA
  can0  74C   [8]  06 41 01 00 04 00 00 AA
  can0  7ED   [8]  06 41 01 00 04 00 00 AA
```

You have now a working connection to the car's CANBUS. The details in the answer will vary between car brands but if `candump` only shows one line the car has not responded. The first line is just the data from `cansend`.

## Closing the connection

Do most of the steps in reverse

```
$ sudo killall ldattach
$ sudo ip link set can0 down
$ sudo rfcomm unbind /dev/rfcomm0
$ bluetoothctl disconnect D2:E0:2F:8D:53:6C
$ bluetoothctl power off
```

## Troubleshooting

The chain of things that need to be connected is long and the cheap OBDII devices are flaky.

### Checking that the OBDII device is working.

Minicom can be used to talk directly to the device using AT-commands. After doing bind to `/dev/rfcomm0` and before running `ldattach` run

```
minicom -D /dev/rfcomm0
```

and try to type the command `ATZ` it should then respond with the ELM327 protocol number. Mine says `ELM 2.3`. Quit minicom with `Ctrl-A q` to quit without hanging up. If you use `Ctrl-A x` it will close the bluetooth connection.

### Monitoring the bluetooth traffic

Run `btmon` while trying cansend. If it shows activity the can traffic goes over the bluetooth connection and you have a healthy connection.

### Watch the kernel messages

If you see something like this the connection is not healthy

```
$ dmesg -T
[Sat Feb  1 14:10:19 2025] can0: Received illegal character 0a.
[Sat Feb  1 14:10:19 2025] can0: bus-off
[Sat Feb  1 14:10:19 2025] can0: ELM327 misbehaved. Blocking further communication.
[Sat Feb  1 14:24:39 2025] can0 (unregistered): can327 off rfcomm0.

```

Try to reconnect using `bluetoothctl`. You might have to rebind etc.

<!-- This is **bold** text, and this is _emphasized_ text. -->

