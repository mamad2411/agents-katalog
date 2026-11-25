---
name: speed-loop
description: Make burner's phone commands faster without breaking them - bench, trace, change, verify, compare, repeat. Use for any performance work on bin/burner, the u2 or scrcpy helpers, or recipes.
---

# The speed loop

Every speedup must ship in the package (first install or `burner update`).
Nothing hand-tuned on one phone or one computer.

## One round

Run these on a machine that reaches the phone: Muse's computer, or the
dev machine (see tools/README.md, "Benching from the dev machine").

```
burner update                       # or git pull in a checkout
bash tools/loop.sh                  # bench -> verify -> compare with last round
```

`loop.sh` runs a warm-up pass ("cold" column), then 3 timed passes, and
saves the results to `run/bench-history.jsonl`. Then it runs
`tools/verify.py` (scroll distance, a fresh read after a scroll, row taps,
dialog refusal, landscape taps, unique screenshot names), and
`tools/benchcmp.py`, which fails on anything 20% and 300ms slower or newly
failing. A red round is not pushed on top of.

## Finding where the time goes

```
python3 tools/tracesum.py --clear
BURNER_TRACE=json burner tap "Search settings"
python3 tools/tracesum.py --last 1
```

The waterfall shows adb calls, every fixed `sleep`, the u2 helper's RPCs
(dump, tap, shot) and "unaccounted" time. `tracesum --clear` also stops the
helper writing spans. `BURNER_TRACE=1` still prints plain lines on stderr.
`bash tools/linkbench.sh` times the raw link: one adb call costs 0.3-0.4s,
and 5 commands in one call cost the same as 1.

## What we already know (Oct 2)

- A screen read is about 1s and a capture about 1s on the phone itself.
  Below that needs a phone-side helper, not tuning.
- Batching shell commands into one adb call is the biggest lever left for
  anything that still shells out.
- Turning animations off made no measurable difference.
- The u2 swipe RPC (about 2s) is slower than an adb or scrcpy swipe.
- The first command after an update restarts the helpers, so it's slow once.

## Before pushing

- `python3 -m unittest discover -s tests` passes (the pre-commit hook does
  this; turn it on with `git config core.hooksPath tools/hooks`).
- A wrong tap decision gets a saved screen first:
  `burner dump --save tests/fixtures/<name>.xml`, then a case in
  `tests/fixtures/cases.json`. Watch it fail, then fix.
- Stage only your own files (`git add <file>`). Use your own worktree if
  another session shares the folder (tools/README.md).
