---
name: now
description: "Rebuild per-project now/ status snapshots from recent diary entries. Run after a backfill, or any time the injected project state looks stale."
---

# Now — Rebuild Project Status Snapshots

Regenerates the per-project `now/<project>.md` files that the SessionStart hook
injects so a new session knows where each project left off. Each file is a short
3-5 bullet status synthesized from recent diary entries, grouped by project via
the shared project-identity resolver (`.multiplai/project-map.yaml`).

The live pipeline keeps these fresh automatically (each session refreshes its
own project after writing its diary). Use this skill for a **full rebuild** —
e.g. after a `/multiplai-context:backfill`, after editing `project-map.yaml`, or to
recover from stale/incorrect snapshots.

## Usage

- **Full rebuild (all projects):**
  ```
  uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/synthesize_now.py"
  ```
- **Single project:**
  ```
  uv run --project "${CLAUDE_PLUGIN_ROOT}/scripts" "${CLAUDE_PLUGIN_ROOT}/scripts/synthesize_now.py" --project <name>
  ```

## Steps

1. Run the script (full rebuild unless the user named a specific project).
2. Report which `now/<project>.md` files were written. If the output directory
   was empty afterward, tell the user no diary entries fell inside the lookback
   window (48h) — there was nothing recent to summarize.

## Notes

- Project names come from `.multiplai/project-map.yaml`. If snapshots are landing
  under unexpected names (e.g. a subdirectory or `workspace`), the fix is in that
  config, not here — point the user at `/multiplai-context:setup` to revise it.
- Summarization uses the configured model client; with no client it falls back to
  an extractive (truncated-snippet) summary. Both paths write the same file shape.
