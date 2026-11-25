---
name: communications
description: >
  Terminal and voice outreach for Cooper — email (Himalaya IMAP/SMTP + gog Gmail API),
  iMessage (BlueBubbles / osascript), and outbound AI phone calls (Vapi/Twilio/ElevenLabs).
  Use when reading/sending email, sending iMessages without imsg, calling a business/support
  line, waiting on hold, negotiating by phone, or checking mail-source connectivity for cron.
version: 2.4.0
metadata:
  hermes:
    tags: [email, imessage, phone, vapi, messaging, himalaya, bluebubbles, gog]
    category: communication
    related_skills: [gog, financial-operations, yuanbao]
---

# Communications (email · iMessage · phone)

Class-level skill for outbound/inbound human outreach channels operated from the agent.
Three modes share "reach a human"; pick the section that matches the task.

| Mode | Channel | When |
|---|---|---|
| **Email** | Himalaya (IMAP/SMTP) or `gog` (Gmail API) | Read/send/search mail; triage labeling lives in `gog` |
| **iMessage** | BlueBubbles API or osascript | Send iMessages when `imsg` CLI unavailable |
| **Phone** | Vapi → Twilio → ElevenLabs | Real voice calls, hold queues, IVR, refunds |

`sag` / ElevenLabs TTS only produces audio files — it does **not** place phone calls. Phone = Vapi.

Yuanbao group @mentions are a separate gateway skill (`yuanbao`); do not fold them here.

---

# Mode A — Email

## Mail source connectivity check

Before read/send (especially cron), verify at least one source:

```bash
# 1. Hermes Email gateway
hermes status 2>&1 | grep -A1 "Email"
# 2. Himalaya
which himalaya && ls ~/.config/himalaya/config.toml 2>/dev/null
# 3. gog (Gmail API)
which gog && gog auth list
# If empty accounts but user authenticated before → keyring backend mismatch.
# See `gog` skill "Backend mismatch" before recommending re-auth.
```

No source connected → report setup steps. Do NOT emit `[SILENT]` for "no inbox"; that means "no new mail on a connected inbox."

### gog auth state

Credentials file presence ≠ authenticated. Confirm with `gog auth list` or `gog -a <email> auth doctor`.

When file backend is config-forced, load keyring password before every gog command (construction avoids interactive prompts):

```bash
export GOG_KEYRING_PASSWORD=<REDACTED>
```

Deep auth/keyring/OAuth/triage labels/multi-account/batch unsubscribe → load **`gog`** skill.

### Inbox Zero with gog

For autonomous Gmail triage, use a durable Kanban card and process **one thread/card at a time**. Labels, archive, mark-read, and filters are `EXECUTE-SAFE` only after a per-action Gmail query verifies the state change. Never send/delete mail, click financial or fraud email links, alter account security, or approve OAuth permissions without the correct gate.

Do not use `--all` on a large inbox as the first step: it can exhaust Gmail per-user query quota or time out. Enumerate with bounded `--max 10` pages, preserve each returned `nextPageToken`, and resume slowly if `403 rateLimitExceeded` occurs. A `gog auth doctor` client-credentials config warning is not evidence that email access is broken; prove access with `gog auth list` plus a small Gmail search before re-authentication.

Detailed checklist and recovery: `references/gog-inbox-zero.md`.

## Himalaya CLI (IMAP/SMTP)

Separate from the Hermes Email gateway adapter.

**Prereqs:** `himalaya --version`, `~/.config/himalaya/config.toml`, IMAP/SMTP creds.

```bash
brew install himalaya  # macOS
```

Full config (Gmail/iCloud/OAuth2/folder aliases): `references/himalaya-configuration.md`.

> **Folder alias pitfall:** use `folder.aliases.X` (plural, dotted) in v1.2.0+. Old `[accounts.NAME.folder.alias]` is silently ignored → save-to-Sent failures / duplicate sends.

### Integration notes

- List/read/search/move/delete via `terminal`
- Compose via pipe: `cat << EOF | himalaya template send`
- `--output json` for structure
- `himalaya account configure` needs PTY: `terminal(..., pty=true)`

### Common ops

```bash
himalaya folder list
himalaya envelope list
himalaya envelope list from john@example.com subject meeting
himalaya message read 42
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send
himalaya message move 42 "Archive"
himalaya message delete 42
himalaya attachment download 42 --dir ~/Downloads
himalaya --account work envelope list
```

