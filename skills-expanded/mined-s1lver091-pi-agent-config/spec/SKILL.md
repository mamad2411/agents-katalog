---
name: spec
description: Write a technical specification for a feature, API, or system component. Use when asked to spec out, design, or document a feature before it is built.
---

# Technical Specification

A spec exists to align everyone on what is being built before any code is written. It should be precise enough that two engineers would build the same thing after reading it.

## What to include

Work through each section. Skip a section only if it genuinely does not apply.

---

### Overview
One paragraph: what this feature is, why it exists, and who it is for.

### Goals
Bulleted list of what this spec achieves. Be specific.
- Good: "Users can reset their password via email within 10 minutes of the request"
- Bad: "Improve auth UX"

### Non-goals
What this spec explicitly does NOT cover. This prevents scope creep.

### Background
Context a new engineer would need: existing behavior, related systems, constraints, prior decisions and why they were made.

### Design

**Data model**
New fields, tables, or types. Use actual type notation.

```typescript
interface PasswordResetToken {
  id: string;
  userId: string;
  token: string;       // bcrypt hash of the raw token
  expiresAt: Date;
  usedAt: Date | null;
}
```

**API / Interface**
New endpoints, functions, or components. Include signatures and behavior contracts.

```
POST /auth/password-reset
Body: { email: string }
Response 200: {} (always, to avoid email enumeration)
Response 429: { retryAfter: number } (rate limited)
```

**Flow**
Step-by-step description of the happy path and the main error paths.

**State changes**
What persists, what is temporary, what gets deleted.

### Edge cases and error handling
Enumerate the cases that could go wrong and how each is handled.

| Case | Behavior |
|------|---------|
| Email not found | Return 200 silently (avoid enumeration) |
| Token expired | Return 400 with clear message |
| Token already used | Return 400 |
| Multiple requests | Invalidate previous tokens |

### Security considerations
Authentication, authorization, rate limiting, input validation, data exposure.

### Testing strategy
What needs to be tested and at what level (unit, integration, e2e).

### Open questions
Decisions that are not yet made. Name the tradeoffs and who should decide.

### Out of scope
Explicitly list related things this spec does not cover.
