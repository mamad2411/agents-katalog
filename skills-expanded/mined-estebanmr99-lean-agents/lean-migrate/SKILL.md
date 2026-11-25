---
name: lean-migrate
description: Guide an OpenCode 1.x to 2.x upgrade through the lean-agents engine: permanent session backup, dry run, apply, check, then port the manual items by hand, and undo if anything fails. Use when the user wants to move OpenCode 1.x to 2.x without losing config or sessions. Opt-in.
---

# lean-migrate

You guide the upgrade; the engine changes files. Never edit an OpenCode 1.x file yourself, never run the OpenCode installer or `opencode upgrade` directly, never touch `~/.local/share/opencode` (sessions). Never print secret values. Ask the user before each numbered step that changes something. Full background: `docs/migrate-opencode-v1-to-v2.md` in the lean-agents repository.

1. Close every OpenCode window and its background service; the engine refuses to run while one is open. Hand-built machine (no `~/.config/lean-agents/state.json`)? Run `npx lean-agents --adopt --json` first; it is read-only. Show what it found.
2. Backup plan: `npx lean-agents --upgrade-agent opencode --backup`. It writes nothing and prints the size, the session count and whether free space is enough (2 x size + 1 GB). Ask the user, then run it with `--yes`. This is a permanent, sha256-checked copy of the 1.x sessions and config plus a frozen copy that `opencode1` uses. Tell the user where the backup is; lean-agents never deletes it. Stop if it fails.
3. Dry run: `npx lean-agents --upgrade-agent opencode --dry-run --json`. Writes nothing. Read `upgrade.counts`, `upgrade.plan`, `upgrade.layout.sessions` and each item's `upgrade` block.
4. Show three short lists:
   - **managed**: lean-agents reinstalls these for 2.x.
   - **translatable**: `before -> after` plus its `source`.
   - **manual** (`user-manual`): item and `reason`. Rows marked VERIFY are unproven; say so.
5. Ask whether to go on. Stop on "no". Apply: `npx lean-agents --upgrade-agent opencode --yes`. It checks the backup, adds `opencode1` (OpenCode 1.x on the frozen copy only), installs OpenCode 2, translates the config and adds DCP. A failed step undoes the finished ones by itself; if it prints `RESTORE.md`, show the user that path and stop.
6. Check: `npx lean-agents --doctor`. `opencode --version` must show 2.x, and `opencode1 --version` must show 1.x. The 2.x session count must equal `upgrade.layout.sessions` from step 3 (the 1.x sessions stay readable with `opencode1`). If a plugin looks suspect, add `--probe-plugins` to the doctor run.
7. Port each manual item into the 2.x files only (`~/.config/opencode/opencode.jsonc`, `cli.json`, the 2.x folders), one at a time, asking before each. Use the mapping table in `docs/compatibility.md` ("OpenCode 1.x to 2.x: where things live"). Keep the 1.x originals as they are. Run `npx lean-agents --doctor` after the last one.
8. If the doctor fails or sessions changed: `npx lean-agents --upgrade-agent opencode --undo` shows the plan; after the user agrees, run it with `--yes`, then report the exact error. Undo returns to 1.x and keeps the backup and the frozen copy.

Report what you verified (command and result) and what is left for the user.
