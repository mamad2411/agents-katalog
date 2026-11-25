---
name: actuators
description: "IoT actuation: relays, solid-state relays (SSR), solenoid valves, PWM motor drivers (H-Bridge), and servo positioning"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/actuators/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# IoT Actuator Control

## Scope
Actuation engineering interfaces microcontrollers with high-voltage and high-current electrical/mechanical loads, ensuring galvanic isolation and reliable switching.

## Actuation Circuits & Drivers
- **Electromechanical Relays vs. SSRs**: Flyback diodes ($1N4007$) across inductive coils; Optocouplers ($4N35$) providing $>2.5\text{ kV}$ galvanic isolation between digital MCU and AC/DC mains.
- **H-Bridge DC Motor Control**: Direction control via 4 MOSFET switches; PWM switching frequency ($10-25\text{ kHz}$) above human auditory threshold; dead-time insertion to prevent shoot-through.

## Tools & Standards
- **Standards**: UL 508 (Industrial Control Equipment).
