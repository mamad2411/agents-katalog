---
title: Electrical Arc Flash Analysis
description: Perform IEEE 1584 incident energy calculation, arc flash boundary determination, and PPE assignment for electrical power systems
version: 1.0
frequency_percent: 65.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/electrical-arc-flash-analysis
gigabrain_tags: electrical-engineering, arc-flash, incident-energy, IEEE-1584, PPE, arc-flash-boundary, NFPA-70E, domainforge-ai
openstinger_context: arc-flash-study, incident-energy-calculation, PPE-assignment
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_GLOSSARY.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/ELECTRICAL_AGENTS-REGISTRY-SUMMARY.MD
related_skills:
  - electrical-protection-coordination
  - electrical-sld-processing
  - electrical-cable-sizing
---

# Electrical Arc Flash Analysis

## Overview

Perform arc flash hazard analysis per IEEE 1584: collect system data, calculate bolted fault current at each equipment location, determine arcing current, calculate incident energy at the working distance, determine the arc flash boundary, assign PPE category, generate arc flash warning labels, and document the analysis. This ensures workers are protected from arc flash hazards and equipment is properly labeled with hazard information.

**Announce at start:** "I'm using the electrical-arc-flash-analysis skill to calculate incident energy, determine arc flash boundaries, and assign PPE categories per IEEE 1584."

## When to Use This Skill

**Trigger Conditions:**
- Arc flash hazard assessment required for regulatory compliance (OSHA, NFPA 70E)
- New electrical installation needs arc flash labeling before energization
- System modification (new source, new feeder, protection changes) affects incident energy
- Existing arc flash labels are outdated or system has changed since last study
- Injury investigation or safety audit requires incident energy data
- Risk assessment for energized electrical work permits

**Prerequisites:**
- Fault current data at each equipment location (from short-circuit study)
- Protection device clearing times (from protection coordination study)
- Equipment configuration data (voltage level, bus gap, enclosure type, equipment class)
- Working distance for each equipment type per IEEE 1584 Table 1
- EE-ARC-001 agent or equivalent arc flash analysis capability available
- IEEE 1584 calculation tool or software

## Step-by-Step Procedure

### Step 1: Collect System Data

**Gather all required input data for IEEE 1584 calculations:**

**Data required for each equipment location (bus/switchgear/panel):**
| Data Field | Description | Source |
|------------|-------------|--------|
| Equipment tag | Unique identifier (e.g., MDB-01, DB-A) | SLD / Equipment schedule |
| Equipment type | Switchgear, panelboard, MCC, motor control, feeder | SLD / Equipment schedule |
| Voltage (V) | System voltage at equipment | SLD |
| Equipment class | Class I, II per IEEE 1584 | Equipment datasheet |
| Enclosure type | Open, ventilated box, arc-resistant, etc. | Equipment datasheet |
| Bus gap / electrode configuration | Gap between conductors per IEEE 1584 Table 2 | Equipment datasheet / Standard default |
| Working distance (mm) | Distance from arc source to worker per IEEE 1584 Table 1 | Equipment type |
| Bolted fault current (kA) | Three-phase bolted fault current at bus | Short-circuit study |
| Upstream protective device | Device that clears the arc fault | SLD / Protection study |
| Device clearing time (s) | Total clearing time at the arcing current | Protection coordination study |
| Upstream device type | Relay+CB, fuse, MCCB — method determines calculation | Protection device schedule |
| System grounding | Ungrounded, resistance grounded, solidly grounded | System design |

**Data collection checklist:**
- [ ] Equipment schedule complete for all locations to be analyzed
- [ ] Voltage level confirmed for each location
- [ ] Bus gap / electrode configuration documented (or standard default used)
- [ ] Working distance per equipment type per IEEE 1584 Table 1
- [ ] Bolted fault current available for all bus locations
- [ ] Protective device type and clearing time confirmed for each upstream device
- [ ] Clearing time adjusted for actual arcing current (not bolted fault current)
- [ ] System grounding type documented

### Step 2: Calculate Bolted Fault Current

**Determine bolted three-phase fault current at each equipment location:**

**Calculation methods:**
- If results from short-circuit study available: Use I_sc_bolted directly
- If calculating from system data:
  ```
  I_sc_bolted = S_base / (sqrt(3) x V_base x Z_total)
  ```
  Where Z_total includes source impedance, transformer impedance, cable impedance from source to fault location

