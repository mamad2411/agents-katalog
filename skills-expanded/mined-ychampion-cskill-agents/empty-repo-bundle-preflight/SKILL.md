---
name: empty-repo-bundle-preflight
description: "Fail fast when the repository has no refs so downstream bundling never triggers empty Git bundles."
metadata:
  author: ychampion
---

# SKILL: Empty Repo Bundle Preflight
**Domain:** safety-worktrees  
**Trigger:** Apply before running `git bundle create` to ensure the repository actually has refs, avoiding the 128 exit code and providing a clearer error path.
**Source Pattern:** Distilled from reviewed repo-safety, packaging, and worktree-management patterns.

## Core Method
Run `git for-each-ref --count=1 refs/` from the repository root; if the output is empty, report that the repo has no commits, record an analytics metric with the `empty_repo` outcome, and abort with a helpful message instead of invoking `git bundle create`, which would exit 128 on an empty repo. Sweep stale temporary refs first so the check reflects the true repo state, and treat the empty case as a known failure reason with a dedicated fail reason identifier that consumers can react to.

## Key Rules
- Always clean up `refs/seed/stash` and `refs/seed/root` before testing for refs so old placeholders cannot make an empty repo appear populated.
- Capture the `empty_repo` outcome via analytics or logs so you can audit why bundling never ran.
- Return a structured error with a fail reason (`empty_repo`) so callers can distinguish it from git failures or oversized bundles.
- When the repo has refs, proceed to bundle creation without repeating the check unnecessarily.

## Example Application
When building a git bundle upload helper, call this skill before `_bundleWithFallback`; if it signals an empty repo, stop and surface “Repository has no commits yet” to the UI and telemetry instead of letting `git bundle create` crash.

## Anti-Patterns (What NOT to do)
- Do not rely on the git bundle exit code alone to detect emptiness; it produces a cryptic message and leaves temporary files behind.
- Do not skip the cleanup step—stale refs from prior runs can mask an empty repo and let you bundle garbage.
- Do not proceed to bundle creation when the guard reports no refs; the upload would stall and return a generic failure reason.
