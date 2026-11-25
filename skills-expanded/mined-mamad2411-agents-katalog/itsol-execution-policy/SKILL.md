---
name: itsol-execution-policy
description: "Resolve model, reasoning, agents, parallelism, review, and stop limits—not workflow authority."
---

# ITSOL Execution Policy

Resource and completion contract; resolve after `itsol-workflow-mode`. Bounded administration reuses prior policy and does not create a new budget, review, QA, or completion gate.

## State

```yaml
execution_policy:
  preset: economy | standard | deep | custom
  policy_sources: {base: explicit-user-task-instruction | repo-default | agent-default, constraints: []}
  model_profile: economy | balanced | frontier
  model_control: enforced | advisory
  reasoning_profile: low | medium | high
  reasoning_control: enforced | advisory
  max_subagents: unlimited | 0..64
  max_parallel: 0..10
  max_review_rounds: 0..2
  stop_after: <resolved named stage>
  budget_escalation: forbidden | ask
done_when:
  - <observable criterion with evidence>
```

Use `standard` without explicit/repository policy. Presets are advisory routing intent unless a user/repository ceiling sets `model_control` or `reasoning_control: enforced`; native capability still clamps unsupported levels. `standard`/`deep` default to unlimited distinct identities and `max_parallel: 3`; `economy` disables agents. `max_subagents` counts types, not executions. Never invent a numeric identity ceiling.

## Rules

- Never use `maxTurns` or termination as completion; validate every `done_when` and preserve `completed`, `partial`, `blocked`, and `failed`.
- Record outcome, authority/constraints, `done_when`, focused evidence, unverified gaps, and blockers/next action.
- Only the main agent delegates. Use children only for independent material work or required independent review, with one writer per file/contract, stable `work_item_id`, bounded concurrency, and no nested delegation.
- A required review that exceeds policy remains incomplete; do not weaken the policy or ask for expansion unless `budget_escalation: ask` applies.
- If a hard model/reasoning ceiling cannot be enforced, disable child delegation; inline work must report the limitation.
- Tighten advisory routing, parallelism, review, or stop stages when useful, but never silently turn advisory model/reasoning intent into an enforced ceiling.

Read [references/policy.md](references/policy.md) for precedence and presets, [references/stops-and-delegation.md](references/stops-and-delegation.md) for stop/retry/review semantics, and [references/platform-capabilities.md](references/platform-capabilities.md) for model-specific effort calibration or provider-specific enforcement claims. Propagate the full state through context, plans, packets, reviews, continuations, and handoff.
