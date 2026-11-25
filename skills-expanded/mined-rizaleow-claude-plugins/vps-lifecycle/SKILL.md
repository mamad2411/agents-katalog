---
description: Manage Hostinger VPS lifecycle — list/inspect VMs, start, stop, restart, recreate, take/restore snapshots, and wait for async actions to finish. Use when the user wants to act on a Hostinger virtual machine.
---

# VPS lifecycle via `hostinger-cli`

## Preflight (run before any command)

1. `command -v hostinger-cli` — if missing, tell the user to install:
   `brew install rizaleow/tap/hostinger-cli` (or `go install github.com/rizaleow/hostinger-cli/cmd/hostinger-cli@latest`).
2. `hostinger-cli auth status` — if not logged in, tell the user to run
   `hostinger-cli auth login`. Do **not** prompt for or store tokens
   yourself; the CLI handles its own keychain/config resolution.

## Commands

All VM mutating commands accept `--wait` and `--wait-timeout` (default
`5m`). **Always pass `--wait`** so you observe the terminal state instead
of returning while the action is still queued. Always read state with
`-o json` for parseable output.

| Goal | Command |
| --- | --- |
| List VMs | `hostinger-cli vps vm list -o json` |
| Inspect one VM | `hostinger-cli vps vm get <vm-id> -o json` |
| Start | `hostinger-cli vps vm start <vm-id> --wait` |
| Stop | `hostinger-cli vps vm stop <vm-id> --wait` |
| Restart | `hostinger-cli vps vm restart <vm-id> --wait` |
| Recreate (reimage) | `hostinger-cli vps vm recreate <vm-id> --template-id <id> --wait` |
| List actions on VM | `hostinger-cli vps vm actions <vm-id> -o json` |
| Get one action | `hostinger-cli vps vm action-get <vm-id> <action-id> -o json` |
| Take snapshot | `hostinger-cli vps vm snapshot <vm-id> --wait` |
| Restore snapshot | `hostinger-cli vps vm snapshot-restore <vm-id> --wait` |
| List backups | `hostinger-cli vps vm backups <vm-id> -o json` |
| Restore backup | `hostinger-cli vps vm backup-restore <vm-id> <backup-id> --wait` |
| Set hostname | `hostinger-cli vps vm set-hostname <vm-id> --hostname host.example.com` |
| Set root password | `hostinger-cli vps vm set-root-password <vm-id>` (prompts) |

Other available verbs: `recovery-start`, `recovery-stop`,
`set-nameservers`, `set-panel-password`, `reset-hostname`, `purchase`,
`setup`, `ptr-create`, `ptr-delete`, `attached-keys`,
`monarx-install|metrics|uninstall`.

## Picking a VM by name/state

The user usually refers to a VM by hostname or IP, not ID. Resolve
first:

```sh
hostinger-cli vps vm list -o json --jq '.[] | select(.hostname=="web-01") | .id'
```

If no matches, list candidates and confirm with the user before acting.

## Patterns

- **Snapshot before destructive change.** Before `recreate`, `snapshot-restore`,
  or `set-root-password` on a production VM, take a fresh snapshot.
- **One VM at a time.** Async actions on the same VM are serialised by
  the API; don't fire concurrent `start`/`stop`/`restart` for the same
  `<vm-id>`.
- **Timeouts.** Long restores can exceed 5m. Pass
  `--wait-timeout 15m` for `recreate` / `backup-restore`.
- **Exit codes.** `--wait` returns non-zero if the action ends in a
  failed terminal state. Surface the error message verbatim to the user.
