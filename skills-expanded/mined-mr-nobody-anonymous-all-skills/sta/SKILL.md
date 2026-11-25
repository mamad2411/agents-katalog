---
name: sta
description: "Static Timing Analysis: timing arcs, setup/hold checks, recovery/removal, clock jitter, and on-chip variation (OCV/AOCV/POCV)"
category: semiconductor
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/semiconductor/sta/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Static Timing Analysis (STA)

## Scope
STA exhaustively validates the timing performance of all electrical paths in a digital design under best/worst process, voltage, and temperature (PVT) corners.

## Timing Analysis Methodology
- **Timing Arcs**: Pin-to-pin cell delay look-up tables (NLDM, CCS, ECSM) based on input transition time (slew) and output capacitive load ($C_{\text{load}}$).
- **On-Chip Variation (OCV / POCV)**: Applying statistical derating factors to capture intra-die process variations.
- **Asynchronous Checks**: Recovery time (time reset must remain deasserted before clock edge) and Removal time.

## Tools & Standards
- **Software**: Synopsys PrimeTime, Cadence Tempus.
- **Standards**: Liberty format (`.lib`), Synopsys Design Constraints (`.sdc`).
