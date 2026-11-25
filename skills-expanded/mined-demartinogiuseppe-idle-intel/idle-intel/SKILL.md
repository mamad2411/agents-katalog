---
name: idle-intel
description: Turn Claude Code's wait-state status line into useful micro-briefings about the current project (security vulns, outdated dependencies, unpushed commits, stale branches, TODO/FIXME debt) instead of a generic spinner. Use this skill whenever the user wants to set up idle-intel, customize their Claude Code status line, "make waiting useful", monetize or enrich agent wait time, see project health at a glance, or mentions spinner customization, statusLine configuration, or wait-state productivity. Also use it to add new intel collectors or adjust rotation timing.
---

# idle-intel

**The status line is the most-watched line on a developer's screen while an agent thinks. Today it says "Thinking...". It could say something worth knowing.**

idle-intel replaces the empty wait state with a rotating micro-briefing about the project the user is *already working on*: known vulnerabilities, major dependency updates, unpushed commits, forgotten stashes, stale branches, accumulated TODO/FIXME debt. One line at a time, changing every 12 seconds, zero interruption to the workflow.

Design principle: the wait state is valuable *because* it is empty. So each insight must be glanceable (one line), local (about *this* project, not the world), and silent when there is nothing to say. Never a feed, never an ad, never a distraction.

## Architecture

```
idle-intel/
├── SKILL.md
└── scripts/
    ├── collect.py      # scans the project, writes insights to a cache (slow path, background)
    └── statusline.sh   # reads one cached line, rotates by time (fast path, <50ms)
```

Two-speed design is mandatory: the statusline command runs constantly and must never do heavy work. `collect.py` does the scanning (npm audit, pip outdated, git checks, TODO grep) and writes to `<project>/.claude/idle-intel/cache.txt` with an atomic swap. `statusline.sh` only reads the cache and triggers a background refresh if it is older than 30 minutes.

## Installation (what to do when the user asks to set it up)

1. Copy `scripts/` somewhere stable, e.g. `~/.claude/idle-intel/`:
   ```bash
   mkdir -p ~/.claude/idle-intel
   cp scripts/collect.py scripts/statusline.sh ~/.claude/idle-intel/
   chmod +x ~/.claude/idle-intel/statusline.sh
   ```

2. Wire it into Claude Code's status line in `~/.claude/settings.json` (merge with existing settings, do not overwrite the file):
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "~/.claude/idle-intel/statusline.sh"
     }
   }
   ```

3. Prime the cache for the current project so the first status line is instant:
   ```bash
   python3 ~/.claude/idle-intel/collect.py .
   ```

4. Tell the user to restart Claude Code (or start a new session). During the next wait state they will see lines like:
   ```
   ◈ npm audit: 2 high severity vulns -> run `npm audit fix`
   ◈ git: 3 unpushed commits on this branch
   ◈ 14 FIXME markers in the codebase -- oldest debts bite hardest
   ```


### Windows (Git Bash) specifics

On Windows, three things differ. Apply all of them when the user is on Windows:

1. Python is `python`, not `python3` (scripts auto-detect by trying `python3` then `python`, skipping the Microsoft Store `python3` stub that exists but does not run).
2. Claude Code executes the status line command OUTSIDE Git Bash, so `C:\Windows\System32\bash.exe` (WSL) may shadow Git's bash, and quoting "Program Files" breaks. Solution: generate a `.cmd` wrapper next to the scripts:
   ```bat
   @echo off
   "C:\Program Files\Git\usr\bin\bash.exe" "C:\full\path\to\statusline.sh"
   ```
3. Point `settings.json` at the wrapper using forward slashes: `"command": "C:/full/path/to/statusline.cmd"`.

Always back up an existing `settings.json` and MERGE the statusLine block into it -- never overwrite the user's plugins/marketplaces configuration.

Requirements: `bash`, `python3` (stdlib only). `npm`, `pip`, `git` are each optional — collectors skip silently when a tool or manifest is missing.

## Adding a new collector

Each collector in `collect.py` is a function `(root: Path) -> list[str]` registered in the tuple inside `main()`. Rules:

- Return at most ~3 lines; the cache is a briefing, not a report.
- Never raise: wrap external calls with the provided `run()` helper, which times out and returns `None` on any failure.
- One line = one complete, glanceable insight with a concrete next action where possible.
- Local project facts only. No network calls beyond the package managers' own checks.

Good candidate collectors to suggest if the user wants more: license conflicts in deps, test count vs. last-run status, `Cargo.toml`/`go.mod` support, changelog highlight for the most recently bumped dependency, largest file added in the last week.

## Uninstall

Remove the `statusLine` block from `~/.claude/settings.json` and delete `~/.claude/idle-intel/`. Per-project caches live in `<project>/.claude/idle-intel/` and can be deleted freely.
