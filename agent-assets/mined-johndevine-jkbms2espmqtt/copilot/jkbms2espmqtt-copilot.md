# JKBMS2ESPMQTT Firmware - AI Agent Instructions

> **For AI Coding Agents**: This file provides essential knowledge for working productively with this ESP32 firmware codebase. Located in project root for easy access.

## Project Overview
ESP32 firmware that bridges JK BMS (Jikong Battery Management System) data to MQTT via RS485. Single-file architecture (`src/main.c`) with embedded web server for configuration and comprehensive BMS + ESP32 system monitoring.

## Architecture & Key Components

### Core Data Flow
1. **RS485 → BMS Communication**: UART2 (pins 16/17) reads from JK BMS using proprietary protocol
2. **Data Processing**: Parses 30+ BMS fields into structured `bms_data_t` with validation/CRC checking  
3. **MQTT Publishing**: Publishes comprehensive JSON (~2.9KB) to configurable topics every 5s (default)
4. **Web Configuration**: Captive portal on boot button press for WiFi/MQTT setup

### Single-File Architecture Pattern
- **Everything in `src/main.c`**: ~2320 lines containing all functionality
- **Function Organization**: Grouped by concern (UART, MQTT, WiFi, HTTP, NVS storage)
- **Global State**: Configuration stored in NVS, runtime state in global variables
- **Event-Driven**: FreeRTOS tasks with event handlers for WiFi/MQTT

### Critical Development Workflows

#### Build & Deploy Sequence
```bash
# Complete deployment (firmware + web interface)
pio run --target buildfs    # Build SPIFFS filesystem  
pio run --target uploadfs   # Upload web interface
pio run --target upload     # Upload firmware
pio device monitor --baud 115200  # Monitor serial output
```

#### Version Management
- Source of truth: `version.txt` (project root)
- Build-time define: `APP_VERSION_STR` injected by `firmware/set_version.py`
- **Critical**: Do not add runtime version files; web UI must use compiled version

#### Partition Scheme (partitions.csv)
- OTA-ready: dual app partitions (app0/app1) for future OTA updates
- SPIFFS: 1.5MB for web interface assets (`data/` directory)
- NVS: 20KB for configuration persistence

### Project-Specific Patterns

#### NVS Key Naming Convention
- **15-character limit**: ESP-IDF restriction (e.g., `"watchdog_cnt"` not `"watchdog_counter"`)
- **Namespace**: All keys use `"wifi_storage"` namespace regardless of function
- **Persistence**: WiFi, MQTT, intervals, BMS topics, pack names, watchdog counters

#### MQTT JSON Structure Pattern
```c
// Structured sections for 30+ BMS fields + ESP32 processor metrics
"processor": {
  "WiFiRSSI": 75,                  // WiFi signal strength (% - 0-100%)
  "IPAddress": "192.168.1.150",    // Current IP address
  "CPUTemperature": 32.0,          // ESP32 temperature (°C - placeholder*)
  "SoftwareVersion": "1.3.0",      // Firmware version
  "WDTRestartCount": 2             // Watchdog restart counter
},
"pack": {
  "packName": "configurable",      // First field - user-defined identifier  
  "systemStatus": {...},           // MOSFET states, balancing
  "systemConfig": {...},           // Capacity, calibration, protection
  "temperatureProtection": {...},  // All temperature thresholds
  "systemInfo": {...}              // Device ID, version, working time
},
"cells": {...}                      // Individual cell voltages
```

#### Hardware Abstraction
- **Heartbeat LED**: GPIO2 - flashes ONLY on successful MQTT publish (not periodic)
- **Software Watchdog**: 10× sample interval timeout, auto-reset on MQTT failures
- **Boot Button Logic**: 10-second window on startup for captive portal entry

### Integration Points

#### External Dependencies  
- **ESP-IDF 5.4.0**: Framework dependency with specific menuconfig requirements
- **Supporting Systems**: Optional Docker stack (InfluxDB, Grafana, Node-RED) in `Supporting systems/`
- **Hardware**: MAX485 RS485-to-TTL converter required for BMS communication

