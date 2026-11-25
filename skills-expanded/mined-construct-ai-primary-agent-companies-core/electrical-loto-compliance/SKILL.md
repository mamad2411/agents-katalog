---
title: Electrical LOTO Compliance
description: Generate lockout-tagout procedures for electrical equipment with energy source mapping, isolation point identification, and audit-compliant verification
version: 1.0
frequency_percent: 80.0
success_rate_percent: 96.0
gigabrain_tags: domainforge_ai, electrical-engineering, LOTO, lockout-tagout, NFPA-70E, OSHA, compliance, safety
openstinger_context: electrical-loto, energy-isolation
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00860_electrical-engineering/agent-data/domain-knowledge/00860_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/skills/domainforge_ai/electrical-commissioning/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/electrical-document-generation/SKILL.md
related_skills:
  - electrical-commissioning
  - electrical-document-generation
---

# Electrical LOTO Compliance

## Overview
An AI-native lockout-tagout (LOTO) skill that generates machine-specific procedures for electrical equipment, maps all energy sources (electrical, pneumatic, hydraulic, stored), and creates audit-compliant isolation documentation following NFPA 70E, OSHA 1910.147, and IEC 60364 requirements.

## When to Use This Skill
- Creating new LOTO procedures for electrical equipment
- Updating existing LOTO procedures after system modifications
- Verifying isolation point identification for new installations
- Compliance audits of existing LOTO program
- Pre-commissioning LOTO verification
- Equipment handover documentation

## Prerequisites
- Equipment inventory with IDs, locations, and descriptions
- Electrical single-line diagrams and wiring diagrams
- Energy types inventory (electrical, pneumatic, hydraulic, mechanical, thermal, chemical)
- Isolation point details (switches, breakers, valves, blinds)
- Authorized employee list for the facility

## Step-by-Step Execution

### Step 1: Identify Equipment to Isolate
- Extract equipment details from inventory (equipment ID, name, location)
- Document equipment function and criticality
- Identify whether single or group LOTO required

### Step 2: Identify All Energy Sources
- **Electrical**: Primary feeds, backup feeds, control power, UPS supplies, capacitor banks
- **Pneumatic**: Compressed air lines, stored pressure in vessels
- **Hydraulic**: Hydraulic supply lines, accumulator pressure
- **Mechanical**: Elevated loads, springs, rotating masses
- **Thermal**: Heated components, steam, residual heat
- **Chemical**: Process chemicals, reactive materials

### Step 3: Map Isolation Points
- Electrical: Circuit breakers, disconnect switches, contactors, fuses
- Pneumatic/Hydraulic: Isolation valves, blinds, bleed points
- Mechanical: Lockout pins, mechanical blocks
- Document each isolation point with location and device type
- Verify isolation points are clearly labeled and accessible

### Step 4: Identify Stored Energy Hazards
- Capacitors requiring discharge
- Accumulators requiring bleed
- Elevated loads requiring blocking
- Springs requiring restraint
- Thermal energy requiring cooldown period
- Verify all stored energy can be safely released

### Step 5: Document Lock Positions
- For each isolation point: lock type, tag type, lock position (open/closed)
- Document who applies locks (authorized employee identification)
- Document verification method after isolation
- Include group LOTO procedures if multiple personnel involved

### Step 6: Generate LOTO Procedure
- Create step-by-step procedure in approved format:
  1. Equipment to be isolated
  2. Notify affected personnel
  3. Shutdown equipment normally
  4. Isolate all energy sources (list each)
  5. Apply locks and tags (list each isolation point)
  6. Release or block stored energy
  7. Verify isolation (zero-energy verification test)
  8. Document verification results
- Include diagrams showing isolation point locations
- Add verification checklist

### Step 7: Verify Isolation Point Identification
- Conduct walk-down verification of mapped isolation points
- Verify each isolation point correctly identified on drawings
- Confirm isolation point accessibility during work
- Verify labeling matches procedure
- Document any discrepancies and update procedure

### Step 8: Assign Authorized Employee
- Link procedure to authorized employee roster
- Ensure adequate trained personnel available
- Document training status and authorization date
- Include substitute authorization procedures

### Step 9: Generate LOTO Procedure
- Produce procedure in required format (print card, digital format)
- Include laminated quick-reference card for field use
- Store digital copy in document management system
- Distribute to relevant departments

## Success Criteria
- 100% energy sources identified for each piece of equipment
- All isolation points correctly mapped and verified
- Procedure reviewed and signed by authorized person
- All stored energy addressed with safe release methods
- Audit trail maintained with version control
- LOTO procedure accessible at point of use

## Common Pitfalls
- **Missing Stored Energy**: Capacitors, accumulators, spring loads not identified → unexpected energization risk
- **Multiple Supply Points**: Equipment fed from multiple sources (primary + backup, UPS) → incomplete isolation
- **Backfeed Paths**: Control circuits, PTs, interconnections backfeed equipment → unexpected energization
- **Group LOTO Complexity**: Multiple personnel without proper group lockout → unclear accountability
- **Unlabeled Isolation Points**: Isolation points not clearly labeled in field → confusion during execution

## Cross-References
- NFPA 70E: Electrical Safety in the Workplace
- OSHA 1910.147: Control of Hazardous Energy
- IEC 60364-4-46: Isolation and switching
- 00860 Domain Knowledge: LOTO procedures implementation (Part 11)
- Electrical Commissioning: Pre-energization safety verification
- Electrical Document Generation: LOTO document templates

## Usage Example
```
Scenario: Generate LOTO procedure for 415V motor MCC-3
Step 1: Equipment MCC-3, Motor 3.1, location: Plant Room A
Step 2: Energy sources: 415V 3-phase main supply, 24V DC control power, spring-loaded brake
Step 3: Isolation points: CB-3.1 (415V breaker), CB-24V (24V control), mechanical brake pin
Step 4: Stored energy: Capacitor in VSD (requires 5 min discharge), spring brake (requires blocking pin)
Step 5-8: Generate procedure with diagrams, assign authorized electricians, create field card
Step 9: Distribute to maintenance team, store in LOTO register
```

## Metrics
- Coverage: 100% of registered equipment has LOTO procedures
- Accuracy: 100% of energy sources identified and isolated correctly
- Compliance: All procedures meet NFPA 70E/OSHA 1910.147 requirements
- Audit: Zero findings on LOTO program audits