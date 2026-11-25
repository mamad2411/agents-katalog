---
title: Civil Quality Assurance
description: Execute civil engineering quality assurance workflows including compliance checking, NCR/RFI processing, design review, and quality gate enforcement
version: 1.0
frequency_percent: 70.0
success_rate_percent: 93.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-quality-assurance
gigabrain_tags: civil-engineering, quality-assurance, compliance, NCR, RFI, design-review, quality-gates
openstinger_context: quality-control, compliance-management
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_GLOSSARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/00850_AGENTS-REGISTRY-SUMMARY.MD
related_skills:
  - pre-task-assessment-readiness
  - civil-design-development
  - civil-documentation
  - civil-dwg-processing
---

# Civil Quality Assurance

## Overview

Execute quality assurance workflows for civil engineering projects: code and specification compliance checking, non-conformance report (NCR) processing, request for information (RFI) management, design review validation, and quality gate enforcement at each phase of the design and construction workflow.

**Announce at start:** "I'm using the civil-quality-assurance skill to perform quality checks and compliance validation for the civil engineering project."

## When to Use This Skill

**Trigger Conditions:**
- Design documents need compliance verification against codes and standards
- Site inspection identifies a defect or non-compliant work
- RFI received requiring technical response
- Phase completion requires quality gate validation before proceeding
- ITP hold point needs inspection and approval
- Documentation package needs final quality review

**Prerequisites:**
- Design documents or site data available for review
- Applicable codes and standards identified
- CE-QA-001 agent or equivalent quality capability available
- Quality criteria and acceptance thresholds defined

## Step-by-Step Procedure

### Step 1: Compliance Checking

**Verify design work against applicable codes, standards, and specifications:**

