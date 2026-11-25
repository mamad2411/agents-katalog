---
title: Electrical Cable Sizing
description: Perform IEC 60364/NEC cable sizing with derating factors, voltage drop verification, and short-circuit withstand capacity for electrical distribution systems
version: 1.0
frequency_percent: 85.0
success_rate_percent: 93.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/electrical-cable-sizing
gigabrain_tags: electrical-engineering, cable-sizing, derating, voltage-drop, short-circuit, IEC-60364, NEC, domainforge-ai
openstinger_context: cable-sizing, ampacity-calculation, derating-factors
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_GLOSSARY.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/ELECTRICAL_AGENTS-REGISTRY-SUMMARY.MD
related_skills:
  - electrical-load-analysis
  - electrical-protection-coordination
  - electrical-sld-processing
---

# Electrical Cable Sizing

## Overview

Perform cable sizing calculations per IEC 60364-5-52 or NEC Article 310: determine design current, select cable type, apply derating factors (ambient temperature, grouping, burial depth), verify ampacity meets design current, calculate voltage drop, verify short-circuit withstand, and document the final cable specification. This ensures cables are correctly sized for safe, efficient, and code-compliant operation.

**Announce at start:** "I'm using the electrical-cable-sizing skill to calculate cable sizes with derating, voltage drop, and short-circuit verification."

## When to Use This Skill

**Trigger Conditions:**
- New electrical circuit design requires cable size selection
- Existing cables need verification for increased load
- Cable route conditions change (temperature, grouping, burial)
- Voltage drop complaints require cable upgrade assessment
- Short-circuit withstand verification needed for new protection settings
- Compliance documentation requires cable sizing calculations

**Prerequisites:**
- Load data available (design current in amps, voltage, power factor)
- Cable route information (length, routing method, installation conditions)
- Installation method identified (air, buried, conduit, tray, ladder, duct)
- Ambient conditions known (ambient temperature, soil thermal resistivity for buried)
- Grouping information (number of circuits installed together, spacing)
- EE-CABLE-001 agent or equivalent cable sizing capability available
- Short-circuit current at cable location available

## Step-by-Step Procedure

### Step 1: Determine Design Current

**Calculate the design current for the circuit:**

**Three-phase motor loads:**
```
I_design (A) = P_rated (W) / (sqrt(3) x V_line x PF x efficiency)
```

**Three-phase general loads:**
```
I_design (A) = P_demand (W) / (sqrt(3) x V_line x PF)
```

**Single-phase loads:**
```
I_design (A) = P_demand (W) / (V_phase x PF)
```

**Design current checklist:**
- [ ] Rated/demand power confirmed in watts
- [ ] Operating voltage confirmed (line-line or phase)
- [ ] Power factor documented
- [ ] Motor efficiency included where applicable
- [ ] Design current for continuous load includes 125% factor (NEC) or per IEC installation method

**Continuous vs. non-continuous loads:**
| Load Type | Factor | Notes |
|-----------|--------|-------|
| Continuous (>3 hours) | 1.25x (NEC 210.20) | Required safety margin |
| Non-continuous | 1.0x | No additional factor |
| Motor circuits | Per NEC 430.22 / IEC 60364 | 125% FLC for motor |

### Step 2: Select Cable Type

**Choose cable construction based on application:**

**Cable type selection guide:**
| Application | Recommended Cable Type | Standard |
|-------------|----------------------|----------|
| Indoor fixed wiring (dry) | PVC/PVC, XLPE/PVC | IEC 60502-1 |
| Indoor fixed wiring (fire-rated) | MICC, FP200 | BS 7629 |
| Underground direct burial | XLPE/PVC/SWA/PVC, XLPE/PE | IEC 60502-1 |
| Cable tray/ladder | XLPE/PVC, EPR/PVC (unarmored) | IEC 60502-1 |
| Conduit/duct | PVC/PVC, XLPE/PVC | IEC 60502-1 |
| Hazardous area | Armored, screened per zone | IEC 60079-14 |
| Marine/offshore | XLPE/LSF/SWA/LSF | IEC 60092-350 |

