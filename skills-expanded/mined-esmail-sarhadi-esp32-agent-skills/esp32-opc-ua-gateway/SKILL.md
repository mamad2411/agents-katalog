---
name: esp32-opc-ua-gateway
description: Use when connecting ESP32 telemetry to OPC UA systems through an industrial gateway, edge computer or protocol bridge.
license: MIT
---

# Opc Ua Gateway

OPC UA is a substantial information-model and security stack. An ESP32 should not be assumed to host a full industrial OPC UA server merely because it can publish MQTT or HTTP.

## Architecture choice

For constrained ESP32 nodes, prefer a well-defined field protocol or MQTT/HTTPS uplink to an edge gateway that hosts OPC UA when full server capabilities, certificates, namespaces, subscriptions and information models are required. If using an embedded OPC UA stack, verify supported profile, memory footprint, licensing and security features on the exact target.

## Information model

Map each signal to a stable NodeId, BrowseName, data type, engineering unit, access level, timestamp and quality/status. Preserve source timestamp and distinguish sensor value from gateway receipt time. Define namespace and schema versioning before deployment; avoid changing NodeIds across firmware releases without migration policy.

## Security

Use certificate-based application authentication and trust-list lifecycle. Define certificate issuance, rotation, revocation and time synchronization. Disable anonymous access unless explicitly justified. Restrict writable nodes and validate commands at the device boundary. Network segmentation is not a substitute for application authentication.

## Data quality and outages

Represent stale, uncertain, out-of-range and disconnected states explicitly. Queue telemetry with bounded storage and clear overflow policy. Do not silently convert communication loss into a valid zero. Define whether commands are rejected, queued or expired while the device is offline.

## Verification

| Scenario | Required behavior |
|---|---|
| Gateway offline | Local control remains independent |
| Certificate expired | Connection rejected and diagnostic exposed |
| Node schema upgrade | Stable identity or documented migration |
| Stale sensor | Quality indicates stale/uncertain |
| Unauthorized write | Denied and audited |

## Agent rules

Do not call MQTT-to-OPC-UA bridging native OPC UA support. State which endpoint owns certificates and NodeIds. Include quality, timestamps and schema version in the mapping contract.

## Field evidence to capture

- Record the exact ESP32 SoC, module, board revision and schematic revision.
- Record framework, compiler, driver version and relevant configuration flags.
- Preserve raw measurements and error codes before applying filters or retries.
- Separate a suspected cause from a reproduced root cause and a verified fix.
- Link the test result to a reproducible fixture or documented manual procedure.

## Version and safety boundary

Check the selected target's datasheet, errata and framework release notes before choosing APIs or pin capabilities. Electrical protection, isolation, overcurrent limits and safe outputs must be designed independently of firmware. A passing host test is not evidence of electrical compliance or field reliability.
