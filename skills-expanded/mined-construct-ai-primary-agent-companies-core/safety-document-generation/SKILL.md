---
title: Safety Document Generation
description: Automated generation of safety documentation including Safety Reports, RAMS, HIRA, and compliance certificates for the ConstructAI HSE system
frequency: Per safety event or project milestone
success_rate: 95%
tags:
  - domainforge_ai
  - safety
  - document-generation
  - 02400_safety
docs:
  - docs_construct_ai/disciplines/02400_safety/agent-data/domain-knowledge/02400_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02400_safety/agent-data/prompts/02400_AI-NATIVE-SAFETY-OPERATIONS-PROMPT.md
---

# Safety Document Generation

## Overview
Automated generation of comprehensive safety documentation from structured data sources. Covers Safety Reports, RAMS (Risk Assessment Method Statements), HIRA (Hazard Identification Risk Assessment), JSA, and compliance certificates. Primary agent: HSE Safety Manager.

## Triggers
- Project milestone achieved
- Safety event requiring investigation
- Permit application submitted
- Contractor onboarding
- Scheduled safety review

## Prerequisites
- Access to safety data repository
- Project scope and work method documents
- Applicable safety regulations and standards
- Historical safety documentation templates

## Steps

### Step 1: Document Type Identification
Determine document type from trigger context:
- **Safety Report** → General incident or safety concern
- **RAMS** → Work method requiring risk assessment
- **HIRA** → Hazard identification for new activity
- **JSA** → Task-level job safety analysis
- **Compliance Certificate** → Regulatory requirement verification

### Step 2: Data Collection
Gather required structured data:
- Project identification (name, number, location)
- Work scope description
- Identified hazards and risks
- Control measures and mitigation strategies
- Responsible personnel
- Applicable regulations

### Step 3: Template Selection
Select appropriate template from template registry:
- Match document type to template
- Verify template currency and completeness
- Load template with document metadata

### Step 4: Structured Data Injection
Inject collected data into template:
- Map data fields to template placeholders
- Apply conditional logic for optional sections
- Include hazard-specific control measures
- Insert regulatory references

### Step 5: Quality Validation
Validate generated document against requirements:
- **Completeness check** → All required sections present and populated
- **Regulatory compliance** → References match current standards
- **Risk assessment linkage** → All hazards linked to appropriate controls
- **Personnel sign-off** → Include all required signature fields

### Step 6: Output & Filing
Generate final document:
- Save to document repository
- Apply document numbering convention
- Distribute to stakeholders
- Log in document control register

## Success Criteria
- Document contains all required sections with populated data
- Risk assessments link to control measures
- Regulatory references are current
- Document filed correctly

## Common Pitfalls
1. **Missing hazard-control links** → Ensure each identified hazard has corresponding control measures
2. **Stale regulatory references** → Maintain currency of safety standards database
3. **Incomplete personnel data** → Verify all responsible persons are identified before generation

## Cross-References
- `safety/RAMS-review/SKILL.md` — Document review process
- `safety/hazard-identification/SKILL.md` — Hazard data source