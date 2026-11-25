---
name: help
description: all /lore intents, examples, and setup
---
<!-- tested with: claude code v2.1.81 -->

# /lore help

## what you can ask

| intent | examples |
|---|---|
| dashboard | `/lore` or `/lore today` |
| costs | `/lore how much have i spent` or `/lore cost this month` |
| value/ROI | `/lore value` or `/lore roi` |
| search | `/lore search "websocket"` or `/lore find auth bug` |
| cache | `/lore cache hit rate` |
| projects | `/lore top projects` or `/lore project myapp` |
| tools | `/lore top tools` |
| models | `/lore compare models` |
| mistakes | `/lore mistakes` or `/lore wasted sessions` |
| hotspots | `/lore hotspots` or `/lore most edited files` |
| loops | `/lore loops` or `/lore where am i stuck` |
| workflows | `/lore tool chains` |
| compare | `/lore compare this week vs last week` or `/lore project-a vs project-b` |
| project detail | `/lore project myapp` or `/lore about myapp` |
| story | `/lore story of myapp` or `/lore history of myapp` |
| health | `/lore health` or `/lore stats` |
| time filter | `/lore this week` or `/lore january` |
| backfill | `/lore backfill` or `/lore refresh` |
| watch | `/lore watch` or `/lore every 30 minutes` - scheduled dashboard |
| freeform | `/lore anything else` - builds a query from your question |

## scope

`/lore` auto-detects your scope based on the current directory:
- **project** - if your cwd matches a project in lore.db, defaults to just that project
- **global** - if no match, shows all projects

say "global" or "project" to switch. the scope shows in the freshness line at the top of every output.

## data

all data comes from `~/.claude/lore/lore.db`, a local sqlite database built from your claude code session logs at `~/.claude/projects/`.

- dollar amounts show **API inference value** (what your usage would cost at published per-token rates), not what you actually pay on a subscription
- all counts exclude subagent sessions by default
- use `/lore backfill` if data seems stale

## setup

if you don't have a database yet, just run `/lore` - it'll walk you through setup.
