---
name: esp32-real-hardware-flash
description: Use when flashing or testing ESP32 firmware on real hardware over USB — uploading via PlatformIO, opening the serial port for boot logs, configuring WiFi for home networks, or when the upload fails with "Could not open port" / "Operation not permitted".
---

# ESP32 Real Hardware Flash + WiFi

## Overview

Flash firmware to a physical ESP32 over USB and verify it boots + connects WiFi. Works alongside [wokwi-mcp-testing] (sim) — this skill is for the real board.

## When to Use

- First flash of a new ESP32 (PlatformIO `pio run -t upload`)
- Debug why upload fails to open the serial port
- Set up WiFi on real hardware (home SSID, static vs DHCP)
- Verify boot: WiFi connect + IP + web server start

## Key Rule: Bash tool cannot open serial O_RDWR on macOS

Claude's Bash tool (even with sandbox disabled) gets `Operation not permitted` (EPERM) opening `/dev/cu.*` with `O_RDWR` — esptool/pyserial need O_RDWR, so **uploads fail with "Could not open /dev/cu.usbserial-XXXX, the port doesn't exist"** (esptool masks EPERM). Read-only opens (`O_RDONLY`, e.g. `dd`) succeed.

**Fix: give the user the commands to run in their own terminal.** Do not keep retrying from Bash.

## Flash Workflow (user runs these)

```bash
cd <project>
export PATH="/Users/hoang/.nvm/versions/node/v24.18.0/bin:/opt/miniconda3/bin:$PATH"
~/.platformio/penv/bin/pio run -t upload --upload-port /dev/cu.usbserial-2410
```

**Monitor boot log:**
```bash
~/.platformio/penv/bin/pio device monitor --port /dev/cu.usbserial-2410 --baud 115200
```

If no log appears: tell user to press **EN/RESET** on the board.

## Identifying the Port

- Chip on cheap dev boards is usually **CH340**: `VID 0x1a86 PID 0x7523` → `/dev/cu.usbserial-XXXX`
- Detect: `ls /dev/cu.*` (ignore `cu.Bluetooth-Incoming-Port`), or `system_profiler SPUSBDataType` for VID/PID
- Verify `pio device list` sees it

## WiFi Config (real hardware)

```cpp
const char* WIFI_SSID = "HOME_SSID";
const char* WIFI_PASS = "pass1234";
```

- **Credentials never committed** — they sit in source for a local demo; flag before any commit
- ESP32 is **2.4GHz only** — 5GHz SSID won't connect (symptom: `WiFi connect timeout`)
- **Prefer DHCP + mDNS over static IP** — `esp-light.local` name is stable, self-heals on network change, no IP conflict risk. Static IP only if mDNS fails or port-forwarding needs a fixed address
- Verify via serial log: expect `WiFi connected, IP: 192.168.x.x` then `HTTP server started`; open browser to the IP or mDNS name

## Common Mistakes

| Mistake | Fix |
|---|---|
| Upload fails "port doesn't exist" from Bash | User runs the command in their own terminal (O_RDWR blocked in Bash tool) |
| No serial output after flash | Press EN/RESET; monitor may need restart |
| `WiFi connect timeout` | Wrong SSID/pass, or router is 5GHz-only |
| Committed WiFi password | Strip/guard before commit, or use a config that reads env |
| Wrong port path | `cu.usbserial-*` (CH340), not Bluetooth port |
