---
name: telemetry
description: "Time-series data ingestion, sensor sampling intervals, deadbanding, compaction, protocol buffers (Protobuf), and buffering"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/telemetry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# IoT Telemetry Systems

## Scope
Telemetry systems capture, serialize, buffer, and transport continuous sensor time-series streams efficiently over constrained and intermittent communication links.

## Optimization Strategies
- **Serialization**: Compact binary formats (Protocol Buffers, CBOR, MessagePack) reducing payload size by $60-85\%$ compared to JSON.
- **Data Reduction Techniques**:
  - Deadbanding: Transmit only when value changes by $> \Delta x$.
  - Trend-Triggered Sampling: Increase sampling frequency during transient events (vibration spike, thermal runaway).
- **Local Storage & Forward**: Non-volatile flash buffer storing records with timestamps when offline; batch sync upon reconnection.

## Tools & Standards
- **Software**: Protocol Buffers (nanopb for C), TimescaleDB, InfluxDB, Apache Kafka.
