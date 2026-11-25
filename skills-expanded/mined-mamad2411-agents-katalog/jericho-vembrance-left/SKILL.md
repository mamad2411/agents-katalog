# Jericho Vembrance - Cursor AI Instructions

## Project Context

This is the **Jericho Vembrance Left Gauntlet** project - a tactical heads-up display (HUD) inspired by Rasputin AI from Destiny. The system uses an ESP32-S3 development board with a Waveshare 1.69" ST7789V2 TFT display and a BME680 environmental sensor.

## Hardware Platform

- **Board**: YD-ESP32-S3 (ESP32-S3-WROOM-1-N16R8)
- **MCU**: ESP32-S3 dual-core @ 240 MHz
- **Flash**: 16 MB
- **PSRAM**: 8 MB (Octal SPI)
- **Framework**: Arduino (PlatformIO)

## Display Hardware

- **Model**: Waveshare 1.69" LCD Module
- **Resolution**: 240×280 pixels
- **Driver**: ST7789V2 (Sitronix)
- **Interface**: 4-line SPI (HSPI/SPI3)
- **Color Order**: RGB (not BGR)
- **Pins**: GPIO11 (MOSI), GPIO12 (SCK), GPIO10 (CS), GPIO13 (DC), GPIO14 (RST), GPIO21 (BL)

### Critical Display Settings (DO NOT CHANGE)
- `USE_HSPI_PORT=1` - **MANDATORY** for ESP32-S3 SPI3 peripheral
- `TFT_RGB_ORDER=TFT_RGB` - Correct color order for ST7789V2
- `SPI_FREQUENCY=10000000` - 10MHz SPI clock (tested stable)
- `CGRAM_OFFSET=20` - Display row offset correction

## Environmental Sensor

- **Model**: Bosch BME680 (Adafruit breakout)
- **Interface**: I²C
- **Addresses**: 0x76 (default) or 0x77 (if SDO pulled high)
- **Pins**: GPIO41 (SDA), GPIO42 (SCL)
- **Measures**: Temperature, Humidity, Pressure, Gas Resistance (VOC)
- **Sampling Rate**: 0.1s (100ms) for high-frequency updates

## mmWave Sensor (Human Detection)

- **Model**: S3KM1110-based 24GHz mmWave Radar
- **Technology**: Frequency Modulated Continuous Wave (FMCW)
- **Interface**: UART (Hardware UART1)
- **Pins**: GPIO17 (TX), GPIO18 (RX)
- **Baud Rate**: 115200 (default, verify from sensor docs)
- **Range**: 7m detection radius
- **Features**: Human micro-motion detection, distance, angle, velocity, confidence
- **Status**: Shows "NO DATA" on minimap if sensor not connected

## Software Architecture

### Key Features
- **Differential Rendering**: Only redraws pixels that have changed (60-80% SPI traffic reduction)
- **150ms Update Cycle**: Base refresh rate with selective sub-updates
- **2-Column Layout**: 75% | 25% (Combined Left/Center | Right)
  - Left/Center: Status indicators, maximized minimap, risk rating
  - Right: 5 time-series graphs (Humidity, Temperature, VOC, Pressure, Heat Index)
- **Optimized UI/UX**: Green/yellow/orange/red color coding for intuitive status indication
- **High-Frequency Sensor Sampling**: 0.1s (100ms) sampling rate for responsive data
- **Multi-Factor Survival Risk Assessment**: Combines temperature, humidity, pressure, and VOC
- **Temporal Analysis**: Risk history tracking, rate of change detection, sustained exposure monitoring
- **Context Awareness**: Time-of-day adjustments for temperature/humidity sensitivity
- **Heat Index Calculation**: NOAA/NWS Rothfusz equation for feels-like temperature

