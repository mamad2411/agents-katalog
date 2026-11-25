---
name: uninstall
description: Undo what /svipall:setup changed on this machine — the global memory block, strict mode, and the MCP registration — and optionally remove the Svipall binary and its data. Use when the user runs /svipall:uninstall, or asks to remove, disable or undo Svipall.
---

# Undo the Svipall setup

Ask which of these to do, then do only those. Report each one afterwards. **Never delete
`~/.svipall` without an explicit yes**: it holds logged-in browser profiles, learned tiers and the
page cache, and none of it comes back.

## 1. The global memory block

In `~/.claude/CLAUDE.md`, remove the block between `<!-- BEGIN SVIPALL -->` and
`<!-- END SVIPALL -->`, inclusive, and nothing else. Back the file up first
(`~/.claude/CLAUDE.md.bak-<YYYYMMDD-HHMMSS>`). Then delete `~/.claude/svipall/SVIPALL.md` and the
`~/.claude/svipall` directory if it is now empty.

If the markers are not there, say so and change nothing.

## 2. Strict mode

Delete `~/.svipall/claude_strict`. Claude Code's `WebFetch` and `WebSearch` stop being declined
immediately; no restart. If the file is not there, strict mode was already off.

## 3. The plugin itself

`/plugin uninstall svipall@svipall` removes the plugin, its skills, its hook and its MCP entry. If
the MCP server was registered separately by hand, that entry is still there:
`claude mcp remove svipall` — check `claude mcp list` first and say what you found.

## 4. The binary (only if asked)

Whichever way it went on:

| Installed with | Removed with |
|---|---|
| `install.sh` / `install.ps1` | the same script with `--uninstall` |
| Docker | `docker rmi ghcr.io/ilien-dev/svipall:latest` |
| a package manager | its own uninstall command, once those channels exist |

The installers only ever wrote to a user-owned directory and the user's own PATH, so nothing needs
elevation to undo.

## 5. The data (only if explicitly asked, and confirm again)

`~/.svipall` — profiles, cookies, cache, learned tiers, the captcha corpus, the downloaded browser.
Deleting it is permanent. Say what is in it before deleting, and say `SVIPALL_HOME` may point
somewhere else on this machine.
