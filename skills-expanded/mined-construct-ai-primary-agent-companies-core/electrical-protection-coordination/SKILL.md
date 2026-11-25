---
title: Electrical Protection Coordination
description: Perform relay/fuse coordination, time-current curve (TCC) analysis, and selective tripping verification for electrical protection systems
version: 1.0
frequency_percent: 70.0
success_rate_percent: 91.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/electrical-protection-coordination
gigabrain_tags: electrical-engineering, protection-coordination, TCC-analysis, relay-settings, selective-tripping, fault-protection, domainforge-ai
openstinger_context: protection-study, TCC-curves, selective-coordination
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/domain-knowledge/ELECTRICAL_GLOSSARY.MD
  - docs_construct_ai/disciplines/electrical-engineering/agent-data/ELECTRICAL_AGENTS-REGISTRY-SUMMARY.MD
related_skills:
  - electrical-sld-processing
  - electrical-cable-sizing
  - electrical-arc-flash-analysis
---

# Electrical Protection Coordination

## Overview

Perform protection coordination studies: build the power system model from SLD data, plot time-current curves (TCCs) for all protective devices, determine coordination margins, identify coordination gaps, recommend relay settings, verify selective tripping, and document the coordination study results. This ensures protection devices operate selectively to minimize outage scope while protecting equipment from damage.

**Announce at start:** "I'm using the electrical-protection-coordination skill to build the time-current curve model, analyze device coordination, and recommend protection settings."

## When to Use This Skill

**Trigger Conditions:**
- New protection system design requires device coordination verification
- Protection relay settings must be calculated for commissioning
- Existing system experiences nuisance tripping or coordination failures
- System modification (new source, new feeder) impacts protection coordination
- Arc flash study requires protection clearing time data
- Equipment damage from fault current requires root cause investigation

**Prerequisites:**
- Single-line diagram with all protective devices identified
- Fault current data at each bus/protective device location (from short-circuit study)
- Protection device library with TCC curves (utility relay curves, manufacturer TCC data)
- Equipment damage curves (transformer through-fault, cable thermal, bus short-circuit withstand)
- EE-PROT-001 agent or equivalent protection coordination capability available
- Coordination study software or TCC plotting capability

## Step-by-Step Procedure

### Step 1: Build Power System Model

**Construct the power system protection model from SLD data:**

**Model elements to map:**
- Protective devices: relays (ANSI/IEC functions), fuses, MCCBs, MCBs, ELCBs/RCDs
- Protected equipment: transformers, cables, motors, generators, busbars
- Fault current at each device location
- Device-to-device upstream/downstream relationships

**Model data required for each protective device:**
| Data Field | Description | Source |
|------------|-------------|--------|
| Device tag | Unique identifier | SLD |
| Device type | Relay, fuse, MCCB, MCB | SLD / Device schedule |
| Device manufacturer/model | Specific device for TCC curve | Equipment schedule |
| CT ratio | Current transformer ratio | CT schedule |
| Pick-up/setting current | Device trip setting (or range) | Relay setting sheet / Datasheet |
| Time dial / curve type | Time multiplier and curve shape | Relay setting sheet / Datasheet |
| Instantaneous pickup | Instantaneous trip setting if applicable | Relay setting sheet |
| Upstream device | Next device toward source | SLD topology |
| Downstream device(s) | Next device(s) toward load | SLD topology |
| Fault current at location | Bolted fault current at device | Short-circuit study |

**Model building checklist:**
- [ ] All protective devices from SLD included in model
- [ ] Device CT ratios documented
- [ ] Upstream/downstream relationships mapped for all device pairs
- [ ] Fault current at each device location confirmed
- [ ] Equipment damage curves identified for protected equipment
- [ ] Existing relay settings documented (for existing system studies)

### Step 2: Plot Time-Current Curves (TCC)

**Generate TCC plots for all protective devices in the coordination chain:**

**TCC curve components per device:**
- Operating time curve: device trip time as a function of fault current
- Instantaneous trip line: instantaneous trip threshold (vertical line)
- CT saturation curve: CT accuracy limit (if relevant)
- Equipment damage curve: protected equipment thermal/mechanical withstand

