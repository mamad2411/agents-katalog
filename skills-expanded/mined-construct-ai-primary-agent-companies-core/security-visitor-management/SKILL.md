---
title: Security Visitor Management
description: End-to-end management of visitor pre-registration, on-site verification, badge printing, and escort tracking
frequency: Per visitor arrival
success_rate: 99%
tags:
  - domainforge_ai
  - security
  - visitor-management
  - 02500_security
docs:
  - docs_construct_ai/disciplines/02500_security/agent-data/domain-knowledge/02500_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02500_security/agent-data/prompts/02500_AI-NATIVE-SECURITY-OPERATIONS-PROMPT.md
---

# Security Visitor Management

## Overview
End-to-end management of visitors including pre-registration, on-site verification, badge printing, escort assignment, and departure tracking. Primary agent: SEC-VISITOR-001.

## Triggers
- Visitor pre-registration submitted
- Visitor arrives on site
- Visitor requests access to restricted zone
- Visitor departs
- Visitor overstay detected

## Steps
1. **Pre-registration** → Receive visitor details from requestor, validate
2. **On-site Verification** → Verify identity against pre-registration, check ID documents
3. **Badge Printing** → Issue visitor badge with access restrictions
4. **Escort Assignment** → Assign escort where required for restricted zones
5. **Tracking & Departure** → Track visitor location, badge returned at departure, log departure time

## Success Criteria
- All visitors pre-registered before arrival or registered on arrival
- Identity verified against valid identification
- Badge printed with correct access restrictions
- Visitor departed logged with badge returned
- Escort tracked where required

## Common Pitfalls
1. Visitors arriving without pre-registration → Allow on-site registration with longer processing
2. Badge not returned → Track departures, follow up for missing badges
3. Overstaying → Monitor visitor duration, alert for overstay

## Cross-References
- `security-access-control/SKILL.md` — Visitor access authorization
- `security-incident-management/SKILL.md` — Visitor incidents