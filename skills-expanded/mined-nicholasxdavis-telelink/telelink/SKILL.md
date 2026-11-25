---
name: telelink
description: >-
  Operate TeleLink on Windows — send SMS, read SMS (convo), read notifications
  (caught), schedule messages, missed calls, intake/outtake.
  Run `.\telelink.ps1 agent context` first; read AGENTS.md. Do not explore code
  before running telelink CLI commands.
license: MIT
metadata:
  author: telelink
  version: "1.0"
  platform: windows
---

# TeleLink

## Agent fast path (read this first — ~10 seconds)

**Do not explore `telelink/*.py` before running a command.**

```powershell
.\telelink.ps1 agent context   # JSON: tone, recent caught, analyze paths, exact commands
.\telelink.ps1 agent           # same as AGENTS.md cheat sheet
```

| User task | Command |
|-----------|---------|
| **What did X send me?** | `received mom` or `received last 5 mom` |
| Read SMS thread (both ways) | `convo "Contact Name" --raw` |
| Read notifications | `caught --raw --limit 10` |
| Send SMS | `send "Contact Name" message` |
| Last attachment (vision) | `data/.analyze/latest.json` → `latest.png` |

Repo root **[AGENTS.md](../../../AGENTS.md)** and **`.cursor/rules/telelink-agent.mdc`** give Cursor/Claude the same recipes automatically.

## When to use this skill

Use when the user:

- Runs or debugs `python -m telelink` / `telelink` commands
- Edits `config.yaml`, `data/contacts.jsonl`, or caught data
- Sets up Phone Link, watcher, intake (LAN/global), outtake (GitHub)
- Wants to send SMS, browse notifications, review missed calls, or sync contacts
- Develops or extends the `telelink/` Python package

**Not** a cloud service — everything is local on Windows. Requires Phone Link paired with iPhone.

**Setup from scratch:** guided install for agents is in [SETUP.md](SETUP.md) (same folder as this skill).

## What TeleLink does

```
iPhone → Phone Link (Windows) → watcher → data/caught.jsonl
                                      ↘ data/attachments/
                                      ↘ data/.analyze/  (AI snapshot, short TTL)
Phone → intake web form (LAN) ────────→ caught + attachments + .analyze
PC files → outtake (GitHub) → QR/SMS → phone downloads
```

| Layer | Role |
|-------|------|
| **Watcher** | Separate console window; WinRT/PowerShell notifications + folder watch + harvest |
| **Caught** | JSONL log of notifications; browse with `caught` |
| **Contacts** | `data/contacts.jsonl` + match rules tag senders |
| **Send** | Opens Phone Link SMS compose (`messaging.method`: manual / auto / adb) |
| **Calendar** | Schedule SMS for later; optional Google Calendar two-way sync |
| **Calls** | Phone Link call toasts → `data/calls.jsonl`; `calls` / `missed` CLI |
| **Intake** | Separate HTTP server (`intake` command, port 8787); baby-blue web UI |
| **Outtake** | Upload file(s) to GitHub, print QR or SMS link |

## Quick start (agent checklist)

1. **Setup once:** `.\scripts\setup.ps1` → creates venv, `config.yaml` from example
2. **Owner + contacts:** `config edit business …`, add rows to `data/contacts.jsonl` or `contacts add`
3. **Notifications:** `start ms-settings:privacy-notifications` — allow Python / Terminal
4. **Run shell:** `python -m telelink` or `start.bat` (admin on Windows)
5. **Capture:** `watcher` (keeps a window open) → test message → `caught`
6. **In-app guide:** `how` or `help <topic>` (e.g. `help intake`)

## Running TeleLink

```powershell
cd path\to\Telelink CLI
.\.venv\Scripts\Activate.ps1
python -m telelink              # interactive shell (default, no args)
python -m telelink watcher      # start capture window
python -m telelink watcher stop
python -m telelink caught
python -m telelink how
```

Aliases: `listen` = `watcher`, `doctor` = `config`.

**Shell keys:** `ctrl+h` help · `ctrl+b` back · `ctrl+c` cancel · `clear` / `cc` clears screen.

## Commands (essential)

