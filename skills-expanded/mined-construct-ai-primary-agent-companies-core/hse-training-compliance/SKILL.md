---
title: HSE Training Compliance
description: Track HSE training matrix, monitor certification expiry dates, verify competency requirements, schedule refresher training, and maintain training records with automated compliance monitoring and alert system
version: 1.0
frequency_percent: 80.0
success_rate_percent: 95.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00885_hse-director/hse-training-compliance
gigabrain_tags: disciplines, 00885_hse-director, training-compliance, certification-tracking, competency-verification, training-records
openstinger_context: hse-director, training-management, competency-assurance
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00885_hse-director/agent-data/domain-knowledge/00885_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00885_hse-director/agent-data/prompts/00885_AI-NATIVE-HSE-DIRECTOR-PROMPT.md
related_skills:
  - pre-task-assessment-readiness
  - hse-safety-performance-monitoring
  - hse-executive-reporting
---

# HSE Training Compliance

## Overview

Track HSE training matrix for all personnel, monitor certification expiry dates with automated alerts, verify competency requirements for high-risk activities, schedule refresher training, maintain comprehensive training records, and generate compliance reports. Ensures all personnel have required HSE training and certifications before performing work.

**Announce at start:** "I'm using the hse-training-compliance skill to track HSE training and verify competency."

## When to Use This Skill

**Trigger Conditions:**
- New personnel induction
- Monthly training compliance reporting
- Certification expiry alerts (30/14/7 days before expiry)
- Pre-work competency verification
- Training needs identified from incidents or audits
- Regulatory training requirement changes
- Board-level HSE training compliance reporting

**Prerequisites:**
- HSE training matrix (required training by role/activity)
- Personnel database with current certifications
- Training provider records
- Competency assessment criteria
- Training scheduling system

## Step-by-Step Procedure

### Step 1: HSE Training Matrix Development

Define required HSE training by role and activity:

| Role/Activity | Required Training | Validity Period | Refresher Frequency |
|--------------|-------------------|----------------|---------------------|
| **All Personnel** | HSE Induction | Indefinite | Annual refresher |
| **Site Workers** | Site-Specific Safety | Project duration | Quarterly toolbox talks |
| **Work at Height** | Fall Protection, Harness Use | 3 years | 3-yearly |
| **Confined Space** | Confined Space Entry | 2 years | 2-yearly |
| **Hot Work** | Fire Prevention, Hot Work Permit | 2 years | 2-yearly |
| **Excavation** | Excavation Safety | 3 years | 3-yearly |
| **Lifting Operations** | Lifting Supervisor/Banksman | 3 years | 3-yearly |
| **First Aiders** | First Aid Certificate | 3 years | 3-yearly |
| **Fire Marshals** | Fire Safety, Evacuation | 1 year | Annual |
| **HSE Officers** | NEBOSH/SAMTRAC | Indefinite | CPD annual |
| **Supervisors** | Supervisor Safety Training | 3 years | 3-yearly |

**Matrix Updates:**
- Review annually or when regulations change
- Add new training based on incident lessons learned
- Remove obsolete training requirements

### Step 2: Training Record Management

Maintain comprehensive training records for all personnel:

**Training Record Fields:**
| Field | Content | Purpose |
|-------|---------|---------|
| **Person ID** | Employee/contractor number | Unique identifier |
| **Training Course** | Course name and code | Training type |
| **Training Provider** | Provider name and accreditation | Quality assurance |
| **Training Date** | Date completed | Currency tracking |
| **Expiry Date** | Certification expiry | Compliance monitoring |
| **Certificate Number** | Certificate reference | Verification |
| **Trainer Name** | Who delivered training | Accountability |
| **Competency Assessment** | Pass/fail/score | Effectiveness verification |
| **Renewal Status** | Current/expiring/expired | Alert triggering |

**Record Retention:**
- Active personnel: Current + historical records
- Departed personnel: Retain for 7 years (legal requirement)
- Training attendance registers: Permanent retention

### Step 3: Certification Expiry Monitoring

Monitor certification expiry with automated alerting:

