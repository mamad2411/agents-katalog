---
name: hydraulic-engineering
description: "Open channel flow, Manning's equation, hydraulic jumps, culvert hydraulics, and pipe network analysis (Hardy Cross)"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/hydraulic-engineering/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Hydraulic Engineering

## Scope
Hydraulic engineering applies fluid mechanics to the conveyance of water through pipes, open channels, spillways, culverts, and pumping systems.

## Formulations
- **Manning's Equation (Uniform Open Channel Flow)**:
  $$Q = \frac{1.486}{n} A R_h^{2/3} S_0^{1/2} \quad (\text{US Customary}), \quad Q = \frac{1}{n} A R_h^{2/3} S_0^{1/2} \quad (\text{SI})$$
  where $R_h = A / P$ is hydraulic radius, $S_0$ channel slope.
- **Froude Number**: $Fr = \frac{v}{\sqrt{g D_h}}$ ($Fr < 1$ subcritical, $Fr = 1$ critical, $Fr > 1$ supercritical).
- **Hydraulic Jump (Belanger's Equation)**:
  $$\frac{y_2}{y_1} = \frac{1}{2}\left(\sqrt{1 + 8 Fr_1^2} - 1\right)$$
- **Pipe Network Analysis (Darcy-Weisbach & Hazen-Williams)**: Head loss $h_f = f \frac{L}{D} \frac{v^2}{2g}$.

## Tools & Standards
- **Software**: HEC-RAS (1D/2D unsteady flow), EPA-NET, Flow-3D.
- **Canonical References**: Chaudhry — *Open-Channel Flow*; French — *Open-Channel Hydraulics*.
