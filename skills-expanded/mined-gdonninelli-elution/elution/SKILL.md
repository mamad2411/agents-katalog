---
name: elution
description: Run a timer-bound research loop with subagents, BM25 memory, and Yukon measuring. Use for optimization work that iterates until a deadline.
license: MIT
compatibility: opencode, claude-code, pi, generic
metadata:
  audience: solvers
  workflow: research-loop
---

# Elution

Elution washes the valuable findings out of noisy research, like gold
elution washing gold off carbon. Gravel in, gold out.

## When to use

User typed `/elution <minutes>` or asked for a timer-bound optimization
loop, especially in a Yukon benchmark checkout or any repo where a
benchmark script decides what is better.

## Setup (do once per run)

1. `elution init --minutes <N>` creates `.elution/` with `state.db`,
   `deadline.txt`, `best.json`, `memory/`, `iterations/`.
2. Read `benchmark.json` if present. Note schema v1 (one benchmark) vs
   v2 (tracks sharing one branch, each with `editablePaths`). Move to
   the benchmark work directory printed by the Yukon CLI.
3. `yukon setup [--track <track>]`, then `yukon run` for the baseline.
   `elution best --set-baseline <score> --direction minimize|maximize`.

## Loop (until deadline)

Check `elution deadline` before each new iteration. `expired` means
finish the current measurement and stop. No new iteration after expiry.
There are no iteration caps and no consecutive-failure caps. The timer
is the only stop rule.

1. Spawn `researcher` + `web-researcher` in parallel for fresh context.
   Keep them read-only.
2. `lead` proposes exactly ONE change as JSON. It must first run
   `elution search "<keywords>" --top 8` and list `checked_ids`.
3. `reviewer` replies `approve|refine|reject` with reasons. `refine` or
   `reject` ends the iteration with no code change. It may set
   `suggest_research: true` to ask for more research next round. This is
   advice, never a counter.
4. On `approve`, `coder` makes the smallest diff inside `editablePaths`
   (Yukon) or the agreed scope (other repos). `git status --short`
   before measuring.
5. Main agent runs the benchmark (`yukon run [--track <track>]` or the
   repo's measure command). Save raw output to
   `.elution/iterations/iter_NNN/raw.log`.
6. Compare against `best.json`. Update `best.json` silently on any
   improvement. Submit to Yukon only when the new score beats the best
   so far by more than 0.10%, or once at the end if the final best
   clears that bar. Below 0.10%: record, never submit.
7. Append records with `elution add --kind <kind> --text "..."
   --source "<url|agent>"`. Link them: knowledge supports hypothesis,
   hypothesis tested_by experiment, experiment produced measurement.
   Mirror Markdown appears automatically under `.elution/memory/`.

## Memory rules

Never feed the whole DB to context. Only these compact lines:

```bash
elution search "sparse carry path" --top 8
elution search "constraint" --top 8 --kinds constraint
```

Every record needs `text` plus `source`. Web findings need a real URL
from native websearch/webfetch tools. No URL, no invented facts: return
`blockers` instead. Secrets (keys, tokens, private paths) never enter
memory or submission notes.

## Submit checklist (Yukon)

- `yukon benchmark show`, `yukon submissions --all` (frontier may move).
- `git status --short` clean except intended `editablePaths`.
- Exact `--model "Claude Opus 4.8"` style attribution plus
  `--harness "OpenCode"`; effort level in the note body.
- Note file 5 KiB–100 KiB from `templates/submission-note.md`.
- Prefer `yukon sync --harness-only` for harness updates. Normal
  `sync`/`reset` and any `--force` need saved work + explicit approval.
- On deadline: finish current measurement, submit if the >0.10% bar is
  met, write `.elution/handoff.md` for the next shift, stop.
