# Sprint Technical Health

## Purpose
Monitors technical signals during the sprint and surfaces findings to PM for sprint health decisions.

## Role
Tech Lead (provides signal) + PM (acts on signal)

## Phase
Development

## Triggered By
Daily monitoring throughout sprint.

## Inputs
- Active PRs and kanban cards for the sprint

## Process
1. Daily: scan all active PRs and kanban cards for sprint.
2. Identify any stalled, blocked, or concerning items.
3. For each finding: document clearly (what is stalled, why, what is needed).
4. Surface to PM immediately (do not wait for daily standup).
5. PM decides: adjust scope, re-sequence, or escalate.

### Signals Tech Lead Monitors
- Stalled PRs: PR in review > 24 hours without action
- Blocked complexity: task proving more complex than estimated (sprint at risk)
- Broken dependency chains: story B waiting on story A that is blocked
- Convention drift: multiple PRs showing same convention violation pattern
- Schema drift: `packages/api/src/generated/` not regenerated after schema change
- Missing test coverage: PRs regularly failing coverage gate

### PM Acts On Signals
- Scope adjustment (remove a story if capacity at risk)
- Re-sequencing tasks (unblock critical path)
- Escalation to Edward (if resolution needs a decision)

## Outputs
Daily technical health findings surfaced to PM.

## Quality Gates
- [ ] Daily monitoring performed
- [ ] PM notified of technical signals same day
- [ ] Findings documented specifically (not just "things are slow")

## References
- `.claude/skills/pm/kanban-board-management/SKILL.md`
- `.claude/skills/shared/escalation-to-owner/SKILL.md`
