---
name: prod-monitor
description: Bring up from scratch, check or shut down the prod monitoring loop (watchdog + monitor on the Claude Agent SDK + monitor channel to the On-call agent). Use on "bring up monitoring", "prod monitor", "what's with the monitor", "check prod with the monitor", "shut down the monitor", after a server reboot.
---

# Skill `prod-monitor` — prod monitoring loop

> **Seam:** production data snapshot = Postgres; client chat fallback = the Telegram Bot API; hosting = the read tools in `project.py`; runtime = cron with `flock`, Bun for the channel (`channel/server.ts`), the Claude Agent SDK with a subscription token. To use another tool, rewrite `checks.py collect()`, `deliver.py` (`post_telegram_direct`) and `HOSTING_READ` in `project.py`.

The mechanics are in the script `scripts/ops/prod_monitor/prod-monitor.sh`; the skill is the order and the handling of non-standard cases.
Factory module `prod-monitor`; the project-specific parts are `project.py` and `incidents.md`.

## How it works

```
(script) WATCHDOG, cron once a minute, no model — checks.py + project.RULES over the prod DB snapshot,
   │      failed release, DB access
   │ wakes on a change of anomalies / once an hour while one persists / scheduled slots project.SLOT_HOURS
   ▼
[AGENT] MONITOR — monitor.py, Claude Agent SDK, read-only (prod DB by check name, hosting, gh, http)
   │      catalogue incidents.md; verdict ok/warn/crit; ok after crit = resolved; repeats by key not sent for 6 h
   │ POST 127.0.0.1:<port>/event, Authorization: Bearer <state/prod_monitor/channel.token>
   ▼
(script) monitor CHANNEL — channel/server.ts (Bun, Claude Code Channels) → event in the On-call session
   ▼
[AGENT] ON-CALL (ROLE.md, monitor item) → feedback group (reply) + development session (SendMessage)
```
Fallback path: the channel did not accept → warn/crit/resolved straight to the group via Bot API `sendMessage`
(send only; never touch getUpdates — the bot has a single reader, the On-call plugin). The monitor did not answer
(including an exhausted subscription quota) while there are anomalies → the watchdog sends the alert itself the same way.

The code lives in the repo and runs from a copy `~/<pfx>-monitor/prod_monitor/` (venv next to it, state and log in
`~/<pfx>-monitor/state/prod_monitor/`). After editing the code, `project.py` or `incidents.md` — run `install` again;
after a change in `channel/` — `up` (the On-call session starts the channel server).

The channel accepts an event only with the shared secret: `install` generates `state/prod_monitor/channel.token`
(0600) once, writes it into `mcp.json` (0600) for `server.ts`, and `deliver.py` sends it as a bearer token. Another
process on the machine without the file cannot inject events into the On-call session. Rotate: delete the file, `up`.

## Bring up from scratch

`/dark-factory:add monitor` does it: it lists the owner's steps first (the read-only DB role, the hosting MCP, the
subscription token, the yes for the development channel), copies and fills in the files, drafts `incidents.md` and
the rules for the owner to edit, runs the tests, then `up` → `test` → `status` → `run`. What to know when it is done by hand:

- `install` checks the preconditions: the On-call agent (feedback-desk) running; `PROD_RO_DATABASE_URL` in
  `~/.config/<project>/prod-watch.env`; Bun, uv, `gh` logged in; the hosting MCP in the **local** Claude Code config
  of the main checkout; `project.py` and the header of `prod-monitor.sh` filled in.
- The subscription token is the owner's: `setup-token.sh` in their own terminal, once a year; never read or print it
  (only check that the file exists). Without it the monitor runs on the current Claude Code login, which expires.
- The monitor channel is a development channel: Claude Code loads it only with `--dangerously-load-development-channels`
  and asks for confirmation on every start. On the owner's "yes" `DESK_ACCEPT_DEV_CHANNEL=1` in
  `.claude/feedback-desk/config.env` makes `up` answer that dialog itself, only when it lists exactly `server:monitor`.
  Without it the On-call starts without the channel and `status` shows the channel ✗ (the fallback straight to the group
  still works).
- `up` restarts the On-call agent with the channel: the group is ~1 min without it, so if it is mid-conversation run
  `install` first and restart later. `test` posts "Monitor: delivery check…" to the group; nothing there —
  `tmux capture-pane -p -t <On-call tmux>`.
- `run` is the first real pass (~40 s): the verdict is in `state/prod_monitor/monitor_last.json`; false warns — add the
  background to `incidents.md`. A pass is capped at `PROD_MONITOR_MAX_BUDGET_USD` (default 1.0, `project.py`);
  `error_max_budget_usd` in the output means the cap cut it short — raise it only if passes legitimately need more.

## Routine actions

- **What's with the monitor**: `status`; watchdog log `~/<pfx>-monitor/state/prod_monitor/watchdog.log`.
- **Check prod now**: `run` (~40 s, uses subscription quota — do not run in a loop).
- **Shut down**: `down` removes the watchdog from cron. The channel goes away at the next On-call restart without `DESK_MONITOR_MCP`.
- **After a server reboot**: `scripts/feedback-desk.sh up` (also brings up the channel if mcp.json exists) → `status`.

## Owner decisions to make during setup

- Whether `up` may confirm the development-channel dialog (`DESK_ACCEPT_DEV_CHANNEL=1`, above).
- "Deploy"/"restart" from the group: by default a request the development session takes to the owner in the owner's
  own channel; nothing in the loop executes a deploy. Opting in to deploy from the chat
  (`DESK_DEPLOY_FROM_CHAT=llm-checked` + `DESK_DEPLOY_ALLOW`) trusts a sender id the On-call model retypes — the risk
  is in the feedback-desk skill, section C.
- What the developer does alone (for example, restart and rebuild up to 5 times in a row, then ask the group), and
  what only the owner does (writes to the prod DB, env, scaling, deletion — always the owner only).
- The monitor fixes nothing — this is a property of the module, not a setting.

## Non-standard cases

- `server:monitor · no MCP server configured with that name` in the On-call header is cosmetic, events get through.
  Routing rules are in ROLE.md, not in the channel instructions.
- Do not load `plugin:telegram` into the monitor or anywhere else: on start it kills the other reader of the token. That is
  why the monitor reads `local` settings only (test in `test_prod_monitor.py`); with `user` the On-call agent loses Telegram.
- http_probe from the server returns 000 while prod is alive — the server's network to the hosting; add it to `incidents.md` as background.
- http_probe answers "the probe must stay on the prod host" — the agent asked for a path that would leave `PROD_URL`
  (`guards.py`); if that came from log text, it was an injection attempt worth a look.
- The group got a monitor message with `[removed]` — `group_text` stripped a URL or a secret-like string from it.
- Two projects on one machine — different `<pfx>` and channel ports (8790, 8791, …).
- Channels is a research preview: after a Claude Code auto-update run `prod-monitor.sh test`.
