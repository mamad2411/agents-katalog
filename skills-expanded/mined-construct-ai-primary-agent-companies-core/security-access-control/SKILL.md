---
title: Security Access Control
description: Management of access control including badge scanning, authorization checking, entry/exit logging for the ConstructAI security system
frequency: Per access event
success_rate: 99%
tags:
  - domainforge_ai
  - security
  - access-control
  - 02500_security
docs:
  - docs_construct_ai/disciplines/02500_security/agent-data/domain-knowledge/02500_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02500_security/agent-data/prompts/02500_AI-NATIVE-SECURITY-OPERATIONS-PROMPT.md
---

# Security Access Control

## Overview
End-to-end management of access control including badge scanning, authorization checking, entry/exit logging, and access point management. Primary agent: SEC-ACCESS-001.

## Triggers
- Badge scan at access point
- Tailgating detection
- Unauthorized access attempt
- Access request submitted
- Access revocation required

## Steps
1. **Badge Scanning** → Read badge data and validate authenticity
2. **Authorization Checking** → Verify person has valid access rights for the zone and time
3. **Entry/Exit Logging** → Record timestamp, location, and person details
4. **Access Decision** → Grant or deny based on authorization check
5. **Alert Generation** → Trigger alert for unauthorized attempts or invalid badges

## Success Criteria
- All access attempts logged
- Valid badges processed within 2 seconds
- Unauthorized attempts generate immediate alerts
- Entry/exit records complete and auditable

## Common Pitfalls
1. Badge reader connectivity issues → Ensure reliable connection
2. Invalid badges from expired personnel → Regular badge audit
3. Tailgating not detected → Complement with camera monitoring

## Cross-References
- `security-visitor-management/SKILL.md` — Visitor access
- `security-surveillance/SKILL.md` — CCTV monitoring of access points