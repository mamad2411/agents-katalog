---
title: Commercial Obligation Tracking
description: Monitor and track contractual obligations throughout the contract lifecycle with compliance verification and deadline management
version: 1.0
frequency_percent: 75.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-obligation-tracking
gigabrain_tags: disciplines, 00250-commercial, commercial-obligation-tracking, contract-management
openstinger_context: obligation-management, contract-compliance
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
related_skills:
  - commercial-clause-extraction
  - commercial-compliance-monitoring
---

# Commercial Obligation Tracking

## Overview

Monitor and track all contractual obligations throughout the contract lifecycle, ensuring compliance, managing deadlines, and generating obligation status reports.

**Announce at start:** "I'm using the commercial-obligation-tracking skill to monitor contract obligations."

## When to Use This Skill

**Trigger Conditions:**
- New contract executed requiring obligation registry
- Obligation deadline approaching
- Contract amendment adding/modifying obligations
- Compliance review required
- Contract close-out requiring obligation verification

**Prerequisites:**
- Contract clauses extracted and obligations identified
- Obligation register initialized
- Responsible parties assigned

## Step-by-Step Procedure

### Step 1: Obligation Registry Entry

For each identified obligation, create register entry:
- Obligation ID (unique identifier)
- Source clause reference
- Obligation description
- Obligation type (payment, performance, notice, compliance)
- Responsible party
- Due date / Trigger event
- Status (open, in-progress, completed, overdue)
- Evidence of compliance
- Notes

### Step 2: Deadline Management

1. Calculate upcoming obligation deadlines
2. Generate reminder notifications at defined intervals:
   - 30-day advance notice
   - 14-day advance notice
   - 7-day advance notice
   - 3-day critical notice
3. Track responses to notifications
4. Escalate unfulfilled obligations

### Step 3: Compliance Verification

For each obligation:
1. Verify required action was performed
2. Verify deadline was met
3. Gather evidence of compliance
4. Update obligation status
5. Flag non-compliance with root cause

### Step 4: Obligation Change Management

When contract amendment modifies obligations:
1. Identify affected obligations
2. Update obligation entries with amendment reference
3. Calculate revised deadlines
4. Notify responsible parties
5. Update compliance schedule

### Step 5: Reporting

Generate obligation status reports:
- Summary: Total opened, completed, overdue, open
- Critical: Overdue obligations with root cause analysis
- Upcoming: Obligations due within next 30 days
- Compliance Rate: Percentage of obligations fulfilled on time

## Success Criteria

- [ ] All obligations extracted and entered in register
- [ ] Each obligation has responsible party assigned
- [ ] Deadline notifications generated on schedule
- [ ] Compliance evidence gathered for completed obligations
- [ ] Overdue obligations flagged with escalation
- [ ] Status reports generated and distributed

## Common Pitfalls

1. **Missing Subtler Obligations** — Obligations hidden in non-obvious clauses (e.g., notice obligations in dispute clauses). Review all clauses thoroughly.
2. **No Evidence** — Obligation fulfilled but not documented. Always require evidence of compliance.
3. **Unassigned Obligations** — Obligation without a responsible party will slip. Always assign ownership.
4. **No Deadline** — Obligations without deadlines become open-ended. Always define a trigger or deadline.

## Cross-References

### Related Skills
- `commercial-clause-extraction` — Source obligation extraction
- `commercial-compliance-monitoring` — Compliance verification

### Related Agents
- `COM-002` Commercial Contract Administrator Agent — Primary agent
- `COM-010` Commercial Compliance Monitoring Agent — Supporting agent