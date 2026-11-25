---
name: sentry-triage
description: Query Sentry for production errors, filter by severity/frequency, deduplicate against existing GitHub issues, and create actionable issues for the implement-queue. Invoke with /sentry-triage.
user-invocable: true
---

# Sentry Triage

Automated production error to GitHub issue pipeline. Queries Sentry MCP for actionable errors and creates deduplicated issues for the implement-queue.

## Prerequisites

1. **Sentry MCP configured** in `.mcp.json`
2. **Token with event:read scope** — create at sentry.io/settings/account/api/auth-tokens/
3. **Set SENTRY_ACCESS_TOKEN env var** before running

## Running Triage

```bash
SENTRY_ACCESS_TOKEN=<token> node .claude/skills/sentry-triage/scripts/triage.mjs
```

## Workflow

### Step 1: Query Sentry

Run `fetch-issues.mjs` or `triage.mjs` to get production errors.

### Step 2: Filter Issues

- Only `error` or `fatal` level
- > 5 occurrences in 14 days
- Max 3 issues per run

### Step 3: Deduplicate

Search existing `sentry`-labeled GitHub issues in **every** state (open and
closed, never `state:open` alone), then key the match on the Sentry issue ID
parsed out of each candidate's body URL — never the title string. If the
search itself can't run (network failure, bad credential, non-2xx response),
skip filing rather than risk a duplicate (`scripts/sentry-triage-dedup.mjs`).

### Step 4: Create Issues

Create `ready,sentry,bug` issues for implement-queue pickup.

## Current Status

Pipeline active — 0 production errors across 2 projects.
