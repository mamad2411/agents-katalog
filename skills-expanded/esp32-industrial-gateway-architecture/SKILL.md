---
name: esp32-industrial-gateway-architecture
description: Use when designing an ESP32 industrial gateway between Modbus, CAN, Ethernet, Wi-Fi, LoRa, MQTT or cloud services.
license: MIT
---

# Industrial Gateway Architecture

A gateway joins systems with different timing, trust and failure assumptions. It must isolate slow networks from real-time control, preserve message meaning and fail safely when one side disappears.

## Define boundaries

Draw each physical interface, voltage domain, protocol, data owner and failure domain. Separate deterministic control from best-effort telemetry and cloud connectivity. Define whether the gateway is transparent, translating, aggregating or controlling; each mode has different safety implications. Document data rate, latency, burst size and acceptable loss for every link.

## Software architecture

Give each peripheral driver a clear owner task and bounded queue. Use typed internal messages with timestamp, source, quality, sequence and schema version. Keep protocol adapters separate from business logic and transport adapters. Use backpressure and explicit drop policies; never let a cloud outage block a fieldbus task.

## Reliability and security

Authenticate remote management and updates; do not trust LAN presence as authorization. Segment industrial and management networks where possible. Store credentials in protected storage and never log secrets. Define safe local behavior when MQTT, DNS, Ethernet or radio is unavailable.

## Observability

Expose link state, reconnect count, queue depth, dropped messages, protocol errors and uptime. Preserve raw fault context and monotonic timestamps. Distinguish degraded, disconnected and failed hardware. Provide a local service mode that does not require cloud access.

## Verification

| Scenario | Required property |
|---|---|
| Cloud offline | Local control continues |
| Fieldbus timeout | Bounded retry, visible fault |
| Queue saturation | Defined drop/backpressure policy |
| Gateway reboot | Outputs safe; state reconciled |
| Duplicate/reordered messages | Idempotency or sequence handling |
| Credential compromise | Rotation and revocation procedure |

## Agent rules

Do not implement protocol translation inside ISRs or callbacks. Do not make safety-critical control depend on cloud round trips. Include a failure-mode table and recovery behavior. State which timing guarantees Wi-Fi/TCP do not provide.

