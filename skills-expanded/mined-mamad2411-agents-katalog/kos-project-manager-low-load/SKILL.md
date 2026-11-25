---
name: kos-project-manager-low-load
description: Project-manager low-load registry rules for dispatching one eligible PR-producing workflow without hardcoding only improvement/governance jobs.
user-invocable: true
when_to_use: "When implementing or reviewing project-manager low-load behavior."
category: workflows
keywords: [project-manager, low-load, pr-producing, registry, workflow-dispatch]
metadata:
  author: project-manager
  license: repo
  version: "1.0"
---

# Project Manager Low Load

Low-load mode runs when open PRs and standalone issues are both at or below threshold. It dispatches exactly one eligible PR-producing workflow.

## Registry

Include every workflow that can create PRs via:

- `upsert-pull-request`
- `prepare-automation-branch`
- `_auto-fix-ci.yml`
- another shared PR lifecycle path

Classify workflows as:

- `proactive`: safe low-load candidate.
- `conditional-proactive`: eligible only with extra context, such as a phase id.
- `contextual`: known PR producer but not low-load fan-out.

## Eligibility

Skip workflows with active runs, pending duplicate automation PRs, missing required context, or cooldown.

## Critical constraints

- Dispatch one workflow per run.
- Maintain registry coverage tests so new PR-producing workflows cannot be invisible.
- Do not dispatch contextual repair workflows without their issue, PR, run, finding, or phase context.
