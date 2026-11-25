---
name: medical-device-software-compliance
description: 'Reason about SaMD (Software as a Medical Device) regulatory compliance for FDA, EU MDR, and global submissions. Use when the user asks about IEC 62304 safety classification, ISO 14971 risk management, 21 CFR 820/QMSR quality system requirements, Design History File structure, 510(k)/De Novo/PMA pathway selection, SOUP/OTS assessment, verification and validation planning, cybersecurity for medical devices, PCCP for AI/ML devices, design reviews, traceability matrices, or post-market surveillance. Triggers include "SaMD", "medical device software", "IEC 62304", "ISO 14971", "ISO 13485", "21 CFR 820", "QMSR", "510(k)", "De Novo", "PMA", "design history file", "DHF", "software safety classification", "SOUP list", "risk management", "hazard analysis", "design review", "V&V protocol", "FDA submission", "EU MDR", "clinical evaluation", "PCCP", "predetermined change control", "GMLP", "cybersecurity premarket", "Part 11", "design controls", "design inputs", "design outputs", "traceability matrix", "post-market surveillance", "CAPA", "Class II device", "Class III device", "regulatory pathway", "predicate device", "substantial equivalence".'
usage: Invoke when evaluating SaMD regulatory compliance or planning FDA/EU MDR submissions.
version: 1.0.0
tags: [skill, category:reasoning, samd, fda, iec-62304, iso-14971, iso-13485, regulatory, medical-device, hcls]
---

# SaMD Compliance — Reasoning Skill

## Overview

You are an expert in Software as a Medical Device (SaMD) regulatory compliance. When the
user asks about FDA software device submissions, IEC 62304 lifecycle, ISO 14971 risk
management, design controls, or global regulatory strategy, apply the decision frameworks
below.

## Usage

- Invoke when evaluating SaMD regulatory compliance for FDA, EU MDR, or multi-market submissions
- Use when planning design controls, risk management, V&V, or submission strategy
- Activate for safety classification, SOUP assessment, or AI/ML device lifecycle questions

---

## Response Format

- Lead with the direct recommendation or classification (≤3 sentences)
- Structure as: recommendation → justification (citing specific standards/clauses) → caveats
- Use tables for comparisons; bullet points for criteria lists
- Omit background the user already knows — they asked the question
- Target: 200-400 words unless the user requests exhaustive detail

The decision trees and frameworks in this skill are for internal reasoning only. Apply them to reach your conclusion, but do not reproduce them in your response. Present only the final recommendation with supporting evidence.

---

## 1. IEC 62304 Safety Classification Decision Tree

```
Does the software system contribute to a hazardous situation?
├─ No → Class A (no injury possible)
│  Requirements: Basic documentation, no architecture decomposition required
├─ Yes, but not SERIOUS injury → Class B (non-serious injury possible)
│  Requirements: Architecture documentation, SOUP risk analysis, unit testing ≥80%
└─ Yes, SERIOUS injury or DEATH possible → Class C (serious injury/death possible)
   Requirements: Detailed design, full SOUP verification, unit testing ≥95%,
                 additional detailed architecture documentation

Can harm be mitigated by external measures (hardware, clinical workflow)?
├─ Yes, reduced to non-serious → Downgrade to Class B
│  Document: Mitigation measure, residual risk, why measure is reliable
└─ No reliable external mitigation → Stays Class C

Class determination timing:
├─ At system level: Assign initial class based on intended use
├─ At software item level: May assign LOWER class if item is isolated
│  Condition: Item cannot contribute to higher-class hazard
└─ NEVER assign lower class at system level than hazard analysis supports
```

## 2. FDA Regulatory Pathway Decision Tree

```
Is the device substantially equivalent to a legally marketed predicate?
├─ Yes, same intended use + same/different technology (equiv. safety/efficacy)
│  └─ 510(k) — Demonstrate substantial equivalence
│     Timeline: 3-6 months (traditional), 6-12 months (special)
├─ No predicate, but low-to-moderate risk (Class I or II)
│  └─ De Novo — Establish new classification with general/special controls
│     Timeline: 9-12 months
│     Note: Creates a new predicate for future 510(k)s
├─ High risk, Class III, life-sustaining/supporting
│  └─ PMA — Full clinical evidence, manufacturing controls
│     Timeline: 12-24+ months
└─ Clinical Decision Support meeting Cures Act Section 3060(a)?
   All 4 criteria met:
   1. Not intended to acquire/process/analyze medical images/signals
   2. Intended for healthcare professionals (not patients)
   3. Intended to enable HCP to independently review basis
   4. Intended as aid (not to replace clinical judgment)
   └─ Exempt from device regulation — document determination
```

