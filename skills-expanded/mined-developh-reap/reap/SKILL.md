---
name: reap
description: "Find and clean the zombie processes AI coding agents leave behind on macOS (orphaned claude, codex, cursor-agent, aider and opencode CLIs, detached MCP servers, Playwright and agent-browser Chromiums) and the node_modules of idle agent worktrees, with the reap CLI. Load when the Mac runs hot or slow, load average or swap is high, there are many leftover agent or MCP processes, a disk is filling up with git worktrees, or before killing agent processes by hand."
---

# reap

`reap` is a macOS CLI and LaunchAgent that terminates processes AI-agent wrappers leave behind. It decides by
ownership, not by CPU or memory: a process is only killed when no live terminal or agent host owns it and it has
stayed detached across several scans. Use it instead of `pkill` or `kill` on agent processes: a pattern kill also
takes out the MCP servers and browsers of sessions that are still running, including your own.

## Check what is there

```bash
reap --version || echo "not installed"
```

If it is missing, tell the person and offer to install it. Installing schedules a LaunchAgent that runs every
10 minutes, so ask first:

```bash
brew install developh/tap/reap && reap install
```

Without Homebrew: `curl -fsSL https://raw.githubusercontent.com/Developh/reap/main/install.sh | bash`.

## Diagnose before acting

Always start read-only. None of these kill anything:

| Command | Use it for |
|---|---|
| `reap` | Schedule, active rules, last runs |
| `reap preview` | Every matching PID with its verdict: kill-ready, quarantined or protected, and why |
| `reap top` | Kill-ready candidates sorted by memory |
| `reap doctor` | Scheduler loaded, app bundle intact, config sane, last run recent |
| `reap stats` | What it has cleaned this week and month, top targets |
| `reap logs` | Recent log lines (`-f` to follow) |
| `reap disk` | Idle agent worktrees whose `node_modules` and `.next` would go to the Trash |

Report the numbers to the person: how many kill-ready, quarantined and protected, and the memory involved.

## Clean

- `reap run` terminates the kill-ready processes now (SIGTERM, then SIGKILL only for survivors). Run it after
  `reap preview` and only when the person asked for a cleanup or agreed to it.
- A process in quarantine is not ready yet: it must stay detached for `DETACHED_GRACE_MINUTES`. Do not force it.
  Wait for the next scheduled sweep or check again later.
- A protected process stays. If the person wants it gone, it belongs to a live session: close that session.
- `reap disk run` moves dependency folders of idle worktrees to the Trash. It only touches linked worktrees with a
  clean `git status`, no git activity for `WORKTREE_IDLE_DAYS` and no process inside. It does nothing until
  `WORKTREE_ROOTS` is set in the config. Show `reap disk` first and say how many GB it would move.

## Configure

The config lives in `~/.config/agent-reaper/config.sh` (`reap config` opens it in `$EDITOR`). Rule tiers are bash
arrays of patterns: `ALWAYS_KILL`, `ORPHAN_ONLY`, `OLD_PROCESS`, `HEAVY_MEMORY`, `HIGH_CPU`, `DEDUPE`, `HOSTS`.
When editing it:

- Add the narrowest pattern that matches the leak, then confirm with `reap preview` that it matches what you expect
  and nothing else.
- Never remove the hard protections or try to work around them. They are not configurable on purpose: root is
  refused, only the user's own processes count, live terminal trees and agent hosts are protected, interactive
  browsers (Chrome, Safari, Arc and others) are never killed, and a rule matching more than 50 PIDs is aborted.
- After a change, `reap doctor` must pass.

## What not to do

- Do not `pkill -f claude`, `pkill node` or similar to free memory. Use `reap preview` and `reap run`.
- Do not run `reap` with `sudo`.
- Do not delete worktrees or their folders yourself: `reap disk run` moves only dependency folders, to the Trash.
- Linux is not supported yet. On Linux, say so instead of improvising.

Source and full docs: https://github.com/Developh/reap
Made by Tiago Rodrigues at Developh (https://www.developh.co), a design and development studio in Lisbon.
