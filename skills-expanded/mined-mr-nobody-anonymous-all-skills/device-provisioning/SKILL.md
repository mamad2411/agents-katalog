---
name: device-provisioning
description: "Zero-touch provisioning, PKI certificate enrollment (EST/SCEP), secure elements, factory flashing, and cloud registration"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/device-provisioning/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# IoT Device Provisioning & PKI

## Scope
Device provisioning ensures that only authentic, untampered IoT devices are admitted to corporate and cloud networks, establishing cryptographic identity during manufacturing.

## Enrollment Protocols & Security
- **Public Key Infrastructure (PKI)**:
  - Factory Root Certificate Authority (CA) signs intermediate Device CA.
  - Unique Device Certificate and Private Key generated inside secure element (never leaves silicon).
- **Enrollment Protocols**: Enrollment over Secure Transport (EST, RFC 7030), SCEP.
- **Cloud Registration**: AWS IoT Fleet Provisioning, Azure Device Provisioning Service (DPS) with symmetric key or X.509 attestation.

## Tools & Standards
- **Standards**: IETF RFC 7030 (EST), IEEE 802.1AR (Secure Device Identity).
