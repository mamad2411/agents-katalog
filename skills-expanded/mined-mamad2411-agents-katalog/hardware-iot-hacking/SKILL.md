---
name: hardware-iot-hacking
description: Hardware & IoT hacking — UART/JTAG/SPI/I2C hardware interfaces, firmware
  extraction from flash chips, firmware reverse engineering, binary analysis, radio
  attacks (SDR, BLE, Zigbee), side-channel analysis, and IoT device exploitation.
version: 1.0.0
category: red-teaming
license: MIT
metadata:
  hermes_origin: import
tags:
- hardware
- iot
- firmware
- UART
- JTAG
- SPI
- SDR
- side-channel
- flash-dump
- embedded
related_skills:
- security-orchestrator
- reverse-engineering
- network-pentest
- pentest-workflow
- zero-day-hunting
---

# Hardware & IoT Hacking — Complete Methodology

## Introduction

IoT and embedded device security spans physical hardware interfaces, firmware extraction/reverse engineering, radio protocols, and side-channel attacks.

## 1. Hardware Interfaces

### UART (Universal Asynchronous Receiver/Transmitter)

UART is the most common debug interface on embedded devices. It provides a serial console (root shell or boot log).

```bash
# Finding UART pins
# 1. Visual inspection: 3-4 pins/pads grouped together (TX, RX, GND, VCC)
# 2. Multimeter: Identify GND (continuity to shield), VCC (steady 3.3V/5V)
# 3. Logic analyzer / oscilloscope: TX toggles on boot (data)
# 4. Baud rate detection: common rates 9600, 115200, 57600, 38400

# Connect with USB-UART adapter (FT232, CP2102, CH340)
screen /dev/ttyUSB0 115200
# or
picocom -b 115200 /dev/ttyUSB0
# or
minicom -D /dev/ttyUSB0 -b 115200

# Multi-baud rate detection tool: baudrate.py (from devttys0)
```

### UART Pitfalls

- **Voltage**: Most IoT is 3.3V logic, not 5V. A 5V adapter can fry the board.
- **TX/RX swap**: If no output, swap TX and RX connections.
- **Flow control**: Sometimes RTS/CTS needed; try disabling first.
- **Boot silence**: UART may only output after boot loader finishes.

### JTAG (Joint Test Action Group)

JTAG provides CPU-level debug access: halt processor, read/write memory/registers, flash firmware.

```bash
# Finding JTAG
# 1. Look for 5-20 pin header/pads in rows (TDI, TDO, TMS, TCK, TRST, GND)
# 2. JTAGulator / JTAGenum for pin identification
# 3. Common pinouts: ARM 10-pin, ARM 20-pin, MIPS EJTAG

# Connect with JTAG adapter (FT2232H, J-Link, OpenOCD compatible)
openocd -f interface/ftdi/jtagkey.cfg -f target/stm32f1x.cfg

# GDB via OpenOCD
gdb-multiarch
(gdb) target remote localhost:3333
(gdb) monitor halt
(gdb) monitor flash info
(gdb) dump memory firmware.bin 0x08000000 0x08080000  # dump flash
```

### SPI Flash (Serial Peripheral Interface)

Most IoT devices store firmware on SPI NOR flash chips (8-pin SOIC/WSON).

```bash
# Common flash chips: Winbond W25Qxx, Macronix MX25Lxx, Gigadevice GD25Qxx
# Pinout (8-pin SOIC):
#   1: CS# (Chip Select)  5: DI/IO0 (Data In)
#   2: DO/IO1 (Data Out)  6: CLK (Clock)
#   3: WP#/IO2            7: HOLD#/IO3
#   4: GND                8: VCC (3.3V)

# Extraction methods:
# Method 1: SOIC-8 clip (in-circuit, device powered off)
flashrom -p ch341a_spi -r firmware.bin

# Method 2: Desolder + socket programmer
# Better signal integrity, but destructive

# Method 3: SPI sniffing (logic analyzer)
# Capture all SPI traffic during device operation
sigrok-cli -d fx2lafw --samples 100M -o capture.sr

# Verify dump
hexdump -C firmware.bin | head
binwalk firmware.bin
```

### I2C / TWI (Inter-Integrated Circuit)

Used for sensors, EEPROMs, RTCs, and peripherals.

