---
name: esp32-industrial-analog-io
description: Use when connecting 4–20 mA loops, 0–10 V transmitters, industrial analog inputs, analog outputs or protected field wiring to ESP32.
license: MIT
---

# ESP32 Industrial Analog Io

Industrial analog signals cannot be connected directly to ESP32 GPIO. The design must translate field voltage/current into the ADC input range while controlling fault energy, common-mode voltage, noise and calibration error.

## 4–20 mA input

- Choose a precision shunt resistor from the required voltage span and ADC range. For example, 150 Ω produces 0.6–3.0 V across 4–20 mA; verify power, tolerance and fault current before using it.
- Add input protection and filtering based on the loop supply and fault model. A field wire may be miswired to a higher voltage.
- Decide whether the loop is passive or active and whether the ESP32 node supplies loop power.
- For long cable runs or ground potential differences, consider an isolated loop receiver.

## 0–10 V input

- Use a resistor divider plus buffer/protection designed for the maximum credible fault voltage, not just 10 V nominal.
- Include resistor tolerance, temperature coefficient, ADC input impedance, sampling capacitor and source impedance in the error budget.
- Clamp/protect without allowing clamp current to exceed component or GPIO ratings.
- Verify negative transients and common-mode conditions; a divider alone is not isolation.

## ADC and calibration

- Select the ADC unit and pins for the exact SoC. ADC behavior, attenuation and usable range differ across ESP32 families.
- Use calibration APIs or an external precision ADC when accuracy matters; raw counts are not engineering units.
- Store per-channel offset/gain with calibration version and CRC.
- Apply filtering only after defining sample rate, response time and rejection requirements.

## Fault handling

- Detect open loop, short circuit, overrange and under-range separately where hardware permits.
- Define a safe output state for sensor failure and stale data.
- Record raw ADC, calibrated value, quality flag and timestamp for diagnostics.
- Never report MQ sensor raw ADC as ppm without a validated sensor model and calibration.

## Verification matrix

| Condition | Verify |
|---|---|
| 4, 12, 20 mA | Accuracy and monotonicity |
| Open loop / short | Fault detection and safe state |
| Maximum input / miswire | No GPIO damage; protection survives |
| Temperature corners | Drift within budget |
| Wi-Fi transmit burst | No unacceptable ADC disturbance |

## Agent rules

- Draw the analog front end and calculate every node voltage before writing firmware.
- State accuracy, range, protection and isolation assumptions.
- Keep calibration separate from display scaling.
- Require bench measurements before claiming industrial suitability.
