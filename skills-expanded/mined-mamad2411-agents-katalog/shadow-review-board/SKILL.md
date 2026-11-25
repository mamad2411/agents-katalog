---
name: shadow-review-board
description: "Orchestrates a staged review \u2014 strategy, design intent, engineering, and DX \u2014 with merged findings."
---

# Shadow Review Board

## Purpose

Orchestrates a staged review — strategy, design intent, engineering, and DX — with merged findings.

Acts as a **supervisory** lens: structured review, coaching, and decision support—not default implementation. Findings are recommendations; the user decides what to change.

## When to Use

- Staged multi-lens review (strategy, design, engineering, DX) with merged backlog.
- Time-boxed breadth-first must-fix pass across disciplines.

## When NOT to Use

- Single-domain deep dive only—use the specific shadow skill instead.


## Expected Outcome

- Actionable review or coaching output in the skill’s standard format (below).
- Explicit boundaries: what was reviewed, what was out of scope, and what needs a follow-up skill.
- No fabricated evidence—cite files, diffs, metrics, or user-provided artifacts.

## Inputs to Gather

- Artifact under review (spec, RFC, plan, diff, retro notes, design intent).
- Stated goal, constraints, and operating mode (if scope negotiation applies).
- Related tickets, prior learnings, or incident context when relevant.

## Workflow

1. Run lenses in order: CEO → design critic → engineering lead → devex lead.
2. Pass artifacts forward; dedupe findings at merge step.
3. Produce consolidated report and ordered backlog: must-fix, should-fix, later.
4. If time-boxed, breadth-first on **must-fix** only.

### Rubric and checklists

Run reviews **in order**, passing forward artifacts:

1. **Strategy / CEO lens** — problem, scope mode, alternatives (Shadow CEO rubric).
2. **Design intent** — UX states and IA (Shadow Design Critic rubric).
3. **Engineering** — architecture, failure modes, tests (Shadow Engineering Lead rubric).
4. **DX** — onboarding and contributor friction (Shadow DX Lead rubric).

## Merge step
- Single consolidated report: conflicts resolved, duplicate findings deduped
- Single ordered backlog: must-fix, should-fix, later

If time-boxed, do breadth-first on **must-fix** items only.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Read-only (default) | Default to **read-only** review: inspect plans, diffs, docs, and metrics; do not edit code or production systems unless the user explicitly asks. |
| Write / integrations | Persist notes or tickets only when asked; verify API results. |
| No integration | Review user-pasted content; state what live data would strengthen the pass. |

### Related tool sets

- `openai`
- `notion`

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

- Legacy rubric: `skills/old_skills.json` (`shadow-review-board`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
