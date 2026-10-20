---
name: reconcile-marketplace
description: >
  Import CLI-installed plugins (Claude/Grok) into the RUSHYOP rushy marketplace
  catalog. Use when the user installed a plugin from xAI/Grok/Claude without
  add-plugin, asks to auto-add into rushy, mentions marketplace drift, or runs
  /reconcile-marketplace.
---

# Reconcile marketplace skill

## Rule

CLI install ≠ catalog update. Always land plugins in the **rushy** git marketplace, then enable `@rushy`.

## Run

```bash
ROOT="${RUSHY_MARKETPLACE_ROOT:-/Users/admin/Codes-2/Agentic-setup}"
cd "$ROOT"

# Status
./hooks/check-cli-drift.sh

# Apply into catalog
./hooks/reconcile.sh --sync --only-new --commit --push
```

## Prefer primary path when source is known

```bash
./scripts/add-plugin.sh <name> <owner/repo|git-url> [--path subdir] --sync --commit --push
```

## After reconcile

- Confirm dry-run reports `ADDED:0`
- Enable plugin as `name@rushy` (Claude) or install from rushy marketplace (Grok)
- Do not leave third-party marketplaces as long-term sources

## Hooks (already in this plugin / optional global install)

- **SessionStart** — dry-run drift check only
- **PostToolUse** (shell) — hint after `plugin install`-like commands
- Global install: `./hooks/install-user-hooks.sh`
