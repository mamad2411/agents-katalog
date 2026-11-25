---
name: esp32-surge-and-tvs-protection
description: Use when field wiring can deliver a surge - long cables, outdoor sensors, inductive loads, 24 V miswired into a 3.3 V input. Covers TVS selection, clamping voltage, series impedance and what a TVS cannot do.
license: MIT
---

# Surge protection for ESP32 I/O

A TVS diode is not a lightning arrestor and not a fuse. It clamps a short
transient to a voltage, once, if the energy is small enough.

## The rule that decides the part

Pick the TVS by **standoff voltage and clamping voltage**, not by package:

- Standoff (`Vwm`) must be above the highest normal signal level, with margin.
- Clamping (`Vcl` at the surge current) must be below the absolute maximum of the
  protected pin - not the recommended operating voltage.

A 3.3 V GPIO with a 5.5 V absolute maximum needs a TVS that clamps under 5.5 V at
the expected surge current. Many "3.3 V" TVS parts clamp at 8 V at 1 A, which
protects nothing.

## Series impedance first

A TVS alone on a long cable sees the full surge current. A series resistor or a
common-mode choke ahead of it drops the current and gives the TVS time to clamp:

```
field ---[ 22R or choke ]---+--- to GPIO
                            |
                          TVS to GND
```

Without the series element, the TVS has to absorb everything the cable delivers.

## What each part does

| Part | Job |
|---|---|
| TVS (SMBJ, P6KE) | clamps fast transients, microseconds |
| MOV | higher energy, slower, degrades with each hit |
| GDT | very high energy, crowbars, used upstream |
| fuse / PTC | opens on sustained overcurrent, not on a surge |
| series resistor | limits current into the clamp |

A design that leaves the building needs all four in the right order, not one.

## Grounding

The TVS return path must be short and go to the same ground the transient
arrives on. A TVS on a long thin trace to a distant ground plane clamps at the
pin, then the trace inductance adds hundreds of volts.

## Symptom table

| Symptom | Usually |
|---|---|
| input dies in the field, fine on the bench | no TVS, or clamp above the pin limit |
| TVS itself shorted | surge energy above its rating, no series impedance |
| works until a contactor opens | no protection on the coil, coupled transient |
| ADC readings spike during switching | ground bounce, missing common-mode choke |

## Agent rules

- Give the TVS part number, standoff, and clamping voltage at the rated current.
- Show the series element and the return path in the wiring table.
- Never claim a design is "surge protected" without the energy path written down.