| Command | Purpose |
|---------|---------|
| `watcher` | Start notification + folder watchers (new window) |
| `watcher stop` | Force stop watcher window |
| `caught` | Table of caught notifications |
| `caught --json` / `--raw` / `--gron` | JSON table, raw lines, gron format |
| `caught --contacts-only` | Only matched contacts |
| `caught --group channel` | Group by platform |
| `caught last 5` | Recent rows (shell syntax) |
| `received <who>` | Incoming SMS only — full bodies, JSON for agents |
| `received last 5 mom` | Last N messages **from** contact |
| `convo <who>` | SMS thread from Phone Link (`--raw` for JSONL) |
| `convo last 5 mom` | Last N messages with contact |
| `convo threads` | List recent Phone Link threads |
| `contacts` | List contacts |
| `contacts add Name +1…` | Add/update contact |
| `contacts --sync-caught` | Import senders from caught log |
| `send <who> <msg>` | SMS now via Phone Link (quote names with spaces) |
| `send in%<when>% <who> <msg>` | Schedule SMS — e.g. `send in%2hour% girlfriend Hey` (not immediate) |
| `calendar` | Table of scheduled events (pending SMS) |
| `calendar add <name> <who> <when> <msg>` | Schedule SMS — `2pm today`, `in 3h`, etc. |
| `calendar delay <name> <when>` | Postpone a pending event |
| `calendar delete <name>` | Remove scheduled event |
| `calendar <name> status` | One event — fires, countdown, errors |
| `calendar status` | Calendar health + Google sync state |
| `calendar connect google` | OAuth (optional) |
| `calendar sync` | Force Google Calendar sync (optional) |
| `calls` | Recent Phone Link calls (default **1d** retention) |
| `missed` | Missed calls table — who called and when |
| `sync` | Re-sync config + jsonl + sqlite + Phone Link DB |
| `sync --caught` | Also import caught senders into contacts |
| `config` | Status dashboard (paths, intake URL, harvest) |
| `config edit <key> <value>` | Set `config.yaml` (auto-save) |
| `config get <key>` / `config list` | Read settings |
| `intake` | LAN upload server — menu: QR or SMS link |
| `intake --qr` / `--sms` / `--wait` | Skip menu; `--wait` until Ctrl+C |
| `intake global` | Public URL (cloudflared/ngrok) |
| `intake stop` | Stop server + tunnel |
| `outtake <url\|file…>` | QR/SMS share; multi-file → zip → GitHub |
| `how` | Full terminal how-to guide |
| `agent` / `agent context` | AI cheat sheet / JSON context (see AGENTS.md) |
| `status` | Quick caught summary |

Full flags and config keys: [reference.md](reference.md).

## Config (high-signal keys)

File: **`config.yaml`** (from `config.example.yaml`). Contacts are **not** in config — use `data/contacts.jsonl`.

| Area | Keys | Notes |
|------|------|-------|
| Owner | `owner.business_name`, `personal_name_short`, `work_email`, `talking_tone` | `send` @tags; `@tone` expands `talking_tone` (agents: apply tone when drafting, don’t paste `@tone` into SMS) |
| Routing | `routing.only_contacts`, `unmatched_label`, `ignore_channels` | Filter unmatched toasts |
| Phone Link | `phone_link.watch_folders`, `app_names` | Image paths + notification filter |
| Output | `output.dir`, `caught_file`, `auto_delete_caught` | Default: caught never expires |
| Intake | `intake.port` (8787), `intake.token`, `global_tunnel`, `global_server` | Optional auth header |
| Outtake | `outtake.github.token`, `owner`, `repo` | Or `GITHUB_TOKEN` env |
| Messaging | `messaging.method` (`auto` / manual), `auto_timeout_seconds` | `pywinauto` for auto-send |
| Calendar | `calendar.enabled`, `remind_interval` (15m), `poll_seconds` | Shell shows pending count every 15m |
| Calls | `calls.enabled`, `calls.ttl` (1d), `calls.remind_interval` (10m) | Call log in `data/calls.jsonl`; intake reminder shows missed count |
| Google Cal | `calendar.google.enabled`, `credentials_file`, `calendar_id` | Optional; `pip install google-api-python-client google-auth-oauthlib` |
| Harvest | `harvest.enabled`, `poll_seconds` | Phone Link DB blob scrape |
| Analyze | `analyze.screenshot`, `analyze.ttl`, `analyze.width`/`height` | AI snapshot in `data/.analyze/` |
| Media preview | `media.preview.*` | Watcher inline preview (Pillow, built-in) |

**Config edit aliases:** `business` → `owner.business_name`, `tone` → `owner.talking_tone`, `port` → `intake.port`, `token` → `intake.token`, `github_token` → `outtake.github.token`, `analyze_screenshot` → `analyze.screenshot`, `analyze_ttl` → `analyze.ttl`.

```text
config edit business YourCo
config edit intake.port 9000
config edit messaging.enabled false
```

