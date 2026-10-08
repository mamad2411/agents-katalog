---
name: workflows-driven-development
description: "Dynamic build workflow: plans a goal into tasks, builds each test-first, and reviews every step."
argument-hint: "<goal> | --tasks <file> | help"
disable-model-invocation: true
---

# /workflows-driven-development

User-only entry to the **ultrapowers** harness. Spends real tokens → never auto-invoked.
You (the model running this command) own the two human gates and dispatch the deterministic
Workflow engine. Do **not** re-implement the loop, dispatch the engine.

## Usage
```
/workflows-driven-development <goal>                 plan → build the planned tasks → stop
/workflows-driven-development <goal> --thorough      + completeness-critic loop until clean (GOAL MODE ONLY)
/workflows-driven-development --tasks <tasks.json>    advanced: run a pre-decomposed [{id,spec}] list
/workflows-driven-development help                   modes, cost, task-list format
```

## On `help`
Print the Usage block above, then: "default = one disciplined pass; `--thorough` adds a
completeness critic that loops until no new findings (goal mode only). Built-in always-on:
strict TDD, merged opus review (spec + quality, fail-closed), re-witness RED, per-task commit. Task-list
format: see `${CLAUDE_PLUGIN_ROOT}/reference/task-list.md`. Cost scales with task count, each task runs an implementer plus one merged opus review (plus re-witness RED)." Then stop.

## Workspace isolation (do first, before any gate)
If the target repo is on `main`/`master`, create a feature worktree/branch first
(`EnterWorktree` or `git checkout -b feature/<goal-slug>`). The harness commits per task.

## GATE 1, plan approval (goal mode)
For a `<goal>`: dispatch planning only, then present the task list to the human.
```
Workflow({ scriptPath:'${CLAUDE_PLUGIN_ROOT}/workflow/ultrapowers-development.js', args:{ goal:<goal>, planOnly:true } })
```
Show the proposed tasks and ask: **Approve this plan / edit / abort?** Do not build until approved.
> A Workflow cannot pause mid-run (ADR-0001), so approval happens *before* the build dispatch.

For `--tasks <file>`: **validate first.** Read the file; if any entry is not a
`{id,spec}` object, **reject** with: "tasks must be `[{id,spec}]` objects, bare strings are
silently dropped (see `${CLAUDE_PLUGIN_ROOT}/reference/task-list.md`)." If `--thorough` was
also passed, **warn**: "`--thorough` is ignored in --tasks mode (the completeness critic runs
in goal mode only)." Then skip to dispatch.

## Dispatch (the build)
Default args (product defaults, `implementer:"claude"` so a clean install needs no external CLI):
**Source `verifyCmd`** from the project's real test command (read its `package.json` scripts and any `CLAUDE.md`). Without it the deterministic gate is skipped and re-witness RED goes inert, if the project genuinely has no test command, say so at GATE 1 rather than silently running degraded.
```
Workflow({ scriptPath:'${CLAUDE_PLUGIN_ROOT}/workflow/ultrapowers-development.js', args:{
  // one of:
  goal:  <approved goal>,            // goal mode
  tasks: <validated [{id,spec}]>,    // --tasks mode
  repoDir: '<abs path of the build dir>',
  verifyCmd: <the project's test command>,
  implementer: 'claude',
  implModel: 'sonnet',
  commit: true,
  loopUntilClean: <true only if --thorough AND goal mode>,
  logFile: '<repoDir>/.claude/ultrapowers-run.jsonl',
  maxRounds: 3, maxTasks: 50
} })
```
> **Why `scriptPath`, not `name`:** the engine is intentionally NOT registered in
> `~/.claude/workflows/`, so it stays out of the slash list and the model can't dispatch it
> directly (`Workflow({name})`), which would bypass the two human gates. `scriptPath` resolves
> the bundled engine straight from the plugin and needs no registration.

## GATE 2, critical review (on return)
Surface the final JSON + the per-model token/cost report. If the result sets
`needsHuman:true`, `integration.approved === false`, or a `stopped`/`degraded`/`BLOCKED`
flag, present it and ask: **accept / send back / raise the model ceiling?** Otherwise report
the green summary (tasks built, tests, re-witness outcomes).

## Reference (Read on demand, don't preload)
- task-list format + footgun → `${CLAUDE_PLUGIN_ROOT}/reference/task-list.md`
- engine args + model routing → `${CLAUDE_PLUGIN_ROOT}/reference/harness.md`
- re-witness RED (mechanism + evidence caveat) → `${CLAUDE_PLUGIN_ROOT}/reference/re-witness-red.md`
- deterministic gating/escalation → `${CLAUDE_PLUGIN_ROOT}/reference/gating.md`
