---
name: esp32-isolated-digital-input
description: Use when an ESP32 reads 24 V industrial signals - a PLC output, a proximity sensor, a dry contact - and the input must survive reverse polarity and ground differences. Covers opto input design, thresholds and debounce.
license: MIT
---

# 24 V digital inputs on ESP32

A 24 V signal cannot touch a GPIO. The interface is an optocoupler, a resistor
and a decision about polarity.

## The basic chain

```
24V field --[ R ]--+-- opto LED --> opto transistor -- pull-up --> GPIO
                   |
                 reverse diode
```

- **R** sets the LED current. A typical opto wants 5 to 10 mA; at 24 V that is
  2.2 to 4.7 kohm, and the resistor dissipates 0.1 to 0.25 W - use a 0.5 W part.
- **Reverse diode** across the LED protects against a miswired supply. Without
  it, reverse polarity destroys the opto instantly.
- **The transistor side** pulls the GPIO low when active; enable the internal
  pull-up, or fit an external 10 kohm.

## Thresholds that match real sensors

| Input | Typical on-state |
|---|---|
| PLC output (sourcing) | 24 V, 7 mA minimum per IEC 61131-2 type 1 |
| Proximity sensor PNP | 24 V, 10 to 200 mA |
| Dry contact | needs wetting current, 5 to 10 mA |

A dry contact with 1 mA of wetting current will eventually fail to make contact -
oxide builds up. If the input is a relay contact, keep at least 5 mA through it.

## Speed vs protection

An opto with a 4.7 kohm resistor and no speed-up capacitor is slow: 10 to 50 us.
That is fine for a pushbutton and wrong for an encoder. For fast inputs, use a
digital isolator (Si8610, ISO7721) instead of an opto.

## Debounce belongs in the firmware, not the hardware

20 ms of software debounce covers contact bounce and survives a firmware change.
A hardware RC that is too slow hides fast pulses and cannot be tuned later.

## Symptom table

| Symptom | Usually |
|---|---|
| input reads active with nothing connected | no pull-up, floating opto collector |
| reads inactive at 24 V | LED current too low, resistor too large |
| dies on reverse polarity | no reverse diode |
| counts on every motor start | no common-mode filtering, shared return |
| misses short pulses | opto too slow, or debounce too long |

## Agent rules

- State the resistor value, its power rating and the resulting LED current.
- Say whether the input is sinking or sourcing, and match the sensor type.
- Keep field ground and logic ground separate; the opto is the only bridge.
