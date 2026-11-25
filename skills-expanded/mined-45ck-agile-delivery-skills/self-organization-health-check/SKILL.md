---
name: "self-organization-health-check"
pack: "agile-delivery-pack"
purpose: "Assess whether the team is self-organizing effectively or is stalled by hidden control, poor clarity, overload, or coordination failure."
inputs: ["team norms/context", "recent delivery behavior", "decision patterns", "planning/review signals", "blocker history"]
outputs: ["health summary", "decision/ownership issues", "coordination issues", "warning signals", "recommended experiments"]
handoffs: ["retrospective-pattern-finder", "cross-functional-team-checker", "blocker-escalation-advisor"]
---
# self-organization-health-check

## Purpose
Assess whether the team is self-organizing effectively or is stalled by hidden control, poor clarity, overload, or coordination failure.

## Trigger this skill when
- The team is working in iterations, sprints, or short delivery cycles.
- Backlog items, sprint outcomes, or team process signals need structured review.
- You need clearer delivery discipline instead of vague “be more agile” advice.

## Expected inputs
- team norms/context
- recent delivery behavior
- decision patterns
- planning/review signals
- blocker history

## Deliverables
- health summary
- decision/ownership issues
- coordination issues
- warning signals
- recommended experiments

## Operating procedure
1. Clarify the delivery context, scope, and timebox.
2. Separate what is known from what is assumed or missing.
3. Produce the skill-specific artifact or review output.
4. Surface coordination, quality, sequencing, or blocker risks explicitly.
5. Recommend the next best handoff instead of trying to solve the whole lifecycle at once.

## Quality gates
- The output is specific to the current iteration context.
- Risks, ambiguity, and dependencies are visible.
- Advice is actionable within a real team workflow.
- The result does not confuse commitment with aspiration.

## Handoff targets
- retrospective-pattern-finder
- cross-functional-team-checker
- blocker-escalation-advisor

## Output style
- Be explicit about tradeoffs and delivery risk.
- Prefer concise operational artifacts over long motivational prose.
- Surface evidence gaps instead of inventing certainty.
- Keep the result usable by engineers, leads, or PMs.

## Failure modes to avoid
- Do not treat every backlog item as equally ready.
- Do not hide blocker or dependency risk.
- Do not reward ticket closure over outcome delivery.
- Do not confuse a retrospective observation with a validated root cause.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks / blockers
## Open questions
## Recommended next skill
```
