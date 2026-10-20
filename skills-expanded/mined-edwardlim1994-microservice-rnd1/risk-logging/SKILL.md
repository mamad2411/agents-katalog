# Risk Logging

## Purpose
Captures any identified risk in structured tracked format so nothing falls through the cracks between phases or roles.

## Role
Shared — any role, any time

## Phase
Cross-phase

## Triggered By
Any role identifies a condition that could negatively impact sprint, release, or system quality.

## Inputs
- Risk description and context from the identifying role

## Process

### Risk Score Matrix

| Probability | High Impact  | Med Impact | Low Impact |
|-------------|--------------|------------|------------|
| High        | 9 (Critical) | 6 (High)   | 3 (Low)    |
| Medium      | 6 (High)     | 4 (Medium) | 2 (Low)    |
| Low         | 3 (Low)      | 2 (Low)    | 1 (Low)    |

### Thresholds
- 7-9: Critical → escalate to Edward immediately
- 4-6: High → PM aware, mitigation plan required
- 1-3: Low → logged, monitored, reviewed at retrospective

### Steps
1. Identify risk immediately (do not defer).
2. Document structured risk entry.
3. Calculate risk score.
4. Create kanban card: `type: risk`, priority based on score.
5. Commit to OpenSpec risks folder.
6. Trigger escalation if score 7-9.
7. Notify PM if score 4-6.
8. Monitor and update throughout sprint.

## Outputs
Location: `openspec/changes/{slug}/risks/risk-{ID}.md`

```
# Risk Log — {Risk-ID}
# Identified by: {role} | Date: {date} | Story: KAN-{N}

## Risk Description
## Category: Technical|Security|Compliance|Timeline|Dependency|Infrastructure|Business
## Probability: High|Medium|Low
## Impact: High|Medium|Low
## Risk Score: {N}
## Mitigation Strategy
## Contingency Plan
## Owner: {role}
## Status: Open|Mitigating|Resolved|Accepted
## Review Date: {date}
```

## Quality Gates
- [ ] Risk documented immediately (not deferred)
- [ ] Score calculated correctly
- [ ] Appropriate escalation triggered
- [ ] Owner assigned
- [ ] Review date set

## References
- `.claude/skills/shared/escalation-to-owner/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
