---
name: loopprism
description: Review coding-agent sessions with LoopPrism - what a session cost, what filled the context window, where the agent looped, failed or wasted tokens, what subagents did, and how to spend less. Use when the user asks about the cost, tokens, context, cache hits, loops, errors or efficiency of this session or of past sessions, or about spend across Claude Code, Codex, Gemini CLI, OpenCode, Cursor, DeepSeek Harness or WorkBuddy.
---

<!-- loopprism-skill -->
# LoopPrism

LoopPrism reads the session transcripts that coding agents keep on this machine (nothing is sent
anywhere) and answers: what did this session cost, where did the tokens and the time go, what went
wrong, and what would have cost less. Costs are estimates at API list prices.

## How to call it

If the `loopprism` MCP tools are available, use them:

| Question | Tool |
|---|---|
| Review a session (this one: `session: "current"`, `cwd`: your working directory) | `session_summary` |
| Find sessions, search past prompts and answers | `list_sessions` (with `query`) |
| Read the steps of a session, one event in full | `session_events` |
| What filled the context window (overall, or one `step`) | `session_context` |
| Subagents: what each was asked, returned and cost | `session_agents` |
| Spend across all agents, by model, project, day | `cost_overview` |
| Ways to spend less, with estimated savings | `find_savings` |

Otherwise run the same thing from the shell, always with `--json`, from the project folder:

```bash
npx -y loopprism show current --json        # session_summary
npx -y loopprism sessions --json -n 20      # list_sessions; `search <words>` to search
npx -y loopprism events current --kind tool_call,tool_result --json
npx -y loopprism context current --json     # add --step N for one step
npx -y loopprism agents current --json
npx -y loopprism cost --days 30 --json
npx -y loopprism optimize --days 30 --json
```

A session is `current` (newest session in the working directory), `latest`, an id, or a unique
id prefix. Subagent transcripts are `<session id>~<agent id>`.

## Showing the dashboard

When the user wants to *see* it (charts, the timeline, the context breakdown, the subagent flow, the
cost and optimize pages), open LoopPrism's dashboard in their browser: the `open_dashboard` tool,
or

```bash
npx -y loopprism ui current --detach      # a session id instead of `current`, or nothing for the list
```

It starts a local server in the background (127.0.0.1 only; it stops after an hour unused) and
prints the address. Tell the user the address; do not try to read the page yourself.

## Reviewing a session

1. Get the summary. Lead with the total cost, the main cost drivers (`cost.by_category`,
   `cost.by_model`) and how full the context is (`stats.current_context` against `stats.window`,
   `stats.cache_hit_pct`).
2. Go through `findings`: `repeated_call` (the same tool call with identical input; a loop),
   `error_streak` (tool errors in a row), `compaction` (context was summarized; detail was lost).
   Open the events they point at with `session_events` when the cause is not obvious.
3. Check `largest_tool_results`: big outputs are re-sent with every later step.
4. Turn `savings` into concrete advice for this project (e.g. a note in CLAUDE.md / AGENTS.md
   about a command that keeps failing, reading line ranges instead of whole files, starting a new
   session past ~100k tokens of context, a smaller model for simple tasks).

Keep the answer short: numbers first, then the two or three changes that would matter most.
Say that costs are estimates at API list prices; subscription plans bill differently.
