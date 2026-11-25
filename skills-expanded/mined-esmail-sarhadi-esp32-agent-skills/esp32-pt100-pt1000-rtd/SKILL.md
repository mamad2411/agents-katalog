---
name: esp32-pt100-pt1000-rtd
description: Use when measuring PT100/PT1000 RTDs with ESP32, MAX31865 or another RTD front end, including lead compensation and calibration.
license: MIT
---

# ESP32 Pt100 Pt1000 Rtd

An RTD is a precision resistance measurement, not a generic analog sensor. Excitation current, lead resistance, reference resistor accuracy, wiring mode and self-heating determine the result.

## Front-end selection

- Prefer a dedicated RTD converter such as MAX31865 when its supported wiring and accuracy meet the design requirements.
- Match PT100 or PT1000 configuration and reference resistor to the selected sensor.
- Use 2-wire only when lead resistance is acceptable; 3-wire compensates lead resistance under matched-lead assumptions; 4-wire provides the best lead cancellation.
- Confirm the module's reference resistor value and tolerance rather than assuming breakout-board markings.

## Wiring and installation

- Keep RTD leads paired and route away from PWM, relay and radio power wiring.
- Use shielded cable and grounding per the instrumentation design; avoid creating ground loops.
- Use terminal blocks rated for the environment and strain-relieve field wiring.
- Check sensor class, temperature range, probe construction and immersion/thermal contact.

## Conversion and diagnostics

- Use the converter's fault/status registers and distinguish open, short and over/undervoltage conditions.
- Convert resistance using the correct Callendar–Van Dusen coefficients for the sensor standard and temperature range.
- Average only after considering thermal response; filtering cannot fix a wiring fault.
- Track raw resistance, calculated temperature, fault flags and calibration identity.

## Verification

| Test | Expected result |
|---|---|
| Precision resistor at reference points | Within stated system error |
| Open sensor | Explicit open-circuit fault |
| Shorted leads | Explicit short/fault, not plausible temperature |
| 2/3/4-wire comparison | Lead error matches design assumptions |
| Thermal soak | Stable reading and bounded drift |

## Agent rules

- Never assume a PT100 and PT1000 share the same configuration.
- Include lead mode, reference resistor and sensor standard in code comments.
- State total system accuracy as a budget, not converter resolution alone.
- Do not use a bare ESP32 ADC as a precision RTD front end without a justified analog design.
