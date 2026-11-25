---
name: staging-qa-environment
description: "Group skill: Staging/QA environment setup — infrastructure, Docker Compose, database clone, feature flags, test data, E2E tests, load testing, monitoring, SSL, and smoke tests."
risk: low
source: self
---

# 🏗️ Staging / QA Environment

> **Group Skill** — Orchestrates sub-skills for preparing a staging environment for QA, UAT, or client review.
> Activate by saying: "Set up staging environment" or "QA environment setup"

## When to Use

- Preparing a staging environment for QA, UAT, or client review
- Need to simulate production for testing
- Setting up automated QA workflows

## Step-by-Step Workflow

### Step 1: Infrastructure
**Skill**: `terraform-skill` / `terraform-aws-modules`
- Provision staging infrastructure
- Configure networking and security
- Set up resource quotas

### Step 2: Docker Compose
**Skill**: `docker-expert`
- Create multi-service local stack
- Configure service dependencies
- Set up health checks

### Step 3: Database Clone
**Skill**: `database-admin`
- Clone production data (sanitized)
- Set up data refresh schedule
- Configure access controls

### Step 4: Feature Flags
**Skill**: `azure-appconfiguration-ts`
- Toggle features per environment
- Configure flag rollout rules
- Set up A/B test segmentation

### Step 5: Test Data
**Skill**: `data-autocleaning`
- Sanitize production data for privacy
- Generate synthetic test data
- Maintain data consistency

### Step 6: E2E Tests
**Skill**: `e2e-testing` / `e2e-testing-patterns`
- Set up automated QA test suite
- Configure test runners
- Define test scenarios

### Step 7: Load Testing
**Skill**: `k6-load-testing`
- Performance testing under load
- Set up load test scenarios
- Define performance baselines

### Step 8: Monitoring
**Skill**: `grafana-dashboards` / `prometheus-configuration`
- Set up staging observability
- Configure alerting thresholds
- Create dashboards

### Step 9: SSL/HTTPS
**Skill**: `mtls-configuration`
- Set up TLS certificates
- Configure mTLS if required
- Verify certificate chain

### Step 10: Smoke Tests
**Skill**: `test-automator`
- Quick sanity checks after deploy
- Verify critical paths
- Automated health verification

## Completion

Staging environment is fully configured and ready for QA. 🏗️

## Sub-Skills Referenced

1. `terraform-skill`
2. `terraform-aws-modules`
3. `docker-expert`
4. `database-admin`
5. `azure-appconfiguration-ts`
6. `data-autocleaning`
7. `e2e-testing`
8. `e2e-testing-patterns`
9. `k6-load-testing`
10. `grafana-dashboards`
11. `prometheus-configuration`
12. `mtls-configuration`
13. `test-automator`
