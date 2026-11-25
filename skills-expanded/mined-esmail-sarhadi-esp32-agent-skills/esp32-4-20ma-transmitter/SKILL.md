---
name: esp32-4-20ma-transmitter
description: Use when an ESP32 must drive a 4-20 mA current loop - as a transmitter into a PLC, a valve command, or a two-wire loop. Covers XTR116-class parts, loop power, isolation and the live-zero rule.
license: MIT
---

# 4-20 mA output from ESP32

A current loop is a different discipline from a voltage output: the receiver
measures current, the loop supplies the power, and the wire resistance does not
change the reading.

## The live zero

4 mA means zero, 20 mA means full scale, and **0 mA means the loop is broken**.
That is the whole point of the standard. A transmitter that outputs 0 mA on a
fault is indistinguishable from a cut cable, and the PLC will treat it as one.

- Below-range fault: 3.6 mA or lower, but above 0.
- Above-range fault: 21 mA or higher, below the receiver's limit.
- Pick one convention and document it; NAMUR NE43 is the usual reference.

## Driving the loop

| Approach | Notes |
|---|---|
| XTR116 / XTR117 | 2-wire transmitter, loop-powered, needs a DAC and a resistor |
| Op-amp + transistor current sink | cheap, needs care with loop compliance |
| Dedicated driver with isolation | the right answer when the field wiring is long |

The loop supply must exceed the total voltage drop: receiver burden (often
250 ohm = 5 V at 20 mA) + cable resistance + the transmitter's minimum. A 24 V
supply with a 250 ohm burden leaves about 19 V for everything else, which is
usually enough - but do the arithmetic per installation.

## Accuracy

- The DAC's reference is the accuracy of the loop. 1 % reference is 1 % of the
  reading, forever.
- Calibrate at 4 and 20 mA, not at mid-scale: two points define the line, and the
  endpoints are what the receiver checks.
- Temperature drift in the sense resistor shows up as gain drift; use 25 ppm/degC
  or better.

## Isolation

If the loop ground and the ESP32 ground are the same node, a ground loop current
flows through the cable shield and the reading drifts. Use an isolated
transmitter (or an isolated DAC) whenever the receiver is powered from a
different distribution board.

## Symptom table

| Symptom | Usually |
|---|---|
| reading is 0 mA at the PLC | loop open, or the transmitter is unpowered |
| reading 4 mA regardless of setpoint | DAC not updating, or the resistor is open |
| reading scales but is offset | calibration at mid-scale only |
| drifts with temperature | sense resistor tempco, or reference drift |
| works on the bench, fails in the panel | loop compliance, cable drop |

## Agent rules

- State the loop supply, the receiver burden and the cable resistance, and show
  the compliance arithmetic.
- Never use 0 mA as a fault value.
- Say whether the output is isolated from the ESP32 ground, and why.
