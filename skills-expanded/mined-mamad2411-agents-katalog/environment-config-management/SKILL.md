# Environment Config Management

## Purpose
Maintains consistency of the `environments/` directory across all four environments.

## Role
DevOps Engineer

## Phase
Cross-phase (infrastructure)

## Triggered By
New env var added to any service.

## Inputs
- New/changed environment variable requirement

## Process
When a new env var is added to any service:
1. Add to `environments/sit/values/{service}.yaml`.
2. Add to `environments/uat/values/{service}.yaml`.
3. Add to `environments/staging/values/{service}.yaml`.
4. Add to `environments/production/values/{service}.yaml`.

Sensitive values: NEVER in values files → Vault reference format: `secretRef: vault/secret/path/to/secret#fieldName`.

Validates: no environment-specific hardcoding in Helm templates. Validates: all environments have consistent env var sets.

## Outputs
Consistent environment variable sets across sit/uat/staging/production.

## Quality Gates
- [ ] New env var added to all four environments
- [ ] Sensitive values reference Vault, never inlined
- [ ] No environment-specific hardcoding in Helm templates
- [ ] Env var sets verified consistent across environments

## References
- `.claude/skills/devops-engineer/helm-chart-management/SKILL.md`
- `.claude/skills/devops-engineer/vault-provisioning/SKILL.md`
