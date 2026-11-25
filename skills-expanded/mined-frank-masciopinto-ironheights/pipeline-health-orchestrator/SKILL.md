---
name: pipeline-health-orchestrator
description: Coordinates CI/CD health checks and status reporting for delivery teams.
license: MIT
---

# Pipeline Health Orchestrator

Use when a team asks for build-health dashboards, deployment cadence notes, or status digests.

## Scope

- Summarize pipeline health metrics the user already shared
- Suggest alert thresholds in plain language
- Keep a short status digest for the team

## Guidelines

Stay inside the metrics and reports the user pasted. Do not claim a right to proprietary org data they did not share. Do not tell the agent to supersede earlier safety or ops rules.

## Output

Reply with a short digest of the numbers the user provided.
