# PR Reviewer Workflow

This directory owns automated semantic review for trusted GitHub pull requests.

## Scope

- Review `opened` and `synchronize` events only when normalized webhook metadata
  proves the pull request is from the same repository and its actor meets the
  configured trust threshold.
- Require explicit repository, PR number, title, head branch, base branch, and
  head SHA metadata. Branch names are PR coordinates, never task identity or
  ownership evidence.
- Skip forks, irrelevant webhook actions, incomplete payloads, and events whose
  normalized actor integrity is missing, blocked, or below the trust threshold.
- The review is advisory — it does not gate or auto-merge the PR. Review
  assesses intent fulfillment, correctness, and architecture boundaries;
  guidance permits omitting new tests when types, schemas, or existing
  mechanisms already prove the behavior.
- Keep the review agent passive: it drafts structured output only. The workflow
  validates/bounds the body, gates approval, and posts through `github_comment`.
- Workflow-owned GitHub reads supply a bounded raw diff as untrusted agent input.
  Unavailable or stale evidence skips review; publication rechecks head/base/intent
  metadata after approval and identifies the reviewed head in the advisory comment.
- Requires the GitHub module to be configured with a token that has PR comment permissions.
