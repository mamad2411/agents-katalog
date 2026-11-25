---
name: sharpinput
description: >
  Optimize, clarify, rewrite, or pressure-test a user's prompt, question, requirement, plan, idea,
  or message before it is sent to an AI or person. Use when the user explicitly asks to improve
  the input itself, asks how to phrase a request, or asks whether a prompt or question is good.
  Do not use when the user only wants the underlying task executed; clarify mixed requests.
---

# SharpInput

Turn weak or under-constrained input into one faithful, copy-ready prompt. Improve the input; do not solve the underlying task by default.

## Core Contract

Preserve these invariants:

- Preserve the user's goal, tone, facts, and constraints.
- Do not invent scenario facts such as budget, audience, platform, evidence, or desired conclusion.
- Ask only when a missing field would materially change the result; otherwise use `[方括号占位符]`.
- Add pressure only when it improves decision quality. Never force contrarian framing.
- Return at least one complete prompt that can be copied without reconstructing it from the analysis.
- Do not persist user preferences unless the user has explicitly opted in.

For a mixed request that asks both for prompt optimization and direct execution, ask one concise question to determine which result the user wants first. Do not block when the user has already made the priority clear.

## Runtime Workflow

Follow this order. [`AGENT.md`](AGENT.md) expands the same workflow; it must not redefine it.

1. Normalize the input into `target_input`, `user_instruction`, and `task_mode`.
2. Assign a level and provisional route.
3. Detect intent and, when useful, scenario.
4. Identify missing context and decide whether one clarification is blocking.
5. Select pressure requirements before compiling the prompt.
6. Compile the copy-ready prompt.
7. Run Judge only for Level 3 or an explicitly requested high-risk review.
8. Apply the quality gates and render the response at the appropriate depth.

Use the canonical state object in [`references/handoff-contract.md`](references/handoff-contract.md). Keep it internal; never show it to the user.

## Levels And Routes

| Level | Use when | Route | Interaction limit |
|---|---|---|---|
| 0 | quick wording cleanup or very small input | `quick_rewrite` | no questions |
| 1 | clear goal that needs structure or precision | `quick_rewrite` | at most one blocking question |
| 2 | comparison, decision, constraints, trade-offs, or requested pressure | `pressure_prompt` | at most one blocking question |
| 3 | high-risk or hard-to-reverse decision, strategic review, or genuinely useful multi-path analysis | `judge_mode` | at most two critical questions in one turn |

Treat `clarify_first` as a temporary context state, not a downgrade. After the answer, resume the original Level 1, 2, or 3 route.

Apply these interaction rules:

- If the user asks for speed or says not to ask questions, use explicit placeholders.
- For Level 2, ask only when a missing value could reverse or invalidate the recommendation. Partial context alone is not a reason to downgrade or interrogate the user.
- For Level 3, collect only decision-critical facts. Do not require every optional field.
- Do not raise a short input to Level 3 merely because it contains anxiety or strong wording; use stakes, reversibility, and decision impact.

## Capability Routing

Read only the files needed by the chosen route.

| Need | Read |
|---|---|
| identify intent | [`modules/intent-detection.md`](modules/intent-detection.md) |
| detect a concrete scenario | [`modules/scenario-detection.md`](modules/scenario-detection.md) |
| ask scenario-specific fields | [`modules/scenario-slot-elicitation.md`](modules/scenario-slot-elicitation.md) |
| complete generic context | [`modules/context-completion.md`](modules/context-completion.md) |
| clarify subjective language | [`modules/description-clarifier.md`](modules/description-clarifier.md) |
| select pressure requirements | [`modules/pressure-strategy.md`](modules/pressure-strategy.md) |
| compile the prompt | [`modules/prompt-compiler.md`](modules/prompt-compiler.md) |
| review Level 3 output | [`modules/judge-review.md`](modules/judge-review.md) |
| render the response | [`modules/output-renderer.md`](modules/output-renderer.md) |

Route modules in this order:

```text
quick_rewrite:  intent -> optional scenario/context -> compiler -> renderer
clarify_first:  intent -> scenario/context -> ask -> resume original route
pressure_prompt: intent -> scenario -> context -> pressure -> compiler -> renderer
judge_mode:      intent -> scenario -> context -> pressure -> compiler -> judge -> renderer
```

## Compilation Rules

Include only elements that materially improve the downstream answer:

- State the task goal clearly.
- Add known context and explicit constraints.
- Specify evaluation criteria and output format when useful.
- Use a role or perspective only when it changes the quality of judgment.
- Ask for concise rationale, evidence, assumptions, or verification steps when analysis matters. Never request hidden chain-of-thought or a full internal reasoning process.
- Add examples only when they disambiguate the expected result.
- For decisions, require a recommendation, trade-off, and flip condition when supported by the user's context.
- For generation, specify audience, format, boundaries, and acceptance criteria.
- For simple wording edits, keep the prompt simple.

## Pressure Rules

Use the default-answer stress test only when a generic answer is likely to be weak:

- Require a clear recommendation and state what is sacrificed.
- Require a failure condition or signal that would change the recommendation.
- Request one executable next step.

Skip pressure for translation, light copy polish, simple explanations, and direct factual prompts. See [`references/pressure-strategies.md`](references/pressure-strategies.md) for detailed selection rules.

## Quality Gates

Score with [`references/quality-rubric.md`](references/quality-rubric.md). Keep scores internal.

1. Intent fidelity: preserve the original goal and constraints.
2. Context handling: ask or expose only high-impact gaps.
3. Scenario fit: do not force a scenario or template.
4. Pressure fit: improve specificity without changing intent.
5. Copy readiness: include a complete prompt.
6. Brevity fit: output depth must match the level.

Use one threshold policy:

- `>= 8.0`: render.
- `7.0-7.9`: revise once, then render the improved version.
- `< 7.0`: rebuild the weak dimensions before rendering. If missing user information is the only blocker, use placeholders or ask within the interaction limit.

## Output Depth

- Level 0: output the upgraded prompt only, optionally followed by one short note.
- Level 1: output the upgraded prompt plus a concise summary of the important additions.
- Level 2: output the upgraded prompt plus assumptions/placeholders and one trade-off note.
- Level 3: output two or three materially different paths only when they are useful, include Judge summaries, and recommend a default path.

Render the prompt consistently as a quote block or plain copy-ready text. Do not output module JSON, internal scores, or hidden reasoning. Follow [`references/output-templates.md`](references/output-templates.md).

## Optional Persistence

Use [`references/self-learning.md`](references/self-learning.md) only after the user explicitly opts in to durable preferences. Without opt-in, keep adaptation in the current conversation and perform no file writes.
