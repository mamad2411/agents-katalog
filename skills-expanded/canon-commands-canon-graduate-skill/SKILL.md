---
description: Graduate a repeated task or set of traces into a durable canon skill
argument-hint: "<task-name> [--iterations N] [--from-traces PATH]"
allowed-tools: [Read, Glob, Grep, Bash, Edit, MultiEdit, Write, Skill]
---

# /canon:graduate-skill

Route this slash command to the `graduate-skill` skill.

The user invoked:

```text
/canon:graduate-skill $ARGUMENTS
```

Parse `$ARGUMENTS` as:

```text
<task-name> [--iterations N] [--from-traces PATH]
```

- `<task-name>` (required) — the workspace under `.canon/graduation/tasks/<task-name>/`. If missing, ask for it.
- `--iterations N` (optional) — max iterations before forcing a convergence decision. Default to the skill's convergence rule when absent.
- `--from-traces PATH` (optional) — reuse existing run traces (e.g. a Browserbase workspace) as loop input instead of running the task fresh.

Steps:

1. If the workspace does not exist, scaffold it:

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/graduation/scaffold.sh <task-name>
   ```

2. Follow the `graduate-skill` skill exactly: run/ingest a trace, write a per-iteration report, make **one** bounded `strategy.md` change, re-run, and stop on the convergence rule (passes 2 of last 3 runs, or `--iterations` reached with documented limitations).
3. Graduate a self-contained `SKILL.md` under `.canon/graduation/tasks/<task-name>/graduated/` only when the convergence rule is met. Exclude traces, secrets, and unvalidated claims; wrap the fast path in protected-section markers.
4. Suggest `/canon:optimize` as the next step once an eval can be written — do not run it automatically.