**Cable construction components to specify:**
- Conductor material: Copper (standard) or Aluminium (large feeders)
- Conductor class: Class 2 (stranded) for fixed, Class 5/6 (flexible) for connections
- Insulation: PVC (standard), XLPE (higher temperature, better current rating), EPR (flexible)
- Armor: SWA (steel wire), AWA (aluminum wire), STA (steel tape), or unarmored
- Sheath: PVC (standard), LSF (low smoke), PE (buried), LSZH (public areas)

**Standard conductor sizes:**
1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630 mm²

### Step 3: Apply Derating Factors

**Determine the cable rating under actual installation conditions:**

**Derating factor categories:**

**Ambient Temperature (Ca):**
For XLPE insulated cables (90 deg C rated):
| Ambient Temp (deg C) | In Air | Buried (soil) |
|---------------------|--------|---------------|
| 25 | 1.00 | 1.00 |
| 30 | 0.96 | 0.93 |
| 35 | 0.91 | 0.87 |
| 40 | 0.87 | 0.79 |
| 45 | 0.82 | 0.71 |
| 50 | 0.76 | 0.61 |

**Grouping Factor (Cg):**
For circuits installed together in air (touching):
| Number of Circuits | 1 | 2 | 3 | 4 | 6 | 8 | 10 | 12 | 16 |
|--------------------|---|---|---|---|---|---|----|----|----|
| Grouping Factor | 1.00 | 0.80 | 0.70 | 0.65 | 0.57 | 0.52 | 0.50 | 0.48 | 0.44 |

**Thermal Insulation Factor (Ci):**
| Condition | Factor |
|-----------|--------|
| Cable in thermal insulation (fully enclosed) | 0.50 |
| Cable in thermal insulation (partial contact) | 0.89 |
| Cable in conduit in thermally insulated wall | 0.78 |

**Soil Thermal Resistivity (CC) for buried cables:**
| Soil Type | Resistivity (K.m/W) | Factor |
|-----------|--------------------|--------|
| Wet soil | 0.5-1.0 | 1.00 |
| Damp soil | 1.0-2.0 | 0.91 |
| Dry soil | 2.0-3.0 | 0.84 |

**Combined derating:**
```
I_rating_adjusted = I_tabulated x Ca x Cg x Ci x CC x other
```

**Where:**
- I_tabulated = base current rating from manufacturer or standard tables
- All applicable derating factors are multiplied together

### Step 4: Verify Ampacity

**Check that adjusted cable ampacity meets design current:**

**Ampacity verification:**
```
I_rating_adjusted >= I_design
```

**Selection procedure:**
1. Start with a trial cable size
2. Look up base ampacity from standard table for the installation method
3. Apply all derating factors to get adjusted ampacity
4. Compare adjusted ampacity to design current
5. If adjusted ampacity < design current, move to next larger size and repeat
6. Select the smallest cable size where adjusted ampacity >= design current

**Ampacity verification checklist:**
- [ ] Base ampacity from correct table for installation method
- [ ] All applicable derating factors applied and documented
- [ ] Adjusted ampacity >= design current (I_rating_adjusted >= I_design)
- [ ] Next smaller cable size does NOT satisfy the requirement (confirm minimum size)
- [ ] Neutral conductor sized appropriately (full size for harmonics, or per calculation)
- [ ] Earth/ground conductor sized per fault current and duration (IEC 60364-5-54)

### Step 5: Calculate Voltage Drop

**Verify voltage drop across the cable run is within limits:**

**Three-phase voltage drop:**
```
VD (V) = sqrt(3) x I_design x L x (R x cos(phi) + X x sin(phi)) / 1000
```

**Single-phase voltage drop:**
```
VD (V) = 2 x I_design x L x (R x cos(phi) + X x sin(phi)) / 1000
```

**Voltage drop (%):**
```
VD (%) = VD (V) / V_nominal x 100
```

**Where:**
- I_design = design current (A)
- L = cable length (m)
- R = cable resistance at operating temperature (Ohm/km)
- X = cable reactance (Ohm/km)
- cos(phi) = power factor
- sin(phi) = sqrt(1 - cos(phi)^2)

