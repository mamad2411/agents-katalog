---
name: esp32-energy-meter-modbus
description: Use when an ESP32 reads a Modbus energy meter - SDM120, SDM630, Eastron or similar - and the values are nonsense, swapped, or scaled by 1000. Covers float word order, register tables and polling rates.
license: MIT
---

# Reading an energy meter over Modbus

Energy meters are the most common Modbus device in the field and the most common
source of "the voltage reads 230000". The protocol works; the interpretation does
not.

## The float word order trap

Most meters return 32-bit IEEE-754 floats across two holding registers. Vendors
disagree on order:

- **Big-endian (ABCD)**: register N is the high word.
- **Little-endian word-swapped (CDAB)**: register N is the low word.

Reading 230.0 V as 230000 means the words are swapped. Reading it as
3.2e-41 means the byte order inside the word is wrong too. There are four
combinations and only one is right; check against a known value (mains voltage,
or a load you can measure).

## Register tables are per model

| Meter | Voltage | Current | Power | Energy |
|---|---|---|---|---|
| SDM120 | 0x0000 | 0x0006 | 0x000C | 0x0156 |
| SDM630 | 0x0000 | 0x0006 | 0x000C | 0x0156 |

Those are close but not universal. Take the table from the manual of the exact
model and revision, and record it in the reference file with the page number.

## Polling and scaling

- Default serial settings are usually 2400 8N1 with slave address 1. Change them
  deliberately and record it, or the next technician cannot talk to the meter.
- Energy registers are often 0.001 kWh units. A 32-bit float cannot hold a large
  lifetime total precisely; some meters use two registers or a 64-bit integer.
- Poll no faster than the meter updates. 1 Hz is plenty; 10 Hz on a 2400 baud
  line cannot fit the frames anyway.

## Sanity checks in firmware

Reject a reading when voltage is outside 90 to 300 V, current is negative, or the
power factor is outside -1 to 1. A meter that returns 0x7FC00000 is sending NaN,
and printing it as a float gives "nan" in the dashboard for the rest of time.

## Symptom table

| Symptom | Usually |
|---|---|
| voltage reads 230000 | word order |
| all registers read 0 | wrong slave address, or the meter is in a different mode |
| values update every 10 s only | polling faster than the meter's update rate |
| NaN in the dashboard | uninitialised float registers, or a read that timed out |
| CRC errors | 2400 baud with a long cable, no termination |

## Agent rules

- Record the exact model, the register table source page and the word order.
- Add range validation to the parser, not to the dashboard.
- State the polling interval and show that it fits the line rate.
