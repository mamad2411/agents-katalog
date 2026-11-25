---
name: system-prompt-doctor
description: Audit, optimize, and benchmark a user-owned system prompt, developer prompt, CLAUDE.md, AGENTS.md, or agent instruction file against representative tasks. Use when the user wants to improve an agent's core instructions, make an agent more reliable, reduce instruction bloat, fix tool-use or ask-vs-act behavior, or prove whether a revised system prompt is actually better.
---

# System Prompt Doctor

Do not optimize a system prompt by taste. Optimize it against behavior.

## Scope

This skill works on prompts/instruction files the user owns or can provide, including:

- system/developer prompts
- `CLAUDE.md`
- `AGENTS.md`
- reusable agent instruction files
- agent persona/policy prompts

Do not claim access to hidden platform system prompts that the runtime does not expose.

## Workflow

1. **Capture the contract.** Record the target model, prompt surface, task family, tools, hard constraints, output shape, failure cases, latency/cost limits, and what must not change.
2. **Build the eval before editing.** Prefer real historical failures and corrections. Otherwise create 8 to 20 representative cases plus hard negatives and at least a 20% holdout split.
3. **Baseline the current prompt.** Preserve prompt hash, model/version, outputs, scores, token usage, tool behavior, and failures.
4. **Audit instruction architecture.** Find contradictions, duplicate rules, vague defaults, missing completion criteria, tool-policy gaps, bad ask-vs-act calibration, stale examples, and context that should live outside the system prompt.
5. **Generate a small candidate beam.** Always include:
   - minimal-diff repair
   - structure-first rewrite
   - compact/progressive-disclosure variant
   Add a provider-specific adapter only when eval failures justify it.
6. **Optimize on train/validation only.** If Promptfoo is available, use `promptfoo optimize` with a validation split. Never tune on the final holdout set.
7. **Red-team important boundaries.** Test conflicting instructions, ambiguous tasks, tool misuse, prompt injection exposure, refusal/escalation boundaries, and over/under-triggering where applicable.
8. **Battle the winner against the current prompt.** Same model, same task manifest, same tool permissions. Report quality lift and token/cost/latency change.
9. **Prefer the smallest prompt that preserves measured behavior.** A larger prompt is not a better prompt.
10. **Return evidence, not vibes.** Include the optimized prompt, diff, eval set, before/after scores, regressions, token delta, residual risks, and a shareable result card.

## Recommended references

The closest existing public primitive is Sentry's Apache-2.0 `prompt-optimizer` skill. Promptfoo's optimizer supplies the baseline → candidate → eval → held-out-selection loop. Anthropic's agent-development guidance provides a useful system-prompt structure template. See `references/SOURCES.md` for the source record.

## Output

Produce:

1. `Current prompt audit`
2. `Success criteria`
3. `Eval manifest`
4. `Optimized prompt`
5. `Behavioral diff`
6. `Battle result` (only after real evals)
7. `Token/cost delta`
8. `Regressions / residual risks`
9. `Share card`

Never publish synthetic/demo scores as real benchmark results.
