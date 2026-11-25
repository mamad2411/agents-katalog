---
name: vapi-call-ops
description: >
  Operate Cooper's Vapi outbound phone stack (persona Levi Okada) — place/monitor
  calls, warm-transfer-experimental with AI fallback, DTMF/IVR, mid-call HITL
  (ask_cooper Slack + text_cooper iMessage), payment-on-call guardrails, runaway
  hangup, BlueBubbles hold status, analytics/CLI. Use for any Vapi call work.
  Prefer this over the thinner overlapping vapi-phone / vapi-phone-calls /
  vapi-phone-ops stubs; also pair with communications Mode C for email/iMessage map.
version: 1.1.0
---

# Vapi call ops (Levi Okada)

## Standing identity (assistant `86a092df-2332-4092-bf2d-2cd02c66ac4a`)

- **Name:** Levi Okada (always full name; never “one name”)
- **Relation (immediate one-liner):** “I’m Levi Okada, Cooper Maruyama’s assistant.”
- **Cooper callback:** (310) 989-7067 · me@cooperm.com
- **First message:** short — “Hey — Levi, Cooper’s assistant.”

## Voice (user preference — critical)

People hang up when Levi drones. Standing model system prompt must enforce:

- **Brief.** One or two sentences; yes/no first.
- **Do not parrot** what the agent just said. No “just to confirm you said…”.
- **Do not recap** booking/payment every turn — only correct errors or answer questions.
- Casual-professional: “got it”, “sure”, “yep”, “one sec” OK.
- No stacked apologies/thanks; no hold-time narration unless they return on the line.
- One goodbye, hang up — don’t reopen.

Keep **billing digits / PNR spelling** available in-system, but speak them only when asked — don’t re-dump the whole brief every turn.

## Auth / secrets

```bash
# Vapi key (env → 1P → ~/.vapi-cli.yaml)
source ~/.hermes/skills/communication/communications/scripts/vapi_env.sh

# 1Password NON-interactive (never bare `op` — biometric):
himitsu exec op-service-account/token -- bash -lc \
  'OP_SERVICE_ACCOUNT_TOKEN=$TOKEN op item get <id> --vault <vault> --format json'
# Service accounts REQUIRE --vault (cm | cooper | dev).
# Amex Platinum (default pay card): vault cm, id nj33napkeiybo5o4fezookdb4i
```

## IDs (stable)

| Resource | ID |
|---|---|
| Assistant (Personal Concierge / Levi) | `86a092df-2332-4092-bf2d-2cd02c66ac4a` |
| Twilio phoneNumberId | `68092f67-e7eb-4df9-8a39-e930eb99270d` |
| DTMF tool | `c0849875-e579-454c-a1ee-95c969534fb8` (`keys` string) |
| ask_cooper tool | `f30e31b9-f6ee-48f6-8bec-1d518a43e369` |
| Handoff default | +1 (206) 954-2027 |
| HITL Slack DM | `D0BG4HJ47GE` (hermes_bot ↔ Cooper) |

## Call patterns

### Warm transfer + AI fallback (preferred over cold transfer)

Cold `control.type=transfer` → `assistant-forwarded-call` and **Levi cannot resume**.

Use **`warm-transfer-experimental`** with:

1. Phase 1: Levi alone through IVR/hold (tool description: **only after live human**)
2. Phase 2: warm transfer assistant to 206 (short confirm; cancel on VM/no-answer ~75s)
3. Phase 3: on cancel → Levi **stays** on airline and finishes the task
4. `request-failed` must use `endCallAfterSpokenEnabled: false` so a failed handoff doesn’t drop the airline

Templates: `communications/templates/vapi_call_flight_change_warm_transfer.json`, `vapi_warm_transfer_tool.json`.

### IVR / DTMF

| Setting | Use? |
|---|---|
| **DTMF / dial-keypad tool** | **ON** — Levi presses tones into IVR |
| **keypadInputPlan** | **OFF** for outbound overflow — that’s *inbound digits to the assistant*, not outbound tones |
| **SIP INFO DTMF** | **OFF** on Twilio PSTN (default RFC 2833) |

Conf codes: prefer **phonetic** (“W as in whiskey…”) and/or DTMF when the tree allows keypad; AA STT mangled `WSZTVR` when spoken as a blob.

### Tool usage (prompt + schema — required)

Name-only tool lists failed in live calls. Standing system prompt **and** each tool’s `function.description` need **what / when / don’t**:

| Tool | What | When | Don’t |
|---|---|---|---|
| **dtmf** | Keypad tones into the other party | IVR press 1/2/0; after ~3 conf-code speech fails | Spell PNR to a human with tones |
| **ask_cooper** | Blocking HITL ~90s | Overspend, itinerary fork, cardholder after declines, brief gap | IVR, small talk, “status only” |
| **text_cooper** / BB status | Fire-and-forget | Hold milestones / ticketed summary | Questions; PANs |
| **query-cooper-records** | KB search | Address/email/card/backup asked | Invent contacts or PAN |
| **warmTransferToHuman** | Warm bridge; cancel keeps Levi | Once, after live human greets | IVR/hold; transfer loops |

Call create: keep standing `toolIds` (dtmf + ask_cooper + query tool) when adding warm-transfer `tools[]`. Duplicate dtmf (inline + toolIds) → create error. Overrides that set `model.tools` can wipe toolIds — re-send them.

