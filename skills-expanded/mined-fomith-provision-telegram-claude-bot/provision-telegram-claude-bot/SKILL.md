---
name: provision-telegram-claude-bot
description: Install a persistent Telegram bot on an existing claude-server that bridges Telegram messages to a headless `claude --print` running as `claudeuser`, so the user can drive Claude (read/edit their files) from Telegram 24/7. Runs as a systemd-USER service (auto-start via linger, Restart=always), keeps per-chat conversation context via session resume, and is gated by a numeric Telegram-ID allow-list. Use when the user asks to "поставить телеграм-бота на сервер", "чтобы бот всегда крутился и выполнял запросы к Claude", "set up a Telegram bot that runs Claude on the server", "always-on Telegram Claude bot", or similar. Add-on to a box already provisioned by provision-claude-server. Asks for the bot token and the allow-listed Telegram IDs.
---

# Provision Telegram→Claude bot

Adds an always-on Telegram bot to an **already-provisioned claude-server**. Each
allow-listed Telegram message is run through `claude --print` in the user's folder
(Claude can read and edit those files) and the answer is sent back to Telegram. The
bot is a systemd-**user** service under `claudeuser`, so it reuses the existing
OAuth creds (watchdog-maintained) and `linger=yes`, runs 24/7, restarts on failure,
and survives reboot.

## Why a custom bot, not `claude --channels plugin:telegram`

The official channels plugin is a research preview, needs Bun, and its pairing/allow-list
step is interactive — bad for an unattended daemon. A tiny zero-dependency Node bot
(`bot.js`, built-in `fetch` + `child_process`, no npm install) shelling out to
`claude --print` is fully headless, pre-configurable, restart-safe, and matches this
project's stack. See `bot.js` for the bridge.

## What this skill produces (all under `claudeuser`, additive only)

- `~/telegram-claude-bot/bot.js` — the bridge (long-polls Telegram, runs `claude --print`).
- `~/telegram-claude-bot/config.env` (mode 0600) — `TELEGRAM_BOT_TOKEN`, `ALLOWED_TG_IDS`, `WORK_DIR`, permission mode, timeout.
- `~/telegram-claude-bot/state.json` — per-chat `session_id` map (conversation memory; survives restart).
- `~/.config/systemd/user/claude-telegram-bot.service` — `Restart=always`, `WantedBy=default.target`, started via linger.