**Acceptable voltage drop limits:**
| Circuit Type | Maximum VD | Standard Reference |
|-------------|------------|-------------------|
| LV main feeder from supply | 3% | IEC 60364-5-52 / NEC 210.19 |
| LV branch circuits | 3% | IEC 60364-5-52 / NEC 210.19 |
| Total installed (incoming to load) | 5% | IEC 60364-5-52 / NEC 210.19 |
| Motor starting | 10-15% (momentary) | IEC 60034 |

**If voltage drop exceeds limits:**
- Select next larger cable size and recalculate
- Reduce cable length if possible (reroute)
- Install additional cable in parallel (large feeders)

### Step 6: Verify Short-Circuit Withstand

**Verify the cable can withstand the short-circuit current without thermal damage:**

**Adiabatic equation (IEC 60364-5-54 / IEC 60949):**
```
S_min = sqrt(I_sc^2 x t) / k
```

**Where:**
- S_min = minimum conductor cross-section (mm²)
- I_sc = short-circuit current (A) at cable location
- t = fault clearing time (seconds)
- k = material factor (copper XLPE/PVC: k = 143, copper PVC: k = 115)

**Short-circuit check:**
- Calculate S_min for the available short-circuit current and protective device clearing time
- Verify selected cable cross-section >= S_min
- If cable size is insufficient:
  - Increase cable size, OR
  - Reduce fault clearing time (faster protection), OR
  - Install current-limiting device

**Short-circuit verification checklist:**
- [ ] Short-circuit current at cable location documented
- [ ] Protective device clearing time for the fault current identified
- [ ] Material factor k selected for cable construction
- [ ] S_min calculated per adiabatic equation
- [ ] Selected cable cross-section >= S_min

### Step 7: Document Cable Specification

**Produce complete cable specification documentation:**

**Cable specification format:**
| Field | Value |
|-------|-------|
| Cable tag | — |
| From → To | — |
| Circuit reference | — |
| Design current (A) | — |
| Cable type | — |
| Conductor material/size | — |
| Number of cores | — |
| Insulation/Armor/Sheath | — |
| Installation method | — |
| Route length (m) | — |
| Ambient temperature (deg C) | — |
| Grouping factor | — |
| All derating factors applied | — |
| Base ampacity (A) | — |
| Adjusted ampacity (A) | — |
| Ampacity check | PASS/FAIL |
| Voltage drop (V, %) | — |
| Voltage drop check | PASS/FAIL |
| Short-circuit current (kA) | — |
| Protective device / clearing time | — |
| S_min (mm²) | — |
| SC withstand check | PASS/FAIL |
| Standard reference | IEC 60364-5-52 / NEC Article 310 |

### Step 8: QA Review

**Perform quality review of cable sizing results:**

**QA checklist:**
- [ ] All derating factors correctly identified and applied
- [ ] Cable size is the minimum that satisfies all criteria (not oversized)
- [ ] Voltage drop within limits for the entire circuit
- [ ] Short-circuit withstand verified with actual protective device clearing time
- [ ] Earth conductor sized per fault thermal requirements
- [ ] Standard references documented for all calculations
- [ ] Results reviewed by second check (EE-QA-001 or peer)

## Success Criteria

- [ ] Cable sized correctly per applicable standard (IEC 60364-5-52 or NEC Article 310)
- [ ] All applicable derating factors applied (ambient, grouping, burial, insulation)
- [ ] Adjusted ampacity >= design current (cable will not overheat under sustained load)
- [ ] Voltage drop within limits (<=3% branch, <=5% total from supply to load)
- [ ] Short-circuit withstand verified (S_min <= selected cross-section)
- [ ] Earth/ground conductor correctly sized for fault thermal duty
- [ ] Cable specification complete with all calculation data and standard references
- [ ] QA review completed with zero critical findings

## Common Pitfalls

