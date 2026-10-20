# Status Reporting

## Purpose
Structured status update readable by Edward at any point without requiring a conversation.

## Role
Shared — any role, PM coordinates

## Phase
Cross-phase

## Triggered By
Significant milestone completion, end of sprint day, Edward requests update, blocker identified, phase transition.

## Inputs
- Current kanban board state
- Prior status report (for delta)

## Process

### Status Indicators
- `BLOCKED`: cannot proceed → notify Edward immediately
- `AT_RISK`: potential issue, monitoring → include in next report
- `ON_TRACK`: proceeding as planned → routine report

### Steps
1. Collect current state from kanban board.
2. Identify completed items since last report.
3. Identify in-progress items with expected completion.
4. Identify blockers with owner and resolution path.
5. Identify emerging risks.
6. Assign status indicator.
7. Commit report to kanban card description.
8. Do NOT send unsolicited messages unless BLOCKED.

## Outputs
```
# Status Report — {Sprint/Story/Release}
# Role: {role} | Date: {date} | Status: ON_TRACK|AT_RISK|BLOCKED

## What's Done
## In Progress (with expected completion)
## Blocked (with owner + expected resolution)
## Risks (with mitigation)
## Next (actions + when)
## Metrics (role-specific where applicable)
```

## Quality Gates
- [ ] Status indicator accurately reflects reality
- [ ] Blocked items have owner and resolution path
- [ ] Report committed (pull not push)
- [ ] BLOCKED triggers immediate escalation

## References
- `.claude/skills/shared/escalation-to-owner/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
