---
name: dashbar-status
description: Check Dashbar's status before heavy or parallel agent work, before starting a dev server, or before editing a folder. It shows plan limits and their pace, which coding agents are working or waiting, and which dev servers are running. Use on a Mac where the dashbar command is installed.
---

# Check Dashbar's status

[Dashbar](https://usedashbar.com/) is a macOS menu bar app that watches the person's coding agents (Claude Code, Codex, Gemini CLI, Antigravity, OpenCode, GitHub Copilot), their plan limits and their local dev servers. Its `dashbar` command prints what the app knows. It's read-only and cheap: it reads a file the app keeps up to date and never reads agent logs itself.

## When to check

- **Before heavy or parallel work**: a large refactor, a long run, or starting several subagents or workers. Plan limits decide how much you can do before the person is cut off.
- **Before starting a dev server**: one may already be running for this folder.
- **Before editing files**: another agent may be working in the same folder.
- When the person asks how much of their plan is left, or what their agents are doing.

Check at those moments, not in a loop. The app rewrites the status at most every 3 seconds.

## Run it

```sh
dashbar status --json
```

If `dashbar` isn't found, Dashbar or its command isn't installed: carry on without it, and don't install it unasked. Other exit codes: `2` Dashbar hasn't saved a status yet, `3` Dashbar isn't running, `4` the status file can't be read. In each case nothing on standard output is current, so say you couldn't check and carry on. Never treat a missing status as "no limits" or "nothing running".

## What it holds

- `limits`: one group per account with plan limits. `provider` is `claude`, `codex` or `antigravity`; `account` names an extra account. `stale: true` means the reading is old (`readAt` says when); `problem` explains a reading that failed. Each entry in its `limits` has `label` ("5-hour", "Weekly"), `usedPercent`, `resetsAt` and `pace`. Some, like Claude's "Extra usage", have no window, reset time or pace: only the percentage.
- `pace`, worked out when the command runs: `under` (plenty left at this rate), `on-pace` (lasts until it resets), `runs-out` (on course to run out before it resets, at `runsOutAt`) or `used-up`. It can be missing when there isn't enough of the window yet to tell.
- `todayShare` and `usedToday`, on weekly limits only: how much (%) can be used today and still last until the reset, worked out from what was left at local midnight, and how much today has used so far. They hold for the day of `generatedAt`.
- `sessions`: each agent session Dashbar sees, with `tool`, `workspace`, `folder`, `state` (`working`, `idle`, `needs-you` or `permission`), `since` and `subagents`. Your own session is usually in this list too, and there are no session ids to tell it apart.
- `servers`: listening dev servers with `port`, `command`, `pid`, `workspace` and `folder`. Dashbar reads ports while its panel or window is open, so a server started since then can be missing.
- `usageToday`: tokens per tool since midnight, with `cost` estimated at API list prices.
- `app.paused`: the person has paused Dashbar, so figures may be old. `hidden` lists tools they've switched off in Dashbar; those tools are left out of everything.

It never holds prompts, session titles, session ids or sign-ins.

## What to do with it

- **Your limits.** Find the group for the tool you are (`claude` for Claude Code, `codex` for Codex). If a limit's `pace` is `runs-out` or `used-up`, or it is at 90% or more, tell the person before starting heavy work, with when it resets, and offer a lighter plan: fewer parallel workers, a smaller first step, or waiting for the reset. Don't refuse the work; it's their call. If a weekly limit's `usedToday` is at or over its `todayShare`, mention that before heavy work too: going on is fine, it only leaves later days a smaller share.
- **Stale or failed readings.** If `stale` is true or `problem` is set, say the figures may be out of date rather than relying on them.
- **Dev servers.** If a server is already listening for this folder, use its port instead of starting another one. Ask before stopping a server you didn't start.
- **Other agents.** If more than one session is `working` in your `folder`, one of them is probably you and the others are other agents: mention it before editing files there, since you may both change the same files. If one is `needs-you` or `permission`, you can tell the person another agent is waiting for them.

Only read: don't edit Dashbar's files, and don't read its caches or other agents' logs directly. The command is the interface.

## More

- The command, its other modes and the status file: https://usedashbar.com/docs.md
- Installing Dashbar: https://usedashbar.com/.well-known/agent-skills/install-dashbar/SKILL.md
