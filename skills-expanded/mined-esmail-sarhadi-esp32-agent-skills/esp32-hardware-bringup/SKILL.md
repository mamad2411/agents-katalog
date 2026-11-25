---
name: esp32-hardware-bringup
description: Use when powering a new ESP32 board for the first time, or when a board that used to work stops booting - before changing any firmware. Covers current draw, rails, strapping levels and the order that separates a hardware fault from a software one.
license: MIT
---

# Hardware bring-up

Half of the "firmware problems" on a new board are hardware problems that firmware
cannot fix. This is the order that tells them apart in ten minutes instead of a
day.

## Before the first flash

1. **Measure the current with nothing running.** A board that draws hundreds of
   milliamps before any code is a short. Stop.
2. **Check the 3V3 rail with a scope, not a multimeter.** A multimeter averages
   away the dip that matters. The rail must stay inside spec during a Wi-Fi
   transmit burst; that is when it fails, not at idle.
3. **Confirm the strapping levels at reset.** `GPIO0`, `GPIO2`, `GPIO5`,
   `GPIO12`, `GPIO15` are sampled before your code runs. A pull-up you added for
   a button can hold `GPIO12` high and select 1.8 V flash, and the board stays
   dark with no error.
4. **Look at the serial console at 115200 on `GPIO1`/`GPIO3`.** The ROM prints
   something on every boot. Silence there means the chip is not starting, not that
   your sketch is wrong.

## Then, in this order

5. Flash a minimal blink. It proves the toolchain, the USB path and the flash.
6. Flash a sketch that only starts Wi-Fi and prints the IP. It proves the supply
   under load.
7. Only then flash the real firmware.

Doing 7 first means every later symptom has three possible causes instead of one.

## Reading a boot loop

| Message | Meaning |
|---|---|
| `flash read err, 1000` | flash contents and bootloader disagree - erase and reflash |
| `Brownout detector was triggered` | the rail collapsed under load |
| `invalid header` | wrong flash offset or a corrupted image |
| nothing at all | no power, wrong baud, or the chip is held in reset |

## Ground and decoupling

A board that works on the bench and fails in the enclosure has a ground or
decoupling problem far more often than a code problem. One ground return per
peripheral, a capacitor at each supply pin, and an antenna keep-out that the
enclosure respects.

## Rules for the agent

- When a user reports "it does not boot", ask for the serial output before
  suggesting a code change. Silence and a boot loop are different faults.
- Never propose a firmware fix for a symptom that a scope would explain.
- If a pin was added for a button or an LED, check it against the strapping list
  before assuming it is harmless.
