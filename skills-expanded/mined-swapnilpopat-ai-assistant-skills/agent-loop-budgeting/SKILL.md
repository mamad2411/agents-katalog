---
name: agent-loop-budgeting
description: Put hard budgets and circuit breakers around AI coding agents so they can't burn unbounded tokens, money, or time on a single task. Use when designing an agent harness, debugging runaway loops, or shipping an agent feature to production.
source: self
date_added: 2026-05-01
---

# Agent Loop Budgeting

An unbudgeted agent is an unbounded bill. The cost-per-task variance of a free-running agent is often 100x. Cap it.

## When to Use

- Building or hosting a tool-using agent (Copilot-style, Claude Code, custom).
- Tasks occasionally take 50+ tool calls or run for many minutes.
- Cost-per-task distribution is long-tailed; a few tasks dominate spend.
- Agent gets stuck repeating the same tool call, or "thinks" forever.
- Pre-prod gate: you can't ship an agent without a worst-case bound.

## Budgets to Set

Every agent invocation must declare and enforce ceilings on:

| Budget | Typical default | Why |
| --- | --- | --- |
| Total input tokens | 100k–500k | Bounds context bloat |
| Total output tokens | 8k–32k | Bounds runaway generation |
| Tool calls | 10–40 | Bounds exploration |
| Wall-clock time | 60–300 s | Bounds UX + infra cost |
| Total $ | feature-dependent | The one users actually care about |
| Per-tool calls (e.g. `read_file`) | 5–15 | Stops file-thrashing |
| Self-correction retries | 2–3 | Stops "fix-the-fix" spirals |

Pick the dimension that bites first for your workload and alert on it.

## Circuit Breakers

Stop the loop early when:
- **Same tool + same args** twice in a row (or 3 times within 5 calls).
- **No new files / symbols** touched in the last N calls (agent is spinning).
- **Cumulative tool-output tokens** exceed a threshold without the answer changing.
- **Cost-so-far** exceeds X% of the per-task budget — degrade to a smaller model or surface a "continue?" prompt.
- **Tool error rate** > 50% in last 5 calls — the agent is fighting the environment.

On trip: stop, summarize what was learned, return a partial result with a clear "budget exhausted" signal.

## Loop Detection

Cheap signals that work in practice:

- Hash `(tool_name, normalized_args)` and track a sliding window.
- Track edit-distance between consecutive assistant messages — near-zero means thrash.
- Count distinct files/symbols touched per N calls; if it stops growing, exploration is dead.
- Track tool-output entropy: if the agent keeps reading the same content, it's not learning.

Don't try to be clever. Three simple counters beat one ML detector.

## Checkpoint Compaction

Long agent loops bloat context, which makes every subsequent call more expensive. At natural boundaries (tool call N, end of subtask, error recovery):

1. Summarize the working state into a 5-15 line "scratchpad".
2. Drop raw tool outputs older than the last 1-2 calls.
3. Keep the original task + acceptance criteria verbatim.
4. Re-anchor by restating the next concrete step.

This converts a 50k-token history into a 2k-token one without losing direction.

## Working Memory Pattern

Give the agent an explicit, rewritable memory slot instead of letting it re-derive state from history every turn:

```
WORKING_MEMORY (the agent updates this)
- Goal: <one sentence>
- Done: <bullets>
- Open questions: <bullets>
- Next step: <one sentence>
```

Promotes shorter histories and makes loop detection trivial (compare consecutive memories).

## Graceful Degradation

When budget is 80% spent, don't just kill — degrade:
1. Route remaining calls to a cheaper model.
2. Disable expensive tools (web search, large file reads).
3. Force a structured "best effort so far" output.
4. Return with a continuation token if the user wants to resume.

## Per-Tenant and Per-User Caps

Beyond per-task budgets:
- Per-user daily token cap (prevents one power user blowing the bill).
- Per-tenant rate limit on agent starts.
- Global concurrency cap (LLM provider rate limits + cost predictability).
- Anomaly alert when a single user's cost-per-task moves > 3σ.

## Observability

Per agent run, log:
- All budgets and remaining headroom over time
- Which budget tripped (if any)
- Tool-call sequence with token cost per step
- Compaction events
- Outcome: success / partial / budget-exhausted / error

One dashboard: cost-per-successful-task and budget-trip-rate by feature.

## Quick Wins Checklist

- [ ] Every agent call declares max tokens, max tool calls, max time, max $
- [ ] Loop detector on `(tool, args)` repetition is live
- [ ] Per-tool ceilings exist (especially for `read_file`, `web_search`)
- [ ] Working-memory slot used; raw tool outputs dropped after summary
- [ ] Degrade-then-stop path implemented, not just hard kill
- [ ] Budget-trip rate is a tracked SLI

## Anti-Patterns

- "Just one more retry" with no global retry budget.
- Counting only $ — by the time cost trips, latency already ruined UX.
- Letting the model self-report when it's done with no external timeout.
- Compacting mid-thought — wait for clean checkpoints.
- Hiding budget exhaustion from the user; they need to know it's a partial answer.
- Sharing one budget across many users (noisy-neighbor).

## References

- Related skills: `context-window-management`, `token-efficient-prompting`, `llm-cost-optimization`, `prompt-caching-patterns`
- Anthropic, OpenAI tool-use and agent documentation
