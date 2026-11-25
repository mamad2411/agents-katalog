---
name: effort-sizing
discoverable: false
description: Thin gating skill that classifies a task's complexity when the caller's own heuristics cannot confidently route it. Invoke when you need to decide between going straight to detailed planning versus running a design/ideation pass first, or when a task might be too large to plan directly. Trigger phrases include "score this task's complexity," "run the complexity gate," "decide writing-plans vs brainstorming," "is this task big enough to need a design phase," and "check if this needs to be split up." Called by sdlc-engine as a standing step, and by sdlc-brief or sdlc-direct only as a fallback when their lightweight heuristics can't decide. Delegates the actual scoring to the sizing-analyst agent and normalizes its output into a fixed {score, routing, breakdown} schema. Not for: doing the planning or design itself, or re-scoring a task the caller's own heuristics already routed confidently.
version: 0.1.0
license: Apache-2.0
authors: [agentic-os]
---

# Complexity Scoring

## What this does

`effort-sizing` is a gate, not a scorer. It never computes a complexity
score itself. Its entire job is: decide whether the caller needs a score at
all, dispatch the `sizing-analyst` agent when it does, coerce whatever comes
back into a fixed schema, and hand the caller a routing verdict. Treat every
line of judgment about *how complex* a task is as belonging to the agent —
this skill only formats and routes.

## When to invoke

Call this skill only when the caller's own heuristic-first routing logic
cannot confidently classify a task on its own. The decision of *whether* to
invoke this skill at all belongs to the caller, not to this skill.

- `sdlc-engine` calls this skill as a standing step in its flow.
- `sdlc-brief` and `sdlc-direct` call this skill only as a fallback, when their
  own lightweight heuristics fail to produce a confident route.

Do not invoke this skill to re-check a routing decision the caller has
already made with confidence, and once invoked, do not re-judge the verdict
it returns — see Ownership boundary below.

## Inputs

| Field | Source | Notes |
|---|---|---|
| `task_description` | Verbatim from Phase 1 (`story-intake`) output | Pass through unmodified — do not summarize or rewrite it |
| `feature_area` | Short keyword summary | e.g. `"provider integration SSO"` |
| `repo_path` | Absolute path to the current checkout | Gives the agent filesystem context for its estimate |

## Operating steps

1. **Confirm the gate applies.** This skill assumes the caller already
   decided its own heuristics couldn't resolve the route. Do not second-guess
   that decision — proceed straight to dispatch.
2. **Dispatch the agent.** Invoke `sizing-analyst` via the Agent tool with:
   ```
   subagent_type='sizing-analyst'
   task_description='<input>'
   feature_area='<input>'
   ```
3. **Validate the response** against the output schema below. Confirm
   `score` is an integer 6–36, `breakdown` has all six sub-scores each 1–6
   and summing to `score`, and `routing` is one of the three allowed
   literals.
4. **On a malformed response, retry once** with a stricter prompt that
   restates the exact schema and forbids prose outside the JSON object.
5. **On a second malformed response, do not error.** Fall back to a fixed
   default so the caller can keep moving:
   - `score: 18`
   - `routing: "brainstorming"`
   - `rationale`: state plainly that the fallback fired and why (agent
     output did not parse after retry)
6. **Check for the split signal.** If the agent's response carries the
   `SPLIT REQUIRED` flag, override `routing` to `split-required` regardless
   of the numeric score, and halt — see Routing outcomes below.
7. **Map score to routing** using the thresholds table, unless step 6 already
   forced `split-required`.
8. **Write the result** to `<run_dir>/complexity.json`. This is an R1
   (run-artifact write) operation — no repository files are touched, no
   external side effects occur.
9. **Return** the normalized `{score, breakdown, routing, rationale}` object
   to the caller. Do not add commentary, re-score, or re-route what the
   agent produced or what the fallback set.

## Routing outcomes

| Score range | `routing` | Effect |
|---|---|---|
| 6–14 | `writing-plans` | Skip design/ideation; go straight to detailed planning |
| 15–36 | `brainstorming` | Produce a design doc first (Phase 4), then proceed to detailed planning |
| agent signals `SPLIT REQUIRED` | `split-required` | Halt the pipeline; a human must decompose the task into smaller pieces |

`split-required` overrides the numeric-score mapping whenever the agent
raises the flag — check for it before applying the score thresholds.

## Output schema

```json
{
  "score": "<integer 6..36>",
  "breakdown": {
    "component_scope": "<1..6>",
    "requirements_clarity": "<1..6>",
    "technical_risk": "<1..6>",
    "file_change_estimate": "<1..6>",
    "dependencies": "<1..6>",
    "affected_layers": "<1..6>"
  },
  "routing": "writing-plans | brainstorming | split-required",
  "rationale": "<verbatim from agent, or fallback note>"
}
```

Written to `<run_dir>/complexity.json`.

## Fallback rule

> Malformed agent output is not this skill's failure to absorb quietly —
> it is a signal worth recording. Retry once, with a stricter format
> instruction. If the second attempt is still malformed, do not block the
> pipeline on a scoring agent's formatting failure: emit the fixed default
> (`score: 18`, `routing: "brainstorming"`) and say so in `rationale`, so
> anything reading the run artifact later knows the number is a fallback,
> not a judgment.

## Ownership boundary

> This skill owns exactly one thing: turning an agent response (or a
> fallback) into the fixed schema, plus applying the score-to-routing table.
> It does not own whether a task is actually complex — that's the
> `sizing-analyst` agent's call, grounded in what it's given. It does not own
> whether it gets invoked in the first place — that's the calling
> pipeline's heuristic-first decision. After dispatch, treat both of those
> judgments as final; re-litigating either one here defeats the point of a
> thin gate.

## References tree

- `references/complexity-assessment/guide/complexity-assessment-guide.md` —
  the assessment methodology this skill and the `sizing-analyst` agent share:
  what each of the six breakdown dimensions means, how to read a borderline
  score near the 14/15 boundary, and what should make the agent raise
  `SPLIT REQUIRED` instead of returning a number. Consult it when validating
  a response in step 3, and hand it to the agent as grounding context on
  dispatch so its scoring stays consistent across runs.

## Cross-references

- Upstream: Phase 1 (`story-intake`) produces `task_description`.
- Downstream: `writing-plans` and `brainstorming` (Phase 4) are the two
  planning paths this skill routes into.
- Caller: `sdlc-engine` (standing step), `sdlc-brief` and `sdlc-direct`
  (fallback-only callers).
- Delegate: the `sizing-analyst` agent performs the actual scoring; this
  skill does not.

## Non-goals

- Does not compute a complexity score itself — always delegated to
  `sizing-analyst`.
- Does not decide when it gets invoked — that heuristic-first bypass
  decision belongs to the calling pipeline.
- Does not perform decomposition when `split-required` fires — halts and
  defers to a human.
- Does not define what counts as a "cheap heuristic" or a "high-confidence
  route" for callers — that threshold is the orchestrator's to set.
