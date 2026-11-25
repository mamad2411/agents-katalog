---
name: design-documents
description: Formal RFC/design doc template for significant engineering changes. Covers context, goals, non-goals, proposed solution, alternatives considered, data model changes, API changes with backward compatibility analysis, security considerations, performance implications, rollout plan, rollback plan, second-order effects, open questions, and timeline.
invoke_when: Use when a change exceeds 500 lines of code, introducing a new service, adding a new database table, adopting a new external dependency, making a significant architectural decision, or changing API contracts in a breaking way.
---

# Design Documents

## Core Principle

Design documents are a tool for thinking, not just documentation. Writing a design doc forces you to think through edge cases, alternatives, and second-order effects before writing code. The primary audience is your future self and your teammates who will maintain this system.

---

## When to Write a Design Doc

A design doc is **required** when any of these conditions are met:

| Trigger | Why |
|---|---|
| Change exceeds **500 lines of code** | Large changes need upfront design to avoid expensive rework. |
| Introduces a **new service or major module** | New services create operational burden that must be justified. |
| Adds a **new database table or significant schema change** | Schema changes are hard to undo and affect many consumers. |
| Adopts a **new external dependency or third-party service** | External dependencies add risk, cost, and maintenance burden. |
| Changes **API contracts** in a breaking way | Breaking API changes affect consumers and require migration plans. |
| Makes a **significant architectural decision** affecting multiple teams | Cross-cutting decisions need visibility and buy-in. |
| Introduces a **new data flow** between services | Data flows create coupling and consistency challenges. |

**When NOT to write a design doc:** Bug fixes, refactoring within a module (< 500 LOC), adding a feature that follows an established pattern, updating dependencies, or routine operational work. For these, a thorough PR description is sufficient.

---

## Design Document Template

```markdown
# Design: [Feature/System Name]

## Metadata

- **Author:** [Name]
- **Status:** Draft | In Review | Approved | Rejected | Superseded
- **Date:** YYYY-MM-DD
- **Reviewers:** [Names -- include at least one person from each affected team]
- **Approvers:** [Names -- who must approve before implementation begins]
- **Last Updated:** YYYY-MM-DD

---

## Context & Problem Statement

[What problem are we solving? Why is it a problem? Why now?
Include data that demonstrates the problem:
- Metrics showing the current pain (error rates, latency, support tickets).
- Business context (customer complaints, revenue impact, competitive pressure).
- What happens if we do nothing?

Be specific. "The system is slow" is not a problem statement.
"The product search API has a p99 latency of 4.2 seconds, causing a 15% cart
abandonment rate on mobile devices" is a problem statement.]

---

## Goals

[What must this solution achieve? Be specific and measurable.]

1. Reduce product search p99 latency to < 500ms.
2. Support 10,000 concurrent search queries.
3. Maintain backward compatibility with the existing search API.

---

## Non-Goals

[What is explicitly out of scope? This prevents scope creep and sets expectations.
Non-goals are features or improvements that are related but will NOT be addressed
by this design.]

1. Redesigning the search UI (separate project).
2. Supporting fuzzy/typo-tolerant search (future iteration).
3. Real-time index updates (batch updates within 5 minutes are acceptable).

---

## Proposed Solution

[Detailed description of what you will build. Include:]

### Architecture Overview

[Diagram showing components, data flows, and interactions.
Use ASCII diagrams or reference an attached image.]

```
[Client] --> [API Gateway] --> [Search Service] --> [Elasticsearch]
                                     |
                              [Product Service] --> [PostgreSQL]
