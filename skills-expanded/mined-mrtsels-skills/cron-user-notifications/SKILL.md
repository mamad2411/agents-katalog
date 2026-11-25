---
name: cron-user-notifications
description: Use when scheduling cron reminders that must reach the user.
metadata:
  source_frontmatter:
    tags:
    - cron
    - reminder
    - notification
    - delivery
    - wechat
    triggers:
    - User asks for a reminder / alert / notification at a specific time ("remind me at 17:20")
    - Creating any cron job whose output must actually reach the user, from a TUI/CLI session
    - Choosing or debugging a cron `deliver` target
  imported_from: hermes
---

# Cron User Notifications

Scheduling cron jobs whose output must reach the user (reminders, deadline alerts, digests).

## Core rule

A cron job's output reaches the user ONLY when `deliver` points at a gateway-connected platform. The session type decides the default:

- **TUI/CLI sessions have NO live-delivery channel.** Jobs created there default to `deliver='local'` — output is saved (viewable via `cronjob action='list'`) but NEVER pushed. A "remind me at 17:20" request from TUI will silently do nothing visible unless `deliver` is changed.
- **Messaging sessions** (Telegram/WeChat/etc.): omitting `deliver` (or `'origin'`) auto-detects the current chat and works.

The tool result itself warns on create: "CLI/TUI sessions have no live-delivery channel. To be notified when it runs, recreate or update the job with deliver set to a gateway-connected platform."

## Workflow

1. **Write the reminder prompt SELF-CONTAINED** — cron runs in a fresh session with zero conversation context. Include: what to remind, why it matters (deadline, penalty), the relevant URL, and follow-up steps.
2. **Create the job**: `cronjob(action='create', name='<descriptive>', schedule='2026-08-10T17:20:00', prompt='...')` — ISO timestamps fire once; `'0 9 * * *'` for recurring.
3. **If the user is in TUI and expects a real notification, ASK which platform** — `clarify` with choices (Telegram / 微信 / other) before finalizing delivery. **This user picks WeChat.**
4. **Verify the gateway**: `hermes gateway status` → expect "Gateway is supervised by launchd (PID …)". The "stale plist" warning is cosmetic; only act if there is no PID line (then `hermes gateway start`).
5. **Point delivery at the platform**: `cronjob(action='update', job_id='<id>', deliver='weixin')`. Verify the returned job record: `deliver: weixin` + correct `next_run_at`.
6. **After the run**: `cronjob(action='list')` — `last_status: ok` with no `last_delivery_error` = delivered.

## Delivery targets

| deliver | effect |
|---|---|
| omit / `'origin'` | auto-detect current chat — only works from messaging sessions; from TUI resolves to local-only |
| `'local'` | save-only, never pushed (TUI default) |
| `'weixin'` | WeChat home channel — proven for this user (DeepSeek cost report, email triage, reminders) |
| `'telegram'` | Telegram home channel |
| `'all'` | fan out to every connected home channel |
| `'platform:chat_id:thread_id'` | explicit destination (thread suffix required for topic targeting) |

## Pitfalls

- **Never promise a TUI user that a default-created cron will notify them** — the job record showing `deliver: local` means they will never see the output.
- `deliver='origin'` from a TUI session is NOT a fix — it resolves to local-only.
- WeChat iLink rate limit ~30s cooldown; avoid burst pushes. A rate-limited delivery loses the output (not queued) — see `cron-agent-flow`'s Delivery Failure Recovery section.
- One-shot reminders: keep the prompt tight (URL + deadline + next step). WeChat messages should not contain reasoning blocks (user preference).
- Cron sessions have no conversation history — never write "as we discussed"; restate the context.
- **CLI send tools still demand two-phase confirmation inside a cron** — `agently-cli message +send` (≥1.0.10) returns `confirmation_required: true` + a `confirmation_token` even for a self-recipient cron send; older "cron sends go direct, no token" notes are outdated. Working pattern: first call grabs the ctk, re-run the identical command with `--confirmation-token ctk_xxx` in the same turn (no user to wait for); success = exit 0 + `"queued": true`. See `references/agently-cron-send.md`.
- **Cron sessions can inherit a stale/nonexistent cwd** (e.g. `research-claw/workspace` after a repo move) — every terminal call then fails with `cd: No such file or directory` before the real command runs. Pass `workdir` explicitly on terminal calls; write `--body-file` payloads relative to that explicit workdir.

## Related skills

- `wechat-push-message` (external): immediate/push-now mechanics via cronjob; complements this skill's scheduling + delivery-target logic.
- `cron-agent-flow` (external): agent-in-the-loop pipeline design (script → LLM → action); delivery-channel selection lives here instead.

## References

- `references/tui-reminder-example.md` — worked example: VeriGuide deadline reminder (create → clarify → gateway check → update deliver → verify).
- `references/agently-cron-send.md` — agently-cli `message +send` from cron: two-step confirmation-token flow, success signal, and pitfalls (relative `--body-file`, stale cwd, inline-python rejection).
