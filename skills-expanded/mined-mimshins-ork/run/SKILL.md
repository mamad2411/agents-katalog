---
name: run
description: Use when starting, following or explaining an Ork run - what it's doing, why it failed, what it cost, and what waits on the person - and when the person asks about their Ork runs.
---

# Running and following Ork workflows

Ork runs workflows on the person's machine with their accounts, so a run spends
their money and can push, merge or deploy. Start one only when they ask, and
never answer a decision for them.

## Starting

1. Find it: Ork's `workflows` tool gives each workflow's name and inputs.
2. Check it first with `check` (`workflow: <name>`). Don't start one with an
   error.
3. Start it with `start_run`, giving every required input. Claude Code asks the
   person first, unless they've allowed it. It answers with the run's id; the run goes on in the
   background, whatever happens to this conversation.

Without Ork's tools: `ork run <workflow> --detach --input name=value`.

## Following

- `run` gives a run's status, what it waits on, its cost so far, and each
  node's state. `runs` lists the newest runs.
- `run_events` gives its newest events; `node` narrows them, and `last` or
  `after` widens them. A `node.finished` event with `ok: false` says why a node
  failed.
- `explain_context` says what a node's session was given: its agent,
  instructions, skills and files. Use it when a node didn't know something.
- `usage` says what runs spent, by workflow and model, and how close the limits
  are.

Say what you found plainly: which node, what it said, and what it cost. Quote a
node's own words rather than retelling them.

## What only the person does

- **Decisions.** `decisions` lists the questions waiting on them: a gate, a loop
  that ran out of rounds, a permission. Tell them what each asks, the options,
  and the recommended one, and that they answer in `ork ui` or with
  `ork decide` in their own terminal. Don't answer one: never run
  `ork decide --id … --choose …`; with Ork's plugin, a hook stops it.
- **Stopping, pausing, resuming.** Tell them the command: `ork stop <run>`,
  `ork pause <run>`, `ork continue <run>`, `ork resume <run>`. A node can be
  stopped alone with `--node <id>`.

## Without Ork's tools

| Want                   | Command                        |
| ---------------------- | ------------------------------ |
| Runs, newest first     | `ork ps`                       |
| A run's transcript     | `ork logs <run>` (`--follow`)  |
| Its nodes and cost     | `ork tree <run>`               |
| What runs spent        | `ork usage`                    |
| What waits on a person | `ork decide --list`            |
| A node's context       | `ork context explain <wf> <n>` |
