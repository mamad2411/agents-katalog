---
name: esp32-power-and-boot
description: Use when an ESP32 board resets randomly, browns out, fails to boot, or drains a battery in days. Covers the power budget, the boot strap states and deep-sleep leakage, and says what to measure before changing code.
license: MIT
---

# ESP32 power and boot

"Random resets" is the most misdiagnosed symptom on this platform. It is almost
never the code. Work through the three layers below in order, and measure before
changing anything.

## Layer 1: is the supply actually able to deliver?

The radio is the load. An ESP32 transmitting draws peaks in the region of 240 mA
(the datasheet figure for 802.11b at 17 dBm), while the average is far lower.
A USB port or a small LDO that is fine on average can still dip below the
brownout threshold on every packet.

- The brownout detector trips at roughly 2.4 V by default. A reset whose cause
  reads `RTCWDT_BROWN_OUT_RESET` in the boot log is a supply problem, not a
  firmware problem.
- Put a bulk capacitor (100 µF and up) close to the module's 3V3 pin, plus the
  usual 100 nF. Distance matters more than the printed value.
- Never power a module from the 3.3 V pin of a USB-serial adapter that is rated
  for a few tens of milliamps.
- If the board also drives WS2812 LEDs, the LED current is the load: budget up to
  about 60 mA per LED at full white (vendor figure) and add that to the radio
  peaks before choosing the supply.

## Layer 2: did it even get to `setup()`?

- `GPIO12` HIGH at reset selects 1.8 V flash on a 3.3 V module. The board draws
  current and prints nothing. This is a pin-map bug that looks like dead hardware.
- `GPIO15` LOW at reset silences the boot log, which makes a working board look
  bricked.
- `GPIO0` LOW at reset enters the serial bootloader instead of running the sketch.
- Anything on those pins at power-up — a relay module, a pull-up, a level shifter
  that floats — can hold them at the wrong level.

## Layer 3: deep sleep

- Only RTC GPIOs (`GPIO0`-`GPIO15` on the classic ESP32) can wake the chip.
- A pin that is driven by a peripheral keeps leaking while the chip sleeps unless
  you isolate it: call `rtc_gpio_isolate()` or `gpio_hold_en()` before sleeping
  and `gpio_hold_dis()` after waking.
- A regulator with a quiescent current in the milliamps, or an always-powered
  sensor on the same rail, will dominate the sleep budget. The chip's own sleep
  current is tens of microamps; if you measure milliamps, look at the board, not
  at the firmware.
- Measure with a meter in series, not with a USB power monitor: the meter's own
  burden and the USB bridge both distort the reading.

## What to ask the user before proposing a fix

1. What is the exact board and module variant?
2. How is it powered, and what else is on that rail?
3. What does the boot log say on the first line after reset?
4. Does it reset only when the radio is active, or also when idle?

A fix proposed without those four answers is a guess. Say so instead of guessing.