### Color Palette (Optimized UI/UX)
```cpp
COLOR_BG = 0x0000        // Black background
COLOR_GREEN = 0x07E0     // Green (good/safe)
COLOR_YELLOW = 0xFFE0    // Yellow (caution)
COLOR_ORANGE = 0xFDA0    // Orange (warning)
COLOR_RED = 0xF800       // Red (critical/danger)
COLOR_WHITE = 0xFFFF     // White (high contrast text)
COLOR_DIM = 0x4208       // Dark gray (inactive/dim)
COLOR_ACCENT = 0x8410    // Medium gray (borders/accents)

// Legacy color aliases for compatibility
COLOR_PRIMARY = COLOR_RED
COLOR_WARNING = COLOR_ORANGE
COLOR_CRITICAL = COLOR_RED
COLOR_SUCCESS = COLOR_GREEN
COLOR_TEMP = COLOR_ORANGE
```

### Layout Constants
```cpp
SAFE_TOP = 8
SAFE_BOTTOM = 272
SAFE_LEFT = 10
SAFE_RIGHT = 230
CONTENT_TOP = 40
COL_LEFT_CENTER_WIDTH = 165  // 75% (combined left + center)
COL_RIGHT_WIDTH = 55         // 25%
COL_LEFT_CENTER_X = SAFE_LEFT
COL_RIGHT_X = COL_LEFT_CENTER_X + COL_LEFT_CENTER_WIDTH
```

### Data Structures
- `SystemStatus`: System indicators (name, active, warning)
- `StatusBar`: Power/thermal/signal bars (label, value, color, units)
- `WeatherData`: Weather condition and temperature
- `AirQuality`: VOC, pressure, grade, gradeColor
- `Blip`: Minimap entities (x, y, color, active)
- `TimeSeriesData`: Circular buffer for time-series graphs (values, index, filled, min/max)
- `MmWaveDetection`: mmWave sensor data (detected, distance, angle, velocity, confidence, valid)
- `RiskHistory`: Temporal risk analysis (values, average, rate of change, trend, high-risk duration)
- `WallSegment`: Minimap wall detection (angle, distance, active)

### Differential Update System
Previous values tracked for change detection:
- `prevHour, prevMinute, prevSecond` - Time components (updates every 1 second)
- `prevTemp` - Temperature
- `prevWeatherCondition` - Weather state
- `prevGraphStates[5]` - Previous states for all 5 time-series graphs (values, min/max, colors)
- `prevWallSegments[]` - Previous minimap wall states (active, distance, screen position)
- `minimapBackgroundDrawn` - Background dots drawn once
- `prevMinimapHeading` - Compass heading for ring rotation
- `prevCompassHeading` - Compass heading (±0.5° threshold)
- Risk rating position tracking (x, y, width, height) to prevent broken displays

**⚠️ DO NOT remove differential update logic** - this would severely degrade performance.

## Git Workflow Guidelines

1. **Authorized Git Operations**: You are authorized to use, analyze, and execute git commands
2. **No Pushes to Origin**: You are NOT authorized to push commits to origin
3. **Atomic Commits**: Write, commit, and itemize changes on an atomic level
   - Each commit should represent a single logical change
   - Use clear, descriptive commit messages
   - Group related changes together, but keep commits focused
   - Follow conventional commit format (feat:, fix:, refactor:, style:, docs:)
4. **Commit Organization**: 
   - Separate commits for different features or fixes
   - Document what changed and why in commit messages
   - Include relevant context in commit messages

## Code Style Guidelines

1. **Use constexpr** for compile-time constants
2. **Namespace anonymous** for internal functions
3. **Serial debugging** with `[TAG]` prefixes for easy filtering
4. **Error handling** - Always check sensor initialization before use
5. **Change detection** - Always check previous values before redrawing
6. **Memory efficiency** - Use appropriate data types (uint16_t for colors, etc.)

## Common Tasks

### Adding a New Display Element
1. Add data structure for element state
2. Add previous value tracking variable(s)
3. Create draw function with change detection
4. Add update logic to `loop()` with appropriate cycle timing

### Modifying Sensor Integration
1. Check I2C address (try both 0x76 and 0x77)
2. Verify wiring (SDA/SCL not swapped)
3. Check pull-up resistors (4.7kΩ recommended)
4. Add serial debugging for troubleshooting
5. Handle sensor initialization failures gracefully

