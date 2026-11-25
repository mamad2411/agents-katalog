---
title: Electrical Load Analysis
description: Perform load estimation, diversity factor calculation, demand analysis, and feeder sizing for electrical distribution systems
version: 1.0
frequency_percent: 90.0
success_rate_percent: 94.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/electrical-load-analysis
gigabrain_tags: electrical-engineering, load-analysis, demand-calculation, diversity-factor, feeder-sizing, power-distribution, domainforge-ai
openstinger_context: load-estimation, demand-analysis, diversity-calculation
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_GLOSSARY.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/ELECTRICAL_AGENTS-REGISTRY-SUMMARY.MD
related_skills:
  - electrical-sld-processing
  - electrical-cable-sizing
  - electrical-protection-coordination
---

# Electrical Load Analysis

## Overview

Perform comprehensive electrical load estimation for distribution systems: collect equipment data, apply demand and diversity factors, calculate total connected load and maximum demand, size feeders, verify voltage drop, and document results. This ensures all electrical loads are properly accounted for, demand factors are correctly applied, and feeder capacities are adequate for the calculated demand.

**Announce at start:** "I'm using the electrical-load-analysis skill to perform load estimation, demand calculation, and feeder sizing verification for the electrical distribution system."

## When to Use This Skill

**Trigger Conditions:**
- New electrical distribution system design requires load calculation
- Existing system needs load assessment for expansion or modification
- Feeder capacity verification needed before adding new loads
- Transformer sizing requires maximum demand calculation
- Compliance documentation needs demand analysis for regulatory approval
- Energy audit or load profile study required

**Prerequisites:**
- Equipment schedule or load list available (motors, lighting, HVAC, outlets, etc.)
- Operating parameters for each load (kW/kVA, voltage, power factor, duty cycle, starting method)
- Applicable demand factors identified (NEC Article 220, IEC 60439, or local standard)
- EE-LOAD-001 agent or equivalent load analysis capability available
- Single-line diagram or load distribution topology available

## Step-by-Step Procedure

### Step 1: Collect Equipment Data

**Gather comprehensive equipment and load data:**

**Equipment data required for each load:**
| Data Field | Description | Source |
|------------|-------------|--------|
| Equipment tag | Unique identifier | Equipment schedule / SLD |
| Equipment type | Motor, lighting, HVAC, outlet, process load | Equipment schedule |
| Rated power (kW or HP) | Nameplate rated power | Equipment datasheet / nameplate |
| Voltage (V) | Operating voltage | Equipment datasheet |
| Power factor (PF) | Operating PF at full load | Datasheet or standard values |
| Efficiency (%) | Motor/load efficiency | Datasheet or standard values |
| Duty cycle | Continuous, intermittent, standby | Process requirements / operational data |
| Starting method | DOL, star-delta, VFD, soft starter | Motor control specification |
| Starting current multiplier | Inrush factor (typically 6-8x for DOL) | Datasheet or standard values |
| Phase | Single-phase or three-phase | Equipment datasheet |
| Location/Feeder | Which panel/MCC/switchboard supplies this load | SLD or distribution schedule |

**Data collection checklist:**
- [ ] All equipment listed on equipment schedule
- [ ] Rated power values confirmed from nameplate or datasheet
- [ ] Power factor and efficiency values documented
- [ ] Operating duty cycle identified for each load
- [ ] Standby/redundant equipment identified (exclude from demand)
- [ ] Future/expansion loads noted separately
- [ ] Load categorized by type (motor, lighting, HVAC, receptacle, process)

**Load categorization:**
```
1. Motor Loads (largest contributor, starting current critical)
2. Lighting Loads (continuous, power factor important)
3. HVAC Loads (compressor + fan, seasonal variation)
4. Receptacle/Outlet Loads (miscellaneous, high diversity)
5. Process/Equipment Loads (industrial, application-specific)
6. Emergency/Standby Loads (separate calculation path)
7. Future/Reserve Loads (not included in current demand)
```

### Step 2: Apply Demand Factors

**Apply demand factors to each load category per applicable standard:**

**NEC Article 220 demand factors (examples):**
| Load Category | Demand Factor | NEC Reference |
|---------------|--------------|---------------|
| General lighting - non-dwelling | 100% of first 125 kVA, then per Table 220.42 | 220.42, Table 220.42 |
| Receptacle loads - non-dwelling | First 10 kVA at 100%, remainder at 50% | 220.44 |
| Kitchen equipment - commercial | Table 220.56 based on quantity | 220.56 |
| Motor loads | 125% of largest motor + 100% of others | 430.24 |
| HVAC | Larger of heating vs. cooling load (not both) | 220.60 |
| Fire pump | 125% of rated current | 695.5 |
| Elevator loads | 100% of largest + demand per Table 620.14 | 620.14 |

