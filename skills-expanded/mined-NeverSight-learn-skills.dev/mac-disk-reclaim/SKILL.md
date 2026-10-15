---
name: mac-disk-reclaim
description: Discover and reclaim wasted SSD space on macOS, then delete it interactively with the consequences spelled out. Finds bloat by what it is, wherever it lives — build/dep dirs (node_modules, target, .venv, DerivedData) scattered across every project, package/tool caches, Electron app caches buried under Application Support, AI agent history (Claude/Codex logs), bloated .git objects, merged git worktrees, .DS_Store swarms, per-volume trash, Time Machine local snapshots. Walks findings largest-first and, only after the user confirms each one, deletes it directly (NOT to Trash) — telling the user up front what regenerates vs what is gone forever. Remembers each delete/skip choice so reruns only ask about newly-found items. Use when the user is low on disk/SSD space, wants to free space, clean a Mac, purge caches, or remove build/dependency bloat.
---

# Mac Disk Reclaim

Two phases: **discover** (read-only) then **interactive delete** (confirm each, direct delete).

macOS only. The scanner never surfaces user data — Documents, Photos, Mail, Keychains,
Containers app data, iCloud, the system volume are off-limits. It deletes nothing itself.

## Phase 1 — Discover

```bash
python3 scripts/scan_reclaimable.py --json          # --min-mb N raises the floor (default 200)
```

It does not rely on a fixed path list. It finds bloat by category, including the
**distributed** kind a "largest folders" scan misses (each item moderate, sum huge):

- `build` — node_modules / target / build / dist / .next / .venv / __pycache__ across every project
- `cache` — tool + Electron app caches (Cache / Code Cache / GPUCache under Application Support)
- `browser-cache` — Chrome/Brave/Vivaldi/Firefox caches
- `agent` — Claude/Codex conversation history & log DBs (**permanent — review**)
- `ai-models` — ollama / Hugging Face weights (re-downloadable, large)
- `git-gc` — bloated `.git` objects → `git gc` (repacks, loses nothing)
- `worktree` — git worktrees whose branch is already **merged** → `git worktree remove`
- `dsstore` — thousands of `.DS_Store` files
- `trash` — `~/.Trash` and per-volume `.Trashes`

Each finding carries `size`, `risk` (low/med), and a one-line **consequence** (`desc`):
what regenerates vs what is lost for good. Also returns a `snapshot_note` for Time
Machine local snapshots. Tell the user the total and the top items first.

## Phase 2 — Interactive delete (largest first)

Each finding carries `key` and `remembered` (`delete` / `skip` / `null`). Choices
persist in `~/.config/mac-disk-reclaim/decisions.json` (never swept by this skill),
so **a later run only asks about new items.**

First, split findings by `remembered` (and `reconfirm`):

- `remembered: "delete"` **and `reconfirm: false`** — previously approved, safely
  regenerates. Reclaim each (step 4) without re-asking; state count + total up front
  so the user can abort.
- `remembered: "delete"` **and `reconfirm: true`** — approved before but lossy
  (med-risk, or a `--volumes` prune). **Always re-ask** anyway; memory never
  auto-runs an irreversible command.
- `remembered: "skip"` — previously declined. Do not touch, do not ask. Mention the
  count only.
- `remembered: null` — **new.** Ask interactively (below).

For **each new** item, in size order:

1. Show: `size · category · path`, the `desc` consequence, and the `risk`. For
   `risk: med` (agent history, AI models) state plainly it does not come back.
2. Ask: delete / skip / stop. Wait. Never batch.
3. Persist the choice so the next run skips it:
   ```bash
   python3 scripts/decisions.py set "<key>" delete --path "<path>" --category "<category>"
   python3 scripts/decisions.py set "<key>" skip   --path "<path>" --category "<category>"
   ```
4. On `delete`, reclaim it:
   - `method: cmd` → run the item's `cmd` (the tool's own cleanup, e.g.
     `git gc`, `git worktree remove`, `brew cleanup --prune=all`,
     `docker system prune -af --volumes`, `find ~ -name .DS_Store -delete`).
   - `method: rm` → delete through the guard (refuses danger paths):
     ```bash
     python3 scripts/safe_delete.py "<path>" --yes
     ```
   Deletion is **direct and permanent — not Trash.** Confirm the user knows this once, up front.
5. Report freed space, continue.

Finish by offering the `snapshot_note` command (`sudo tmutil thinlocalsnapshots …`).

Memory controls: `--no-memory` on the scan reviews everything fresh; `decisions.py
list` shows saved choices; `decisions.py forget <key>` / `--all` clears them.

## Swap

Swap **cannot** be flushed on a running Mac. `/private/var/vm` swapfiles are
kernel-managed (encrypted on Apple Silicon); deleting them risks a panic. `sudo purge`
frees inactive RAM, not swap. Only a reboot clears swap. Report this; never offer to touch it.

## Notes

- The scan uses only `du`/`find` (always present). For faster discovery the user can
  `brew install dust`; for a turnkey cleaner, `mac-cleanup-py` — but neither does this
  skill's per-item-confirmed direct delete.
- Never delete anything the scanner did not surface; never hand a typed path to `safe_delete.py`.
- If `safe_delete.py` blocks a path, do not work around it.
