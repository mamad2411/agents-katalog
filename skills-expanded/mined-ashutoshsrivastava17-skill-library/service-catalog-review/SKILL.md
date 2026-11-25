---
name: service-catalog-review
description: >
  Review and maintain service catalogs with ownership, dependencies, SLOs,
  runbooks, and operational metadata. Identify gaps in service documentation
  and operational readiness.
  TRIGGER when: user says /service-catalog-review, "service catalog",
  "service inventory", "service ownership", "catalog review", or asks
  to review or audit service documentation.
argument-hint: "[service or team scope]"
user-invocable: true
---

# Service Catalog Review

You are a platform engineering lead reviewing and maintaining a service catalog. A service catalog is the single source of truth for what services exist, who owns them, how they are operated, and how they relate to each other. Without it, incident response is slow, onboarding is painful, and technical debt hides in the dark.

---

## Process

### Step 1: Define Review Scope

Determine what is being reviewed and why:

| Parameter | Question | Example |
|-----------|----------|---------|
| **Scope** | Which services or teams are in scope? | All services owned by the Payments team |
| **Trigger** | Why is this review happening? | Quarterly audit, post-incident finding, new team onboarding |
| **Catalog tool** | Where is the catalog maintained? | Backstage, Cortex, OpsLevel, spreadsheet, Confluence |
| **Standards** | What is the expected completeness bar? | All Tier-1 services must have 100% of required fields |
| **Reviewers** | Who will validate the information? | Service owners, SRE team, engineering managers |
| **Deadline** | When must the review be complete? | End of quarter |

**Service tiering framework:**

| Tier | Definition | Completeness Requirement | Example |
|------|-----------|------------------------|---------|
| **Tier 1 — Critical** | Revenue-generating, customer-facing, no fallback | 100% of all fields required | Payment gateway, auth service |
| **Tier 2 — Important** | Internal-facing or has manual fallback | 90% of all fields required | Admin dashboard, reporting service |
| **Tier 3 — Supporting** | Batch, async, or development tooling | 75% of all fields required | Log aggregator, CI runner |
| **Tier 4 — Deprecated** | Scheduled for decommission | Deprecation plan only | Legacy monolith modules |

### Step 2: Audit Required Metadata Fields

For each service, verify the following fields are present and current:

| Category | Field | Description | Required Tier |
|----------|-------|-------------|---------------|
| **Ownership** | Team | Owning team name | All |
| **Ownership** | Primary on-call | Person or rotation | Tier 1-2 |
| **Ownership** | Escalation contact | Manager or secondary | Tier 1-2 |
| **Ownership** | Product owner | Business stakeholder | Tier 1-2 |
| **Technical** | Language / framework | Tech stack | All |
| **Technical** | Repository | Link to source code | All |
| **Technical** | Architecture diagram | System context diagram | Tier 1-2 |
| **Technical** | API documentation | Endpoint reference | Tier 1-3 |
| **Operational** | Runbook | Link to operational runbook | Tier 1-2 |
| **Operational** | SLO definitions | Availability, latency targets | Tier 1-2 |
| **Operational** | Monitoring dashboard | Link to Grafana/Datadog dashboard | Tier 1-2 |
| **Operational** | Alerting rules | Link to alert definitions | Tier 1-2 |
| **Operational** | Deployment pipeline | CI/CD pipeline link | All |
| **Operational** | Deployment frequency | How often it deploys | Tier 1-2 |
| **Dependencies** | Upstream services | Services that call this service | All |
| **Dependencies** | Downstream services | Services this calls | All |
| **Dependencies** | Data stores | Databases, caches, queues | All |
| **Dependencies** | External dependencies | Third-party APIs, SaaS tools | Tier 1-2 |
| **Compliance** | Data classification | PII, financial, public | Tier 1-2 |
| **Compliance** | Last security review | Date of most recent review | Tier 1-2 |
| **Lifecycle** | Status | Active, deprecated, planned | All |
| **Lifecycle** | Last updated | Date catalog entry was verified | All |

### Step 3: Identify Gaps and Score Services

Score each service on catalog completeness:

| Score | Label | Criteria |
|-------|-------|----------|
| **A (90-100%)** | Fully documented | All required fields populated and verified current |
| **B (70-89%)** | Mostly documented | Minor gaps in non-critical fields |
| **C (50-69%)** | Partially documented | Missing operational fields (runbook, SLOs, dashboards) |
| **D (< 50%)** | Undocumented | Major gaps — ownership unclear, no runbook, no monitoring |

**Common gap patterns:**

| Gap Pattern | Risk | Typical Cause |
|-------------|------|---------------|
| No runbook | Slow incident response | "We will write it later" |
| No SLO defined | Cannot measure reliability | SLOs never prioritized |
| Stale ownership | Alerts go to wrong team | Team reorgs, attrition |
| Missing dependencies | Cascading failure surprise | Dependencies added informally |
| No architecture diagram | Slow onboarding, misunderstandings | Diagram never created or outdated |
| No data classification | Compliance risk | Security review skipped |

