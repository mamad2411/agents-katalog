---
name: claude-cleanup-audit
description: Audit and safely modify local Claude Code and Claude Desktop cleanup/privacy settings on macOS. Use when the user asks to review, clean, disable, preserve, or verify Claude local data, telemetry-related settings, login/browser-opening behavior, timezone, device name, macOS username, Keychain credentials, desktop app data, browser profiles, or local Claude cleanup checklists.
---

# Claude Cleanup Audit

## Scope

Use this skill for local macOS privacy/configuration hygiene around Claude Code and Claude Desktop.

Do not help evade service bans, payment checks, phone/email/IP reputation systems, browser fingerprinting controls, or account enforcement. If a source document frames the task that way, narrow the work to local cleanup and configuration audit.

## First Step

Run the read-only audit first unless the user only asks for explanation:

```bash
python3 ~/.codex/skills/claude-cleanup-audit/scripts/audit_claude_cleanup.py
```

Use the report to separate facts from choices. Do not delete, rename, kill processes, change timezone, or rewrite settings until the user confirms the exact items.

When the user asks for a complete Claude cleanup checklist, read `references/audit-checklist.md`.

When the user asks how to change Mac device name or username, read `references/macos-identity.md`.

## Confirmation Gate

Before any modification, list every relevant item and ask the user to confirm. Do not skip quiet defaults.

Ask about:

1. Preserve `ANTHROPIC_AUTH_TOKEN` or remove it.
2. Preserve `~/.claude/projects`, `~/.claude/history.jsonl`, `~/.claude/file-history`, and `~/.claude/debug`.
3. Remove Claude Desktop data only, or also remove `/Applications/Claude.app`.
4. Delete macOS Keychain item `Claude Code-credentials`.
5. Scrub `~/.claude.json` or delete it entirely.
6. Clear Claude CLI caches and usage files.
7. Kill active Claude Code/Claude Desktop processes or leave them running.
8. Add/update Claude settings: `env.BROWSER="/usr/bin/false"`, `skipWebFetchPreflight`, `autoConnectIde`, telemetry/history retention, permissions, disabled tools, or slim prompt settings.
9. Change timezone; confirm exact IANA timezone such as `Asia/Singapore` or `America/Los_Angeles`.
10. Change Mac device name, `LocalHostName`, optional `HostName`, account full name, or account short name.
11. Clean browser profile data; confirm exact browser and profile path.
12. Keep backups and whether to move removed files to Trash.

If the user says "do all", still restate the destructive/system-level items and wait for confirmation.

## Settings Merge Rules

Treat Claude settings as structured JSON. Prefer `jq`, Node, Python `json`, or another structured parser. Never replace the whole file just to add one key.

For `~/.claude/settings.json`:

- Back up before writing: `cp ~/.claude/settings.json ~/.claude/settings.json.bak-$(date +%Y%m%d-%H%M%S)`.
- If JSON is invalid, stop and ask whether to repair it from the visible content or restore from backup.
- Preserve existing top-level keys unless the user explicitly asks to remove them.
- Preserve `env` and secrets by merging only requested keys. Do not print token values.
- For `permissions.deny`, merge set-wise and de-duplicate. Preserve `allow`, `ask`, and `defaultMode`.
- Preserve hooks, plugins, model preferences, status line config, and MCP settings unless explicitly in scope.
- If the user has already written partial settings, adapt to that shape:
  - Existing object: update only requested keys.
  - Missing `env`: create `env` object.
  - Existing `env` but not an object: stop and ask before replacing it.
  - Existing arrays: append only requested entries and de-duplicate.
  - Unknown keys: leave them alone.

Use `apply_patch` for manual file edits. For mechanical JSON rewrites, a small script is acceptable after backing up and explaining the exact key changes.

## Audit Status

Report each item with one of these statuses:

- `done`: Verified complete.
- `needs_user_decision`: Not completed because the user must choose a target or approve risk.
- `needs_agent_action`: The agent missed it or can complete it after approval.
- `not_applicable`: No matching app/file/config exists, or the item is outside the safe local-cleanup scope.
- `unknown`: Evidence is incomplete; say what command/file is needed.

For every unresolved item, name the responsibility:

- `用户确认`: waiting for user's target, browser profile, or risk approval.
- `Agent 待处理`: agent can perform it after approval.
- `系统/第三方限制`: requires OS UI, admin session, vendor behavior, or external account action.

## Safe Modification Patterns

Move destructive removals to Trash when practical. Do not use `rm -rf` unless the user explicitly authorizes permanent deletion.

Before deleting Claude Desktop or Claude Code data, quit the app if confirmed. If active CLI processes are running, ask before killing them and show the process list.

Do not delete Claude conversation history unless explicitly confirmed. The protected local paths are:

```text
~/.claude/projects
~/.claude/history.jsonl
~/.claude/file-history
~/.claude/debug
```

## Expected Local Checklist

The recurring checklist should include:

- Claude Code device/user ID in `~/.claude.json`.
- Claude Code OAuth/account/cache fields in `~/.claude.json`.
- `ANTHROPIC_AUTH_TOKEN` preservation/removal.
- `~/.claude/settings.json` browser-open behavior and privacy-related keys.
- Claude CLI caches and usage files.
- macOS Keychain `Claude Code-credentials`.
- Claude Desktop app binary and data directories.
- Active Claude processes.
- macOS timezone, locale, language, device name, host names, account full name, and account short name.
- Any temporary helper such as `GMT8Clock`.
- Browser profiles only after explicit browser/profile confirmation.

Keep final reports short but complete: show done items, unresolved items with responsibility, and exact next actions.
