---
name: esp32-max31865-rtd
description: Use when integrating PT100/PT1000 RTDs with MAX31865 or diagnosing RTD wiring, lead compensation and temperature errors.
license: MIT
---

# MAX31865 RTD Interface

RTD measurement accuracy depends on excitation, reference resistor, lead resistance, wiring topology, self-heating and calibration. The MAX31865 is an RTD-to-digital converter, not a drop-in thermocouple interface.

## Topology and reference

Select 2-, 3- or 4-wire configuration based on required accuracy and cable length. Use a precision low-tempco reference resistor matched to the selected RTD nominal resistance. Verify PT100 vs PT1000 configuration, bias current and fault thresholds against the datasheet.

## Wiring and excitation

Follow the converter's exact FORCE, RTDIN and reference wiring diagram for the chosen topology. Avoid long unshielded runs near contactors or VFD wiring. Use twisted pairs and appropriate shield termination. Balance excitation current, conversion time and self-heating; do not leave bias enabled continuously without considering sensor dissipation.

## Conversion and linearization

Read RTD resistance ratio correctly and apply the appropriate Callendar–Van Dusen coefficients or a validated library implementation. Validate temperature range and coefficient set for the sensor standard. Do not use a PT100 coefficient for PT1000 without checking the implementation's normalization.

## Fault handling and calibration

Decode open/short and over/under-voltage fault bits. Mark faulted samples invalid. Calibrate the complete installed chain, not just the IC, using traceable temperature points and documented uncertainty. Store sensor type, wiring topology, reference resistor value and calibration date.

## Verification

| Test | Evidence |
|---|---|
| Precision resistor substitution | Resistance conversion error |
| 2/3/4-wire comparison | Lead compensation behavior |
| Open/short sensor | Fault detection |
| Thermal reference points | Temperature error and uncertainty |
| Long cable near switching load | Noise and stability |

## Agent rules

Keep RTD and thermocouple interfaces distinct. State wiring topology and reference resistor. Preserve raw ratio and fault status for service diagnostics.

## Field evidence to capture

- Record exact ESP32 SoC, board revision, MAX31865 breakout schematic and RTD part.
- Record reference resistor measured value, tolerance and temperature coefficient.
- Preserve raw RTD ratio, fault register and cold/ambient reference readings.
- Record cable length, wiring topology and shield/ground termination.
- Distinguish measured accuracy from a single successful temperature reading.

## Version and safety boundary

Check the target-specific SPI driver and board pin constraints before selecting GPIOs. RTD excitation, input protection and insulation are hardware design decisions. A software calibration cannot correct an incorrectly wired or thermally compromised probe.