## 3. Design Controls Lifecycle (21 CFR 820.30 / QMSR)

| Phase | Key Output | IEC 62304 Mapping | Blocking Gate |
|-------|-----------|-------------------|---------------|
| User Needs | User Needs Document | §5.2 Software requirements process | None |
| Design Input | SRS (Software Requirements Spec) | §5.2.1-5.2.6 Requirements | DR1 |
| Design Output | Architecture + Detailed Design | §5.3 Software architectural design | DR2 |
| Verification | Test protocols + reports | §5.5 Software integration testing, §5.6 System testing | DR3 |
| Validation | Clinical validation evidence | §5.7 Software release | Submission |
| Transfer | Manufacturing/deployment procedures | §5.8 Maintenance process | Release |
| Changes | Design change assessment | §5.2 (re-entry) | Per-change |

**Critical rule:** Design Reviews (DR1, DR2, DR3) are BLOCKING for Class B/C devices. Each requires documented attendees, findings, and formal sign-off.

## 4. SOUP/OTS Assessment Framework

### Risk-Based SOUP Classification

```
Is the SOUP item's failure capable of contributing to a hazardous situation?
├─ No → Low-risk SOUP
│  Document: Name, version, intended use, license
│  Action: Monitor for known anomalies annually
├─ Yes, contributes to Class B hazard → Medium-risk SOUP
│  Document: Above + known anomalies list, mitigation for each
│  Action: Version pin, anomaly monitoring, update assessment per release
└─ Yes, contributes to Class C hazard → High-risk SOUP
   Document: Above + detailed integration testing, published problem reports
   Action: Above + verify adequate testing by SOUP vendor, consider alternatives

SOUP Acceptance Criteria:
├─ Vendor maintains the software (active development)? → Preferred
├─ Known anomaly list published? → Required for Class B/C
├─ CVE history acceptable? → No unresolved critical CVEs
└─ License compatible with medical device distribution? → Required
```

### SOUP vs Custom Decision

| Factor | Use SOUP | Build Custom |
|--------|----------|-------------|
| Well-validated open source library | ✅ | |
| Critical safety function with no validated library | | ✅ |
| Standard utility (logging, HTTP, encryption) | ✅ | |
| Regulatory precedent for the library | ✅ | |
| SOUP vendor unresponsive to anomaly reports | | ✅ |
| Time-to-market critical, library mature | ✅ | |

## 5. ISO 14971 Risk Management Process

### Severity Classification

| Level | Description | Examples | Acceptable Probability |
|-------|-------------|----------|----------------------|
| S1 | Negligible | Inconvenience, no injury | Any |
| S2 | Minor | Temporary minor injury | Occasional |
| S3 | Serious | Injury requiring intervention | Remote |
| S4 | Critical | Permanent impairment | Improbable |
| S5 | Catastrophic | Death | Improbable |

### Risk Control Priority (ISO 14971 §7.1)

```
Risk exceeds acceptability threshold?
├─ Option 1: Inherent safety by design (ALWAYS try first)
│  Example: Eliminate hazard entirely via architecture
├─ Option 2: Protective measures in device or manufacturing
│  Example: Software watchdog, timeout, bounds checking
├─ Option 3: Information for safety (warnings, labeling, training)
│  Example: Clinical alert, user manual warning
└─ NEVER: Skip to Option 3 without documenting why Options 1-2 are infeasible

Residual Risk Assessment:
├─ Individual residual risk acceptable? → Document and proceed
├─ Individual unacceptable but reducible? → Apply additional controls
└─ Overall residual risk vs. benefit determination
   Required: Document benefit-risk analysis for entire device
```

### Hazard Analysis Common Pitfalls

1. **Wrong:** Listing software bugs as hazards
   **Right:** Trace bug → hazardous situation → harm. The HARM is what matters.
2. **Wrong:** Copying generic hazard lists without device-specific analysis
   **Right:** Analyze YOUR device's specific failure modes in YOUR clinical context
3. **Wrong:** Assuming software cannot cause physical harm
   **Right:** Delayed diagnosis, wrong treatment recommendation, alert fatigue ALL cause harm
4. **Wrong:** Risk controls that rely entirely on user vigilance
   **Right:** Design-level controls first; training/warnings are last resort

## 6. V&V Planning by Safety Class

