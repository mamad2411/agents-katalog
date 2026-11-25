---
name: octopus
description: Use the Octopus CLI to check the user's Octopus connection or review a chosen staged diff, working change set, or connected pull request when the user asks for Octopus.
---

# Octopus review

Run commands in the user's intended Git checkout, using the environment where
your terminal tool actually executes. A host login or binary may not exist in a
remote workspace or container.

1. Run `octp --version` and `octp whoami`. Confirm the intended organization.
   If the CLI is missing or authentication fails, stop and direct the user to
   https://octopus-review.ai/docs/cli/ai-agents. The user runs `octp login`.
   Never ask for a token in chat, read credential files, or put tokens in this skill.
2. Establish the requested scope with `git status --short`. Review only the
   changes or PR the user selected. If the scope is unclear, ask before sending code.
3. Choose the matching command:
   - Staged changes: `octp review --staged --no-index --format json`.
   - Working/branch changes: `octp review --no-index --format json`.
     This can include committed changes since the upstream branch plus unstaged
     tracked changes; it does not reliably include staged-only changes. Inspect
     the intended diff first. Untracked files are not automatically reviewed.
   - A connected PR: `octp review --pr 42` (replace 42 with the requested number),
     or pass a full GitHub, GitLab, or Bitbucket PR URL after `--pr`.
     Forgejo full PR URLs are not accepted by native CLI 0.6.0; use the PR number
     from the connected repository checkout.
4. Explain the result accurately. Local review JSON contains findings and
   coverage information. If `truncated` is true, report that coverage is incomplete.
   A successful PR request means queued, not finished: check Octopus Review Logs
   and the PR for the final result. Never claim success after an error.
5. Present findings before changing files. Apply fixes, commit, push, or post
   comments only when the user's request authorizes those actions. Follow the
   repository's validation instructions and preserve unrelated changes.

Reviews send code/diffs and review metadata to the configured Octopus server
and AI services and use the organization's credits or provider budget.
`--no-index` prevents a new repository upload/indexing run; it does not make the
review offline and may still use existing indexed context. Do not add `--index`
or upload more repository content without the user's authorization.

Use `octp --help` to inspect the installed command set. Do not substitute
`octopus`, `npx @octp/cli`, `octp ask`, or invented `--claude`/`--codex` flags.
