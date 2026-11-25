---
name: esp32-mcpwm-power-stage
description: Use when driving a motor, inverter, half bridge, complementary PWM output or other power stage with ESP32 MCPWM; especially when dead time, synchronization, fault braking or safe startup matters.
license: MIT
---

# MCPWM power-stage control

MCPWM generates coordinated motor-control waveforms. It does not make a power stage safe by itself.
The external gate driver, current sensing, protection and hardware shutdown path remain part of the design.

## Establish hardware capability

- Identify exact SoC and ESP-IDF version; MCPWM features and operator/timer counts vary by target.
- Read the SoC technical reference manual and the selected gate-driver datasheet before assigning pins.
- Confirm GPIO matrix routing, output polarity, complementary-output support and fault input availability.
- Keep the build example pinned to one driver API generation; legacy MCPWM and the newer handle-based driver are not source-compatible.
- Do not infer that a peripheral exists because another ESP32 family exposes it.

## Define the safe electrical state first

- Draw the power-stage truth table for reset, bootloader, firmware startup, normal run, fault and brownout.
- Use external pull resistors so gate-driver inputs remain OFF while ESP32 pins are high impedance.
- Prefer a hardware enable/fault path that disables switching independently of the application task.
- Configure fault actions to force the documented safe output state; verify active-high/active-low polarity.
- Never rely on a software task watchdog as the only overcurrent or shoot-through protection.

## PWM timing

- Derive timer period from the selected clock source and prescaler; document resolution and frequency error.
- Set compare values with explicit bounds and define what 0% and 100% mean electrically.
- Use complementary outputs and dead-time insertion only after validating gate-driver requirements and propagation delays.
- Check that dead time is represented in timer ticks and remains valid across clock changes.
- Use synchronization for multi-phase outputs; do not start independent timers and assume phase alignment.
- Keep updates at a defined boundary (for example, timer-zero event) to avoid mid-cycle glitches.

## Fault handling

- Wire overcurrent, gate-driver fault and emergency-stop signals to hardware-capable fault inputs where supported.
- Define one-shot versus cycle-by-cycle behavior from the power-stage protection requirements.
- Latch faults in firmware for diagnosis, but do not let firmware clear a fault while the physical cause remains.
- Require an explicit re-arm sequence after fault removal; default to outputs disabled after reset.
- Record fault source, timestamp, operating point and recovery action without blocking the ISR.

## Current and speed feedback

- Sample current with a documented trigger point relative to PWM switching edges.
- Account for amplifier settling, ADC acquisition time, offset and gain calibration.
- Use hardware comparators or external protection when software ADC latency cannot meet the shutdown requirement.
- Filter encoder/speed feedback without hiding a real stall or overspeed condition.
- Separate control-loop execution time from telemetry and logging.

## Verification

- Unit-test duty conversion, saturation, phase calculations and fault-state transitions on the host.
- On hardware, first test with the gate driver disabled or a current-limited low-voltage supply.
- Observe all complementary outputs with a scope and verify dead time at voltage and temperature corners.
- Inject each fault input and prove the gate-driver enable drops without waiting for a task.
- Test reset, brownout and firmware crash while outputs are active.
- Do not connect a motor or mains-powered stage until the independent protection path has been reviewed.

## Acceptance criteria

- The build targets a named SoC and pinned driver API.
- A state-machine test proves every fault transitions to outputs-disabled.
- Scope captures show polarity, frequency, duty limits and dead time.
- The document states that software validation is not a substitute for power-electronics safety review.

## References

- ESP-IDF MCPWM: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/mcpwm.html
- ESP-IDF GPIO: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html
- Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents
