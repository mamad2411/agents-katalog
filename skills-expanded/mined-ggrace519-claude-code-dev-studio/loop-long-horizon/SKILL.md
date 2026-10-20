---
name: loop-long-horizon
description: Long-horizon loop kit. Use when a task will outlive one context window — unattended runs, multi-session features, or any "keep going until it's all done" request; sets up durable state files and a one-task-per-iteration loop.
---

# Long-Horizon Loop

Context windows end; tasks don't. Work that spans sessions survives only if its state
lives in files the next fresh context can rebuild from — and fails predictably when an
agent tries to carry it in conversation memory instead. This loop is the kit for
unattended runs and multi-session features.

## When to reach for this

- A feature list or spec is too large for one session
- An unattended loop is being set up (a `while` loop, a Stop-hook loop, an overnight run)
- Resuming work in a fresh session and reconstructing "where was I"
- A session is being ended deliberately partway through a larger effort

## Iron law

**The loop's memory is files, not context — and each iteration takes exactly one
task.** A second task in the same iteration is the first step toward a half-finished
tree nobody can resume. The two halves do not trade: verifying the first task
properly does not earn a second one, and no amount of remaining context changes
the count.

## Setup (once, before the first iteration)

Create the state kit — templates in [references/state-files.md](references/state-files.md):

- **`feature_list.json`** — every unit of work, all `"passes": false` initially. JSON
  deliberately: models corrupt structured JSON far less readily than Markdown plans.
- **`progress.md`** — append-only log: what was done, why, what's next.
- **`init.sh`** — one command that proves the project still runs (build + smoke).
- **`PROMPT.md`** (unattended runs) — the per-iteration instructions, carrying the
  one-task rule, the completion promise string, and an iteration cap.

## The iteration

1. **Bootstrap ritual** — before touching code: `pwd`, `git log -5`, read
   `progress.md`, read `feature_list.json`, run `init.sh`. If `init.sh` fails, fixing
   that *is* this iteration's task.
2. **Pick ONE incomplete item** — the highest-priority `"passes": false` entry.
3. **Search before building.** Confirm the feature isn't already implemented; false
   "not implemented yet" is a documented failure mode of fresh contexts.
4. **Implement completely.** No placeholders, no stubs, no "simplified version for
   now" — stubbing is the documented long-run failure mode (compiling code is the
   model's reward signal, not working code).
5. **Verify with fresh evidence** (`loop-verify`), then flip the item to
   `"passes": true` — evidence first, flip second, never the reverse. Only the
   item's own verify command counts as evidence; "I watched it compile" or "I
   wrote it carefully" flips nothing.
6. **Append to `progress.md`** (what / why / next) and **commit**.
7. **End the context.** Fresh context per iteration beats compaction for long runs —
   compaction feeds "context anxiety": premature wrap-up as the window fills.

## Termination and recovery

| Condition | Action |
|---|---|
| All entries `"passes": true` | Emit the completion promise string; the loop harness stops on it |
| Iteration cap reached | Stop and summarize remaining work — never loop unbounded |
| Tree broken beyond this iteration's change | `git reset --hard` to last good commit and re-loop |
| Repeated drift from intent | Fix the spec/`PROMPT.md`, not the code — drift is a prompt bug |

## Rationalizations

| Excuse | Reality |
|---|---|
| "I can squeeze in a second task" | The second task is the one the context dies inside |
| "Verify this one properly, *then* continue to the next — best of both" | A fake bargain: verification guards the flip, ending the context guards the tree; neither buys out the other |
| "It basically works, mark it done" | An unverified `"passes": true` poisons every later iteration's trust in the file |
| "Continuing in this context saves re-reading" | It spends the window on history instead of work — the files exist to make re-reading cheap |
| "The plan can live in my head until the end" | There is no end of session, only an end of context |

## Pitfalls

- Keeping the work list in Markdown prose — models rewrite it destructively; use JSON
- A `progress.md` that records *what* but never *why* — the next session repeats the
  dead ends
- An `init.sh` that only builds — it must also prove the app minimally *runs*
- No completion promise or iteration cap on an unattended loop — unclear success
  criteria loop forever

---
*Related: `loop-verify` (the evidence bar for every flip), `loop-parallel` (fan-out
within one iteration), `loop-compound` (harvest learnings as you go) · output/ADR
format: `playbook-conventions`*
