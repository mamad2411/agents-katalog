---
name: vapi-phone
description: >-
  Outbound AI phone calls via Vapi (Twilio + ElevenLabs, persona Levi Okada) for Cooper —
  credentials, light assistantOverrides, warm-transfer-experimental with Levi fallback,
  DTMF vs keypadInput vs SIP INFO, IVR phonetics, HITL ask_cooper/text_cooper, billing/payment
  guardrails, hangup/runaway kill, Studio BlueBubbles bb-hook.cm.xyz receive, handoff pings
  (iMessage/BB first; Twilio SMS often 30034), CLI/analytics. Use for placing/monitoring
  Vapi calls, warm handoff, mid-call human authority, card-on-call, or BB inbound. Complements
  communications Mode C for Vapi depth.
version: 1.5.0
metadata:
  hermes:
    tags: [vapi, phone, twilio, warm-transfer, dtmf, hitl, analytics, levi, bluebubbles, billing]
    category: communication
    related_skills: [communications]
---

# Vapi phone (outbound AI calls)

Stack: **Vapi** → **Twilio** → **ElevenLabs**. Persona **Levi Okada** = permanent assistant "Personal Concierge". Never PATCH the permanent assistant for one-offs — use `assistantOverrides`.

Overlaps **`communications` Mode C**. Prefer **this skill** for Vapi mechanics. Shared paths:

```text
PKG=~/.hermes/skills/communication/communications
SCRIPTS=$PKG/scripts
TEMPLATES=$PKG/templates
```

## Credentials

1Password **`vapi`**: `credential` = **PRIVATE** key (Bearer). Never `username` (public → 401 tip).

**Never bare interactive `op`** (biometric). Service account + **`--vault`** (required):

```bash
himitsu exec op-service-account/token -- bash -lc \
  'OP_SERVICE_ACCOUNT_TOKEN=$TOKEN op item get vapi --vault <vault> --format=json'
# Amex Platinum vault cm:nj33napkeiybo5o4fezookdb4i
# day-to-day Vapi key:
source $SCRIPTS/vapi_env.sh   # SOURCE only — bare exec dumps key into logs
```

CLI: `~/.vapi/bin/vapi` (`~/.local/bin/vapi`). Config `~/.vapi-cli.yaml` mode 600.

Known tool IDs (verify if rotated):

| Tool | ID |
|---|---|
| `dtmf` | `c0849875-e579-454c-a1ee-95c969534fb8` |
| `ask_cooper` | `f30e31b9-f6ee-48f6-8bec-1d518a43e369` |

## Prompt style + voice (Cooper — hard rules)

Agents hang people up when they **parrot and over-narrate**. Standing + override prompts MUST enforce:

- Keep system prompts **light**. Short facts + a few guidance lines beat multi-PHASE imperative trees.
- After a failed attempt, change **one** variable (phonetics / DTMF / carrier) — not a wall of conditionals.
- **Brief.** Real person: "got it", "sure", "yep", "one sec".
- **Do NOT parrot** the agent’s last sentence. No "just to confirm you’d like…".
- **Do NOT recap** the whole booking/payment story every turn — only correct errors or answer direct Qs.
- Don’t stack thanks/apologies; don’t narrate hold ("still holding, thank you") unless they pick back up.
- Yes/no first, then one short clause.
- First-message style: `Hey — Levi, Cooper’s assistant.`

User feedback (2026-07): "if we havent done so already - we need the agent to be less verbose… it repeats the details verbatim… putting people off… less professional and more concise." Also: "dont add too many imperative conditionals… just dont go overboard."

## Cooper defaults

- **Warm transfer preferred** over cold forward when a human handoff exists.
- Confirm handoff number each task (session examples used `+12069542027`).
- Status-ping handoff contact **when call starts** (on hold / will warm-connect / Levi fallback) via **iMessage/BB**, not Twilio SMS.
- If human misses/declines/VM → **Levi finishes the business task**.
- Reasonable fees OK when authorized. Callback: Cooper `(310) 989-7067` / `me@cooperm.com`.
- Full PAN/CVV only when payment authorized for **this** call (standing Platinum block or explicit card) — one card only; scrub temp payloads after POST.

