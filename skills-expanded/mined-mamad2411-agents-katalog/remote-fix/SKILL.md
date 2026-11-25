---
name: remote-fix
description: >
  Remote fix workflow. Receives a diagnostic (from Cowork scheduled task,
  manual observation, or user report), investigates the issue, fixes it,
  and creates a PR. Designed for quick fixes triggered remotely via
  Channels (Discord/Telegram). Use when the user says "fix this",
  "handle this diagnostic", "the scheduled task found X", or sends a
  Cowork diagnostic summary.
---

# Remote Fix

You are running a remote fix triggered from outside the terminal
(Channels, Dispatch, or manual). The human may have limited context
(on phone, at work). Be autonomous but conservative.

## Step 1 — Understand the diagnostic

Read the message. Identify:
- What's broken (error, metric, behavior)
- Where (which service, file, endpoint)
- Severity (blocking vs degraded vs cosmetic)

If a Cowork diagnostic file exists in monitoring/, read it.
Read tasks/lessons.md for related past issues.

## Step 2 — Investigate

Find the root cause. Read logs, grep errors, check recent commits.
If the issue is unclear after 5 minutes of investigation, STOP
and report what you found — don't guess-fix.

## Step 3 — Fix

If the fix is clear and touches ≤ 3 files:
- Create a branch: fix/[description]
- Implement the minimal fix
- Run tests
- Commit with conventional commit message

If the fix is complex (> 3 files, architectural):
- STOP. Report the diagnosis and recommended approach.
- The human decides: fix now or defer to a proper sprint.

## Step 4 — PR and report

- Push the branch, create a PR with description
- Report back via Channel: "PR #XX ready — [1-line summary]"
- Wait for human to merge

## Step 5 — Verify (after merge)

If the human says "merged" or "verify":
- Check deploy status
- Verify the metric/error is resolved
- Update tasks/lessons.md if this is a new pattern
- Report: "Deploy OK, issue resolved"

STOP. Do not continue to other phases. Do not start a sprint.
This is a surgical fix, not a sprint cycle.

## Gotchas

- You're being commanded from a phone. Keep responses SHORT.
  No walls of text. Summary + PR link + status.
- Don't start a full sprint cycle. This is a surgical fix.
- If you're not sure, SAY SO. Better to wait than ship a bad fix.
- Never force-push to main. Always PR, always wait for merge.
- The human may take hours to respond (they're at work). That's
  normal. Don't spam updates.
- If the diagnostic mentions multiple issues, fix only the most
  critical one. Add the rest to tasks/backlog.md.