```

### How It Works

[Step-by-step description of the solution. Be specific enough that another
engineer could implement it from this description.]

1. [Step 1: ...]
2. [Step 2: ...]
3. [Step 3: ...]

### Key Design Decisions

[For each significant choice, explain what you chose and why.]

- **Why Elasticsearch over Algolia:** Self-hosted gives us control over ranking
  algorithms and avoids per-query pricing at our scale (2M queries/day).
- **Why batch indexing over real-time:** Simplifies consistency model and reduces
  infrastructure complexity. 5-minute delay is acceptable per product team.

---

## Alternatives Considered

[At least 2 alternatives. For each: describe the approach, list pros and cons,
and explain why it was rejected. This demonstrates that the proposed solution
is not the first idea that came to mind.]

### Alternative A: [Name]

**Description:** [What this approach would look like.]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Why rejected:** [Specific reason this approach was not chosen.]

### Alternative B: [Name]

**Description:** [What this approach would look like.]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Why rejected:** [Specific reason this approach was not chosen.]

---

## Data Model Changes

[New tables, columns, indexes. Include the actual schema.
For existing tables, show the before and after.]

### New Tables

```sql
CREATE TABLE search_index_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending, running, completed, failed
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    records_processed INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_search_index_jobs_status ON search_index_jobs(status);
```

### Modified Tables

```sql
-- Before
-- products table has no full_text_search column

-- After
ALTER TABLE products ADD COLUMN search_vector tsvector;
CREATE INDEX idx_products_search ON products USING gin(search_vector);
```

### Migration Strategy

[How will the schema change be applied? Expand-contract? Backfill?
See the migration-strategies skill for guidance.]

---

## API Changes

[New or modified endpoints. Include request/response examples.]

### New Endpoints

```
POST /v1/search
Content-Type: application/json

Request:
{
  "query": "wireless headphones",
  "filters": {
    "category": "electronics",
    "price_min": 50,
    "price_max": 200
  },
  "page": 1,
  "page_size": 20
}

Response (200 OK):
{
  "results": [
    {
      "id": "prod_123",
      "name": "Wireless Headphones Pro",
      "price": 149.99,
      "relevance_score": 0.95
    }
  ],
  "total": 342,
  "page": 1,
  "page_size": 20
}
```

### Backward Compatibility Analysis

[Will existing consumers break? If so, what is the migration plan?
Reference the api-backward-compatibility skill.]

- The existing `GET /v1/products?search=` endpoint will continue to work.
- The new `POST /v1/search` endpoint is additive -- no existing consumers are affected.
- In Phase 2 (3 months after launch), the old search will be deprecated with
  a 6-month sunset period.

---

## Security Considerations

[What new attack surface does this create? Reference the threat-modeling skill.]

- The search endpoint is public and must have rate limiting (100 req/min per API key).
- Search queries must be sanitized to prevent Elasticsearch injection.
- Search results must respect authorization -- users should only see products
  they have access to.
- The Elasticsearch cluster is on a private subnet, not accessible from the internet.

---

## Performance Implications

[Expected load, query patterns, resource requirements.]

- **Expected load:** 2M search queries/day (peak: 500 req/s).
- **Latency target:** p99 < 500ms.
- **Resource requirements:** 3-node Elasticsearch cluster (16GB RAM each).
- **Indexing load:** Full reindex runs nightly (2M products, ~30 minutes).
  Incremental updates every 5 minutes.
- **Caching strategy:** Popular queries cached in Redis with 5-minute TTL.

---

## Rollout Plan

[How will this be deployed? Include milestones and go/no-go criteria.]

| Phase | What | Duration | Go/No-Go Criteria |
|---|---|---|---|
| 1 | Deploy search infrastructure (Elasticsearch cluster) | Week 1 | Cluster healthy, replication working |
| 2 | Shadow traffic: run new search in parallel, compare results | Week 2-3 | Result quality >= existing search |
| 3 | 5% traffic to new search via feature flag | Week 4 | p99 < 500ms, error rate < 0.1% |
| 4 | 50% traffic | Week 5 | Same criteria, no user complaints |
| 5 | 100% traffic | Week 6 | Same criteria |
| 6 | Deprecate old search endpoint | Week 12+ | All consumers migrated |

---

## Rollback Plan

[How to undo if it goes wrong. Specific steps, not "we will figure it out."]

1. Toggle the `new_search_engine` feature flag to OFF. All traffic reverts to the
   existing search within 60 seconds.
2. If the Elasticsearch cluster is unhealthy, the circuit breaker will automatically
   fall back to the PostgreSQL-based search.
3. If data corruption is detected in the search index, delete and rebuild the index
   from the PostgreSQL source of truth (takes ~30 minutes).

---

## Second-Order Effects

[What else does this change affect? Think beyond the immediate feature.]

- **Other teams:** The analytics team currently queries the products table for search
  analytics. They will need to consume search events from the new system instead.
- **Data pipelines:** The nightly product export job may conflict with the search
  indexing job. Schedule them at different times.
- **Monitoring:** New dashboards needed for Elasticsearch cluster health, search
  latency, and indexing lag.
- **On-call burden:** On-call engineers need to learn basic Elasticsearch operations.
  Add a runbook section.
- **Cost:** Elasticsearch cluster costs ~$500/month. Approved by [manager name].
- **Future flexibility:** This design supports adding typo-tolerant search, faceted
  search, and personalized ranking in future iterations without architectural changes.

---

## Open Questions

[What is still unresolved? Who needs to answer? Set a deadline.]

| Question | Owner | Deadline | Resolution |
|---|---|---|---|
| Should we use Elasticsearch managed service or self-hosted? | @infra-team | 2025-07-01 | [TBD] |
| What relevance ranking algorithm should we use? | @search-team | 2025-07-05 | [TBD] |
| Do we need search-as-you-type (typeahead)? | @product-team | 2025-07-01 | [TBD] |

---

## Timeline

[Rough estimate. Not a commitment, but a sense of scale.
Break into phases with effort estimates.]

| Phase | Effort | Calendar Time |
|---|---|---|
| Infrastructure setup | 3 days | Week 1 |
| Search indexing pipeline | 5 days | Week 2 |
| Search API implementation | 5 days | Week 3 |
| Testing and shadow traffic | 5 days | Week 4 |
| Gradual rollout | 2 weeks | Week 5-6 |
| **Total** | **~4 weeks engineering** | **~6 weeks calendar** |
```