**Standard relay curve types (IEC 60255):**
| Curve Type | Equation | Application |
|-----------|----------|-------------|
| Standard Inverse (SI) | t = 0.14 x TMS / ((I/I_p)^0.02 - 1) | General feeder protection |
| Very Inverse (VI) | t = 13.5 x TMS / ((I/I_p) - 1) | Transformer protection |
| Extremely Inverse (EI) | t = 80 x TMS / ((I/I_p)^2 - 1) | Fuse coordination, motor protection |
| Long-Time Inverse (LI) | t = 120 x TMS / ((I/I_p) - 1) | Overload protection |
| Definite Time (DT) | t = TMS (fixed) | Stage backup protection |

**TCC plotting procedure:**
1. Start at the lowest device (most downstream) in the coordination chain
2. Plot the device TCC using manufacturer curve data or standard relay equation
3. Move upstream and plot the next device's TCC
4. Continue upstream until the source protection is plotted
5. Overlay equipment damage curves on the same TCC plot
6. Repeat for each coordination chain in the system

**TCC plot axes:**
- X-axis: Logarithmic current (A or multiples of CT primary)
- Y-axis: Logarithmic time (seconds, typically 0.001s to 10,000s)

### Step 3: Determine Coordination Margins

**Calculate the coordination margin between device pairs:**

**Coordination margin definition:**
Coordination margin is the time difference between the upstream device curve and the downstream device curve at the maximum available fault current through the downstream device.

**Minimum coordination margin:**
| Device Pair Combination | Minimum Margin |
|------------------------|---------------|
| Relay upstream / Relay downstream | 0.3-0.4 seconds |
| Relay upstream / Fuse downstream | 0.2-0.3 seconds |
| Fuse upstream / Fuse downstream | 0.2-0.3 seconds |
| Relay upstream / MCCB downstream | 0.3 seconds |

**Margin verification procedure:**
1. For each device pair (upstream U, downstream D):
   - Find the maximum fault current through D (before U would also see it)
   - Read the trip time of D at that current: t_D
   - Read the trip time of U at that current: t_U
   - Margin = t_U - t_D
2. Verify margin >= minimum required margin for that device pair
3. Document margins for all device pairs

**Margin visualization on TCC:**
On the TCC plot, the upstream device curve should be above and to the right of the downstream device curve with a clear gap (the coordination margin) across the full current range.

### Step 4: Identify Coordination Gaps

**Identify where coordination margins are insufficient:**

**Coordination gap types:**
| Gap Type | Description | Consequence |
|----------|-------------|-------------|
| Time gap too small | t_U - t_D < minimum margin | Both devices may trip simultaneously (no selectivity) |
| Curve crossing | Upstream curve crosses downstream curve | Loss of coordination for certain fault current ranges |
| Instantaneous overlap | Upstream instantaneous trips before downstream operates | Loss of coordination for high fault currents |
| Equipment damage violation | Device curve is to the right of equipment damage curve | Equipment damaged before protection operates |

**Gap identification procedure:**
1. Review each device pair on the TCC plot
2. Check that:
   - Upstream curve is always above downstream curve (no crossing)
   - Coordination margin is met at all current levels
   - Equipment damage curve is to the right of all protective device curves
   - CT saturation does not cause protection blind spots
3. Flag each gap found with its location, severity, and recommended action

**Gap severity classification:**
| Severity | Description | Action |
|----------|-------------|--------|
| Critical | No selectivity for faults; equipment damage before protection operates | MUST FIX before energization |
| Major | Selectivity lost for high-magnitude faults | FIX before commissioning |
| Minor | Selectivity marginal (within 10% of minimum) | Consider adjusting settings |

### Step 5: Recommend Relay Settings

**Calculate and recommend relay settings to achieve coordination:**

**Relay setting parameters to determine:**
| Parameter | Description | Guidance |
|-----------|-------------|----------|
| Pick-up current (I_p) | Minimum current to initiate trip | >= maximum load current, < minimum fault current |
| Time Multiplier Setting (TMS) | Time dial that scales the curve | Set to achieve coordination margin with downstream device |
| Instantaneous pickup (I_inst) | Current level for instantaneous trip | > maximum through-fault that downstream should clear, < minimum fault at device location |
| Curve type | SI, VI, EI, LI | Match to protected equipment and downstream device |
| Earth fault pickup | Earth fault sensitivity | >= maximum imbalance during normal operation |

