---
title: Root Cause Analysis (RCA)
description: Systematic root cause analysis methodology for safety incidents using 5-Why, Fishbone, and Fault Tree Analysis techniques
frequency: Per safety incident requiring investigation
success_rate: 95%
tags:
  - domainforge_ai
  - safety
  - RCA-analysis
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02400_safety/agent-data/prompts/02400_AI-NATIVE-SAFETY-OPERATIONS-PROMPT.md
---

# Root Cause Analysis (RCA)

## Overview
Systematic root cause analysis for safety incidents using structured methodologies including 5-Why, Fishbone/Ishikawa diagram, and Fault Tree Analysis. Primary agent: Incident Investigation Specialist.

## Triggers
- Safety incident requiring investigation
- Recurring similar incidents identified
- High-severity incident (LTI, fatality)
- Regulatory requirement for investigation

## Prerequisites
- Incident details and initial report available
- Evidence collected and witness statements recorded
- Investigation team assembled
- Applicable investigation methodology selected

## Steps

### Step 1: Incident Description
Document the incident clearly:
- **What happened** → Sequence of events
- **Where it happened** → Location and area
- **When it happened** → Date, time, shift
- **Who was involved** → Injured persons, witnesses
- **Why it matters** → Impact (injury severity, damage, environmental)

### Step 2: Data Collection
Gather all relevant evidence:
- Photographs of the scene
- Witness statements
- Documentation (permits, training records, procedures)
- Physical evidence
- Equipment and material records

### Step 3: Causal Factor Identification
Identify all factors that contributed:
- **Direct causes** → Immediate events leading to incident
- **Contributing factors** → Conditions that enabled the incident
- **Root causes** → Systemic failures that, if corrected, would prevent recurrence

### Step 4: RCA Methodology Application
Apply selected analysis method:

**5-Why Analysis:**
- Start with the problem statement
- Ask "why" iteratively until root cause is identified
- Validate each "why" with evidence
- Typically 5 levels deep, but adjust as needed

**Fishbone/Ishikawa Analysis:**
- Create main categories: People, Methods, Materials, Equipment, Environment, Management
- Brainstorm potential causes for each category
- Analyse relationships between causes
- Identify most likely root causes

**Fault Tree Analysis:**
- Define top event (the incident)
- Identify immediate causes with AND/OR gates
- Work downward to basic events
- Calculate probabilities if data available

### Step 5: Root Cause Validation
Verify identified root causes:
- **Evidence-based** → Supported by collected evidence
- **Controllable** → Organisation can implement corrective actions
- **System-level** → Addresses systemic failure, not just symptoms
- **Recurrence prevention** → Correcting this cause prevents similar incidents

### Step 6: Corrective Action Recommendations
Generate corrective actions for each root cause:
- **Immediate actions** → Address immediate danger
- **Corrective actions** → Fix the root cause
- **Preventive actions** → Prevent recurrence across similar activities

## Success Criteria
- Root cause analysis completed within investigation timeline
- Root causes are evidence-based and systemic
- Corrective actions address identified root causes
- Analysis methodology documented and defensible

## Common Pitfalls
1. **Blaming individual** → Stopping at "worker error" without exploring system causes
2. **Insufficient evidence** → Root causes not supported by adequate evidence
3. **Too many root causes** → Over-analysis leads to diffuse corrective actions
4. **Missing contributing factors** → Focusing only on direct causes, missing systemic issues

## Cross-References
- `safety-incident-tracking/SKILL.md` — Incident tracking source
- `safety-CAPA-management/SKILL.md` — Corrective action management