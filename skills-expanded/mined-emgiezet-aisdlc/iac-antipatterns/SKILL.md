---
name: iac-antipatterns
description: Forbidden IaC/container/CI patterns — public cloud resources, unencrypted storage, privileged containers, unpinned images, insecure CI workflows.
paths: ["**/*.dockerfile","**/*.tf","**/*.tfvars","**/*.yaml","**/*.yml","**/Dockerfile",".github/workflows/**/*.yaml",".github/workflows/**/*.yml",".gitlab-ci.yml","charts/**","templates/**/*.yaml"]
user-invocable: false
---

# IaC / containers / CI anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-TF-001 — Attach `aws_s3_bucket_public_access_block` with all four block flags set to `true`.
- AP-TF-002 — Never allow `0.0.0.0/0` inbound on admin/database ports; restrict to specific CIDRs.
- AP-TF-003 — Enable server-side encryption on every EBS, RDS, and S3 resource.
- AP-TF-004 — List specific IAM actions and resource ARNs; never use `Action: *` or `Resource: *`.
- AP-TF-005 — Use `sensitive = true` on secret outputs; load credentials from env vars or secrets manager.
- AP-K8S-001 — Set `privileged: false`, `allowPrivilegeEscalation: false`, and `runAsNonRoot: true`.
- AP-K8S-005 — Reference `secretKeyRef` from a Kubernetes Secret; never hard-code secrets in env or ConfigMap.
- AP-DOCKER-003 — Never put secrets in ENV/ARG/COPY; inject at runtime via env vars or use BuildKit secrets.
- AP-DOCKER-004 — Never pipe download to shell in RUN; add `set -o pipefail` before any pipe in RUN.
- AP-CI-001 — Pin every `uses:` to the full commit SHA (e.g. `actions/checkout@abc123...`).
- AP-CI-002 — Never check out PR code inside a `pull_request_target` workflow; use `pull_request` instead.
- AP-CI-003 — Pass event data via `env:` variables in run steps; never interpolate `${{ }}` into `run:`.

## Errors
- AP-TF-006 — Pin every provider and module to an exact version constraint in `required_providers`.
- AP-K8S-002 — Define `resources.requests` and `resources.limits` for every container.
- AP-K8S-003 — Pin container images to an explicit version tag or an immutable digest.
- AP-DOCKER-001 — Pin base images to a specific digest; never use `:latest` in production.
- AP-DOCKER-002 — Create a non-root user in the Dockerfile and end with `USER nonroot` before CMD.
- AP-CI-004 — Declare `permissions:` at the top level and restrict each job to the minimum needed.
- AP-CI-006 — Pin GitLab CI images to digests; use `include: { integrity: }` for remote includes.

## Warnings
- AP-DOCKER-005 — Use multi-stage builds; copy only the compiled artifact into the final minimal image.

Details for any ID: `reference/<ID>.md`
