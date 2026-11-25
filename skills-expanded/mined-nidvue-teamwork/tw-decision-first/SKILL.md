---
name: tw-decision-first
description: Decide first: before prose reasoning, ask the small typed question — which record kind owns a defect, is this action destructive, keep or drop this tool output. Answers arrive as a choice with a probability, or a boolean with a probability. Use when a lane is about to choose between two record types, weigh an irreversible action, or trim context, and whenever a decision is about to be recorded without a number.
---

# Decision-first: ask the small question

Owner: CEO
Related: [Decisions.md](../../../docs/Team/Decisions.md), [tw-number-vet](../tw-number-vet/SKILL.md)

## What it is

Three questions, each with a fixed typed shape and a fixed threshold. Anything
outside those three goes back on the chat model and the human gates; the engine
does not consult this layer for anything else.

| Q | Shape | Threshold | Action |
|---|---|---|---|
| `defect_ownership` | choice `task`/`lesson`/`skill`/`knowledge` | `p(task) ≥ 0.60` | a task carries a named defect and its reproducer; below it, a `lesson add` record |
| `is_destructive` | bool | `p(true) ≥ 0.80` | stop, escalate to the CEO for authorization, do not execute |
| `context_keep` | bool | `p(true) ≥ 0.55` | keep the tool output in context before compaction; below it, summarise it |

The probability and the threshold go in the record, next to the reasoning —
`tw-number-vet` vets the number, this skill produces it.

## Probe

1. pi runs it natively: `pi --list-models` lists `typesafe/jev-latest (chat)`
   and the classifier path is `ctx.modelRegistry.classify(...)` — see
   [pi models doc](https://github.com/earendil-dev/pi/blob/main/docs/models.md),
   accessed 2026-11-22; the model page is
   [TypeSafe SystemOne](https://typesafe.ai), accessed 2026-11-22.
2. `pi --print -ne -e <probe>` prints, for the same state:
   `STOP=stop`, an `ANSWER` with `p` and `confidence`, and a `USAGE` token count.
3. `pi auth check --provider typesafe --json` must print `{"status":"ready"}`.
4. A run with no `STOP=stop` line is a failure, not an empty answer; do not
   decide on it.

## Evidence

Every run records command + revision + observed result, as the team requires.

- verdict: no observed effect
- answer: `defect_ownership choice task p=0.96 confidence=0.94 threshold=0.60
  model=typesafe/jev-latest @6a5b4842` (probe `pi --print -ne -e jev_probe.ts`,
  401 input tokens, 272 ms, exit 0)
- answer: `is_destructive bool false p=0.05 confidence=0.94 threshold=0.80
  model=typesafe/jev-latest @6a5b4842` (same probe run, same state)
- contrast: prose decisions in `Decisions.md` (for example `D-20261122-Reviewer`
  on the retired T-0007 worktree) carry reasoning but no number; the same
  question asked of the classifier returns `defect_ownership` choice `task`
  `p=0.96` and `is_destructive` bool `p=0.05`
  (`pi --print -ne -e jev_probe.ts -> CLASSIFIERS=["typesafe/jev-latest"]`,
  `STOP=stop`, exit 0).
- measured: 401 input tokens answered in 272 ms of wall time
  (`POST api.typesafe.ai/v1/systemone/chat/completions -> HTTP 200`), against
  21.9k of always-on startup read and 87.3 k-110.5 k per-role budget
  (`teamwork.py harness budget`, cap 106.5 k).
- NO_ENTRY — no task has been decided by this layer yet. Adoption is ruled in
  `Decisions.md` D-20261122-CEO; the falsifier there (same state asked twice
  differing by more than 0.15 in probability, or a decision needing repeated
  asks) retires the layer and this skill with it.

## Pitfalls

- `JEV_API_KEY` is not the provider's variable: the model reads
  `TYPESAFE_API_KEY`, exported from `JEV_API_KEY` in `~/.bashrc` —
  `bash -lc 'echo ${#TYPESAFE_API_KEY}'` → 107. Never print the key.
- Consensus is not evidence: one answer is provisional; ask the same state twice
  and keep the pair when the number drives a red line.
- A `confidence` of 0.60 on a `bool` is not certainty; when the threshold sits
  near the boundary, the engine's own gate decides, not the number.
- Never route work, size a swarm or call a task done from this layer.
  `AC-DEC-3` is not met by any answer this model gives; only a role other than
  the owner on the merged revision meets it.
- A classifier that disagrees with a red line does not weaken the red line.

## Guardrails

- This skill does not replace `AGENTS.md`, the red lines, or the quality gates.
  If it conflicts with them, they win and this file must be fixed.
- It never bypasses: self-check, independent review, the PR, or the Reviewer-only
  merge. It may not weaken or skip a test layer.
- Changing this skill is normal work: branch, commit with the fixed message style,
  PR, review, merge. Never edit it on `main`.