```bash
# Scan I2C bus for devices
i2cdetect -y 1  # on Raspberry Pi / Bus Pirate

# Dump I2C EEPROM
i2cdump -y 1 0x50  # 24Cxx EEPROM common address
```

### SD/MMC/eMMC

```bash
# eMMC: BGA package, use ISP/SWD mode on SoC
# SD card: standard reader + dd
# ISP (In-System Programming): many SoCs have USB bootloader mode
```

## 2. Firmware Analysis

### Firmware Extraction

```bash
# Step 1: Identify firmware format
file firmware.bin
binwalk firmware.bin

# Common signatures:
# - U-Boot header (0x27051956 magic)
# - SquashFS (hsqs, sqsh, tqsh)
# - JFFS2
# - YAFFS2
# - cramfs
# - ROMFS
# - EXT2/3/4

# Step 2: Extract filesystem
binwalk -e firmware.bin  # auto-extract known formats
# or manually:
dd if=firmware.bin of=squashfs.bin bs=1 skip=<offset>
unsquashfs squashfs.bin

# Step 3: Mount extracted filesystem
sudo mount -o loop rootfs.img /mnt/firmware/
cd /mnt/firmware

# Step 4: Find secrets and vulns
find . -name "*.conf" -o -name "*.ini" -o -name "*.cfg" | xargs grep -l "password"
find . -name "*.pem" -o -name "*.key" -o -name "*.crt"
grep -r "TODO" .  # developer notes often reveal bugs

# Check for hardcoded credentials
grep -rn "admin" etc/ 2>/dev/null
strings bin/busybox | grep -i "password\|secret\|key"
```

### Firmware Emulation

```bash
# Full system emulation with QEMU
# ARM:
qemu-system-arm -M versatilepb -kernel zImage -initrd rootfs.img \
  -nographic -append "console=ttyAMA0"

# MIPS:
qemu-system-mips -M malta -kernel vmlinux -hda rootfs.img \
  -nographic

# Partial emulation (user-mode): run a single binary
qemu-arm -L ./rootfs ./rootfs/bin/binary
qemu-mipsel -L ./rootfs ./rootfs/usr/sbin/httpd

# Firmadyne / FirmAE: automated firmware emulation
```

### Common Firmware Vulnerability Patterns

```python
FIRMWARE_VULNS = {
    'hardcoded_creds': 'Search for admin:admin, root:root, fixed passwords in etc/passwd, config files',
    'backdoors': 'Hidden telnet/SSH on non-standard ports, magic packet triggers',
    'command_injection': 'Web CGI scripts passing user input to system(), popen()',
    'buffer_overflow': 'strcpy/sprintf in network services (httpd, upnpd, snmpd)',
    'debug_services': 'UART shell without auth, JTAG left enabled, ADB enabled',
    'insecure_update': 'Firmware update without signature verification, MITM over HTTP',
    'default_keys': 'Shared SSH host keys across all devices, weak TLS certs',
    'info_leak': 'SNMP public community, debug endpoints exposing config',
}
```

### Binwalk Advanced Usage

```bash
# Entropy analysis (find compressed/encrypted blocks)
binwalk -E firmware.bin

# Scan for file signatures
binwalk -B firmware.bin

# Extract with custom signatures
binwalk --signature firmware.bin

# Disable some scans (faster)
binwalk --dd='.*' firmware.bin  # extract everything
binwalk -Me firmware.bin  # recursive extraction
```

## 3. Radio & Wireless Attacks

### Software-Defined Radio (SDR)

```bash
# Hardware: RTL-SDR ($25), HackRF ($300), LimeSDR, USRP

# Basic spectrum analysis
rtl_power -f 2400M:2483M:1M -g 30 -i 10 antenna.csv
# → Heatmap of 2.4 GHz activity

# FM capture and replay
rtl_sdr -f 433.92M -s 2048000 capture.bin  # capture
./send -f 433.92M capture.bin               # replay

# GQRX / SDRangel: GUI for spectrum browsing

# GNU Radio: build custom demodulators, protocol decoders
gnuradio-companion

# Universal Radio Hacker (URH): protocol analysis + reverse engineering
```

### BLE (Bluetooth Low Energy)

```bash
# Hardware: Ubertooth, Adafruit BLE Sniffer, nRF52840 Dongle

# Passive sniffing (Wireshark + nRF Sniffer)
# Wireshark can decode BLE with nRF Sniffer plugin

# Active attacks
bettercap -eval 'ble.recon on; ble.show'
btlejack -f 37 38 39  # jam + hijack BLE connections
gattacker  # BLE MITM

# GATT service enumeration
gatttool -b <MAC> --primary
gatttool -b <MAC> --characteristics
```

