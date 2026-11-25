---
title: Electrical Power Quality Analysis
description: Perform harmonic analysis, power factor correction, voltage fluctuation mitigation per IEEE 519/IEC 61000 standards for electrical systems
version: 1.0
frequency_percent: 60.0
success_rate_percent: 90.0
gigabrain_tags: domainforge_ai, electrical-engineering, power-quality, harmonics, power-factor, IEEE-519, IEC-61000
openstinger_context: electrical-power-quality, harmonic-analysis
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00860_electrical-engineering/agent-data/domain-knowledge/00860_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/skills/domainforge_ai/electrical-load-analysis/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/electrical-protection-coordination/SKILL.md
related_skills:
  - electrical-load-analysis
  - electrical-protection-coordination
---

# Electrical Power Quality Analysis

## Overview
An AI-native power quality skill that performs harmonic analysis, designs power factor correction, and mitigates voltage fluctuations per IEEE 519/IEC 61000 standards for electrical system reliability and compliance.

## When to Use This Skill
- Non-linear loads present (VFDs, UPS, rectifiers, LED drivers)
- Power factor below 0.95 or penalty from utility
- Harmonic distortion causing equipment malfunction or heating
- Voltage fluctuations causing flicker or nuisance tripping
- Commissioning of facilities with sensitive electronic equipment

## Prerequisites
- Load inventory with non-linear load identification
- Harmonic spectrum data (measurement or manufacturer data for VFDs, drives)
- Power quality measurements (voltage THD, current THD, individual harmonics)
- System configuration (source impedance, existing capacitors, transformer data)
- Utility requirements for power factor and harmonics

## Step-by-Step Execution

### Step 1: Identify Non-Linear Loads
- Catalog all equipment that draws non-sinusoidal current
- Document equipment ratings, operating modes, harmonic spectra
- Calculate total non-linear load as percentage of system capacity
- Identify harmonic-producing equipment (VFDs, rectifiers, SMPS, LED drivers)

### Step 2: Measure/Estimate Harmonic Currents
- Obtain harmonic spectra from manufacturer data or measurement
- Calculate individual harmonic currents (h5, h7, h11, h13, etc.)
- Determine characteristic harmonics for each load type
- Account for diversity and phase angle cancellation

### Step 3: Calculate Total Harmonic Distortion (THD)
- Calculate current THD: THDi = √(Σ I_h²)/I_1
- Calculate voltage THD: THDv = √(Σ V_h²)/V_1
- Calculate total demand distortion (TDD) per IEEE 519
- Identify dominant harmonic orders and their magnitudes

### Step 4: Compare to IEEE 519 Limits
- Voltage THD limits: 5% (general systems), 3% (sensitive)
- Current TDD limits: 5-20% depending on Isc/IL ratio
- Individual harmonic limits: 3-15% depending on harmonic order
- Identify which limits exceeded and by how much

### Step 5: Design Mitigation
- **Passive Filters:** Single-tuned (h5, h7, h11) for specific harmonics
- **Active Filters:** Broad-spectrum harmonic cancellation
- **K-Factor Transformers:** Rated for harmonic heating (K-13, K-20, K-30)
- **Detuned Reactors:** Series reactors with capacitors to avoid resonance
- **Harmonic Mitigating Transformers:** Phase-shifting for cancellation
- Size and specify mitigation equipment
- Verify expected reduction in THD/TDD

### Step 6: Calculate Power Factor
- Measure real power (kW), reactive power (kVAR), apparent power (kVA)
- Calculate existing power factor: PF = kW/kVA
- Determine target power factor (typically 0.95-0.98)
- Calculate required correction: kVAR = kW × (tan φ₁ - tan φ₂)

### Step 7: Size Correction Capacitors
- Select capacitor bank size and voltage rating
- Determine switching method (fixed, automatic, stepped)
- **CRITICAL:** Verify no resonance with system harmonics
- Check resonance frequency: f_res = f_system / √(Xc/Xl)
- If resonance near dominant harmonic, add detuning reactor
- Specify capacitor type (dry, oil-filled, harmonic-filtered)

### Step 8: Verify No Resonance
- Model system impedance vs frequency
- Identify parallel resonance frequencies
- Verify resonance not near 5th, 7th, 11th, 13th harmonics
- If resonance exists, redesign with detuned reactors
- Verify harmonic absorption by existing equipment

### Step 9: Document Analysis and Recommendations
- Record measured/calculated THD, TDD, power factor values
- Document mitigation equipment specifications
- Compare before/after harmonic levels
- Provide implementation recommendations with sequencing
- Include maintenance requirements for power quality equipment

## Success Criteria
- Voltage THD within IEEE 519 limits (≤5% general, ≤3% sensitive)
- Current TDD within IEEE 519 limits for Isc/IL ratio
- Power factor improved to ≥0.95
- No resonance conditions with installed capacitors or filters
- Mitigation equipment properly sized and specified
- Analysis documented with before/after comparison

## Common Pitfalls
- **Harmonic Resonance with Capacitors:** Installing power factor capacitors without checking resonance → amplified harmonics, capacitor failure
- **Underestimating Non-Linear Loads:** Missing VFDs, UPS, rectifiers in load inventory → undersized mitigation
- **Missing Interharmonics:** Non-characteristic harmonics between standard order → undetected resonance, equipment stress
- **Wrong Harmonic Spectrum:** Using generic data instead of measured → incorrect filter design
- **Ignoring System Changes:** Future load additions not considered → mitigation inadequate after expansion

## Cross-References
- IEEE 519: Recommended Practice for Harmonic Control in Electric Power Systems
- IEC 61000: Electromagnetic compatibility standards
- 00860 Domain Knowledge: Power quality section (Part 9)
- Electrical Load Analysis: Non-linear load identification
- Protection Coordination: Harmonic impact on relay operation

## Usage Example
```
Scenario: Harmonic analysis for facility with 500kW VFD loads
Step 1: Non-linear loads: 5x 100kW VFDs (20% of 2500kVA system)
Step 2: Harmonic spectra: VFD typical 5th (30%), 7th (20%), 11th (8%), 13th (5%)
Step 3: THDi = 28%, TDD = 8.4% exceeds IEEE 519 limit of 5%
Step 4: Voltage THD = 4.2% below 5% limit but margin small; TDD exceeds limit
Step 5: Design passive filter for h5 (tuned to 4.7), active filter for h7, h11
Step 6: Existing PF = 0.85, target = 0.95, requires 185kVAR correction
Step 7: 200kVAR automatic capacitor bank with detuning reactors (7% reactance → 189Hz resonance, away from 250Hz h5)
Step 8: Resonance check: system resonance at 189Hz, 5th harmonic at 250Hz → safe margin
Step 9: Document: TDD reduced from 8.4% to 3.5%, PF improved from 0.85 to 0.97
```

## Metrics
- THD reduction: 50-70% reduction from pre-mitigation levels
- Power factor improvement: ≥0.95 sustained
- Resonance margin: ≥15% away from dominant harmonic frequencies
- Equipment protection: Zero capacitor failures from harmonic resonance