**Setting calculation procedure:**
1. For each relay, starting from the most downstream:
   - Set pick-up current to 1.1-1.5 times maximum load current (or per equipment thermal limit)
   - Select curve type based on downstream device type (VI for transformer, EI for motor/fuse)
   - Calculate TMS to achieve required coordination margin with downstream device
   - Set instantaneous pickup above the maximum fault current the downstream relay should clear
2. Move upstream and repeat
3. Verify all recommended settings produce coordinated TCC curves
4. Cross-check equipment damage curves remain to the right of all relay curves

### Step 6: Verify Selective Coord

**Confirm selective tripping is achieved across the full fault current range:**

**Selectivity verification checks:**
| Check | Pass Condition |
|-------|----------------|
| Overload range | Only the device closest to the overload should trip |
| Low-magnitude fault range | Only downstream device trips, upstream provides backup |
| High-magnitude fault range | Down instantaneous or downstream relay clears; upstream does not operate first |
| Ground fault range | Earth fault protection coordinates with phase protection and upstream earth protection |
| Transformer through-fault | Relay curve within transformer damage curve (IEEE/IEC through-fault limit) |
| Motor starting | Device does not trip during motor starting current (inrush) |

**Verification procedure:**
1. For each device pair, verify coordination margin is met across the full current range
2. For each piece of equipment, verify the upstream protection operates within the equipment damage curve
3. For each motor, verify the protection does not trip during motor acceleration time
4. Review all gaps identified in Step 4 and confirm they have been resolved
5. Generate final TCC plots showing all devices in coordinated position

### Step 7: Document Coordination Study

**Compile the complete protection coordination study report:**

**Report structure:**
1. Executive summary with coordination status and critical findings
2. System description (SLD, voltage levels, sources, fault current data)
3. Device schedule with existing and recommended settings
4. TCC plots for each coordination chain
5. Coordination margin table for all device pairs
6. Equipment damage curve overlay results
7. Identified gaps and corrective actions taken
8. Relay setting recommendations with justifications
9. Special considerations (motor starting, transformer inrush, ground fault)

**Device schedule format:**
| Device | Type | CT Ratio | I_pickup (A) | Curve | TMS | I_inst (A) | Existing/Recommended | Notes |
|--------|------|----------|-------------|-------|-----|-----------|---------------------|-------|
| RLY-001 | Relay | 200:1 | 200 | VI | 0.15 | 2400 | Recommended | Feeder protection |
| FDR-002 | MCCB | 400:1 | 400 | N/A | N/A | 4000 | Existing | — |

## Success Criteria

- [ ] All protective devices in the SLD modeled and included in coordination study
- [ ] TCC plots generated for every coordination chain in the system
- [ ] Coordination margins documented for all device pairs (upstream vs. downstream)
- [ ] Coordination gaps identified with severity classification
- [ ] Critical gaps resolved before system energization (no gaps remaining)
- [ ] All relay/fuse settings recommended with specific values and curve types
- [ ] Selective tripping verified across the full fault current range
- [ ] Equipment damage curves satisfied (no equipment damage before protection clears)
- [ ] Complete coordination study report generated with TCC plots and device schedules
- [ ] Recommended settings validated against manufacturer TCC data

## Common Pitfalls

1. **Insufficient Coordination Margins** — Using 0.1s margin instead of the required 0.3-0.4s causes both devices to trip under fault. Always apply minimum margin per device combination.
2. **Incorrect Clearing Times** — Using assumed clearing times instead of the actual manufacturer TCC data produces inaccurate coordination. Always use the specific device model's TCC curve.
3. **Missing Backup Protection** — Relying solely on primary protection without backup means a device failure exposes equipment to uncontrolled faults. Verify backup protection operates if the primary fails.
4. **Ignoring Transformer Inrush** — Transformer energization can produce inrush currents of 8-12x rated for several cycles. Protection should not trip on inrush. Check that TCC curves do not intersect inrush region.
5. **Motor Starting Blind Spot** — DOL motor starting draws 6-8x FLC for seconds. If the protection curve intersects the motor acceleration time, nuisance tripping occurs. Verify coordination with motor starting current.
6. **CT Saturation Not Considered** — During high fault currents, CTs can saturate, causing the relay to see less current than actual. Check CT knee point voltage and verify accurate operation at maximum fault current.
7. **Not Reviewing After System Changes** — Adding a new source or feeder changes fault current distribution and can break existing coordination. Re-study coordination after any system modification.

