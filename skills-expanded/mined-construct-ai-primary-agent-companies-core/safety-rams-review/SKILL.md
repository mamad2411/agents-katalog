---
title: RAMS Review
description: Systematic review and assessment of Risk Assessment Method Statements (RAMS) documents for adequacy, completeness, and compliance with safety standards
frequency: Per RAMS submission
success_rate: 95%
tags:
  - domainforge_ai
  - safety
  - RAMS-review
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02400_safety/agent-data/prompts/02400_AI-NATIVE-SAFETY-OPERATIONS-PROMPT.md
---

# RAMS Review

## Overview
Systematic review and assessment of Risk Assessment Method Statements (RAMS) documents for adequacy, completeness, and compliance with organisational and regulatory safety standards. Primary agent: RAMS Review Specialist.

## Triggers
- New RAMS submitted for approval
- RAMS revision following changes to work method
- Periodic RAMS review scheduled
- Safety incident triggers RAMS reassessment

## Prerequisites
- RAMS document submitted
- Work scope and method statement available
- Applicable safety regulations and standards
- Historical RAMS data for similar activities

## Steps

### Step 1: RAMS Completeness Check
Verify all required sections are present:
- **Work activity description** → Clear scope and location
- **Task breakdown** → Individual steps identified
- **Hazard identification** → All relevant hazards listed per task
- **Risk assessment** → Likelihood × severity ratings provided
- **Control measures** → Hierarchy of controls applied for each hazard
- **Residual risk assessment** → Risk after controls applied
- **Competence requirements** → Personnel qualifications identified
- **Emergency arrangements** → Emergency response specified

### Step 2: Hazard Identification Validation
Cross-check hazard identification:
- Compare with historical hazards for similar activities
- Verify all task steps have associated hazards
- Check for missing environmental hazards
- Review adjacent activity conflicts

### Step 3: Risk Rating Review
Validate risk ratings for each hazard:
- **Likelihood rating** → Based on frequency of occurrence and controls
- **Severity rating** → Based on potential harm (injury, fatality, damage)
- **Residual risk** → Reduced risk after controls applied
- **Risk matrix consistency** → Ratings match organisational risk matrix

### Step 4: Control Measures Assessment
Verify control measures for each hazard:
- **Adequacy** → Controls sufficient to reduce risk to acceptable level
- **Specificity** → Controls specific to identified hazard
- **Hierarchy of controls applied** → Elimination → Substitution → Engineering → Administrative → PPE
- **Residual risk acceptable** → Final risk within organisational tolerance

### Step 5: Review Outcome & Approval
Document review findings:
- **Approve** → RAMS meets all requirements
- **Approve with conditions** → Minor improvements required
- **Reject** → Significant deficiencies requiring resubmission
- Provide feedback on deficiencies
- Record review decision with rationale

## Success Criteria
- All required sections present and adequately completed
- Risk ratings consistently applied
- Control measures reduce risks to acceptable levels
- Review decision documented with rationale

## Common Pitfalls
1. **Insufficient task breakdown** → Tasks too general, hazards missed
2. **Overly conservative risk ratings** → Inflates risk, wastes control resources
3. **Missing control verification** → Controls not linked to specific hazards
4. **Stale RAMS** → Historical RAMS not updated for current conditions

## Cross-References
- `safety-document-generation/SKILL.md` — Document generation source
- `safety/hazard-identification/SKILL.md` — Hazard identification validation