---
name: device-management
description: "IoT fleet lifecycle: provisioning, remote configuration, heartbeat monitoring, firmware updates (FOTA), and decommissioning"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/device-management/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# IoT Device Management

## Scope
IoT device management manages the end-to-end lifecycle of distributed hardware fleets, from factory provisioning and secure onboarding to remote monitoring and decommissioning.

## Lifecycle Phases
1. **Onboarding & Provisioning**: Zero-touch bootstrapping using hardware secure elements (ATECC608), X.509 client certificates, and cloud device registries.
2. **Configuration & Digital Twins**: Synchronizing desired device state with reported state across intermittent connectivity.
3. **Firmware Updates (FOTA)**: Phased rollout, canary deployments, automatic rollback on health check failure.
4. **Decommissioning**: Cryptographic zeroization of local secrets and revocation of cloud credentials.

## Tools & Standards
- **Standards**: OMA LwM2M (Lightweight M2M), TR-069.
- **Cloud Suites**: AWS IoT Device Management, Azure IoT Hub Device Management.
