---
name: esp32-ethercat-gateway-boundary
description: Use when evaluating EtherCAT integration, an ESP32 gateway boundary or translating industrial real-time fieldbus data.
license: MIT
---

# Ethercat Gateway Boundary

EtherCAT is a deterministic industrial Ethernet fieldbus with strict timing and topology requirements. A normal ESP32 Ethernet interface, W5500 socket or lwIP TCP/IP stack is not an EtherCAT master/slave implementation.

## Capability boundary

Do not promise EtherCAT master/slave behavior from RMII Ethernet or W5500 hardware. Determine whether the requirement is monitoring through a separate gateway, bridging non-real-time telemetry, or implementing a certified EtherCAT node. The latter requires a suitable ESC, stack, timing design and conformance validation.

## Topology and timing

Record cycle time, distributed-clock requirements, frame size, node count and topology. Keep ordinary IP traffic and application logging away from deterministic cycle handling. Assess vendor stack licensing, reference clock, synchronization and watchdog behavior using the selected vendor documentation.

## Gateway pattern

Use a dedicated EtherCAT master/controller or industrial edge computer to expose a supported northbound interface such as Modbus TCP, OPC UA or MQTT. The ESP32 can consume this northbound interface for supervisory telemetry where timing requirements allow it. Preserve quality flags, timestamps and source identity.

## Safety and validation

Never route safety-critical motion or interlocks through a best-effort Wi-Fi/cloud gateway. Validate vendor stack licensing, conformance test requirements, EMC, isolation and recovery behavior. Define safe behavior on lost master, cable break and watchdog expiry.

## Decision table

| Requirement | ESP32 role |
|---|---|
| EtherCAT real-time master | Use dedicated supported controller/stack |
| EtherCAT slave device | Requires suitable ESC and validated stack |
| Telemetry mirror | Northbound gateway client may be suitable |
| Cloud dashboard | Consume buffered gateway telemetry |
| Safety motion control | Do not delegate to best-effort ESP32 link |

## Agent rules

State clearly when EtherCAT is outside the ESP32 native capability boundary. Do not confuse Ethernet frame access with EtherCAT conformance. Require cycle-time and recovery measurements before claiming suitability.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
