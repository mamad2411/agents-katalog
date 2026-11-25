---
name: setup-audit
description: Hygiene check for a coding-agent setup: finds unused, failing, duplicate and never-signed-in connectors, plugins and skills, measures startup cost, and trims them with the user. Use when asked to audit, clean up or optimize a setup, or when this repo is opened.
---

# setup-audit

You are setting this up **with** the user, not for them. They should end up understanding their setup: what was there, what it cost, what changed and why. Nothing changes until they approve a plan, and every change can be undone.

Talk plainly. Lead with numbers, then explain what they mean. Explain any jargon the first time it comes up.

## Phase 0: Set expectations (one short message)

Say what will happen: read-only inventory → a report on the current setup → a few questions → a plan → apply only what they approve → re-measure. It takes about 10 minutes, and measuring costs a few cents to about a dollar of API usage, which they approve separately.

## Phase 1: Inventory (read-only)

1. Back up: `B=~/.claude/backups/pre-audit-$(date +%Y%m%d-%H%M%S); mkdir -p "$B"; cp ~/.claude/settings.json ~/.claude.json "$B"/ 2>/dev/null`.
2. `python3 -I <skill>/scripts/inventory.py --live --json`: MCP servers per scope and disabled ones, plugins (skills, servers, hooks, uses), skills (auto vs manual, description size, uses), agents (with "MUST BE USED"/"PROACTIVELY" wording), commands, always-on vs path-scoped rules, memory index sizes, transcript history and median first-turn tokens. `--live` adds each server's connection status from `claude mcp list`, claude.ai connectors and plugin servers included. It launches every user-scoped and plugin server once (run from HOME, so project `.mcp.json` files are skipped); tell the user before running it.
3. Start from its `findings`: unused, failing, never-signed-in and duplicate servers (the same endpoint as a claude.ai connector and a local or plugin server), unused plugins, a skill listing over Claude Code's budget (descriptions past it get cut, so auto-picking breaks), oversized memory indexes and pushy agents. Check each one before you report it. Without `--live`, list claude.ai connectors from your own tool names (`mcp__claude_ai_<Name>__*`) and mark any that only expose `authenticate` as never signed in.
4. Other agents: `~/.codex/AGENTS.md`, `~/.codex/config.toml` (`[mcp_servers]`), `~/.gemini/GEMINI.md`, `~/.gemini/settings.json`, `~/.cursor/mcp.json`.
5. Their stack: project folders (`~/.claude.json` → `projects`) and what they're built with (package.json, Package.swift, pyproject.toml, go.mod…).
6. Ask before measuring. If they agree: `python3 -I <skill>/scripts/measure.py --cwd <their usual folder> --reps 2`.

## Phase 2: Report "Your setup today" (show it, explain it)

One message. Write it for someone who has never thought about context windows.

1. **Headline:** startup cost in tokens (measured, plus the interactive median from transcripts if there is one) and what that means. "Before you type anything, N tokens of instructions and tool names are already loaded. That's X% of a 200k window, and it gets resent with every message."
2. **Inventory table:** connectors (signed in / never signed in), MCP servers (user / project), plugins (and the skills they bring), skills (auto / manual), agents (pushy wording), always-on rules (KB), memory index (KB).
3. **What's costing the most**, ranked, with evidence. Usage counts over N days of history. Measured deltas where you have them (see *Reference numbers*), otherwise labeled estimates.
4. **What's working:** the things they use often. Say plainly that these stay.
5. **Caveats:** how much transcript history exists (default retention is 30 days, so "unused" is weak evidence), and that headless measurements undercount connectors.

## Phase 3: Interview (one question round, at most 4 questions)

Use the agent's question tool if it has one. Tailor the questions to what you found. Typical ones:
- What do you mostly build, and which agents do you use (Claude Code, Codex, Gemini, Cursor)? This decides which skills and rules to link and where `AGENTS.md` goes.
- Output style: concise only, or concise + i-have-adhd always-on? The ADHD flag injects its rules every session (measured at about 2.5k tokens).
- Borderline items you couldn't classify, such as a media generator or a payments sandbox: keep, scope to one project, or disable?
- Optional tools from `docs/TOOLKIT.md` that fit their stack: graphify for big unfamiliar repos, serena for large typed codebases, caveman `/ultracave` for very long sessions.