Rich/multipart/MML: `references/himalaya-message-composition.md`.

## gog shortcuts (when using Gmail API)

- Attachments: `--attach /path/a,/path/b`
- Reply thread: `--thread-id <id> --reply-all --body "..."` or `--reply-to-message-id <id>`
- Send-as: `--from me@cm.xyz` (verified alias)
- Long bodies: `--plain` truncates ~700 chars → use `--json` + base64. See `gog` → `references/multi-account-search.md`
- Multi-account search + triage labels: `gog` → those references

### Auth warning vs. actual mailbox access

`gog -a <account> auth doctor` can warn that the OAuth client-credentials config file is missing and suggest `gog auth credentials <file>`, while stored account tokens remain healthy. Do **not** reconfigure OAuth just to clear that warning. Verify the functional path first:

```bash
gog auth list
gog -a <account> gmail search "newer_than:1d" --max 1 -j
```

If the account appears in `auth list` and the live Gmail search succeeds, Gmail access is usable. Only run `gog auth credentials <credentials.json>` when intentionally registering/replacing the OAuth client credentials.

### Bulk unsubscribe fallback

For marketing cleanup, prefer the message `List-Unsubscribe` header. Some providers emit a literal truncated HTTPS token (`...`) that cannot be followed; look for the header's `mailto:` alternative and send an unsubscribe email instead. With `gog`, use flags rather than RFC-style headers on stdin:

```bash
gog -a <account> gmail send \
  --to 'leave-...@leave.vendor.example' \
  --subject 'Unsubscribe' \
  --body 'Please unsubscribe me from all email lists.'
```

A `List-Unsubscribe-Post: List-Unsubscribe=One-Click` header can often be actioned with a direct HTTP request; preference-center URLs may need a browser confirmation or a provider-specific POST. Record successful vs. pending links rather than assuming a 200 response confirms unsubscribed status.

---

# Mode B — iMessage (BlueBubbles / osascript)

When `imsg` is missing.

## BlueBubbles API (preferred)

```bash
lsof -iTCP -sTCP:LISTEN -P -n | grep -i bluebubbles
# password column is "name", path is lowercase hyphenated:
sqlite3 ~/Library/Application\ Support/bluebubbles-server/config.db \
  "SELECT value FROM config WHERE name='password'"
curl -s "http://127.0.0.1:1234/api/v1/server/info?password=<PASSWORD>" | python3 -m json.tool
# chat/query and message/query are POST (GET → misleading 404)
curl -s -X POST "http://127.0.0.1:1234/api/v1/chat/query?password=<PASSWORD>" \
  -H "Content-Type: application/json" \
  -d '{"limit": 15, "sort": "lastmessage", "with": ["lastMessage"]}' -o /tmp/chats.json
curl -s "http://127.0.0.1:1234/api/v1/message/text?password=<PASSWORD>" \
  -X POST -H "Content-Type: application/json" \
  -d '{"chatGuid":"iMessage;-;+1XXXXXXXXXX","text":"Hello!","ddwc":true,"subject":"","method":"private-api"}'
```

Port may differ — always check `lsof`.

### macOS Tahoe (26) Private API breakage

`helper_connected` / `private_api` false → lose typing indicators, tapbacks, reliable private-api sends.

1. NVRAM boot-args (AMFI) then reboot:
   ```bash
   sudo nvram boot-args="amfi_get_out_of_my_way=1 amfi_allow_any_signature=1 -arm64e_preview_abi ipc_control_port_options=0"
   ```
2. Patched dylib for `_newChatItems` crash:
   - Release: `https://github.com/willsigmon/bluebubbles-helper/releases/tag/v0.0.22-tahoe`
   - Backup + replace `BlueBubblesHelper.dylib` under app Resources `private-api/macos11/`.

May also need `csrutil disable` + ad-hoc `codesign -s - <dylib>`. Remaining regressions: APNs delay #779, reply-thread stall #814, AppleScript -1700 #777. Detail: `references/bluebubbles-tahoe-fix.md`.

## osascript fallback

Reference service by **service type**, not name:

```bash
osascript -e '
tell application "Messages"
    set theService to 1st service whose service type = iMessage
    set theBuddy to buddy "+1555121212" of theService
    send "message text" to theBuddy
end tell'
```

Pitfalls: `Invalid key form (-10002)` = wrong service reference; port mismatch.

---

# Mode C — AI phone calls (Vapi)

