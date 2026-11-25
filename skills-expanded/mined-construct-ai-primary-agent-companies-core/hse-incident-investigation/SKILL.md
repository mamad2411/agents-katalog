---
title: HSE Incident Investigation
description: Conduct structured incident investigations, perform root cause analysis, identify contributing factors, recommend corrective and preventive actions, and track lessons learned with evidence-based investigation methodology
version: 1.0
frequency_percent: 70.0
success_rate_percent: 91.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00885_hse-director/hse-incident-investigation
gigabrain_tags: disciplines, 00885_hse-director, incident-investigation, root-cause-analysis, contributing-factors, corrective-actions, lessons-learned
openstinger_context: hse-director, incident-analysis, investigation-methodology
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00885_hse-director/agent-data/domain-knowledge/00885_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00885_hse-director/agent-data/prompts/00885_AI-NATIVE-HSE-DIRECTOR-PROMPT.md
related_skills:
  - pre-task-assessment-readiness
  - hse-safety-performance-monitoring
  - hse-audit-management
---

# HSE Incident Investigation

## Overview

Conduct structured incident investigations using evidence-based methodology (5 Whys, Fishbone, ICAM, TapRoot), perform root cause analysis to identify underlying causes, document contributing factors, recommend corrective and preventive actions, track implementation effectiveness, and maintain lessons learned database. Thorough investigations prevent incident recurrence and drive continuous HSE improvement.

**Announce at start:** "I'm using the hse-incident-investigation skill to investigate incidents and identify root causes."

## When to Use This Skill

**Trigger Conditions:**
- New incident reported (safety or environmental)
- Investigation required per incident classification
- Pattern detection identifies similar incidents
- Repeat incident in same location or activity
- High-potential near-miss requiring investigation
- Regulatory requirement for incident investigation
- Lessons learned capture from completed investigations

**Prerequisites:**
- Incident details and initial report
- Investigation authority and team composition
- Access to incident scene and evidence
- Witness availability for interviews
- Investigation tools and templates

## Step-by-Step Procedure

### Step 1: Investigation Scope Determination

Determine investigation scope based on incident severity:

| Incident Severity | Investigation Level | Investigation Team | Timeline |
|------------------|--------------------|--------------------|----------|
| **Fatality** | Comprehensive | Senior HSE Director, external specialists, legal | 30 days, formal report to board |
| **Serious Injury (LTI)** | Detailed | HSE Director, line management, specialists | 14 days, formal report |
| **Medical Treatment** | Standard | HSE Officer, supervisor, safety representative | 7 days, internal report |
| **First Aid** | Basic | Supervisor, site HSE | 3 days, incident log |
| **High-Potential Near-Miss** | Standard | HSE Officer, supervisor | 7 days, internal report |
| **Minor Near-Miss** | Basic | Supervisor | 3 days, incident log |

**Investigation Authority:**
- Fatality/Serious: HSE Director leads or appoints investigation leader
- Standard: HSE Officer investigates with supervisor support
- Basic: Supervisor investigates with HSE Officer review

### Step 2: Evidence Collection

Collect all available evidence while scene is preserved:

**Evidence Types:**
| Evidence Type | Collection Method | Preservation |
|--------------|-------------------|--------------|
| **Physical Evidence** | Photographs, measurements, samples | Secure in evidence locker, chain of custody |
| **Documentary Evidence** | Procedures, permits, training records, maintenance logs | Copy and secure originals |
| **Witness Statements** | Interviews (individual, private, no blame) | Written statements, signed and dated |
| **Environmental Conditions** | Weather, lighting, noise levels, temperature | Record at time of incident |
| **Equipment/Tools** | Condition, calibration, maintenance status | Quarantine, inspect, photograph |
| **Timeline** | Sequence of events | Reconstruct from all sources |

**Evidence Collection Rules:**
1. **Preserve the Scene** — Do not disturb unless emergency response required
2. **Photograph Everything** — Scene, equipment, PPE, conditions (with scale reference)
3. **Interview Separately** — Prevent witness influence, maintain confidentiality
4. **No Blame Approach** — Focus on facts, not fault
5. **Chain of Custody** — Document evidence handling for legal defensibility

### Step 3: Incident Timeline Reconstruction

Reconstruct detailed timeline of events leading to incident:

**Timeline Components:**
```
NORMAL OPERATIONS (baseline)
    ↓
PRECURSOR EVENTS (early warning signs)
    ↓
IMMEDIATE CAUSES (actions or conditions directly causing incident)
    ↓
INCIDENT OCCURS
    ↓
IMMEDIATE RESPONSE (first aid, containment, notification)
    ↓
INVESTIGATION INITIATED
```