#### Configuration Interface
- **Captive Portal**: Triggered by boot button (GPIO0) during 10s startup window
- **Web Endpoints**: `/params.json` (config data), `/update` (save config), `/parameters.html` (UI)
- **Field Validation**: Manual SSID entry (no WiFi scanning), URL validation for MQTT brokers

### Debugging & Monitoring

#### Enabling Debug Output
Debug output is controlled by two mechanisms for different types of information:

**1. Debug Logging Flag (Application Debug)**
```c
// In src/main.c around line 71
static bool debug_logging = false;  // Production (minimal output)
static bool debug_logging = true;   // Development (verbose output)
```

**2. ESP Log Level (System Debug)**
```c
// In app_main() - toggle for development
esp_log_level_set("*", ESP_LOG_WARN);   // Production (warnings/errors only)
esp_log_level_set("*", ESP_LOG_INFO);   // Debug mode (info + warnings/errors)
esp_log_level_set("*", ESP_LOG_DEBUG);  // Full debug (all messages)
```

**Debug Output Types:**
- **debug_logging = true**: BMS data parsing details, cell voltages, temperatures, MQTT payload info
- **ESP_LOG_INFO**: MQTT connection status, system initialization, successful operations
- **ESP_LOG_DEBUG**: Detailed protocol debugging, frame parsing, CRC validation

#### BMS Protocol Debugging
- **Frame Structure**: Start marker (0x4E), length, data, CRC, end marker (0x68)
- **Field Parsing**: Uses lookup table for field ID to name mapping
- **Data Validation**: CRC16 verification, frame length checks

#### Watchdog Counter Tracking
- **Purpose**: Counts automatic system resets due to MQTT communication failures
- **Storage**: Persisted in NVS, displayed in web interface
- **Reset Logic**: Only increments on watchdog timeout, not manual reboots

### Common Modification Patterns

#### Adding New BMS Fields
1. Update field lookup table in `parse_and_print_bms_data()`
2. Add to appropriate JSON section in `publish_bms_data_mqtt()`
3. Test with actual BMS hardware (protocol varies by BMS version)

#### Configuration Parameters
1. Add NVS load/save functions following existing pattern (`load_*_from_nvs()`)
2. Update HTTP handlers: `params_json_get_handler()` and `params_update_post_handler()`
3. Add form field to `data/parameters.html`

#### Development Debugging Workflow
1. **Enable Debug Output**: Set `debug_logging = true` and `ESP_LOG_INFO` level
2. **Build & Upload**: `pio run -t upload` for firmware + `pio run -t uploadfs` for web files
3. **Monitor Output**: `pio device monitor` to see console output in real-time
4. **BMS Protocol Issues**: Look for CRC errors, frame parsing warnings, field ID mismatches
5. **MQTT Debugging**: Check connection events, payload structure, topic configuration
6. **Return to Production**: Set `debug_logging = false` and `ESP_LOG_WARN` before deployment

#### Network/MQTT Changes
- **WiFi Events**: Handled in unified event handler with connection retry logic
- **MQTT Reconnection**: Automatic via ESP-IDF client with event-driven reconnects
- **Topic Structure**: Configurable base topic + "/BMS" suffix pattern

## Quick Reference

### Essential Files
- `src/main.c` - All firmware logic (~2320 lines)
- `data/parameters.html` - Web configuration interface  
- `platformio.ini` - Build configuration (ESP-IDF 5.4.0)
- `partitions.csv` - Memory layout (OTA-ready)
- `README.md` - Build, deployment, and versioning procedures

### Key Functions to Understand
- `app_main()` - Entry point and main loop
- `parse_and_print_bms_data()` - BMS protocol parsing
- `publish_bms_data_mqtt()` - JSON structure generation
- `params_*_handler()` - Web interface endpoints
- `*_from_nvs()` - Configuration persistence

### Debug Control Points
- **Line ~71**: `static bool debug_logging = false;` (application debug output)
- **Line ~1583**: `esp_log_level_set("*", ESP_LOG_WARN);` (system log level)
- **Production**: Both set to minimal output for clean operation
- **Development**: Change to `true` and `ESP_LOG_INFO` for detailed debugging

### Hardware Connections
- GPIO16/17: RS485 UART (to MAX485 module)
- GPIO2: Heartbeat LED (flashes on MQTT success only)
- GPIO0: Boot button (10s window for captive portal)
