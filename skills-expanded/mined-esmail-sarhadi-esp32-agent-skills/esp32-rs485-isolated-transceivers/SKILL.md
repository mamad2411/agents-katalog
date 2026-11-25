---
name: esp32-rs485-isolated-transceivers
description: Use when an RS485 port must survive a real installation - ground potential between buildings, a 24 V miswire, a drive that destroys transceivers, or a bus that works on the bench and fails on site. Covers ADM2587E, ISO3082, MAX3485 and protection.
license: MIT
---

# Isolated RS485 on ESP32

A non-isolated MAX3485 on a 3.3 V rail is fine on a bench with one power supply.
In a building, two nodes 50 m apart sit on grounds that differ by volts, and the
first surge finds the transceiver.

## The three parts of an RS485 port

1. **Transceiver** - converts logic to differential.
2. **Isolation** - breaks the ground loop between the ESP32 and the bus.
3. **Protection** - clamps what gets past the isolation.

Skipping any one of them is a decision, and it should be written down.

## Transceiver choices

| Part | Isolation | Speed | Notes |
|---|---|---|---|
| MAX3485 / SP3485 | none | 10 Mbit/s | 3.3 V, cheapest, dies first on a surge |
| MAX485 | none | 2.5 Mbit/s | 5 V part, needs level shifting on a 3.3 V MCU |
| ISO3082 | 2.5 kV, needs isolated power | 20 Mbit/s | fast, but you must supply VISO |
| ADM2587E | 2.5 kV, integrated DC-DC | 500 kbit/s | one part, no separate isolated supply, 5 V both sides |

For a 9600 or 19200 baud Modbus line, the ADM2587E is usually the right answer:
one chip, no isolated DC-DC to design, and 500 kbit/s is ten times the line rate.

## Termination and biasing

- 120 ohm at both physical ends, nowhere else.
- Fail-safe biasing (a pull-up on A and pull-down on B, typically 560 to 680 ohm)
  holds the idle state when no driver is active. Without it a floating bus reads
  as constant start bits and every slave sees a framing error.
- Bias resistors belong at **one** node only. Two sets in parallel load the bus.

## Protection that actually protects

- TVS on A/B to the local ground, chosen so the clamping voltage stays inside
  the transceiver's absolute maximum (usually -8 V to +13 V common mode).
- Series resistors (10 to 22 ohm) or a common-mode choke before the TVS.
- A GDT or MOV upstream if the cable leaves the building.
- The shield connects at one end only, or through a capacitor - both ends makes
  it an antenna and a ground-loop path.

## Symptom table

| Symptom | Usually |
|---|---|
| transceiver dies after a storm | no TVS, or TVS clamp above the part's limit |
| works on the bench, framing errors on site | ground potential, no isolation |
| bus idle reads as start bits | no fail-safe bias |
| one node loads the bus | two termination resistor sets |
| CRC errors only on long cable | no termination, or wrong baud tolerance |
| works until a VFD starts | no common-mode choke, cable routed with motor leads |

## Agent rules

- Ask for the distance between nodes and whether the grounds are bonded. That
  answer decides isolation, not preference.
- Never put a 5 V MAX485 on a 3.3 V ESP32 without checking the RO output level
  against the ESP32's input threshold on the actual part.
- State the termination count and where the bias lives in the wiring table.
