---
name: staged-bundle-fallback-chain
description: "Retry Git bundle creation across decreasing scopes (all, HEAD, squashed) to stay under upload size limits while keeping relevant history."
metadata:
  author: ychampion
---

# SKILL: Staged Bundle Fallback Chain
**Domain:** safety-worktrees  
**Trigger:** Apply when you are creating a Git bundle for upload and you need a staged fallback chain from full history to a minimal seed that still fits the byte ceiling.
**Source Pattern:** Distilled from reviewed repo-safety, packaging, and worktree-management patterns.

## Core Method
Attempt to bundle the full repo first (`git bundle create --all`), then inspect the resulting file size; if the artifact exceeds the configured limit, rerun the bundling command with a narrower base (`HEAD`). If HEAD still produces an oversized bundle, collapse to a squashed root commit (built from the stash tree when WIP exists) so you ship only the working tree snapshot without history. At every step log the rationale, and return the scope label (`all`, `head`, `squashed`) that succeeded so downstream uploaders know how much history is included.

## Key Rules
- Always check the generated bundle size immediately after each `git bundle create` call and only stop when the artifact fits within the configured max bytes.
- When rerunning, overwrite the same bundle file so callers do not need to swap paths, and log a debug message summarizing the last size versus limit.
- For the squashed fallback, create a parentless commit from the stash tree (if WIP was captured) or `HEAD^{tree}` and bundle that single root, then update `refs/seed/root` so downstream consumers can find it.
- Surface the chosen scope (`all`, `head`, or `squashed`) in the upload metadata so receivers know whether history was preserved.
- Respect abort signals throughout the fallback chain so the bundling command can stop cleanly when the parent process is cancelled.

## Example Application
If building an "export repository" CLI that feeds upstream tooling, call this skill to drive the bundling logic: start with the feature-flagged `maxBytes`, attempt `--all`, check the file size, retry with HEAD, and finally fall back to squashed-root while reporting the scope and bytes to the telemetry system.

## Anti-Patterns (What NOT to do)
- Do not assume the first `git bundle create` succeeds; skipping the size check leads to uploads that exceed quotas and fail at the network layer.
- Do not rerun all bundling scopes on separate files; leaving stale bundles confuses cleanup and telemetry.
- Do not forget to include the final scope in the response metadata, because receivers won’t know if they need to fetch history-aware refs.
