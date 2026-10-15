---
name: ralphi
description: >
  Quality-loop discipline. Enforces a per-cycle token budget (setup → worker → verifier → commit → handoff phases) and runs a between-cycle philosophy auto-check via rg sweep over the diff. Halts on any introduced ROP / version-hardcoding violation. Etymology — "ralph" (from Ralph Wiggum, persistent retry) + "-i" (inspection).
  Triggers: "ralphi", "사이클 점검", "loop budget", "cycle gate", "philosophy sweep", "between-cycle check"
version: 0.1.0
ssl:
  scheduling:
    anti_triggers:
      - "Full inspection skill with file-type criteria + Necessity Check — use harnish:ralphi"
      - "Session-action gate before commit — use galmuri:self-audit"
      - "Completion-claim gate on UI / code — use galmuri:polish"
      - "SKILL.md SSL audit — use galmuri:skill-audit"
      - "First-cycle planning / scope definition — write the cycle goal manually first"
  structural:
    scenes: [Setup, Worker Dispatch, Verifier, Philosophy Sweep, Commit, Handoff]
    resumable: true
    resume_marker: "tmp/ralphi-state-<n>.json"
    branches:
      - "philosophy sweep finds violation → halt loop + surface to user before next cycle"
      - "any phase exceeds budget → write tmp/ralphi-state-<n>.json, pause; resume on user signal"
      - "Necessity Check Q1 or Q4 fail → tag item [warning] unjustified existence"
      - "fix would require new abstraction/module/feature → [unfixed] structural change required"
  logical:
    tools: [Bash, Read, Agent]
    side_effects:
      reads: ["git diff", "git diff HEAD~1", "tmp/ralphi-state-<n>.json when resuming"]
      writes:
        - "tmp/ralphi-state-<n>.json on phase-budget overflow or graceful pause"
        - "one commit per cycle (caller drives `git commit` — ralphi never batches cycles)"
      deletes: []
      network: []
    idempotent: false
    rollback: "Cycle commits are atomic; revert any single cycle with `git revert <cycle-sha>`. State file is overwritten each cycle — restore from prior `tmp/ralphi-state-<n-1>.json` if present."
---

# galmuri:ralphi — quality-loop discipline

> Etymology — *Ralph Wiggum* (The Simpsons): persistent retry until it works. The `-i` suffix marks the *inspection* family.

The lean discipline-gate version. Bounds token spend per cycle and forbids philosophy regressions from sneaking in between cycles. If you need the full file-type-aware inspection skill (criteria-prd / criteria-skill / criteria-script / criteria-code + Necessity Check), use `harnish:ralphi`.

If invoked bare (no cycle goal), ask: *"What is this cycle's narrow goal? e.g. `migrate 3 callers off legacy adapter`, `remove 5 dead exports` — name something verifiable in one cycle."*

## Cycle phases (budget pattern)

| # | Phase | Budget | What runs |
|---|---|---|---|
| 1 | Setup | ≤ 500 tokens | State the cycle goal in one sentence; list affected files via `rg -l` (not `rg`); confirm baseline branch + SHA. No file reads. |
| 2 | Worker Dispatch | ≤ 4 parallel sub-agents, each ≤ 2000 tokens out | Each worker emits `{file, change, 3-line summary}` — no full-file contents in worker output. |
| 3 | Verifier | ≤ 1000 tokens | One verifier sub-agent re-reads ONLY changed lines via `rg -A 3 -B 3 'pattern' <file>`; never full files. Apply the **Necessity Check** (below) per diff hunk. |
| 4 | Philosophy Sweep | ≤ 200 tokens | `rg` sweep across the new diff for ROP / version-name violations (below). Halt if any hit. |
| 5 | Commit | n/a | One commit per cycle. **Never batch multiple cycles into a single commit.** |
| 6 | Handoff | ≤ 300 tokens | 5-line summary: what changed, what verified, next cycle's narrow goal. Then advance counter or pause. |

If any phase exceeds its budget, write `tmp/ralphi-state-<n>.json` (cycle counter, goal, pending files, last verifier output) and pause. Next invocation resumes from that state.

## Necessity Check (Socratic 4 questions)

Apply to each diff hunk in the Verifier phase. Lifted from the original `harnish:ralphi` — the only inspection method that gates on *purpose* before *correctness*.

1. **Why** is this here? — *(purpose)*
2. **What** is it composed of? — *(composition, scaffold for Q1/Q4)*
3. **What is it really**, stripped of framing? — *(truth, scaffold for Q1/Q4)*
4. What happens **if it's removed**? — *(necessity)*

**Verdict.** Q1 and Q4 are the only gates. Q2 and Q3 are scaffolding to reach honest answers. Items failing Q1 or Q4 → `[warning] unjustified existence` (kept only by convention / inheritance / authority).

**Fix discipline.** Subtraction is the default. For `[critical/warning]`, minimal additive patches are allowed (null check, missing import, type fix, error guard). Do NOT introduce new abstractions, modules, or features. If a fix would require new abstraction/module/feature → tag `[unfixed] structural change required` and hand off to the user.

## Philosophy auto-check (between cycles)

Run between cycles, before advancing the counter. Halt the loop and surface to the user on any hit.

```bash
# ROP — defensive timeouts / silent catches added by this cycle
git diff HEAD~1 | rg -n 'withTimeout|timeout:\s*\d+|catch\s*\([^)]*\)\s*\{[^}]*//' \
  && echo "VIOLATION: possible ROP breach in last cycle"

# SSOT — hardcoded version-specific field names
git diff HEAD~1 | rg -n 'v\d+\.\w+|schema_v\d' \
  && echo "VIOLATION: possible hardcoded version"
```

Baseline note: `HEAD~1` assumes the previous cycle already committed. If running against a feature branch with multiple cycles, prefer `git diff $(git merge-base HEAD main)..HEAD` for the full branch range.

## Halt conditions

- Philosophy sweep hit → halt, surface, wait for user judgement
- Worker / verifier exceeds its phase budget → write state, pause
- Necessity Check tags `[unfixed] structural change required` → halt the autonomous loop, hand off to user
- Two consecutive cycles fail the verifier on the same hunk → halt (convergence failure)

## What this skill does NOT do

- ✗ Type detection + criteria-file matching (that's `harnish:ralphi`)
- ✗ Run tests by itself — assumes the caller's loop drives the runner
- ✗ Auto-fix philosophy violations — surfaces them for user judgement
- ✗ Replace `galmuri:polish` (completion-claim gate) or `galmuri:self-audit` (single-session audit)
