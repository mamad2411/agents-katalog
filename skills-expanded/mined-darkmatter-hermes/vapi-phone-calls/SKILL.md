---
name: vapi-phone-calls
description: >-
  Outbound AI phone calls for Cooper via Vapi (Twilio transport + ElevenLabs voice + Levi/Personal Concierge).
  Use when calling businesses/support, warm-transferring a human, DTMF/IVR navigation, mid-call ask_cooper HITL,
  killing runaway calls, payment-on-call, or Vapi CLI/analytics. Complements umbrella communications Mode C —
  prefer this skill for Vapi-specific ops learned/hardened in live sessions.
version: 1.0.0
metadata:
  hermes:
    tags: [phone, vapi, twilio, elevenlabs, dtmf, hitl, warm-transfer]
    category: communication
    related_skills: [communications, financial-operations]
---

# Vapi phone calls (Levi)

Stack: **Vapi** → **Twilio PSTN** → **ElevenLabs**. Permanent assistant **Personal Concierge** (persona **Levi**). One-off work lives in **`assistantOverrides` only** — never PATCH the standing assistant for a single task.

Related umbrella (email/iMessage): `communications`. This skill owns phone-call ops.

## Standing IDs / secrets

| Piece | Where |
|---|---|
| Private API key | 1Password item `vapi` → **`credential`** (not `username`/public) |
| Twilio SID/token | same item `twilio-sid` / `twilio-token` |
| `phoneNumberId` | `68092f67-e7eb-4df9-8a39-e930eb99270d` (or `GET /phone-number`) |
| Assistant id | `86a092df-2332-4092-bf2d-2cd02c66ac4a` |
| DTMF tool | `c0849875-e579-454c-a1ee-95c969534fb8` (`function.name=dtmf`, param **`keys`**) |
| ask_cooper tool | `f30e31b9-f6ee-48f6-8bec-1d518a43e369` |
| HITL Slack DM | Hermes bot ↔ Cooper **`D0BG4HJ47GE`** (`U092MDGBK0R`) — not openclaw D0AK… |
| Warm-transfer default | `+12069542027` (override per call) |

```bash
source ~/.hermes/skills/communication/communications/scripts/vapi_env.sh
# or: export VAPI_API_KEY="$(op item get vapi --fields credential --reveal)"
```

Scripts live under the communications skill dir (shared):
- `scripts/vapi_env.sh`, `vapi_analytics.sh`, `watch_call.sh`
- `scripts/ask_cooper_server.py`, `start_ask_cooper_hitl.sh`
- templates: `vapi_call*.json`, `vapi_warm_transfer_tool.json`

## Pre-flight (before POST /call)

1. Single clear **GOAL** + facts + DO-NOT list.
2. **No parallel outbound** unless Cooper asks — `GET /call?limit=10` must show zero `in-progress|ringing|queued`.
3. If money/cancel involved:
   - Payment ready **or** explicit quote-only.
   - Explicit **$ cap**; over cap → must call `ask_cooper` first.
   - **Never** approve irreversible cancel / remove-from-flight / "proceed" without card **and** authority.
4. Attach tools deliberately: `toolIds: [dtmf, ask_cooper]` + inline warm-transfer only when needed.
5. Hold-proof: `firstMessageMode: assistant-waits-for-user`, `maxDurationSeconds`/`silenceTimeoutSeconds` high for queues.

## DTMF vs keypad input vs SIP INFO

| Setting | Direction | Default |
|---|---|---|
| Tool `dtmf` | Levi → IVR | **ON** for menus ("press 1") — prefer tones over spoken digits |
| `keypadInputPlan` | human keypad → Levi | **OFF** unless inbound digit collection |
| `sipInfoDtmfEnabled` | signaling | **OFF** on Twilio PSTN (RFC 2833). SIP-trunk edge cases only |

**Duplicate DTMF 400:** cannot combine dashboard `toolIds` DTMF with another inline `{"type":"dtmf"}` in the same override. One only.

**IVR record locators:** slow phonetic every time
`W as in whiskey... S as in sierra... Z as in zulu...`
Bare letters get mangled by airline STT. After two failures → 0 / representative, don't thrash speech.

## Warm transfer (preferred handoff)

Not cold `controlUrl` `{"type":"transfer"}` (ends `assistant-forwarded-call`, no Levi fallback).

Use `transferCall` + destination `transferPlan.mode: "warm-transfer-experimental"`:

1. Levi solos IVR + hold until a **real human** greets.
2. Try warm transfer to Cooper’s human once.
3. No answer / VM / decline → `transferCancel` → Levi finishes himself (`request-failed` / cancel messages: `endCallAfterSpokenEnabled: false`).

Templates: `templates/vapi_warm_transfer_tool.json`, `vapi_call_flight_change_warm_transfer.json`.

## Mid-call ask_cooper (HITL)

Blocking sync function tool → local server → Slack DM → reply.

```bash
export SLACK_BOT_TOKEN=<REDACTED>
export SLACK_CHANNEL=D0BG4HJ47GE
python3 ~/.hermes/skills/communication/communications/scripts/ask_cooper_server.py
# other terminal:
cloudflared tunnel --url http://127.0.0.1:8788
# PATCH tool server.url when tunnel URL changes
```

Answer: reply in Hermes DM, or
`curl -sS -X POST localhost:8788/reply -H 'Content-Type: application/json' -d '{"id":"…","answer":"fee ok up to $200"}'`

Timeout ~90s → `NO_REPLY_TIMEOUT`; continue under guardrails only (no invented spend authority).

**Any payment/cancel call must include ask_cooper** and a prompt rule requiring it before irreversible actions.

## Kill runaway calls (user says stop / looping)

Live API often shows **`transcript_len=0` for a long time** while $ still accrues — don't wait for transcript.

1. `POST controlUrl` system STOP (`triggerResponseEnabled: true`)
2. `POST controlUrl` `{"type":"end-call"}`
3. Still active → `DELETE /call/{id}`
4. Hard hangup: Twilio `POST …/Calls/{phoneCallProviderId}.json` `Status=completed`
5. Verify no actives; kill `watch_call.sh` for that id
6. **Do not redial** until Cooper explicitly okays after PNR/app check

Detail recipes: `references/kill-and-ops.md`.

## Payment-on-call rules

- Full PAN only in ephemeral override (mode 600 file → POST → **scrub/unlink**). Last4 only in chat.
- Speak cards digit-by-digit when asked.
- **1–2 declines → stop retry loops**, ask bank/cardholder on line, or different card via ask_cooper. No five-fold PAN re-reads.
- Cardholder verification: agent calls **Cooper (310) 989-7067** and/or warm-transfer. Prompt must say this — live inject alone may arrive too late.
- Cancel→travel-credit→rebook is high-risk; verify app/email credit before a second call.

## Messaging during hold

- Twilio SMS from agent long-code often **30034** A2P undelivered — don't retry spam.
- Prefer **iMessage**: write a temp `.scpt`, `osascript /tmp/….scpt` (service type `iMessage`). Avoid complex `osascript -e` with em-dashes/smart quotes (shell `-2741`).
- BlueBubbles apple-script API needs `tempGuid` + `message`; private-api needs helper (often false on Tahoe).

## Live inject

```bash
curl -sS -X POST "$CONTROL" -H 'Content-Type: application/json' \
  -d '{"type":"add-message","message":{"role":"system","content":"…"},"triggerResponseEnabled":false}'
```

Also supports `say`, `end-call`, warm `transfer` destination. Scrub any card-bearing inject files immediately.

## CLI + analytics

- Binary: `~/.vapi/bin/vapi` / `~/.local/bin/vapi`; `~/.vapi-cli.yaml` mode 600.
- Prefer `scripts/vapi_analytics.sh` — CLI `call list` can fail schema drift on 0.2.1.
- Analytics `groupBy` must be an **array**: `["endedReason"]`.
  `POST https://api.vapi.ai/analytics` with private key.

## Prompt skeleton (outbound)

1. Identity + who authorized
2. ONE GOAL (caps)
3. Facts only
4. IVR: short phrases + phonetic locators + dtmf for keypad
5. Hold: silent
6. Warm-transfer ONCE after human greets (if configured)
7. Spend cap + ask_cooper gates
8. Payment digits only if pre-authorized; else quote-only
9. WRAP-UP: confs, amount, ticketed y/n, case #

## Do NOT

- Multiple concurrent AA (or same-goal) outbounds.
- Cold-transfer mid-IVR hoping a human can rejoin later.
- Infinite payment retries / cancel without card.
- Leave PAN JSON under `/tmp` after fire.
- Trust empty live transcript as "call idle".
- Auto-redial after messy cancel/credit without Cooper + PNR check.