## Cross-References

### Related Skills
- `electrical-sld-processing` — SLD provides system topology and device information for the model
- `electrical-cable-sizing` — Cable short-circuit withstand time affects protection clearing time requirement
- `electrical-arc-flash-analysis` — Protection clearing time directly determines incident energy at each location
- `electrical-load-analysis` — Load data determines overcurrent pickup and overload settings

### Related Agents
- `EE-PROT-001` (deep-agents) — Primary protection coordination agent with TCC analysis
- `EE-ARC-001` (deep-agents) — Arc flash analysis uses protection clearing times
- `EE-SC-001` (deep-agents) — Short-circuit fault current data for TCC plotting
- `EE-QA-001` (OpenClaw) — Quality validation of coordination study results

### Standards & References
- IEEE 242 (Buff Book) — IEEE Recommended Practice for Protection and Coordination of Industrial and Commercial Power Systems
- IEC 60255 — Measuring relays and protection equipment
- IEC 60947 — Low-voltage switchgear and controlgear
- ANSI/IEEE C37 — Power switchgear standards
- IEEE 1584 — Guide for Performing Arc-Flash Hazard Calculations

## Example Usage

**Scenario:** Protection coordination study for 11kV/400V industrial facility

1. **System Model:** Built from SLD: 11kV utility source (I_sc = 12kA), 11kV relay (R1) feeding 1600kVA transformer, 400V incomer MCCB (CB1) feeding LV bus, 6 outgoing MCCBs to feeders
2. **TCC Plots Generated:** 4 coordination chains plotted:
   - Chain 1: Utility relay -> R1 (11kV side of transformer) -> CB1 (400V incomer)
   - Chain 2: CB1 -> MCCB-001 (motor feeder 1, DOL 75kW)
   - Chain 3: CB1 -> MCCB-003 (distribution board feeder)
   - Chain 4: CB1 -> MCCB-006 (transformer cooling fan)
3. **Gaps Identified:**
   - CRITICAL: R1 and CB1 curves intersect at 8kA — no selectivity for high-current 400V faults
   - MAJOR: MCCB-001 instantaneous setting (800A) below motor starting current (560A x 6.5 = 3,640A)
4. **Setting Recommendations:**
   - R1: VI curve, I_p = 160A (CT 200:1), TMS = 0.30, I_inst = 1600A (CT primary)
   - CB1: I_p = 2,000A, TMS = N/A, I_inst = 8,000A (increased to coordinate with MCCB-001)
   - MCCB-001: I_p = 200A, LSIG with L=0.9x200A, S=5x200A (0.1s), I_inst disabled (rely on short-time delay)
   - MCCB-003: I_p = 400A, I_inst = 4,000A
5. **Post-Adjustment Verification:** All coordination gaps resolved. R1/CB1 margin = 0.45s at 400V fault level (32kA). MCCB-001 now clears before CB1 for feeder faults. Transformer through-fault curve satisfied.
6. **Report:** Complete coordination study with 4 TCC plots, device schedule, and recommended setting sheets issued for download to protection relays.

## Performance Metrics

**Target Performance:**
- Device coverage: 100% of protective devices from SLD included in coordination study
- TCC completeness: All coordination chains plotted with equipment damage curves overlaid
- Coordination margin: All device pairs meet or exceed minimum margin (0.3s relay/relay) after adjustment
- Gap resolution: Zero critical gaps, 0 major gaps remaining in final settings
- Equipment protection: All equipment damage curves satisfied (protection operates before damage)
- Report completeness: All required sections present, device schedule complete, TCC plots included
