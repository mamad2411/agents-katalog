---
name: "code-comment-patterns"
description: "Inline comment rules: why not what, when a comment is required, TODO standards, placement, file headers, deprecation notices, and anti-patterns such as lying or commented-out code. Use when writing or reviewing inline comments."
---

# Code Comment Patterns

## The Core Rule: Why, Not What

Code already shows what is happening. Comments should explain why a choice was made, or what non-obvious constraint applies.

```typescript
// Bad: describes what the code says
// Convert kilometers to miles
const miles = km * 0.621371;

// Bad: states the obvious
// Increment counter by 1
count++;

// Good: explains non-obvious choice
// Using 0.621371 (exact IEEE 754 value) rather than 0.62 to match
// the precision required by the vehicle compliance API (see VehicleSpec §3.4)
const miles = km * 0.621371;

// Good: explains a business constraint
// Skip users with no verified email - marketing has agreed not to contact them
// until verification completes. See: Jira GDPR-142
const eligible = users.filter(u => u.emailVerified);
```

## When Comments Are Required

### Non-obvious algorithm
```python
def levenshtein_distance(s1: str, s2: str) -> int:
    # Dynamic programming approach: build a matrix where cell (i,j)
    # represents the edit distance between s1[:i] and s2[:j].
    # Space complexity is O(n) using only two rows instead of the full matrix.
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1, 1):
        curr = [i]
        ...
```

### Workaround for external bug
```javascript
// Safari 15.4 incorrectly reports WebGL2 as unsupported when in private
// browsing mode even when the device supports it. We detect private mode
// explicitly and fall back to WebGL1 only in that case.
// Remove this after we drop Safari 15.x support (target: 2025 Q3).
const isPrivateSafari = await detectSafariPrivateMode();
```

### Magic numbers
```rust
// 65535 = u16::MAX - the legacy API stores session IDs as 16-bit unsigned ints.
// Any session ID above this value is from the new system and uses the v2 endpoint.
const LEGACY_SESSION_ID_MAX: u32 = 65535;
```

### Business rule implementation
```go
// Orders under $0.50 are not processed - the payment processor minimum
// transaction fee would exceed the order value. See billing contract §2.1.
if order.TotalCents < 50 {
    return ErrOrderBelowMinimum
}
```

## TODO Comment Standards

Always include owner and expiry context. A `TODO` without these is noise:

```python
# Bad: no owner, no deadline, no context
# TODO: fix this

# Good: actionable, owned, bounded
# TODO(alice): Remove this compatibility shim after all clients
# have migrated to API v3. Track progress in JIRA-4521.
# Safe to delete after: 2025-09-01
```

## Inline Comment Placement

```typescript
// Bad: comment after every line (narrating)
const base = getBasePrice();  // get the base price
const tax = base * taxRate;   // calculate tax
const total = base + tax;     // add tax to base

// Good: one comment for the non-obvious block
// Tax calculation uses the rate at time of order creation, not current rate.
// This prevents retroactive tax changes from affecting existing orders.
const base = getBasePrice();
const tax = base * order.taxRateAtCreation;
const total = base + tax;
```

## Module/File Header Comments

For files with non-obvious scope or important constraints:

```typescript
/**
 * Authentication middleware for the Express application.
 *
 * Handles JWT validation, session management, and role-based access control.
 * Does NOT handle OAuth flows - see src/auth/oauth.ts for that.
 *
 * Session tokens use RS256 (asymmetric) signatures so the public key can
 * be distributed to microservices without sharing the signing key.
 *
 * @module auth/middleware
 */
```

## Deprecation Pattern

Never deprecate without a replacement path:

```typescript
/**
 * @deprecated Since 2.1.0. Use {@link createSecureSession} instead.
 * `createSession` uses HS256 (symmetric) which requires sharing the
 * secret key with all services. `createSecureSession` uses RS256.
 *
 * Migration: replace `createSession(userId)` with
 * `createSecureSession(userId, { algorithm: 'RS256' })`.
 *
 * Will be removed in 3.0.0.
 */
export function createSession(userId: string): string
```

## Anti-Patterns

### Comment echoing the type
```typescript
// Bad: the type signature already says userId is a string
/**
 * @param userId - The user ID string
 */
function getUser(userId: string)

// Good: adds information the type does not
/**
 * @param userId - Opaque identifier from the auth service. Format: `usr_[a-z0-9]{20}`.
 *   Do not parse the internal structure.
 */
function getUser(userId: string)
```

### Commented-out code
```python
# Bad: dead code in comments
def process_payment(amount):
    # result = old_processor.charge(amount)
    # if result.code == 200:
    #     return True
    return new_processor.charge(amount)

# Good: delete it, git history preserves old code
def process_payment(amount):
    return new_processor.charge(amount)
```

### Lying comments (worse than none)
```javascript
// Bad: comment says one thing, code does another
// Returns null if user not found
function getUser(id) {
  const user = db.find(id);
  if (!user) throw new Error('User not found'); // throws, doesn't return null
  return user;
}
```

### Apologetic comments
```python
# Bad: explains bad code instead of fixing it
# I know this is messy but it works
def calculate(x, y, z, mode, flag1, flag2, extra=None):
    ...

# Good: refactor the code, or if truly blocked, explain the constraint
# Matches the legacy API's parameter order which cannot be changed
# without a major version bump (scheduled for Q3). See ADR-0023.
def calculate(x, y, z, mode, flag1, flag2, extra=None):
    ...
```

## References
- [TSDoc Specification](https://tsdoc.org/)
- [Google Python Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [Rust API Documentation Guidelines](https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html)
- [Effective Go - Commentary](https://go.dev/doc/effective_go#commentary)
- [eslint-plugin-jsdoc](https://github.com/gajus/eslint-plugin-jsdoc)
- [darglint](https://github.com/terrencepreilly/darglint)