## Phase 4: Plan (tailored, one approval)

A table: change · why (evidence) · expected effect (measured / estimated) · undo. Group it:
1. **Clean up:** disable, scope to a project, make manual, archive, de-push (rules below).
2. **Install from this repo:** global instructions for their agents, the skills that match their stack (`./install.sh --skills a,b,c`), `personal_docs/` + global gitignore, settings merge.
3. **Optional tools** they said yes to.

Show `./install.sh --dry-run [--skills …]` output as part of the plan. Ask once for approval. They can strike rows.

### Classification rules

| Verdict | When | How |
|---|---|---|
| Keep | Used, or clearly matches the stack | nothing |
| Scope to project | Only one or two projects use it | project `.mcp.json` / project `enabledPlugins`; disable elsewhere |
| Make manual | Run by hand, never needs auto-pick | `disable-model-invocation: true` or `skillOverrides: {name: "user-invocable-only"}` |
| Disable | Never signed in, a duplicate, or unrelated to the stack | `/mcp` toggle (per project); claude.ai connector → disconnect on claude.ai to remove it everywhere |
| Archive | Unused, and overlaps a built-in or another skill | `mv` to `~/.claude/archive/{skills,agents}/` |
| De-push | Agent description says "MUST BE USED"/"PROACTIVELY" | rewrite as when it helps |
| Dedupe | Same endpoint loaded twice (claude.ai connector + local/plugin server) | keep the one with uses; remove or `/mcp`-disable the other |
| Trim index | A `MEMORY.md` over ~8 KB (it loads every session) | back it up, shorten each line to a hook, check that every link survives |
| Owner-only | claude.ai connectors and plugins synced from claude.ai | list them for the user to disconnect on claude.ai, or set `syncClaudeAiPlugins: false` |

Before archiving a skill, grep the kept skills for its name, since another skill may call it. Point those references at something kept. Plugin-bundled skills can't be hidden with `skillOverrides`. Disable or scope the plugin instead.

## Phase 5: Apply

- Archive with `mv`, never `rm`. Per-project MCP disables go through `/mcp`. If you edit `~/.claude.json` directly, write it atomically and warn that a running session may rewrite it on exit.
- Synced claude.ai content: `syncClaudeAiPlugins` / `syncClaudeAiSkills: false`.
- Install: `./install.sh [--skills …] [--no-plugins]`. It symlinks the repo into place, backs up whatever it replaces, and prints the backup path.
- Record what changed, with the backup path, in the agent's memory.

## Phase 6: Verify and explain the result

1. The user restarts their agent. Re-run `measure.py` with the same `--cwd` and `--reps`, and `inventory.py`.
2. Show a before/after table: startup tokens, connectors, servers, skills, agents, always-on KB. Use measured numbers only. If a change didn't move the number, say so.
3. Check that each disabled item is gone (`/mcp`, `/skills`) and that each kept server still answers one call.
4. Explain how to work with the new setup in 3–5 lines: `personal_docs/` gets created on their next project task, edits to the repo apply live, `setup-audit` can be re-run any time, and how to undo.
5. List anything only they can do, such as disconnecting a connector on claude.ai.

## Reference numbers (from this repo's experiments)

Headless `claude -p`, Opus, one machine, 2026-11-21. Details: `docs/EXPERIMENTS.md`.
- The floor is Claude Code's own system prompt and built-in tools: about 35k tokens.
- Connectors were the biggest variable: +3k to +13k headless (it depends on how many connect before the first request), and more in interactive sessions.
- i-have-adhd always-on: +2.5k. One plugin with 49 skills: +0.9k.
- Trimming skills, agents and rules alone: −0.2k. Do it for clarity and correctness, not for tokens.