Stack: **Vapi** (orchestration + LLM) → **Twilio** (telephony) → **ElevenLabs** (voice). Already wired in Cooper's Vapi org.

## Standing infrastructure

- **1Password item `vapi`** (`op item get "vapi" --format=json`):
  - `username` = Vapi **public** key
  - `credential` = Vapi **PRIVATE** key ← use as `Authorization: Bearer <REDACTED> on `api.vapi.ai`
  - `twilio-sid` / `twilio-token`
  - `vapi-assistant-id` = permanent assistant
  - `twilio-number` often **masked** — resolve real `phoneNumberId` via `GET https://api.vapi.ai/phone-number`
- **Permanent assistant:** "Personal Concierge" (persona **Levi**). Standing inbound prompt — never PATCH for one-off calls; use `assistantOverrides`.

### 401 "Invalid Key / public vs private"

Server REST needs the **private** `credential` field, not `username`.

## Workflow

1. Gather: callee number, goal, facts (names, refs, dates, amounts, card last-4), guardrails.
2. Verify: `GET /phone-number` with private key → `phoneNumberId`, `assistantId`.
3. Payload: `templates/vapi_call.json` — one-time `assistantOverrides` only.
4. Fire: `POST https://api.vapi.ai/call` → 201 + `status: queued`. Keep `id`, `monitor.listenUrl`, `monitor.controlUrl`.
5. Monitor: `scripts/watch_call.sh <call_id> <private_key>` via `terminal(background=true, notify_on_complete=true)` (polls 30s → ended + cost + transcript).
6. Report outcome, case numbers, next steps.

## Hold-proofing overrides

- `"firstMessageMode": "assistant-waits-for-user"` (outbound; let IVR/human speak first)
- `"maxDurationSeconds": 7200`
- `"silenceTimeoutSeconds": 3600`

## System prompt sections for the override