**IEC 60439 / general demand factors (examples):**
| Load Category | Typical Demand Factor | Notes |
|---------------|----------------------|-------|
| Lighting (general) | 0.8-1.0 | Higher for commercial/industrial |
| Power outlets | 0.2-0.5 | Higher for fewer outlets |
| HVAC | 0.5-0.9 | Depends on simultaneity |
| Motors (group) | 0.7-1.0 | Depends on process interlocks |
| Process equipment | 0.7-1.0 | Application-specific |

**Demand factor application:**
```
Demand Load = Connected Load x Demand Factor
```

### Step 3: Calculate Diversity Factor

**Calculate diversity factor to account for non-simultaneous operation:**

**Diversity factor definition:**
```
Diversity Factor = Sum of Individual Maximum Demands / Maximum Demand of Group
```

**Typical diversity factors:**
| System Level | Typical Range | Notes |
|-------------|---------------|-------|
| Individual circuit | 1.0 | No diversity |
| Sub-distribution panel | 1.1-1.5 | Moderate diversity |
| Main distribution board | 1.3-2.0 | High diversity |
| Main incoming | 1.5-2.5 | Highest diversity (whole building) |

**Calculation procedure:**
1. Sum individual maximum demands (after demand factors applied) at each level
2. Apply diversity factor to get group maximum demand:
   ```
   Group Maximum Demand = Sum of Individual Demands / Diversity Factor
   ```
3. Aggregate from lowest level (circuit) to highest level (main incoming)
4. Document diversity factors used and justification

### Step 4: Calculate Total Connected Load

**Sum all connected loads by category:**

**Connected load calculation:**
| Category | Connected kW | Demand Factor | Demand kW | Diversity Factor | Max Demand kW |
|----------|-------------|---------------|-----------|-----------------|---------------|
| Motors | - | 1.0 (NEC 125% largest) | - | - | - |
| Lighting | - | 1.0 | - | - | - |
| HVAC | - | Select larger of heating/cooling | - | - | - |
| Receptacles | - | Per NEC 220.44 | - | - | - |
| Process loads | - | Per application | - | - | - |
| **TOTAL** | - | - | - | - | - |

**Three-phase current calculation:**
```
I_max (A) = Max Demand (W) / (sqrt(3) x V_line x PF x efficiency)
```

**Single-phase current calculation:**
```
I_max (A) = Max Demand (W) / (V_phase x PF x efficiency)
```

### Step 5: Determine Maximum Demand

**Calculate maximum demand for each distribution level:**

**Maximum demand determination:**
1. Start at circuit level - apply demand factor to each circuit
2. Group circuits by panel/MCC - sum circuit demands, apply panel diversity
3. Group panels by sub-distribution - sum panel demands, apply sub-distribution diversity
4. Group sub-distributions by main board - sum board demands, apply board diversity
5. Calculate main incoming maximum demand - sum all, apply overall diversity

**Maximum demand result format:**
| Distribution Level | Connected (kVA) | After Demand Factor | After Diversity | Max Demand (kVA) | Max Current (A) |
|-------------------|-----------------|---------------------|-----------------|------------------|-----------------|
| Circuit group 1 | - | - | - | - | - |
| Panel A total | - | - | - | - | - |
| Sub-distribution DB-1 | - | - | - | - | - |
| Main board MDB | - | - | - | - | - |
| Main incoming | - | - | - | - | - |

### Step 6: Size Feeders

**Determine feeder sizes based on maximum demand:**

**Feeder sizing procedure:**
1. Take maximum demand current at each distribution level
2. Select cable based on ampacity >= design current (use electrical-cable-sizing skill for detailed calculation)
3. Check voltage drop across feeder length
4. Verify short-circuit withstand capacity
5. Verify protective device coordination with feeder rating

**Feeder sizing summary:**
| Feeder | From -> To | Design Current (A) | Select Cable | Voltage Drop (%) | Protective Device |
|--------|-----------|--------------------|-----------|-----------------|----------|
| FDR-001 | MDB -> DB-1 | - | - | - | - |
| FDR-002 | MDB -> DB-2 | - | - | - | - |
| FDR-003 | DB-1 -> Panel A | - | - | - | - |

### Step 7: Verify Voltage Drop

**Verify voltage drop is within acceptable limits:**

**Voltage drop calculation (three-phase simplified):**
```
VD (%) = (sqrt(3) x I x L x (R*cos(phi) + X*sin(phi))) / (V_line x 10)
```
Where:
- I = design current (A)
- L = cable length (m)
- R = cable resistance (Ohm/km)
- X = cable reactance (Ohm/km)
- cos(phi) = power factor

**Acceptable voltage drop limits:**
| Circuit Type | Maximum VD | Standard Reference |
|-------------|------------|-------------------|
| Main feeder | 3% | NEC 210.19 / IEC 60364-5-52 |
| Branch circuit | 3% | NEC 210.19 / IEC 60364-5-52 |
| Total (incoming to load) | 5% | NEC 210.19 / IEC 60364-5-52 |