**Bolted fault current documentation:**
| Equipment | Voltage (V) | I_sc_bolted (kA) | X/R Ratio | Source | Notes |
|-----------|------------|-----------------|-----------|--------|-------|
| MDB-01 | 11,000 | — | — | Short-circuit study | — |
| DB-A | 400 | — | — | Short-circuit study | — |

**Note:** If the X/R ratio at the fault location differs from the test conditions for the protective device, adjust the clearing time accordingly.

### Step 3: Determine Arcing Current

**Calculate the arcing current (I_arc) using IEEE 1584 empirical equations:**

**IEEE 1584 (2018 Edition) arcing current calculation:**

**For 3-phase arcs in open air or in boxes (0.208 kV to 15 kV):**

The arcing current is typically 80-90% of the bolted fault current for LV systems and varies by voltage, gap, and enclosure.

**Simplified relationship (typical values):**
| System Voltage | Typical I_arc / I_bolted Ratio | Notes |
|---------------|-------------------------------|-------|
| 480V LV | 0.70-0.85 | Depends on bus gap and enclosure |
| 600V MV | 0.80-0.95 | Depends on bus gap and enclosure |
| 4.16kV MV | 0.85-0.95 | Depends on bus gap and enclosure |
| 11kV MV | 0.90-0.98 | Depends on bus gap and enclosure |

**Precise calculation per IEEE 1584 equations:**
The IEEE 1584 calculation tool uses empirical equations that incorporate:
- System voltage (kV)
- Bolted fault current (kA)
- Bus gap (mm)
- Conductor orientation
- Enclosure type and dimensions
- Electrode configuration

**Iterative adjustment for protective device clearing:**
1. Calculate initial I_arc
2. Check protective device TCC at I_arc to find actual clearing time
3. If I_arc is below the device pickup threshold, the device may operate in the long-time region (much longer clearing time) — use the actual clearing time from the TCC at I_arc

**Arcing current checklist:**
- [ ] I_arc calculated per IEEE 1584 equations (not estimated)
- [ ] Arcing current adjusted for bus gap, enclosure, and configuration
- [ ] Protective device clearing time evaluated at I_arc (not at I_sc_bolted)
- [ ] If I_arc is below instantaneous pickup, actual TCC clearing time used

### Step 4: Calculate Incident Energy

**Calculate the incident energy at the working distance using IEEE 1584:**

**Incident energy equation (simplified IEEE 1584):**
```
E = 4.184 x C_f x E_n x (t / 0.2) x (610^x / D^x)
```

**Where:**
- E = incident energy (J/cm²) at the working distance
- C_f = calculation factor (1.0 for voltage >= 1000V, 1.5 for < 1000V)
- E_n = normalized incident energy (from IEEE 1584 equations)
- t = arc clearing time (seconds) — actual clearing time at I_arc
- D = working distance (mm) from the arc source
- x = distance exponent (from IEEE 1584 equations, typically 1.5-2.0 depending on configuration)

**Key factors affecting incident energy:**
| Factor | Impact on Incident Energy |
|--------|--------------------------|
| Arc clearing time | Directly proportional — halving the clearing time halves the incident energy |
| Working distance | Inversely related — greater distance means lower incident energy |
| Bolted fault current | Higher fault current typically means higher incident energy (but may trip faster) |
| System voltage | Affects arcing current ratio and calculation factor |
| Enclosure type | Enclosed arcs generally have higher incident energy than open air |

**Incident energy classification (NFPA 70E Table 130.7(C)(15)(c)):**
| PPE Category | Incident Energy Range (cal/cm²) | Typical Protection Required |
|-------------|-------------------------------|---------------------------|
| Category 1 | Up to 4 cal/cm² | Arc-rated long sleeve + pants or coverall, arc flash face shield |
| Category 2 | 4-8 cal/cm² | Arc flash suit (jacket, pants, or coverall), balaclava, arc flash face shield |
| Category 3 | 8-25 cal/cm² | Arc flash suit (higher rating), balaclava, arc flash hood or face shield |
| Category 4 | 25-40 cal/cm² | Full arc flash suit and hood (highest off-the-shelf rating) |
| > 40 cal/cm² | Prohibited zone — arc flash hazard exceeds PPE | Do NOT work energized; de-energize or implement arc-resistant design |