## Levi identity (required in every outbound override)

Airlines/agents demand a **surname** and a **relation**. Encode both, flush:

1. Full name: **Levi Okada** (user-chosen; do not invent Hart/Brooks/etc. mid-call).
2. First chance on relation / "who is calling" / authority: **"I'm Levi Okada, Cooper Maruyama's assistant."** — no hedge, no authorization monologue.
3. Document caller as assistant for Cooper who authorized changes; callback Cooper's number/email.
4. Outbound override must restate **Levi Okada** even if standing inbound already says "assistant".

## SOP — outbound call

1. Gather: callee E.164, GOAL, facts only, handoff #, guardrails.
2. Template under `$TEMPLATES/` (strip `_comment` if API rejects). Warm: `vapi_call_flight_change_warm_transfer.json` / `vapi_warm_transfer_tool.json`.
3. Hold-proof: `firstMessageMode: assistant-waits-for-user`, `maxDurationSeconds: 7200`, `silenceTimeoutSeconds: 3600`, `keypadInputPlan.enabled: false`.
4. Pack tools carefully (see DTMF section). `POST /call` → save `id`, `controlUrl`, `listenUrl`.
5. **Status-ping handoff** (iMessage first — see channels).
6. `$SCRIPTS/watch_call.sh <id>` with `terminal(background=true, notify_on_complete=true)`.

## Warm-transfer-experimental

```
PHASE 1: IVR/hold alone — no transfer
PHASE 2: live human greets → warmTransferToHuman ONCE
  ├─ transferSuccessful → merge handoff ↔ agent; Levi exits
  └─ transferCancel / no answer / VM → Levi PHASE 3 completes GOAL
```

- `transferPlan.mode: "warm-transfer-experimental"`; cancel on voicemail in transferAssistant prompt.
- Tool `request-failed`: **`endCallAfterSpokenEnabled: false`**.
- **Cold** `controlUrl` `{"type":"transfer"}` → `assistant-forwarded-call`, **no Levi fallback**. Avoid when fallback required.
- Stock Vapi does **not** rejoin a party who drops after successful merge (needs Twilio Conference).

Detail checklist: `references/warm-transfer-sop.md`.

## DTMF vs keypad input vs SIP INFO

| Control | Direction | Outbound support calls |
|---|---|---|
| **`dtmf` tool** | Levi → IVR | **On** — param `keys` (`"1"`, `"2"`, `"0"`) |
| **`keypadInputPlan`** (dashboard "Keypad Input") | Human → Levi | **Off** |
| **`sipInfoDtmfEnabled`** | SIP INFO vs RFC 2833 | **Off** on Twilio PSTN |

Pitfalls:

- Two dtmf tools (toolId + inline) → **400** `more than one tool of type 'dtmf'`.
- Empty `function.parameters` on dtmf tool → useless; PATCH `keys` string required.
- Overrides don't magically merge tools — include every tool the call needs via `toolIds` and/or single inline blocks.
- PATCH assistant `model` needs full valid `provider`/`model` object (toolIds-only patch can 400).

## IVR record locators

Airline bots mangle bare codes (`WSZTVR` → `WSVTVR`/`WFZTVR` then disconnect). Use **slow phonetics**:

> W as in whiskey… S as in sierra… Z as in zulu… T as in tango… V as in victor… R as in romeo.

"Press 1/2" readback → **dtmf**, not spoken "two". Two fails → 0/rep or operating-carrier locator (e.g. BA). Ops notes: `references/ivr-and-channels.md`.

## Handoff status channels

Priority when notifying the human target at dial **or** mid-hold updates:

