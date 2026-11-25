---
name: ulw-loop
description: "[OMCP] Ultrawork loop that does not finish until the verifier (Oracle) confirms completion — parallel routing with a mandatory verification gate"
orchestrates-agents: "executor, debugger, designer, writer, test-engineer, verifier"
argument-hint: "[--max-iterations=N] [--strategy=reset|continue] <task description>"
level: 4
---

# [OMCP] ULW Loop — Ultrawork with Oracle Verification

[ULW LOOP - ITERATION {{ITERATION}}/{{MAX}}]

## What this is

`ulw-loop` is `ultrawork` parallel routing wrapped in a **mandatory
verification gate**. The work is not "done" when the executor says it is —
the work is done only when the `verifier` agent (the Oracle) confirms it.
Emitting a `<promise>DONE</promise>` opens the verification gate; it does
not close the loop.

This is the ultrawork variant with Oracle verification (max 500
iterations) for the Copilot CLI execution model.

## When to use

- "ulw", "ulw-loop", "/omcp:ulw-loop"
- "ultrawork until verified", "don't stop until oracle confirms"
- High-stakes parallel work where a premature "done" is expensive
  (refactors, migrations, multi-file fixes that touch shared invariants).

## When not to use

- Single-task work — delegate directly to an `executor` agent.
- Work that already has a PRD-shaped acceptance contract — use `/omcp:ralph`
  which is PRD-driven and already has verification baked in.
- Fire-and-forget parallel work where the user manages completion themselves
  — use `/omcp:ultrawork` (no gate).
- Diagnosis or root-cause work without an implementation deliverable — use
  `/omcp:debug` or `/omcp:trace`.

## Why this exists

`ultrawork` alone is parallel routing with no completion contract. The
executor can return early, leave hidden regressions, or claim done while
edge cases are unhandled. `ralph` adds a PRD-driven loop but requires
upfront story decomposition that is overkill for many tasks. `ulw-loop`
sits between them: parallel throughput + an Oracle gate, without
demanding a PRD up front.

## Execution contract

### The completion promise

When the orchestrator believes the work is complete, emit exactly this
inline token in the response:

```
<promise>DONE</promise>
```

The completion promise opens the verification gate. It does **not** end
the loop. The system continues until the Oracle confirms.

The default completion promise is `DONE`. Override via the skill's
optional `completion-promise=TEXT` flag.

### The Oracle verification gate (MANDATORY)

After the promise is emitted, dispatch the `verifier` agent with the
following payload:

```text
<oracle-task>
Task description (verbatim from user):
<user-task>
[the user's original ulw-loop task]
</user-task>

What was done (the executor's claim):
[summary the executor produced before emitting <promise>DONE</promise>]

Evidence the executor cited:
- files touched: [list]
- commands run: [list]
- output / diagnostics: [snippets or paths]

YOUR TASK (Oracle):
1. Verify each claim against actual repository state. Read the touched
   files. Re-run cited commands and inspect their output.
2. Identify any acceptance gap the executor missed (edge cases, regressions,
   stale references, undocumented changes, broken cross-module invariants).
3. Return one of:
   - VERIFIED — concrete evidence the work meets the user's request.
   - REJECTED — list the specific gaps. Each gap MUST be actionable
     (file:line or command + observation), not vague critique.

Do NOT modify files. Verification only.
</oracle-task>
```

If the Oracle returns **VERIFIED**: the loop ends. Report to the user with
the Oracle's evidence summary.

If the Oracle returns **REJECTED**: the loop continues. Feed the Oracle's
gap list back to the executor lane with one of two strategies (see
"Strategy" below). Re-iterate.

The Oracle is **not optional**. Emitting `<promise>DONE</promise>` without
the verifier dispatch is the most common failure mode — guard against it
explicitly in your todo list.

### Strategy

- **`--strategy=continue`** (default) — feed the rejection back to the
  same executor session via continuation. Preserves context; cheapest path.
- **`--strategy=reset`** — start a fresh executor delegation with the
  rejection added to the task. Use when the executor seems stuck in a
  failed pattern (3+ Oracle rejections on related concerns).

### Iteration limit

Default `--max-iterations=500`. Stop with a hard failure report if the
limit is hit:

```
ULW loop hit max iterations (N). Oracle's last rejection:
<paste Oracle's last REJECTED gap list>

The task did NOT pass verification. Do not silently mark complete.
```

Cancel anytime via `/omcp:cancel` (clears active mode + state).

## Run

1. **Restate the task** in one sentence so the executor and Oracle share
   scope.
2. **Identify parallel work units** the same way `ultrawork` does:
   dependency-aware, independent tasks fire in parallel waves.
3. **Dispatch the parallel wave** to executor / debugger / designer /
   writer / test-engineer agents as appropriate.
4. **Collect results** as each agent returns.
5. **Synthesize a completion claim** — what was done, files touched,
   commands run, observed output.
6. **Emit `<promise>DONE</promise>`** with the claim summary.
7. **Dispatch the Oracle** (see "Oracle verification gate" above).
8. **Branch on the verdict**:
   - VERIFIED → end loop. Report to user.
   - REJECTED → feed gap list back to executor (per strategy). Increment
     iteration counter. Re-iterate from step 3 if new work is required,
     or from step 5 if the executor only needs to address the gaps.
9. **State persistence**: store loop progress under
   `mcp__omcp__state_write` with key `ulw-loop/<slug>` so a follow-up
   session can resume on rejection.
10. **Stop** when Oracle returns VERIFIED, the user runs `/omcp:cancel`,
    or the iteration limit is hit (hard failure, no silent mark complete).

## Hard rules

- The verifier dispatch is **mandatory** after every `<promise>DONE</promise>`.
- Do NOT mark a task complete on the executor's word alone — that defeats
  the entire skill.
- Do NOT downgrade the Oracle to a "quick check" — the Oracle reads files,
  re-runs commands, and produces evidence.
- Do NOT delete failing tests or weaken acceptance to make the Oracle
  pass — that is the worst failure mode and the skill explicitly forbids
  it.
- Iteration limit is a hard stop — do not silently bypass it.

## Output format per iteration

```
[ULW LOOP - ITERATION K/N]

Parallel wave dispatched:
  - <agent>: <task>
  - <agent>: <task>
  ...

Wave results:
  - <agent>: <one-line outcome>
  ...

Completion claim:
  <one paragraph synthesis>

<promise>DONE</promise>

Oracle verdict: VERIFIED | REJECTED
  [if REJECTED]: gaps to address — <bulleted list>
  [if VERIFIED]: evidence summary — <bulleted list>
```

## Tools used

- Copilot's native delegation primitives for executor / verifier dispatch.
- `mcp__omcp__state_write` / `mcp__omcp__state_read` for loop state.
- `mcp__omcp__notepad_write_working` to track in-progress claims.
- `mcp__omcp__pipeline_record_transition` to log iteration boundaries
  (optional — useful for post-run audit).

## Differences from sibling skills

| Skill | Parallelism | Verification | PRD required | Loop until |
| --- | --- | --- | --- | --- |
| `ultrawork` | yes | none | no | user manages |
| `ralph` | yes | reviewer pass on PRD stories | yes | all stories verified |
| `ulw-loop` | yes | Oracle gate after each promise | no | Oracle confirms |
| `autopilot` | yes | ralph + extras | yes | pipeline completes |

`ulw-loop` is the lowest-ceremony skill that still guarantees
verified completion.
