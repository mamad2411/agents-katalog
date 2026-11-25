---
name: target-memory-bootstrap
description: "Create the target repository's local memory skeleton after repo init. Use from repo-init-scan during first substantial plugin use, when `memories/repo` is missing, or when MEDIUM/LARGE work needs persistent recovery state. Do not store active project memory in the plugin package."
---

# Target Memory Bootstrap

Create durable target-local memory routing files. Generated memory starts empty and project-neutral; later tasks fill it with verified target repository facts and progress.

Load `references/templates.md` for exact file contents.

## Boundary

- Write into the target repository, never into the installed plugin package or plugin cache.
- Create missing files only. Do not overwrite existing target memory.
- Do not copy this plugin repository's current work, decisions, examples, `memories/**`, or `spec/**` as active target memory.
- Memory stores recovery state, verified decisions, compact facts, last verification, and next resume action.
- Memory does not store long logs, secrets, PII, raw chat transcripts, or unverified guesses.

## Files To Create

- `memories/README.md`
- `memories/repo/INDEX.md`
- `memories/repo/current-workstreams.md`
- `memories/repo/project-state.md`
- `memories/repo/workflow-rules.md`
- `memories/repo/decisions.md`
- `memories/repo/logs/README.md`
- `memories/repo/archive/deprecated-decisions.md`

## State Recovery Requirements

`current-workstreams.md` must be able to resume work without chat history. It must include fields for:

- `topic`
- `status`
- `linked_spec`
- `linked_memory`
- `current_focus`
- `completed_tasks`
- `blocked_tasks`
- `next_resume_action`
- `last_verified`
- `last_state_sync`
- `owner_lane`
- `residual_risk`

`INDEX.md` must route by `load_tier`, `tags`, `use_for`, `linked_spec`, `last_updated`, and a one-line summary.

## Procedure

1. Determine the target repository root from the active init flow or PM packet.
2. Read existing memory files when present.
3. Create only absent files using `references/templates.md`.
4. If existing files are present but lack resumable workstream fields, append a compatible recovery section instead of replacing project-specific content.
5. Verify every required path exists.
6. Return created files, preserved files, repaired files, and missing paths.

## Verification

- Confirm all missing files were created in the target repository.
- Confirm existing target memory files were preserved.
- Confirm placeholders are neutral (`unknown` or `None yet`) and do not describe the plugin repository as the target project.
- Confirm `current-workstreams.md` has the state recovery fields above.
- If invoked because `memories/repo/**` was missing and required files still do not exist, return `BLOCKED target_memory_bootstrap_incomplete` with the missing paths. Do not let the caller continue the substantive task as if initialization succeeded.
