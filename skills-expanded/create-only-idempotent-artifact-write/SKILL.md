---
name: create-only-idempotent-artifact-write
description: "Persist deterministic artifacts with a create-only write and treat existing files as replay success instead of an error."
metadata:
  author: ychampion
---

# SKILL: Create-Only Idempotent Artifact Write
**Domain:** tool-orchestration  
**Trigger:** Apply when a deterministic artifact is keyed by a stable invocation ID and may be replayed across retries, compaction, or resume passes.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
When an artifact path is derived from a stable identity, write it once with an atomic create-only operation instead of checking for existence first. If the write hits "already exists," treat that as proof the earlier successful write already materialized the deterministic content and continue with the normal readback or preview path. This removes the stat-then-write race, avoids useless rewrites during replay, and keeps repeated passes behaviorally identical.

## Key Rules
- Derive the artifact path from a stable key such as `tool_use_id` so repeated calls target the same location.
- Use a create-only write primitive like `flag: 'wx'` to collapse "create if absent" into one filesystem operation.
- Treat `EEXIST` as idempotent success when the content is deterministic for that key; only unexpected filesystem errors should fail the operation.
- Continue into the downstream preview or response-building path even when the file already existed, so replayed calls return the same contract as fresh ones.
- Avoid preflight existence checks because they reintroduce races and duplicate I/O under concurrency.

## Example Application
If a large tool result is persisted under `tool-results/<tool_use_id>.json`, write it once with a create-only flag. When transcript replay or micro-compaction revisits that same tool result, the write sees `EEXIST`, skips the rewrite, and still returns the same preview payload and saved path to the caller.

## Anti-Patterns (What NOT to do)
- Do not `stat()` and then `writeFile()` for idempotency; another writer can win between those calls.
- Do not overwrite existing artifacts on every replay when the file path is already the canonical output for that key.
- Do not treat "file already exists" as a hard error in deterministic replay flows; it is often the success path.
