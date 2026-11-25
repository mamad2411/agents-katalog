---
name: error-budget-management
description: Advises on SLOs, error budget burn, and release trade-offs such as feature freezes or reliability sprints. Use when balancing velocity against reliability targets.
---

# Error budget management

## Purpose

Connect product delivery decisions to SLOs and error budgets with numeric burn, remaining budget, and explicit trade-offs—not generic "be more reliable" advice.

## When to Use

- User asks about error budget, SLO burn, release freeze, or reliability vs features.
- Post-incident policy on shipping during elevated risk.
- Planning sprint focus when observability data shows fast burn.

## When NOT to Use

- Raw dashboard queries → **grafana**, **datadog**, **cloudwatch**.
- Writing the postmortem → **postmortem-authoring**.
- Defining SLO implementations from scratch → **monitor-slos**.

## Expected Outcome

- Short recommendation with SLO, burn rate, budget remaining, and suggested policy (freeze, slow down, or invest).
- Explicit tradeoffs for product and engineering leads.

## Inputs to Gather

- SLO definitions and measurement window (30d rolling, etc.).
- Current burn rate and incidents in period.
- Upcoming releases and risk profile.
- Organizational policy on exhausted budgets.

## Workflow

1. Pull SLO/error budget signals from user or observability tools.
2. State SLO target, current SLI, and budget consumed/remaining.
3. Compare burn to policy thresholds.
4. Recommend freeze, reduced risk releases, reliability sprint, or safe feature investment.
5. Document assumptions if data is incomplete.

## Domain guidance

Tie product pace to **reliability objectives**.

- State SLO and current burn; compare to budget remaining.
- If budget is exhausted or burning fast: recommend **feature freeze**, reduced risk releases, or reliability sprint.
- If budget is healthy: note where to safely re-invest (debt, features).

Output: short recommendation with numbers and explicit tradeoffs.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Use metrics/SLO tools for live burn calculations. |
| Read-only | Compute from user-supplied numbers; show formula. |
| No data | Ask for SLO, SLI, and window; do not invent burn rates. |

### Related tool sets

- `jira`
- `github`

## Review / Decision / Execution Criteria

- Numbers must be sourced or labeled as estimates.
- Recommendations proportional to burn severity.
- Align with blameless culture—policy, not blame.

## Output Format

1. SLO/SLI snapshot.
2. Budget status (remaining %, burn rate).
3. Recommendation (ship / slow / freeze / invest).
4. Tradeoffs and assumptions.

## Quality Bar

- Exec-readable in under one screen.
- Actionable policy guidance.

## Safety and Boundaries

- Do not fabricate SLO metrics.
- Do not mandate production changes without stakeholder alignment.

## Escalation / Dispatch Rules

- Metric proof → observability skills.
- Incident narrative → **postmortem-authoring**.

## References

- `skills/old_skills.json` (`error-budget-management`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
