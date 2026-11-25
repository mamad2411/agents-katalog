---
name: pi-durable-telegram
description: Turn this machine into an always-on durable pi agent the user talks to in Telegram (pi-durable-telegram). Use when the user asks to run pi as a Telegram bot, to reach their agent from Telegram or the phone, or to install, restart, update or debug pi-durable-telegram.
license: MIT
compatibility: Linux with systemd and Node.js 22.19+; pi installed and logged in on the same machine
---

# Durable pi agent in Telegram

You are running inside pi on the user's server. Your job: install `pi-durable-telegram`, connect it to a Telegram bot
and leave it running as a systemd user service. The daemon reuses this pi's login (`~/.pi/agent/auth.json`) and its
default provider, model and thinking level, so the user does not log in again.

Never print tokens or keys into the chat, files you show, or logs.

## 1. Check the machine

Run these and fix what fails before going on:

```sh
node --version          # 22.19 or newer
systemctl --user status >/dev/null && echo systemd-user-ok
jq -r 'keys[]' ~/.pi/agent/auth.json 2>/dev/null     # providers pi is logged in to (names only)
jq '{defaultProvider, defaultModel, defaultThinkingLevel}' ~/.pi/agent/settings.json 2>/dev/null
```

- No providers listed: ask the user to run `/login` in pi, pick any provider, and tell you when done.
- Node too old: install a newer one next to it (for example `nvm install 24`) without changing the default; other
  services may depend on it. Note the absolute path of that `node`.
- If `PI_CODING_AGENT_DIR` is set, use that directory instead of `~/.pi/agent` everywhere.

## 2. Get the bot

Ask the user for a bot token. If they have none: open @BotFather in Telegram, send `/newbot`, choose a name and a
username ending in `bot`, copy the token. The bot must not be used by any other program (one token can be polled by
one process only). Check it:

```sh
curl -s "https://api.telegram.org/bot$TOKEN/getMe" | jq -c '.result | {username}'
curl -s "https://api.telegram.org/bot$TOKEN/getWebhookInfo" | jq -c '.result | {url, pending_update_count}'
```

Then find the user's Telegram id without asking for it: tell them to send any message to the bot, and read it:

```sh
curl -s "https://api.telegram.org/bot$TOKEN/getUpdates" | jq -r '.result[].message.from | "\(.id) \(.username)"' | sort -u
```

Confirm the id with the user. Add more ids only if they ask; everyone on the list gets full shell access.

## 3. Install and configure

```sh
npm install -g pi-durable-telegram
pi-durable-telegram --version
mkdir -p ~/.config/pi-durable-telegram ~/pi-agent
( umask 077; cat > ~/.config/pi-durable-telegram/env <<EOF
TELEGRAM_BOT_TOKEN=$TOKEN
TELEGRAM_ALLOWED_USER_IDS=$USER_ID
PI_WORKDIR=$HOME/pi-agent
EOF
)
```

Add the model to the env file. Use the provider and model you are running as right now (a fresh pi has no default
saved in its settings, so the daemon cannot guess it), unless the user wants a different or cheaper one for Telegram:

```sh
printf 'PI_PROVIDER=%s\nPI_MODEL=%s\n' "<provider>" "<model id>" >> ~/.config/pi-durable-telegram/env
```

`PI_THINKING` is optional (`off`, `low`, `medium`, `high`, ...); the daemon refuses to start when the model does not
support the level and names the ones it does. For voice messages add `DEEPGRAM_API_KEY` if the user has one.

Write `~/pi-agent/AGENTS.md`: it goes into the agent's system prompt and is re-read when it changes. Look around the
server first (`systemctl --user list-units --type=service`, the home directory) and draft it with the user:

- the language to answer in;
- what runs on this server and where projects, notes or a knowledge vault live;
- what the agent must not touch (other services, other people's data, production databases);
- to ask before anything hard to undo.

## 4. Run it as a service

systemd does not load the shell's `PATH`, so use absolute paths:

```sh
NODE="$(command -v node)"                       # or the newer node from step 1
MAIN="$(npm root -g)/pi-durable-telegram/dist/cli/main.js"
mkdir -p ~/.config/systemd/user
sed -e "s|^ExecStart=.*|ExecStart=$NODE $MAIN run --env-file %h/.config/pi-durable-telegram/env|" \
    -e "s|^WorkingDirectory=.*|WorkingDirectory=%h/pi-agent|" \
    "$(npm root -g)/pi-durable-telegram/deploy/pi-durable-telegram.service" \
    > ~/.config/systemd/user/pi-durable-telegram.service
systemctl --user daemon-reload
systemctl --user enable --now pi-durable-telegram
loginctl enable-linger "$USER"
```

## 5. Verify for real

1. `systemctl --user is-active pi-durable-telegram` prints `active`.
2. `journalctl --user -u pi-durable-telegram -n 20 -o cat` shows `polling_started bot=<name>` and `started model=...`.
3. Ask the user to message the bot. The journal shows `message_admitted`, then `delivered`, and the user confirms the
   answer arrived. Only then say it works.
4. Suggest trying a voice note, a photo and `/status`.

## Operate

- Logs: `journalctl --user -u pi-durable-telegram -f`
- Restart: `systemctl --user restart pi-durable-telegram` (unfinished runs resume after start)
- Update: `npm install -g pi-durable-telegram@latest`, then restart
- Telegram commands: `/new`, `/stop`, `/compact`, `/status`, `/help`

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Exit code 2 at start | Bad config, rejected bot token or a thinking level the model lacks; the journal names each problem |
| Exit code 3 | Another process owns the data directory; stop it |
| Exit code 4 or "run login" in chat | pi is not logged in to the provider in use: `/login` in pi, then restart the service |
| 409 Conflict in the journal | Another process polls the same bot token; stop it or use another bot |
| No answer and nothing in the journal | The sender is not in `TELEGRAM_ALLOWED_USER_IDS`; strangers are ignored silently |
| Voice notes arrive as audio files, not text | Add `DEEPGRAM_API_KEY` to the env file and restart |

## Security

The agent gets a full shell as this user: whoever is on the allow-list can run any command this user can. Say this
before installing, and suggest a dedicated system user when the server holds important data.