### WiFi Attacks (Beyond WPA2)

```bash
# PMKID capture (no clients needed)
hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=3
hcxpcapngtool -o hash.hc22000 -E essidlist capture.pcapng
hashcat -m 22000 hash.hc22000 rockyou.txt

# WPA3 Dragonblood attacks
# WPA3-Transition: downgrade to WPA2 → capture handshake
# WPA3-SAE side-channel: timing attacks on password encoding

# KRACK attacks (WPA2 4-way handshake)
# Reinstallation of pairwise keys → decryption

# FragAttacks (2021)
# Frame aggregation + fragmentation flaws → inject plaintext frames

# Enterprise WiFi: EAP-TLS, PEAP, EAP-TTLS
# Rogue RADIUS server, certificate validation bypass
hostapd-wpe  # rogue AP with RADIUS to capture MSCHAPv2
asleap  # crack MSCHAPv2 challenge/response
```

### Zigbee / Z-Wave / LoRa

```bash
# Zigbee: 2.4 GHz, used in smart home (Philips Hue, IKEA Trådfri)
# Tools: CC2531 USB dongle + zigbee2mqtt, KillerBee, ApiMote

# Z-Wave: 868/908 MHz, regional
# Tools: Z-Wave.me USB stick, Zniffer

# LoRa: 868/915 MHz, long-range IoT
# Tools: LoRaStik, RNode, rtl_433 (for 433 MHz ISM devices)

# 433 MHz: OOK/ASK, weather stations, doorbells, TPMS, alarms
rtl_433 -f 433920000 -F json  # decode common 433 MHz devices
```

### RFID / NFC

```bash
# Proxmark3 — the universal RFID tool
pm3 --> auto  # auto-detect card type
pm3 --> hf mf rdbl --blk 0 -a -k <key>  # MIFARE Classic read
pm3 --> hf mf chk --1k  # check MIFARE keys
pm3 --> hf iclass read  # iClass (HID)

# Flipper Zero — multi-tool
# NFC: read/emulate MIFARE, NFC-A/B/F/V
# RFID: read/emulate 125kHz HID, EM4100
# Sub-GHz: capture/replay 315/433/868/915 MHz
# iButton: Dallas touch memory
# Infrared: capture/replay IR remotes

# MIFARE Classic attack
mfoc -O card.dmp  # nested attack → recover keys → dump
# Default keys for MIFARE Classic: FFFFFFFFFFFF, A0A1A2A3A4A5, 000000000000
```

## 4. Side-Channel Attacks

### Power Analysis (SPA/DPA)

```python
# SPA: Simple Power Analysis — visual inspection of power trace
# DPA: Differential Power Analysis — statistical correlation

# ChipWhisperer — open source side-channel platform
# Attacks: AES-128 key extraction via CPA (Correlation Power Analysis)

# Setup:
# 1. Connect ChipWhisperer to target board
# 2. Capture power traces during encryption
# 3. Use CPA to correlate Hamming weight models with key bytes
# 4. Extract 16-byte AES key (seconds to minutes)
```

### Fault Injection (Glitching)

```bash
# Voltage glitching: brief voltage drop → CPU skips instruction
# Clock glitching: clock pulse at wrong time → instruction corruption
# EM fault injection: EM pulse near chip → bit flips

# ChipWhisperer-Glitch: voltage + clock glitching
# Targets: skip signature verification, bypass password checks
# Classic: glitch during bootloader → bypass secure boot
```

### Timing Attacks

```python
# Timing side channel: measure response time to infer secrets
# Example: string comparison that returns early on mismatch

def timing_attack(target_func, known_prefix=''):
    """Discover secret byte-by-byte via timing."""
    for byte_pos in range(32):
        for candidate in range(256):
            test = known_prefix + bytes([candidate]) + b'\x00' * (31 - byte_pos)
            start = time.perf_counter_ns()
            target_func(test)
            elapsed = time.perf_counter_ns() - start
            if elapsed > threshold:  # longer = more bytes matched
                known_prefix += bytes([candidate])
                break
    return known_prefix
```

## 5. Automotive / CAN Bus

