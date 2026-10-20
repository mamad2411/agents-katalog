# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Code for workshop machine utilities — currently an Arduino sketch for a Bridgeport mill.

## Projects

### Bridgeport Control Panel (`Bridgeport_control_panel/Bridgeport_control_panel.ino`)

Arduino Nano sketch that reads the VFD's 0–10 V analog output, converts it to spindle speed (RPM), and displays it on a TM1637 4-digit 7-segment LED display.

**Hardware signal chain:**
- VFD outputs 0–10 V proportional to frequency, with a −5% bias
- A voltage divider + MCP6002 differential op-amp converts this to 0–5 V for the Arduino's analog input (A0)
- A 1 µF capacitor provides a low-pass filter (cutoff ~1.59 Hz)
- Speed is averaged over 1-second windows before updating the display

**Calibration constants** (in the sketch):
- `calibration`: converts raw ADC reading to RPM (currently `4025.0 / 1023.0`)
- `bias`: corrects for the VFD's −5% bias (currently `195.0`)
- To recalibrate: set `calibration = 1.0` and `bias = 0.0`, read raw values, then compute new constants from `calibration_measurements.csv`

**Speed ranges:** A button on pin 5 toggles between high and low spindle range. Low range divides by `BACKGEAR_RATIO` (8.3). The display shows "HI" or "LO" for 1 second after switching.

**Debug mode:** Set `#define DEBUG 1` (or `2` for verbose) to enable serial output at 9600 baud.

**To upload:** Use the Arduino IDE or `arduino-cli`. Requires the `TM1637Display` library.

```bash
# With arduino-cli (adjust port as needed):
arduino-cli compile --fqbn arduino:avr:nano Bridgeport_control_panel/
arduino-cli upload -p /dev/cu.usbserial-* --fqbn arduino:avr:nano Bridgeport_control_panel/
```
