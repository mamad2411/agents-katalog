---
title: Electrical Short-Circuit Analysis
description: Execute fault current calculation (3-phase, L-G, L-L, L-L-G) per IEC 60909/IEEE standards for electrical system protection and equipment rating verification
version: 1.0
frequency_percent: 75.0
success_rate_percent: 92.0
gigabrain_tags: domainforge_ai, electrical-engineering, short-circuit, fault-current, IEC-60909, IEEE-399, protection
openstinger_context: electrical-study, fault-analysis
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00860_electrical-engineering/agent-data/domain-knowledge/00860_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/skills/domainforge_ai/electrical-cable-sizing/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/electrical-protection-coordination/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/electrical-arc-flash-analysis/SKILL.md
related_skills:
  - electrical-cable-sizing
  - electrical-protection-coordination
  - electrical-arc-flash-analysis
---

# Electrical Short-Circuit Analysis

## Overview
An AI-native short-circuit analysis skill that calculates fault currents per IEC 60909/IEEE 399 standards. Used to verify equipment ratings, coordinate protection devices, and ensure system safety through comprehensive fault analysis.

## When to Use This Skill
- Performing short-circuit studies for new or modified electrical systems
- Sizing cables for short-circuit withstand (used by cable sizing skill)
- Verifying equipment fault duty against available fault current
- Supporting protection coordination analysis
- Arc flash analysis input

## Prerequisites
- Single-line diagram with complete system topology
- Equipment impedance data (transformers, generators, cables, motors)
- Utility source data (available fault MVA or source impedance)
- System operating mode (maximum/minimum fault level)

## Step-by-Step Execution

### Step 1: Build System Model
- Identify all buses and interconnections from SLD
- Assign positive/negative/zero-sequence impedances to each component
- Verify transformer winding connections for zero-sequence paths
- Document system voltage levels and base MVA

### Step 2: Calculate Thevenin Equivalent
- Reduce network to Thevenin equivalent at each fault location
- Calculate source impedance including utility contribution
- Include motor contributions (2-6x rated current for L-L-G faults)
- Verify network reduction accuracy

### Step 3: Calculate 3-Phase Symmetrical Fault Current
```
I''k3 = c × U_n / (√3 × Z_k)
where:
  c = voltage factor (1.05 for LV, 1.10 for HV)
  U_n = nominal voltage
  Z_k = total positive-sequence impedance to fault point
```

### Step 4: Calculate Asymmetrical (Peak) Fault Current
```
i_p = κ × √2 × I''k
where:
  κ = 1.02 + 0.98 × e^(-3R/X) (IEC 60909)
  R/X = ratio at fault point
```

### Step 5: Calculate L-G, L-L, L-L-G Fault Currents
- Use symmetrical component method
- L-G: I_f = 3 × V_1 / (Z_1 + Z_2 + Z_0)
- L-L: I_f = V_1 / (Z_1 + Z_2)
- L-L-G: Use positive/negative/zero-sequence network
- Compare with 3-phase result (L-G may exceed 3-phase in solidly grounded systems)

### Step 6: Verify Equipment Fault Duty
- Compare calculated fault current against equipment short-circuit rating
- Verify breaker interrupting capacity
- Verify busbar and cable short-time withstand (I²t)
- Identify equipment requiring upgrade

### Step 7: Document Results
- Record fault currents at each bus
- Generate fault current table
- Identify critical buses with highest fault levels
- Document equipment duty verification status

## Success Criteria
- Fault currents calculated for all required fault types (3-phase, L-G, L-L, L-L-G)
- Results within 5-10% of independent verification
- Equipment duty verified or deficiencies documented
- IEC 60909 or IEEE 399 methodology correctly applied
- All calculations documented with source data

## Common Pitfalls
- **Incorrect Impedance Data**: Using nameplate impedance instead of tested values gives inaccurate results
- **Missing Zero-Sequence Data**: Incomplete transformer/connection data leads to wrong L-G fault calculations
- **Motor Contribution Ignored**: Motors contribute significant fault current during first few cycles
- **Infinite Bus Assumption**: Assuming zero source impedance overestimates fault currents, leading to oversized equipment
- **Wrong Method**: Using IEC 60909 initial symmetrical peak vs RMS method inconsistently

## Cross-References
- IEC 60909: Short-circuit currents in three-phase AC systems
- IEEE 399: Recommended Practice for Industrial and Commercial Power Systems Analysis
- IEC 60947: Low-voltage switchgear fault rating
- Cable sizing skill: Uses short-circuit withstand in sizing
- Protection coordination skill: Uses fault currents for relay settings
- Arc flash analysis skill: Uses bolted fault current as input

## Usage Example
```
Scenario: Calculate fault current at 415V bus of 1MVA transformer
Input: Utility fault MVA = 500, Transformer Z = 5.5%, Cable Z = 0.002 + j0.003 ohm
Step 1: Model system (utility → transformer → cable → 415V bus)
Step 2: Calculate total impedance to 415V bus = 0.017 + j0.065 ohm
Step 3: I''k3 = 1.05 × 415 / (√3 × 0.067) = 3,745 A
Step 4: i_p = κ × √2 × 3,745 = 1.72 × 1.414 × 3,745 = 9,090 A
Step 5: L-G fault = 3,200 A (with solid grounding)
Step 6: Verify breaker rated > 4,500 A Icu ✓
Step 7: Document results and equipment verification
```

## Metrics
- Typical accuracy: ±5-10% vs independent calculation
- Execution time: 5-15 minutes per bus for simple systems
- Equipment coverage: 100% of affected equipment assessed