---

## Review Process

### Before Review

1. Author writes the design doc and self-reviews (wait 24 hours and re-read).
2. Author identifies reviewers: at least one from each affected team, plus a senior engineer for architectural oversight.

### During Review

3. Reviewers provide feedback within 3 business days.
4. Focus review feedback on:
   - **Feasibility:** Can this actually be built as described?
   - **Risks:** What could go wrong that the author has not considered?
   - **Alternatives:** Are the rejected alternatives truly inferior?
   - **Completeness:** Are the rollback plan, security considerations, and second-order effects thorough?
5. Do not bikeshed on naming or minor details. Focus on the architecture.

### After Review

6. Author addresses all feedback (accept, reject with justification, or discuss).
7. Doc moves to "Approved" when all approvers sign off.
8. Implementation begins only after approval.
9. If the design changes significantly during implementation, update the doc.

---

## After Implementation

Update the design doc with a retrospective section:

```markdown
## Retrospective (added YYYY-MM-DD)

**What actually happened vs. what was planned:**
- Timeline was 8 weeks instead of 6 (Elasticsearch tuning took longer than expected).
- We chose managed Elasticsearch (resolved open question).
- Search quality exceeded expectations -- p99 came in at 180ms vs. 500ms target.

**What would we do differently:**
- Start with managed service from day one instead of debating self-hosted.
- Include load testing in the timeline estimate.

**Decisions that held up well:**
- Batch indexing was the right choice. Real-time was not needed.
- Feature flag rollout caught a ranking bug at 5% traffic.
```

---

## Checklist for Design Doc Authors

- [ ] Problem statement is specific, measurable, and includes data.
- [ ] Goals are measurable and non-goals are explicit.
- [ ] At least 2 alternatives are described with clear rejection reasoning.
- [ ] Data model changes include actual schema (SQL or equivalent).
- [ ] API changes include request/response examples and backward compatibility analysis.
- [ ] Security considerations reference the STRIDE framework.
- [ ] Performance implications include expected load and resource requirements.
- [ ] Rollout plan has phases with go/no-go criteria at each stage.
- [ ] Rollback plan has specific steps (not "we will figure it out").
- [ ] Second-order effects cover other teams, pipelines, monitoring, cost, and on-call.
- [ ] Open questions have owners and deadlines.
- [ ] Timeline is broken into phases with effort estimates.
- [ ] Reviewers from all affected teams are identified.
