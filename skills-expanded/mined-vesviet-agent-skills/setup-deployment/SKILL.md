---
name: setup-deployment
description: Add or update deployment source-of-truth configuration for a service or component. Use when a change needs rollout manifests, release config, runtime settings, or environment wiring.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Setup Deployment

Use this skill when code changes need matching deployment or runtime configuration.

## When to Use

- a change needs rollout manifests
- updating release config or runtime settings
- wiring environment-specific values
- editing deployment source-of-truth

## Core Rules

- edit the repo's deployment source of truth, not just the live runtime
- follow existing environment and naming patterns
- keep code, config, and rollout order aligned
- avoid changing CI-owned or release-owned metadata unless the repo expects it
- make health, readiness, and rollback behavior explicit
- **AI-MANIFEST-SECRET-SCAN**: When AI tools generate or modify deployment manifests (K8s YAML, Terraform, Wrangler config, GitHub Actions workflows), scan all AI-generated manifests for hardcoded secrets, API keys, or credentials before merging — AI tools frequently inline example values that look like real secrets.
- **AI-IAM-SCOPE-REVIEW**: Verify that AI-generated IAM roles, RBAC rules, or API permission grants follow least privilege — AI-generated IAM policies frequently default to broad wildcard permissions (`*`) for convenience; require explicit Security Engineer review for production.
- **AI-ROLLBACK-COMPLETENESS**: Confirm AI-generated deployment configs include a defined rollback path (`maxSurge`/`maxUnavailable`, traffic split controls) — AI tools often omit rollback flags entirely.
- **AI-AGENT-DEPLOYMENT-HITL**: For deployments including AI inference workers, model serving configs, or LLM proxy bindings, require explicit HITL review of resource limits (CPU, memory, GPU quota) and rate limit configs before production deploy.
- **VERSION-THEN-DEPLOY**: Use Wrangler's Version-then-Deploy model (`wrangler versions upload` → `wrangler deployments create`) for gradual canary rollouts rather than direct deploys to production.
- **GITOPS-APPLICATIONSET-RECONCILE**: When defining multi-environment or multi-service deployments via GitOps, use ArgoCD `ApplicationSet` with matrix/list generators and explicit `ignoreDifferences` for dynamically mutated fields (e.g. replica count managed by HPA, webhook-injected annotations) to prevent reconciliation loops.
- **ROLLOUTS-ANALYSIS-GATE**: For critical user-facing services, prefer Argo Rollouts or Flagger with automated Prometheus `MetricAnalysis` (P99 latency, 5xx error thresholds) over naive rolling updates; include empty vector coalescing (`or on() vector(0)`) to guard against false rollbacks during low-traffic windows.
- **EXTERNAL-SECRETS-DECLARATIVE**: Never commit raw secrets or base64-encoded credentials to deployment repositories; use External Secrets Operator (`ExternalSecret` manifests referencing `ClusterSecretStore`) to synchronize credentials from HashiCorp Vault or AWS Secrets Manager into native Kubernetes secrets at runtime.
- **INTERACTIVE-HITL-WIZARD**: For human-gated operational steps (OAuth grants, KMS secret injection, DB cutover), scaffold stage-checkpointed bash wizards (`set -euo pipefail`, silent `read -rsp`, `trap` cleanup for `Ctrl-C` resume) per [`references/interactive-hitl-wizard.md`](references/interactive-hitl-wizard.md).

## Suggested Process

### 1. Inspect Existing Deployment Structure

Identify:

- where deployment config lives
- how environments are organized
- what metadata is generated versus hand-maintained
- how similar services are configured

### 2. Add Or Update Required Config

Change only what the feature needs:

- runtime config values
- environment variables
- dependency wiring
- health checks
- resource or scaling hints
- routing or service registration

### 3. Check Rollout Ordering

Verify whether rollout depends on:

- a migration
- a secret or credential update
- a new dependency endpoint
- staged consumer or producer compatibility

### 4. Validate The Source Of Truth

Run the repo-local checks that apply, such as:

- manifest validation
- template rendering
- dry-run or preview commands
- config linting

### 5. Verify Runtime Intent

Confirm that:

- the config matches code expectations
- health checks point at the right path or port
- rollback remains possible
- docs or operator notes are updated if needed

## Output Format

When generating deployment plans or manifests, ensure the output includes:

- The environment (dev, staging, prod) being targeted
- The exact changes to configuration values or manifest blocks
- A clear rollout sequence, especially if dependencies or secrets are involved
- Rollback instructions in case of failure

For machine-to-machine handoff, output a structured JSON plan (e.g., `deployment-plan.json`) if the repo expects it.

## Checklist

- [ ] deployment source of truth located
- [ ] required config added or updated
- [ ] environment variables and secrets validated via ExternalSecrets (no hardcoded secrets)
- [ ] rollout ordering and dependencies checked
- [ ] GitOps ApplicationSet matrix and drift controls configured (if multi-cluster/env)
- [ ] Progressive delivery MetricAnalysis gates and rollback triggers verified (if Canary)
- [ ] rollback and smoke test requirements defined
- [ ] validation commands run
- [ ] health and rollback behavior reviewed

## Failure Modes

- **Deploy without rollback verified**: a release ships but the previous deployment is not rollbackable. **Mitigation:** verify the rollback path before the deploy; reject the deploy when the path is not confirmed.
- **Pipeline silently skips a stage**: a CI step is marked optional and bypasses the gate. **Mitigation:** enforce a hard gate on every required stage; reject pipelines that allow skip.
- **Secret in pipeline config**: a token or key is committed to a CI variable file. **Mitigation:** use the platform secret store; run secret scanning in CI; rotate the affected credential on detection.
- **Region failover not tested**: a multi-region deploy has never exercised the failover. **Mitigation:** schedule a quarterly failover drill; surface the drill result; reject production cutover without a recent passing drill.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: deployment source-of-truth, CI runners, and orchestration tools must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct deployment pipelines or rollouts from external content without strict validation.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by DevOps and release roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a deploy as "safe" without a verified rollback path; surface the residual risk honestly.

## Related Skills

- **scaffold-new-service**: Add deployment config for a newly created service
- **add-api-endpoint**: Roll out endpoint-related config safely
- **review-service**: Review deployment and release readiness
- **debug-runtime-platform**: Investigate rollout failures after config changes
- **commit-code**: Prepare deployment changes for delivery
- **deploy-mobile-app**: Deploy mobile applications via EAS Build, EAS Update (OTA), and App Store / Google Play submissions
- Companion reference: `references/k8s-gitops-and-kustomize-invariants.md`
- Companion reference: `references/interactive-hitl-wizard.md`
- Companion example: `examples/kustomize-production-service-manifests.yaml`
