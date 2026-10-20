# JARVIS OS

Build a personal AI operating system using Claude Code as the engine. Designed by @zoout.

## Stack

| Layer | Tool |
|-------|------|
| Engine | Claude Code (AI reasoning + execution) |
| Memory | Obsidian (markdown vault — persistent context) |
| Voice | Local Voice STT/TTS (speak to your OS) |
| Face | One HUD (dark terminal interface) |

## What It Does

- Pulls context from your Obsidian vault automatically
- Executes tasks via Claude Code
- Responds by voice (local STT/TTS)
- Displays everything in a single dark terminal HUD

## A Real Day With JARVIS

| Time | Command |
|------|---------|
| 7AM | "Morning brief." |
| 9AM | "Plan today." |
| 2PM | "Metrics pull." |
| 7PM | "Close the day." |
| Anytime | "Ask anything." |

## HUD Build Prompt

```
Build a dark terminal HUD for my OS: system vitals · command deck · schedule audio I/O · live data from the vault. One screen. No tabs.
```

## Setup Steps

1. **Install Claude Code** — `npm install -g @anthropic-ai/claude-code`
2. **Set up Obsidian vault** — create a vault at `~/vault/` as your persistent memory store
3. **Point Claude Code at the vault** — add vault path to your CLAUDE.md context
4. **Add local voice** — install [whisper.cpp](https://github.com/ggerganov/whisper.cpp) for STT + [piper](https://github.com/rhasspy/piper) for TTS
5. **Build the HUD** — use the prompt above with Claude Code to generate the terminal interface

## CLAUDE.md Snippet for Vault Memory

```markdown
## Memory
My Obsidian vault lives at ~/vault/. Always check it for context before answering:
- Daily notes: ~/vault/Daily/
- Projects: ~/vault/Projects/
- People: ~/vault/People/
- Goals: ~/vault/Goals/
```

## Daily Workflow Prompt

```
I am starting my [morning / workday / evening]. Check my Obsidian vault for:
1. Today's schedule and priorities
2. Any open tasks or projects
3. Metrics or KPIs I track

Give me a brief (morning brief / day plan / close-of-day summary).
```
