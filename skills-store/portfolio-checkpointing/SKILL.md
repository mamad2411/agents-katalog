---
name: portfolio-checkpointing
description: "Preserve a recoverable baseline before major rewrites without staging unrelated work."
---

# portfolio-checkpointing

Record HEAD, status, and affected paths before a major rewrite. Preserve existing edits and index state. For a dirty tree, save a binary diff and copies/archive of affected untracked files to a task-owned ignored or temporary directory. Report that location.

A targeted commit is appropriate only when its paths are owned and reviewed; do not blanket-stage, auto-stash, reset, or publish. A worktree from HEAD does not contain uncommitted work: transfer only needed reviewed edits explicitly. Small reversible edits do not require ceremonial checkpoint commits. Respect filesystem/Git permissions.
