---
name: checkpoint
description: Let a coding-agent host join a branch-scoped Code Relay subscription and verify incoming runbooks.
---

# Code Relay checkpoint

The checkpoint is bound to one canonical repository URL and one remote ref. Verification always runs in an isolated worktree at the runbook's `source_commit` through the repository's GitHub Actions self-hosted runner.

When the user pastes a Code Relay join link, preview repository, ref, runbook path, artifact policy, and permissions. Ask for confirmation before joining. If the current workspace is empty, offer to clone the invited repository and ref into a confirmed directory.

The `code-relay-checkpoint` runner receives runbook workflows from GitHub Actions. `code-relay-agent run-pending` deduplicates by `repository + ref + runbook_id + source_commit`, creates an isolated worktree, and publishes the receipt. The bounded runner must not push code or alter the active worktree. Failures and blocked commands always produce a receipt.

Use `$code-relay:checkpoint status` for an explicit checkpoint status request.
