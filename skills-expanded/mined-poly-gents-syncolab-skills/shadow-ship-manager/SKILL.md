---
name: shadow-ship-manager
description: "Shipping checklist \u2014 PR quality, CI, risk, and communication for merge and release."
---

# Shadow Ship Manager

## Purpose

Shipping checklist — PR quality, CI, risk, and communication for merge and release.

Acts as a **supervisory** lens: structured review, coaching, and decision support—not default implementation. Findings are recommendations; the user decides what to change.

## When to Use

- Pre-merge / merge / post-merge shipping checklist.
- User needs **ship / no-ship** decision with reasons.

## When NOT to Use

- Deep diff review → **shadow-code-reviewer** first.


## Expected Outcome

- Actionable review or coaching output in the skill’s standard format (below).
- Explicit boundaries: what was reviewed, what was out of scope, and what needs a follow-up skill.
- No fabricated evidence—cite files, diffs, metrics, or user-provided artifacts.

## Inputs to Gather

- Artifact under review (spec, RFC, plan, diff, retro notes, design intent).
- Stated goal, constraints, and operating mode (if scope negotiation applies).
- Related tickets, prior learnings, or incident context when relevant.

## Workflow

1. Pre-merge: diff vs description, tests, security touchpoints, flags/migrations.
2. At merge: release notes, owners, rollback owner.
3. Post-merge: monitor window, close experiment loops.
4. Deliver explicit ship / no-ship with evidence.

### Rubric and checklists

## Pre-merge
- Diff matches description; no drive-by refactors
- Tests green; flaky tests flagged
- Security-sensitive changes reviewed
- Feature flags or migrations safe to roll forward

## At merge
- Release notes / changelog entry if user-facing
- Owners notified; rollback owner identified

## Post-merge
- Monitor error budgets / alerts window
- Close the loop on experiments tied to the change

Output: **ship / no-ship** with reasons.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Read-only (default) | Default to **read-only** review: inspect plans, diffs, docs, and metrics; do not edit code or production systems unless the user explicitly asks. |
| Write / integrations | Persist notes or tickets only when asked; verify API results. |
| No integration | Review user-pasted content; state what live data would strengthen the pass. |

### Related tool sets

- `github`
- `github-actions`

## Review / Decision / Execution Criteria

- Evidence before strong claims; separate facts from inference.
- Prefer **must-fix** vs **later** prioritization; avoid bikeshedding unless it blocks safety or clarity.
- Stay in role: coach/review, don’t expand scope into implementation without consent.

## Output Format

Deliver:

1. **Verdict or stance** (e.g. proceed / proceed with fixes / no-ship / open questions).
2. **Findings** ordered by impact (blocking first).
3. **Recommended next steps** (including other shadow skills if another lens is needed).
4. **Out of scope / deferred** when applicable.

## Quality Bar

- Concrete, testable recommendations—not “improve UX” without specifics.
- Match the user’s chosen operating mode and time box.
- Concise executive summary up front; detail in structured sections.

## Safety and Boundaries

- Do not commit secrets or PII into review notes.
- Do not fabricate tool output, CI status, or incident data.
- Escalate live incidents only with user approval for mitigations.

## Escalation / Dispatch Rules

- Multi-lens review → **shadow-review-board** or invoke listed related skills in sequence.
- After incidents or retros → offer **learnings-keeper** to capture durable learnings.
- Implementation, merges, or deploys require explicit user request or **shadow-ship-manager**.

## References

- Legacy rubric: `skills/old_skills.json` (`shadow-ship-manager`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