**Compliance verification categories:**
| Category | Check | Standard Reference |
|----------|-------|-------------------|
| Drainage | Pipe capacity (Manning's), self-cleansing velocity | EN 752, local bylaws |
| Roads | Geometric design (sight distance, gradients, curves) | AASHTO, local road authority |
| Pavements | Layer thickness, material grades | TG1/TG2, AASHTO |
| Concrete | Cover, strength class, exposure durability | EN 206, ACI 318 |
| Earthworks | Compaction density, layer thickness | SANS 1200 DB, ASTM D1557 |
| Retaining Walls | Stability (overturning, sliding, bearing) | EN 1997, SANS 10400-H |
| SuDS | Storage volume, water quality treatment | CIRIA C753, local requirements |

**Compliance process:**
1. Identify all applicable codes and standards (from Phase 1 compliance matrix)
2. For each design element, list the relevant code clauses
3. Check design parameters against code requirements
4. Document any non-compliances with specific clause references
5. Generate compliance report with pass/fail status for each check
6. Flag critical non-compliances that prevent design approval

**Compliance report format:**
| Element | Code Clause | Requirement | Actual | Status | Remarks |
|---------|-------------|-------------|--------|--------|---------|
| Pipe P-001 | EN 752 §4.2 | v_min ≥ 0.6 m/s | 0.82 m/s | PASS | Self-cleansing verified |
| Road VC-1 | AASHTO §3.4.2 | SSD ≥ 150m @ 60km/h | 800m VC, SSD=180m | PASS | — |
| Retaining Wall RW-3 | EN 1997 §6.5 | FoS_sliding ≥ 1.5 | 1.35 | FAIL | Increase base width or add key |

### Step 2: NCR (Non-Conformance Report) Processing

**Process non-conformances identified during site inspection or document review:**

**NCR structure:**
```
NCR Number: NCR-YYYY-NNN
Date Raised: [Date]
Raised By: [Name/Agent]

Project: [Project Name]
Location: [Grid lines / chainage / coordinates]
Element: [Description of non-conforming element]

Description of Non-Conformance:
- What was observed (defect description)
- What was required (specification clause)
- Evidence (photos, measurements, test results)

Reference Clause:
- Specification section and clause number
- Drawing reference

Severity Classification:
- Critical (affects safety or structural integrity)
- Major (fails performance requirement, requires rework)
- Minor (cosmetic or documentation deficiency)

Recommended Action:
- [ ] Accept as-is (with engineering justification)
- [ ] Repair (specify repair method)
- [ ] Rework (replace or redo work)
- [ ] Reject (remove from site)

Response Required By: [Date]
Responsible Party: [Contractor/Supplier]

Close-Out:
- Corrective action taken:
- Verification inspection date:
- Closed By: [Name/Agent]
```

### Step 3: RFI (Request for Information) Management

**Process RFIs from contractors, consultants, or stakeholders:**

**RFI processing workflow:**
1. **Receive and Log:** Record RFI number, date, originator, subject, urgency
2. **Categorize:**
   - Design clarification
   - Drawing discrepancy
   - Specification gap
   - Site condition query
   - Alternative material/method proposal
   - Commercial impact query
3. **Assess Impact:**
   - Does it affect design intent? (Yes/No — route to designer if Yes)
   - Does it affect cost or schedule? (Yes/No — notify commercial team if Yes)
   - Does it affect regulatory compliance? (Yes/No — escalate if Yes)
4. **Research:** Review drawings, specs, codes, and design calculations for answer
5. **Draft Response:** Clear, unambiguous answer with drawing/spec references
6. **Quality Review:** Check for completeness, conflicts, and unintended consequences
7. **Issue:** Distribute to originator and all affected parties
8. **Close:** Log response date and update drawing/spec if modification required

**Response quality checklist:**
- [ ] Answer is clear and unambiguous
- [ ] Drawing and specification references are accurate
- [ ] Response does not conflict with other RFI responses
- [ ] Cost/schedule impact assessed (or stated as "none")
- [ ] If drawing/spec change needed, change order initiated
- [ ] All affected parties included in distribution

### Step 4: Design Review Validation

**Conduct structured design review before issue:**

**Design review checklist:**
| Review Item | Check | Status |
|-------------|-------|--------|
| Drawing consistency | Cross-references between drawings accurate | Pass/Fail |
| Spec-drawing match | Drawings reference correct spec sections | Pass/Fail |
| Calculation trail | All design parameters traceable to calculations | Pass/Fail |
| Code compliance | All applicable code clauses satisfied | Pass/Fail |
| Constructability | Design is practical to build safely | Pass/Fail |
| Maintainability | Long-term maintenance access considered | Pass/Fail |
| ITP coverage | All critical activities have ITP hold/witness points | Pass/Fail |
| BOQ completeness | BOQ covers all drawing items | Pass/Fail |
| Revision control | All documents at correct revision | Pass/Fail |
| Sign-off | All documents signed/stamped by responsible professional | Pass/Fail |

### Step 5: Quality Gate Enforcement

**Enforce quality gates at phase boundaries — work cannot proceed to next phase until gate passed:**

**Quality gates by phase:**
| Gate | Between Phases | Gate Criteria |
|------|---------------|---------------|
| Gate 1 | Phase 1 → Phase 2 | Feasibility report approved, all go/no-go criteria met |
| Gate 2 | Phase 2 → Phase 3 | Options analysis complete, preferred option selected and justified |
| Gate 3 | Phase 3 → Phase 4 | All calculations checked, coordination complete, drawings issued for review |
| Gate 4 | Phase 4 → Phase 5 | Full compliance check passed, all NCRs closed, ITPs complete |
| Gate 5 | Phase 5 → Construction | Tender documents complete, all annexures compiled, quality review done |

**Gate enforcement rules:**
- No gate may be bypassed without documented justification and approval
- Gate failures generate a punch list of required corrective actions
- Gate pass requires sign-off by QA lead and discipline lead
- Emergency gate pass (with conditions) requires director-level approval

## Success Criteria

- [ ] Compliance check completed for all applicable code clauses
- [ ] All NCRs processed with severity classification and recommended action
- [ ] RFI response time within SLA (<48 hours for standard, <4 hours for urgent)
- [ ] Design review checklist completed with zero critical findings
- [ ] Quality gates enforced — no phase advanced without gate pass
- [ ] All documentation traceability maintained (design → calc → spec → ITP)

## Common Pitfalls

1. **Rubber-Stamp Reviews** — A review that finds nothing is suspicious. Systematically check every item; superficial reviews let errors through.
2. **NRC Without Reference Clause** — An NCR without a specific specification or drawing clause reference is just an opinion. Always cite the authority.
3. **RFI Contradicts Prior RFI** — Maintain an RFI log and cross-check new responses against existing answers.
4. **Missing Gate Enforcement** — Skipping a quality gate because of schedule pressure creates risk that compounds later. Every gate must be passed.
5. **No Trend Analysis** — Individual NCRs are symptoms. Look for patterns: is the same defect recurring? That signals a systemic issue requiring root cause analysis.

## Cross-References

### Related Skills
- `civil-design-development` — Design review validates Phase 2-3 output
- `civil-documentation` — Documentation review before issue
- `civil-dwg-processing` — DWG extraction validation
- `pre-task-assessment-readiness` — Assess readiness before review
- `sow-generation` — SOW quality review

### Related Agents
- `CE-QA-001` (OpenClaw) — Primary quality assurance agent
- `CE-QC-001` (JS Swarm) — Construction quality control
- `CE-RFI-001` (JS Swarm) — RFI processing and routing
- `Reviewer` (DevForge) — Quality assurance and standards validation

## Example Usage

**Scenario:** Quality review of preliminary drainage design documents before client issue

1. **Compliance Check:** 42 checks performed across EN 752 (drainage), local bylaws, and project specs. 39 passed, 3 flagged:
   - Pipe P-005 velocity 0.52 m/s (fails 0.6 m/s self-cleansing) — MAJOR
   - Manhole MH-07 cover level 10mm below road profile — MINOR
   - Detention basin freeboard 250mm (spec requires 300mm) — MAJOR
2. **Design Review:** 10-item checklist completed. 2 failures: spec-drawing mismatch on MH type, ITP missing for detention basin compaction.
3. **Action:** Return to designer for corrective action. Re-submit when pipe gradient adjusted to meet ≥0.6 m/s and freeboard increased to 300mm.
4. **Gate 3:** NOT PASSED. Corrective actions identified, gate remains closed until re-submitted.

## Performance Metrics

**Target Performance:**
- Compliance check coverage: 100% of applicable code clauses checked
- NCR processing time: <24 hours from identification to issuance
- RFI response SLA: 95% of standard RFIs responded within 48 hours
- Design review findings: Zero critical findings at final gate
- Gate enforcement: Zero unapproved gate bypasses