```bash
# CAN bus: Controller Area Network — vehicle internal network
# Tools: SocketCAN (Linux), can-utils, CANtact, Macchina M2

# Setup SocketCAN
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0

# Sniff CAN traffic
candump can0
cansniffer can0  # grouped by arbitration ID

# Replay / inject CAN messages
cansend can0 123#DEADBEEF12345678

# CAN MITM / bridging
# candump + cansend combined → filter + modify specific IDs

# UDS (Unified Diagnostic Services): ECU reprogramming, security access
# OBD-II adapter + ELM327 or STN1110 chip
```

## 6. Essential Hardware Toolkit

```python
MINIMAL_LAB = {
    'soldering': 'TS100/Pinecil soldering iron, flux, solder wick, tweezers',
    'multimeter': 'UNI-T UT61E, Brymen BM235 (True RMS, capacitance)',
    'logic_analyzer': 'Saleae Logic 8 ($399) or DSLogic Plus ($99)',
    'uart_adapter': 'FT232H breakout (JTAG + UART + SPI + I2C in one)',
    'flash_programmer': 'CH341A ($5) or Dediprog SF100 ($200)',
    'oscilloscope': 'Rigol DS1054Z ($350) or Siglent SDS1104X-E',
    'sdr': 'RTL-SDR v3 ($25) + HackRF One ($300)',
    'rfid_nfc': 'Proxmark3 RDV4 ($300) + Flipper Zero ($169)',
    'jtag_swd': 'J-Link EDU ($60) or ST-Link v2 ($5)',
    'microscope': 'Andonstar AD407 ($180) or similar digital microscope',
    'tools': 'iFixit toolkit, security bit set, lock picks',
    'can_bus': 'CANtact or Macchina M2 + OBD-II cable',
}

# Budget alternatives:
# - Logic analyzer: FX2LP CY7C68013A ($10) + sigrok PulseView
# - Flash programmer: CH341A cheap programmer + SOIC-8 clip
# - SDR: RTL-SDR v3 ($25) alone for 99% of needs
```

## 7. Key Resources

### Books
- *The Hardware Hacking Handbook* (Wagenaar, O'Flynn) — THE bible
- *Practical IoT Hacking* (Fotios Chantzis)
- *IoT Penetration Testing Cookbook* (Guzman, Gupta)
- *Car Hacker's Handbook* (Craig Smith) — automotive/CAN

### Conferences
- **hardwear.io** — dedicated hardware security conference
- **DEF CON** — IoT Village, Hardware Hacking Village, Car Hacking Village
- **Chaos Communication Congress (CCC)** — hardware + firmware
- **Black Hat** — embedded systems track

### GitHub Repos
```
https://github.com/nccgroup/ (various IoT/embedded tools)
https://github.com/exploitagency/ (hardware hacking)
https://github.com/newaetech/chipwhisperer
https://github.com/RFStorm/tools
https://github.com/atlas-0/car-hacking-tools
https://github.com/saleae/SaleaeAnalyzerSDK
```

## Deep Knowledge References

- **references/re-hardware-mobile-reference.md §4-6** — Hardware interface analysis (UART/JTAG/SPI/I2C), firmware extraction and reverse engineering, radio protocol analysis (SDR, BLE, Zigbee, LoRa), side-channel analysis (power/EM fault injection), and automotive/CAN bus analysis.

## Pitfalls

- **Voltage mismatch**: 3.3V vs 5V logic levels is the #1 mistake. Check voltage before connecting.
- **Flash chip specific bitrates**: SPI flash chips have different command sets and maximum clock speeds.
- **Bricking risk**: Flashing wrong firmware can permanently brick devices. Always backup first.
- **Secure boot**: Many modern devices have secure boot + encrypted firmware. Hardware extraction may be impossible.
- **EMI/RFI**: Nearby electronics can corrupt SPI/UART signals. Use short wires and ferrite beads.
- **SMD soldering skill**: QFN/BGA packages need hot air rework station + experience.
- **FCC/legal**: Transmitting on licensed frequencies without authorization is illegal in most countries.
- **RF emissions compliance**: Intentional interference/jamming is illegal. Passive reception + analysis only.
- **Device destruction**: Probing wrong pins can short power → GND and destroy the board. Triple-check pinouts.
- **Read protection**: Many MCUs (STM32, ESP32) have firmware readout protection. May need fault injection to bypass.