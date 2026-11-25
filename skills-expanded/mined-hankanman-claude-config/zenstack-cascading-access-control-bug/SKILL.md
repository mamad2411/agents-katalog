---
name: zenstack-cascading-access-control-bug
description: |
  Fix ZenStack access control bug where cascading check(relation, 'read') policies
  allow unauthorized data access. Use when: (1) Users can see other users' private
  data they shouldn't access, (2) Access control works at User/Profile level but
  fails for related models, (3) Public profile access unintentionally grants access
  to private related data. Covers ZenStack @@allow policies with check() function
  and defense-in-depth patterns.
author: Claude Code
version: 1.0.0
date: 2026-02-05
---

# ZenStack Cascading Access Control Security Bug

## Problem

ZenStack access control policies using `check(relation, 'read')` can create cascading
permission chains that grant unintended access to private data. Users who can read a
public profile may gain access to ALL related private data (availability, bookings, etc.)
through chained policies.

## Context / Trigger Conditions

**Symptoms:**
- Users can see other users' private data when they shouldn't
- Access control works correctly for User/Profile models but fails for related data
- Testing with multiple users reveals data leakage
- Calendar or dashboard shows overlapping data from multiple users

**When this occurs:**
- Using ZenStack with `@@allow('read', check(relation, 'read'))` patterns
- Models have public read access (e.g., approved instructor profiles)
- Related models inherit access through relationship checks
- No explicit filtering in WHERE clauses

## Root Cause

The cascading chain works like this:

```zmodel
// Profile - Public read for approved instructors
@@allow('read', isActive && type.name == 'Instructor' && verificationStatus == APPROVED)

// User - Inherits from profile
@@allow('read', check(profile, 'read'))

// Availability - Inherits from user
@@allow('read', check(user, 'read'))  // ❌ BUG!
```

**What happens:**
1. Emily Chen (instructor) can read other instructors' public profiles ✓ (intended)
2. Therefore Emily can read those instructors' User records (via `check(profile, 'read')`)
3. Therefore Emily can read those instructors' Availability records (via `check(user, 'read')`) ❌ (BUG!)

## Solution

### Fix 1: Replace Cascading Checks with Explicit Conditions

**BEFORE (Vulnerable):**
```zmodel
model Availability {
  // ...
  @@allow('read', check(user, 'read'))  // Too permissive!
  @@allow('all', userId == auth().id)
}
```

**AFTER (Secure):**
```zmodel
model Availability {
  // ...

  // Public read ONLY for FREE slots of approved instructors (for booking flow)
  @@allow('read',
    status == FREE &&
    user.profile.type.name == 'Instructor' &&
    user.profile.verificationStatus == APPROVED &&
    user.profile.isActive == true
  )

  // Users can manage their own availability
  @@allow('all', userId == auth().id)

  // Admins have full access
  @@allow('all', auth().role == 'ADMIN')
}
```

### Fix 2: Add Defense in Depth - Explicit Query Filtering

Even with corrected access control, add explicit filtering in queries:

**BEFORE (Relies only on access control):**
```typescript
const blocks = await db.$setAuth({ id: user.id, role: user.role })
  .availability.findMany({
    where: {
      status: AvailabilityStatusEnum.FREE,
      // Missing: userId filter
    },
  });
```

**AFTER (Defense in depth):**
```typescript
const blocks = await db.$setAuth({ id: user.id, role: user.role })
  .availability.findMany({
    where: {
      userId: user.id,  // Explicit filtering
      status: AvailabilityStatusEnum.FREE,
    },
  });
```

**Benefits:**
- Performance: Uses indexed `userId` field
- Clarity: Code is self-documenting
- Safety: Works even if access control policies change
- Resilience: Multiple layers prevent bugs

## Verification

1. **Test with Multiple Users:**
   ```bash
   # Create two instructor accounts
   # Set up availability for both
   # Log in as instructor A
   # Navigate to calendar/dashboard
   # Verify ONLY instructor A's data appears (no instructor B data)
   ```

2. **Check Access Control Output:**
   ```typescript
   // In development, log query results
   console.log('Availability count:', blocks.length);
   console.log('User IDs:', blocks.map(b => b.userId));
   // Should only show current user's ID
   ```

3. **Review All `check()` Policies:**
   ```bash
   # Search for potentially problematic patterns
   grep -r "check(.*'read')" packages/database/zenstack/schema.zmodel
   # Review each instance for cascading issues
   ```

## Example

Real-world bug from RoadDux driving instructor platform:

**Symptom:** Emily Chen's calendar showed availability blocks from ALL instructors, not just her own.

**Root Cause:**
```zmodel
model Availability {
  @@allow('read', check(user, 'read'))  // Cascades from public profile access
  @@allow('all', userId == auth().id)
}
```

**Fix:**
```zmodel
model Availability {
  // Explicit conditions instead of cascading check
  @@allow('read',
    status == FREE &&  // Only public availability
    user.profile.type.name == 'Instructor' &&
    user.profile.verificationStatus == APPROVED &&
    user.profile.isActive == true
  )
  @@allow('all', userId == auth().id)
  @@allow('all', auth().role == 'ADMIN')
}
```

Plus added explicit filtering:
```typescript
const blocks = await db.$setAuth({ id: user.id, role: user.role })
  .availability.findMany({
    where: {
      userId: user.id,  // Explicit user scoping
      status: AvailabilityStatusEnum.FREE,
      // ... other conditions
    },
  });
```

## Notes

### When `check()` is Safe

The `check()` function is safe when checking relationships in the SAME direction as data ownership:

```zmodel
model Booking {
  // Safe: Checking if I can read MY OWN booking's instructor
  @@allow('read', learnerUserId == auth().id && check(instructor, 'read'))
}
```

### When `check()` is Dangerous

Dangerous when it cascades UPWARD through public data:

```zmodel
model PrivateData {
  // Dangerous: Anyone who can read my public profile can read this!
  @@allow('read', check(user.profile, 'read'))
}
```

### Security Principles

1. **Principle of Least Privilege:** Start restrictive, explicitly allow public access where needed
2. **Defense in Depth:** Use both access control AND explicit query filtering
3. **Test with Multiple Users:** Access bugs only appear with multi-user testing
4. **Separate Public and Private:** Different policies for public-facing vs private data

### Other Models to Review

Check these patterns in your schema:

- ✅ **Booking:** `@@allow('read', instructorUserId == auth().id || learnerUserId == auth().id)` (Correct - explicit IDs)
- ✅ **Payment:** `@@allow('read', booking.instructorUserId == auth().id || booking.learnerUserId == auth().id)` (Correct - through explicit ownership)
- ❌ **Any model with:** `@@allow('read', check(user, 'read'))` without additional constraints (Review carefully!)

## References

- [ZenStack Access Control Documentation](https://zenstack.dev/docs/reference/zmodel-language#access-policy)
- [ZenStack check() Function](https://zenstack.dev/docs/reference/zmodel-language#attribute-functions)
- [Prisma Security Best Practices](https://www.prisma.io/docs/guides/security)
- [OWASP Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)
