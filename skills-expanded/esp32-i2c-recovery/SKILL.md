---
name: esp32-i2c-recovery
description: Use when an I2C bus hangs, SDA/SCL is stuck, a peripheral powers off independently, or device initialization must recover safely.
license: MIT
---

# I2c Recovery

I2C is an open-drain shared bus. Missing pull-ups, voltage mismatch, power sequencing or a slave holding SDA low can make every device appear dead. Recovery must be bounded and safe for all bus participants.

## Electrical checks

Confirm compatible logic voltage and ensure ESP32 pins are not exposed to 5 V pull-ups. Calculate pull-up resistance from bus capacitance, rise-time requirement and sink-current limits; do not blindly stack breakout-board pull-ups. Assess cable capacitance, routing near switching loads and back-powering when a peripheral is unpowered but bus lines remain high.

## Transaction design

Set a finite transaction timeout supported by the selected framework/driver release. Probe optional devices with bounded retries so an absent sensor cannot block boot indefinitely. Use a single bus owner or documented thread-safe driver. Validate address width, register width, repeated-start behavior and maximum transfer size against the peripheral datasheet.

## Recovery strategy

Determine whether SCL or SDA is held low before attempting recovery. Prefer the official bus-clear/recovery API for the exact ESP-IDF release. GPIO clock-pulse recovery is board-specific: ensure no other master is active and follow I2C bus-clear timing. Reset or power-cycle a faulty peripheral only through a designed reset or switched-power path.

## Verification matrix

| Fault injection | Expected result |
|---|---|
| Device absent at boot | Bounded timeout; system continues safely |
| SDA held low | Recovery attempted and failure reported |
| Slave loses power mid-transaction | Bus returns or device is isolated |
| Two tasks access bus | Serialized transactions |
| Slow rise time | Measured and corrected electrically |

## Agent rules

Do not hide a stuck bus with infinite retry loops. State the I2C driver generation and exact recovery API. Do not pulse SCL blindly when another master may own the bus. Record address, bus speed, pull-up value and measured rise time. Include fault flags in application telemetry.


## Field notes

- Capture SDA and SCL at the device connector during the failure, not only at the MCU pins.
- Record whether the peripheral shares reset and power sequencing with the ESP32.
- A bus recovery that restores logic levels does not prove the peripheral state machine is healthy; reinitialize and verify its identity/configuration registers.
- Keep a counter for recovery attempts and escalate repeated failures to a visible degraded state.
