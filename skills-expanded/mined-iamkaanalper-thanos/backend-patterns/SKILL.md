---
name: backend-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When building or reviewing backend services, APIs, database layers, especially with backend-dev agent or in swarms with API tracks.
---

# Backend Patterns Skill (Grok Port)

Production-grade patterns for reliable, scalable, secure backends. Focus on patterns that prevent common pitfalls in real-world services.

## Core Architecture Patterns

### Layered Architecture (Controller -> Service -> Repository)
- Controllers handle HTTP, validation, auth.
- Services contain business logic, orchestration.
- Repos abstract data access (never leak DB specifics to services).

**Example (Node/Express):**
```ts
// controller.ts
app.post('/users', auth, async (req, res) => {
  const user = await userService.create(req.body);
  res.json(user);
});

// service.ts
async create(data: CreateUserDto) {
  // business rules, events, etc.
  return userRepo.create(data);
}
```

### API Design (REST + GraphQL hybrids)
- Consistent error shapes ( { error: { code, message, details } } ).
- Pagination: cursor-based for large sets.
- Versioning via headers or /v1/ (prefer headers for long-term).
- Rate limiting per user/key, with clear 429 + Retry-After.

### Database Optimization
- Index for query patterns, not just "add index later".
- N+1 prevention: joins, eager loading, or DataLoader for GraphQL.
- Transactions only when atomicity is required (use with care for perf).
- Read replicas for heavy read workloads.
- Soft deletes + audit columns for compliance.

### Error Handling & Resilience
- Never leak stack traces in prod responses.
- Circuit breakers for downstream services (use resilience4j or opossum).
- Idempotency keys for POSTs that must be safe to retry.
- Structured logging with correlation IDs (request-id).

### Security (tie to sast, gdpr)
- Input validation at boundary (zod, class-validator).
- Parameterized queries always.
- Secrets via env + vault, never hardcoded.
- CORS strict, no * in prod.
- Helmet, rate limit, slow down.

## Grok Integration (Production Contract)
- Primary for backend-dev agent.
- Fire on_db_change, on_infra_change, on_api_feature hooks.
- Pre-Flight: "Have we modeled the data access patterns? N+1 risk? Cost at scale?"
- Ledger for any DB migration or breaking API change.
- Handoff: include data model, query plans, failure modes, rollback plan.
- Friction + compound: every "this pattern caused outage" or "N+1 in prod" goes to compound for better defaults or linter rules.
- Palace: store "chose single-table for this domain because read patterns are X".
- Claim-verif: always read the actual query plan / schema before claiming "optimized".

## When to Activate
- Any new backend feature or refactor touching data/API.
- In swarm Phase 2/3 for backend tracks.
- Before deploys that touch DB or public APIs.
- When reviewing PRs with backend changes.

Use with api-patterns, security-review, test-enforcement.

These patterns come from years of production backend pain. Use them so the system stays fast, reliable, and maintainable.
