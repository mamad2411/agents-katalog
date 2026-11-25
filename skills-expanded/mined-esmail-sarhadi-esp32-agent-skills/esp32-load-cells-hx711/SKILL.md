---
name: esp32-load-cells-hx711
description: Use when reading load cells with HX711, diagnosing unstable weight, drift, saturation or calibration errors.
license: MIT
---

# Load Cells Hx711

A load-cell reading is a mechanical and analog measurement. Firmware averaging cannot correct bad mounting, excitation, wiring, overload, creep or temperature drift.

## Wiring and mechanics

Identify bridge wiring and excitation/sense arrangement from the load-cell datasheet; wire colors are not universal. Keep signal wiring twisted and shielded as appropriate, away from motors and relay conductors. Mount the load cell within its specified load direction and avoid side loading or mechanical binding.

## HX711 operation

Confirm RATE pin/sample rate and gain/channel configuration. Read data-ready timing correctly and avoid blocking a real-time control task while waiting for conversion. Treat missing-ready and timeout as sensor faults. Verify supply and reference arrangement and ensure ADC input common-mode constraints are met.

## Calibration

Tare with a stable unloaded platform and calibrate using traceable known masses spanning the intended range. Use multiple points to check linearity; do not assume one-point calibration is adequate. Store calibration with units, date, sensor identity and schema version. Recheck zero and span after mechanical changes.

## Filtering and faults

Use median/outlier rejection or low-pass filtering only after preserving raw samples. Define settling time and filter latency. Detect open circuit, short circuit, overload, implausible slew and persistent saturation. Report measurement quality separately from numeric value.

## Verification

| Test | Expected result |
|---|---|
| Known masses across range | Error within declared tolerance |
| Eccentric loading | Characterized corner error |
| Empty platform over time | Drift bounded and recorded |
| Motor/relay switching | Noise immunity measured |
| Sensor disconnect | Explicit invalid status |

## Agent rules

Do not equate HX711 counts with grams without calibration. Keep raw counts available. Record load-cell capacity, excitation, mechanical mounting and calibration uncertainty.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
