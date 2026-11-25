---
name: esp32-factory-test-and-calibration
description: Use when units are built in more than one - the test rig has to pass or fail a board in seconds, calibration values must survive flashing, or a returned unit cannot be identified. Covers the test firmware, the jig and per-unit data.
license: MIT
---

# Factory test and calibration

A board that works on your desk is one data point. A production run needs a
decision per unit, in seconds, with a record.

## Separate the test firmware

Do not bolt a test mode onto the product firmware with a magic GPIO. Build a
second environment that links the same drivers and runs the checks:

- Radio: scan and report RSSI of a known AP.
- Flash: write and verify a pattern in the unused tail of the partition.
- Every sensor: read once, compare to a plausible range, report the raw value.
- Every output: toggle, and let the operator confirm visually (a prompt, not a
  guess).
- Current draw at idle, measured by the jig, compared to a limit.

The test firmware is flashed first, run, and then the product image replaces it.
That also proves the flashing path works on that unit.

## The jig defines the interface

Pogo pins on test pads, not on connectors that wear out. Power the unit from the
jig, not from USB, so the current measurement means something. Two things worth
adding to the PCB for this: a test pad on every rail, and a pad on the boot
button line so the jig can force download mode without a human.

## Identity

Every unit needs a serial that is not the MAC address (MACs get reused on
replacement boards). Write it once, into NVS in a namespace the product firmware
never writes:

- Serial number, hardware revision, build date.
- Test results: pass/fail per check, measured values.
- Calibration coefficients.

A returned unit that reports its own test history saves an hour of guessing.

## Calibration that is worth doing

| What | How |
|---|---|
| ADC offset and gain | two known voltages, store slope and intercept |
| Battery voltage divider | measure the real rail, compare to the ADC reading |
| Current sensor zero | measure with the load off, store the offset |
| Temperature offset | one reference point is enough for a few degrees |
| RTC drift | optional: compare against GPS or SNTP, store ppm |

Store coefficients in NVS, apply them in one place in the code, and version the
calibration format - a unit calibrated with v1 coefficients must not be read by
v2 firmware as if nothing changed.

## What makes a rig pay for itself

| Symptom | Usually |
|---|---|
| a unit passes the rig and fails in the field | the rig never tested the radio, or only at 20 cm |
| different results from two rigs | no calibration of the rig itself; measure a golden unit daily |
| calibration lost after a service reflash | `erase_flash` wiped NVS - use `--erase-all` deliberately, and re-run calibration |
| test takes 90 seconds | waiting for a GNSS fix or a full charge; test what matters, not everything |
| operator error | the rig should refuse to continue, not warn |
