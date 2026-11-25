---
name: api-principles
description: |
  Apply and review adherence to our API engineering principles when designing, building, or
  reviewing APIs. Always use this skill for API endpoint design, contract or schema reviews,
  security and access control checks, versioning and backwards compatibility, integration
  boundary validation, and observability. Use it even when the user doesn't explicitly ask for
  a principle-based review — any API design discussion, code review touching an API layer, or
  architecture conversation involving service boundaries should be grounded in these principles.
  Covers: API design, API-as-product, backwards compatibility, consumer experience, security,
  observability, type consistency, boundary validation, and efficiency.
metadata:
  category: API
  version: "1.0.0"
  source: principles
---

# API Principles

Our API engineering principles for designing, building, and reviewing APIs as first-class products.
These principles apply to all APIs — internal, experience-facing, and public.

## When to Apply

Apply this skill when:
- Designing or reviewing API endpoints, contracts, or schemas
- Reviewing API code for security, access control, or input validation
- Managing API versioning, deprecation, or breaking changes
- Checking observability and logging at integration boundaries
- Reviewing integration boundary resilience (timeouts, retries, circuit breakers)
- Evaluating API consistency, naming conventions, or error shapes
- Assessing whether an API is designed for its consumers

## Principles Overview

| Principle | Coverage | Reference |
|-----------|----------|-----------|
| APIs are the Product | Full guidance | `principles/apis-are-the-product.md` |
| Abstract the Architecture | Full guidance | `principles/abstract-the-architecture.md` |
| Design for Autonomous Consumers | Full guidance | `principles/design-for-autonomous-consumers.md` |
| One Definition, Zero Drift | Full guidance | `principles/one-definition-zero-drift.md` |
| Secure by Construction | Full guidance | `principles/secure-by-construction.md` |
| Validate at the Boundary | Full guidance | `principles/validate-at-the-boundary.md` |
| Observable by Default | Full guidance | `principles/observable-by-default.md` |
| Change Without Breaking | Full guidance | `principles/change-without-breaking.md` |
| Efficient by Design | Full guidance | `principles/efficient-by-design.md` |

## Quick Review Checklist

Use this for a fast adherence scan. Load individual principle files for detailed guidance.

### APIs are the Product
- [ ] Each API has documented consumers, a clear contract, and a named owner
- [ ] API design is consistent with the wider ecosystem and not surprising to new consumers

### Abstract the Architecture
- [ ] The API hides business complexity — consumers cannot infer internal structure from the interface
- [ ] Internal service names, infrastructure identifiers, or provider details do not appear in payloads or errors

### Design for Autonomous Consumers
- [ ] A new consumer can integrate using only the contract and documentation, without bespoke guidance
- [ ] The API is unambiguous enough for automated clients to use correctly

### One Definition, Zero Drift
- [ ] Types, validation, and spec are generated or derived from the same schema
- [ ] The published specification matches production behaviour

### Secure by Construction
- [ ] Access control is explicit, scoped, and least-privilege by default
- [ ] Sensitive fields are protected — not leaking via responses or logs

### Validate at the Boundary
- [ ] All integration boundaries validate incoming data and detect breaking changes
- [ ] Resilience controls exist and are exercised (timeouts, retries, circuit breakers)

### Observable by Default
- [ ] A single request can be followed end-to-end using correlation IDs and distributed tracing
- [ ] SLOs exist per API with alerts aligned to them

### Change Without Breaking
- [ ] Every API version has documented status and lifecycle dates, including a deprecation plan
- [ ] Breaking changes are delivered only through new versions with clear upgrade guidance

### Efficient by Design
- [ ] Performance targets are documented and validated with measurements
- [ ] Resource usage is monitored in production with alerts on key regressions

## How to Use

Load the relevant principle file when you need detailed guidance:

```
principles/apis-are-the-product.md            — when designing API contracts or reviewing consumer experience
principles/abstract-the-architecture.md       — when checking if API exposes internal implementation details
principles/design-for-autonomous-consumers.md — when evaluating API usability and self-service capability
principles/one-definition-zero-drift.md       — when checking type consistency and schema alignment
principles/secure-by-construction.md          — when reviewing security, auth, or access control
principles/validate-at-the-boundary.md        — when checking boundary validation and resilience patterns
principles/observable-by-default.md           — when reviewing logging, metrics, tracing, SLOs, or alerting strategy
principles/change-without-breaking.md         — when managing versioning, deprecation, or breaking changes
principles/efficient-by-design.md             — when reviewing API performance and resource efficiency
```

## Gotchas

- **Change Without Breaking applies to public and internal APIs only — not experience APIs.** Experience APIs (BFF/consumer-specific layer) are exempt from versioning and deprecation requirements because they are owned end-to-end by a single team.

## Process Reminders

These Tier 2 principles require human action and cannot be verified automatically:

> **Named ownership** — Every API must have a named owner responsible for quality, uptime, support, and evolution. Assign ownership before launch, not as a backlog item.

> **Deprecation as a managed process** — Deprecation requires timelines, direct consumer communication, migration guidance, and confirmation of zero traffic before removal. A `Sunset` header alone is not a deprecation plan.
