---
name: iot-platform
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: IoT platform architecture, device management system, telemetry ingestion pipeline, firmware OTA update, device twin, IoT edge gateway, sensor data processing, IoT device provisioning, industrial IoT, MQTT broker design, device lifecycle management, IoT data pipeline
compose: edge-computing
---

# Skill — IoT Platform

## When this skill activates
This skill activates when building IoT device management systems, telemetry ingestion pipelines, firmware over-the-air (OTA) update mechanisms, device twin/shadow architectures, edge-to-cloud data flows, MQTT brokers, device provisioning, or industrial IoT platforms.

## Mandatory actions when this skill is active

### Before writing any code
1. Design device lifecycle management: provisioning (certificate issuance, device registration, initial config push) → active (telemetry streaming, command execution) → maintenance (firmware updates, config changes) → decommissioning (certificate revocation, data archival), with state machine transitions and audit trails
2. Model telemetry ingestion architecture: devices publish MQTT messages (QoS 1 for critical, QoS 0 for high-frequency) → broker buffers (HiveMQ, AWS IoT Core) → stream processor (Kafka, Kinesis) → time-series database (InfluxDB, TimescaleDB) → analytics/alerting, with backpressure handling and dead letter queues
3. Map device twin/shadow pattern: desired state (cloud wants device at firmware v2.1, config A) vs reported state (device currently at v2.0, config B) → delta detection → command sent to device → device applies change → reports new state → convergence detected

### During implementation
- Implement MQTT broker with scalability: support 100K+ concurrent connections, message throughput (10K msg/sec), QoS 0/1/2 support (at-most-once, at-least-once, exactly-once), retained messages (last known state), last will and testament (detect disconnections), topic ACLs (device can only publish to devices/{device_id}/telemetry)
- Build device provisioning flow: device boots with factory cert → requests device-specific cert from provisioning service (using CSR) → service validates manufacturing batch, issues cert signed by CA, registers device in registry → device stores cert in secure element (TPM, TEE) → uses cert for future MQTT authentication
- Design firmware OTA update with safety: cloud creates firmware campaign (target devices by tag, rollout percentage), device polls for updates (or push notification), downloads firmware chunk-by-chunk (resumable, checksum verified), stores in secondary partition, validates signature (RSA/ECDSA), swaps partitions on next boot, rollback on boot failure (watchdog timer, 3 attempts)
- Implement device twin with conflict resolution: cloud updates desired state (twin document with version), device polls for changes, detects delta, applies change, reports new state, cloud reconciles (last-write-wins or version vector), handle offline devices (queue commands, apply on reconnect up to 7 days)
- Build telemetry pipeline with windowing: ingest raw sensor data (temperature, pressure, vibration at 1 Hz) → stream processor aggregates (1-minute windows: avg, min, max, stddev) → anomaly detection (Z-score >3 triggers alert) → store aggregates (reduce storage 60x), retain raw data for 7 days (hot storage), archive aggregates for 5 years (cold storage)

### After implementation
- Validate device connectivity resilience: simulate network failures (disconnect device mid-message), verify QoS 1 retries (message delivered after reconnect), test persistent sessions (broker retains subscriptions), measure reconnect time (<5s for 95th percentile), verify backoff exponential retry (1s, 2s, 4s, 8s, max 60s)
- Test firmware OTA reliability: simulate power loss during download (resume from last chunk), corrupt firmware signature (device rejects), partial update failure (automatic rollback to previous version), measure update success rate (>99% for targeted devices), track update latency (time from campaign start to device running new firmware)
- Execute telemetry load testing: simulate 10K devices sending data at 1 Hz (10K msg/sec), measure broker latency (p99 <100ms), stream processor lag (<1s behind real-time), database write throughput (handle burst traffic 10x normal), verify no message loss (QoS 1 delivery confirmed)

## Self-check before task completion
- [ ] Device lifecycle managed: provisioning (cert issuance, registration), active (telemetry/commands), maintenance (OTA updates), decommissioning (cert revocation)
- [ ] MQTT broker scalable: 100K+ concurrent connections, QoS 0/1/2 support, topic ACLs, retained messages, LWT for disconnect detection
- [ ] Device provisioning secure: factory cert → CSR → device-specific cert (signed by CA), stored in secure element (TPM/TEE), cert-based MQTT auth
- [ ] Firmware OTA robust: resumable downloads (chunk-by-chunk), signature validation (RSA/ECDSA), dual-partition swap, automatic rollback on failure
- [ ] Device twin functional: desired vs reported state, delta detection, command queuing for offline devices (7 day retention), conflict resolution
- [ ] Telemetry pipeline optimized: windowed aggregation (1-min windows), anomaly detection (Z-score >3), hot/cold storage tiering (7 days raw, 5 years aggregates)
- [ ] Connectivity resilient: QoS 1 retries, persistent sessions, exponential backoff (1s to 60s), reconnect time <5s for 95th percentile
