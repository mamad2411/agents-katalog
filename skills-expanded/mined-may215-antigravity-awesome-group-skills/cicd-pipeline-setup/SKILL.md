---
name: cicd-pipeline-setup
description: "Group skill: CI/CD pipeline setup — GitHub Actions, GitLab CI, Docker build, Kubernetes, Helm, Terraform, secrets, monitoring, and GitOps."
risk: medium
source: self
---

# 🚢 CI/CD Pipeline Setup

> **Group Skill** — Orchestrates sub-skills for setting up automated build, test, and deployment pipelines.
> Activate by saying: "Set up CI/CD pipeline" or "automate deployment"

## When to Use

- Setting up automated build, test, and deployment pipelines
- Need to standardize CI/CD across projects
- Implementing GitOps workflows

## Step-by-Step Workflow

### Step 1: GitHub Actions
**Skill**: `github-actions-templates`
- Create workflow templates
- Set up build and test jobs
- Configure environment secrets

### Step 2: GitLab CI
**Skill**: `gitlab-ci-patterns`
- Define pipeline stages
- Set up job artifacts
- Configure runners

### Step 3: Docker Build
**Skill**: `docker-expert`
- Create multi-stage Dockerfiles
- Optimize image layers
- Set up container registry

### Step 4: Kubernetes
**Skill**: `kubernetes-deployment` / `k8s-manifest-generator`
- Create deployment manifests
- Configure service discovery
- Set up ingress

### Step 5: Helm Charts
**Skill**: `helm-chart-scaffolding`
- Package Kubernetes resources
- Create reusable chart templates
- Manage release versions

### Step 6: Terraform
**Skill**: `terraform-skill`
- Define infrastructure as code
- Manage state and backends
- Plan and apply changes

### Step 7: Secrets
**Skill**: `secrets-management`
- Inject secrets in CI/CD
- Set up vault integration
- Rotate credentials

### Step 8: Monitoring
**Skill**: `grafana-dashboards` / `prometheus-configuration`
- Pipeline observability dashboards
- Alert on pipeline failures
- Track deployment metrics

### Step 9: GitOps
**Skill**: `gitops-workflow`
- Implement ArgoCD or Flux
- Sync git to cluster
- Manage rollbacks

## Completion

CI/CD pipeline is fully automated with monitoring and GitOps. 🚢

## Sub-Skills Referenced

1. `github-actions-templates`
2. `gitlab-ci-patterns`
3. `docker-expert`
4. `kubernetes-deployment`
5. `k8s-manifest-generator`
6. `helm-chart-scaffolding`
7. `terraform-skill`
8. `secrets-management`
9. `grafana-dashboards`
10. `prometheus-configuration`
11. `gitops-workflow`