**Strictly additive** (per provision-claude-server's hard rule): no edits to sshd/nginx/
system units/fstab. Only new files in claudeuser's home + one user unit.

## Required inputs

| Input | Notes |
|---|---|
| Target server | an **already-provisioned** claude-server — its SSH alias (e.g. `SERGEFIL-ROOT`) or `root@<IP>` by key |
| Telegram bot token | from [@BotFather](https://t.me/BotFather), shape `123456:ABC...` — **secret**, only into `config.env` |
| Allow-listed Telegram IDs | comma-separated numeric ids; **may start empty** — the bot tells each sender their id so you can add it, then re-run |
| WORK_DIR | optional, default = claudeuser's home (`/home/claudeuser`). The folder Claude reads/edits. |

## Prerequisite (hard)

`claudeuser` must have completed Claude OAuth at least once (creds present in
`~/.claude/.credentials.json`). On a brand-new claude-server that hasn't been logged
into yet, the file is absent — `claude --print` will fail with an auth error and the
bot will reply telling the user to run `claude` once over SSH. Check with
`ssh <NAME>-ROOT '~claudeuser/Чек_креды.sh'` (или `sudo -u claudeuser claude --version`
не проверяет креды — нужен реальный OAuth). If creds are missing, tell the operator to
SSH in as claudeuser and run `claude` once before the bot can answer.

## Workflow

### 1. Verify the target is a claude-server

```bash
ssh <NAME>-ROOT 'id claudeuser && command -v claude && command -v node && loginctl show-user claudeuser -p Linger'
```
Expect `claudeuser` to exist, `claude` + `node` present, `Linger=yes`. Abort if not — this
is an add-on, not a fresh-server skill (run provision-claude-server first).

### 2. Collect bot token + allow-list

Ask the user (AskUserQuestion or plain prompt) for:
- the **bot token** from @BotFather (keep it in a shell variable only — never echo, never
  write to the operator's disk; it lands only in `config.env` on the server, mode 0600);
- the **allow-listed Telegram IDs** if they know them. If they don't yet, proceed with an
  empty allow-list — the bot will reply each sender their numeric id; collect it and re-run
  step 4 with `ALLOWED_TG_IDS` filled.

Sanity: token matches `^[0-9]+:[A-Za-z0-9_-]+$`. If not, re-ask — don't "fix" it silently.

### 3. Upload bot + setup script

```bash
SKILL_DIR="/path/to/provision-telegram-claude-bot"   # папка с setup-telegram-bot.sh + bot.js
scp -o BatchMode=yes "$SKILL_DIR/setup-telegram-bot.sh" "$SKILL_DIR/bot.js" <NAME>-ROOT:/root/
```

### 4. Run the installer (token inline, never logged)

```bash
ssh <NAME>-ROOT "TELEGRAM_BOT_TOKEN='<TOKEN>' ALLOWED_TG_IDS='<ids or empty>' WORK_DIR='/home/claudeuser' bash /root/setup-telegram-bot.sh"
```
Prints `=== DONE ===` and the service shows `is-active: active`. The installer is
idempotent — to add allow-list ids later, just re-run this one command with the new
`ALLOWED_TG_IDS` (it refreshes config + restarts).

### 5. Acceptance tests

- `ssh <NAME>-ROOT 'sudo -u claudeuser env XDG_RUNTIME_DIR=/run/user/$(id -u claudeuser) systemctl --user is-active claude-telegram-bot.service'` → `active`.
- Linger: `loginctl show-user claudeuser -p Linger` → `Linger=yes`.
- Logs clean: `journalctl --user -u claude-telegram-bot.service` shows `claude-telegram-bot up …`, no crash loop.
- **Live smoke test**: from Telegram send `/id` to the bot → it replies your numeric id.
  Add that id to `ALLOWED_TG_IDS`, re-run step 4, then send a real request
  (e.g. «прочитай CLAUDE.md и перескажи правила»). Within a few seconds Claude answers.
  - If it replies an auth error → claudeuser hasn't done OAuth; have them run `claude` once over SSH.
  - If Claude prompts/refuses to edit → confirm `--permission-mode bypassPermissions` is honored
    on this version; fall back to adding `--dangerously-skip-permissions` in `bot.js`'s `runClaude`.

### 6. Cleanup staged files on the server

```bash
ssh <NAME>-ROOT 'shred -u /root/setup-telegram-bot.sh; rm -f /root/bot.js; echo cleaned'
```
(The real bot.js + config now live in claudeuser's home.)

### 7. Report to the user

State: which server, that the bot is a 24/7 systemd-user service (auto-restart + boot),
the work dir Claude can edit, that conversation context is per-chat and persistent, how to
add/remove allow-list ids (re-run step 4), bot commands (`/id`, `/new` to reset context),
and the security posture (allow-list is the only gate — anyone on it has code-exec as
claudeuser via Telegram; token + allow-list are secrets).

## Bot commands (for the end user)

On startup the bot self-registers the full Telegram quick-command menu (via
`setMyCommands` from the single `COMMANDS` array in `bot.js`), so they show up under the
"/" button automatically — nothing to set in @BotFather. **Commands run immediately,
outside the per-chat queue** (so `/cancel` can kill a running request).

Any plain text → a Claude request in the chat's work dir. Plus:

- **Session:** `/new` (reset context), `/continue` (resume last), `/retry` (repeat last
  prompt), `/cancel` (kill the running request), `/forget` (silent reset), `/status`.
- **Claude:** `/model opus|sonnet|haiku`, `/plan` (next request plans only —
  `--permission-mode plan`), `/think` (deeper reasoning next request), `/agent <name>`,
  `/safe` (toggle file edits: bypass ↔ read-only), `/lang ru|en`.
- **Workspace:** `/cd <path>` (confined to the home dir), `/pwd`, `/project <name>`
  (own subfolder + fresh context), `/ls`, `/tree`, `/find <text>`, `/cat <file>`.
- **Server/bot:** `/disk`, `/load`, `/uptime`, `/url` (needs `SERVER_URL`), `/restart`
  (admin only — `ADMIN_TG_IDS`, default = first allow-listed id), `/id`, `/help`.

Optional config env (in `config.env`): `SERVER_URL` (для `/url`), `ADMIN_TG_IDS`
(кто может `/restart`; по умолчанию — первый из `ALLOWED_TG_IDS`).

## Edge cases handled (see bot.js)

- **Not on allow-list** → bot refuses and shows the sender's id; Claude is never invoked.
- **Concurrent messages in one chat** → serialized per chat (no racing `--resume` on one session).
- **Long Claude runs** → spawn is async (polling never blocks); `typing…` kept alive; hard
  `CLAUDE_TIMEOUT_MS` (default 10 min) kills a stuck run.
- **Output > 4096 chars** → split into chunks.
- **Claude error / non-zero exit / bad JSON** → reported to chat, bot keeps running; auth
  errors get a "run `claude` once" hint.
- **Bot restart / reboot** → `session_id` map persisted to `state.json`; context preserved.
- **Telegram 5xx / network blip** → poll retried with backoff.

## Things explicitly NOT in this skill

- Provisioning a fresh server — that's `provision-claude-server` (this is an add-on).
- A standalone-server variant (bot on a box without claudeuser/claude) — would need its own
  auth + work-dir story; out of scope here.
- Group-chat fan-out, inline mode, media handling — text messages only.
