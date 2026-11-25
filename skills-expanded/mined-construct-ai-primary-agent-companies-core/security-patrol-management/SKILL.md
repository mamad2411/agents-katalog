---
title: Security Patrol Management
description: Planning, scheduling, GPS tracking, and checkpoint verification for security patrols across the site
frequency: Per patrol schedule or patrol request
success_rate: 98%
tags:
  - domainforge_ai
  - security
  - patrol-management
  - 02500_security
docs:
  - docs_construct_ai/disciplines/02500_security/agent-data/domain-knowledge/02500_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02500_security/agent-data/prompts/02500_AI-NATIVE-SECURITY-OPERATIONS-PROMPT.md
---

# Security Patrol Management

## Overview
End-to-end management of security patrols including planning, scheduling, GPS tracking, checkpoint verification, and patrol exception handling. Primary agent: SEC-PATROL-001.

## Triggers
- Patrol schedule activated
- Patrol route change required
- Checkpoint missed or delayed
- Patrol exception reported

## Steps
1. **Patrol Planning** → Define patrol route, frequency, and checkpoint sequence
2. **Schedule Generation** → Assign patrol officers to patrol times
3. **GPS Tracking** → Monitor patrol officer location against planned route
4. **Checkpoint Verification** → Record time and evidence at each checkpoint
5. **Exception Handling** → Alert for missed checkpoints, delays, or deviations

## Success Criteria
- All scheduled patrols executed
- GPS tracking active throughout patrol
- All checkpoints verified with timestamps
- Patrol exceptions generate alerts for management review

## Common Pitfalls
1. Patrol route not optimal → Missing blind spots or high-risk areas
2. GPS signal issues → Checkpoints not recorded reliably
3. No evidence at checkpoints → Photo or note evidence required

## Cross-References
- `security-alert-system/SKILL.md` — Patrol exception alerts
- `security-incident-management/SKILL.md` — Incidents identified during patrol