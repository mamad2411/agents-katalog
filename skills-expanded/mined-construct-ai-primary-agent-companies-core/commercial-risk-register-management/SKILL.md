---
title: Commercial Risk Register Management
description: CRUD operations on risk register, score updates, mitigation tracking, status reporting for commercial risk management
version: 1.0
frequency_percent: 80.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-risk-register-management
gigabrain_tags: disciplines, 00250-commercial, commercial-risk-register-management, risk-management, risk-register
openstinger_context: risk-management, mitigation-tracking
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00250-commercial/agent-data/prompts/00250_AI-NATIVE-COMMERCIAL-PROMPT.md
related_skills:
  - commercial-risk-assessment
  - commercial-counterparty-risk-assessment
---

# Commercial Risk Register Management

## Overview

Manage the commercial risk register through CRUD operations on risks, score updates, mitigation tracking, and status reporting.

**Announce at start:** "I'm using the commercial-risk-register-management skill to update the risk register."

## When to Use This Skill

**Trigger Conditions:**
- New risk identified from risk assessment
- Risk score needs updating
- Mitigation action completed or overdue
- Periodic risk register update
- Risk close-out required

**Prerequisites:**
- Risk assessment completed with risk identified
- Risk owner assigned
- Risk register initialized

## Step-by-Step Procedure

### Step 1: Risk Entry

For each new risk:
1. Generate unique Risk ID
2. Record risk description
3. Assign risk category
4. Assign risk owner
5. Record date identified

### Step 2: Score Update

1. Update likelihood score (1-5)
2. Update impact score (1-5)
3. Calculate risk score (L × I)
4. Update risk rating (Low/Medium/High/Critical)

### Step 3: Mitigation Tracking

1. Record mitigation action description
2. Record mitigation strategy (avoid/reduce/transfer/accept)
3. Record mitigation owner
4. Record target completion date
5. Track mitigation status (not started/in-progress/completed/overdue)

### Step 4: Escalation

1. Identify overdue mitigations (past target date)
2. Escalate to risk owner's manager
3. Record escalation action taken
4. Set new target date

### Step 5: Risk Review

1. Schedule periodic risk reviews
2. Assess if risk still exists
3. Update likelihood and impact scores
4. Update mitigation status
5. Close risk if no longer applicable

### Step 6: Reporting

Generate risk register report:
- Risk summary by category
- Top 10 risks by score
- Overdue mitigations list
- Risk score trend analysis
- Risk closure summary

## Success Criteria

- [ ] All risks logged with unique IDs
- [ ] Risk scores current and calculated correctly
- [ ] Mitigation owners assigned for all risks
- [ ] Overdue mitigations escalated
- [ ] Periodic reviews conducted
- [ ] Risk register report generated

## Common Pitfalls

1. **Stale Data** — Risk register not updated regularly becomes useless. Update at least monthly.
2. **No Mitigation Owner** — Without an owner, mitigation doesn't happen. Always assign.
3. **Escalation Ignored** — If escalation doesn't trigger action, escalate further.

## Cross-References
### Related Skills
- `commercial-risk-assessment` — Risk identification and scoring
- `commercial-counterparty-risk-assessment` — Counterparty risk input
### Related Agents
- `COM-011` Commercial Risk Register Agent — Primary agent
- `COM-001` Commercial Coordinator Agent — Supporting agent
