---
name: devops
description: Work on Docker, deployment, CI/CD, environment variables, server configuration, build pipelines, health checks, logs, monitoring, rollbacks, infrastructure scripts, and production operations.
---

# DevOps

## Workflow

1. Identify environment: local, CI, staging, production, container, VM, or Kubernetes.
2. Read existing scripts, workflows, Dockerfiles, compose files, manifests, and deployment docs.
3. Keep configuration outside the image and source code.
4. Define health checks, startup order, logs, metrics, traces, and rollback path.
5. Validate with the least risky command available.

## Required Checks

- Do not commit or bake secrets into images or repositories.
- Use least privilege for runtime users and credentials.
- Keep images small and deterministic where practical.
- Make production-impacting operations explicit before execution.
- Prefer reversible deployment and migration steps.

## Output

State changed operational behavior, validation command, rollback note, and any production risk.
