---
name: circleci-pipelines
description: "Write CircleCI pipelines: orbs, executor and cache strategy, parallelism, workflow dependencies, and secure approval gates."
type: procedural
category: devops
domain: devops
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - circleci config yaml
  - circleci orb usage
  - circleci cache strategy
  - circleci workflow approval
  - circleci docker executor
keywords:
  - circleci
  - ci
  - pipelines
  - orbs
  - caching
  - workflows
source: custom
enabled: true
---

# CircleCI Pipelines

## Purpose

Write CircleCI pipelines: orbs, executor and cache strategy, parallelism, workflow dependencies, and secure approval gates.

## When to Use

- A project uses CircleCI and needs pipeline structure or fixes.
- Builds are slow due to missing caches or serial jobs.
- Deployments need manual approval and environment gating.

## When NOT to Use

- The project uses GitHub Actions or GitLab CI; config syntax does not transfer.
- You need to design CI strategy from scratch without a chosen platform.
- The failure is in the application rather than the pipeline.

## Capabilities

- Structure workflows with reusable commands and executors.
- Pin orbs to exact versions for reproducibility.
- Cache dependency directories keyed by lockfile hashes.
- Gate production deploys behind approval jobs and contexts.

## Inputs

- The CircleCI config (`.circleci/config.yml`) and the project's build commands.
- Runtime versions and service dependencies (databases, queues).
- Required secrets and contexts for deploys.

## Workflow

1. Read the current workflow graph and identify the critical path.
2. Pin orb versions and image tags; floating tags break reproducibility.
3. Key caches on lockfile checksums and restore with fallback keys.
4. Split independent jobs and use `requires` to parallelize safely.
5. Protect deploy jobs with contexts, approval jobs and restricted SSH keys.

## Tools

- CircleCI CLI (`circleci config validate`)
- orbs
- contexts and approvals

## Examples

- `circleci config validate`
- `circleci local execute --job test`
- `circleci config process .circleci/config.yml`

## Safety

- Unpinned orbs and `latest` images can change behaviour without a commit.
- Deploy contexts should be restricted to protected branches.
- Caching secrets or build artifacts across branches can leak privileged data.

## Source

All-Skills canonical library (`skills/devops/circleci-pipelines`). First-party skill, maintained in this repository.

## Notes

- `circleci config process` shows the resolved config before you push.
- Test splitting by timing data keeps parallel runs balanced.
- Pairs with: `devops/ci-cd-pipeline`, `security/secrets-management`.
