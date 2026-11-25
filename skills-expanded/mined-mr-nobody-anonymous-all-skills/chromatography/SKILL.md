---
name: chromatography
description: "HPLC, GC, TLC, column chromatography, separation mechanisms, retention models, and method development"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/chromatography/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Chromatography

## Scope
Chromatography encompasses the physical separation, identification, and purification of components in a complex chemical mixture based on differential partitioning between stationary and mobile phases.

## Fundamental Principles

### 1. Separation Theory & Band Broadening
- **Retention Factor ($k$)**: $k = (t_R - t_0) / t_0$.
- **Separation Factor (Selectivity, $\alpha$)**: $\alpha = k_2 / k_1 \ge 1.0$.
- **Column Efficiency (Plate Count, $N$)**:
  $$N = 16 \left(\frac{t_R}{W}\right)^2 = 5.545 \left(\frac{t_R}{W_{1/2}}\right)^2$$
- **Van Deemter Equation**:
  $$H = A + \frac{B}{u} + C u$$
  where $A$ is eddy diffusion, $B/u$ is longitudinal diffusion, $Cu$ is mass transfer resistance, and $u$ is mobile phase linear velocity.
- **Peak Resolution ($R_s$)**:
  $$R_s = \frac{2(t_{R2} - t_{R1})}{W_1 + W_2} = \frac{\sqrt{N}}{4}\left(\frac{\alpha - 1}{\alpha}\right)\left(\frac{k_2}{1 + k_2}\right)$$
  (Baseline separation requires $R_s \ge 1.5$).

### 2. Modes of Chromatography
- **Reversed-Phase HPLC (RP-HPLC)**: Non-polar stationary phase ($C_{18}, C_8$), polar mobile phase ($H_2O / MeCN / MeOH$). Elution order: Most polar first.
- **Normal-Phase HPLC (NP-HPLC)**: Polar stationary phase (Silica), non-polar mobile phase (Hexane / IPA).
- **Gas Chromatography (GC)**: Volatile/semivolatile analytes, carrier gas ($He, H_2, N_2$), capillary column (DB-5ms), FID/MS detectors.

## Standards & References
- **Standards**: USP <621> Chromatography, EP 2.2.46.
- **Software**: Empower, ChemStation, Chromeleon.
- **Canonical References**: Snyder, Kirkland & Glajch — *Practical HPLC Method Development*.