**Example Timeline:**
```
08:00 - Shift start, safety briefing conducted
08:30 - Work at height permit issued for structural steel installation
09:00 - Worker ascends to work platform
09:15 - Worker reported harness uncomfortable, removed chest strap
09:30 - Worker leans over edge to reach steel member
09:32 - Worker loses balance, falls 3 meters
09:33 - Co-worker activates emergency alarm
09:35 - First aider arrives, provides care
09:40 - Ambulance called
10:00 - Worker transported to hospital (broken arm, LTI)
```

### Step 4: Root Cause Analysis

Apply root cause analysis methodology to identify underlying causes:

**5 Whys Method:**
```
Incident: Worker fell from height
Why 1: Worker lost balance
Why 2: Worker was leaning over edge
Why 3: Steel member was out of reach
Why 4: Work platform positioning was inadequate
Why 5: Method statement did not specify platform positioning requirements

ROOT CAUSE: Inadequate method statement (did not address platform positioning)
```

**Fishbone (Ishikawa) Diagram Categories:**
| Category | Contributing Factors to Explore |
|----------|--------------------------------|
| **People** | Training, competency, fatigue, behavior, communication |
| **Procedures** | Adequacy, availability, compliance, updates |
| **Equipment** | Condition, suitability, maintenance, guarding |
| **Environment** | Weather, lighting, noise, housekeeping, access |
| **Management** | Supervision, planning, resources, safety culture |

**ICAM (Incident Cause Analysis Method) Structure:**
```
INCIDENT (what happened)
    ↓
IMMEDIATE CAUSES (unsafe acts or conditions)
    ↓
CONTRIBUTING FACTORS (why immediate causes existed)
    ↓
ROOT CAUSES (organizational/systemic issues)
    ↓
RECOMMENDATIONS (address root causes)
```

### Step 5: Contributing Factor Identification

Identify all contributing factors, not just primary root cause:

**Contributing Factor Categories:**
| Category | Examples | Control Type |
|----------|----------|--------------|
| **Individual Factors** | Lack of training, fatigue, inexperience | Training, competency, fitness for work |
| **Task Factors** | Inadequate procedures, unclear instructions | Method statements, work instructions |
| **Equipment Factors** | Equipment failure, missing guards, inadequate PPE | Maintenance, inspection, PPE provision |
| **Environmental Factors** | Poor visibility, extreme weather, confined space | Environmental controls, monitoring |
| **Organizational Factors** | Inadequate supervision, production pressure, poor safety culture | Management systems, leadership |

**Swiss Cheese Model Application:**
```
HAZARD → Defense Layer 1 (failed) → Defense Layer 2 (failed) → INCIDENT
Example:
Work at Height Hazard → Method Statement (inadequate) → Permit System (not enforced) → Supervision (absent) → FALL
```

### Step 6: Corrective and Preventive Action Recommendations

Develop corrective actions (fix immediate problem) and preventive actions (prevent recurrence):

**Action Hierarchy (most to least effective):**
| Level | Action Type | Example | Effectiveness |
|-------|------------|---------|---------------|
| **1. Elimination** | Remove hazard completely | Use ground-level assembly instead of work at height | Highest |
| **2. Substitution** | Replace with safer alternative | Use mobile elevating work platform instead of ladder | High |
| **3. Engineering Controls** | Physical barriers or guards | Install edge protection, guardrails | Moderate-High |
| **4. Administrative Controls** | Procedures, training, supervision | Enhanced method statement, increased supervision | Moderate |
| **5. PPE** | Personal protective equipment | Improved harness, better training | Lowest |

**Recommendation Template:**
```
Corrective Action 1: Update method statement to specify work platform positioning requirements
Responsible: Method Statement Author
Due Date: 7 days
Verification: HSE Officer reviews updated method statement

Preventive Action 1: Conduct method statement review of all work at height activities
Responsible: HSE Manager
Due Date: 30 days
Verification: HSE Director approves review findings

Preventive Action 2: Implement mandatory toolbox talk on platform positioning before each shift
Responsible: Site Supervisors
Due Date: Immediate
Verification: Supervisor sign-off on toolbox talk records
```

### Step 7: Similar Incident Pattern Detection

Search historical incidents for similar patterns:

**Pattern Matching Criteria:**
- Same location or work area
- Same activity type
- Same equipment or tools
- Same contractor or crew
- Same root cause category

**Pattern Detection Algorithm:**
```
FOR each current_incident_attribute:
    SEARCH historical_incidents for matching attribute
    IF matches > 2 within 12 months THEN
        FLAG as PATTERN
        ESCALATE to HSE Director
        REQUIRE systemic investigation
    END IF
END FOR
```

**Example:**
```
Current Incident: Fall from height - structural zone
Historical Search Results:
- 2025-11-12: Fall from height - structural zone (near-miss)
- 2025-09-03: Fall from height - structural zone (medical treatment)
- 2025-06-22: Fall from height - structural zone (LTI)

PATTERN DETECTED: Structural zone work at height (4 incidents in 9 months)
Action: Systemic investigation required, stop work at height in structural zone until controls reviewed
```

### Step 8: Lessons Learned Documentation

