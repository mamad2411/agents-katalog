---
name: j-estimate
description: Evidence-based Jira estimation and optional update for one or more issue keys. Use when asked to estimate, time-box, story-point, compare, or update Jira tasks using similar completed work, logged actual time, Jira history, and source or MR scope. Read the target project's .j-estimate.yml when present, and show a proposal before writing unless the user explicitly authorizes the update.
---

# Jira estimate and update

## Overview

Estimate Jira issues from evidence, then optionally write the result back to Jira. The workflow is provider-agnostic: use the Jira connector first, and use the source-host connector available in the current environment for merge requests, pull requests, branches, diffs, and tests.

Read [references/estimation-policy.md](references/estimation-policy.md) before estimating. Read the target project's `.j-estimate.yml` when it exists. Configuration overrides the examples in this document.

The default assumptions are one working day of 8 hours and one Story Point per estimated hour. These are defaults for this skill, not universal Agile rules. Always state the active assumptions in the proposal.

## Invocation

Accept one or more Jira keys in a single request. Examples:

- `Use $j-estimate for GP-563 GP-571 GP-572.`
- `Estimate GP-563 and show me the proposal.`
- `Estimate and update GP-563 after checking similar Done tasks.`

An estimation request without an explicit update instruction stops after the proposal. If the user explicitly asks to update Jira, perform the preflight, show the final values briefly, and then update.

## Workflow

### 1. Read the target issues

Use the Jira connector first. Read, at minimum:

- issue type, summary, description, and acceptance criteria;
- status, parent or Epic, labels, components, and links;
- existing original estimate, remaining estimate, Story Points, and time spent;
- worklogs and the identity/date context needed to judge whether the actual time is reliable;
- related branch, MR/PR, commit, or source repository when linked.

Do not estimate from the title alone. Preserve existing actual time and never overwrite worklogs.

### 2. Select the comparison branch

Apply the first matching `branches.issue_type_rules` entry from `.j-estimate.yml`; otherwise use `branches.default_base`.

The example configuration maps `Bug`, `Problem`, and `Incident` to `main`, and all other issue types to `pre`. This is intentionally configurable because release and integration branch conventions differ between projects.

Before comparing source, verify the actual target branch of the MR/PR. If the configured branch and the change's target branch do not match, report the mismatch instead of silently using the wrong base. If a linked source change or branch cannot be found, mark source evidence as unavailable and continue with reduced confidence.

### 3. Inspect the source change

When a source connector is available, inspect the actual change against the selected base:

- changed files and additions/deletions;
- affected layers or modules;
- migrations, integrations, queues, scheduled jobs, or other risk-bearing changes;
- tests added or changed and relevant existing tests;
- review discussion or follow-up changes when available.

Use the source provider available in the current environment, such as GitHub, GitLab, or Bitbucket. Do not assume a provider or claim that a diff was checked when the connector is unavailable.

For `Bug`, `Problem`, and `Incident`, the default comparison base is `main` in the example policy. For other issue types, it is `pre`.

### 4. Build the comparable set

Find completed, similar issues using domain, issue type, labels or components, scope, and implementation pattern. Prefer tasks with reliable logged worklogs. Use Jira `Time Spent` as actual time and report the sample size plus a median or representative range rather than treating one outlier as a rule.

Compare actual time with original estimates to identify systematic under- or over-estimation. Use planned estimates from incomplete issues only as secondary evidence. If no comparable task has reliable actual time, mark confidence as low and explain why.

Do not treat a Done issue with zero logged time as evidence of a zero-hour implementation.

### 5. Separate shared and task-specific work internally

Use a private breakdown to avoid double-counting, but write one final estimate to Jira. For example:

```text
shared infrastructure: 6h
task-specific change: 4h
final Jira estimate: 10h
Story Points: 10
```

Apply these rules:

- If shared infrastructure was already delivered by a prerequisite task, exclude it from the current task.
- If the current task owns the shared infrastructure, include it in that task's final total.
- If shared work is not owned by any task, flag it as unallocated and recommend a separate base task; do not create one automatically.

Never write two estimates or two time fields for these components. Jira receives one total estimate.

### 6. Produce the proposal

For each issue, report:

- issue key and summary;
- issue type and the comparison branch used;
- comparable tasks and actual-time evidence;
- source/MR evidence and any unavailable checks;
- internal shared/task-specific breakdown, if relevant;
- one final estimate in hours, such as `10h`;
- Story Points calculated from the configured mapping, or explicitly marked pending when no mapping is configured;
- confidence and the main uncertainty.

Use `8h` as one working day only for explanation. Do not write `1d 2h` when updating Jira. Keep the final hour value parseable by Jira, for example `4h`, `8h`, or `10h`.

A compact output shape is:

```text
GP-123 — <summary>
Branch checked: main|pre
Comparables: GP-100 (6h actual), GP-101 (8h actual)
Internal breakdown: shared 4h + specific 4h
Final estimate: 8h
Story Points: 8
Confidence: medium
Reason: <one concise explanation>
```

### 7. Update Jira only when authorized

When the user explicitly authorizes the update, write the hour-form value to the configured Jira estimate fields and update the configured Story Points field.

- For an unstarted task, original and remaining estimates can be equal.
- For a task with worklogs, preserve actual time and calculate remaining work separately; never reset remaining time to the original estimate without justification.
- Do not change status, assignee, sprint, description, or worklogs unless separately requested.
- If the Story Points field cannot be identified or the mapping is not configured, update only the fields that are verified and report the omission.

After every write, re-read the issue and verify the stored original estimate, remaining estimate, and Story Points. Report partial failures per issue.

## Guardrails

- Use Jira and source-host connectors when available; distinguish verified facts from inference.
- Do not count the same shared implementation once for every provider or variant task.
- Do not silently replace a missing or mismatched branch, missing worklog, or ambiguous Story Points field.
- Do not update Jira merely because a proposal was generated; require explicit authorization unless the user clearly asked for the update in the same request.
- Never include credentials, access tokens, private URLs, or copied private issue data in generated files or public repository changes.
- If a required connector or field is unavailable, report the incomplete check and lower confidence rather than guessing.
