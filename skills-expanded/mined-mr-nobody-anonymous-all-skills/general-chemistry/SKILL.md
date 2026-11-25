---
name: general-chemistry
description: "Stoichiometry, atomic structure, periodic trends, chemical bonding, gas laws, solutions, and thermochemistry"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/general-chemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# General Chemistry

## Scope
General chemistry establishes the fundamental principles governing matter, its properties, transformations, and energy changes. This skill provides systematic calculation frameworks and experimental principles for stoichiometric, structural, and thermochemical analysis.

## Core Principles & Formulations

### 1. Stoichiometry & Reaction Yields
- **Molar Mass & Mole Concept**: $n = m / M$, where $m$ is mass (g) and $M$ is molar mass (g/mol).
- **Limiting Reactant Determination**:
  1. Calculate moles of each reactant: $n_i = m_i / M_i$.
  2. Normalize by stoichiometric coefficient: $\xi_i = n_i / \nu_i$.
  3. Limiting reactant is the reactant with $\min(\xi_i)$.
- **Theoretical & Percent Yield**:
  $$\text{Percent Yield} = \left(\frac{\text{Actual Yield}}{\text{Theoretical Yield}}\right) \times 100\%$$

### 2. Electronic Structure & Periodic Trends
- **Quantum Numbers**: $n$ (principal, $1,2,\dots$), $l$ (orbital angular momentum, $0\dots n-1$), $m_l$ (magnetic, $-l\dots +l$), $m_s$ (spin, $\pm 1/2$).
- **Aufbau Principle, Hund's Rule, Pauli Exclusion Principle**: Fill lowest energy subshells ($1s < 2s < 2p < 3s < 3p < 4s < 3d$).
- **Periodic Trends**:
  - *Atomic Radius*: Increases down a group, decreases across a period.
  - *Ionization Energy*: Decreases down a group, increases across a period: $X(g) \to X^+(g) + e^-$.
  - *Electronegativity*: Pauling scale, highest for F (3.98), decreases down and left.

### 3. Gas Laws & Solutions
- **Ideal Gas Equation**: $PV = nRT$, with $R = 0.08206\text{ L}\cdot\text{atm}/(\text{mol}\cdot\text{K}) = 8.314\text{ J}/(\text{mol}\cdot\text{K})$.
- **Van der Waals (Real Gases)**:
  $$\left(P + \frac{an^2}{V^2}\right)(V - nb) = nRT$$
- **Solution Concentrations**:
  - Molarity: $M = n_{\text{solute}} / V_{\text{solution}} (\text{L})$
  - Molality: $m = n_{\text{solute}} / m_{\text{solvent}} (\text{kg})$
  - Dilution: $M_1 V_1 = M_2 V_2$

### 4. Thermochemistry
- **First Law of Thermodynamics**: $\Delta U = q + w$, where $w = -P\Delta V$.
- **Enthalpy of Reaction**:
  $$\Delta H_{\text{rxn}}^\circ = \sum \nu_p \Delta H_f^\circ(\text{products}) - \sum \nu_r \Delta H_f^\circ(\text{reactants})$$
- **Hess's Law**: Total enthalpy change is independent of the pathway.

## Standard Analytical Protocols
1. **Titration Calculations**: Equivalence point when $n_{\text{acid}} = n_{\text{base}} \times (\nu_a / \nu_b)$.
2. **Standard Solution Preparation**: Weigh analytical grade reagent on 4-decimal balance, dissolve, quantitatively transfer to volumetric flask, dilute to mark at calibrated temperature ($20^\circ\text{C}$).

## Tools & Standards
- **Standards**: IUPAC Gold Book (Compendium of Chemical Terminology), NIST Chemistry WebBook.
- **Software**: ChemDraw, Avogadro, RDKit, OpenBabel, SciFinder.
- **Canonical References**: Chang & Goldsby — *Chemistry*; Zumdahl — *Chemical Principles*.
