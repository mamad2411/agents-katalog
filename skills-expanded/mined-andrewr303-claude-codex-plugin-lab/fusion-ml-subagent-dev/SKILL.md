---
name: fusion-ml-subagent-dev
description: >-
  Fusion-enhanced execution of ML experiment plans. Use when an ML implementation
  plan exists and you want ml-subagent-dev discipline plus Fusion councils,
  builder/breaker review, Python swarm patterns, and Loop-God verification.
---

# Fusion-ML Subagent Development

This skill wraps `ml-subagent-dev`; it does not weaken it. The original ML gates
still decide completion:

- Code subtasks: TDD red→green, spec review, quality review, lightweight
  conclusion.
- The single `[INTEGRATION]` subtask: TDD red→green, spec review, quality
  review, L0 static checks, L1 runtime validation, full metric-backed
  conclusion.

## Fusion Enhancements

Use Fusion for independent advice and adversarial review; Codex still owns final
repo edits and verification.

### 1. Plan Gate Council

Before implementation, validate the plan:

- exactly one `[INTEGRATION]` subtask
- evaluation split is explicit when evaluation exists
- review_criteria exists
- L0/L1 scope is clear
- core code has no test/toolkit dependency

For ambiguous or high-risk plans, run a Fusion huddle or council using
`fusion-orchestrate`. Panelist output is advisory; do not let it override the
written plan unless the human approves or you revise the plan through the
proper design/plan path.

### 2. Agent Allocation

Default allocation:

| Work | Fusion pattern | Agents |
|---|---|---|
| Small component code | ladder | copilot → opencode → codex |
| Boilerplate-heavy code | ladder / flow | opencode, copilot |
| Architecture-sensitive code | council | codex, agy, grok, opencode |
| Integration subtask | builder/breaker | opencode builder, grok breaker, agy reviewer, codex integrator |
| Performance bottleneck | heavy / profile-first | agy analysis, grok verification, codex diagnosis |
| Verification | gate | deterministic test/build/typecheck command |

### 3. Builder-Breaker Use

For the `[INTEGRATION]` subtask, prefer:

```bash
bash "$FUSION_ML_PLUGIN_ROOT/scripts/swarm.sh" breaker "<integration risk summary>" --builder opencode --breaker grok --json
```

Read the returned transcript, then implement only changes that survive your own
source inspection and deterministic checks.

### 4. Validation Pyramid Is Non-Negotiable

Do not let Fusion votes substitute for VP:

- L0 static review must pass before L1.
- L1 must run the six-stage runtime validation unless explicitly skipped in the
  design doc; Auto Research cannot skip L1.
- Any VP failure routes to `diagnostics` before speculative fixes.

### 5. Loop-God Wrapper

For each subtask, maintain:

- objective and done signal
- files in scope
- checks to run
- retry/fix budget
- honest stop condition

Use `update_plan` for user-visible progress in Codex.

## Completion

After all subtasks pass their type-specific gates, preserve the original
Post-Completion Gate:

- If the design has an Autoresearch Protocol: ask **Research / Train / Done**.
- Otherwise ask **Train / Done**.

Do not decide this silently.

