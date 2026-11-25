---
name: nodus-troubleshooting
description: Use when nodus add, sync, doctor, update, or relay is failing and you need a structured debugging workflow based on workspace state, lock state, package discovery, and managed outputs.
---

# Nodus Troubleshooting

Debug Nodus failures from first principles: workspace state, dependency resolution, lock state, discovery results, managed outputs, and relay state.

## Workflow

1. Identify the failing stage.
   - Parse or validation error
   - Dependency resolution error
   - Sync collision or managed file drift
   - Relay state or local checkout mismatch
2. Inspect the package or workspace state.
   - Read `nodus.toml` and `nodus.lock`.
   - Run `nodus info <alias-or-path>` for the failing package.
   - Run `nodus doctor` for workspace verification.
3. Check for the common root causes.
   - invalid dependency source or ref
   - unsupported or duplicate component selection
   - invalid `managed` mappings
   - duplicate artifact ids across discovery roots
   - pending relay edits blocking sync
   - lockfile drift when using `--locked` or `--frozen`
4. Repair with the smallest correct action.
   - rerun `nodus sync`
   - rerun `nodus update`
   - inspect with `nodus info <alias-or-path>`
   - refresh the manifest entry
   - fix the package layout
   - remove or adopt conflicting managed paths only when the ownership is clear
   - only if normal recovery fails, consider a last-resort reset: delete `nodus.lock`, clear Nodus-managed outputs, then reinstall or resync
5. Verify again with `nodus doctor`.

## Debug Commands

```bash
nodus info .
nodus info <alias>
nodus doctor
nodus sync
nodus sync --locked
nodus sync --frozen
nodus outdated
nodus update
```

## Decision Rules

- If `nodus doctor` reports drift, prefer regenerating state with `nodus sync` before deeper changes.
- If `sync` is blocked by pending relay edits, do not overwrite them; inspect the linked checkout and relay state first.
- If discovery looks wrong, inspect `content_roots`, artifact ids, and package-relative paths before touching adapter outputs.
- Treat deleting `nodus.lock` and managed adapter outputs as a final reset path, not a normal repair step.
- In that reset flow, only remove Nodus-managed files. Do not delete the user's handwritten source code.
