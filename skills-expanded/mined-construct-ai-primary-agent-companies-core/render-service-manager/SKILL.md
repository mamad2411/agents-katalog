---
name: render-service-manager
description: >
  Use when creating new Render services, managing Render infrastructure,
  configuring auto-scaling, or handling Render-specific deployments.
  This skill manages Render platform operations.
---

# Render Service Manager - SaaSForge AI

## Overview
Render Service Manager specializes in creating, configuring, and managing Render services for the white-label multi-client platform, automating service provisioning and lifecycle management.

## When to Use
- When creating new client Render services
- When provisioning databases per client
- When configuring render.yaml files
- When managing service scaling
- When setting up domains and SSL
- **Don't use when:** Deployment orchestration needed (use Deployment-Orchestrator), or GitHub configuration needed (use GitHub-Branch-Manager)

## Core Procedures

### New Client Service Provisioning
1. **Service Plan** - Determine required plan based on client needs
2. **render.yaml Creation** - Create service configuration
3. **Service Creation** - Create service via Render API
4. **Database Provisioning** - Create PostgreSQL database
5. **Environment Variables** - Set all required env vars
6. **Domain Configuration** - Configure custom domain
7. **SSL Setup** - Enable automatic SSL
8. **Health Check** - Verify service is healthy

### render.yaml Configuration
```yaml
# render.yaml
services:
  - type: web
    name: companya-app
    env: node
    region: oregon
    branch: main
    repo: https://github.com/yourorg/companya-system
    buildCommand: npm ci && npm run build
    startCommand: npm start
    healthCheckPath: /health
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: companya-db
          color: blue

databases:
  - name: companya-db
    databaseName: companya_db
    plan: starter
    color: blue
```

### Auto-Scaling Configuration
```yaml
auto_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_percent: 70
  target_memory_percent: 80
  scale_up_cooldown: 300
  scale_down_cooldown: 600
```

### Domain & SSL Management
1. **Domain Verification** - Verify DNS ownership
2. **SSL Certificate** - Automatic via Let's Encrypt
3. **WWW Redirect** - Configure www to non-www redirect
4. **Custom Domain** - Point client domain to service

## Service Lifecycle Management

### Monitoring
- **Health Checks** - Periodic health check monitoring
- **Performance Metrics** - CPU, memory, request metrics
- **Error Rates** - Track 5xx error rates
- **Response Times** - Monitor p95/p99 response times

### Scaling Operations
1. **Scale Up** - Increase instances for high traffic
2. **Scale Down** - Reduce instances during low traffic
3. **Plan Upgrade** - Upgrade service tier as needed
4. **Plan Downgrade** - Optimize costs with smaller plan

### Decommissioning
1. **Data Export** - Export all client data
2. **Database Backup** - Create final backup
3. **Service Suspension** - Suspend service gracefully
4. **Final Export** - Export logs and metrics
5. **Cleanup** - Remove all resources

## Integration Points

### With Deployment-Orchestrator
- Execute deployments to target services
- Report service health status
- Support rollback operations

### With GitHub-Branch-Manager
- Configure auto-deploy from branches
- Set up build hooks
- Connect branches to services

### With Tenant-Manager
- Create services for new tenants
- Coordinate resource allocation
- Plan service capacity

## Error Handling

### Service Health Failure
- **Response:** Restart service, check logs
- **Investigation:** Review error logs
- **Escalation:** Escalate to DevOps Engineer if persistent

### Provisioning Failure
- **Response:** Retry provisioning
- **Validation:** Check render.yaml syntax
- **Escalation:** Check Render API status

## Success Metrics
- Service provisioning success: 100%
- Service uptime: ≥99.9%
- Average provisioning time: <15 minutes
- Database provisioning success: 100%
