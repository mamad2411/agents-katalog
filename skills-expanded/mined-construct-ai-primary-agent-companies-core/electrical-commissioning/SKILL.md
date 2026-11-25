---
title: Electrical Commissioning
description: Generate commissioning test sequences, pre-energization checklists, and functional test protocols for all electrical systems with safety verification
version: 1.0
frequency_percent: 70.0
success_rate_percent: 95.0
gigabrain_tags: domainforge_ai, electrical-engineering, commissioning, testing, pre-energization, functional-testing, safety
openstinger_context: electrical-commissioning, system-handover
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00860_electrical-engineering/agent-data/domain-knowledge/00860_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/skills/domainforge_ai/electrical-loto-compliance/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/electrical-protection-coordination/SKILL.md
related_skills:
  - electrical-loto-compliance
  - electrical-protection-coordination
  - electrical-arc-flash-analysis
---

# Electrical Commissioning

## Overview
An AI-native commissioning skill that generates comprehensive test sequences and procedures for all electrical systems, including pre-energization safety checklists, functional test protocols, and commissioning documentation for handover.

## When to Use This Skill
- Developing commissioning plans for new electrical installations
- Creating pre-energization checklists before energizing equipment
- Generating functional test protocols for protection systems
- Commissioning reports and handover documentation
- Integration testing of power systems (ATS, generators, UPS)

## Prerequisites
- Approved commissioning plan and test procedures
- Test equipment with valid calibration certificates
- Approved LOTO procedures for affected equipment
- Single-line diagrams and wiring diagrams (as-built or latest revision)
- Safety clearances and work permits approved

## Step-by-Step Execution

### Step 1: Verify Installation Complete
- Check all equipment installed per drawings
- Verify cable terminations complete
- Confirm equipment labeling matches drawings
- Document any installation deficiencies

### Step 2: Review Test Equipment Calibration
- Verify all test instruments have valid calibration
- Check test leads and accessories in good condition
- Confirm test equipment suitable for voltage class (CAT III, CAT IV)
- Document test equipment used for each test

### Step 3: Execute Pre-Energization Checklist
- Confirm all work permits closed
- Verify all personnel clear of energized parts
- Check temporary earths/grounds removed
- Verify LOTO procedures in place for adjacent equipment
- Confirm fire protection systems operational
- Verify adequate lighting and ventilation
- Check PPE requirements communicated

### Step 4: Perform Insulation Resistance Testing
- Test phase-to-phase and phase-to-earth insulation
- Record insulation resistance values (MΩ)
- Compare with minimum acceptable values per standard
- Document results and identify any failures

### Step 5: Perform Continuity Testing
- Verify protective conductor continuity
- Check circuit continuity for all cables
- Record loop impedance values
- Verify earth fault loop impedance within limits

### Step 6: Verify Protection Relay Settings
- Confirm relay settings match approved coordination study
- Verify current transformer ratios correct
- Check voltage transformer ratios correct
- Test relay trip function without tripping breaker (inject secondary)
- Document all settings verified

### Step 7: Functional Testing
- Test main breaker operation (open/close)
- Test interlock functions between equipment
- Test ATS transfer (normal to emergency and back)
- Test generator auto-start and load acceptance
- Test UPS transfer and battery backup
- Test fire alarm interface to emergency power
- Document all functional test results

### Step 8: Commissioning Report Generation
- Compile all test results into commissioning report
- List any deficiencies and corrective actions
- Document all personnel involved in commissioning
- Include as-built drawings and updated SLDs
- Generate handover documentation and O&M manuals
- Obtain sign-off from client/owner

### Step 9: Handover Documentation
- Deliver O&M manuals with all test data
- Provide as-built drawings reflecting final installation
- Document all protection settings applied
- Record arc flash labels and PPE requirements
- Schedule periodic testing reminder for maintenance

## Success Criteria
- All tests completed with results documented
- Protection system verified and functional
- Pre-energization safety checklist complete
- No outstanding safety deficiencies
- Commissioning report with all required sections
- Handover documentation complete and accepted by client

## Common Pitfalls
- **Tests Performed Out of Sequence**: Testing protection before continuity → false results
- **Test Equipment Uncalibrated**: Invalid results from out-of-calibration instruments
- **Missing Safety Clearances**: Personnel not cleared before energization → safety incident
- **Incomplete Pre-Energization Checks**: Temporary grounds not removed → phase-to-earth fault on energization
- **Protection Settings Not Verified**: Incorrect relay settings cause nuisance tripping or no protection

## Cross-References
- NFPA 70B: Recommended Practice for Electrical Equipment Maintenance
- IEC 60076: Power transformers testing
- IEC 62271: High-voltage switchgear testing
- 00860 Domain Knowledge: Commissioning and handover (Part 4, Part 8)
- LOTO Compliance: Pre-energization safety verification
- Protection Coordination: Relay setting verification

## Usage Example
```
Scenario: Commission 1MVA 11kV/415V transformer installation
Step 1: Verify installation (transformer, cables, switchgear all installed) ✓
Step 2: Test equipment calibrated (IR tester, megger, primary injection set) ✓
Step 3: Pre-energization (all permits closed, personnel cleared, LOTO on adjacent) ✓
Step 4: IR test: HV 5000MΩ, LV 200MΩ (both > 100MΩ) ✓
Step 5: Continuity: phase-earth < 1Ω all circuits ✓
Step 6: Protection settings: relay 50/51 settings verified, CT ratio 400/5A ✓
Step 7: Functional: breaker open/close, interlocks, ATS transfer all verified ✓
Step 8: Commissioning report generated with all test results
Step 9: Handover: O&M manuals, as-builts, arc flash labels delivered
```

## Metrics
- Test completion rate: 100% of tests performed and documented
- Protection verification: 100% of relays verified before energization
- Safety: Zero incidents during commissioning
- Documentation: 100% of handover documents delivered within schedule