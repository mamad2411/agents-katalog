---
name: environment-maintenance
description: "Interactive hygiene pass over a Claude Code setup: MCP server health, installed plugins and their always-on token cost, file-sync conflict copies in the config folder, invalid settings files, heavy hooks, oversized CLAUDE.md or MEMORY.md, and which skills, commands, and agents are never used. Read-only until the user approves each fix. Use for periodic maintenance, when sessions feel slow or bloated, when an MCP server keeps failing, or after syncing the config between machines."
user-invocable: false
---

# Maintain: keep the Claude Code environment healthy

> Look first, change nothing until the user says so, and never delete: move to a dated trash folder instead.

## Paths

- Config folder: `CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"`
- SessionFlow home: `SESSIONFLOW_HOME`, else `home` in `${SESSIONFLOW_CONFIG:-$HOME/.claude/sessionflow.json}`, else `~/.claude/sessionflow`. Reports go to `<home>/reports/`, moved files to `<home>/trash/<YYYY-MM-DD>/`.

## Step 1: quick scan (read-only)

Run these and collect the results; each one is safe:

```bash
claude mcp list                                   # every MCP server with its health check
claude plugin list                                # installed plugins, enabled or disabled
find "$CFG" -maxdepth 4 -not -path "*/projects/*" \( -name "*.sync-conflict-*" -o -name "*conflicted copy*" -o -name "*.orig" -o -name "*.rej" \) 2>/dev/null
for f in "$CFG/settings.json" "$CFG/settings.local.json" .claude/settings.json .claude/settings.local.json; do [ -f "$f" ] && { jq empty "$f" 2>/dev/null && echo "ok $f" || echo "INVALID $f"; }; done
python3 ${CLAUDE_PLUGIN_ROOT}/bin/usage.py --recent 50
```

Size checks:

- `CLAUDE.md` files (user level `$CFG/CLAUDE.md`, the project's `CLAUDE.md`): `wc -l`. Every line loads into every session, so long files cost context on every turn.
- `MEMORY.md` in the project's auto memory folder (its path is in the session context when auto memory is on): `wc -l -c`. Claude Code loads only the start of it (up to 200 lines, about 25 KB); anything past that is silently not loaded.

## Step 2: present the scan and ask where to focus

A short table, one row per area, with a status of ok, warn, or fail and a one-line finding:

| Area | What counts as a problem |
|---|---|
| MCP health | A server that fails its health check or needs authentication |
| Plugins | A disabled plugin still installed, or an enabled one nobody uses |
| Sync conflicts | Any conflict copy in the config folder |
| Settings | A settings file that is not valid JSON |
| Memory and CLAUDE.md | MEMORY.md past the load limit; a CLAUDE.md long enough to crowd the context |
| Usage | Skills, commands, or agents never used in the scanned sessions |
| Hooks | Hooks that spawn heavy processes or make network calls (see Step 3) |

Then ask which area to work on: one area, several, or "full report".

## Step 3: act on the chosen area

### MCP health

For each failing server, `claude mcp get <name>` shows its configuration. Diagnose the likely cause (missing binary, expired auth, bad URL, missing environment variable) and propose the fix. Apply a fix only after a yes. Remove a server (`claude mcp remove <name>`) only when the user asks for exactly that.

### Plugins and token cost

`claude plugin details <plugin>@<marketplace>` prints a plugin's components and its projected always-on token cost. For plugins that cost context but never show up in the usage scan, suggest `claude plugin disable <plugin>@<marketplace>`. Disabling is reversible with `claude plugin enable`.

### Sync conflicts

For each conflict copy, show `diff` between the copy and the original it shadows. Propose, per file: keep the original, keep the copy, or merge. On approval, apply the choice, then move the conflict copy into `<home>/trash/<YYYY-MM-DD>/`, keeping its relative path. Never `rm`.

### Settings

For an invalid file, show the parse error (`jq . <file>` prints its line and column) and propose the corrected JSON. Write it only on approval, after copying the original into the trash folder.

### Memory and CLAUDE.md

For a MEMORY.md past the load limit, propose which entries to fold into topic files so the index fits. For a long CLAUDE.md, point at sections that are reference material and could move into a skill or an imported file. Show the proposed edit; apply on approval.

### Usage

From the usage report: list never-used skills, commands, and agents, grouped by where they live. Suggest archiving candidates (moving them out of the config folder into the trash folder), and never archive anything the user has not named. Point out that a skill used only by typing its slash command still counts as used.

### Hooks

Read the hooks in `$CFG/settings.json`, the project's `.claude/settings.json`, and those that installed plugins declare. For each hook command, check for:

- process spawning of formatters, linters, or test runners on every tool call
- network calls (`curl`, `git fetch`, package managers)
- platform assumptions (a Linux-only command in a config synced to a Mac)
- side effects (staging files, deleting, writing into the repo)

Classify each as keep (a light observer) or review (heavy or risky), and explain why. Hooks should observe and guard, not do invisible work. Propose leaner versions; change nothing without approval.

### Full report

Run every area's checks read-only and write `<home>/reports/maintain-<YYYY-MM-DD>.md` with the table from Step 2 and each area's findings. Print the path.

## Step 4: summary

- what was found
- what was fixed (and where anything moved)
- what is left, as a short list for next time

## Rules

- Read-only by default. Every change needs an explicit yes for that change.
- Move, never delete. The trash folder keeps relative paths so anything can be put back.
- Never print secrets. When showing MCP configs or settings, mask values of keys that look like tokens, keys, or passwords.