Capture and disseminate lessons learned from investigations:

**Lessons Learned Components:**
| Component | Content |
|-----------|---------|
| **Incident Summary** | Brief description of what happened |
| **Root Cause** | Primary root cause identified |
| **Contributing Factors** | Key contributing factors |
| **What Went Wrong** | Critical failures in defense layers |
| **What Went Right** | Effective controls or responses (if any) |
| **Key Lessons** | 3-5 key takeaways |
| **Recommendations** | Actions to prevent recurrence |
| **Applicability** | Where else might this lesson apply? |

**Dissemination Methods:**
- Safety alerts (immediate, critical incidents)
- Toolbox talks (site-level communication)
- Management meetings (strategic lessons)
- Lessons learned database (searchable repository)
- Industry sharing (anonymized, high-value lessons)

### Step 9: Investigation Quality Assurance

Verify investigation quality before closure:

**Quality Checklist:**
- [ ] All witnesses interviewed
- [ ] All evidence collected and preserved
- [ ] Timeline reconstructed and verified
- [ ] Root cause analysis methodology applied correctly
- [ ] Contributing factors comprehensively identified
- [ ] Recommendations address root causes (not just symptoms)
- [ ] Action hierarchy applied (elimination/substitution preferred)
- [ ] Similar incident patterns searched
- [ ] Lessons learned documented
- [ ] Investigation report peer-reviewed
- [ ] HSE Director approval obtained

**Investigation Report Rejection Reasons:**
- Superficial analysis (stopped at immediate cause, did not reach root cause)
- Incomplete evidence collection
- Blame-focused (individual fault) rather than system-focused
- Recommendations address symptoms only
- No consideration of action hierarchy

## Success Criteria

- [ ] Investigation scope determined per incident severity
- [ ] All evidence collected and preserved with chain of custody
- [ ] Incident timeline reconstructed and verified
- [ ] Root cause analysis completed using structured methodology
- [ ] Contributing factors comprehensively identified
- [ ] Corrective and preventive actions recommended using action hierarchy
- [ ] Similar incident patterns detected and escalated
- [ ] Lessons learned documented and disseminated
- [ ] Investigation quality assured and approved

## Common Pitfalls

1. **Stopping at Immediate Cause** — Identifying "worker error" as root cause. Always ask "Why did the worker make that error?" to reach systemic causes.
2. **Blame Focus** — Focusing on individual fault rather than system failures. Use no-blame approach to encourage openness.
3. **Delayed Investigation** — Waiting days or weeks to start investigation. Evidence degrades, memories fade. Initiate immediately.
4. **Inadequate Evidence** — Not collecting sufficient evidence to support conclusions. Photograph everything, interview all witnesses.
5. **Symptom Treatment** — Recommending training or discipline without addressing underlying system weaknesses.
6. **Missing Similar Incidents** — Not searching for patterns. Historical data reveals systemic issues.

## Cross-References

### Related Skills
- `hse-safety-performance-monitoring` — Uses root cause data for trend analysis
- `hse-audit-management` — Audit findings may require investigation
- `hse-training-compliance` — Training gaps identified from investigations
- `hse-executive-reporting` — Major investigations reported to board

### Related Agents
- `Incident Investigation Agent` (HSE-INC-001) — Primary owner of this skill
- `Safety Performance Agent` (HSE-SAF-001) — Consumes root cause data
- `HSE Audit Agent` (HSE-AUD-001) — Tracks corrective action implementation

## Example Usage

**Scenario:** Lost Time Injury investigation - fall from height

1. **Scope:** LTI = Detailed investigation, 14-day timeline, HSE Director leads
2. **Evidence:** Scene photos, harness inspection, permit review, witness interviews (3 workers, 1 supervisor)
3. **Timeline:** Reconstructed from 08:00 shift start to 10:00 hospital transport
4. **Root Cause (5 Whys):** Method statement did not specify platform positioning requirements
5. **Contributing Factors:** Inadequate supervision, worker removed harness chest strap (discomfort), production pressure
6. **Corrective Actions:** Update method statement (7 days), retrain all workers on harness use (immediate)
7. **Preventive Actions:** Method statement review for all work at height (30 days), increase supervisor presence (immediate)
8. **Similar Incidents:** 3 similar falls in structural zone in past 9 months — pattern detected, systemic investigation escalated
9. **Lessons Learned:** Platform positioning critical for work at height, harness comfort affects compliance, supervision gaps in high-activity periods
10. **Output:** Investigation report approved by HSE Director, safety alert issued, toolbox talks conducted, systemic review initiated

## Performance Metrics

**Target Performance:**
- Investigation initiation time: <24 hours from incident
- Investigation completion time: Per severity (3-30 days)
- Root cause identification rate: 100% (all investigations reach root cause, not just immediate cause)
- Corrective action implementation: >90% within due date
- Repeat incident rate: <5% (same root cause within 12 months)
- Investigation quality score: >85% (peer review assessment)
