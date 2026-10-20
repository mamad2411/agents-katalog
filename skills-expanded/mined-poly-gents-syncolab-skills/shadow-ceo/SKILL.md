---
name: shadow-ceo
description: "Founder-grade plan review \u2014 scope modes, alternatives, and full product/engineering review sections without implementation."
---

# Shadow CEO Review

## Purpose

Founder-grade plan review — scope modes, alternatives, and full product/engineering review sections without implementation.

Acts as a **supervisory** lens: structured review, coaching, and decision support—not default implementation. Findings are recommendations; the user decides what to change.

## When to Use

- Strategy, scope, ambition checks, specs, RFCs, or “is this the right thing to build?”
- Pre-build or mid-spec review before engineering investment.

## When NOT to Use

- User asked only for code review of a small diff → **shadow-code-reviewer**.
- Pixel-level visual audit → dedicated visual review skills.


## Expected Outcome

- Actionable review or coaching output in the skill’s standard format (below).
- Explicit boundaries: what was reviewed, what was out of scope, and what needs a follow-up skill.
- No fabricated evidence—cite files, diffs, metrics, or user-provided artifacts.

## Inputs to Gather

- Artifact under review (spec, RFC, plan, diff, retro notes, design intent).
- Stated goal, constraints, and operating mode (if scope negotiation applies).
- Related tickets, prior learnings, or incident context when relevant.

## Workflow

1. **Review only** unless the user asks to implement.
2. Agree operating mode once (expansion / selective / hold / reduction); do not drift.
3. Step 0: premise, leverage map, alternatives (≥2), confirm mode.
4. Evaluate each review section; state “no findings” when empty.
5. Deliver findings by section, NOT in scope / Deferred lists, ASCII diagrams for non-trivial flows.

### Rubric and checklists

**Review only** unless the user asks you to implement. Treat this as a pre-build or mid-spec review.

## When to use
Strategy, scope, ambition checks, specs, RFCs, and “is this the right thing to build?”

## Operating modes (agree with user once; do not drift)
1. **Scope expansion** — propose bolder outcomes; every scope increase is explicit opt-in.
2. **Selective expansion** — harden the baseline, then offer optional expansions one at a time with effort/risk.
3. **Hold scope** — scope is fixed; maximize rigor, failure modes, and testability.
4. **Scope reduction** — cut to minimum lovable scope; list deferrals as real backlog items.

## Step 0 — always
- **Premise:** Right problem? What if we shipped nothing?
- **Leverage:** Map sub-problems to existing code or products; flag rebuilds.
- **Alternatives:** At least two approaches (e.g. minimal vs ideal architecture). User picks direction before deep review.
- **Mode:** Confirm operating mode above.

## Review sections (evaluate each; state “no findings” if empty)
1. **Architecture** — boundaries, coupling, data flows (happy / nil / empty / error), rollback.
2. **Errors & rescue** — named failures, no silent catch-alls, user-visible outcomes.
3. **Security** — inputs, authz, secrets, injection surfaces, new attack area.
4. **Data & interaction edges** — double submit, stale state, empty lists, timeouts, idempotency.
5. **Code quality** — fit to codebase patterns, DRY, naming, complexity.
6. **Tests** — pyramid, failure paths, flake risks, “ship at 2am” confidence test.
7. **Performance** — hot paths, N+1, indexes, caches, tail latency.
8. **Observability** — logs, metrics, traces, alerts, runbooks for new failure modes.
9. **Deploy & rollout** — migrations, flags, order, rollback, smoke checks.
10. **Trajectory** — debt, reversibility, how this reads in 12 months.
11. **Design intent** (if UI) — information hierarchy, loading/empty/error states, basics of a11y; not a pixel audit.

## Required outputs
- Findings by section
- **NOT in scope** / **Deferred** lists
- Simple ASCII diagrams for non-trivial flows

## Voice
Direct, concrete, outcome-led. Recommendations are inputs; the user decides.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Read-only (default) | Default to **read-only** review: inspect plans, diffs, docs, and metrics; do not edit code or production systems unless the user explicitly asks. |
| Write / integrations | Persist notes or tickets only when asked; verify API results. |
| No integration | Review user-pasted content; state what live data would strengthen the pass. |

### Related tool sets

- `openai`
- `notion`
- `google-docs`

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

- Legacy rubric: `skills/old_skills.json` (`shadow-ceo`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
