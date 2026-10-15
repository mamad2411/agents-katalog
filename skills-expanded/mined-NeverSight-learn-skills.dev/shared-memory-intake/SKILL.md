---
name: shared-memory-intake
description: Curate shared Codex memory when Claude submits findings or Codex reviews, promotes, or maintains task memory.
---

# Shared Memory Intake

Use `~/.codex/memories/` as the canonical shared knowledge store and
`~/.agents/shared-memory-inbox/` as the external submission store. Read
`MEMORY.md` before opening matching `rollout_summaries/` files. Treat dynamic claims
as `UNCONFIRMED` until verified in the active session.

## Actor contract

Require an explicit actor: `--as claude` or `--as codex`. Never infer it from the
runtime.

| Actor | Allowed operations | Forbidden operations |
|---|---|---|
| `claude` | read official memory; create one submission in `inbox/pending/` | edit or delete official memory, or another submission |
| `codex` | read, review, promote, supersede, maintain | delete historical summaries or silently overwrite a current claim |

## Claude: submit

1. Read `MEMORY.md`; do not restate an existing current claim as a new submission.
2. Create one uniquely named Markdown file under `~/.agents/shared-memory-inbox/pending/` with YAML frontmatter:

   ```yaml
   schema_version: 1
   source_runtime: claude
   submitted_at: 2026-07-26T00:00:00Z
   cwd: /absolute/path
   source_session: opaque-session-id
   claim_status: unverified
   ```

3. Keep only reusable conclusions, source references, evidence, and unknowns. Never
   include credentials, tokens, private keys, cookies, or raw transcripts.
4. Validate before handoff:

   ```sh
   python3 ~/.agents/skills/shared-memory-intake/scripts/validate_submission.py /absolute/path/to/submission.md
   ```

5. A correction is a new submission with `supersedes_submission`; never overwrite the
   earlier proposal.

## Codex: review and promote

1. Acquire the single-curator lease before promotion: `mkdir ~/.agents/shared-memory-inbox/.curator.lock`.
   If it already exists, stop and report the active-curator conflict. Release it with
   `rmdir` after the outcome is recorded.
2. Run the validator on the candidate. Reject on schema or secret-pattern failure.
3. Inspect the cited source and live-verify every dynamic claim that would enter the
   current index.
4. Re-read `MEMORY.md` immediately before its update. If its relevant topic changed
   during review, restart the review instead of merging assumptions.
5. Promote accepted knowledge to a new immutable `rollout_summaries/*.md` record and
   update `MEMORY.md` as the only current index. Give every changed reusable claim a
   lifecycle state: `active`, `superseded`, or `UNCONFIRMED`.
6. Move the candidate to `processed/` or `rejected/` without deleting its audit trail.

## Codex: maintain

1. Acquire the same single-curator lease and re-read `MEMORY.md` immediately before
   every official-memory write; stop on an active-curator conflict.
2. Scan current index entries for changed paths, versions, models, deployments, or
   stale references.
3. Demote unverified dynamic claims to `UNCONFIRMED`; mark replaced claims
   `superseded` with their replacement reference.
4. Consolidate duplicate current entries. Do not rewrite historical rollout summaries.
5. Re-run the validator on any newly promoted submission and report the paths changed.

## Validator

Use `scripts/validate_submission.py`. It is a narrow preflight gate, not proof that a
claim is true and not a complete secret scanner. A pass authorizes review only; Codex
still owns evidence verification and promotion.
