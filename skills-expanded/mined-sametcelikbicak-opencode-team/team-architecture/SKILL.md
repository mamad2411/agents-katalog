---
name: team-architecture
description: Technical architecture design methodology. Data model, API contract, module boundaries, technology selection rationale, scalability. The playbook of the architect role.
---

# Technical Architecture Design

## Core principle: the smallest working architecture

In an MVP, the architecture is the simplest structure that gets the job done. Every layer, every service, every abstraction must be a **proven need**.

Question: "What would happen without this?" → If the answer is "nothing would happen", delete that layer.

## 1. Technology selections

A table for each selection:

| Selection | Rationale | Alternative | Why the alternative was rejected |
|---|---|---|---|
| PostgreSQL | relational integrity, flexibility with JSONB | MongoDB | schema is less explicit, queries are not relational |

The rationale must come from **the project context**: "it will run on a single server, there will be 5 users, relational data integrity is essential". "Most popular" is not a rationale.

List only the selections that **require a decision**. Do not write decisions like the language choice, the editor, formatters.

## 2. Data model

- Entities, fields (type + requiredness + default), relationships, constraints
- For each table: delete behavior (cascade or restrict)
- **Enums**: free text or a controlled list?
- **Time**: UTC or local? Timestamp format?
- **Money**: decimal, or integer cents? Which currency, and how is currency conversion handled?
- **Schema history**: backward compatible from the first version? If not, a migration + rollback plan is mandatory

Identity: UUID or auto-incrementing integer? Use UUID if there is a privacy requirement.

## 3. API contract

For each endpoint:

| Method | Path | Body | Response | Errors | Authentication |
|---|---|---|---|---|---|

Rules:
- Resources use plural naming (`/invoices`, `/users`)
- The response envelope should be consistent (the same shape in every response)
- Pagination, sorting and filtering semantics should be defined
- Standard error body: `{ error: { code, message, details? } }` — `message` is shown to the user, `details` is logged
- **Idempotency**: is a repeated POST safe? If not, `Idempotency-Key` support is required
- Versioning: a `/v1` path or a header? What is the breaking change policy?

Show an example request/response for one endpoint. The contract is where the frontend will work from — leave no ambiguity.

## 4. Module boundaries

```
domain/     → business rules, framework independent
application/→ use cases, calls the domain
adapters/   → framework, DB, HTTP
```

The dependency direction must be **inward**: `adapters → application → domain`. The domain does not depend on anything outside itself.

Write a one-sentence responsibility for each module. If a module has a two-sentence responsibility, it should be split.

## 5. Scalability

When does it become a problem? Give concrete thresholds:

| Resource | Today | Problem threshold | Mitigation |
|---|---|---|---|
| DB connections | 5 | 50+ concurrent | connection pool |
| Single server CPU | 10% | 70% | horizontal scaling |
| File storage | 2 GB | 50 GB | CDN |

Write a mitigation **only** if the threshold is genuinely close. Hypothetical scale-out design is the most common waste in an MVP.

## 6. Security boundaries

- Where is the authentication boundary? (session, token, OAuth provider)
- Authorization model: role, resource ownership, or both?
- Where do secrets live, who can access them, and how are they rotated?
- Which data is personal data, and which regulation applies (KVKK, GDPR)?

## 7. Risks

| Risk | Impact | Early signal | Mitigation |
|---|---|---|---|

## Common mistakes

| Mistake | The right way |
|---|---|
| Extracting microservices | Monolith + clean module boundaries |
| "It might change in the future" abstraction | No abstract class without a concrete need |
| Listing technologies without writing a decision | A rationale for every selection |
| A schema change without a rollback plan | A rollback plan is mandatory |
| Solving a scale problem that does not exist | Write a concrete threshold |

## Output format

Markdown. Sections: Overview / Technology selections / Data model / API contract / Module boundaries / Scalability / Security boundaries / Risks.

Explanations in the user's language (Turkish or English), schema/SQL/type definitions in English.
