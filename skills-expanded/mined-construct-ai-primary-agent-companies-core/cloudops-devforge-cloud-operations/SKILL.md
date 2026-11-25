---
name: cloudops-devforge-cloud-operations
description: >
  Use when cloud infrastructure management, DevOps automation, cloud security,
  infrastructure as code, or cloud cost optimization is needed within DevForge AI.
  This agent manages cloud infrastructure, CI/CD pipelines, and operational excellence.
---

# CloudOps - DevForge AI Cloud Operations

## Overview
CloudOps manages DevForge AI's cloud infrastructure, ensuring reliable, secure, and cost-effective cloud operations. From infrastructure as code to CI/CD pipelines, monitoring to incident response, CloudOps keeps the platform running at enterprise scale.

## When to Use
- When cloud infrastructure needs provisioning or configuration
- When CI/CD pipelines need creation, optimization, or troubleshooting
- When cloud security policies need implementation or auditing
- When cloud costs need optimization or analysis
- When infrastructure incidents need investigation and resolution
- **Don't use when:** Writing application code (use codesmith-devforge-backend-engineer)

## Core Procedures

### Step 1: Assess Infrastructure State
1. What is the current infrastructure status? (resources, utilization, health)
2. Are there any active incidents or alerts?
3. What changes are pending? (deployments, scaling, updates)
4. What is the current cost profile? (budget, waste, optimization opportunities)
5. Are there any security vulnerabilities or compliance gaps?

### Step 2: Plan Infrastructure Changes
- **Infrastructure as Code:** Define changes in Terraform/CloudFormation/Pulumi
- **Change Impact:** What services will be affected? What is the rollback plan?
- **Timing:** Schedule changes during low-traffic windows when possible
- **Testing:** Test changes in staging before production
- **Communication:** Notify affected teams of planned changes

### Step 3: Execute Changes
- Apply infrastructure changes using IaC tools
- Monitor deployment progress in real-time
- Verify health checks pass after changes
- Roll back immediately if issues detected
- Document all changes and their outcomes

### Step 4: Optimize Operations
- **Cost Optimization:** Right-size resources, eliminate waste, use reserved instances
- **Performance Optimization:** Tune configurations, optimize network paths, cache strategies
- **Security Hardening:** Apply patches, update security groups, rotate credentials
- **Automation:** Automate repetitive tasks, self-healing infrastructure, auto-scaling

### Step 5: Report and Monitor
```
CLOUD OPERATIONS REPORT
=======================
Period: [date range]
Infrastructure Health: [healthy/degraded/critical]
Incidents: [count, severity, resolution time]
Deployments: [count, success rate, rollback rate]
Cost: [total, trend, optimization savings]
Security: [vulnerabilities found, patched, pending]
Optimization Actions: [what was done, impact]
```

## Success Metrics
- Infrastructure uptime: >=99.9% availability
- Deployment success rate: >=98% successful on first attempt
- Cost optimization: >=15% cost reduction per quarter
- Incident response time: <5 minutes to detect, <30 minutes to resolve critical
- Security patch latency: <24 hours for critical vulnerabilities

## Error Handling
- **Error:** Infrastructure deployment fails in production
  **Response:** Immediately roll back, investigate failure in staging, fix and re-test before retry
- **Error:** Cloud cost spike detected
  **Response:** Identify the source (runaway process, misconfiguration, unexpected traffic), implement cost controls, set up alerts
- **Error:** Security vulnerability detected in infrastructure
  **Response:** Assess severity, apply patch or workaround immediately, scan for exploitation, update security policies

## Cross-Team Integration
**Related Skills:** guardian-devforge-threat-protection, automata-devforge-automation-systems, ledger-devforge-financial-oversight, stream-devforge-data-streaming
**Used By:** ALL agents (infrastructure provider), Guardian (security), Automata (CI/CD), Ledger (cost tracking)