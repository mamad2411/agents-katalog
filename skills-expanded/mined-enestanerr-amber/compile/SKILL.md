---
description: >-
  Turn a workflow the user keeps asking Claude to repeat (same steps, different inputs, MCP
  tools) into a compiled Amber program that runs it for a fraction of the tokens, with replay
  tests and guards. Use when the user wants to automate, schedule or compile a recurring agent
  task, or asks how to stop paying for the same agent run every day.
when_to_use: >-
  Requests such as: compile this workflow, make this repeatable, run this every Monday without
  the agent, automate this report, turn these runs into a program.
argument-hint: "[workflow-name]"
---

# Compile a repeated workflow with Amber

Amber records an agent doing a workflow a few times and compiles the recordings into a Python
program: deterministic code for the mechanical steps, small schema-validated `llm()` calls for
the judgment, replay tests generated from the recordings, and guards on every live call. Docs:
https://github.com/enestanerr/Amber

Work through the steps below with the user. Steps 3 and 7 cost the user's tokens or touch real
systems: ask before each of them.

## 0. Check the tools

```bash
amber --version        # missing? uv tool install amber-compiler
claude --version       # recordings run Claude Code headless (a claude.ai subscription is enough)
```

Model calls use a logged-in `claude` CLI, or the Anthropic API when `ANTHROPIC_API_KEY` is set.

## 1. Understand the workflow

Ask, or read from the conversation:

- Which MCP servers and tools does the task use? Amber compiles MCP tool calls. Ad-hoc shell
  commands and file edits do not compile, apart from a few safe builtins.
- Which values change from run to run? Those become declared inputs, such as `week=2026-W42`,
  `since=2026-10-27` or `repo=acme/api`. Aim for one to three.
- Which steps write something (post a message, add labels, send mail)? Those are dry-run unless
  the user passes `--allow-writes`.

If the work is "one call per item" (label every new issue separately), say that Amber 0.1 does
not collapse loops yet. A batch tool (one call with a list) compiles well.

## 2. Set up a project directory

```bash
mkdir my-workflow && cd my-workflow && amber init     # writes amber.toml and .amber/
```

1. In `amber.toml`, add one `[servers.<name>]` table per MCP server, with the same command the
   agent uses: `command = "uv"` and `args = ["run", "python", "server.py"]`, or `url = "http://..."`.
2. Write `mcp.json` in Claude Code's `--mcp-config` format with the same servers.
3. Write `task.md`: the prompt with `{input}` placeholders. Keep it tight. Name the tools, say
   what the output is, and end with "Use the <x> and <y> tools only." A vague task makes the
   agent take different paths in different runs, and those paths do not align.

## 3. Record three runs with different inputs (ask first)

Each recording is a full agent run on the user's account. Writes happen for real, so point the
servers at a sandbox if needed.

```bash
amber record <workflow> --input week=2026-W42 --mcp mcp.json \
  --allow 'mcp__shop__*' --allow 'mcp__slack__*' --permission-mode acceptEdits \
  -- claude -p "<task.md with the inputs filled in>" --model claude-sonnet-5-5 --setting-sources user
```

- Always pass `--model` explicitly, so a recording never runs on the user's default (possibly
  most expensive) model. The fallback later reuses the same flags.
- `--setting-sources user` keeps the project's `CLAUDE.md` out of the recording.
- `--allow` pre-approves the MCP tools. Recordings must run unattended: a permission prompt
  aborts them.
- Amber adds `--strict-mcp-config`, so only the servers in `mcp.json` are visible to the agent.
- If the agent read files instead of using tools, add `--disallowedTools Read,Glob,Grep`.

Use different input values each time. Identical runs give the compiler nothing to generalise
from.

## 4. Read the skeleton with the user

```bash
amber align <workflow> --show
```

Each step should be `deterministic` or carry one hole: `transform-needed` (code the model
writes) or `judgment` (a prompt and schema). Watch for:

- an *inferred input* the user did not intend: a value nobody could derive. Declare it with
  `--input`, or change the task.
- steps present in only one or two of three runs: the agent took different routes. Tighten
  `task.md` and re-record that run (`amber traces rm <id>`).
- pruned steps: exploratory reads nothing used. These are fine.

## 5. Compile, then review the program

```bash
amber compile <workflow>              # holes filled by the model, then replayed against every run
```

Open `programs/<workflow>/v<N>/REPORT.md` and `program.py` with the user. The program is
ordinary Python. Do not edit it silently. If the user changes it, `amber verify` must still pass.

## 6. Verify (free, no model calls)

```bash
amber verify <workflow>               # exit 3 if any recording diverges
```

## 7. Run it (writes only with consent)

```bash
amber run <workflow> --input <name>=<value>                  # write tools dry-run
amber run <workflow> --input <name>=<value> --allow-writes   # only after the user says yes
```

Report the step log, tokens, agent turns (should be 0) and the output. Exit code 4 means a guard
stopped the run: use the `heal` skill.

## 8. Schedule and monitor

```bash
amber schedule add <workflow> --cron "0 9 * * *" --input product=all   # fixed inputs only
amber scheduler                       # foreground loop that runs due schedules
amber doctor <workflow>               # drift report; exit 5 unless healthy
amber ui                              # local panel at http://127.0.0.1:8787
```

A schedule stores fixed inputs. When an input depends on the date (last week, yesterday), set up
a cron or CI job that computes it and calls `amber run`, for example
`amber run weekly-report --input week=$(date -d 'last week' +%G-W%V) --allow-writes`.

## Budgets and costs

`[budgets]` in `amber.toml` caps llm tokens per run, wall-clock time and the call count. The
budgets apply at run time, so raising one needs no recompile. Judgments default to
`claude-haiku-5-5` and synthesis to `claude-sonnet-5-5` (`[models]`). Do not switch them to a
larger model without asking.
