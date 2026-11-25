---
name: esp32-thermocouple-max31855
description: Use when integrating K-type thermocouples with MAX31855 or diagnosing open sensor, cold-junction error and noisy temperature readings.
license: MIT
---

# Thermocouple Max31855

Thermocouple systems measure a small differential voltage and compensate using a cold-junction sensor. Connector metallurgy, extension wire and thermal gradients can dominate the error.

## Sensor and wiring

Use thermocouple-grade connectors and matching extension wire; ordinary copper transitions create unintended thermocouple junctions. Keep the cold-junction IC away from regulators, radios or heat sources. Route away from switching nodes and use appropriate shielding/grounding.

## MAX31855 interface

Read the full 32-bit result with correct SPI mode and timing from the datasheet. Decode thermocouple temperature, internal cold-junction temperature and fault bits separately. Check open-thermocouple, short-to-ground and short-to-supply indicators. Do not interpret faulted temperature bits as a valid measurement.

## Accuracy and response

Understand the device resolution and total error budget, including thermocouple class, cold-junction accuracy, connector gradients and installation. Probe response depends on construction and thermal contact, not just conversion interval. Avoid oversampling claims beyond converter update behavior.

## Fault handling

On a fault, mark the measurement invalid and expose the fault code. Do not substitute zero or the last value without a stale flag. Detect implausible rate-of-change and compare cold-junction readings with board temperature when useful.

## Verification

| Condition | Check |
|---|---|
| Open thermocouple | Fault bit and invalid quality |
| Reversed polarity | Sign/direction sanity |
| Connector heated | Cold-junction gradient effect |
| Known temperature point | Calibration error |
| SPI contention | Correct frame and CS timing |

## Agent rules

Preserve raw register words and fault bits. Never use copper wire as arbitrary thermocouple extension. State probe type, wire grade, connector and calibration method.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
