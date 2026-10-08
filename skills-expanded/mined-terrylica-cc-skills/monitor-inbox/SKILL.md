---
name: monitor-inbox
description: Monitor INCOMING Pushover notifications (the messages that ARRIVE on the account — e.g. noip-ddns self-healer alerts) from a Claude Code session, via the Pushover Open Client API. On-demand pull, not a background daemon. Register a dedicated receive-device once (masked account-password prompt, password never stored), then pull new messages headlessly into a local JSONL inbox. Use when the user asks to read, check, watch, or monitor received/incoming Pushover messages, or what alerts landed. TRIGGERS - monitor pushover, incoming pushover, received notifications, check pushover inbox, what alerts arrived, pull pushover messages, read incoming alerts.
---

# monitor-inbox

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

The rest of pushover-commander only **sends**; its audit log (`po-audit.jsonl`)
can never show what **arrived**. This skill wraps the Pushover **Open Client API**
(the REST surface the desktop/mobile apps use to _receive_) so a session can read
incoming notifications. Core: `_lib/pushover_inbox.ts`.

Model = **on-demand pull** (run `pull` when asked; no background daemon).

## Commands

```bash
CORE="$(cc-plugin-root pushover-commander)/skills/_lib/pushover_inbox.ts"

# One-time, INTERACTIVE — mints a receive-device. Prompts for the Pushover ACCOUNT
# email + password (password is MASKED, used once in-memory, NEVER stored). Only the
# derived client secret + device_id are persisted, to the SCS vault scope `pushover`.
env -u HTTPS_PROXY -u HTTP_PROXY bun "$CORE" register [--name claude-mac] [--force]

# On demand — fetch new messages → append to po-inbox.jsonl → ack (update_highest).
env -u HTTPS_PROXY -u HTTP_PROXY bun "$CORE" pull [--json] [--limit N]

# Read back the local inbox (NO network).
bun "$CORE" list [--limit N] [--json]

# Health: creds present? device registered? API reachable / how many waiting?
env -u HTTPS_PROXY -u HTTP_PROXY bun "$CORE" doctor
```

## One-time setup (operator must run `register`)

Only the operator can type the account password, so **guide them to run `register`
themselves** (or run it and let them type into the masked prompt). After that,
`pull`/`list`/`doctor` all work headlessly — no password, no Touch ID — because the
client secret + device_id live in the vault **automation tier** (agent-readable).

## Secret handling (SCS doctrine — `cc-skills/docs/self-custody-secrets.md`)

| Secret                        | Class            | Where it lives                                                                              |
| ----------------------------- | ---------------- | ------------------------------------------------------------------------------------------- |
| Account email + password      | **crown jewel**  | masked prompt, in-memory only — **never stored / never sent / never in argv or transcript** |
| client `secret` + `device_id` | automation token | SCS `vault` scope `pushover` (agent-readable, so headless `pull` needs no prompt)           |

Never Pushover, email, commit, or otherwise transmit any of these off-machine.

## Caveats (verified 2026-07-05)

- **No history back-fill.** A freshly-registered Open-Client device only receives
  messages sent **after** registration. It will NOT pull the alerts already sitting
  in the native Pushover.app. Register first, then future alerts arrive.
- **IMAP-style queue.** `messages.json` returns the pending queue; `pull` calls
  `update_highest` to ack, else the same messages re-download every time.
- **Desktop/Open-Client license.** Registering a receive-device may require a
  Pushover Desktop license on the account. If so, `/1/devices.json` errors — the
  message is surfaced verbatim by `register`.
- **2FA.** If the account has two-factor enabled, `register` re-prompts for the code
  and retries login.
- **Proxies.** Always `env -u HTTPS_PROXY -u HTTP_PROXY` for the network commands, so
  Pushover HTTPS bypasses the sandbox MITM proxy (otherwise 502).

## Files

- Core: `_lib/pushover_inbox.ts`
- Inbox log: `~/.local/state/pushover/po-inbox.jsonl` (UUID-keyed, sits beside the
  send-side `po-audit.jsonl`); override with `PUSHOVER_INBOX_PATH`.
- Creds: SCS vault scope `pushover` → `client.secret`, `client.device_id`,
  `client.device_name`.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did `pull` actually ack?** If the same messages reappear on the next `pull`,
   `update_highest` isn't landing — fix the ack path, not the reader.
2. **Did the operator expect an alert that didn't arrive?** Confirm it was sent
   _after_ `register` (no back-fill) before assuming a bug.
3. **Any credential leak surface?** The account password must never appear in a log,
   argv, the inbox JSONL, or a transcript. If it did, that's a real defect — fix now.

Only update if the issue is real and reproducible — not speculative.
