---
name: ci-cd-awareness
description: Pipeline design, environment configuration, secret management in CI, deployment rollback strategies, and feature flags for gradual rollout.
invoke_when: Use when configuring CI/CD pipelines, discussing deployment strategies, setting up automated workflows, or when the project has CI config files.
---

# CI/CD Awareness

## Pipeline Structure

A well-designed pipeline follows this order:

### 1. Lint (fastest feedback)
- Run linters and formatters
- Fail fast on style violations
- Takes seconds, catches obvious issues

### 2. Type Check
- `tsc --noEmit` or equivalent
- Catches type errors before tests run

### 3. Test
- Unit tests first (fast)
- Integration tests second (slower)
- E2E tests last (slowest)
- Fail the pipeline if any test fails

### 4. Build
- Compile/bundle the application
- Verify the artifact is valid

### 5. Deploy
- Deploy to staging first
- Run smoke tests against staging
- Deploy to production with rollback capability

## Environment Configuration

- **Never** hardcode environment-specific values
- Use environment variables for all configuration
- Maintain separate configs: `.env.development`, `.env.staging`, `.env.production`
- Validate all environment variables at startup (fail fast if missing)

## Secrets in CI

- Use the CI platform's secret store (GitHub Secrets, etc.)
- Never echo secrets in logs
- Rotate secrets regularly
- Use minimal permissions (principle of least privilege)

## Deployment Strategies

- **Blue/green**: run two environments, switch traffic
- **Rolling**: gradually replace old instances
- **Canary**: route small % of traffic to new version first
- **Feature flags**: deploy code behind flags, enable gradually

## Rollback Plan

Every deployment must have a rollback strategy:
1. How to detect a bad deployment (health checks, error rates)
2. How to revert (previous container image, git revert, feature flag off)
3. How long rollback takes
4. Who is responsible for rollback decisions
