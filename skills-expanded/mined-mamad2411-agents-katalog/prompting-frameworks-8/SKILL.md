---
name: prompting-frameworks-8
description: Eight prompt frameworks — TRACE, TAG, RTF, CLEAR, PACT, STAR, RISE, RASCEF — with when-to-use guidance, fill-in templates, and a selector that picks the right one for a task and rewrites the user's rough prompt into it. Distinct from claude-prompt-frameworks (CLARITY/SOCRATES/etc.). Run via /prompt-frame.
---

# 8 Prompting Frameworks

Source: smarterwithai.news infographic (titled "ChatGPT Prompting Frameworks"; they work identically in Claude). Sibling of `claude-prompt-frameworks` — different acronyms, no overlap.

## Selector

| Need | Use |
|---|---|
| Repeatable, high-clarity instructions | **TRACE** |
| Quick, lightweight prompt | **TAG** |
| Control tone and structure | **RTF** |
| Refine a messy prompt | **CLEAR** |
| Stakeholder-aware output | **PACT** |
| Case write-ups, structured narratives | **STAR** |
| Feedback loops and iteration | **RISE** |
| Complex multi-stage task | **RASCEF** |

## Templates

**01 TRACE** — Task, Request, Action, Context, Example. Start with the outcome to reduce ambiguity; add constraints; give a reference output.
```
Task: [goal]
Request: [what you want back]
Action: [steps/criteria]
Context: [background/constraints]
Example: [sample format or mini exemplar]
```

**02 TAG** — Task, Action, Goal. Make success measurable.
```
Task: [objective]
Action: [do X using Y]
Goal: [metric/definition of done]
```

**03 RTF** — Role, Task, Format.
```
Role: Act as a [expert]
Task: Produce [deliverable]
Format: [bullets/table/checklist], include [sections]
```

**04 CLEAR** — Concise, Logical, Explicit, Actionable, Responsible. Remove noise; order requirements stepwise; make assumptions explicit and testable; add safety/ethics limits.
```
Concise ask: [one sentence]
Logic: [ordered requirements]
Explicit constraints: [must/avoid]
Actionable output: [next steps/checklist]
Responsible guardrails: [limits/compliance]
```

**05 PACT** — Perspective, Action, Context, Task.
```
Perspective: As a [stakeholder/expert]
Action: [analyze/compare/design]
Context: [situation, constraints, audience]
Task: [clear objective + success criteria]
```

**06 STAR** — Situation, Task, Action, Result.
```
Situation: [context]
Task: [what needed to happen]
Action: [steps taken]
Result: [outcome + metric + lesson]
```

**07 RISE** — Reflect, Inquire, Suggest, Elevate.
```
Reflect: [what's working / what you see]
Inquire: [2–3 diagnostic questions]
Suggest: [concrete changes]
Elevate: [stronger version / next level]
```

**08 RASCEF** — Role, Action, Steps, Context, Example, Format.
```
Role: [expert]
Action: [create/analyze/plan]
Steps: 1) … 2) … 3) …
Context: [constraints, audience, inputs]
Example: [mini sample]
Format: [table/sections/length]
```

## How to apply

1. Read the user's task; pick ONE framework from the selector and say why in one line.
2. List which slots the user's text already fills and which are missing.
3. Ask for the missing slots in one batch (max 4 questions). If the user says "just do it", fill them with stated assumptions labelled `ASSUMED`.
4. Return the finished prompt in a code block, plain text, copy-paste ready.
5. Offer the second-best framework as an alternative only if the task is borderline.

Rule: never stack two frameworks in one prompt — combine only via RASCEF, which already contains Role/Steps/Example/Format.
