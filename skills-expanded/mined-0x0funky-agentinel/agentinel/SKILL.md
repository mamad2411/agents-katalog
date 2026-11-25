---
name: agentinel
description: Inspect this machine's live resource usage via the Agentinel CLI — find runaway / zombie / leaking AI-agent processes (Claude Code, Codex, Gemini, OpenCode, MCP & dev servers, Ollama…), duplicate sessions, heavy memory users, and reclaimable disk caches. Use when the user asks what's eating RAM/CPU/disk, whether they have forgotten or leaking agent sessions, which agents are still running, or wants a cleanup recommendation. Read-only — it never kills or deletes.
---

# Agentinel — local resource sentinel (CLI)

Agentinel ships a zero-overhead CLI (~12 MB, no WebView) that snapshots every
process on the machine, classifies AI-agent CLIs, and flags leaks / zombies /
duplicate sessions / heavy disk. Use it to answer "what's going on with my
machine right now" without guessing.

## When to use

Trigger when the user asks things like:

- "What's eating my RAM / CPU?" · "為什麼這麼吃記憶體?" · "什么最吃内存?"
- "Do I have any zombie or forgotten agent sessions?" · "有沒有忘了關的 agent?"
- "Which Claude / Codex sessions are still running?"
- "Is anything leaking?" · "What can I clean up on disk?" · "磁碟可以清什麼?"

## How to run

Run from the repo root (or anywhere `agent_monitor/` is importable). The wrapper
`./agentinel` auto-finds a sibling `.venv`; otherwise use `python -m agent_monitor`.
**Prefer `--json` for parsing**, fall back to the text table for display.

```bash
agentinel scan --json                 # whole-system snapshot (parse this)
agentinel scan --agents-only --json   # AI agents only
agentinel scan --top 50               # text table, top 50
agentinel advise                      # local AI CLI writes markdown advice
agentinel advise --engine codex       # pick the engine (claude|codex|gemini|opencode)
agentinel doctor                      # which AI CLIs are installed + fallback order
# (equivalently:  python -m agent_monitor <subcommand> …)
```

## What `scan --json` returns

`{ system, processes[], findings[] }`:

- **system**: `ram_used_gb`, `ram_total_gb`, `ram_pct`, `cpu_pct`, `swap_used_gb`, `swap_total_gb`
- **processes[]**: `pid`, `label`, `category`, `project`, `mem_mb`, `cpu`, `age_hr`,
  `idle_min`, `parent_name`, `parent_alive`, `ports[]`, `children`, `cmdline`
- **findings[]**: rule-engine anomalies — `{ severity, title, detail, pids, action }`

## How to respond

1. Summarize the 1–2 things that matter most (biggest RAM users, suspected leaks,
   idle zombies, duplicate sessions in the same project).
2. Cite concrete evidence: memory size/growth, `idle_min`, `parent_alive=false`,
   bound `ports`, child count.
3. Recommend **keep / end / watch** for each — but **do not kill or delete anything.**

## Safety

- `scan` / `advise` / `doctor` are **read-only**. There is **no** CLI kill or cleanup —
  do not invent one. Destructive actions (kill / suspend / disk cleanup) live only in
  the GUI's confirm-to-run flow (`python agentinel.py`). If the user wants to act, point
  them there, or ask for explicit confirmation before running anything destructive.
