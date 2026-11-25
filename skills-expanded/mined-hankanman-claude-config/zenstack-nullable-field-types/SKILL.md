---
name: zenstack-nullable-field-types
description: |
  Fix TypeScript type errors when passing ZenStack query results to components expecting Zod schema types. Use when: (1) Getting "Type 'null' is not assignable to type 'undefined'" errors, (2) Database query results don't match component prop types, (3) ZenStack findMany/findFirst results have nullable fields but Zod schemas expect optional (undefined) fields, (4) Working with ZenStack + TypeScript in Next.js. Covers null vs undefined handling, type transformations, and proper interface definitions.
author: Claude Code
version: 1.0.0
date: 2026-02-03
---

# ZenStack Nullable Field Type Mismatches

## Problem

ZenStack query results return `null` for nullable database fields, but TypeScript interfaces and Zod schemas often expect `undefined` for optional fields. This causes type errors when passing query results to components or functions that use schema types.

## Context / Trigger Conditions

**Exact Error Pattern**:
```
error TS2322: Type 'string | null' is not assignable to type 'string | undefined'.
  Type 'null' is not assignable to type 'string | undefined'.
```

**When This Occurs**:
- Passing ZenStack query results directly to React components
- Component props use Zod schema types (e.g., `z.infer<typeof mySchema>`)
- Database schema has nullable fields: `field String?`
- Query results include nullable fields without type transformation

**Example Scenario**:
```tsx
// Database query
const availability = await db.availability.findMany({
  select: {
    id: true,
    reason: true, // nullable in database
  },
});

// Component expects
interface Props {
  availability: Array<{
    id: string;
    reason?: string; // optional (undefined), not nullable (null)
  }>;
}

// Type error! reason is string | null, not string | undefined
<MyComponent availability={availability} />
```

## Solution

### Option 1: Define Explicit Database Result Types (Recommended)

Create interfaces that match actual database result types instead of using Zod schema types:

```tsx
// ✅ Correct: Define DB result type
interface AvailabilityFromDB {
  id: string;
  userId: string;
  dayOfWeek: number;
  startTime: Date;
  endTime: Date;
  timezone: string;
  reason: string | null; // Explicitly null, not undefined
  recurrenceRule: string | null;
  effectiveFrom: Date;
  effectiveUntil: Date | null;
  status: "FREE" | "BUSY";
}

// Component props
interface Props {
  availability: AvailabilityFromDB[];
}

// Server component
const blocks = await db.availability.findMany(); // Returns AvailabilityFromDB[]
return <MyComponent availability={blocks} />;
```

### Option 2: Transform Null to Undefined

If you must use Zod schema types, transform the data:

```tsx
// Transform function
function nullToUndefined<T extends Record<string, any>>(obj: T): T {
  const result: any = {};
  for (const key in obj) {
    result[key] = obj[key] === null ? undefined : obj[key];
  }
  return result;
}

// Usage
const blocks = await db.availability.findMany();
const transformed = blocks.map(nullToUndefined);
return <MyComponent availability={transformed} />;
```

### Option 3: Type Assertion (Use Sparingly)

When you're certain the types are compatible:

```tsx
<MyComponent availability={blocks as ComponentProps['availability']} />
```

**Warning**: This bypasses type checking and can hide real issues.

### Option 4: Adjust Component Types to Accept Null

Make component props accept null explicitly:

```tsx
interface Props {
  availability: Array<{
    id: string;
    reason: string | null | undefined; // Accept both
  }>;
}

// Or use a utility type
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

interface Props {
  availability: Nullable<AvailabilitySchema>[];
}
```

## Best Practices

### 1. Use Database Result Types for Server-Fetched Data

```tsx
// ✅ Good: Explicit DB types
type BookingFromDB = {
  id: string;
  status: string;
  learner: { name: string } | null; // relation can be null
};

const bookings: BookingFromDB[] = await db.booking.findMany({
  select: {
    id: true,
    status: true,
    learner: { select: { name: true } },
  },
});
```

### 2. Use Zod Schema Types for Form Data

```tsx
// ✅ Good: Zod types for client input
import { createBookingSchema, type CreateBooking } from "database/schemas";

function BookingForm() {
  const [data, setData] = useState<CreateBooking>({
    // ... undefined for optional fields
  });
}
```

### 3. Document the Distinction

```tsx
/**
 * Database result type - fields are null when not set
 */
type AvailabilityFromDB = {
  reason: string | null;
};

/**
 * Input/form type - fields are undefined when optional
 */
type CreateAvailability = z.infer<typeof createAvailabilitySchema>;
```

## ZenStack-Specific Considerations

### Nullable Relations

Relations in ZenStack queries return `null` when not found:

```tsx
// Query with relation
const booking = await db.booking.findFirst({
  include: {
    learner: true, // Can be null if deleted/not found
  },
});

// Type must account for null
type BookingWithLearner = {
  learner: User | null; // Not undefined
};
```

### Optional vs Nullable Fields

ZenStack schema:
```prisma
model Availability {
  reason String? // Optional in schema
}
```

TypeScript result:
```tsx
{ reason: string | null } // NOT string | undefined
```

### Select vs Include

Both return nullable types for optional fields:

```tsx
// Select
const result = await db.model.findFirst({
  select: { optionalField: true },
}); // optionalField: Type | null

// Include
const result = await db.model.findFirst({
  include: { relation: true },
}); // relation: RelationType | null
```

## Verification

After fixing types:

```bash
# TypeScript should compile without errors
pnpm tsc --noEmit

# No type errors like:
# "Type 'null' is not assignable to type 'undefined'"
```

## Example: Complete Fix

**Before** (with type errors):

```tsx
// Server component
const blocks = await db.availability.findMany({
  select: {
    id: true,
    reason: true, // string | null
  },
});

// Component props expect Zod type
interface Props {
  blocks: z.infer<typeof availabilitySchema>[]; // reason?: string (undefined)
}

return <AvailabilityList blocks={blocks} />; // TYPE ERROR
```

**After** (fixed):

```tsx
// Define explicit DB result type
interface AvailabilityBlock {
  id: string;
  reason: string | null; // Match database reality
}

// Server component
const blocks: AvailabilityBlock[] = await db.availability.findMany({
  select: {
    id: true,
    reason: true,
  },
});

// Component props accept DB type
interface Props {
  blocks: AvailabilityBlock[];
}

return <AvailabilityList blocks={blocks} />; // ✅ No error
```

## Notes

- This issue is common in ORMs (Prisma, ZenStack, TypeORM) because SQL NULL maps to `null` in TypeScript
- Zod schemas typically use `optional()` which generates `undefined`, not `null`
- The mismatch is by design: database layer uses `null`, application layer often prefers `undefined`
- Consider establishing a convention: "DB types use null, business logic uses undefined"
- Some teams create mapper functions to convert between the two

## Common Mistakes

1. **Using Zod Types Everywhere**: Don't use `z.infer<>` types for database query results
2. **Ignoring Nullability**: Assuming optional fields are `undefined` when they're actually `null`
3. **Loose Type Assertions**: Using `as any` to bypass the issue instead of fixing it properly
4. **Not Handling Relations**: Forgetting that relations can be `null` even if marked as required in schema

## References

- [ZenStack Documentation](https://zenstack.dev/)
- [Prisma Null vs Undefined](https://www.prisma.io/docs/orm/reference/prisma-client-reference#null-and-undefined)
- [TypeScript Null vs Undefined](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#null-and-undefined)
- [Zod Optional Fields](https://zod.dev/?id=optional)
