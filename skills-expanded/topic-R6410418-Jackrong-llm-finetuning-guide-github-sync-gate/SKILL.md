---
name: github-sync-gate
description: Enforce this repository's local-review-first GitHub sync policy. Use when Codex is preparing, validating, staging, committing, pushing, or opening a pull request for this repository and must wait for the exact approval phrase before any remote write.
---

# GitHub Sync Gate

Remote writes are forbidden until the user sends exactly:

```text
同步
```

Do not treat any other approval phrase as sync approval.

## Before Sync

After exact approval and before any remote write:

1. Re-run privacy scans.
2. Re-run repository-relative Markdown link validation.
3. Re-run syntax checks.
4. Re-run `git diff --check`.
5. Inspect staged files for tokens, private paths, private SSH aliases, logs, caches, datasets, model weights, GGUF files, safetensors files, and checkpoints.
6. Fetch the latest remote state and handle divergence safely.

## Push Policy

- Never force-push.
- Prefer a direct push to `main` only when the local integration can be applied safely and the remote branch has not diverged.
- If direct push is unsafe or blocked, push the feature branch and open a pull request.
- Report the pushed branch, commit hash, and remote result.
- Never publish Hugging Face models merely because GitHub sync was approved.