### Display Troubleshooting
- **Blank display**: Check SPI connections, CS pin, DC pin
- **Wrong colors**: Verify `TFT_RGB_ORDER` build flag
- **Garbled display**: Lower SPI frequency, check wiring
- **No updates**: Check differential update logic, verify loop() is running

### Sensor Troubleshooting
- **Not detected**: Try both I2C addresses (0x76, 0x77)
- **Wrong readings**: Check wiring, verify power supply (3.3V)
- **Intermittent**: Check connections, add pull-up resistors
- **Gas readings unstable**: BME680 requires 24h burn-in period

## File Structure

```
src/
  main.cpp           # Main application (display + sensor logic)
docs/
  ST7789V2-SPECSHEET.md    # Display controller specs
  BME680-SPECSHEET.md       # Environmental sensor specs
  WIRING.md                 # Hardware connections (includes mmWave sensor)
  YD-ESP32-S3-SPECSHEET.md  # Board specifications
  RISK-CALCULATION.md        # Multi-factor risk assessment methodology
  TEMPORAL-ANALYSIS-PLAN.md # Temporal analysis implementation
  LIDAR-INTEGRATION.md      # mmWave sensor integration guide
platformio.ini              # Build configuration
README.md                   # Project overview
.cursorrules               # AI assistant context (this file)
```

## Library Dependencies

```ini
lib_deps =
    bodmer/TFT_eSPI @ ^2.5.43
    adafruit/Adafruit BME680 Library @ ^2.0.3
    adafruit/Adafruit Unified Sensor @ ^1.1.14
```

## Build Configuration

Critical build flags in `platformio.ini`:
- `USE_HSPI_PORT=1` - ESP32-S3 SPI3 peripheral
- `TFT_RGB_ORDER=TFT_RGB` - Color order
- `SPI_FREQUENCY=10000000` - 10MHz clock
- `CGRAM_OFFSET=20` - Row offset

## Debugging Tips

1. **Serial Monitor**: Use `[TAG]` prefixes to filter output
2. **I2C Scanner**: Built-in scanner at startup (check serial output)
3. **Display Skip**: Use `SKIP_DISPLAY_INIT` define to debug sensors without display
4. **Heartbeat**: System logs heartbeat every 5 seconds with status

## Important Notes

- **Never remove differential update system** - critical for performance
- **Never change critical build flags** without testing thoroughly
- **Always check sensor initialization** before using readings
- **Handle sensor failures gracefully** - show "NO DATA" instead of crashing
- **Use appropriate delays** for sensor readings (BME680 needs time between readings)

## Current Status

- ✅ Display working (ST7789V2)
- ✅ BME680 sensor integrated and working
- ✅ mmWave sensor integration (S3KM1110-based) - GPIO17/18
- ✅ Differential rendering system (clock, graphs, minimap)
- ✅ 2-column layout (75% | 25%)
- ✅ Optimized UI/UX color coding (green/yellow/orange/red)
- ✅ Minimap with real mmWave sensor data (shows "NO DATA" if not connected)
- ✅ 5 time-series graphs (Humidity, Temperature, VOC, Pressure, Heat Index)
- ✅ Multi-factor survival risk assessment
- ✅ Temporal analysis and context awareness
- ✅ Heat index calculation (NOAA/NWS Rothfusz equation)
- ✅ High-frequency sensor sampling (0.1s)
- ✅ Status indicators (3-letter labels with colored dots)
- ✅ Risk rating display (prominent bar below minimap)

## Key Features Implemented

1. **Real Sensor Integration**: BME680 for environmental data, mmWave for human detection
2. **Advanced Risk Assessment**: Multi-factor survival risk with temporal analysis
3. **Dynamic Color Coding**: All graphs and labels change color based on sensor values
4. **Differential Rendering**: Optimized for minimal screen updates
5. **High-Frequency Updates**: 0.1s sensor sampling for responsive data
6. **Context Awareness**: Time-of-day adjustments for risk sensitivity
7. **Heat Index**: Accurate feels-like temperature calculation

