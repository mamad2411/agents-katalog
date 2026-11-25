---
name: oj-statusline
description: Multi-line Claude Code statusline with token breakdown (cached/new/total/ctx%), MCP and hook counts, and a soft-wrapped list of enabled skills highlighting the most-recently-active one. Augments oh-my-claudecode HUD when present, runs standalone otherwise. Trigger phrases - "install oj statusline", "oj statusline install", "/oj-statusline".
---

# oj-statusline

Single-file Node.js statusline for Claude Code. Drop-in for any machine with Node 18+.

## What it shows

```
tok cached:50.2k new:1.0k total:51.2k ctx:42% mcp:3x hk:5x
[OMC HUD line, if oh-my-claudecode is installed]
skills: line-check · oj-statusline · forge-council · ... [active: line-check]
```

Three layers, top to bottom:

1. **Token line** — context-window breakdown:
   - `cached` (cyan) — `cache_read_input_tokens`
   - `new` (yellow) — `input_tokens + cache_creation_input_tokens`
   - `total` (white) — sum
   - `ctx` (green/yellow/red @ 50/80 thresholds) — used percentage
   - `mcp:Nx` (magenta) — count of `mcp__*` tool_use blocks in last assistant turn
   - `hk:Nx` (gray) — count of `hook_*` attachments around the most recent user prompt

2. **OMC HUD line** — preserved when oh-my-claudecode plugin is installed; silently skipped otherwise.

3. **Skills line** (bottom) — magenta `skills:` label + cyan plugin names from `enabledPlugins`. Bolds the most-recently-used skill (detected via `Skill` tool_use OR `<command-name>` slash invocation parsed from transcript tail). Soft-wraps to terminal width.

> **Honest limit**: per-tool token attribution does not exist in transcript JSONL. `mcp:` and `hk:` are **counts**, not tokens.

## Why bottom-anchor the skills line?

Long plugin lists used to push token/HUD info off-screen on narrow terminals (half-width tile, side-by-side panes). Moving skills to the bottom keeps token data + HUD always visible regardless of plugin count.

## Install

Two commands inside Claude Code, then restart:

```text
/plugin marketplace add ojesusmp/claude-skills
/plugin install oj-statusline@claude-skills
```

Restart Claude Code. The plugin's `SessionStart` hook auto-runs `install.mjs` (idempotent) and the statusline activates on the next session start.

> **Note**: the SessionStart hook patches `~/.claude/settings.json` `statusLine.command` and copies the runtime to `~/.claude/hud/oj-statusline.mjs`. Both are reversible via the uninstaller below.

### Manual install (advanced / CI)

If you want explicit control or are scripting CI setup, run the installer directly:

```sh
node "$(find ~/.claude/plugins -path '*oj-statusline*install.mjs' | head -1)"
```

Check current state without changing anything:

```sh
node <path>/install.mjs --check
```

Uninstall (restores prior command if backed up):

```sh
node <path>/install.mjs --uninstall
```

## Verification

After install, restart Claude Code. Or test directly:

```sh
echo '{"context_window":{"current_usage":{"input_tokens":1000,"cache_read_input_tokens":50000,"cache_creation_input_tokens":2000},"used_percentage":42}}' | node ~/.claude/hud/oj-statusline.mjs
```

Expect 2 lines (token + skills). 3 lines if oh-my-claudecode HUD plugin installed.

## Files

- `SKILL.md` — this file
- `statusline.mjs` — the runtime (reads stdin, prints 2-3 lines)
- `install.mjs` — installer that wires `settings.json`
- `README.md` — full documentation
- `INSTALLATION.md` — install paths per platform
- `EXAMPLES.md` — sample outputs and color codes
- `CHANGELOG.md` — version history
- `LICENSE` — MIT

## Notes

- File at `~/.claude/hud/oj-statusline.mjs` survives plugin updates (lives outside the plugin cache).
- HUD delegation runs as `spawnSync` child process so its output is guaranteed to flush before the skills line is printed.
- Silent fail on malformed input — never breaks statusline rendering.
- Idempotency markers in source: `// PERMANENT - oj-statusline` and `// oj-statusline v1.0.0`.