**Alert Tiers:**
| Alert Tier | Timing | Recipients | Action Required |
|-----------|--------|-----------|------------------|
| **Advance Notice** | 30 days before expiry | Individual, line manager | Schedule refresher training |
| **Urgent Notice** | 14 days before expiry | Individual, line manager, HSE officer | Expedite training booking |
| **Critical Alert** | 7 days before expiry | Individual, line manager, HSE officer, HSE director | Urgent training or stop work |
| **Expired** | Day of expiry | All above + site management | Stop work until recertified |

**Expiry Calculation:**
```
Days_to_Expiry = Expiry_Date - TODAY
IF Days_to_Expiry = 30 THEN SEND advance_notice
IF Days_to_Expiry = 14 THEN SEND urgent_notice  
IF Days_to_Expiry = 7 THEN SEND critical_alert
IF Days_to_Expiry <= 0 THEN SEND expired_alert AND FLAG work_prohibition
```

### Step 4: Pre-Work Competency Verification

Verify competency before high-risk work commences:

**Verification Workflow:**
```
HIGH-RISK WORK PLANNED (e.g., work at height, confined space, hot work)
    ↓
IDENTIFY personnel assigned to work
    ↓
CHECK training matrix for required training
    ↓
QUERY training database for each person's current certifications
    ↓
IF all required training valid THEN
    APPROVE work commencement
ELSE
    IDENTIFY training gaps
    PROHIBIT work until gaps closed
    NOTIFY line manager and HSE officer
END IF
```

**Verification Certificate:**
```
Work Type: Confined Space Entry
Permit Number: CSE-2026-042
Personnel: John Smith (ID: EMP-1234)
Required Training: Confined Space Entry
Current Certification: CSE-2024-JAN (expires 2027-01-15)
Status: VALID ✓
Verified By: HSE Officer - Jane Doe
Date: 2026-03-28
```

### Step 5: Training Needs Analysis

Identify training gaps and prioritize training delivery:

**Gap Analysis Sources:**
- Incident investigations (training deficiencies)
- Audit findings (non-compliances)
- New equipment or procedures
- Regulatory changes
- Competency assessments (failed or low scores)

**Training Priority Matrix:**
| Priority | Criteria | Response Time |
|----------|---------|---------------|
| **Critical** | Expired certification for active work, regulatory requirement | Immediate (stop work if needed) |
| **High** | Certification expiring <30 days, incident-identified gap | Within 14 days |
| **Medium** | Certification expiring 30-90 days, audit-identified gap | Within 30 days |
| **Low** | Enhancement training, competency development | Within 90 days |

### Step 6: Training Effectiveness Assessment

Assess training effectiveness through competency evaluation:

**Assessment Methods:**
| Method | Use Case | Frequency |
|--------|---------|-----------|
| **Written Test** | Knowledge verification (e.g., regulations, procedures) | Post-training |
| **Practical Demonstration** | Skill verification (e.g., harness donning, fire extinguisher use) | Post-training |
| **Workplace Observation** | On-the-job competency (e.g., permit compliance, hazard recognition) | Monthly/quarterly |
| **Refresher Assessment** | Retention verification | At refresher training |
| **Incident Analysis** | Training adequacy verification | Post-incident |

**Competency Score:**
```
Pass: ≥80% (competent, no restrictions)
Marginal: 70-79% (competent with supervision required)
Fail: <70% (not competent, retraining required)
```

**Training Effectiveness Metrics:**
| Metric | Target | Calculation |
|--------|--------|-------------|
| **Pass Rate** | >90% | (Passed / Total assessed) × 100 |
| **Competency Retention** | >85% at refresher | Refresher assessment pass rate |
| **Post-Training Incident Rate** | Decreasing | Incidents attributable to training deficiency |

### Step 7: Training Compliance Reporting

Generate training compliance reports for management:

