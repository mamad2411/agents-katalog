---
name: esp32-fault-injection-hil
description: Use when creating hardware-in-the-loop tests, fault injection, soak tests or regression rigs for ESP32 industrial devices.
license: MIT
---

# Fault Injection Hil

Host tests and compilation prove only part of an embedded system. HIL is required for electrical timing, brownout, radio coexistence, bus contention, power loss and hardware-specific behavior.

## Test layers

Host tests validate parsers, state machines, CRCs, scaling and deterministic logic. Simulator tests validate selected scenarios but do not prove analog behavior or RF performance. On-target tests validate compiled firmware and drivers. HIL validates board, wiring, power, external devices and timing as an integrated system.

## Fixture design

Give each fixture controlled power, current measurement, programmable load or relay matrix, serial capture and safe emergency stop. Use isolated interfaces where the DUT connects to industrial voltages or external networks. Identify instruments, calibration date, firmware version and wiring revision. Prevent fixture faults from applying destructive energy to the DUT.

## Fault injection catalogue

Inject power interruption at boot, flash erase/write, OTA verification and runtime. Inject UART framing errors, RS485 collision, missing termination, stuck I2C line and CAN bus-off. Simulate DHCP/DNS outage, Wi-Fi AP loss, TLS certificate failure and peer reset. Test sensor open/short, ADC overrange, relay inrush and thermal corners.

## Measurement and pass criteria

Define recovery time, data-loss bound, safe output state and maximum retry count before running. Capture raw logs, rail waveforms, bus traces, reset reason and fixture state on every failure. Repeat enough times to expose intermittent faults; report sample count and confidence. Separate one successful run from a statistically meaningful soak.

## CI integration

| Test class | CI execution |
|---|---|
| Host unit / fuzz | Every pull request |
| Build matrix | Every pull request |
| Simulator | Every pull request where deterministic |
| On-target smoke | Scheduled or hardware runner |
| HIL / soak | Nightly or release candidate |

## Agent rules

Never label a software unit test as hardware validation. Keep test wiring, fixture firmware and DUT firmware versioned. Make failures reproducible from captured artifacts. Ensure fault injection cannot create unsafe field outputs.


## Evidence record

For each fixture run, save the wiring revision, instrument settings, firmware hash, raw capture and pass/fail criteria so another engineer can reproduce the same fault.
