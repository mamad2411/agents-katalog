---
name: "iteration-outcome-reviewer"
pack: "agile-delivery-pack"
purpose: "Assess what an iteration actually delivered against its goal, commitments, quality expectations, and unresolved spillover."
inputs: ["sprint goal", "planned items", "completed items", "defects/regressions", "carryover context"]
outputs: ["iteration outcome summary", "goal achievement assessment", "slip/carryover notes", "quality observations", "follow-up actions"]
handoffs: ["retrospective-pattern-finder", "blocker-escalation-advisor", "backlog-groomer"]
---
# iteration-outcome-reviewer

## Purpose
Assess what an iteration actually delivered against its goal, commitments, quality expectations, and unresolved spillover.

## Trigger this skill when
- The team is working in iterations, sprints, or short delivery cycles.
- Backlog items, sprint outcomes, or team process signals need structured review.
- You need clearer delivery discipline instead of vague “be more agile” advice.

## Expected inputs
- sprint goal
- planned items
- completed items
- defects/regressions
- carryover context

## Deliverables
- iteration outcome summary
- goal achievement assessment
- slip/carryover notes
- quality observations
- follow-up actions

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
- blocker-escalation-advisor
- backlog-groomer

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
