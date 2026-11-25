---
name: esp32-sparkplug-b-mqtt
description: Use when an ESP32 publishes to an industrial MQTT broker that expects Sparkplug B - Ignition, HiveMQ, or a plant historian - and the topic namespace, birth messages or sequence numbers are wrong.
license: MIT
---

# Sparkplug B on ESP32

Sparkplug B is a specification on top of MQTT that makes device data
self-describing and stateful. A broker or SCADA host that speaks Sparkplug will
reject plain JSON topics, and a device that publishes without a birth message
appears as unknown.

## The topic namespace is the contract

```
spBv1.0/<group_id>/<message_type>/<edge_node_id>[/<device_id>]
```

| Message | When |
|---|---|
| NBIRTH | node comes online, declares every metric |
| NDATA | periodic or change-of-state data |
| NDEATH | published by the **broker** as the will message |
| DBIRTH / DDATA / DDEATH | same for a child device |
| NCMD / DCMD | commands from the host |

The node id, group id and metric names are not free choices - they are what the
host is configured with. Get them from the host's device definition.

## Payload is protobuf, not JSON

The payload is a Protocol Buffers message (`sparkplug_b.proto`). On an ESP32 that
means either a small hand-written encoder for the fields you use, or nanopb. The
encoder must handle the `metrics` repeated field, `timestamp`, `alias` and
`datatype`; the host maps aliases to names from the birth message, so an alias
that is not in NBIRTH is a dropped metric.

## Sequence numbers and bdSeq

- `seq` increments 0 to 255 and wraps. The host uses it to detect gaps.
- `bdSeq` increments per **reboot** and is sent in NBIRTH; NDEATH carries the same
  value. A device that restarts bdSeq at 0 every boot confuses the host's session
  tracking.
- The will message must be NDEATH, registered at connect time, or the host never
  learns the device died.

## Timestamps

Every metric needs a timestamp in milliseconds since epoch. A device without an
RTC sends 1970 until SNTP completes, and the historian files the data under 1970.
Either wait for time sync before NBIRTH, or use the birth timestamp consistently
and let the host stamp on receipt.

## Symptom table

| Symptom | Usually |
|---|---|
| device shows as unknown in Ignition | NBIRTH missing or malformed |
| metrics appear then vanish | alias not declared in NBIRTH |
| data with 1970 timestamps | no time sync before publishing |
| host reports sequence gaps | seq not incremented per message |
| offline detection never fires | will topic is not NDEATH |
| commands ignored | NCMD subscription topic wrong |

## Agent rules

- Take group id, node id and metric names from the host configuration, never
  invent them.
- Declare every alias in NBIRTH before using it in NDATA.
- Persist bdSeq and seq across reboots; both are part of the contract.
