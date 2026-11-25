---
name: pii-detection
description: Detect and flag PII (emails, SSNs, credit cards, phone numbers) in code, test fixtures, and logs. Enforce masking before logging and GDPR/CCPA-aware data handling.
invoke_when: Use when writing or reviewing code that handles user data, creating test fixtures, building logging/observability, or working with strings that may contain personal information (PII).
---

# PII Detection

## PII Patterns to Flag

Any of these in source code, test fixtures, config files, or seed data is a finding:

| Type | Pattern | Example |
|------|---------|---------|
| Email | `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b` | `john.doe@company.com` |
| SSN | `\b\d{3}-\d{2}-\d{4}\b` | `123-45-6789` |
| Credit card | 13-19 digit sequences (validate with Luhn) | `4111111111111111` |
| Phone | `\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b` | `(555) 867-5309` |
| IP address | `\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b` (in user context) | `192.168.1.42` |

## Test Fixtures: Use Fake Data

Never use real PII in tests. Use obviously fake values:

```typescript
// BAD -- looks like real data
const user = { email: "jsmith@gmail.com", ssn: "078-05-1120" };

// GOOD -- clearly synthetic
const user = { email: "test-user@example.com", ssn: "000-00-0000" };
```

For bulk test data, use libraries like `@faker-js/faker` with deterministic seeds.

## Log Masking Requirements

PII must never reach logs, metrics, or error tracking unmasked.

```typescript
function maskPII(value: string): string {
  return value
    .replace(/\b\d{3}-\d{2}-\d{4}\b/g, '***-**-****')
    .replace(/\b\d{13,19}\b/g, (m) => '****' + m.slice(-4))
    .replace(/\b[\w.+-]+@[\w.-]+\.\w{2,}\b/g, '****@****');
}

// Apply at the logging boundary, not per-call
logger.info('Processing request', { userId: user.id }); // OK: ID only
logger.info('Processing request', { user });             // BAD: full object
```

### Rules

1. **Log IDs, not objects** -- pass `userId`, not the user record.
2. **Mask at the boundary** -- a single log sanitizer, not scattered `maskPII` calls.
3. **Audit log output** -- grep production logs periodically for PII patterns.
4. **Structured logging only** -- no string interpolation with user data.

## GDPR / CCPA Awareness

- **Purpose limitation** -- only collect PII you actually need.
- **Retention policy** -- define how long each PII field is kept. Soft-delete is not deletion.
- **Right to deletion** -- the system must support purging a user's PII from all stores (DB, caches, logs, backups).
- **Consent tracking** -- record what the user consented to and when.
- **Data export** -- users can request all data held about them (Article 15 / CCPA right to know).

## Data Retention Guidance

| Data Type | Suggested Max Retention | Notes |
|-----------|------------------------|-------|
| Session tokens | 24 hours | Rotate, don't extend |
| Access logs with IPs | 90 days | Anonymize after |
| Payment card data | Don't store | Use tokenized processor (Stripe, etc.) |
| User profile PII | Until account deletion + 30 days | Legal hold exceptions |

## Code Review Checklist

- [ ] No real PII in test fixtures or seed files
- [ ] Log statements do not include raw user objects
- [ ] PII fields are masked before reaching any logging/error tracking
- [ ] Data retention is defined for any new PII field
- [ ] Deletion/export paths cover the new data
