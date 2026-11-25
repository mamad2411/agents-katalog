# Documentation and ADRs

## Description
Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.

## Core Philosophy: Document the Why, Not the What

Code already tells you *what* it does. Documentation should tell you:
- **Why** was this approach chosen over alternatives?
- **What** was considered and rejected?
- **What** are the known trade-offs?
- **What** will break if you change this?

## Documentation Types

### 1. Architecture Decision Records (ADRs)
Capture significant architectural decisions with context, alternatives, and consequences.

### 2. API Documentation
Consumer-facing docs that explain how to use interfaces correctly.

### 3. Inline Documentation
Code-level docs that explain non-obvious behavior, invariants, and edge cases.

## ADR Format

Every ADR follows this 7-section template:

```markdown
# ADR-[NUMBER]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the problem we are solving? What forces are at play?
What constraints do we have? What is the background?

Include:
- Business drivers
- Technical constraints
- Team context
- Timeline considerations
- Related decisions]

## Decision
[What did we decide? State the decision clearly and concisely.

We will use [technology/approach] to solve [problem] because [reason].]

## Consequences
[What are the trade-offs? What becomes easier? What becomes harder?

Positive:
- [Benefit 1]
- [Benefit 2]

Negative:
- [Cost 1]
- [Cost 2]

Neutral:
- [Change in process/team/operations]
]

## Alternatives Considered
[What other options did we evaluate? Why were they rejected?

### Alternative 1: [Name]
- Pros: ...
- Cons: ...
- Rejected because: ...

### Alternative 2: [Name]
- Pros: ...
- Cons: ...
- Rejected because: ...
]

## Implementation Plan
[How will we implement this decision?
- Phase 1: ...
- Phase 2: ...
- Phase 3: ...
]

## Notes
[References, links, related ADRs, follow-up tasks.
- Related: ADR-012, ADR-015
- Supersedes: ADR-008
]
```

### ADR Naming Convention
`ADR-001-decision-title.md` (padded numbers, kebab-case title)

### ADR Location
`docs/adr/` at project root

### When to Write an ADR
- Adding a new dependency or framework
- Changing database or storage layer
- Changing API design or protocol
- Changing deployment infrastructure
- Changing team workflow or processes
- Any decision with significant, hard-to-reverse consequences

## Documentation Maturity Model

| Level | Name | Characteristics |
|-------|------|-----------------|
| 0 | None | No documentation. Tribal knowledge only. |
| 1 | Minimal | README exists. Some inline comments. |
| 2 | Reactive | ADRs for major decisions. API docs exist. Docs updated when asked. |
| 3 | Proactive | ADRs for all decisions. Docs written before code. Doc review in PRs. |
| 4 | Living | Docs auto-generated. Diagrams as code. Docs tested in CI. |
| 5 | Self-documenting | Clear code reduces need for external docs. System enforces documented patterns. |

Target: Level 3 for most projects. Level 4 for critical infrastructure.

## Doc Review Process

### For ADRs
1. Author drafts ADR
2. Team reviews in ADR review meeting (or async PR)
3. At least one senior engineer approves
4. ADR is merged and numbered
5. ADR is referenced in code comments and other docs

### For API Documentation
1. Docs are part of the PR that implements the API
2. Changes to public API must include doc changes
3. Docs are reviewed for accuracy, clarity, completeness
4. Examples are tested (in CI, if possible)
5. Breaking changes include migration guide

### For Inline Documentation
1. Document why, not what
2. Document invariants and assumptions
3. Document non-obvious behavior and edge cases
4. Keep comments close to the code they describe
5. Remove commented-out code (not documentation)

## Inline Documentation Standards

### TypeScript / JavaScript
```typescript
/**
 * Processes the payment for an order.
 *
 * This handles both credit card and digital wallet payments.
 * For international transactions, currency conversion is applied
 * using the daily exchange rate cached in Redis.
 *
 * @param order - The order to process (must have valid payment details)
 * @returns Payment result with transaction ID
 * @throws {PaymentError} If payment gateway is unreachable or declines
 *
 * @remarks
 * This function is called from the checkout flow only.
 * Do NOT call from admin order-edit flows (use reprocessPayment instead).
 * Idempotency key is generated from order.id + payment.attempt.
 */
```

### Python
```python
def process_payment(order: Order) -> PaymentResult:
    """
    Processes payment for an order.

    Handles credit card and digital wallet payments.
    International transactions use daily exchange rate from Redis cache.

    Args:
        order: The order to process (must have valid payment details)

    Returns:
        Payment result with transaction ID

    Raises:
        PaymentError: If payment gateway unreachable or declines

    Note:
        Called only from checkout flow, not admin edit flows.
        Idempotency key = f"{order.id}:{payment.attempt}"
    """
```

### Rust
```rust
/// Processes payment for an order.
///
/// Handles credit card and digital wallet payments.
/// International transactions use daily exchange rate from Redis cache.
///
/// # Arguments
/// * `order` - Must have valid payment details
///
/// # Returns
/// Payment result with transaction ID
///
/// # Errors
/// Returns `PaymentError` if gateway unreachable or declines
///
/// # Safety
/// This function is called from checkout flow only.
/// Not safe to call from admin edit flows.
```

## API Documentation Template

```markdown
## [Endpoint Name]

`[METHOD] /api/[path]`

### Description
[What does this endpoint do? When should it be called?]

### Request
```json
[Request body schema with examples]
```

### Response
```json
[Response body schema with examples]
```

### Errors
| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 400 | Invalid request body |
| 401 | Authentication required |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 429 | Rate limited |
| 500 | Internal server error |

### Examples
[curl or code examples for common use cases]

### Notes
[Idempotency, rate limits, pagination, caching behavior]
```

## Usage
Load this skill when documenting architectural decisions, creating API documentation, or reviewing inline docs. Use the ADR template for significant decisions, maintain doc maturity at Level 3+, and enforce documentation reviews in PRs.
