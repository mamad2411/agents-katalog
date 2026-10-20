---
name: github-actions-engineering
description: Build reliable GitHub Actions workflows. Use when authoring or
  debugging workflows.
metadata:
  tags: github, actions, engineering
---

# GitHub Actions Engineering

## Use this skill when
- Writing workflows, jobs, and reusable actions
- Managing triggers, caching, and concurrency
- Debugging failing runs

## Do not use this skill when
- Other CI platforms
- Shallow “add a step” without design

## Instructions
1. Pin action versions (tags or SHA) and audit third-party actions.
2. Use workflow_call reusable workflows for shared logic.
3. Set resource limits, timeout-minutes, and concurrency groups.
4. Cache dependencies with valid keys and check restore.
5. Use matrix builds intentionally; keep the matrix small.
6. Store secrets in GitHub secrets; never inline.
7. Leverage environment protection rules for prod deploys.
8. Use actions/checkout defaults; trim permissions to needed.

## Checklist
- Actions pinned
- timeout-minutes everywhere
- Least-privilege GITHUB_TOKEN

## Output Format
- Workflow design | jobs | caching | permissions | triggers

## Common Mistakes
- Unpinned mutable actions
- No timeouts (runaway jobs)
- Default full token permissions