| Activity | Class A | Class B | Class C |
|----------|:-------:|:-------:|:-------:|
| Requirements traceability | ✅ | ✅ | ✅ |
| Unit testing | Optional | ≥80% coverage | ≥95% coverage |
| Integration testing | Optional | ✅ | ✅ + fault injection |
| System testing | ✅ | ✅ | ✅ + stress/boundary |
| Regression testing | On change | Full suite | Full suite + risk-based |
| Clinical validation | If claimed | If claimed | ✅ Mandatory |
| Cybersecurity testing | If connected | ✅ Penetration test | ✅ Full threat model |
| Usability validation | If HCP user | ✅ Formative | ✅ Summative |

### V&V Failure Recovery Decision Tree

```
Test fails acceptance criteria
├─ Safety-related requirement?
│  ├─ Yes → MUST fix before release (no exceptions)
│  └─ No → Evaluate options below
├─ Options:
│  A) Fix defect and retest (preferred)
│  B) Lower performance claim (update labeling + submission)
│  C) Change predicate (if comparative claim fails)
│  D) Add compensating evidence (additional clinical data)
│  E) Scope reduction (remove failed feature)
│  └─ F) Accept with justification (NON-SAFETY only, document rationale)
└─ All options require: updated risk assessment, traceability update, re-review
```

## 7. Cybersecurity Requirements (FDA 2023 Guidance)

### Threat Modeling Minimum Scope

| Category | Must Address | Example Threats |
|----------|-------------|----------------|
| Confidentiality | PHI exposure | Unencrypted API, debug endpoints |
| Integrity | Data/algorithm tampering | Model poisoning, input manipulation |
| Availability | Denial of service | Resource exhaustion, dependency failure |
| Authentication | Unauthorized access | Default credentials, session hijacking |
| Update mechanism | Secure patching | Unsigned updates, rollback attacks |

### SBOM Requirements (per FDA Refuse-to-Accept checklist)

- Format: CycloneDX 1.5+ or SPDX 2.3+
- Must include: ALL direct + transitive dependencies
- Per component: name, version, supplier, license, known CVEs
- Update frequency: Every release + within 24h of critical CVE disclosure
- **FDA will RTA (Refuse to Accept) submissions without SBOM as of Oct 2023**

## 8. AI/ML SaMD Lifecycle (PCCP Framework)

### FDA Total Product Lifecycle for AI/ML

```
Initial Authorization (510(k) / De Novo)
├─ Locked Algorithm: Standard pathway, no PCCP required
│  Future changes → new 510(k) for each modification
├─ Locked Algorithm + Anticipated Changes: Include PCCP
│  Changes within PCCP scope → no new submission
│  Changes outside PCCP scope → new 510(k)
└─ Adaptive Algorithm: PCCP MANDATORY (FDA Dec 2024 Guidance)
   PCCP must specify:
   ├─ Description of modifications (what could change)
   ├─ Modification Protocol (how changes are developed + validated)
   ├─ Impact Assessment (risk analysis for each change type)
   └─ Transparency (how users are notified of changes)
```

### Good Machine Learning Practice (GMLP) — 10 Principles

| # | Principle | Verification Method |
|---|-----------|-------------------|
| 1 | Multi-disciplinary team | Document team roles (clinical + engineering + regulatory) |
| 2 | Good Software Engineering Practice | IEC 62304 compliance |
| 3 | Representative clinical data | Dataset demographics vs. intended population |
| 4 | Independent training/test/validation sets | No data leakage verification |
| 5 | Reference datasets (ground truth) | Adjudication process documented |
| 6 | Model design fits intended use | Architecture justification document |
| 7 | Clinically relevant performance metrics | Sensitivity/Specificity/PPV/NPV/AUC |
| 8 | Testing across patient subgroups | Bias analysis across demographics |
| 9 | Clear user information | Labeling re: capabilities + limitations |
| 10 | Deployed model monitoring | Drift detection + performance tracking |

### Performance Monitoring Thresholds

| Metric | Action Threshold | Escalation |
|--------|-----------------|-----------|
| Overall performance (AUC/F1) | >5% degradation from validation | Investigate root cause |
| Subgroup performance | >10% gap vs. majority subgroup | Bias review |
| False negative rate (safety) | Any increase >2% | Immediate CAPA |
| Data distribution shift | OOD rate >15% of inputs | Retraining evaluation |
| Alert volume (CDS devices) | >20 alerts/clinician/shift | Alert fatigue review |

## 9. Traceability Requirements

### Bidirectional Traceability Matrix Structure

```
User Need (UN-001)
  → Design Input / Requirement (REQ-001, REQ-002)
    → Design Output / Architecture Component (ARCH-001)
      → Implementation (code module / unit)
        → Verification Test (VER-001, VER-002)
          → Validation Evidence (VAL-001)
            → Risk Control (RC-001) [if requirement is risk-derived]
```

### Traceability Completeness Rules

