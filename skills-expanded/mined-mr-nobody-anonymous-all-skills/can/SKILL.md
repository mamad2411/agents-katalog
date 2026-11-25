---
name: can
description: "Controller Area Network (CAN 2.0A/B, CAN FD): differential signaling, bit stuffing, arbitration, error frames, and DBC file parsing"
category: embedded
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/embedded/can/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Controller Area Network (CAN & CAN FD)

## Scope
CAN protocol engineering for automotive, industrial, and aerospace control networks, covering bitwise arbitration, differential PHY, error handling, and CAN FD.

## Protocol Mechanics & Electrical PHY
- **Differential Bus**: CAN_H and CAN_L, $120\Omega$ split termination at both bus ends. Dominant bit (logic 0, $V_{\text{diff}} \approx 2.0\text{ V}$), Recessive bit (logic 1, $V_{\text{diff}} \approx 0.0\text{ V}$).
- **Bitwise Non-Destructive Arbitration**: Lower identifier wins bus control without packet corruption (ID 0x000 has highest priority).
- **Standard (2.0A, 11-bit ID)** vs. **Extended (2.0B, 29-bit ID)**.
- **CAN FD (Flexible Data-Rate)**: Payload extended from 8 bytes up to 64 bytes; bit rate switched up to $5-8\text{ Mbps}$ during data phase.
- **Error Handling**: Bit monitoring, 15-bit CRC, bit stuffing (5 consecutive identical bits $\implies$ 1 inverted stuff bit), automatic node isolation (Error Active $\to$ Error Passive $\to$ Bus Off).

## Tools & Standards
- **Standards**: ISO 11898-1 (Data link layer), ISO 11898-2 (High-speed physical layer).
- **Software**: CANoe, PCAN-View, python-can, cantools.
