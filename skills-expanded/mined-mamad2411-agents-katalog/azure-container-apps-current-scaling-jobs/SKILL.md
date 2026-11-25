---
name: azure-container-apps-current-scaling-jobs
description: Reviews Azure Container Apps scaling rules, replica limits, scale-to-zero behavior, KEDA-style triggers, and Container Apps jobs. Use when tuning scale, diagnosing replica behavior, or designing finite jobs.
license: MIT
compatibility: Azure Container Apps managed service, current Microsoft Learn guidance.
---

# Azure Container Apps Scaling and Jobs

This skill helps agents reason about replica limits, scale rules, and Container Apps jobs.

## When to Use

Use this skill when the task involves:

- min/max replicas;
- scale-to-zero;
- HTTP or event-based scale rules;
- queue/event/database scaler connectivity;
- job create/update/start/stop commands;
- scheduled jobs;
- parallelism, retry, and timeout behavior;
- high cost, cold starts, or under-scaling.

## Scaling Principles

1. Scaling is a combination of replica limits, rules, and behavior.
2. Minimum replicas affect availability, cold starts, and cost.
3. Maximum replicas affect cost, downstream pressure, and database/queue limits.
4. Scale rules must be reachable from the Container Apps environment.
5. Troubleshoot scaler connectivity before increasing limits.
6. Jobs are for finite tasks; long-running services should be container apps.
7. Record operational goals before changing scale settings.

## Workflows

Use `workflows/scale-and-jobs-review-workflow.md` to review scale or job behavior.

## Resources

Use `resources/scale-jobs-checklist.md`.

## Examples

Use `examples/job-definition-example.md` for a generic job definition.
