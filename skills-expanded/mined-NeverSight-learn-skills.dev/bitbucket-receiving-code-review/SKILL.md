---
name: bitbucket-receiving-code-review
description: Monitor an open Bitbucket pull request for reviewer feedback, respond to comments, apply fixes, resolve threads via API, and drive the PR to a ready state. Use after creating a Bitbucket PR or when the user asks to check review status, "check my PR", or respond to feedback on a Bitbucket-hosted PR.
---

Author-side companion to `bitbucket-code-review`. If the repo defines its own bot ready-gate (e.g. betico via `bot: ready` / `bot: not ready`), this skill respects it.

## When to run

- Triggered automatically by `creating-bitbucket-prs` on an hourly cadence during working hours on weekdays.
- On demand when the user asks to "check my PR", "see review comments", or "respond to feedback".

## Step 1 — Pull review state

Identify the PR (from the current branch or a URL). Then fetch:

```bash
REMOTE_URL=$(git remote get-url origin)
REPO_PATH=$(echo "$REMOTE_URL" | sed -E 's#.*/([^/]+/[^/]+?)(\.git)?$#\1#')

# Pipeline status
PIPELINE_UUID=$(bkt pipeline list --json \
  --jq '[.[] | select(.target.ref_name == "'"$(git branch --show-current)"'")][0].uuid')
bkt pipeline view "$PIPELINE_UUID" --json --jq '.state.name, .state.result.name'

# Unresolved review comments
bkt api "/repositories/${REPO_PATH}/pullrequests/${PR_ID}/comments" \
  --method GET --paginate \
  | jq '[.values[] | select(.deleted == false and .resolution == null)]'
```

Bucket results into: **new feedback**, **pending author response**, **blocking (needs code change)**, **informational**.

**Stale-resolution gotcha:** the list endpoint sometimes shows child comments with `resolution: null` even when the thread root has `resolution: comment_resolution`. Treat resolution at the **thread-root** level, not per-comment.

## Step 2 — Respond

For each unresolved thread:

- **Valid feedback** — apply the change, push, then respond on the Bitbucket thread summarizing what changed and link to the commit. Mark the thread resolved via the API once pushed.
- **Disagreement** — reply with evidence (link to docs, benchmarks, prior decisions). Don't get defensive. If the thread grows past three back-and-forths, schedule a sync and post the outcome as a top-level comment.
- **Question about intent** — the reviewer asking *why* usually means the code needs a comment. Add it, push, then respond.
- **Offline discussion happened** — post the outcome on Bitbucket anyway. Visibility for the next reader.
- **Stalemate** — escalate to a Tech Lead.

Always respond on Bitbucket even when the conversation moved to chat or a call.

## Step 3 — Resolve via API

Every time a thread reaches a conclusion — a fix landed, the disagreement closed, the reviewer confirmed the answer — mark it resolved through the API. Same action as clicking the Resolve button, but programmatic so automation has an audit trail and nothing silently drifts to "resolved by click".

```bash
bkt api "/repositories/${REPO_PATH}/pullrequests/${PR_ID}/comments/<COMMENT_ID>/resolve" \
  --method POST
```

**Only inline comments are API-resolvable.** Top-level comments (`inline.path == null`) cannot be resolved through the resolve endpoint — they live until the PR closes.

Never resolve from the UI. The API call is the source of truth.

## Step 4 — Ready gate

If the repo uses a bot ready-gate (betico-style), post the top-level `bot: ready` comment ONLY when ALL of these are true:

- Every dependency PR listed in the PR description's Dependencies field has merged. Unmerged dep → `bot: not ready`, no exceptions.
- Every review thread is resolved via the API (Step 3). No UI-only resolves.
- The latest pipeline state is `COMPLETED` with `SUCCESSFUL` result.
- Your own self-review pass found nothing new.

```bash
bkt api "/repositories/${REPO_PATH}/pullrequests/${PR_ID}/comments" \
  --method POST \
  --input '{"content": {"raw": "bot: ready"}}'
```

If something regresses (pipeline fails, new comment lands, bug found) while the PR is already in ready state, post:

```bash
bkt api "/repositories/${REPO_PATH}/pullrequests/${PR_ID}/comments" \
  --method POST \
  --input '{"content": {"raw": "bot: not ready"}}'
```

**Race-condition guard:** before posting `bot: ready`, re-read the source commit hash. If it changed since your checks, restart from Step 1 — a new push invalidates the green pipeline you just observed.

If the bot owns the PR title, never edit the title manually.

## Cadence

When launched by `creating-bitbucket-prs`, this skill runs every hour between 09:00 and 18:00 local time, Monday–Friday. Outside that window, it sleeps until the next work-hour slot. Stop the cadence once the PR is merged or closed.

## Report

Each run, summarize for the user:

- Pipeline state.
- Count of unresolved threads (by bucket).
- Actions taken this run.
- Next action + ETA (or "nothing to do, sleeping until HH:MM").
