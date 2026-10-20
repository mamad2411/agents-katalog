# Repo AI Checks Workflow

This workflow runs trusted repo-local AI check definitions against GitHub pull
request events.

- Discover check definitions from the daemon's trusted project checkout, never
  from untrusted PR-head payload fields.
- Keep check agents passive and read-only; they return structured verdicts
  only.
- Workflow-owned GitHub reads supply a bounded raw diff as untrusted input.
  Unavailable or stale evidence yields skipped checks, never passes; summary and
  comment publication recheck head/base/intent metadata without downloading the
  diff again. Never execute PR-head code to evaluate checks.
- Persist per-check artifacts before emitting summaries or posting advisory
  GitHub comments.
- Use the same deterministic prepare, policy, approval, and `github_comment`
  posting shape as other autonomy PR workflows.
