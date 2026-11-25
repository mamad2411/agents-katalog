---
name: statusline
description: Wire the Claude Code status line to the quota watchdog, so quota data comes from every model reply instead of a `claude -p` probe. Installs a stable wrapper into ~/.claude/settings.json that finds the newest installed plugin version and keeps the human's existing status line. Dry run first, writes only after the human's yes; --uninstall restores the previous status line. Invoked by the human as /dark-factory:statusline.
argument-hint: "[--uninstall] [--feed-only]"
disable-model-invocation: true
---

# /dark-factory:statusline — the quota feed in the status line

The quota watchdog (`docs/quota-guard.md` of this plugin) reads the subscription's 5h/7d usage either from a short
`claude -p` probe or, for free, from the JSON Claude Code hands the status-line command after every model reply. This
command wires the second. The mechanics are one script, `${CLAUDE_PLUGIN_ROOT}/scripts/statusline.py`; this skill
is the dry run and the "yes".

**This command is for Claude Code only.** Under Codex there is nothing to wire, so tell the human that and stop:
- the watchdog reads Codex's quota from `codex app-server` (`account/rateLimits/read`), which costs nothing;
- Codex's own `/statusline` can show the rate limits.

## Rules

1. **Dry run first, then write.** Show the dry-run output to the human; write only after an explicit "yes".
2. **A user file.** The script edits `~/.claude/settings.json` (or `$CLAUDE_CONFIG_DIR/settings.json`): only the
   `statusLine` key, everything else stays. Do not edit that file by hand instead.
3. **The human's status line stays.** The previous `statusLine` command is saved and chained by the wrapper; its
   output comes first. A previous hand-wired `quota.py statusline` feed is replaced, not chained.

## Steps

1. Dry run (the arguments, if any, are passed through):
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/statusline.py" $ARGUMENTS
   ```
   Show the human: the settings file, the wrapper path, the status line that is kept, the old → new `statusLine`.
   `--feed-only` feeds the watchdog without adding a quota line to the status line.
2. After "yes", the same command with `--apply`.
3. Check: the next model reply refreshes `~/.cache/claude-quota.json` with `"source": "statusline"`
   (`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/quota.py" status` prints the line). Plugin updates need no rerun: the
   wrapper (`~/.claude/dark-factory/statusline.sh`) looks up the newest installed version each time.

`--uninstall` (dry run, then `--uninstall --apply`) restores the previous `statusLine` and removes the wrapper.
