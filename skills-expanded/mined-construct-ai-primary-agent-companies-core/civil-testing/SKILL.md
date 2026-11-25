---
title: Civil Engineering Testing
description: Testing skill for civil engineering workflows including skill validation, scenario testing, and quality assurance verification
version: 1.0
frequency_percent: 20.0
success_rate_percent: 100.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-testing
gigabrain_tags: civil-engineering, testing, validation, quality-assurance
openstinger_context: civil-testing, skill-validation
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/prompts/00850_CIVIL-DOCUMENTATION-WORKFLOW-PROMPT.md
related_skills:
  - pre-task-assessment-readiness
  - testing-verification
  - civil-quality-assurance
---

# Civil Engineering Testing

## Overview

Systematically test all 10 civil engineering skills against realistic scenarios to verify correctness, completeness, and readiness. Covers each skill's trigger conditions, step-by-step procedures, success criteria, and cross-references.

**Announce at start:** "I'm using the civil-testing skill to validate civil engineering skills."

## When to Use This Skill

**Trigger Conditions:**
- New skills created and ready for validation
- Skills updated after remediation
- Pre-deployment readiness verification
- Post-change regression testing

## Skill Validation Test Scenarios

### Test 1: civil-dwg-processing
**Scenario:** Process a 25MB site drainage DWG (Revision B)
- [ ] File reception and pre-check passes
- [ ] 7-stage cleaning pipeline completes
- [ ] Feature extraction identifies pipes, manholes, catch basins
- [ ] Structured JSON output generated
- [ ] Validation rules pass (velocity, gradient, elevation)
- [ ] Provenance tags attached to all features
- [ ] Handoff to quantity takeoff successful

### Test 2: civil-site-assessment
**Scenario:** Assess a 1.5ha urban infill site
- [ ] Project brief structured
- [ ] Survey data validated
- [ ] Geotechnical assessment completed
- [ ] Environmental constraints mapped
- [ ] Regulatory compliance matrix complete
- [ ] Go/no-go recommendation made
- [ ] Risk register with ≥5 items

### Test 3: civil-design-development
**Scenario:** Develop 3 road alignment options for a 2km subdivision
- [ ] 3 options developed and scored
- [ ] Preferred option selected with justification
- [ ] Road design: horizontal, vertical, pavement
- [ ] Drainage design: catchments, pipes, detention
- [ ] Multi-discipline coordination (≥3 disciplines)
- [ ] Cost estimate with confidence level
- [ ] Preliminary drawings issued

### Test 4: civil-documentation
**Scenario:** Compile construction documentation package
- [ ] SOW complete (no blank fields)
- [ ] Specifications developed (all sections)
- [ ] Drawing register complete
- [ ] Calculations signed
- [ ] ITPs with hold/witness points
- [ ] All annexures compiled
- [ ] Quality review checklist passed

### Test 5: civil-quality-assurance
**Scenario:** Review preliminary drainage design
- [ ] Compliance checks completed (100% code clauses)
- [ ] NCRs processed with severity classification
- [ ] RFI responses within SLA
- [ ] Design review checklist complete
- [ ] Quality gates enforced

### Test 6: civil-mobile-field-ops
**Scenario:** Daily site inspection (offline)
- [ ] Field session initialized offline
- [ ] Inspections completed and signed
- [ ] NCRs auto-generated for failures
- [ ] Progress data captured
- [ ] Issues logged with photos
- [ ] Data queued for sync

### Test 7: civil-ui-card-system
**Scenario:** Navigate Phase 1 cards
- [ ] Dashboard loads with all 14 cards
- [ ] Dependencies enforced (Card 5 blocked until Phase 1 complete)
- [ ] Status transitions work
- [ ] Agent processing initiated per card
- [ ] Phase gate enforced
- [ ] Progress report exported

### Test 8: civil-quantity-takeoff
**Scenario:** Extract BOQ for drainage package
- [ ] All BOQ categories populated
- [ ] Extraction verified (3 spot-checks within 3%)
- [ ] Units correct throughout
- [ ] Quantities traceable to drawings
- [ ] Waste factors applied
- [ ] Material schedule generated

### Test 9: civil-desktop-mobile-sync
**Scenario:** Sync field data with limited connectivity
- [ ] Sync direction assessed
- [ ] Priority tiers enforced (P0-P2 via cell, P3-P4 queued)
- [ ] Conflicts detected and resolved
- [ ] Offline functionality maintained
- [ ] Integrity checks pass post-sync

### Test 10: civil-tender-preparation
**Scenario:** Tender for drainage works
- [ ] Tender package complete
- [ ] Internal consistency verified
- [ ] Prequalification: ≥3 contractors shortlisted
- [ ] Bid evaluation: all 5 phases completed
- [ ] Award recommendation documented

## Success Criteria

- [ ] All 10 skills pass their test scenarios
- [ ] Zero critical defects found
- [ ] Cross-references between skills resolve correctly
- [ ] Agent assignments verified and functional
- [ ] Glossary terms used correctly in all skill outputs
- [ ] Frequency and success rate metrics realistic

## Performance Metrics

**Target:**
- Test coverage: 100% of skills tested
- Pass rate: 100% of test scenarios passed
- Defect rate: 0 critical defects, <3 minor issues
- Documentation: All test results documented