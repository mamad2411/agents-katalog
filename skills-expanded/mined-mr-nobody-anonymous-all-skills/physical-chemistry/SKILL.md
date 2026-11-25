---
name: physical-chemistry
description: "Chemical thermodynamics, statistical thermodynamics, chemical kinetics, quantum chemistry, and spectroscopy fundamentals"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/physical-chemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Physical Chemistry

## Scope
Physical chemistry applies the principles of physics to chemical systems, encompassing macroscopic thermodynamics, reaction rates, molecular quantum mechanics, and statistical mechanics.

## Core Formulations

### 1. Chemical Thermodynamics & Equilibrium
- **Gibbs Free Energy**: $G = H - TS = U + PV - TS$.
- **Reaction Equilibrium**:
  $$\Delta G^\circ = -RT \ln K_{eq}$$
- **Van 't Hoff Equation**:
  $$\frac{d \ln K_{eq}}{dT} = \frac{\Delta H^\circ}{RT^2} \implies \ln \frac{K_2}{K_1} = -\frac{\Delta H^\circ}{R}\left(\frac{1}{T_2} - \frac{1}{T_1}\right)$$
- **Chemical Potential**: $\mu_i = \left(\frac{\partial G}{\partial n_i}\right)_{T, P, n_{j\neq i}} = \mu_i^\circ + RT \ln a_i$.

### 2. Chemical Kinetics & Transition State Theory
- **Integrated Rate Laws**:
  - 0-order: $[A]_t = [A]_0 - kt$, $t_{1/2} = [A]_0 / (2k)$
  - 1st-order: $\ln [A]_t = \ln [A]_0 - kt$, $t_{1/2} = \ln 2 / k$
  - 2nd-order: $1/[A]_t = 1/[A]_0 + kt$, $t_{1/2} = 1 / (k[A]_0)$
- **Arrhenius Equation**: $k = A \exp(-E_a / RT)$.
- **Eyring-Polanyi Transition State Equation**:
  $$k = \frac{k_B T}{h} \exp\left(-\frac{\Delta G^{\ddagger}}{RT}\right) = \frac{k_B T}{h} \exp\left(\frac{\Delta S^{\ddagger}}{R}\right) \exp\left(-\frac{\Delta H^{\ddagger}}{RT}\right)$$

### 3. Molecular Spectroscopy Principles
- **Rotational (Microwave)**: $E_J = B J(J+1)$, selection rule $\Delta J = \pm 1$.
- **Vibrational (IR)**: Harmonic oscillator $E_v = (v + 1/2)\hbar\omega$, selection rule $\Delta v = \pm 1$.
- **Electronic (UV-Vis)**: Franck-Condon principle (electronic transitions are instantaneous relative to nuclear motion).

## Tools & Standards
- **Software**: Cantera, Thermo-Calc, Gaussian, NWChem, Q-Chem.
- **Canonical References**: Atkins & de Paula — *Physical Chemistry*; McQuarrie & Simon — *Physical Chemistry: A Molecular Approach*.