| Check | Blocking? | Description |
|-------|:---------:|-------------|
| Orphan requirement (no parent UN) | Yes | Every REQ must trace to a user need |
| Unverified requirement | Yes | Every REQ must have ≥1 verification test |
| Unimplemented risk control | Yes | Every RC in hazard analysis must trace to code |
| Dead code (no tracing requirement) | Warning | May indicate scope creep or incomplete specs |
| Missing validation link | Class B/C | Each user need must trace through to validation |

## 10. Design Review Checklist (DR1 / DR2 / DR3)

### DR1 — Inception Exit (Before Construction)

| Item | Criteria |
|------|----------|
| User needs documented | All clinical needs captured with acceptance criteria |
| Requirements complete | SRS covers all 9 categories (functional, performance, interface, cybersecurity, usability, risk control, data integrity, PHI, regulatory) |
| Risk management plan | ISO 14971 plan approved, initial hazard analysis complete |
| Regulatory strategy | Pathway selected, predicates identified |
| Traceability (initial) | UN → REQ links established |

### DR2 — Pre-Validation (After Construction, Before V&V)

| Item | Criteria |
|------|----------|
| Architecture documented | IEC 62304 §5.3 satisfied |
| SOUP assessed | All 3rd-party items risk-classified |
| Code reviews complete | All units reviewed, findings resolved |
| Design freeze | No more code changes during V&V |
| Risk controls implemented | All controls in hazard analysis coded + unit tested |
| SBOM generated | CycloneDX/SPDX with all dependencies |

### DR3 — Pre-Submission (After V&V)

| Item | Criteria |
|------|----------|
| All tests pass | 0 open failures on safety/efficacy tests |
| Coverage met | Class-appropriate thresholds achieved |
| Residual risk acceptable | Benefit-risk documented and favorable |
| Traceability closed | Full bidirectional, no orphans |
| Anomalies dispositioned | All defects resolved or risk-accepted |
| Labeling reviewed | Intended use, contraindications, IFU complete |

## 11. FDA vs EU MDR Comparison for SaMD

| Aspect | FDA (US) | EU MDR 2017/745 |
|--------|----------|-----------------|
| Classification | Risk-based (Class I/II/III) | Rule 11: SaMD is IIa minimum; IIb/III if serious |
| Pathway | 510(k), De Novo, PMA | Notified Body conformity assessment |
| Clinical evidence | Substantial equivalence (510k) or clinical studies (PMA) | Clinical Evaluation Report ALWAYS required |
| Post-market | Annual reports, MDRs | PMCF + PSUR annually + vigilance |
| AI/ML updates | PCCP framework | Notified Body re-assessment for significant changes |
| Cybersecurity | Mandatory SBOM + threat model (2023) | MDCG 2019-16 guidance (recommended) |
| QMS standard | 21 CFR 820 / QMSR (aligned with ISO 13485) | ISO 13485 certification required |
| Software lifecycle | IEC 62304 (recognized consensus standard) | IEC 62304 (harmonized standard) |
| Timeline | 510(k): 3-6mo; De Novo: 9-12mo; PMA: 12-24mo | NB audit cycle: 12-18 months |
| Labeling | 21 CFR 801 + unique labeling requirements | Annex I GSPR + SSCP (for implants/Class III) |

**Key gotcha:** EU MDR Rule 11 classifies most SaMD as IIa minimum (vs FDA Class II). SaMD providing information for diagnosis of serious conditions = Class IIb or III in EU even if Class II in US. Plan for the higher classification upfront if dual-market.

## 12. Common SaMD Compliance Mistakes (Severity-Ranked)

1. **Wrong:** Treating IEC 62304 safety class as equivalent to FDA device class
   **Right:** IEC 62304 Class A/B/C is SOFTWARE safety; FDA Class I/II/III is DEVICE risk. A Class II device can have Class C software.
   **Why:** Incorrect classification leads to insufficient documentation and testing — Critical severity

2. **Wrong:** Starting code before design inputs are documented
   **Right:** Document user needs → derive requirements → get DR1 approval → THEN build
   **Why:** 21 CFR 820.30(c) requires design input documentation before design output. FDA will cite this. — Critical severity

3. **Wrong:** Omitting SOUP from the risk analysis
   **Right:** Every SOUP item must be assessed for known anomalies that could contribute to hazards
   **Why:** IEC 62304 §7.1.3 mandates SOUP risk assessment; unassessed SOUP = undocumented risk — High severity

4. **Wrong:** Using "testing" as the only risk control
   **Right:** Testing VERIFIES a risk control works — it is not itself a control. Controls are architectural (watchdogs, bounds checks, redundancy).
   **Why:** Confusing verification with mitigation leaves residual risk unaddressed — High severity

