---
name: esp32-din-rail-power
description: Use when an ESP32 board lives in a control cabinet - 24 V DC rail, wide input, isolated output, hold-up through a contactor drop. Covers buck selection, inrush, reverse protection and the 24 V to 3.3 V budget.
license: MIT
---

# 24 V cabinet power for ESP32

In a cabinet the rail is 24 V nominal, 18 to 30 V in practice, and it is shared
with contactors, relays and drives. The ESP32 supply has to survive all of that.

## Topology

| Stage | Part type | Why |
|---|---|---|
| reverse polarity | P-FET or ideal diode | a series Schottky wastes 0.4 V at 1 A |
| transient clamp | TVS 33 to 36 V standoff | the rail sees inductive kickback |
| step down | buck, 36 V rated input | an LDO from 24 V burns 2 W at 100 mA |
| isolation (if needed) | isolated DC-DC module | when the field side must float |

A linear regulator from 24 V to 3.3 V at 200 mA dissipates 4 W. In a sealed box
that is a design fault, not a choice.

## The input range is wider than the label

- Nominal 24 V, but a 26 V transformer with a light load can sit at 30 V, and a
  contactor opening can add a transient well above that.
- Choose the buck for 36 V continuous input and the TVS for 33 V standoff so the
  clamp acts before the buck's limit.
- Reverse polarity protection at the input, before everything else.

## Hold-up

If the 24 V rail drops for 20 ms during a contactor transition, the ESP32 resets
unless there is capacitance to ride through. `C = I * t / dV`: at 200 mA for
20 ms with 2 V of allowed sag, that is 2 mF. Two 1000 uF electrolytics are
usually the practical answer, plus a ceramic for the high frequency.

## Inrush

A 2 mF capacitor bank on a 24 V rail is a short circuit at power-up. An NTC or an
active inrush limiter keeps the upstream breaker from tripping.

## Symptom table

| Symptom | Usually |
|---|---|
| resets when a contactor closes | no hold-up, or the TVS is clamping late |
| supply hot in the box | linear regulator from 24 V |
| dead after a wiring mistake | no reverse polarity protection |
| breaker trips at power-up | inrush current from bulk capacitance |
| works on the bench supply, not in the panel | 24 V rail sagging below the buck's dropout |

## Agent rules

- Show the dissipation arithmetic for the chosen regulator at the real load.
- State the hold-up time required and the capacitance that provides it.
- Include reverse polarity and inrush in the schematic, not in a recommendation.
