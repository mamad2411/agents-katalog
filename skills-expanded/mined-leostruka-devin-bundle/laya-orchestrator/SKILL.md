---
name: laya-orchestrator
description: Use when a cheap typed check beats reading files into context - batch file classification (contains auth data? has tests?), review risk scoring, or pre-dispatch triage. Laya ranks and abstains, never proves - it is not a substitute for reading primary sources (Rule 12).
---

# Laya Orchestrator

`laya` is the bundle's System-1 decision engine: typed answers
(`choice`, `score`, `noul`) in one forward pass, offline, free. This
skill teaches WHEN to interrogate it and how to treat the answers.
Contract modes (`off|shadow|assist`) and the resident daemon are in
`.devin/research/LAYA_MASTER_ARCHITECTURE.md`.

## When to interrogate

| Situation | Call |
|---|---|
| >10 files + one boolean question ("contains auth data", "has tests") | `ask_laya_glob` / `ask_laya_filebool` (filebool-v1) |
| "Is this command risky?" before a non-trivial exec | already gated by `laya-guard` hook (cmd-risk-v1) |
| "Is this diff risky?" before review | review-risk-v1 (planned consumer) |
| "Which subagent?" / "which effort?" | agent-route-v1: shadow only until calibrated; Rule 20 decides |
| A recurring yes/no assumption you keep checking | propose promotion to a frozen contract profile |

Muscle calls (run inside `extensions/laya-tools/` via its `.venv`):

```bash
.venv/Scripts/python filebool.py --glob "src/**/*.py" \
    --question "contains authentication data"
.venv/Scripts/python laya_cli.py predict --state '{"body": "..."}' \
    --questions-file q.json          # ad-hoc advisory only
```

## When NOT to interrogate

- The fact is directly checkable with `read`/`grep`/`exec` → verify,
  don't ask (Rule 12). Laya answers *what to read first*, never
  *what the fact is*.
- Fewer than ~10 files: reading them is cheaper and certain.
- Binary/unreadable files: they abstain anyway.

## Output doctrine

- `abstain` = "check it yourself", never silently dropped from the
  result map.
- `yes`/`no` = reading-order priority, not a conclusion. Never cite a
  Laya verdict to the user as evidence without tool verification.
- `confidence` is entropy-based, not calibrated accuracy; thresholds
  come only from the profile's own calibration.

## Fencing (Camada 10)

`laya_cli.py predict` with ad-hoc questions is advisory: its output
MUST NOT feed hooks, policies, or gating scripts. If a question
recurs, promote it to a frozen `-vN` profile in decision_contract.

## Layer 7: LAYA-GATE notices

The `compact-gate` hook injects a one-line `LAYA-GATE` directive when
pressure and trajectory warrant it (prune | fold | handoff | clear).
Execute it inside the current turn, never mid tool-batch:

- `prune` → run `extensions/laya-compactor/compact.py` on the session
  transcript.
- `fold` → offload >50k-token artifacts to files (`context-folding`).
- `handoff`/`clear` → invoke `handoff` skill, then `clear`.

## Cost table

| Call | Cost |
|---|---|
| filebool per file | ~200-460 ms CPU on daemon; zero bytes of content into context |
| laya-guard | <50 ms amortized (T0/T1 tiers absorb most exec calls) |
| compact-gate eval | ≤1 per 8 tool calls below 70% pressure; every call above |