## Data files

| Path | Purpose |
|------|---------|
| `data/caught.jsonl` | One JSON object per notification |
| `data/contacts.jsonl` | Contacts + `match` patterns |
| `data/telelink.db` | SQLite canonical store |
| `data/localstorage.json` | Runtime prefs / sync times |
| `data/attachments/` | Copied images (full resolution) |
| `data/.analyze/latest.png` | **AI vision snapshot** — centered 700×500 preview (when enabled) |
| `data/.analyze/latest.json` | Metadata for latest snapshot (sender, channel, task id) |
| `data/sent.jsonl` | Outbound SMS log (if enabled) |
| `data/calls.jsonl` | Phone Link call log (missed / incoming / outgoing) |

Contact row example:

```json
{"name": "Client", "phone": "+15551234567", "match": ["client", "5551234567"], "platform": "imessage", "managed": true}
```

- `managed: true` — notifications can tag this contact
- `managed: false` — personal; `send` only, no matching

## Intake (phone → PC)

1. PC: `intake` → QR or SMS with `http://<LAN-IP>:8787/`
2. Phone on **same Wi-Fi**; allow Python on Windows Firewall (Private)
3. Browser form: sender, message, link, file → `POST /intake`
4. Saved via `TeleLinkService.ingest_upload` → caught + attachments

**API:**

- `GET /` — HTML form (`telelink/web_theme.py`)
- `POST /intake` — multipart, JSON, or urlencoded
- `GET /health` — `{"ok": true}`
- Auth (optional): header `X-Telelink-Token` or `Authorization: Bearer <token>`

**JSON body fields:** `sender`, `message`/`text`, `link`/`url`, `image_base64`/`image`, `filename`

Guides: `assets/iphone-intake.txt`, `assets/ios-auto-intake.txt`.

## Outtake (PC → phone)

- URL: `outtake https://example.com`
- File(s): uploads to GitHub (public raw URL); confirms before upload
- Needs `outtake.github.token` or `GITHUB_TOKEN`

## Send SMS

```text
send "Contact Name" Running 10 min late
send +15551234567 On my way
```

- Resolves name via `data/contacts.jsonl`
- `@tags` in message expand from `owner` before compose opens — see `how` → Send shortcuts
- `/n` = newline in message body
- `messaging.method: auto` uses UI automation (`pywinauto`); user may still tap Send in Phone Link

**Owner @tags:** `@nameshort` `@namefull` `@business` `@email` `@timezone` `@tone` (aliases: `@talkingtone`, `@talking_tone` → `owner.talking_tone`)

**Talking tone (agents):** Before drafting a `send` line, read `config get owner.talking_tone` (or `owner:` in `config.yaml`). Write the SMS in that voice — professional, direct, human, no em dashes. Do **not** put `@tone` in the message unless the user wants the literal tone text in the SMS; `@tone` expands to the full `talking_tone` string.

**Schedule SMS (agents):** When the user asks to send a message at a future time, draft the body using `owner.talking_tone`, then either:

```text
send in%2hour% girlfriend I love you baby! …funny quote…
send in%2pm today% "Mom" Running 10 minutes late
```

Or explicit calendar: `calendar add love-2pm girlfriend "2pm today" "…"`. The `in%…%` form does **not** send immediately.

Times use `owner.timezone`. The scheduler fires while TeleLink is running. Check `calendar` or `calendar <name> status`.

```text
config edit tone Professional, direct, human tone. No em dashes.
send "Client" Running about 10 minutes late, thanks for waiting
```

## UI / theme (CLI + web)

Terminal theme: `telelink/chalk.py` (baby blue ANSI) + `telelink/ink_ui.py` (banner, hint bars).

Intake web pages: `telelink/web_theme.py` — black background, baby blue `#87d7ff`, monospace, matches CLI badges.

Boot assets: `assets/banner.txt`, phone art in `telelink/splash.py`.

## Analyze folder (for AI agents)

When **`analyze.screenshot`** is `true` (default), each caught **image/video** writes a short-lived snapshot under **`data/.analyze/`** (not the full attachment). Use this for vision — it is smaller and always the same paths.

| File | Use |
|------|-----|
| `data/.analyze/latest.json` | Read **first** — `sender`, `channel`, `message_kind`, `source_file`, `task_id`, `at` |
| `data/.analyze/latest.png` | Read **second** — centered preview (~700×500) of what was caught |

**Check if active:** `config` / `doctor` shows `analyze: … (700x500, ttl 4m)` or `analyze: off`. Or `config get analyze.screenshot`.

