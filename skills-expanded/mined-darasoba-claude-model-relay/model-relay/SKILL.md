---
name: model-relay
description: Route a coding task through a three-stage model relay — Fable 5 plans and classifies complexity, Opus 4.8 or Sonnet 5 implements based on that complexity, then Fable 5 reviews the result. Includes model fallback chains for when a usage limit is exhausted or a model is unavailable. Use for any non-trivial code change: features, refactors, bug fixes with unknown root cause, or multi-file work. Do NOT use for trivial edits, questions, or read-only exploration.
---

# Model relay

Three stages, three subagents. You are the orchestrator — you run the relay, you do not do the work yourself.

```
Fable 5 (relay-planner)  →  plan + complexity
        ↓
   HIGH → Opus 4.8   ┐
                     ├→ relay-implementer  →  diff + verification
   STANDARD → Sonnet ┘
        ↓
Fable 5 (relay-reviewer) →  APPROVE / REVISE
```

## When to run it

Run the relay for non-trivial code changes: multi-file work, features, refactors, bugs whose root cause is unknown.

Skip it — and just do the work — for trivial mechanical edits (a typo, a renamed variable, a version bump), for questions and explanations, and for read-only exploration. Announce that you're skipping and why. The relay costs three model runs; a one-line fix does not earn that.

## Stage 1 — Plan

Call the `relay-planner` subagent with the user's task plus any context you already have (files you've read, errors you've seen). Do not pre-solve it; hand over the problem, not your answer.

It returns `COMPLEXITY`, `CONTEXT`, `PLAN`, `VERIFY`, `OPEN QUESTIONS`.

**If `OPEN QUESTIONS` is non-empty and the answers would change the implementation, stop and ask the user before spending an implementer run.** This is the cheapest possible moment to catch a misunderstanding.

## Stage 2 — Implement

Call `relay-implementer` with the planner's **complete** output as the briefing. Set the model by the planner's classification:

| `COMPLEXITY` | `model` parameter |
|---|---|
| `HIGH` | `opus` |
| `STANDARD` | `sonnet` |

The `model` parameter on the Agent call overrides the agent's frontmatter, so pass it explicitly every time rather than relying on the default.

## Stage 3 — Review

Call `relay-reviewer` with the original plan **and** the implementer's output. It re-verifies independently and returns `APPROVE` or `REVISE`.

- `APPROVE` → report the result to the user. Include the reviewer's nits if any.
- `REVISE` → send the blockers back to `relay-implementer` (same model as before), then review again.

**Cap this at two revise rounds.** If it still returns `REVISE`, stop and bring the disagreement to the user with both positions. Do not loop. Two models disagreeing three times is a sign the plan was wrong, not the code — and that is a decision for the user, not for another round of tokens.

## Fallback chains

Claude Code's built-in `fallbackModel` setting only covers *overload and unavailability*. It explicitly does **not** fire on rate-limit or usage-limit exhaustion. So handle those here, in the orchestrator.

A stage has failed when the Agent call returns `Agent terminated early due to an API error`, or the error mentions a usage limit, rate limit, or that the model is unavailable. On failure, retry the same subagent with the next model in its chain:

| Stage | Chain |
|---|---|
| `relay-planner` | `fable` → `opus` → `sonnet` |
| `relay-implementer` (HIGH) | `opus` → `sonnet` |
| `relay-implementer` (STANDARD) | `sonnet` → `opus` → `haiku` |
| `relay-reviewer` | `fable` → `opus` → `sonnet` |

Rules:

- **Fable never implements.** It appears in the planner and reviewer chains only. If an implementer chain is exhausted, stop and tell the user — do not reach for Fable, and do not write the code yourself in the main session.
- **Haiku never implements HIGH-complexity work.** The planner flagged it as architectural, concurrency-sensitive, or security-touching for a reason. If both Opus and Sonnet are exhausted, fail loudly and tell the user to wait for a limit to reset. A wrong change to code like that costs more than the delay.
- **Tell the user, in one line, whenever you fall back.** "Fable 5 is at its limit; planning with Opus 4.8 instead." Silent degradation is the failure mode that matters here — the user must know which model actually did the work.
- **Never let the reviewer run on the same model that implemented.** If the chain would land the reviewer on the implementer's model, skip to the next entry. An independent check is the entire point of the review stage; the same model reviewing its own diff mostly agrees with itself.
- If a partial output came back before the error, the subagent was cut off mid-run. Treat it as failed and retry — do not build on a truncated plan or a half-applied diff.
- If **every** model in a chain is exhausted, stop and tell the user. Do not silently do the work yourself in the main session.

## Reporting back

Tell the user which model did each stage, the verdict, and what changed. Lead with the outcome:

> Done. Fable 5 planned it as STANDARD, Sonnet 5 implemented, Fable 5 approved with one nit.

If any stage fell back to a different model, say so in that same line.