**Report Components:**
1. **Overall Compliance Rate:** (Valid certifications / Required certifications) × 100
2. **Expiry Forecast:** Certifications expiring in next 30/60/90 days
3. **Non-Compliance List:** Personnel with expired or missing training
4. **Training Delivery Status:** Scheduled vs. completed training
5. **Competency Assessment Results:** Pass rates, failed assessments
6. **Contractor Compliance:** Contractor training verification status

**Compliance Targets:**
- Overall compliance: 100%
- No expired certifications for active personnel
- All high-risk work personnel verified before work start

### Step 8: Contractor HSE Training Verification

Verify contractor personnel HSE training before site access:

**Contractor Verification Process:**
```
CONTRACTOR MOBILIZES
    ↓
REQUEST training certificates for all personnel
    ↓
VERIFY certificates against training matrix requirements
    ↓
CHECK certificate validity (within expiry date)
    ↓
VERIFY training provider accreditation
    ↓
IF all valid THEN
    ISSUE site access approval
    LOG certificates in contractor file
ELSE
    IDENTIFY gaps
    REQUIRE training before site access
END IF
```

**Contractor Training Register:**
- Company name
- Personnel name and ID
- Training courses and expiry dates
- Certificate verification date
- Site access approval status

## Success Criteria

- [ ] HSE training matrix defined for all roles and activities
- [ ] Training records maintained for all personnel (100% coverage)
- [ ] Certification expiry monitoring operational with automated alerts
- [ ] Pre-work competency verification conducted for all high-risk activities
- [ ] Training needs analysis identifies and prioritizes gaps
- [ ] Training effectiveness assessed through competency evaluation
- [ ] Compliance reports generated monthly
- [ ] Contractor training verified before site access

## Common Pitfalls

1. **Outdated Training Matrix** — Not updating matrix when regulations or procedures change. Review annually and after regulatory changes.
2. **No Expiry Tracking** — Relying on manual reminders instead of automated system. Certifications expire unnoticed.
3. **Certificate Not Verified** — Accepting training certificates without verifying provider accreditation or certificate authenticity.
4. **No Competency Assessment** — Assuming training = competency. Always assess competency post-training.
5. **Contractor Verification Gaps** — Not verifying contractor personnel training. Verify before site access.
6. **Refresher Training Delays** — Waiting until expiry to schedule refresher. Schedule 30+ days in advance.

## Cross-References

### Related Skills
- `hse-safety-performance-monitoring` — Uses training compliance as leading indicator
- `hse-incident-investigation` — Identifies training gaps from incidents
- `hse-audit-management` — Audit verification of training compliance
- `hse-executive-reporting` — Training metrics for board briefings

### Related Agents
- `HSE Training Compliance Agent` (HSE-TRN-001) — Primary owner of this skill
- `Safety Performance Agent` (HSE-SAF-001) — Consumes training compliance data
- `HSE Executive Reporting Agent` (HSE-RPT-001) — Consumes training metrics

## Example Usage

**Scenario:** Monthly training compliance review for March 2026

1. **Training Matrix:** 12 required training types defined, matrix reviewed and current ✓
2. **Training Records:** 450 personnel on project, 5,400 training records (12 per person average)
3. **Certification Expiry:** 23 certifications expiring in next 30 days, alerts sent to personnel and managers
4. **Non-Compliance:** 3 personnel with expired confined space certification, work prohibited until recertified
5. **Competency Verification:** 45 pre-work verifications conducted, all passed ✓
6. **Training Delivery:** 18 training sessions scheduled for March, 16 completed (2 postponed due to weather)
7. **Compliance Rate:** 99.3% (3 expired out of 450 personnel)
8. **Contractor Verification:** 2 new contractors mobilized, 28 personnel verified, all compliant ✓
9. **Output:** Monthly compliance report with amber alert on 3 expired certifications, corrective action initiated (training booked for next week)

## Performance Metrics

**Target Performance:**
- Training compliance rate: 100%
- Alert response time: <24 hours (training scheduled within 24 hours of alert)
- Pre-work verification completion: 100% (all high-risk work verified)
- Competency pass rate: >90%
- Contractor verification rate: 100% (all contractor personnel verified before site access)
- Training effectiveness: <2% incident rate attributable to training deficiency