1. Identity & authority (Levi; on behalf of whom)
2. **GOAL** (one sentence, caps)
3. Facts block (only known facts)
4. What happened (numbered narrative for disputes)
5. IVR (listen, DTMF; "existing reservations" / 0-for-agent)
6. Hold (silent wait; greet human)
7. Negotiation rules (refunds, DOT, process extraction)
8. DO NOT (SSN, full PAN, payment creds, commitments); unknown → "not in front of me"; callback (310) 989-7067 / me@cooperm.com
9. WRAP-UP (spell case #, amount, timeline; hang up cleanly)

Third-party booking: extract required process + document on account even if business refuses agent authority.

## Warm transfer to a human (preferred handoff)

Pattern Cooper wants for support lines:

1. **Levi stays on** through IVR + hold until a **real human agent** answers.
2. Then **warm-transfer-experimental** to a human phone (e.g. `+12069542027`).
3. If that human **doesn't pick up / declines / voicemail** → transfer **cancels** and **Levi keeps the airline agent** and **finishes the task himself**.

This is **not** cold `control.type=transfer` (that drops Levi immediately and cannot fall back).

### Templates

- `templates/vapi_warm_transfer_tool.json` — reusable `transferCall` tool block (`warmTransferToHuman`)
- `templates/vapi_call_flight_change_warm_transfer.json` — full AA flight-change payload with tool + phased prompt

### Mechanics

- Tool type `transferCall` with destination `transferPlan.mode: "warm-transfer-experimental"`
- Nested `transferAssistant` dials the human, confirms live answer, then:
  - `transferSuccessful` → merge human ↔ airline agent; AI exits
  - `transferCancel` → human leg drops; **original assistant (Levi) resumes** on the business leg
- Auto-cancel also on: no answer, `maxDurationSeconds`, silence timeout, voicemail (prompt the transfer assistant to cancel on VM)
- On tool `messages` / `request-failed`: set `endCallAfterSpokenEnabled: false` so a failed handoff does **not** hang up the airline call

### Prompt rules (must be explicit in system prompt)

```
PHASE 1 — Reach human agent yourself. No warmTransfer during IVR/hold.
PHASE 2 — When human greets: call warmTransferToHuman ONCE.
PHASE 3 — If transfer fails/cancels: apologize briefly, continue GOAL yourself. Do not abandon the task.
```

### Fire

```bash
source ~/.hermes/skills/communication/communications/scripts/vapi_env.sh
# edit destination/facts in the JSON first
curl -sS -X POST https://api.vapi.ai/call   -H "Authorization: Bearer <REDACTED>"   -H "Content-Type: application/json"   -d @~/.hermes/skills/communication/communications/templates/vapi_call_flight_change_warm_transfer.json
```

Then `scripts/watch_call.sh <call_id>` (key optional if env loaded).

### Pitfalls

- Cold live-control `{"type":"transfer"}` ≠ warm transfer. Cold cannot "try human then fall back to Levi".
- Don't warm-transfer into IVR of the human's carrier voicemail without cancel instructions — configure transfer assistant to `transferCancel` on VM.
- Changing the human number: update `destinations[0].number`, `function.parameters.properties.destination.enum`, and the tool description.
- Permanent assistant "Personal Concierge" stays untouched; all of this lives in `assistantOverrides` for one call.

## Mid-call ask_cooper (HITL)

Levi can pause mid-call, ask Cooper a question, and wait for a Slack reply before continuing.

### Components

- Server: `scripts/ask_cooper_server.py` (blocking webhook, default port `8788`)
- Public tunnel: `cloudflared tunnel --url http://127.0.0.1:8788` (URL changes each restart)
- Vapi tool: `ask_cooper` (`f30e31b9-f6ee-48f6-8bec-1d518a43e369`) → `POST {tunnel}/vapi/tools`
- Slack: Hermes bot DM with Cooper (`D0BG4HJ47GE`, user `U092MDGBK0R`)
- Attached on assistant **Personal Concierge** toolIds along with `dtmf`

### Run (each machine boot / when tunnel dies)

```bash
# 1) HITL server
export SLACK_BOT_TOKEN=<REDACTED>
export SLACK_CHANNEL=D0BG4HJ47GE
python3 ~/.hermes/skills/communication/communications/scripts/ask_cooper_server.py

# 2) Tunnel (separate terminal)
cloudflared tunnel --url http://127.0.0.1:8788
# copy https://….trycloudflare.com

# 3) Point tool at new tunnel URL if it changed
source ~/.hermes/skills/communication/communications/scripts/vapi_env.sh
curl -sS -X PATCH "https://api.vapi.ai/tool/f30e31b9-f6ee-48f6-8bec-1d518a43e369" \
  -H "Authorization: Bearer <REDACTED>" -H "Content-Type: application/json" \
  -d '{"server":{"url":"https://NEW-TUNNEL.trycloudflare.com/vapi/tools","timeoutSeconds":120}}'
```

### How to answer during a call

1. Slack DM from hermes_bot — **just reply with text** in that DM (polled), or
2. Manual API: `curl -sS -X POST localhost:8788/reply -H 'Content-Type: application/json' -d '{"id":"<id from message>","answer":"fee up to $200 ok"}'`

Timeout default **90s** → Levi gets `NO_REPLY_TIMEOUT` and continues under existing guardrails (no invented spend authority).

### Prompt snippet (include in assistantOverrides for tasks that may need you)

```
If you need Cooper's authority on fees, payment, or accepting a compromise, call ask_cooper with a short question and context. Tell the agent you are confirming with a colleague. Wait for the tool result, then continue.
```

### Pitfalls

- Quick tunnels are ephemeral — update the tool `server.url` after each cloudflared restart.
- Do not DM openclaw's old channel; use Hermes bot IM `D0BG4HJ47GE`.
- Tool must be **sync** (`async: false`) so Levi waits. Server timeout ≤ Vapi tool timeout (120s).
- `keypadInputPlan` is unrelated (inbound human keypad → Levi). Keep off unless needed.

## BlueBubbles Studio webhook (inbound iMessage)

Stable receive path for the agent-dedicated Mac Studio BlueBubbles:

| | |
|---|---|
| Studio BB (API) | Cloudflare quick tunnel currently `https://stomach-multi-barnes-providence.trycloudflare.com` (port 1234) — **ephemeral**, refresh if Studio BB restarts it |
| Webhook endpoint | `https://bb-hook.cm.xyz/bb/webhook?secret=...` |
| Inbox API | `https://bb-hook.cm.xyz/messages?secret=...` / `/inbox` / `/health` |
| Local process | `scripts/bb_webhook_server.py` on `:8790` |
| Tunnel | Cloudflare named tunnel `hermes-pro-webhooks` (`cec4b29a-…`) → `bb-hook.cm.xyz` |
| Secret | `~/.hermes/bb/webhook-secret` (also try `himitsu read hermes/bb-hook-secret`) |
| Config meta | `~/.hermes/bb/config.json` |

### Auth for Studio BB API

Same server password as local BB config DB:

```bash
PASS=$(sqlite3 "$HOME/Library/Application Support/bluebubbles-server/config.db" "SELECT value FROM config WHERE name='password'")
curl -sS "$STUDIO_BB/api/v1/server/info?password=$PASS"
```

### Ops

```bash
# health
SEC=$(cat ~/.hermes/bb/webhook-secret)
curl -sS "https://bb-hook.cm.xyz/health?secret=$SEC"

# recent inbound
curl -sS "https://bb-hook.cm.xyz/messages?secret=$SEC&limit=20" | python3 -m json.tool

# register/update webhook on Studio BB after tunnel URL change for Studio itself:
# POST $STUDIO/api/v1/webhook  {"url":"https://bb-hook.cm.xyz/bb/webhook?secret=SEC","events":["new-message",...]}
```

`bb-hook.cm.xyz` is **stable**. The Studio-side quick tunnel URL is not — when it changes, update callers; the webhook target on our side stays the same.

## CLI + analytics

Official **Vapi CLI** is installed at `~/.vapi/bin/vapi` (symlinked to `~/.local/bin/vapi`). Auth via private key in `~/.vapi-cli.yaml` (mode 600) sourced from 1Password item `vapi` → `credential`. Prefer scripts below so key resolution stays automatic.

```bash
# ensure PATH (already in ~/.zshrc after install)
export PATH="$HOME/.vapi/bin:$HOME/.local/bin:$PATH"

# load key + IDs into current shell
source ~/.hermes/skills/communication/communications/scripts/vapi_env.sh
# or: eval "$(.../scripts/vapi_env.sh)"

vapi auth status
vapi assistant list
vapi call get <call_id>          # note: `vapi call list` may fail on API schema drift; use helper
vapi logs list
```

### `scripts/vapi_analytics.sh` (preferred for metrics)

Wraps `POST https://api.vapi.ai/analytics` + call list/get. Auto-loads private key via `vapi_env.sh`.

```bash
SCRIPTS=~/.hermes/skills/communication/communications/scripts

$SCRIPTS/vapi_analytics.sh                     # 7-day summary dashboard
$SCRIPTS/vapi_analytics.sh summary --days 30
$SCRIPTS/vapi_analytics.sh ends --days 14      # groupBy endedReason
$SCRIPTS/vapi_analytics.sh cost --days 14 --step day
$SCRIPTS/vapi_analytics.sh success
$SCRIPTS/vapi_analytics.sh calls 20            # tabular recent calls
$SCRIPTS/vapi_analytics.sh get <call_id>       # summary + transcript preview
$SCRIPTS/vapi_analytics.sh query '[{"table":"call","name":"x","operations":[{"operation":"count","column":"id"}]}]'
$SCRIPTS/vapi_analytics.sh cli assistant list  # pass-through to official CLI
```

Dashboard UI: https://dashboard.vapi.ai/ · API docs: https://docs.vapi.ai/api-reference/analytics/get

### Pitfall: CLI `call list` unmarshal error

`vapi call list` (CLI v0.2.1) can fail with `cannot unmarshal string into Go struct field .embed.assistant`. Use `vapi_analytics.sh calls` / raw `GET /call` instead. `vapi call get <id>` still works.

## Phone references

- `templates/vapi_call.json` — known-good outbound payload (copy/modify)
- `templates/vapi_call_flight_change.json` — flight-change (no warm transfer)
- `templates/vapi_call_flight_change_warm_transfer.json` — flight-change + warm handoff + Levi fallback
- `templates/vapi_warm_transfer_tool.json` — reusable warm-transfer tool block
- `scripts/vapi_env.sh` — resolve private key + put CLI on PATH
- `scripts/vapi_analytics.sh` — analytics + call list/get helper
- `scripts/watch_call.sh` — poll until ended (`watch_call.sh <id>` key optional)

---

# Related

- **`gog`** — full Gmail API ops, auth, triage labels (canonical for gog)
- **`financial-operations`** — live Chrome CDP (shared by gog OAuth + banks)
- **`yuanbao`** — 元宝 group gateway @mentions (leave separate)
- **`operator-status`** — feed digests that consume mail triage outputs
- Archived predecessors: `messaging`, `ai-phone-calls` (bodies also under `references/*-skill.md`)