**If voltage drop exceeds limits:**
- Increase cable size and recalculate
- Consider route optimization (shorter path)
- Consider reactive power compensation (power factor correction)

### Step 8: Document Results

**Compile complete load analysis report:**

**Report structure:**
1. Executive summary with total connected load and maximum demand
2. Equipment schedule with all data fields
3. Demand factor table with standard references
4. Diversity factor calculation with justification
5. Load summary by category and distribution level
6. Feeder sizing results
7. Voltage drop verification
8. Recommendations (power factor correction, load balancing, future expansion)

## Success Criteria

- [ ] All loads accounted for in equipment schedule (verified against SLD)
- [ ] Demand factors applied correctly per applicable standard (NEC Article 220, IEC 60439, or local)
- [ ] Diversity factors documented with justification for each level
- [ ] Maximum demand calculated at each distribution level
- [ ] Demand <= feeder capacity verified for all feeders
- [ ] Voltage drop within limits (<=3% branch, <=5% total) for all critical circuits
- [ ] Standby/redundant equipment excluded from demand calculation
- [ ] Future load provision noted separately
- [ ] Complete load analysis report generated with all calculations

## Common Pitfalls

1. **Missing Equipment** - Incomplete equipment schedules lead to undersized feeders. Always cross-reference SLD, equipment schedule, and architectural load requirements.
2. **Incorrect Demand Factors** - Applying the wrong demand factor (e.g., using residential factors for industrial) gives wrong results. Always verify the applicable standard and load category.
3. **Diversity Not Considered** - Simply summing all loads without diversity produces oversized feeders (wasteful) or masks real peak demand. Apply diversity at each distribution level with documented justification.
4. **Ignoring Motor Starting Current** - DOL motors draw 6-8x rated current on starting. Check that protective devices do not trip during motor starting and voltage dip is acceptable.
5. **Double-Counting HVAC** - NEC requires taking the larger of heating vs. cooling, not both. Including both adds phantom load.
6. **Not Verifying Existing Capacity** - When expanding an existing system, verify the spare capacity in the existing main incomer and busbars before designing new feeders.

## Cross-References

### Related Skills
- `electrical-sld-processing` - SLD extraction provides load topology for analysis
- `electrical-cable-sizing` - Feeder sizing results feed detailed cable calculation
- `electrical-protection-coordination` - Maximum demand determines protective device rating
- `electrical-arc-flash-analysis` - Load data contributes to fault current calculation

### Related Agents
- `EE-LOAD-001` (OpenClaw) - Primary load analysis agent
- `EE-CABLE-001` (OpenClaw) - Feeder sizing input/output
- `EE-LIB-001` (OpenClaw) - Demand factor reference library

### Standards & References
- NEC Article 220 - Branch-Circuit, Feeder, and Service Calculations
- IEC 60439 - Low-voltage switchgear and controlgear assemblies
- IEC 60364-5-52 - Electrical installations of buildings - Selection and erection of wiring systems
- IEEE 141 (Red Book) - IEEE Recommended Practice for Electric Power Distribution for Industrial Plants

## Example Usage

**Scenario:** Load analysis for a commercial building main distribution board

1. **Equipment Data Collected:** 45 loads across 6 panels: 12 motor loads (3.7-75kW), 8 lighting circuits (4-12kW each), 10 HVAC units (5-35kW), 10 receptacle circuits (2-8kW each), 5 process loads (10-50kW)
2. **Demand Factors Applied:** Motors at 125% largest + 100% others (NEC 430.24), lighting at 100% (general), receptacles at 100% first 10kVA + 50% remainder (NEC 220.44), HVAC at larger of heating/cooling (NEC 220.60)
3. **Diversity Factors:** Circuit level = 1.0, panel level = 1.3, MDB level = 1.5
4. **Results:** Total connected load = 847kW, maximum demand at MDB = 612kW (diversity applied), design current at 400V 3-phase PF 0.85 = 1,038A
5. **Feeder Sizing:** Main incomer sized at 1,200A MCCB (next standard size above 1,038A), verified against transformer 1,600kVA capacity
6. **Voltage Drop:** Main feeder (50m, 2x240mm2 per phase) = 1.8% - within 3% limit
7. **Report:** Complete load analysis report generated with all calculations and equipment schedules

## Performance Metrics

**Target Performance:**
- Load completeness: 100% of loads from equipment schedule accounted for
- Demand factor accuracy: All demand factors traceable to specific code clauses
- Demand calculation: Maximum demand within +-5% of measured peak (for validated existing systems)
- Voltage drop: All circuits <=5% total (incoming to load)
- Processing time: Typical commercial building (<100 loads) analyzed within 15 minutes
