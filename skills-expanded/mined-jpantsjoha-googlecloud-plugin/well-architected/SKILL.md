---
name: well-architected
description: "Google Cloud Well-Architected Framework reference. Six pillars: operational excellence, security, reliability, cost optimization, performance, and sustainability. Referenced by gcp-architect and gcp-security for every design review. Use when the user mentions: GCP framework, architecture pillars, reliability GCP, cost optimization GCP, performance GCP, sustainability GCP, WAF review."
license: MIT
metadata:
  "googlecloud-plugin/version": "0.1"
  "googlecloud-plugin/triggers": "well-architected, GCP framework, architecture pillars, reliability GCP, cost optimization GCP, performance GCP, sustainability GCP, operational excellence, WAF review"
  "googlecloud-plugin/required-scopes": ""
---

# GCP Well-Architected Framework

Six pillars that every GCP workload should be evaluated against. Referenced in every HLD, security review, and operational readiness check.

## The Six Pillars

| Pillar | Core Question | Key Practices |
|--------|--------------|---------------|
| **Operational Excellence** | Can we build, run, and evolve the system reliably? | IaC, CI/CD, runbooks, monitoring-as-code |
| **Security** | Is the system protected against threats? | Least-privilege IAM, encryption, no public exposure by default |
| **Reliability** | Will the system recover from failures? | Multi-region, health checks, SLOs, chaos testing |
| **Cost Optimization** | Are we spending efficiently? | Right-sizing, committed use, lifecycle policies, budget alerts |
| **Performance** | Can the system handle load and scale? | Autoscaling, CDN, caching, regional proximity |
| **Sustainability** | Are we minimizing environmental impact? | Carbon-aware regions, efficient resource use |

## Quick Review Checklist (per design)

### Operational Excellence
- [ ] Infrastructure as Code (Terraform or Config Connector)
- [ ] CI/CD pipeline with automated tests
- [ ] Runbook for each primary failure mode
- [ ] Alerting tied to SLOs

### Security
- [ ] Least-privilege IAM throughout
- [ ] No public exposure without intent
- [ ] Secrets in Secret Manager
- [ ] Network deny-by-default

### Reliability
- [ ] SLO defined (availability + latency)
- [ ] Health checks configured
- [ ] Multi-zone or multi-region for production
- [ ] Backup and recovery tested

### Cost Optimization
- [ ] Right-sized instances (use GCP recommender)
- [ ] Committed use discounts evaluated
- [ ] Budget alerts configured
- [ ] Lifecycle policies on storage

### Performance
- [ ] Load tested at target traffic
- [ ] Caching layer evaluated
- [ ] CDN for static assets
- [ ] Autoscaling configured

### Sustainability
- [ ] Low-carbon region selected where latency allows
- [ ] Idle resources scheduled for shutdown

## References

- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)
- [Operational Excellence Pillar](https://cloud.google.com/architecture/framework/operational-excellence)
- [Security Pillar](https://cloud.google.com/architecture/framework/security)
- [Reliability Pillar](https://cloud.google.com/architecture/framework/reliability)
- [Cost Optimization Pillar](https://cloud.google.com/architecture/framework/cost-optimization)
- [Performance Optimization Pillar](https://cloud.google.com/architecture/framework/performance-optimization)
