<!-- engram:harness-adapter:v1 -->
---
name: engram-end-session
description: Use when Cursor Agent is closing out work, preparing a handoff, or recording durable Memory OS changes.
---
# Engram End Session

Use this skill when Cursor Agent is closing out a task or preparing a handoff.

Before ending:
- Call `memory(action=changes_since, commit_id=<memory_cursor.commit_id>,
  timestamp=<memory_cursor.timestamp>, scope={relevance_mode:"related", project:..., cwd:...})` from the latest cursor.
- Call `obligations(action=detect, project=..., cwd=...)` and
  `obligations(action=doctor, scope={relevance_mode:"related", project:..., cwd:...})`.
- Resolve open obligations or state explicit skip reasons in the handoff.
- Update or compile `handoff` with completed work, open decisions, next actions, and risks.
- If durable memory changed, prepare a `memory(action=commit)` candidate.
- Use this same flow before context compaction or any context transition.
- Use writer provenance with `writer_harness=cursor`.
- Leave migration and digest promotions review-gated; do not auto-promote orphan data.