1. **Studio BlueBubbles** API (`hermes/bb-studio-url`) — body field **`message`** + `tempGuid` for apple-script; try private-api if helper true.
2. **iMessage osascript** on Pro (BB private-api often false on Tahoe Mac Pro).
3. **Twilio SMS** from Vapi long code frequently **error 30034** (A2P 10DLC) — never sole critical path.
4. HITL `text_cooper` once wired to BB/studio (preferred for Levi-initiated pings).

## Mid-call HITL (ask_cooper + text_cooper)

| Tool | Mode | Use |
|---|---|---|
| `ask_cooper` | **Sync block** | Fee authority, payment choice, irreversible cancel, compromises |
| `text_cooper` | Fire-and-return | Status iMessage to Cooper (or `to` override) while on hold |

- Server: `$SCRIPTS/ask_cooper_server.py` / `start_ask_cooper_hitl.sh` (`:8788`) — also `/imessage` helper
- Tunnel: `cloudflared tunnel --url http://127.0.0.1:8788` — **URL dies each restart**; PATCH tool `server.url` → `https://HOST/vapi/tools`
- Slack: Hermes bot DM **`D0BG4HJ47GE`** (Cooper `U092MDGBK0R`). Not openclaw DM ids (`channel_not_found` / wrong bot).
- Reply: text in that DM, or `POST localhost:8788/reply {"id","answer"}`.
- Timeout ~90s → `NO_REPLY_TIMEOUT` + existing guardrails (**no invented spend**).
- Manual inject without tool: `POST controlUrl` `add-message` + `triggerResponseEnabled`.
- **Must** `ask_cooper` (or human on line) before approving large/new fees beyond brief, canceling PNR without payment path, or after card declines.

`text_cooper` / status pings should prefer **Studio BlueBubbles** (see BB webhook section) over Pro osascript when Studio tunnel is up.

## Billing block (stop inventing cards)

Production failure mode: Levi kept a **wrong/stale PAN** despite inject / different Amex available.

Rules:

1. **One named card only** in the override (build at call time from 1Password; chmod 600 payload; **scrub file after POST**).
2. Default preferred card: **Amex Platinum** — 1P title `Amex Platinum` vault `cm`. Cardholder often **Koutarou Maruyama**. Coinbase One Amex only if Cooper explicitly chooses it.
3. Speak digit-by-digit when asked; never invent PAN/CVV/exp.
4. Billing ZIP try **90015**. If rejected, ask agent what ZIP is on file.
5. If airline requires **cardholder on the line**: have them call Cooper **(310) 989-7067** and/or warm-transfer — do not role-play as cardholder beyond authorized assistant.
6. Auto-approve cap from brief (e.g. ~$1200 rebook delta). Above that → `ask_cooper`.
7. **After 1–2 hard declines**: stop re-reading the same card; escalate. Do not thrash.
8. Live card swap mid-call: `add-message` with full Platinum digits + "do not use Coinbase One" + cardholder-call instruction (then scrub temp payload).

Permanent standing assistant prompt should **not** store full PAN. Put billing in **per-call overrides** or a secure short-lived inject.

## Hangup / runaway loops

If Levi cancels/rebooks/pays in circles or ignores STOP:

1. `controlUrl` system: stop cancel/rebook/pay; goodbye if needed.
2. `{"type":"end-call"}`.
3. If stuck `in-progress` with empty transcript: `DELETE /call/{id}` (works when end-call lags).
4. Twilio `POST Calls/{phoneCallProviderId}.json` `Status=completed`.
5. Confirm no other `in-progress`/`queued` outbounds to the airline.
6. Kill local `watch_call.sh` for that id.

Prefer **one** heavy support call at a time. After multi-agent mess (cancel then unpaid rebook), **verify PNR/app/email before redialing**.

## BlueBubbles Studio webhook (receive)

Stable inbound path for the agent-dedicated Studio BB:

