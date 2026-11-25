---
name: workspace
description: Attach a host-provided CodeRail runtime to one product repository, resolve isolated governance paths, preview migration or detachment, and export explicit product files.
---

# Workspace access

The plugin provides the runtime and skills. Resolve this skill's directory to
the installed plugin root, then run `python <plugin-root>/scripts/coderail.py`
with `--target <product-repository>`. Never substitute consumer scripts for the
plugin runtime. A project-local launcher is only an exact-version convenience.

Use `workspace paths` to resolve the active layout before reading governance
files. Legacy logical `docs/TASKS.md` maps to `.coderail/workspace/TASKS.md`
only when `.coderail/config.json` explicitly selects `workspace-v1`; a missing
selected file is an error, not permission to read a legacy copy.

## Access and archives

- `workspace attach` previews a fresh project connection; `--apply` creates it.
- `workspace migrate --confirm-process-file docs/TASKS.md ...` previews an
  explicit legacy migration. Confirm each process-only source individually;
  include NORTH_STAR and TRACELOG. Preserve mixed product documents unless the
  owner confirms their entire file is process-only. Add `--apply` after reviewing.
- `workspace detach` previews detachment; `--apply` disables governed commands,
  removes only proven unchanged tool integration, and retains archives/recovery.
- `workspace recover` previews rollback of an interrupted access transition;
  `--apply` restores exact before-bytes unless user edits conflict.

Use normal `start`, `check`, `done`, `drive`, `switch`, `progress-view`, and
`knowledge query` after attachment. Their product cwd is always the repository
root. Supply all acceptance statuses before the first done call. A valid receipt
only avoids repeated CI inside that same transaction.

`product-export --file product.py --file docs/api.md` previews a positive
product file manifest; `--output <new-isolated-directory>` writes it. Verify the
actual exported product's own build/test entry points. Archives never belong to
the product package, but committed archive history remains visible in full Git.
Detachment is an access change and must never be described as product delivery.
