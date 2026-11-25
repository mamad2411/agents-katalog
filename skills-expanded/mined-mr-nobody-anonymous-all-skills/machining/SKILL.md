---
name: machining
description: "CNC milling, turning, cutting tool mechanics (Merchant's circle), feeds, speeds, tool wear (Taylor equation), and G-code"
category: mechanical-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mechanical-engineering/machining/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Machining & CNC Fabrication

## Scope
Machining removes material via subtractive mechanical cutting tools, covering CNC milling, lathe turning, grinding, EDM, and tool path optimization.

## Metal Cutting Physics
- **Merchant's Shear Circle**:
  $$\phi = 45^\circ + \frac{\alpha}{2} - \frac{\beta}{2}$$
  where $\phi$ is shear angle, $\alpha$ rake angle, $\beta$ friction angle ($\tan \beta = \mu$).
- **Taylor's Tool Life Equation**:
  $$V T^n = C$$
  where $V$ is cutting speed ($m/min$), $T$ tool life ($min$), $n, C$ empirical constants.
- **Cutting Speed & Feed Rate**:
  - Spindle speed: $N = \frac{1000 V_c}{\pi D}\text{ RPM}$.
  - Feed rate: $v_f = N \times z \times f_z\text{ mm/min}$ ($z$ number of teeth, $f_z$ feed per tooth).

## Tools & Standards
- **Software**: Mastercam, Autodesk Fusion CAM, Siemens NX CAM.
- **Standards**: ISO 6983 (G-code / M-code).
