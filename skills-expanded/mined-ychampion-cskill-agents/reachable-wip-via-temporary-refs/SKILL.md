---
name: reachable-wip-via-temporary-refs
description: "Capture in-flight WIP via `git stash create`, make it reachable through temporary refs, and tear down the refs after bundling finishes."
metadata:
  author: ychampion
---

# SKILL: Reachable WIP Via Temporary Refs
**Domain:** safety-worktrees  
**Trigger:** Apply when bundling or seeding a repository and you want to include uncommitted work without disturbing the working tree or leaving dangling refs.
**Source Pattern:** Distilled from reviewed repo-safety, packaging, and worktree-management patterns.

## Core Method
Call `git stash create` to materialize the working tree and index into a temporary commit while leaving the workspace untouched. If the command returns a SHA then advertise it via a short-lived ref such as `refs/seed/stash` so downstream tooling (bundle list-heads, receivers) can reach those objects; treat an empty response as “no WIP,” log both success and error cases, and clean up the temporary ref after the upload completes or earlier runs leave stale pointers.

## Key Rules
- Always run the ref cleanup loop (`refs/seed/stash`, `refs/seed/root`) before bundling so previous runs do not influence new bundles or leak stale WIP markers.
- Accept that `git stash create` can fail non-fatally; log the stderr, skip ref creation, but continue bundling the committed tree.
- Only call `git update-ref refs/seed/stash <sha>` when the stash SHA is non-empty; otherwise the ref would dereference to nothing.
- Record a boolean flag (`hasWip`) when the temporary stash exists so telemetry and later steps can know whether to expect extra objects.
- After the bundle (and after the `finally` block), delete the temporary refs even if the upstream run failed to keep the user repo clean.

## Example Application
When writing an upload helper for a CLI that seeds a remote CCR process, use this skill to wrap the `git stash create`/`git update-ref` pair, expose `hasWip`, and ensure the `finally` block always runs `git update-ref -d refs/seed/stash` before returning.

## Anti-Patterns (What NOT to do)
- Do not rely on the regular stash stack (refs/stash) because `git bundle` should not touch the user-visible stack; `git stash create` avoids a working-tree mutation.
- Do not advertise an empty SHA: bundlers that list heads will fail to find objects.
- Do not skip cleanup: leaving `refs/seed/stash` behind pollutes the repo and may cause future bundling runs to include WIP twice.
