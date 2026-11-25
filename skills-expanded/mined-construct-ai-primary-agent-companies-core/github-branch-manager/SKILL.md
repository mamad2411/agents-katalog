---
name: github-branch-manager
description: >
  Use when managing GitHub repositories, branch workflows, merge operations,
  or GitHub Actions configurations for client systems. This skill handles
  version control operations.
---

# GitHub Branch Manager - SaaSForge AI

## Overview
GitHub Branch Manager specializes in managing GitHub repositories, branches, and workflows for the white-label multi-client platform, ensuring proper version control isolation.

## When to Use
- When setting up new client repository
- When configuring branch protection rules
- When automating merge workflows
- When setting up GitHub Actions CI/CD
- When managing release tagging
- **Don't use when:** Deployment execution needed (use Deployment-Orchestrator), or Render service changes needed (use Render-Service-Manager)

## Core Procedures

### New Client Repository Setup
1. **Repository Creation** - Create new repo from template
2. **Branch Structure** - Set up dev and main branches
3. **Branch Protection** - Configure protection rules for main
4. **Collaborator Access** - Add team members with appropriate permissions
5. **GitHub Actions** - Configure CI/CD workflows
6. **Webhook Setup** - Set up deployment webhooks

### Branch Protection Configuration
```yaml
main_branch:
  protection:
    require_pull_request: true
    required_reviews: 1
    enforce_admins: true
    require_status_checks: true
    status_checks:
      - test
      - lint
      - build
```

### Dev-to-Main Merge Workflow
1. **Feature Complete** - All changes on dev branch
2. **Pull Request** - Create PR from dev to main
3. **Code Review** - Review changes and approve
4. **Status Checks** - Verify all checks pass
5. **Merge** - Execute merge to main
6. **Deploy Trigger** - Trigger production deployment

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches:
      - main
      - dev

jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Production
        run: ./deploy.sh production
      
  deploy-dev:
    if: github.ref == 'refs/heads/dev'
    steps:
      - name: Deploy to Development
        run: ./deploy.sh dev
```

## Repository Template Structure
```
client-template/
├── src/
├── tests/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── render.yaml
├── .env.example
├── README.md
└── .gitignore
```

## Integration Points

### With Deployment-Orchestrator
- Coordinate branch updates with deployment schedule
- Provide release tag management
- Generate deployment changelogs

### With DevOps-Engineer
- Integrate with CI/CD pipeline
- Coordinate build configurations
- Set up test automation

### With Client-Config-Manager
- Manage configuration-specific branches
- Coordinate feature branches
- Handle hotfix branches

## Error Handling

### Merge Conflict
- **Response:** Notify team, resolve conflicts on feature branch
- **Strategy:** Rebase feature branch before merge
- **Verification:** Test after conflict resolution

### Failed Status Checks
- **Response:** Block merge, notify team
- **Debug:** Investigate failed checks
- **Remediation:** Fix issues, re-run checks

## Success Metrics
- Repository setup success: 100%
- Branch policy compliance: 100%
- Merge conflict resolution: <30 minutes
- CI/CD pipeline reliability: ≥99%