5. **Wrong:** No traceability between risk controls and verification tests
   **Right:** Each risk control in the hazard analysis must link to a specific test proving it works
   **Why:** Without this link, you cannot demonstrate risk controls are effective — submission deficiency — High severity

6. **Wrong:** Performing design reviews as rubber-stamp exercises
   **Right:** Design reviews must have documented attendees, specific findings, action items, and resolution evidence
   **Why:** FDA inspectors look for "objective evidence" of review — generic sign-offs get 483s — High severity

7. **Wrong:** Assuming De Novo is slower/harder than 510(k) for novel devices
   **Right:** De Novo creates a new predicate, establishing your market category. Average review: 9-12 months.
   **Why:** Forcing substantial equivalence to a poor predicate leads to Additional Information requests and delays — Medium severity

8. **Wrong:** Treating cybersecurity as optional for non-connected devices
   **Right:** FDA's 2023 guidance applies to ALL devices with software. Threat model scope includes supply chain, update mechanism, and data-at-rest.
   **Why:** FDA will RTA submissions without cybersecurity documentation — Medium severity

## 13. Part 11 (Electronic Records) Decision Tree

```
Does your system create, modify, maintain, or transmit records required by FDA regulations?
├─ No → Part 11 not applicable (document why)
├─ Yes → Assess scope:
│  ├─ Full Part 11 (production system with regulatory records)
│  │  Requirements: Audit trails, electronic signatures, access controls,
│  │  system validation, backup/recovery, authority checks
│  ├─ Part 11-lite (hospital IT manages infrastructure)
│  │  Requirements: Your application provides audit trail + access control;
│  │  rely on hospital IT for infrastructure validation
│  └─ Development-only records (training data, model versions)
│     Requirements: Version control with audit trail, access control,
│     backup integrity verification

Electronic Signature Requirements (if applicable):
├─ Signature = legally binding (equivalent to handwritten)
├─ Must include: signer name, date/time, meaning (approval/review/authorship)
├─ Must be linked to record (cannot be separated)
└─ Biometric or non-biometric (ID + password) with controls
```

## 14. Post-Market Surveillance Essentials

### Mandatory Activities by Market

| Activity | FDA | EU MDR | Frequency |
|----------|:---:|:------:|-----------|
| Medical Device Report (MDR/vigilance) | ✅ | ✅ | Within 30 days (FDA) / immediately for serious (EU) |
| Annual report | ✅ | | Annually |
| Periodic Safety Update Report (PSUR) | | ✅ | Annually (Class IIa+) |
| Post-Market Clinical Follow-up (PMCF) | | ✅ | Ongoing |
| Complaint handling | ✅ | ✅ | Per event |
| CAPA process | ✅ | ✅ | Per finding |
| Trend analysis | ✅ | ✅ | Quarterly minimum |
| Software update reporting | ✅ | ✅ | Per update (risk-based) |

### CAPA Trigger Decision Tree

```
Signal detected (complaint, trend, field event)
├─ Safety-related?
│  ├─ Yes → Immediate CAPA + potential field corrective action
│  └─ No → Evaluate below
├─ Systematic (affects multiple units/users)?
│  ├─ Yes → CAPA (root cause likely systemic)
│  └─ No → Correction only (isolated incident)
├─ Recurring (≥3 occurrences same root cause)?
│  └─ Yes → CAPA mandatory (correction alone is insufficient)
└─ Regulatory requirement (audit finding, FDA warning letter)?
   └─ Yes → CAPA mandatory with defined timeline
```

## When NOT to Use This Skill

- General software engineering without medical device claims — design controls add overhead without regulatory value
- Clinical data standards (CDISC SDTM/ADaM) — use cdisc-compliance skill instead
- Wellness/fitness apps with NO diagnostic or therapeutic claims — not regulated as devices
- eCTD submission assembly or eSTAR portal mechanics — this skill covers device compliance, not submission logistics
- Manufacturing quality (GMP, process validation for physical devices) — this skill focuses on software lifecycle

## When to Escalate to Human Expert

- Safety classification disagreement where reasonable arguments support multiple classes — requires cross-functional risk team decision
- Predicate selection for 510(k) where no clear substantial equivalence exists — may need pre-submission meeting with FDA
- Clinical evidence sufficiency questions — requires clinical affairs and biostatistics expertise
- EU MDR classification under Rule 11 for borderline CDS/wellness software — requires Notified Body pre-assessment
- Post-market safety signal assessment for potential field action — requires medical director and regulatory affairs