### Step 4: Validate Dependencies

Cross-check dependency information:

| Validation | Method | What to Look For |
|-----------|--------|-----------------|
| **Upstream accuracy** | Compare catalog to actual traffic (service mesh, API gateway logs) | Services calling this one not listed in catalog |
| **Downstream accuracy** | Compare catalog to outbound connection logs | Services this calls that are not listed |
| **Circular dependencies** | Graph analysis of dependency map | A -> B -> C -> A cycles |
| **Single points of failure** | Identify services with no redundancy that many services depend on | Shared database, single auth service |
| **Orphaned services** | Services with no upstream callers | May be candidates for decommission |
| **Shadow dependencies** | Services calling each other through shared databases or queues | Not visible in API-level dependency maps |

### Step 5: Generate the Review Report

Compile findings into an actionable report:

| Section | Content |
|---------|---------|
| **Summary** | Overall catalog health score; number of services reviewed; top-line findings |
| **Service scorecards** | Per-service completeness score with gap details |
| **Dependency map** | Visual or tabular view of service relationships |
| **Gap analysis** | Categorized list of missing metadata with risk assessment |
| **Ownership issues** | Services with unclear, stale, or missing ownership |
| **Action items** | Prioritized remediation tasks with owners and deadlines |
| **Trends** | Comparison to previous review (if available) |

### Step 6: Create Remediation Plan

| Priority | Gap Type | Action | Owner | Deadline |
|----------|----------|--------|-------|----------|
| **P0** | No owner assigned | Assign ownership immediately | Engineering manager | 1 week |
| **P0** | No runbook for Tier-1 service | Write runbook | Service team | 2 weeks |
| **P1** | No SLO defined | Define and instrument SLOs | Service team + SRE | 1 month |
| **P1** | Stale dependency map | Update from traffic data | Platform team | 2 weeks |
| **P2** | Missing architecture diagram | Create or update diagram | Service team | 1 month |
| **P2** | No data classification | Complete security questionnaire | Service team + Security | 1 month |
| **P3** | Missing API documentation | Generate from code or write manually | Service team | 1 quarter |

---

## Output Format

```markdown
# Service Catalog Review — [Team / Scope] — [Date]

## Executive Summary
- **Services reviewed:** [count]
- **Overall health score:** [A/B/C/D] ([percentage]%)
- **Critical gaps found:** [count]
- **Top finding:** [one sentence]

## Service Scorecards

| Service | Tier | Owner | Score | Critical Gaps |
|---------|------|-------|-------|--------------|
| ...     | ...  | ...   | ...   | ...          |

## Dependency Map
[Table or diagram of service relationships]

## Gap Analysis

### Ownership Gaps
| Service | Issue | Recommended Owner |
|---------|-------|-------------------|
| ...     | ...   | ...               |

### Operational Gaps
| Service | Missing Field | Risk | Priority |
|---------|--------------|------|----------|
| ...     | ...          | ...  | ...      |

## Remediation Plan
| Priority | Action | Owner | Deadline |
|----------|--------|-------|----------|
| ...      | ...    | ...   | ...      |

## Recommendations
- [Prioritized list of systemic improvements]
```

---

## Quality Checklist

- [ ] Every in-scope service has been reviewed, not just the well-known ones
- [ ] Service tiers are assigned based on business impact, not team preference
- [ ] Ownership fields reflect current team structure, not historical
- [ ] Dependencies are validated against actual traffic data, not just documentation
- [ ] SLO definitions exist for all Tier-1 and Tier-2 services
- [ ] Runbooks exist and have been verified as current for all Tier-1 services
- [ ] Orphaned and deprecated services are identified with decommission plans
- [ ] Data classification is completed for services handling PII or financial data
- [ ] Action items have specific owners and deadlines, not "the team"
- [ ] Review date is recorded so the next review can measure progress

---

## Edge Cases

| Scenario | Handling Approach |
|----------|-------------------|
| **Shared service with no clear owner** | Assign a single owning team. If truly shared, create a platform team or assign to the team with the most usage. Shared ownership is no ownership. |
| **Service exists but no one knows what it does** | Check traffic logs. If it receives traffic, investigate. If it does not, schedule for decommission with a grace period and monitoring. |
| **Microservices sprawl (100+ services)** | Focus the review on Tier-1 and Tier-2 first. Use automated tooling (Backstage, Cortex) to enforce catalog completeness. |
| **Team refuses to update their catalog entries** | Escalate to engineering leadership. Tie catalog completeness to operational readiness reviews and deploy gates. |
| **Catalog tool migration in progress** | Review the current source of truth. Document the migration plan. Do not let the migration be an excuse for stale data. |
| **Acquisitions bringing in unknown services** | Treat acquired services as Tier-unknown until classified. Run a discovery exercise before integrating into the main catalog. |
| **Services running in shadow IT or personal accounts** | Flag as critical risk. Migrate to official infrastructure. Update catalog with the service even before migration. |
