---
name: environment-management
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: environment management platform, preview environment design, ephemeral environment, environment parity, configuration drift detection, ephemeral environment provisioning, staging environment, environment lifecycle, environment as code, environment cleanup, environment promotion workflow, branch environment
---

# Skill — Environment Management

## When this skill activates

This skill activates when the user is designing or implementing environment management capabilities. This includes preview environments (per-PR), ephemeral environments, environment parity (dev/staging/prod consistency), configuration drift detection, automated environment provisioning, staging environment design, environment lifecycle management, environment-as-code, automatic cleanup, environment promotion workflows, and branch-based environments.

## Mandatory actions when this skill is active

### Before writing any code

1. Inventory existing environments: count, purpose, cost, utilization, and configuration drift from production.
2. Define environment types: production, staging, QA, developer sandbox, preview (per-PR), load testing. Establish parity requirements for each.
3. Assess environment provisioning time: how long from request to usable environment. Target: under 10 minutes.
4. Identify configuration drift: where do dev/staging/prod differ (versions, feature flags, resource sizes, network topology). Quantify drift percentage.
5. Establish environment cleanup policies: when to delete ephemeral environments (after PR merge, after N days of inactivity).

### During implementation

- **Preview Environments (Per-PR):** Automatically create an isolated environment for each pull request. Include: full application stack, seeded test data, unique URL. Preview environment should be ready in under 10 minutes. Delete automatically when PR is merged or closed.
- **Ephemeral Environments:** Short-lived environments created on-demand and destroyed after use. Use for: testing, demos, training, experiments. Include cost cap ($50-$200) and auto-deletion after 7 days of inactivity.
- **Environment Parity:** Dev, staging, and prod should be as similar as possible. Use same: container images, Terraform modules, network topology, resource sizes (scale down in non-prod, but maintain same architecture). Differ only in: data (synthetic in non-prod), scale (fewer replicas), and external integrations (use mocks in non-prod).
- **Environment as Code:** All environments defined via IaC (Terraform, CloudFormation, Pulumi). No manual changes in cloud console. Code should be versioned and reviewed via PRs. Use modules to ensure consistency across environments.
- **Configuration Drift Detection:** Use Terraform plan or CloudFormation drift detection. Run drift detection daily and alert on any manual changes. Automatically remediate drift by reapplying IaC.
- **Environment Provisioning:** Self-service provisioning via CLI, API, or portal. Provisioning should: validate inputs, estimate cost, apply IaC, seed data, run smoke tests, return URL. Complete in under 10 minutes.
- **Environment Lifecycle:** Define stages: provisioning → active → idle → scheduled for deletion → deleted. Idle environments (no activity for 3+ days) should be flagged for review. Auto-delete after 7 days idle (with 24-hour warning).
- **Environment Promotion:** Promote changes from dev → staging → production. Use GitOps workflow: commit to environment-specific branch triggers deployment. Include smoke tests and rollback on failure.
- **Staging Environment Design:** Staging should mirror production as closely as possible. Use 20-30% of production scale. Include: same services, same network topology, same feature flags, same monitoring. Differ only in: data volume and external integrations (use mocks or sandbox APIs).

### After implementation

- Verify preview environments are created automatically for each PR and deleted on merge.
- Confirm ephemeral environments include cost caps and auto-deletion after 7 days.
- Validate environment parity: dev/staging/prod use same IaC modules and container images.
- Ensure configuration drift detection runs daily and alerts on manual changes.
- Check that environment provisioning completes in under 10 minutes with cost estimates.

## Self-check before task completion

- [ ] Preview environments are created automatically per PR and deleted on merge.
- [ ] Ephemeral environments include cost caps and auto-deletion after 7 days idle.
- [ ] Environment parity is maintained: dev/staging/prod use same IaC modules.
- [ ] Configuration drift detection runs daily and alerts on manual changes.
- [ ] Environment provisioning is self-service and completes in under 10 minutes.
- [ ] Environment lifecycle includes idle detection and auto-cleanup after 7 days.
- [ ] Environment promotion uses GitOps workflow with smoke tests and rollback.
- [ ] Staging environment mirrors production at 20-30% scale with same architecture.