**Incident energy threshold:**
- Hazard exists when incident energy >= 1.2 cal/cm² (the threshold for second-degree burns)
- Below 1.2 cal/cm²: No arc flash PPE required, but still require shock protection

**Incident energy result format:**
| Equipment | Voltage (V) | Working Dist (mm) | I_bolted (kA) | I_arc (kA) | Clearing Time (s) | Incident Energy (cal/cm²) | E_inc (J/cm²) |
|-----------|------------|-------------------|---------------|------------|-------------------|---------------------------|---------------|
| MDB-01 | 400 | 455 | 32.0 | 26.5 | 0.15 | — | — |
| DB-A | 400 | 455 | 12.0 | 9.8 | 0.25 | — | — |

### Step 5: Determine Arc Flash Boundary

**Calculate the arc flash boundary (AFB) — the distance at which incident energy equals 1.2 cal/cm²:**

**Arc flash boundary calculation (per IEEE 1584):**
```
AFB = 610 x (4.184 x C_f x E_n x (t / 0.2))^0.5
```

Where AFB is in millimeters and the result is the distance at which incident energy = 1.2 cal/cm² (5 J/cm²).

**Arc flash boundary result format:**
| Equipment | Incident Energy (cal/cm²) | AFB (mm) | AFB (meters) |
|-----------|--------------------------|---------|-------------|
| MDB-01 | — | — | — |
| DB-A | — | — | — |

**Interpretation:**
- Within the AFB: Arc flash hazard exists — appropriate PPE required
- Outside the AFB: Incident energy < 1.2 cal/cm² — no arc flash PPE required (shock protection still required)
- Restricted approach boundary and limited approach boundary per NFPA 70E Table 130.4(D)(a) must also be considered

### Step 6: Assign PPE Category

**Assign the appropriate PPE category for each equipment location:**

**PPE assignment table:**
| Incident Energy (cal/cm²) | PPE Category | Minimum Arc Rating (cal/cm²) | Required PPE Components |
|--------------------------|-------------|------------------------------|------------------------|
| < 1.2 | No arc flash PPE | N/A | Standard work clothing, shock protection only |
| 1.2 - 4 | Category 1 | 4 | Arc-rated shirt + pants or coverall, arc flash face shield or balaclava |
| > 4 - 8 | Category 2 | 8 | Arc-rated jacket + pants or coverall, arc flash face shield, balaclava |
| > 8 - 25 | Category 3 | 25 | Arc-rated suit (jacket + pants), balaclava, arc-rated gloves, arc flash hood or face shield |
| > 25 - 40 | Category 4 | 40 | Arc-rated suit (highest rating), arc-rated gloves and hood |
| > 40 | Prohibited zone | N/A | Do NOT work energized |

**PPE assignment checklist:**
- [ ] Incident energy calculated for each equipment location
- [ ] PPE category assigned per NFPA 70E incident energy tables
- [ ] PPE category rounded up to next standard level (e.g., 3.8 cal/cm² -> Category 2, not Category 1)
- [ ] Equipment with incident energy > 40 cal/cm² flagged for arc-resistant design or de-energized work requirement
- [ ] Shock protection boundaries also addressed (limited, restricted, prohibited approach distances)

### Step 7: Generate Arc Flash Labels

**Create arc flash warning labels for each equipment location:**

**Label content (per NFPA 70E and ANSI Z535):**
```
DANGER: ARC FLASH HAZARD
PPE CATEGORY: X  |  INCIDENT ENERGY: X.X cal/cm²
NOMINAL SYSTEM VOLTAGE: XXX V
ARC FLASH BOUNDARY: X.XX m

Appropriate PPE and work practices required.
Refer to NFPA 70E for details.
```

**Label format:**
| Field | Value |
|-------|-------|
| Equipment tag | — |
| PPE Category | — |
| Incident Energy (cal/cm²) | — |
| Arc Flash Boundary (m) | — |
| Working Distance (mm) | — |
| Limited Approach Boundary (m) per NFPA 70E | — |
| Restricted Approach Boundary (m) per NFPA 70E | — |
| Nominal System Voltage (V) | — |
| Date of Analysis | — |
| Study Reference | — |

### Step 8: Document Analysis

**Compile the complete arc flash analysis report:**

