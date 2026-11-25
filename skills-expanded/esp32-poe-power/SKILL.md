---
name: esp32-poe-power
description: Use when an ESP32 board is powered over Ethernet - no power at all, a PD that never negotiates, resets under load, or a design that must survive a PoE switch. Covers 802.3af/at classes, PD controllers and the isolation barrier.
license: MIT
---

# Power over Ethernet for ESP32 boards

PoE puts 44 to 57 V on the same cable as the data. The board needs a PD
controller to ask for power, an isolated DC-DC to step it down, and a magjack
with the centre taps brought out.

## Classes and budgets

| Standard | PSE output | PD available | Typical use |
|---|---|---|---|
| 802.3af (type 1) | 15.4 W | 12.95 W | ESP32 + sensors |
| 802.3at (type 2) | 30 W | 25.5 W | ESP32 + display + heater |

A type-1 PSE will not power a type-2 PD at full class. If the board draws more
than 12.95 W it will be classified and then cut off under load, which looks like
a random reboot.

## The PD controller is not optional

The PSE detects a 25 kohm signature resistor before applying power, then reads a
classification pulse. A board that just connects a DC-DC to the spare pairs gets
nothing - the port stays off, and it looks like a dead switch port.

Parts that do this properly: TPS23753A (integrated), LTC4267, or a module with
the controller and the transformer already on it.

## Isolation is the point

PoE is isolated at the PD: the DC-DC transformer separates the cable side from
the board side. Skipping it (a non-isolated buck from 48 V) works on the bench
and creates a ground path between every device on the switch.

- Keep the isolation barrier intact: no shared ground, no scope probe across it.
- The magjack's centre taps go to the bridge rectifier, not to the PHY pins.

## Thermal

A 12 W PD in a sealed box dissipates several watts in the DC-DC. At 85 %
efficiency, 12 W out is 2 W of heat - inside a DIN-rail enclosure that is a
30 degC rise before the ESP32 adds anything.

## Symptom table

| Symptom | Usually |
|---|---|
| no power from a PoE switch | no signature resistor, or wrong classification |
| powers up, drops under load | class mismatch, PSE current limit |
| works on a PoE injector, not on the switch | non-standard passive injector vs 802.3af |
| reboots when the link renegotiates | hold-up capacitance too small |
| hot, then shuts down | DC-DC efficiency and no airflow |

## Agent rules

- State the class, the PD controller part and the DC-DC topology.
- Keep the isolation barrier in the wiring table; never bond the two grounds.
- Compute the thermal budget for the enclosure, not for the bench.
