---
name: ab-experimentation
description: Plans and interprets A/B tests with clear hypotheses, primary metrics, guardrails, and statistical conclusions. Use when designing, analyzing, or stopping controlled experiments.
---

# A/B experimentation

## Purpose

Help design and interpret controlled experiments: hypothesis, primary metric, guardrails, sample size/runtime, and statistically sound conclusions—avoiding peeking bias and vague "try again" advice.

## When to Use

- User asks for A/B test design, analysis, or whether to ship variant B.
- Choosing primary metric, guardrails, and runtime.
- Interpreting inconclusive or negative results.
- Linking experiment data in sheets/BI when tools exist.

## When NOT to Use

- Feature flag rollout without experiment framing → **feature-flagging**.
- Product roadmap prioritization without experiment → **prioritize-roadmap**.
- Casual UX opinions without measurement plan.

## Expected Outcome

- Experiment brief (hypothesis, metrics, population, duration).
- Analysis with effect size, interval, and decision (ship, extend, stop, redesign).
- Concrete next steps if underpowered—not vague retry language.

## Inputs to Gather

- Hypothesis and user-facing change.
- Primary metric and guardrails (latency, errors, revenue).
- Assignment unit (user, session, account) and integrity checks.
- Runtime, sample size, and peeking/sequential rules if any.
- Novelty/seasonality concerns.

## Workflow

1. Lock hypothesis and primary metric before viewing results (or note breach if peeked).
2. Validate assignment integrity and sample ratio mismatch.
3. Report effect size, CI, and runtime; compare guardrails.
4. If inconclusive: compute power or recommend duration/design change with numbers.
5. Document ship/kill/iterate recommendation.

## Domain guidance

- **Hypothesis** and **primary metric** first; guardrails (latency, errors) second.
- Check assignment integrity, novelty, and seasonality.
- Report effect size, confidence interval, and runtime; avoid peeking bias unless using sequential methods.
- If inconclusive: recommend power, duration, or design change—not vague "try again."

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full tool access | Pull experiment metrics from sheets/BI tools when connected. |
| Read-only | Analyze user-supplied tables; show calculations. |
| No data | Provide design template; do not invent significance. |

### Related tool sets

- `google-sheets`
- `jira`

## Review / Decision / Execution Criteria

- One primary metric; guardrails explicit.
- Call out peeking, SRM, and low power explicitly.
- Decisions tied to pre-registered success criteria when available.

## Output Format

1. Experiment summary.
2. Results (primary + guardrails) with effect and CI.
3. Decision and rationale.
4. Next steps (extend, redesign, ship).

## Quality Bar

- Statistically literate but readable for PMs.
- No fabricated p-values or lift percentages.

## Safety and Boundaries

- Do not recommend shipping on guardrail regressions without explicit acceptance.
- Ethical/user harm review for sensitive experiments.

## Escalation / Dispatch Rules

- Rollout mechanics → **feature-flagging**.
- Metric definitions in dashboards → observability skills.

## References

- `skills/old_skills.json` (`ab-experimentation`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
