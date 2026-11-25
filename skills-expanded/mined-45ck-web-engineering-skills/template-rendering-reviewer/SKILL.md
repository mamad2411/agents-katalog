---
name: "template-rendering-reviewer"
pack: "web-engineering-pack"
purpose: "Review server-side templates or rendering logic for duplication, unsafe assumptions, presentation leakage, and missing states."
inputs: ["feature scope", "existing routes or pages", "data inputs/outputs", "constraints or stack context"]
outputs: ["structured recommendation", "design notes", "risks or gaps", "recommended next artifact"]
handoffs: ["presentation-model-designer", "mvc-boundary-checker", "error-page-and-fallback-planner"]
---
# template-rendering-reviewer

## Purpose
Review server-side templates or rendering logic for duplication, unsafe assumptions, presentation leakage, and missing states.

## Expected inputs
- feature scope
- existing routes or pages
- data inputs/outputs
- constraints or stack context

## Deliverables
- structured recommendation
- design notes
- risks or gaps
- recommended next artifact

## Trigger this skill when
- You are designing or reviewing a web feature rather than a generic backend-only function.
- Request flow, form handling, rendering, state, or navigation decisions materially affect correctness.
- A feature needs clearer boundaries between route handling, server logic, and presentation.

## Operating procedure
1. Clarify the feature, request path, actors, and current or intended flow.
2. Separate facts, assumptions, constraints, and unresolved web-specific risks.
3. Prefer concrete request/response behavior over abstract framework talk.
4. Explicitly handle invalid, missing, unauthorized, and degraded states where relevant.
5. Recommend the next most useful web engineering or testing skill.

## Quality gates
- The recommendation respects actual web request boundaries and browser behavior.
- Missing and invalid states are not ignored.
- Assumptions and unresolved decisions are visible.
- Output is specific enough to influence implementation or testing.

## Output style
- Be concrete and structured.
- Separate findings, assumptions, and recommendations.
- Prefer explicit tradeoffs over single-answer absolutism.
- Use severity or priority where useful.

## Failure modes to avoid
- Do not rely on client-side behavior as the only safeguard.
- Do not blur controller, rendering, validation, and persistence responsibilities.
- Do not describe happy-path behavior only.
- Do not hide uncertainty behind framework-specific jargon.

## Minimum output skeleton
```md
## Summary
## Findings or proposal
## Evidence vs assumptions
## Risks or tradeoffs
## Recommended next skill
```

## Handoff targets
- presentation-model-designer
- mvc-boundary-checker
- error-page-and-fallback-planner
