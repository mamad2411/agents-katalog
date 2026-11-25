---
name: esp32-sx126x-lora
description: Use when integrating SX1261/SX1262 radios, diagnosing BUSY/DIO1 issues, configuring RF paths or migrating from SX127x.
license: MIT
---

# Sx126x Lora

SX126x uses a command-based interface with BUSY handshaking and different control semantics from SX127x. A driver written for SX127x cannot be reused by changing only the chip name.

## Board integration

Confirm module variant, frequency band, TCXO supply/control, RF switch configuration, antenna path and reset wiring. SX1261 and SX1262 have different output-power capabilities; respect module thermal and supply limits. Check BUSY is connected to the correct GPIO and is not treated as an ordinary interrupt.

## Command sequencing

Wait for BUSY to deassert within a bounded timeout before issuing commands. Respect reset and wakeup sequences and check command status. Configure packet type, RF frequency, modulation parameters, packet parameters, buffer base addresses and IRQ routing explicitly. Clear handled IRQ flags to avoid repeated events.

## LoRa link budget

Choose spreading factor, bandwidth, coding rate, preamble and payload length based on link budget and airtime. Evaluate receive sensitivity against actual bandwidth and implementation. Account for regional duty-cycle, dwell-time and EIRP limits. ADR and retransmissions must not violate airtime rules.

## Debugging

Capture RESET, BUSY, NSS/SCK/MOSI/MISO and DIO1. A permanently high BUSY line may indicate wiring, reset, power or driver sequencing problems. A missing DIO1 event may be IRQ routing/mask configuration, not RF range. Verify with a minimal transmit/receive example before adding LoRaWAN.

## Agent rules

State exact radio/module variant and board RF switch. Never assume SX127x register APIs apply. Use bounded BUSY waits, IRQ diagnostics and region-specific airtime checks.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
