---
name: code-explanation
description: Use this skill when writing code comments, explaining code decisions, documenting the "why" behind implementation choices, or narrating technical reasoning in PRs or architecture docs. Trigger on keywords: explain this code, why did you write it this way, add comments, document this, write inline comments, explain my decision.
---

# Code Explanation

## Core Principle

**Comments explain WHY. Code explains WHAT.**

If you need a comment to explain what the code does, the code should be cleaner. If you need a comment to explain why it's done this way — write that comment.

---

## The Four Levels of Code Explanation

| Level | Where | Explains |
|---|---|---|
| Inline comment | Next to specific line | Non-obvious logic or gotcha |
| Function docstring | Top of function | What it does, parameters, returns, side effects |
| Module header | Top of file | What this module is responsible for |
| Architecture note | README / ADR | Why this approach was chosen over alternatives |

---

## What to Comment (and What Not To)

### Comment This
```typescript
// Using exponential backoff here because the payment API 
// has a 429 rate limit that triggers on burst traffic
await retryWithBackoff(() => paymentAPI.charge(amount))

// Intentionally not validating here — validation happens 
// upstream in the middleware layer (see auth.middleware.ts)
const user = req.user

// This looks backwards but the API returns results 
// in reverse chronological order — newest = index 0
const latest = results[0]
```

### Don't Comment This
```typescript
// Increment counter by 1
count++

// Check if user is authenticated
if (user.isAuthenticated) {
```

---

## Docstring Template

```typescript
/**
 * Calculates the discount amount for a given order.
 * 
 * @param order - The order to calculate discount for
 * @param promoCode - Optional promo code to apply
 * @returns The discount amount in cents, or 0 if no discount applies
 * @throws InvalidPromoCodeError if the promo code format is invalid
 * 
 * Note: Does NOT check if the promo code is active — 
 * call validatePromoCode() first.
 */
```

---

## PR Description: Explaining Your Decisions

When your PR makes non-obvious decisions, explain them:

```markdown
## Technical Decisions

**Why I chose X over Y:**
[reasoning — constraints, trade-offs, what you considered]

**Known limitations:**
[what this doesn't handle and why that's acceptable for now]

**What I'd do differently with more time:**
[honest reflection — shows growth mindset]
```

---

## Architecture Decision Records (ADR)

For significant technical decisions, write a short ADR:

```markdown
# ADR: [decision title]

**Date:** [date]  
**Status:** Accepted

## Context
[What situation led to this decision?]

## Decision
[What did we decide to do?]

## Reasoning
[Why this over the alternatives?]

## Trade-offs
[What do we give up with this choice?]

## Consequences
[What becomes easier? What becomes harder?]
```

Store in `/docs/decisions/` or similar — these are gold for future developers.
