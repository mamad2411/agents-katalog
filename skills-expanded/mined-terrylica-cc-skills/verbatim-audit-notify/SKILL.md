---
name: verbatim-audit-notify
description: Send Pushover notifications with UUID-linked verbatim JSONL audit trail. TRIGGERS - pushover notify, send pushover, observability alert, verbatim notification, fleet alert, pushover-lookup, audit log notification, push notification with UUID
---

# Pushover Verbatim+UUID Notification

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

A two-script skill that solves the **"Pushover message hit my phone but I don't remember what it was about"** problem for personal automation fleets. Every notification carries a UUID; the full verbatim payload (including everything that didn't fit in Pushover's 1024-char body) lands in a local JSONL audit log keyed by that UUID. You look it up by pasting the UUID back.

**Designed for**: cron-fired scripts, launchd daemons, hook outputs — any place that wants "fire-and-forget alerting with full context if you ever need to dig in." Personal scale; one Mac; one Pushover account. Not a microservices observability stack.

## Why this exists

Pushover messages are limited to 1024 UTF-8 characters in the body and 250 in the title (per [pushover.net/api](https://pushover.net/api)). Real failure events often need thousands of chars of context: stack traces, full env dumps, file paths, the exact failing command. Truncating loses what you actually need to debug.

The fix is the **correlation-ID-plus-JSONL** pattern: short summary on the device, full verbatim payload in a local newline-delimited JSON file, UUID linking them. When a notification fires, the body contains the UUID and a `pushover-lookup` command. Run that and you get the complete entry.

## Five scripts + three launchd templates

| Asset                                            | Role                                                                                            |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `scripts/pushover-notify.sh`                     | Sender: generates UUID, writes verbatim JSONL, dispatches Pushover with summary+UUID            |
| `scripts/pushover-lookup.sh`                     | Retriever: given a UUID (or prefix), prints the pretty-printed JSONL entry                      |
| `scripts/pushover-prune.sh`                      | Retention pruner: deletes audit-YYYYMMDD.jsonl files older than N days (default 30)             |
| `scripts/pushover-quota.sh`                      | Quota monitor: hits Pushover /apps/limits.json, persists JSON, alerts when low (iter 12b)       |
| `scripts/pushover-heartbeat.sh`                  | Daily fleet status summary — companion+kokoro+github-notif+quota+disk+failed services (iter 20) |
| `templates/com.terryli.pushover-prune.plist`     | launchd timer — daily at 04:15, 90-day retention (iter 8)                                       |
| `templates/com.terryli.pushover-quota.plist`     | launchd timer — daily at 03:30, alerts when remaining <20% (iter 12b)                           |
| `templates/com.terryli.pushover-heartbeat.plist` | launchd timer — daily at 09:03, INFO heartbeat (auto-promotes to WARN on failure) (iter 20)     |

Add the scripts to your PATH:

```bash
ln -sf "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/scripts/pushover-notify.sh" ~/.local/bin/pushover-notify
ln -sf "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/scripts/pushover-lookup.sh" ~/.local/bin/pushover-lookup
ln -sf "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/scripts/pushover-prune.sh" ~/.local/bin/pushover-prune
ln -sf "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/scripts/pushover-quota.sh" ~/.local/bin/pushover-quota
ln -sf "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/scripts/pushover-heartbeat.sh" ~/.local/bin/pushover-heartbeat
```

**Verify the symlinks resolve to THIS skill** (iter 13a 2026-05-19 caught the trap where stale symlinks from a legacy pushover-notify in `~/.claude/tools/notifications/` silently masked the new flag-rich script — the legacy didn't understand `--service/--level/--extra`, so dispatches "succeeded" but wrote no JSONL audit and sent malformed Pushover payloads):

```bash
for cmd in pushover-notify pushover-lookup pushover-prune pushover-quota; do
    readlink "$HOME/.local/bin/$cmd" | grep -q "cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify" \
        && echo "✓ $cmd → iter-5 skill" \
        || echo "✗ $cmd → STALE target ($(readlink "$HOME/.local/bin/$cmd" || echo 'not a symlink')) — rerun the ln -sf commands above"
done
```

Then sanity-fire the alert path once to catch any other silent failures:

```bash
pushover-quota --alert-threshold 1.0   # always fires; check phone + audit log
pushover-lookup --recent 2             # confirm WARN + pushover-notify dispatch lines pair up
```

Install the launchd timers (retention + quota monitor — see each template header for tuning):

```bash
# Retention (daily 04:15, 90-day window)
cp "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/templates/com.terryli.pushover-prune.plist" ~/Library/LaunchAgents/
mkdir -p ~/.local/state/launchd-logs/pushover-prune
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.terryli.pushover-prune.plist

# Quota monitor (daily 03:30, alert at <20% remaining)
cp "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/templates/com.terryli.pushover-quota.plist" ~/Library/LaunchAgents/
mkdir -p ~/.local/state/launchd-logs/pushover-quota
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.terryli.pushover-quota.plist

# Daily fleet heartbeat (09:03, INFO; auto-promotes to WARN on failure)
cp "$HOME/.claude/plugins/marketplaces/cc-skills/plugins/pushover-commander/skills/verbatim-audit-notify/templates/com.terryli.pushover-heartbeat.plist" ~/Library/LaunchAgents/
mkdir -p ~/.local/state/launchd-logs/pushover-heartbeat
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.terryli.pushover-heartbeat.plist
```

### Heartbeat sample output (iter 20)

```text
🔔 Fleet daily heartbeat

companion: ok · up 11h 36m · 320MB · audio✓ · bot=watching · tts=ready
kokoro: ok · idle=-1s · queue=0
pushover quota: 611/10000 (6.11%)
disk: launchd-logs=119MB · audit days=1
failed services: com.terryli.maccy-backup=1
```

Auto-promotes from INFO (silent) to WARN when any subsystem is degraded (companion or kokoro not `ok`, OR any `com.terryli.*` launchd service has `last_exit != 0`). The structured `--extra` payload captures every dimension as JSON for forensic lookup via `pushover-lookup`.

## Quick start

### Send a notification

```bash
pushover-notify \
    --title "maccy-backup failure" \
    --message "Maccy DB unreadable for 31 days; backup script needs TCC Full Disk Access" \
    --service maccy-backup \
    --level ERROR \
    --extra '{"db_path":"/Users/terryli/Library/Containers/org.p0deje.Maccy/Data/Library/Application Support/Maccy/Storage.sqlite","last_success":"2026-04-17","days_since":31}'
```

**Optional device targeting + sound override** (iter 14, 2026-05-19) — useful for high-priority events that should land on a specific device with an attention-grabbing sound:

```bash
pushover-notify \
    --title "Telegram rate-limit" \
    --message "Bot blocked for 4900s" \
    --service telegram-bot \
    --target rate-limit \
    --level ERROR \
    --priority 1 \
    --device iphone_13_mini \
    --sound siren
```

`--device <name>` sends only to the named Pushover device (omit to broadcast to all). `--sound <name>` selects the alert tone (`siren`, `magic`, `intermission`, `none`, etc.); the chosen device+sound are also persisted into the JSONL audit entry for forensic completeness.

Output (stdout): the UUID, e.g.

```
3f8c2d9e-4a1b-4c5d-8e7f-1a2b3c4d5e6f
```

Your phone receives:

```
[maccy-backup] level=ERROR priority=1
Maccy DB unreadable for 31 days; backup script needs TCC Full Disk Access

lookup: pushover-lookup 3f8c2d9e-4a1b-4c5d-8e7f-1a2b3c4d5e6f

UUID: 3f8c2d9e-4a1b-4c5d-8e7f-1a2b3c4d5e6f
```

### Look it up

Paste the UUID back:

```bash
pushover-lookup 3f8c2d9e-4a1b-4c5d-8e7f-1a2b3c4d5e6f
```

Or pipe the whole Pushover message body:

```bash
pbpaste | pushover-lookup
```

Output: full pretty-printed JSON with **every** field that was in `--extra`, plus the canonical schema.

## JSONL schema

Each line in `~/.local/state/pushover/audit-YYYYMMDD.jsonl` is one event:

```json
{
  "run_id": "3f8c2d9e-4a1b-4c5d-8e7f-1a2b3c4d5e6f",
  "ts": "2026-05-19T07:23:01.123Z",
  "host": "terryli-mbp",
  "service": "maccy-backup",
  "actor": "launchd",
  "target": "Storage.sqlite",
  "level": "ERROR",
  "title": "maccy-backup failure",
  "message": "Maccy DB unreadable...",
  "priority": 1,
  "extra": {
    "db_path": "...",
    "last_success": "2026-04-17",
    "days_since": 31
  }
}
```

Followups (the Pushover API response, dispatch failures) are appended as separate lines with the same `run_id` — so `jq -c 'select(.run_id == "...")' *.jsonl` reconstructs the full timeline.

## Credentials

By default, the sender pulls Pushover credentials from 1Password Claude Automation vault, item `<pushover-item>` (registered in `docs/1password-credential-registry.md`). It follows the cc-skills canonical pattern:

1. Unset `HTTPS_PROXY` / `HTTP_PROXY` (Claude Code OAuth proxy returns 502 on 1P endpoints)
2. Try Service Account token first (`~/.claude/.secrets/op-service-account-token`)
3. Fall back to biometric (`unset OP_SERVICE_ACCOUNT_TOKEN; op read ...`) on permission denied

Override for testing / non-1P environments:

```bash
PUSHOVER_TOKEN=... PUSHOVER_USER=... pushover-notify ...
```

Or skip the remote call entirely (write JSONL only):

```bash
NO_PUSHOVER=1 pushover-notify ...
```

## Priority and TTL

| Level | Default priority | Phone behavior                                                |
| ----- | ---------------- | ------------------------------------------------------------- |
| INFO  | -1               | Silent (no sound, no vibration); inbox-only                   |
| WARN  | 0                | Default sound and vibration                                   |
| ERROR | 1                | Bypass quiet hours                                            |
| —     | 2 (manual)       | Emergency — repeats until acknowledged (retry=30, expire=600) |

For low-signal events (heartbeats, "nothing changed" pings) set a TTL so the message self-expires on the phone:

```bash
pushover-notify --level INFO --ttl 300 --title heartbeat --message "..." --service some-service
```

## Wrapper patterns for common use cases

### Wrap a launchd script (alert on failure only)

```bash
#!/bin/bash
set -e
LOG=$(mktemp)
if ! /path/to/your/script.sh > "$LOG" 2>&1; then
    pushover-notify \
        --title "script.sh failed (exit $?)" \
        --message "$(tail -c 400 "$LOG")" \
        --service script-name \
        --level ERROR \
        --extra "$(jq -Rs '{stdout_tail: .}' < "$LOG")"
    exit 1
fi
```

### Use from a pipe

```bash
some-long-running-job 2>&1 \
    | tee /tmp/job.log \
    | tail -n 0  # block until job done
pushover-notify \
    --title "job completed" \
    --service my-job \
    --message "$(tail -c 500 /tmp/job.log)" \
    --extra "$(jq -Rs --arg exit "$?" '{exit_code: ($exit | tonumber), log_tail: .}' < /tmp/job.log)"
```

## Operational notes

- **Log location**: `~/.local/state/pushover/audit-YYYYMMDD.jsonl` — one file per UTC day.
- **Rotation vs retention** (iter 7, 2026-05-19): the per-day filename gives you natural size-rotation for free — every UTC midnight a new file starts, so size never grows unboundedly within a file. Size-based rotation in `~/.config/log-rotation.conf` is therefore **not needed and intentionally not wired** (the conf file documents this explicitly). What IS needed is **retention** — pruning old days. `pushover-prune` handles this: default 30-day window, dry-run by default, never deletes today's file. Run manually or wire into a daily launchd timer:

  ```bash
  pushover-prune                  # show what would be pruned (30d default)
  pushover-prune --apply          # delete files older than 30 days
  pushover-prune --keep 7 --apply # tighter 7-day window
  ```

- **Privacy**: JSONL is on the local Mac. Pushover only sees what's in the message body (1024 chars max). Secrets should NOT go in `--message` or `--title`.
- **Tested**: Pushover-side validated end-to-end during iter 4 (test UUID `C3B649E1-BF34-4346-A211-511EFE7CDCBD` delivered). Prune script boundary-tested iter 7 (today's file preserved even at `--keep 0`).

## References

- [Pushover API docs](https://pushover.net/api) — message format, priorities, receipts
- [Pushover May 2026 quota changes](https://blog.pushover.net/posts/2026/4/app-limits) — per-account 10k msgs/month
- 1Password registry: `docs/1password-credential-registry.md`
- Companion hook: `plugins/devops-tools/hooks/posttooluse-1password-pattern-reminder.sh` (reminds Claude of credential pattern)

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the notification deliver?** — Pushover returns a receipt token; if delivery silently failed, fix the instruction (auth, rate-limit, malformed body) that caused it.
2. **Did the JSONL audit entry write correctly?** — `pushover-lookup <uuid>` should round-trip the full payload. If not, the writer is dropping fields — fix the schema.
3. **Was the message truncated?** — If the body exceeded 1024 chars, confirm the `--extra` payload captured everything that didn't fit. Update Usage examples if the truncation boundary moved.
4. **Did `pushover-lookup` find by UUID prefix?** — If only the full UUID worked, the prefix-search needs fixing.

Only update if the issue is real and reproducible — not speculative.
