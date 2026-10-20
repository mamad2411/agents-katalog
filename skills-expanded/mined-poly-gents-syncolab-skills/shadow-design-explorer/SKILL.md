---
name: shadow-design-explorer
description: "Breadth-first design exploration \u2014 many cheap concepts before commitment."
---

# Shadow Design Explorer

## Purpose

Breadth-first design exploration — many cheap concepts before commitment.

Acts as a **supervisory** lens: structured review, coaching, and decision support—not default implementation. Findings are recommendations; the user decides what to change.

## When to Use

- Breadth-first design exploration before commitment.
- Many cheap concepts needed with kill criteria up front.

## When NOT to Use

- Deep collaborative critique loop → **shadow-design-partner**.


## Expected Outcome

- Actionable review or coaching output in the skill’s standard format (below).
- Explicit boundaries: what was reviewed, what was out of scope, and what needs a follow-up skill.
- No fabricated evidence—cite files, diffs, metrics, or user-provided artifacts.

## Inputs to Gather

- Artifact under review (spec, RFC, plan, diff, retro notes, design intent).
- Stated goal, constraints, and operating mode (if scope negotiation applies).
- Related tickets, prior learnings, or incident context when relevant.

## Workflow

1. Time-box ideation; quantity before quality; label safe / bold / hybrid.
2. State kill criteria upfront (latency, cost, a11y, brand).
3. Shortlist 1–2 directions with rationale.

### Rubric and checklists

- Time-box ideation; quantity before quality
- Label concepts: safe / bold / hybrid
- Note kill criteria up front (latency, cost, a11y, brand)

Output: shortlist of 1–2 directions with rationale.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Read-only (default) | Default to **read-only** review: inspect plans, diffs, docs, and metrics; do not edit code or production systems unless the user explicitly asks. |
| Write / integrations | Persist notes or tickets only when asked; verify API results. |
| No integration | Review user-pasted content; state what live data would strengthen the pass. |

### Related tool sets

- `figma`
- `openai`

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

- Legacy rubric: `skills/old_skills.json` (`shadow-design-explorer`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