| Piece | Value |
|---|---|
| Webhook | `https://bb-hook.cm.xyz/bb/webhook?secret=…` |
| Inbox | `GET https://bb-hook.cm.xyz/messages?secret=…` |
| Receiver | `$SCRIPTS/bb_webhook_server.py` `:8790` |
| CF tunnel | `hermes-pro-webhooks` → DNS `bb-hook.cm.xyz` |
| Secret | `~/.hermes/bb/webhook-secret` / `himitsu hermes/bb-hook-secret` |
| Meta | `~/.hermes/bb/config.json` |
| Studio API | **Stable** `https://bb-api.cm.xyz` (named CF tunnel on Studio; himitsu `hermes/bb-api-url` / `hermes/bb-studio-url`) |
| Studio iMessage | `cooperton42391@gmail.com` · host `coopers-mac-studio` / Tailscale `100.111.149.47` |

BB create webhook body: `{"url":"https://bb-hook.cm.xyz/bb/webhook?secret=SEC","events":["new-message","updated-message","message-send-error","chat-read-status-changed","typing-indicator"]}` (or `["*"]`).

```bash
PASS=$(sqlite3 "$HOME/Library/Application Support/bluebubbles-server/config.db" \
  "SELECT value FROM config WHERE name='password'")
curl -sS "https://bb-api.cm.xyz/api/v1/server/info?password=$PASS"
# send: field `message` (not only text); apple-script needs tempGuid
```

darwin durability (`machines.git`): `programs.bb-hook` (Pro webhook+tunnel), `programs.bb-studio` (Studio keep-alive + bb-api tunnel). Creds `~/.cloudflared/<id>.json` + webhook secret **not** in git. Studio cloudflared may be BB-app-bundled if brew missing. HM agents need `sudo darwin-rebuild switch`.
See `references/bluebubbles-studio-webhook.md`.

## Analytics + CLI

```bash
source $SCRIPTS/vapi_env.sh
$SCRIPTS/vapi_analytics.sh summary --days 14
$SCRIPTS/vapi_analytics.sh ends|cost|calls|get <id>
```

- Analytics **`groupBy` must be an array** (`["endedReason"]`).
- Prefer helper over `vapi call list` (CLI ≤0.2.1 unmarshal break). `vapi call get` OK.
- Heredoc after `curl | python` steals stdin — write API JSON to a temp file first.

## What this does NOT do

- Conference rejoin-on-drop after warm merge (custom Twilio).
- Email/iMessage umbrella (that's `communications`).

## References

- `references/ops-checklist.md` — preflight/during/after + AA lesson summary
- `references/warm-transfer-sop.md` — handoff checklist
- `references/ivr-and-channels.md` — DTMF/phonetics/SMS/iMessage/HITL + AA IVR failures
- `references/bluebubbles-studio-webhook.md` — stable bb-hook.cm.xyz receive path + Studio API
- `references/nix-bb-durable.md` — darwin modules, CF tunnels, LaunchAgents, rebuild host keys
- `references/payment-and-hangup.md` — billing block, decline limits, runaway kill sequence
- Shared templates/scripts under `$PKG/{templates,scripts}/` (incl. `bb_webhook_server.py`, `ask_cooper_server.py`)

Note: Umbrella `communications` is manually authored (curator cannot auto-patch). Keep deep Vapi ops **here**; mirror shared scripts/templates under that package when useful.

## Session durable lessons (encode, don't re-learn)

- **Status pings:** iMessage/BB first; Twilio long-code SMS often **30034** — never sole path.
- **Warm > cold** when Levi must fall back and finish (esp. pay).
- **ask_cooper required** before large fees / cancel without payment path / thrash after card decline.
- **Stable BB API** is `https://bb-api.cm.xyz` — not the trycloudflare quick tunnel UI string.
- **op:** service account always needs `--vault`; never bare biometric `op` in agent turns.
- After any cancel/pay mess: **verify PNR in app/email before redial**.