**Report structure:**
1. Executive summary with hazard level overview and key findings
2. System description and single-line diagram reference
3. Calculation methodology (IEEE 1584 2018 Edition, equations used)
4. Input data summary for each equipment location
5. Results summary table (incident energy, AFB, PPE category for all locations)
6. Arc flash warning labels for each equipment location
7. Sensitivity analysis (impact of clearing time, fault current variation)
8. Recommendations for incident energy reduction
9. Appendices: calculation spreadsheets, protective device TCCs, reference data

**Reducing incident energy recommendations:**
| Strategy | Effect |
|----------|--------|
| Reduce clearing time (faster protection) | Directly proportional reduction in incident energy |
| Zone-selective interlocking | Reduces clearing time for downstream faults |
| Maintenance switch / instantaneous override | Temporarily reduces clearing time during maintenance |
| Arc-resistant switchgear | Redirects arc energy away from worker |
| Lower bolted fault current (current-limiting devices) | Reduces arcing current and incident energy |
| Increase working distance | Reduces incident energy at the worker location |

## Success Criteria

- [ ] Incident energy calculated within IEEE 1584 model accuracy bounds (+/-25% typical)
- [ ] Arc flash boundary calculated for every equipment location analyzed
- [ ] PPE category assigned correctly per NFPA 70E incident energy tables
- [ ] All equipment with incident energy >= 1.2 cal/cm² has arc flash labels
- [ ] Equipment with incident energy > 40 cal/cm² flagged — no energized work permitted
- [ ] Clearing time based on actual arc (I_arc) clearing time from TCC, not bolted fault current
- [ ] Complete arc flash analysis report generated with all calculation data and results
- [ ] Label content verified against calculation results before printing/installation

## Common Pitfalls

1. **Incorrect Working Distances** — Using generic 455mm for all equipment is wrong. IEEE 1584 Table 1 specifies working distance by equipment type (e.g., 455mm for LV switchgear, 610mm for LV MCCs, 910mm for MV switchgear). Always use the correct working distance.
2. **Outdated Clearing Times** — Using assumed clearing times instead of actual protective device TCC clearing times at the arcing current severely underestimates incident energy. If the arcing current is below the instantaneous trip region, the device operates in the long-time region — clearing time could be seconds instead of cycles.
3. **Missing Fault Current Data** — Without accurate bolted fault current at each bus location, arcing current and incident energy calculations are unreliable. Run a short-circuit study first if data is not available.
4. **Using the Wrong IEEE 1584 Edition** — IEEE 1584-2002 and IEEE 1584-2018 have different equations and produce different results. Always use the 2018 Edition for new studies and clearly state which edition was used.
5. **Ignoring System Grounding** — Arcing current and incident energy differ between solidly grounded, resistance grounded, and ungrounded systems. Grounding type affects the calculation.
6. **Not Accounting for Maintenance Mode** — Some systems have a maintenance switch that temporarily reduces relay settings during maintenance. If present, calculate incident energy with both normal and maintenance settings and label accordingly.
7. **Incident Energy > 40 cal/cm²** — Standard off-the-shelf PPE is rated up to 40 cal/cm² maximum. If incident energy exceeds this, the only safe options are to de-energize the equipment, redesign the protection, or install arc-resistant switchgear.

## Cross-References

### Related Skills
- `electrical-protection-coordination` — Protection clearing times directly determine incident energy; reducing clearing time is the primary way to reduce incident energy
- `electrical-sld-processing` — SLD provides equipment topology and voltage levels for the analysis
- `electrical-cable-sizing` — Cable short-circuit withstand relates to fault current levels that affect incident energy
- `electrical-load-analysis` — Load data affects bolted fault current calculation

### Related Agents
- `EE-ARC-001` (deep-agents) — Primary arc flash analysis agent
- `EE-PROT-001` (deep-agents) — Protection clearing time data and TCC analysis
- `EE-SC-001` (deep-agents) — Short-circuit fault current data
- `EE-QA-001` (OpenClaw) — Quality validation of arc flash analysis results

### Standards & References
- IEEE 1584-2018 — IEEE Guide for Performing Arc-Flash Hazard Calculations
- NFPA 70E — Standard for Electrical Safety in the Workplace
- NFPA 70 (NEC) — National Electrical Code
- OSHA 29 CFR 1910.269 and 1910 Subpart S — Electrical safety regulations
- ANSI Z535 — Safety signs and tags
- IEC 61482 — Live working — Protective clothing against thermal hazards of electric arc
