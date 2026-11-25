---
title: Security Incident Management
description: End-to-end management of security incidents from initial report through investigation, evidence collection, resolution, and lessons learned
frequency: Per security incident
success_rate: 98%
tags:
  - domainforge_ai
  - security
  - incident-management
  - 02500_security
docs:
  - docs_construct_ai/disciplines/02500_security/agent-data/domain-knowledge/02500_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02500_security/agent-data/prompts/02500_AI-NATIVE-SECURITY-OPERATIONS-PROMPT.md
---

# Security Incident Management

## Overview
End-to-end management of security incidents including initial report, severity classification, investigation coordination, resolution, and lessons learned. Primary agent: SEC-INCIDENT-001.

## Triggers
- Security breach detected
- Unauthorized access attempt
- Property theft or damage reported
- Safety incident with security implications
- Emergency situation requiring security response

## Steps
1. **Incident Registration** → Log initial report with who/what/where/when
2. **Severity Classification** → Classify as Low, Medium, High, or Critical based on impact
3. **Immediate Response** → Assign security resources based on severity
4. **Investigation Coordination** → Gather evidence, interview witnesses, review CCTV
5. **Resolution** → Determine root cause, assign corrective actions
6. **Closure & Lessons Learned** → Document outcomes and share with security team

## Success Criteria
- Incidents registered within required timeframe
- Severity classification consistent and accurate
- Investigation completed within SLA
- All incidents closed with documented outcomes

## Common Pitfalls
1. Delayed reporting → Incidents not reported immediately
2. Inconsistent severity classification → Similar incidents rated differently
3. Missing evidence → Evidence not preserved promptly
4. No lessons learned → Repeat incidents from unaddressed root causes

## Cross-References
- `security-alert-system/SKILL.md` — Alert generation for incidents
- `security-surveillance/SKILL.md` — CCTV evidence for investigations