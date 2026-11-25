---
name: ci-operator
description: Operate long-running CI/CD jobs asynchronously and retry-safely for Codex/X and other coding agents. Use for GitHub Actions, CodeBuild, CodeBuild-hosted GitHub Actions runners, CodePipeline, or GitLab CI/CD when the agent must trigger or observe builds, runners, pipelines, queued jobs, failed webhooks, retries, or redeliveries. Prefer durable run/build IDs, historical-duration waits, compact status readback, adaptive backoff, failure-only logs, reconcile-before-retry, sparse GitHub evidence, and the owning repository's existing authority.
---

# CI Operator

Operate CI like an asynchronous controller, not a human staring at a terminal.

## Core loop

```text
resolve owning repo + authority
-> reconcile prior execution
-> trigger once if still needed
-> persist exact run/build/execution ID
-> estimate expected duration
-> sleep
-> compact status readback
-> back off if still running
-> inspect detailed logs only when needed
-> record one durable terminal/checkpoint result
```

## Authority

Before any mutation, inherit authority from the current user instruction and owning repository `AGENTS.md`, active `SPEC.md`, Issue, and PR.

This Skill does **not** grant repository, AWS, deployment, PROD, or retry authority.

- DEV/LAB: when the durable repo contract explicitly grants bounded standing authority, do not ask again for the same bounded CI/build operation.
- PROD read-only observation: proceed only when repo policy allows it.
- PROD deployment/mutation/destructive work: follow the repo's explicit approval gates.

## Reconcile before trigger or retry

Before starting or repeating a workflow/build/pipeline:

1. read the owning Issue/PR/checkpoint;
2. find any exact prior run/build/execution ID for the same intent;
3. read that provider state;
4. if running, wait/read back instead of retriggering;
5. if terminal, report/use that result;
6. if outcome is ambiguous, fail closed and reconcile provider state first.

Loss of shell/session/runner/controller is not permission to replay a mutation.

## Adaptive waiting

Prefer observed/historical duration over high-frequency polling.

When no better history exists:

- expected under 1 minute: wait about 30-60 seconds;
- expected 1-5 minutes: wait about 1-2 minutes;
- CodeBuild/hosted-runner jobs commonly taking several minutes: wait about 2-5 minutes;
- longer jobs: progressively increase the interval.

If still running, wait again with equal or longer backoff.

Avoid continuous watch loops such as `gh run watch --interval 15` for agent execution unless live streaming is specifically necessary.

## Compact readback

Prefer status queries that return only what changes the next decision:

- exact run/build/execution ID;
- status/conclusion;
- relevant timestamps;
- failing job/stage when available.

Do not stream unchanged status or full logs into model context.

## Logs and diagnosis

Fetch verbose logs only when:

- failed, cancelled, or timed out;
- unexpectedly stuck;
- a specific error requires diagnosis;
- a meaningful transition needs proof.

After diagnosis, make routine in-scope fixes and continue the same owning Goal/PR when authorized.

## Retry and redelivery

Before retry/redelivery, prove what happened to the previous intent.

For failed webhook delivery:

- verify the delivery failed;
- verify the required provider execution was not already admitted;
- redeliver only that exact failed event when authorized;
- never broadly replay unrelated events.

For provider retries:

- keep the same intent identity;
- persist the new execution ID;
- do not create parallel duplicate executions unless the owning contract explicitly requires it.

## Sparse durable evidence

GitHub is durable state, not a polling transcript.

Write/update durable evidence only for:

- run/build/execution ID;
- meaningful state transition;
- retry/redelivery decision;
- terminal PASS/FAIL;
- blocker;
- acceptance or next authority gate.

Do not comment for every sleep, poll, unchanged queue state, or local observation.

## Continuity

Keep the approved repository/worktree/controller lane sticky.

After interruption:

```text
reload owning Issue/PR
-> reload exact execution IDs
-> read provider state
-> continue
```

Do not silently switch writer/controller merely because CI is delayed.

## Providers

Read `references/providers.md` only when provider-specific behavior is needed.

## Completion

Return a compact result containing:

- provider + exact execution ID;
- terminal/current state;
- material failure/recovery if any;
- evidence pointer;
- next real gate/action.

Do not ask for confirmation while authorized routine CI work remains.
