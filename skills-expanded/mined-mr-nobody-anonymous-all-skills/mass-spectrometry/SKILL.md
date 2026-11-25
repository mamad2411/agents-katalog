---
name: mass-spectrometry
description: "Ionization techniques (ESI, MALDI, EI), mass analyzers (Q-TOF, Orbitrap, Quadrupole), fragmentation, and tandem MS (MS/MS)"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/mass-spectrometry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mass Spectrometry

## Scope
Mass spectrometry (MS) measures the mass-to-charge ratio ($m/z$) of gas-phase ions to determine elemental compositions, isotopic patterns, molecular weights, and structural fragmentation.

## Core Components & Architectures

### 1. Ionization Mechanisms
- **Electrospray Ionization (ESI)**: Soft ionization, produces multiply charged ions $[M + zH]^{z+}$; suitable for peptides, proteins, polymers.
- **MALDI**: Matrix-assisted laser desorption ionization; soft ionization generating predominantly singly charged $[M + H]^+$.
- **Electron Ionization (EI)**: Hard ionization ($70\text{ eV}$), extensive fragmentation matching standard NIST spectral libraries.

### 2. Mass Analyzers & Metrics
- **Resolving Power**: $R = m / \Delta m$ (FWHM).
  - Quadrupole: Unit resolution ($R \sim 1,000$)
  - TOF: High resolution ($R \sim 30,000 - 80,000$)
  - Orbitrap / FT-ICR: Ultra-high resolution ($R > 100,000 - 1,000,000$)
- **Mass Accuracy**: $\Delta m_{\text{ppm}} = \frac{m_{\text{exp}} - m_{\text{calc}}}{m_{\text{calc}}} \times 10^6$ ($<5\text{ ppm}$ required for high-res HRMS).

### 3. Tandem Mass Spectrometry (MS/MS)
- Collision-Induced Dissociation (CID), Higher-energy C-trap dissociation (HCD), Electron-transfer dissociation (ETD).
- Proteomics backbone fragmentation: $b$-ions (N-terminal) and $y$-ions (C-terminal).

## Tools & Standards
- **Software**: Xcalibur, MassLynx, Skyline, MaxQuant, OpenMS.
- **Canonical References**: Gross — *Mass Spectrometry: A Textbook*; Watson & Sparkman — *Introduction to Mass Spectrometry*.
