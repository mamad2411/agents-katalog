---
title: Pre-Award Tender Specification
description: Tender specification generation from procurement requirements with compliance validation and template management
frequency: Per tender requirement
success_rate: 95%
tags:
  - domainforge_ai
  - pre-award
  - tender-specification
  - 00425_contracts-pre-award
docs:
  - docs_construct_ai/disciplines/00425_contracts-pre-award/agent-data/domain-knowledge/00425_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00425_contracts-pre-award/agent-data/prompts/00425_AI-NATIVE-CONTRACTS-PRE-AWARD-PROMPT.md
---

# Pre-Award Tender Specification

## Overview
Automated generation of tender specifications from procurement requirements including scope definition, technical requirements, evaluation criteria, and delivery terms. Primary agent: 00425-001 Tender Specification Agent.

## Triggers
- Procurement requirement received
- New tender initiated
- Tender specification modification requested

## Steps
1. **Requirements Analysis** → Extract scope, technical requirements, delivery terms from input data
2. **Template Selection** → Select appropriate tender template based on procurement type (RFP, RFQ, ITT)
3. **Specification Drafting** → Generate tender specification with scope, technical requirements, evaluation criteria, BOQ, delivery schedules
4. **Compliance Validation** → Validate against procurement regulations and organizational standards
5. **Review & Publication Routing** → Route to tender committee for review and approval

## Success Criteria
- Tender specification covers all requirements
- Evaluation criteria aligned with procurement type
- Procurement compliance validated
- Specification ready for publication workflow

## Cross-References
- `pre-award-tender-publication/SKILL.md` — Publication routing
- `pre-award-evaluation-analysis/SKILL.md` — Evaluation criteria input