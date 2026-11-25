---
name: trailkeep-open-items
description: Use when extracting what is still open per project (pending work, owner decisions to unblock, things to test, durable decisions) from trailkeep's Markdown conversation backups into _open_items.json, or when rendering that sidecar into a repo's STATUS.md.
---

# Trailkeep Open Items

Turns months of AI-coding conversations into a short list per project of what
is still open, cross-checked against later conversations and the repo, so the
owner never has to read transcripts. It replaces the review layer in
`skills/trailkeep-project-review/` for this purpose: no gates, no eval suites,
no preprocessed-input dump.

Model calls go through the user's coding agent; trailkeep's scripts and viewer
stay local and zero-network. Only the redacted digest parts and read-only repo
facts reach the model.

## Pipeline

1. **Digest** (deterministic, $0):
   `python3 converters/extract_digest.py BACKUP_DIR [--project NAME ...]`
   Writes `BACKUP_DIR/_open_items_inputs/<project>/part-NNN.md` and
   `_manifest.json` (parts, batches, conversation ids, repo path). Every
   exchange is kept (owner message + last agent text reply); tool calls are
   dropped; Codex subagents and repeated-title automated runs are skipped;
   secrets are redacted.
2. **Budget check.** Sum `estimated_tokens` of the selected projects from the
   manifest and check the user's plan usage before starting. Pilot on 2-3
   projects and show the result before a full run.
3. **Extract** with one subagent per batch (model: Sonnet). Batches of a
   project run in order, because each one reads the previous state; different
   projects can run in parallel. For batch `i` of `n`, fill
   `batch-prompt.md`:
   - `{project}`: manifest key.
   - `{parts}`: absolute paths of the batch's parts.
   - `{state_path}`: `<project dir>/state-<i-1>.json` (none for `i = 1`).
   - `{out_path}`: `<project dir>/state-<i>.json`.
   - `{final_step}`: for `i < n`, "This is not the final batch: skip the
     repo check." For `i = n`, the repo check below.
4. **Merge**: `python3 skills/trailkeep-open-items/scripts/merge_open_items.py
   BACKUP_DIR PROJECT <project dir>/state-<n>.json --model <model>`. On
   failure, send the printed problems back to the same subagent and rerun.
   Writes `BACKUP_DIR/_open_items.json` (other projects kept).
5. **STATUS.md**: `python3 skills/trailkeep-open-items/scripts/write_status.py
   BACKUP_DIR --project NAME` prints the merged `STATUS.md`. Show it to the
   owner; add `--write` only after the owner approves that repo. Never commit
   or push from this step; the repo's own rules decide that.

## Repo check (final batch only)

Fill `{final_step}` with:

> Final batch: cross-check against the repo at `<repo_path>` (read-only; never
> fetch, pull, checkout, or edit). Run `git -C <repo_path> log
> --since=<first_date> --date=short --format='%ad %h %s'` and read whichever
> exist of `STATUS.md`, `BACKLOG.md`, `BACKLOG-HECHO.md`, `TODO.md`,
> `ROADMAP.md`, `docs/backlog*.md`, `docs/agent-handoff.md`. Move items shown
> done there to `resolved`. For pending items tracked in the backlog, add
> `backlog_ref` (file and id or heading). Then consolidate: merge related
> items, drop items superseded by later work in the same area or older than the
> repo's newer state, and order each list most important first. Then write `next_session`.

If the repo path is unknown or missing, skip the check and say so in
`next_session`.

## Output contract (`_open_items.json`)

```json
{"version": 1, "projects": {"<name>": {
  "generated_at": "...", "model": "...", "repo_path": "...",
  "coverage": {"conversations": 0, "first_date": "", "last_date": ""},
  "pending":   [{"text": "", "evidence": [{"id": "", "date": ""}], "backlog_ref": ""}],
  "unblock":   [{"text": "", "options": ["", ""], "recommendation": "", "evidence": []}],
  "test":      [{"text": "", "how": "", "evidence": []}],
  "decisions": [{"text": "", "evidence": []}],
  "resolved":  [{"text": "", "how": "", "evidence": []}],
  "next_session": ""}}}
```

`backlog_ref` and `how` are optional. Evidence ids must exist in the project's
digest; the merge script enforces it.
