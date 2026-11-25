---
name: operate
description: Supervise a long-running, unattended agent run — an autonomous loop or a scheduled wake-up — that self-checkpoints against the repo's eval skills so it can't silently drift. Rides the platform's /loop + /schedule; adds halting guardrails (iteration cap, wall-clock budget, drift) and durable run state. Opt-in; not wired into the default pipeline. Use when a task needs many iterations or to run on a cadence without a human watching each step.
---

# /operate — run long, without silent drift

Goal: let an agent work unattended across many iterations (or wake on a schedule) and
**guarantee it halts** rather than drifting — spinning on a dead end, burning budget, or
quietly breaking the repo. This skill is the *discipline layer*: the platform `/loop` and
`/schedule` are the engine; `/harness-claude:operate` adds guardrails, durable state, and a drift check
wired to the harness's own eval skills.

> **Opt-in.** No default-pipeline skill or hook starts a run. Running long is always
> explicit. **Git boundary:** a run never commits or pushes unless you explicitly arm it
> for that in the objective; branch creation for the run's non-trivial work follows
> `rules/git.md` (branch-at-first-write).

## How it works
Each iteration the operator does one increment of work, then runs a **checkpoint**:
```
node scripts/operate/step.js --id <run-id> [--spec <path>] [--cmd '<check>' ...] \
     [--max-iterations <n>] [--max-fails <n>] [--budget-ms <n>]
```
`step.js` loads the durable run state (`.claude/runs/<id>.json`), runs the drift check —
`harness-claude:health` (test/lint pulse) and, when `--spec` is set, `harness-claude:eval`
(acceptance-criteria gate) — updates and persists state, evaluates the guardrails, and exits:
- **0 = continue** — schedule the next iteration.
- **1 = halt** — a guardrail tripped (`drift` | `budget` | `iteration-cap`); stop and report.
- **2 = usage/error** — fix the invocation (e.g. missing `--id`).

The state file is the **sole source of truth across firings** — each `/loop` firing may be a
fresh context, so iteration count, budget spent, and the consecutive-fail counter persist there
and resume automatically. Config flags are honored only when the run is first created; later
firings ignore them so counts accumulate rather than reset.

## Do this
1. **Frame the run.** Name a one-line objective, a `--max-iterations` ceiling, a drift
   threshold `--max-fails` (default 2 — one failure can be transient, two is a trend), and a
   `--budget-ms` wall-clock cap. Point `--spec` at the spec the run must keep satisfying when
   one exists (that arms the `harness-claude:eval` half of the drift check).
2. **Pick a trigger.**
   - **Interval / autonomous:** drive iterations with the platform `/loop` (fixed interval) or
     let the model self-pace; each firing advances the work one increment, then calls `step.js`.
   - **Scheduled / cron:** use the platform `/schedule` to wake on a cadence; each wake runs one
     checkpointed iteration.
3. **Supervise by exit code.** Continue on `0`; on `1`, stop the loop, read the printed summary,
   and surface the halt reason and the failing criterion — never restart blindly past a `drift`
   halt. Delegate the per-iteration work to the `harness-claude:loop-operator` agent.
4. **Report on halt.** Always end with the run summary: iterations run, budget spent, last
   verdict, halt reason. (`step.js` prints it; relay it.)

## Guardrails (each can HALT — priority: drift > budget > iteration-cap)
- **drift** — `--max-fails` consecutive failing checkpoints → stop and surface. The "can't
  silently diverge" guarantee. Outranks the benign ceilings. On a drift halt the **failing check
  itself** is recorded secret-safely in the eval artifact `.claude/eval/continuous/latest.json`
  (check name + command + pass, never output) — read it to see *what* failed after the fact.
- **budget** — wall-clock (`--budget-ms`) exceeded. *(Token/cost is best-effort in v1 — a plain
  `/loop` doesn't expose token spend; lean on wall-clock + iteration count.)*
- **iteration-cap** — `--max-iterations` reached.

> **`0` is a live cap, not "off".** `--max-iterations 0` halts before any work, `--max-fails 0`
> halts on the first checkpoint, `--budget-ms 0` halts at once. To *disable* a cap, omit the flag.

## Security & trust
- `step.js` shells the eval runners, which execute the repo's own check commands / spec `eval`
  fences with your privileges — same trust boundary as `harness-claude:health` /
  `harness-claude:eval`. Don't `/operate` a repo whose checks you don't trust.
- **Secret-safe:** the run state records only metrics, verdicts, and the halt reason — never a
  check's output (the eval runners stream output to the tty and capture nothing).

## Notes
- Self-contained: pure Node (`scripts/operate/{step,state,guardrails}.js`) + the existing eval
  runners. No new dependency, no new MCP server.
- Distinct from a one-shot `harness-claude:verify`: this is a *bounded, guarded, many-iteration*
  run with durable state.

## Exit criterion
A run has reached a clean halt (`done`, `iteration-cap`, `budget`, or `drift`) with its summary
reported, and on `drift` the failing criterion surfaced — never a run left silently looping.
