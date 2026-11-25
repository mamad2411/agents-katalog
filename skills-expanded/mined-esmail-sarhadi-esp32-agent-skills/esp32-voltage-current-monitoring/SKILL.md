---
name: esp32-voltage-current-monitoring
description: Use when measuring supply voltage, current or power with INA219, INA226 or similar monitor ICs.
license: MIT
---

# Voltage Current Monitoring

Digital current monitors depend on shunt value, common-mode range, calibration register, bus voltage and layout. A plausible display value can still be off by a large scale factor.

## Shunt and layout

Choose shunt resistance from maximum current, voltage burden and power dissipation. Check pulse/continuous power and tolerance. Use Kelvin connections to the shunt sense pins and keep high-current copper away from sensitive analog paths. Confirm the monitor's common-mode range includes startup and fault transients.

## Calibration math

Derive current LSB and calibration register from the exact device datasheet equations. Verify shunt value in ohms, not milliohms, and use signed arithmetic where bidirectional current is possible. Validate bus-voltage LSB, power register scaling and overflow behavior with known loads and a calibrated reference meter.

## Sampling and dynamics

Understand conversion time, averaging and update rate. Short inrush events may be missed by slow conversion settings. Use hardware protection for fast overcurrent; a telemetry monitor is not automatically a safety trip circuit. Avoid I2C reads from ISR context and bound bus timeouts.

## Fault interpretation

Distinguish bus voltage, shunt voltage, calculated current and calculated power. Detect open shunt, reversed orientation, saturation and I2C communication failure. Mark stale samples explicitly and avoid reporting a disconnected monitor as zero load.

## Verification

| Reference test | Acceptance evidence |
|---|---|
| Zero current | Offset and noise recorded |
| Known resistive load | Current/power error |
| Maximum expected current | Shunt temperature and linearity |
| Reverse current if supported | Correct sign |
| Fast load step | Response time and missed peak bound |

## Agent rules

Document exact IC, shunt value/tolerance, calibration equation and conversion configuration. Do not use software telemetry as a substitute for independent overcurrent protection.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
