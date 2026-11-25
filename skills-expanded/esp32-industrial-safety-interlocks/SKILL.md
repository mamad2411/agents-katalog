---
name: esp32-industrial-safety-interlocks
description: Use when ESP32 firmware controls relays, contactors, pumps, heaters, valves or machinery where an unsafe output state could damage equipment or injure people; especially when designing interlocks, E-stop behavior or restart policy.
license: MIT
---

# Industrial output interlocks and safe states

An ESP32 is a general-purpose controller, not a certified safety controller.
Firmware interlocks can reduce operational risk but must not replace required safety-rated relays, guards, contactors or independent protection.

## Define hazards before writing logic

- List hazards for each actuator: unexpected energization, failure to stop, restart after power return, overtemperature, dry run and stuck contact.
- Define a safe state for loss of power, MCU reset, brownout, watchdog, sensor fault and communication loss.
- Identify which safety functions require a certified safety relay or hardwired circuit independent of the ESP32.
- Use a risk assessment and applicable machinery/electrical standards with qualified engineering review.
- Do not market an ordinary ESP32 design as SIL/PL compliant based on software tests.

## Electrical output design

- Select relay/contactor drivers for coil voltage, inrush, inductive suppression and isolation requirements.
- Use external pull resistors and driver topology that keep outputs de-energized during reset and boot.
- Add feedback contacts where failure to release or weld is a credible hazard.
- Separate logic supply and actuator supply where appropriate; measure transients during switching.
- Verify output polarity at the actual driver and load, not only at the GPIO.
- Include fusing, surge suppression, creepage/clearance and enclosure requirements in the hardware review.

## Interlock state machine

- Represent each actuator with explicit states: disabled, ready, running, stopping, fault-latched and service.
- Define permissive conditions as a conjunction of validated sensor and operator inputs.
- Make emergency stop and hardwired safety-chain feedback dominate all normal commands.
- Reject commands that arrive before startup checks or while a fault is latched.
- Require deliberate reset/re-arm after a fault; never auto-restart a hazardous load merely because a sensor recovers.
- Define a timeout for actuator feedback and report commanded-versus-observed mismatch.

## Sensor and communication faults

- Treat open circuit, short circuit, out-of-range and stale sensor values as faults, not as zero.
- Add plausibility checks between redundant or physically related measurements.
- Set a maximum age for remote commands and reject stale retained MQTT messages for actuator control.
- Use sequence numbers or transaction IDs to prevent replaying an old command after reconnect.
- On communication loss, enter the pre-defined local safe state; do not wait forever for a cloud command.
- Keep safety-critical decisions local and deterministic.

## Runtime behavior

- Keep the control task bounded and independent of web, logging and telemetry tasks.
- Use watchdogs as diagnostics, not as the safety shutdown mechanism.
- Ensure reset, brownout and firmware update paths leave outputs disabled until self-checks pass.
- Store fault cause and event history without delaying the physical safe-state transition.
- Use an independent hardware timeout or safety circuit when a software task cannot meet the required stop time.

## Verification

1. Test the state machine on the host with every input combination and transition.
2. Inject stuck-high, stuck-low, open-wire and stale sensor conditions.
3. Interrupt power and reset the MCU while each actuator is commanded on.
4. Simulate welded contactor feedback and prove restart is inhibited.
5. Remove network connectivity and replay an old command after reconnect.
6. Measure physical de-energization time with a scope or current probe.
7. Review the independent safety chain separately from firmware acceptance tests.

## Acceptance criteria

- A hazard-to-safe-state matrix exists for every output.
- Host tests cover all fault and re-arm transitions.
- Hardware tests prove default-off behavior and measured stop time on the named board.
- Safety-rated functions are implemented and assessed independently of ESP32 firmware.

## References

- IEC 61508 overview: https://www.iec.ch/functional-safety
- IEC 60204-1 machinery electrical equipment: https://webstore.iec.ch/
- ESP-IDF watchdog guidance: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/wdts.html