1. **Incorrect Derating** — Applying wrong ambient temperature factor, missing grouping factor, or double-counting factors produces unsafe cable sizing. Always use the factor for the actual installation condition.
2. **Missing Grouping Factors** — Cables installed close together must be derated for mutual heating. A circuit alone in a tray has no grouping, but 4 circuits in a conduit have significant derating. Always count adjacent loaded circuits.
3. **Insufficient Short-Circuit Rating** — A cable may handle the load current but fail catastrophically if its cross-section is below S_min for the available fault current. Always verify SC withstand with the actual protective device clearing time.
4. **Using Room Temperature Tables for Hot Environments** — Standard ampacity tables assume 30 deg C ambient. In 45-50 deg C environments (near equipment, tropical), derating can reduce capacity to 60-70% of tabulated value.
5. **Ignoring Harmonics** — Non-linear loads (VFDs, IT equipment) produce neutral current that can exceed phase current. In these cases, neutral must be sized equal to or larger than phase conductors.
6. **Wrong Installation Method Table** — Cable installed in conduit underground has different ampacity than the same cable in free air. Always use the table that matches the actual installation method.

## Cross-References

### Related Skills
- `electrical-load-analysis` — Design current and demand data feed cable sizing
- `electrical-protection-coordination` — Protective device clearing time required for SC withstand
- `electrical-sld-processing` — SLD provides circuit topology and cable routing information
- `electrical-arc-flash-analysis` — Cable SC rating relates to incident energy calculation

### Related Agents
- `EE-CABLE-001` (OpenClaw) — Primary cable sizing agent
- `EE-LOAD-001` (OpenClaw) — Load analysis input/output
- `EE-SC-001` (deep-agents) — Short-circuit current data
- `EE-QA-001` (OpenClaw) — Quality validation of cable sizing results

### Standards & References
- IEC 60364-5-52 — Electrical installations of buildings — Selection and erection of wiring systems
- IEC 60364-5-54 — Selection and erection of earthing arrangements
- IEC 60949 — Calculation of thermally permissible short-circuit currents
- NEC Article 310 — Conductors for General Wiring
- NEC Article 250 — Grounding and Bonding
- BS 7671 (IEE Wiring Regulations) — Requirements for Electrical Installations

## Example Usage

**Scenario:** Size cable for a 75kW motor feeder, 400V 3-phase, DOL start, 45m run in cable tray with 3 other circuits, ambient 40 deg C

1. **Design Current:** 75kW / (sqrt(3) x 400V x 0.88 PF x 0.94 eff) = 130.2A. Continuous duty per NEC requires 125%: I_design = 162.8A
2. **Cable Type Selected:** XLPE/PVC/SWA/PVC, 4-core, copper, Class 2 stranded (industrial motor feeder)
3. **Derating Factors:** Ca (40 deg C, XLPE) = 0.87, Cg (4 circuits in air, trefoil) = 0.65, Ci (none) = 1.00. Combined derating = 0.87 x 0.65 = 0.566
4. **Ampacity Verification:** Trial 70mm²: base ampacity (free air, XLPE) = 248A. Adjusted = 248 x 0.566 = 140.4A < 162.8A. FAIL. Trial 95mm²: base = 298A. Adjusted = 298 x 0.566 = 168.7A >= 162.8A. PASS.
5. **Voltage Drop:** 95mm² Cu: R = 0.242 Ohm/km (at 90 deg C), X = 0.080 Ohm/km. VD = sqrt(3) x 130.2 x 45 x (0.242 x 0.88 + 0.080 x 0.47) / 1000 = 3.5V = 0.88%. Well within 3% limit.
6. **Short-Circuit:** Available I_sc = 15kA, MCCB clearing time = 0.2s, k = 143 (Cu XLPE). S_min = sqrt(15000^2 x 0.2) / 143 = 46.8mm². 95mm² >> 46.8mm². PASS.
7. **Final Cable Spec:** 95mm² 4C Cu XLPE/SWA/PVC, I_design = 162.8A, I_rating_adj = 168.7A, VD = 0.88%, SC withstand OK, earth 35mm² per Table 54.7.

## Performance Metrics

**Target Performance:**
- Ampacity check: 100% of cables pass I_rating_adjusted >= I_design
- Voltage drop: 100% of circuits within 5% total, 3% branch
- Short-circuit withstand: 100% of cables have S_min <= selected cross-section
- Standard compliance: All calculations reference specific IEC/NEC clauses
- QA review: Zero critical findings in final cable specification
- Processing time: Individual circuit sizing completed within 5 minutes
