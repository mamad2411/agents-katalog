---
description: >-
  Diagnose and repair a compiled Amber program after a run stopped on a guard or the world
  changed (a renamed field, a new label taxonomy, a changed tool schema). Use when amber run
  exits with code 4, amber doctor reports degraded or broken, or the user says an Amber
  workflow broke.
when_to_use: >-
  Requests such as: the amber run stopped, amber doctor says degraded, my compiled workflow
  broke, fix the weekly report program.
argument-hint: "[workflow-name]"
---

# Heal an Amber program

A compiled Amber program refuses to guess. When a tool result no longer looks like the
recordings, a tool errors or a budget runs out, a guard stops the run. Nothing after that step
runs, and the run exits with code 4. Your job is to find out why and pick the cheapest repair.

## 1. Diagnose

```bash
amber doctor <workflow>
```

It probes the MCP servers (schema drift), reads the recent runs of the current program version
(result shapes, stop rate, llm health), checks staleness and lints `program.py`. It prints a
verdict (`healthy`, `degraded` or `broken`) and a recommendation. Exit code 5 means "not
healthy". Show the user the findings marked ✗ or ~.

For one specific run: `amber run` prints the stopped step and the guard, for example
`#3 shop.list_orders stopped $[0]: missing key 'total'`. `amber ui` shows the step timeline.

## 2. Act on the recommendation

| recommendation | what to do |
|---|---|
| `none` | Nothing. If a run stopped anyway, read its guard event: a budget stop is fixed in `amber.toml`. |
| `recompile` | `amber compile <workflow> --refresh`, then `amber verify <workflow>`. |
| `fallback` | Hand the stopped step back to the agent (below), then refresh. |
| `re-record` | The task itself changed. Record two or three fresh runs (see the `compile` skill). |

### Fallback (ask first: it runs the agent and may write)

```bash
amber run <workflow> --input <k=v> --allow-writes --fallback agent
```

The arbiter checks vetoes first: the daily fallback budget, writes already done, servers
unreachable. Then the agent is relaunched with the completed steps as context, with the same
`--model` and flags the recordings used. Its run is saved as a `fallback` trace. Then:

```bash
amber compile <workflow> --refresh    # new version from all traces, including the fallback one
amber verify <workflow>               # must pass on every trace
amber doctor <workflow>               # should now say healthy
```

Without `--allow-writes`, a fallback that still has writes to do is refused. That is the safety
rule, not an error.

## 3. Common causes

| symptom | likely cause | fix |
|---|---|---|
| `result_shape: missing key 'total'` | the server renamed a field | fallback, then refresh |
| `schema_drift` in doctor | a tool's input schema changed | fallback or re-record |
| `error` guard: tool rejected the arguments | a taxonomy or validation rule changed | fallback, then refresh |
| `budget: llm token budget exceeded` | a judgment needed more tokens | raise `[budgets].max_llm_tokens` (no recompile) |
| `llm_output` invalid or low confidence | a prompt is too weak for the new data | recompile, or edit the prompt in `program.py` and verify |
| `no model backend available` | no `claude` CLI login and no `ANTHROPIC_API_KEY` | log in or set the key |

## Exit codes

`0` ok · `1` error · `2` usage · `3` verify failed · `4` guard stopped the run · `5` doctor
found drift.
