---
name: electrical
description: "Residential and commercial electrical installation, NEC compliance (NFPA 70), conduit bending, circuit sizing, panel load balancing, and grounding"
category: skilled-trades
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/skilled-trades/electrical/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Electrical Trade & NEC Compliance

## Scope
Electrical installations, service entrance sizing, branch circuit wiring, raceway conduit bending, overcurrent protection, and equipment grounding following the National Electrical Code (NEC / NFPA 70).

## Core NEC Specifications & Calculations
- **Ohm's & Joule's Laws**: $V = I R$, $P = V I = I^2 R$.
- **Continuous Load Sizing (NEC 210.19 / 215.2)**: Conductors and overcurrent protection devices (OCPD) sized for $125\%$ of continuous load ($>3\text{ hours}$) plus $100\%$ of non-continuous load.
- **Voltage Drop Guidelines**: $\Delta V \le 3\%$ for branch circuits, $\Delta V \le 5\%$ total (feeder + branch).
  $$V_{\text{drop}} = \frac{2 K I L}{C_{mil}} \quad (\text{Single-phase copper, } K \approx 12.9)$$
- **Conductor Ampacity & Derating (NEC 310.15)**: Derated by ambient temperature and number of current-carrying conductors in raceway ($4-6$ conductors $\implies 80\%$, $7-9 \implies 70\%$).
- **Grounding vs. Bonding (NEC 250)**: Grounding Electrode Conductor (GEC) connects to earth; Equipment Grounding Conductor (EGC) bonds metallic enclosures to provide low-impedance fault clearing path.

## Standards & Tools
- **Standards**: NFPA 70 (NEC), NFPA 70E (Electrical Safety in the Workplace).
- **Tools**: Digital Multimeter (CAT III/IV), Conduit Benders, Insulation Resistance Tester (Megger).
