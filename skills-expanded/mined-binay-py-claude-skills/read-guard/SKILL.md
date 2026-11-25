---
name: read-guard
description: Stop Claude Code from filling its context window with whole-file reads of huge files and log dumps. A PreToolUse hook that denies Read of files over ~800 lines / 80 KB without offset/limit, and `cat` / `type` / `Get-Content` of big files with nothing limiting the output (cd-aware), telling Claude to Grep and read a slice instead. Retrying the exact same call is allowed, so nothing is ever blocked for good. Use when the user hits usage limits fast, when claude-token-audit shows Read or Bash output dominating, or when they ask to make Claude Code cheaper.
---

# read-guard

`scripts/read-guard.mjs` is zero-dependency Node 22+. Every whole-file read of a 3,000-line file puts ~40k tokens into the context, and **every later turn re-reads them**. That's usually the single biggest avoidable cost (claude-token-audit shows it per tool).

## Install (ask the user first, it changes their settings)
If you installed the binay-skills plugin, this hook is already on (it ships in the plugin's `hooks/hooks.json`); turn it off with `"env": { "BINAY_SKILLS_HOOKS_OFF": "read-guard" }`. Otherwise, without the plugin:

Merge into `~/.claude/settings.json` (or a project's `.claude/settings.json`), using the absolute path:
```json
{ "hooks": { "PreToolUse": [
  { "matcher": "Read|Bash|PowerShell",
    "hooks": [{ "type": "command", "command": "node \"/ABSOLUTE/PATH/read-guard/scripts/read-guard.mjs\" hook" }] }
] } }
```

## What it does
| Call | Decision |
|---|---|
| `Read` of a text file > 800 lines or > 80 KB, without `limit` | **deny**. Claude is told the size and token cost and to Grep and then Read with `offset`/`limit` |
| `Read` with `limit` ≤ 800, images, PDFs, notebooks, binaries | allow |
| `cat` / `type` / `more` / `Get-Content` of a big file (follows `cd`, Git Bash `/c/...` paths, `2>&1`) | **deny**, with suggestions to use `grep -n`, `head`, `tail` |
| the same command piped into another program (`head`, `grep`, `jq`, `node script.js`…, but not `tee`/`cat`/`more`), redirected to a file, or `Get-Content -Tail/-TotalCount` | allow |
| **the exact same call repeated within 10 minutes** | allow (escape hatch: a file that really must be read whole costs one extra turn, never a dead end) |
| anything else, or any error in the hook | allow (fails open) |

Thresholds: `READ_GUARD_MAX_LINES` (default 800) and `READ_GUARD_MAX_KB` (default 80).

```
node read-guard.mjs test path/to/file [--offset 100 --limit 200]
node read-guard.mjs test-cmd "cat server.log"
```

## Limits
- It can't shrink output from other commands (test runners, builds). Tell Claude to pipe noisy commands through `tail -50` or use quiet flags.
- Deny reasons go to Claude, not to the user. The user only sees a slightly different tool call.
- Claude's Edit tool needs the file to have been read first. If a targeted Read isn't enough for an edit, Claude simply repeats the full Read and the escape hatch allows it.
