---
name: developer-platform
last_reviewed: 2026-09-06
group: Ship and run
description: >-
  Build golden paths and self-service provisioning so teams stop rebuilding the same scaffolding.
  Use when building internal developer portals, CLI scaffolds, or dev tooling.
---

# Developer Platform

Designs and maintains internal developer platforms that provide golden paths, self-service infrastructure, and smooth developer workflows.

## Phased Workflow

### Phase 1: Developer Experience Audit
1. Map the current developer journey: onboarding time, environment setup friction, deployment complexity, and feedback loop latency.
2. Identify the top 5 developer pain points through surveys, time-tracking, and support ticket analysis.
3. Define platform success metrics: time-to-first-deploy, mean deployment frequency, change failure rate, DORA metrics.

### Phase 2: Golden Path & Template Architecture
1. Build opinionated project scaffolding templates (service templates, library templates, infrastructure modules).
2. Standardize CI/CD pipeline templates with built-in security scanning, testing, and deployment stages.
3. Create self-service provisioning: databases, caches, queues, and environments via API/CLI/portal.

### Phase 3: Portal & Documentation
1. Build or configure a developer portal (Backstage, Port, custom) as the single entry point for all platform services.
2. Maintain living documentation that updates automatically with infrastructure changes.
3. Implement platform observability: track adoption rates, template usage, and developer satisfaction scores.

## Verification & Quality Checklist
- [ ] New developer can deploy their first service within 30 minutes using golden path templates.
- [ ] Self-service provisioning requires zero manual tickets or Ops intervention.
- [ ] Platform templates include security, testing, and observability by default.
- [ ] DORA metrics tracked and reported monthly.

## Anti-Patterns & Constraints
- NEVER build a platform without continuous developer feedback loops.
- NEVER mandate platform adoption through policy alone; earn adoption through superior DX.
- NEVER create golden paths that are impossible to escape when teams have legitimate edge cases.
