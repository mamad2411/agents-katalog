---
name: deployment-orchestrator
description: >
  Use when coordinating multi-client deployments, managing deployment queues,
  rolling out updates across multiple company instances, or handling deployment
  rollbacks. This skill manages cross-instance deployment orchestration.
---

# Deployment Orchestrator - SaaSForge AI

## Overview
Deployment Orchestrator manages the coordination and automation of deployments across all client instances within the SaaSForge AI white-label multi-tenant platform.

## When to Use
- When rolling out updates to multiple client instances
- When coordinating deployment schedules across companies
- When managing deployment queues and priorities
- When executing rollback procedures
- When configuring auto-deployment triggers
- **Don't use when:** Individual service configuration is needed (use Render-Service-Manager), or branch management is needed (use GitHub-Branch-Manager)

## Core Procedures

### Multi-Client Deployment Workflow
1. **Pre-Deployment Check** - Verify all prerequisites, test environments, and client readiness
2. **Deployment Queue** - Queue deployments by priority and scheduled maintenance windows
3. **Staged Rollout** - Execute phased rollouts (canary → percentage → full)
4. **Health Verification** - Run health checks post-deployment
5. **Client Notification** - Notify clients of successful deployment
6. **Rollback if Needed** - Execute immediate rollback on failure

### Deployment Queue Management
1. **Queue Request** - Add deployment to queue with priority level
2. **Dependency Check** - Verify dependencies between deployments
3. **Resource Allocation** - Ensure resources available for deployment
4. **Execution** - Execute deployment in sequence
5. **Monitoring** - Monitor deployment progress and results

### Rollback Procedures
1. **Trigger Rollback** - Execute one-click rollback to previous version
2. **Service Restart** - Restart affected services
3. **Health Check** - Verify service health after rollback
4. **Notification** - Notify stakeholders of rollback

## Deployment Architecture

### Per-Company Structure
```
GitHub Repo (per company)
├── dev branch → dev.{company}.saasforge.ai (development)
└── main branch → {company}.saasforge.ai (production)

Deployment Pipeline:
dev branch merge → staging test → main branch merge → production deploy
```

### Multi-Instance Coordination
- **Deployment Targets:** All active company Render services
- **Rollout Strategy:** Phased by company priority
- **Health Monitoring:** Real-time across all instances
- **Communication:** Client notification on each deployment

## Integration Points

### With Render-Service-Manager
- Deploy to target services
- Coordinate with service health status
- Execute service restarts during deployment

### With GitHub-Branch-Manager
- Trigger deployments on main branch updates
- Coordinate merge-to-main with deployment schedule
- Manage release tagging

### With Client-Config-Manager
- Deploy environment variables with code
- Coordinate branding updates
- Manage feature flag rollouts

## Error Handling

### Deployment Failure
- **Response:** Immediately trigger rollback to previous working version
- **Notification:** Alert Deployment Orchestrator and DevOps Engineer
- **Investigation:** Log failure details for post-mortem

### Partial Rollout Failure
- **Response:** Pause remaining rollouts, assess impact
- **Decision:** Rollback affected instances or fix and continue
- **Communication:** Update all stakeholders on status

## Success Metrics
- Deployment success rate: ≥99.5%
- Average deployment time: <10 minutes
- Zero client downtime deployments: 100%
- Rollback success rate: 100%