### Mid-call HITL

- **Durable server URL:** `https://ask-cooper.cm.xyz/vapi/tools` (Pro LaunchAgent → `:8788`; same CF tunnel host family as bb-hook — **not** trycloudflare)
- **Slack:** hermes_bot DM **`D0BG4HJ47GE`**
- **Reply preference:** (1) iMessage reply to Studio-BB ping, (2) Slack, (3) `POST /reply {"id","answer"}`
- **iMessage send identity:** Studio **`cooperton42391@gmail.com` only** via bb-api — never Pro `koutaroum@icloud.com` Messages/osascript (self-chat)
- **iMessage inbound:** poll bb-hook inbox; allowlist Cooper/206; one open ask → any reply; multi → include `[req_id]`
- Timeout → standing guardrails only (no new spend authority)
- Live control while `in-progress`: `say` / `add-message` / `end-call` on `monitor.controlUrl`

### Knowledge base (query-cooper-records)

Local `~/.hermes/vapi/kb/` + Vapi files (see `manifest.json`):

- contacts/addresses (home **1111 S Grand Apt 715** billing; condo **1155 Unit 1810** AT&T only)
- payment methods (Platinum primary + Coinbase One backup)
- ops/tool checklist

Standing prompt: **query before inventing** address/email/card.

### Payment-on-call

Only when **this call** authorizes pay:

- Default **Amex Platinum** (1P vault `cm`); backup Coinbase One **only** after 2 Platinum hard declines or explicit brief
- Name often **Koutarou Maruyama**; billing ZIP **90015** / home Apt 715 (not condo unless AT&T call)
- Cardholder live → Cooper **(310) 989-7067** or warm-transfer 206
- **Stop after 2 hard declines**; don’t thrash; no invented PANs
- Prefer standing billing + KB over fragile mid-call inject that the model may ignore

### Hold status / messaging

1. Studio BB iMessage first — never Twilio SMS from Vapi long code (**30034** A2P)
2. bb-api / bb-hook secrets as in **bluebubbles-studio**

### Hangup / runaway / airline retry budget

If Levi loops, empty stuck `in-progress`, or payment thrash:

1. `end-call` on controlUrl (+ optional short farewell)
2. If sticky: Vapi DELETE / force-end; confirm 0 live legs
3. **User preference:** max **2 failed call outcomes** then stop for human review
4. **AA callback queued** (place held on Cooper’s cell) is **not** a thrash-fail — **do not redial** until callback finishes or user cancels that path
5. After messy cancel/credit: no redial until PNR/credit/Amex state verified (app/email/online preferred)

## CLI / analytics

```bash
export PATH="$HOME/.vapi/bin:$PATH"
# groupBy MUST be an array for POST /analytics
~/.hermes/skills/communication/communications/scripts/vapi_analytics.sh summary|ends|cost|calls|get
# caveat: `vapi call list` broken on CLI 0.2.1 — use analytics/get instead
```

## Scripts / templates (under communications skill)

- `scripts/vapi_env.sh`, `watch_call.sh`, `vapi_analytics.sh`, `ask_cooper_server.py`, `bb_webhook_server.py`, `start_ask_cooper_hitl.sh`
- `templates/vapi_call*.json`, `vapi_warm_transfer_tool.json`

## Pitfalls

- **Overrides replace tools** — when setting `assistantOverrides.model.tools`, also keep DTMF via `toolIds` or re-include the dtmf tool; warm-only overrides once dropped DTMF.
- **Duplicate DTMF** (inline + toolIds) → API reject call create.
- Assistant PATCH via urllib sometimes 403; **curl + Bearer** is reliable.
- Empty live `transcript` while on hold is normal; don’t assume dead until status ends.
- Log PAN only in scrubbed temp files; never commit card payloads.
- **Ask_cooper extract_tool_calls** must read top-level **and** `message.toolCallList` (Vapi shapes vary); empty results = wrong extractor.
- Condo address (1155 Unit 1810) is **AT&T/service only** — card billing default is home **1111 Apt 715**.
- After cancel/credit chaos: **online verify** before another airfare spend.
- **AA callback queues:** do not burn the 2-attempt budget or re-dial while place-in-line is held for Cooper’s cell — wait or cancel with user.
- **Tool teaching:** if calls ignore tools, check standing TOOLS table **and** `function.description` — name-only lists are insufficient.
- **Vapi Files/KB:** good for addresses/emails/cards/backups/ops markdown; still rate-limit PANS spoken; teach “query before invent”.

## Related skills

- `communications` — email/iMessage umbrella Mode C pointer
- `bluebubbles-studio` — Studio-only iMessage identity + hooks
- `financial-operations` — 1P service-token pattern for card pull
- Darwin BB durable tunnels in `~/darwin` modules `bb-hook` / `bb-studio`

**Overlap note:** `vapi-phone`, `vapi-phone-calls`, `vapi-phone-ops` still exist as thinner stubs — prefer **this** umbrella (`vapi-call-ops`) so ops don’t three-way diverge.

## Support files

- `references/warm-transfer-and-hitl.md` — transfer JSON + ask_cooper loop
- `references/bluebubbles-status.md` — bb-api / bb-hook, A2P 30034, flake host attr, netrc 401
- `references/airline-rebook-lessons.md` — AA WSZTVR session lessons, retry budget, online fallover
