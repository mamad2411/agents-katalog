---
name: solar-installation
description: "Photovoltaic (PV) system installation: string sizing, open-circuit voltage calculations, microinverters vs. string inverters, and NEC 690 rapid shutdown"
category: skilled-trades
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/skilled-trades/solar-installation/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Solar PV Installation & NEC 690

## Scope
Rooftop and ground-mount solar photovoltaic system installation, racking mechanics, DC string voltage calculations, inverter configurations, and rapid shutdown safety compliance.

## Electrical Calculations & NEC 690
- **Maximum System Voltage (NEC 690.7)**:
  $$V_{\max} = V_{oc} \times \left[1 + \beta_{Voc} (T_{\min} - 25^\circ\text{C})\right] \times N_{\text{modules}}$$
  Must not exceed inverter maximum DC input voltage or $600\text{ V}$ (residential) / $1000\text{ V}$ (commercial).
- **Overcurrent Protection (NEC 690.8)**: Conductors and OCPD sized for $1.25 \times 1.25 \times I_{sc} = 1.56 \times I_{sc}$.
- **NEC 690.12 Rapid Shutdown**: Voltage inside array boundary reduced to $\le 80\text{ V}$ within 30 seconds of initiation.

## Standards & Tools
- **Standards**: NFPA 70 Article 690/705, UL 1741, IEEE 1547.
- **Tools**: Solar PV I-V Curve Tracer, MC4 crimper, Solar irradiance meter.
