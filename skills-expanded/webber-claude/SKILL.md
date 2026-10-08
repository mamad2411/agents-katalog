# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ESP32-S3 LED display controller ("tv-remote") that drives WS2812 RGB LED strips with content from SD card. Features OLED status display, rotary encoder input, WiFi connectivity, and WebSocket remote control.

## Build Commands

```bash
# Set IDF environment (required before any build commands)
export IDF_PATH='/home/conor/esp/v5.4.1/esp-idf'
source $IDF_PATH/export.sh

# Build
idf.py build

# Flash and monitor
idf.py flash monitor

# Clean build
idf.py fullclean && idf.py build

# Configure options
idf.py menuconfig
```

## Architecture

### Task Structure (FreeRTOS)

```
supervisor (super.c)     - Main orchestration, spawns all tasks
├── ui_task             - OLED display rendering, UI state machine
├── tv_task             - LED playback engine, frame interpolation
├── wifi_task           - Station + AP mode connectivity
└── websocket_task      - Remote control messaging
```

Inter-task communication uses FreeRTOS queues (`qRotor` for encoder events, supervisor queue for commands).

### Core Modules

| File | Purpose |
|------|---------|
| `main.c` | Entry point (`app_main`), type definitions |
| `super.c` | Task supervisor, SD card detection, hue state |
| `tv.c` | LED strip control (RMT), frame playback, interpolation |
| `ui/ui_state.c` | UI state machine (12 states), event handling |
| `rotary_encoder.c` | PCNT-based encoder input |
| `oled_i2c.c` | I2C display driver (128x64 SH1106) |
| `sddcard.c` | SD card filesystem, animation file reading |
| `wifi_man.c` | WiFi STA+AP, mDNS, captive portal |
| `server.c` | HTTP server, WebSocket handler |
| `nvs_mgr.c` / `creds.c` | Persistent settings and credentials |

### Key Data Structures (main.h)

- `tv_preferences_t` - User settings (mode, brightness, speed, interpolation)
- `tv_runtime_status_t` - Playback state (filename, frame position)
- `tv_hardware_config_t` - Hardware settings (LED count, resolution, rotor direction)

### TV Modes

`OFF`, `SEQUENTIAL`, `LOOP`, `RANDOM`, `LAMP`, `LIFE` (Conway's Game of Life)

### UI States (ui_state.c)

`idle`, `splash`, `menu`, `projector`, `file_browser`, `brightness`, `tweens`, `millis_dial`, `mode`, `lamp`, `settings`, `about`, `error`, `update`

Button events: `UI_SHORT_PRESS` (100ms), `UI_MEDIUM_PRESS` (500ms), `UI_LONG_PRESS` (3000ms)

## Hardware Pinout

- GPIO 21: WS2812 LED data (RMT)
- GPIO 37/38: Rotary encoder A/B (PCNT)
- GPIO 36: Encoder button
- GPIO 8: SD card detect
- GPIO 17/18: I2C SDA/SCL (OLED)

## File Storage

- **NVS**: User preferences, hardware config, WiFi credentials
- **SPIFFS** (`spiff/`): Web UI assets (HTML/CSS/JS)
- **SD Card** (`/sdcard`): Animation files (raw binary frames)

## Dependencies (managed_components/)

- `espressif/mdns` - Network discovery
- `espressif/led_strip` - WS2812 driver
- `espressif/esp_websocket_client` - WebSocket client

## Animation Format

Raw binary frame files on SD card. Use `giffer.py` in convert/ for conversion from image sequences.