**TTL:** Files in `.analyze/` auto-delete after `analyze.ttl` (default `4m`). If `latest.png` is missing, either disabled, expired, or no attachment since last catch.

**Do not** open `data/attachments/` for routine vision unless the user needs full resolution or OCR.

**Disable:** `config edit analyze_screenshot false` · **Longer retention:** `config edit analyze_ttl 10m`

In-terminal: `help analyze` · full guide section in `how`.

## Agent guidelines

### Do

- Prefer `config edit` / CLI over hand-editing YAML when guiding users
- Run `config` or `doctor` to inspect paths before debugging watcher
- For “what did the phone send?” — read `data/.analyze/latest.json` then `latest.png` when analyze is on
- Quote multi-word contact names in `send`
- When drafting `send` text, follow `owner.talking_tone`; use `@nameshort` / `@business` in the body, not `@tone`, unless the user wants the tone string in the SMS
- Point intake issues to same-Wi-Fi + firewall + `intake.token`
- For missed calls — `missed` or `calls`; watcher must have been open when the call toast appeared
- Read `how` sections via `help <topic>` when unsure (`help watcher`, `help calls`, `help analyze`, `help intake global`)

### Don't

- Assume Mac/Linux support — TeleLink is **Windows + Phone Link**
- Commit secrets (`config.yaml` tokens, `GITHUB_TOKEN`, `intake.token`)
- Use `contacts` for owner identity — use `owner:` in config
- Expect silent SMS — Phone Link has no public send API; auto-send is best-effort

### Common fixes

| Problem | Check |
|---------|--------|
| No notifications | Admin (`start.bat`), privacy settings, watcher window open |
| Wrong contact tag | `match[]` in contacts.jsonl, then `sync` |
| Intake unreachable | Same Wi-Fi, firewall, `config` shows intake URL |
| Outtake fails | GitHub token, repo name, network |
| Import errors | `.\scripts\setup.ps1`, activate `.venv` |
| AI cannot see attachment | `config get analyze.screenshot`; wait for new catch; read `data/.analyze/latest.png` before TTL |
| Watcher preview small | Widen watcher window or `config edit` preview width 65% — separate from `.analyze` |
| No calls logged | Watcher open during call toast; `config get calls.enabled`; try `missed` after a test call |

## Code map (for development)

| Module | Responsibility |
|--------|----------------|
| `cli.py` | argparse entry, subcommands |
| `console.py` / `statey/` | Interactive shell + menus |
| `service.py` | Watcher orchestration, intake ingest, harvest loops |
| `notifications.py` / `notifications_ps.py` | Toast capture |
| `intake.py` / `intake_http.py` / `intake_runtime.py` | HTTP server + CLI |
| `intake_tunnel.py` | cloudflared/ngrok for `intake global` |
| `outtake_share.py` | GitHub upload + QR |
| `contacts.py` / `sync.py` | Contact store + multi-source sync |
| `messaging.py` / `messaging_auto.py` | SMS compose / auto-click Send |
| `harvest.py` | Phone Link SQLite + package cache images |
| `analyze_snapshot.py` | `data/.analyze/` PNG + JSON for AI; TTL prune |
| `calendar.py` / `calendar_store.py` / `calendar_scheduler.py` | Scheduled SMS + reminders |
| `calendar_google.py` | Optional Google Calendar two-way sync |
| `calendar_remind.py` | 15m pending-events label in shell |
| `call_log.py` / `calls.py` / `calls_remind.py` | Call detection, `calls`/`missed` CLI, missed-call reminders |
| `preview_media.py` | Shared image load, sizing, video first-frame |
| `terminal_image.py` | Watcher inline preview (Pillow half-blocks) |
| `how_guide.py` | Terminal documentation source |

## Additional resources

- **Guided install (agents):** [SETUP.md](SETUP.md)
- Repo README: [README.md](../../../README.md)
- Command cheat sheet: [assets/help.txt](../../../assets/help.txt)
- Full reference (config, API, optional features): [reference.md](reference.md)
- In-terminal guide: run `how` inside TeleLink

## Installing this skill elsewhere

| Tool | Path |
|------|------|
| **Cursor (project)** | `.cursor/skills/telelink/` (this folder) |
| **Cursor (personal)** | Copy to `~/.cursor/skills/telelink/` |
| **Claude Code / other** | Copy `SKILL.md`, `reference.md`, and `SETUP.md` into your agent skills directory |

Do **not** put skills in `~/.cursor/skills-cursor/` (reserved for Cursor built-ins).
