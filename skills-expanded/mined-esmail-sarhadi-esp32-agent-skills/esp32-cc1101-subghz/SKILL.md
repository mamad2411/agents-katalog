---
name: esp32-cc1101-subghz
description: Use when integrating CC1101 sub-GHz radios, diagnosing packet loss, selecting RF settings or building a low-power point-to-point link.
license: MIT
---

# Cc1101 Subghz

CC1101 is a configurable sub-GHz transceiver, not a LoRa modem. Its modulation, packet engine, frequency plan and regulatory constraints differ from SX127x/SX126x LoRa devices.

## Hardware and RF plan

Verify the exact module frequency range, antenna matching, supply decoupling, crystal tolerance and RF layout. Select frequency, bandwidth, deviation, modulation and data rate as a coherent modem profile. A library preset must match the actual crystal and board variant.

## Packet protocol

Define sync word, preamble, packet length mode, CRC, address filtering and whitening consistently on both ends. Add application-level message type, version, sequence number and bounded payload length. Use ACK/retry with backoff only where link budget and regional rules allow it.

## Interrupt and SPI handling

Keep GDO interrupt handlers short; record event and defer SPI reads to a task. Check SPI mode, maximum clock and chip-select timing from the datasheet. Handle FIFO overflow/underflow and radio state transitions explicitly. Do not perform long SPI transactions inside an ISR.

## Range and regulation

Measure RSSI and packet error rate across distance, antenna orientation and interference conditions. Verify legal band, EIRP, channel access, duty-cycle and listen-before-talk requirements for deployment region. Do not infer range from advertised module power alone.

## Regression matrix

| Test | Measure |
|---|---|
| Wrong modem profile | Sync/CRC failure counter |
| Burst traffic | FIFO overflow and loss |
| Weak signal | PER vs RSSI |
| Radio reset mid-packet | State-machine recovery |
| Region configuration | Frequency and airtime compliance |

## Agent rules

Never describe CC1101 as LoRa. Record all modem registers/profile parameters and crystal frequency. Avoid unbounded retransmissions and verify regional radio rules before field deployment.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
