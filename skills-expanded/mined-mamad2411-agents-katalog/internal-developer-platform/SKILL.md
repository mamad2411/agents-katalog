---
name: internal-developer-platform
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: internal developer platform, golden path design, developer portal architecture, service catalog platform, platform engineering, IDP design, backstage implementation, developer self-service, platform team scope, developer experience platform, service template, platform API design
---

# Skill — Internal Developer Platform

## When this skill activates

This skill activates when the user is designing, building, or evolving an Internal Developer Platform (IDP). This includes defining golden paths, building developer portals, creating service catalogs, implementing platform engineering practices, defining platform team scope, building self-service capabilities, and designing platform APIs for developer consumption.

## Mandatory actions when this skill is active

### Before writing any code

1. Map the current developer journey from idea to production, identifying friction points and toil hotspots.
2. Define the platform boundary: what belongs in the platform vs what belongs in application teams.
3. Identify the personas using the platform (backend devs, frontend devs, data engineers, SREs) and their distinct needs.
4. Assess existing tooling sprawl and identify consolidation opportunities (reduce tool count by 40-60% is typical).
5. Establish platform success metrics (time-to-first-deploy, cognitive load score, toil hours saved, adoption rate).

### During implementation

- **Golden Paths:** Create opinionated, paved roads for common tasks (new service, new API, new data pipeline). Each golden path should reduce a multi-day task to under 30 minutes. Include defaults that work for 80% of cases and escape hatches for the 20%.
- **Service Catalog:** Maintain a living registry of all services, APIs, data stores, and infrastructure with ownership, dependencies, and health status. Use Backstage, OpsLevel, or ServiceCatalog.io. Each entry must have: owner, on-call, docs, runbooks, and SLOs.
- **Developer Portal:** Single entry point for all platform capabilities. Include: service catalog, golden paths, documentation, status page, internal API marketplace, cost dashboard. Portal must be searchable and load in under 2 seconds.
- **Self-Service Capabilities:** Enable developers to provision environments, request resources, deploy services, configure monitoring, and manage secrets without filing tickets. Each self-service action should complete in under 5 minutes.
- **Platform APIs:** Design platform APIs as products. Use OpenAPI specs, provide SDKs, maintain changelogs, version properly. Platform APIs should have 99.9% uptime SLOs (higher than most application services).
- **Avoid Paving Cowpaths:** Don't automate broken processes. Simplify first, then automate. If a process requires 12 approval steps, fix the process before building the platform.
- **Platform as a Product:** Treat internal developers as customers. Collect feedback, measure satisfaction (NPS or CSAT), prioritize features by impact. Platform teams should spend 20% of time on user research.

### After implementation

- Verify each golden path reduces task time by at least 70% compared to manual execution.
- Confirm the service catalog is auto-populated and stays in sync with production reality (via discovery, not manual updates).
- Validate that the developer portal has search functionality and surfaces the most-used capabilities within 2 clicks.
- Ensure platform APIs have monitoring, alerting, and SLOs defined and tracked.
- Check that self-service actions have audit logs and cost attribution.

## Self-check before task completion

- [ ] Golden paths exist for the top 5 most common developer tasks.
- [ ] Service catalog includes all production services with ownership and dependencies.
- [ ] Developer portal is the single source of truth and loads in under 2 seconds.
- [ ] Platform success metrics are defined, instrumented, and tracked.
- [ ] Platform APIs have OpenAPI specs, SDKs, and 99.9% uptime SLOs.
- [ ] Self-service capabilities complete in under 5 minutes and include audit logs.
- [ ] Platform team spends 20% of time on user research and feedback collection.
