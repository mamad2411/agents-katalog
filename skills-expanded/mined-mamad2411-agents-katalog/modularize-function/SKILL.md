---
name: modularize-function
description: Refactor large, complex functions into testable, modular pieces. Ensures Cognitive Complexity stays at or below 12, separates unrelated concerns, and extracts pure functions from I/O. Use when a function is too complex, hard to test, or mixes multiple responsibilities.
---

# Modularize Function

Refactor large, complex functions into testable, modular pieces following these principles:

1. **Cognitive Complexity <= 12** per function
2. **Single Responsibility** - no unrelated concerns in the same function
3. **Pure Functions** - separate I/O from business logic

## When to Use This Skill

- Function has Cognitive Complexity > 12
- Function mixes database/API calls with business logic
- Function handles multiple unrelated concerns
- Function is difficult to unit test
- Function exceeds ~50 lines of logic

## Safety Check

Before making any changes, verify it's safe to modularize:

1. **Confirm test coverage exists** - Run existing tests to establish a baseline. If no tests exist, write characterization tests first to capture current behavior.
2. **Check for callers** - Identify all places that call this function. Ensure refactoring won't break public APIs or external contracts.
3. **Verify version control** - Ensure changes are committed or stashed so you can revert if needed.
4. **Review for hidden dependencies** - Look for closures capturing external state, implicit globals, or side effects that aren't obvious from the signature.

Only proceed once you're confident the refactoring can be safely tested and reverted if necessary.

## Analysis Phase

Before refactoring, analyze the target function:

### 1. Measure Cognitive Complexity

Count these patterns (each adds +1 to complexity):
- `if`, `else if`, `else`, `? :` (ternary)
- `for`, `while`, `do while`, `for...of`, `for...in`
- `&&`, `||` in conditions
- `catch`, `switch case`
- Nested control structures (+1 per nesting level)
- Recursion

**Target: <= 12 per function**

### 2. Identify Concerns

List distinct responsibilities:
- Data fetching (DB queries, API calls, file reads)
- Data transformation (mapping, filtering, reshaping)
- Business logic (calculations, validations, decisions)
- Side effects (caching, logging, notifications)
- Output formatting (serialization, response building)

### 3. Map I/O Boundaries

Identify all impure operations:
- Database queries
- External API calls
- File system operations
- Cache reads/writes
- Date/time access (`new Date()`, `Date.now()`)
- Random number generation

## Modularization Strategy

### Module Structure

Create a directory named after the feature. The files depend on what concerns you identify:

```
{feature-name}/
  types.ts                    # Always: all type definitions
  input-schema.ts             # If validation needed: Zod schemas
  fetch-data.ts               # If I/O exists: all DB/API/file operations
  {identified-concern-1}.ts   # Pure function for concern 1
  {identified-concern-2}.ts   # Pure function for concern 2
  ...                         # One file per distinct concern
  {feature-name}.ts           # Orchestrator (composes pure functions)
  index.ts                    # Public exports
  __tests__/
    {concern-1}.test.ts
    {concern-2}.test.ts
    {feature-name}.integration.test.ts
```

**Naming conventions:**
- Name pure function files after what they DO: `calculate-totals.ts`, `validate-input.ts`, `transform-response.ts`
- Use kebab-case for file names
- The orchestrator file matches the feature name

### 1. Extract Types (`types.ts`)

Move all type definitions to a dedicated file:

```typescript
// types.ts
import type { users, orders } from "@/db/schema";

// Row types (DB selections)
export type UserRow = Pick<typeof users.$inferSelect, "id" | "name" | "email">;
export type OrderRow = Pick<typeof orders.$inferSelect, "id" | "total" | "status">;

// Computed/intermediate types
export type UserSummary = {
  userId: string;
  totalOrders: number;
  lifetimeValue: number;
};

// Output types
export type ComputeResult = {
  users: UserSummary[];
  computedAt: number;
};
```

### 2. Isolate I/O (`fetch-data.ts`)

All database queries, API calls, and side effects go here:

```typescript
// fetch-data.ts
import type { DbContext } from "@/db";
import type { UserRow, OrderRow } from "./types";

export async function fetchUserData(
  ctx: DbContext,
  input: { userId: string }
): Promise<{ user: UserRow | null; orders: OrderRow[] }> {
  const [user, orders] = await Promise.all([
    ctx.db.select(...).from(users).where(eq(users.id, input.userId)),
    ctx.db.select(...).from(orders).where(eq(orders.userId, input.userId)),
  ]);

  return { user: user[0] ?? null, orders };
}
```

### 3. Extract Pure Functions

Each concern becomes a pure function with:
- **Explicit inputs** - all data passed as arguments
- **No side effects** - no DB calls, no mutations of external state
- **Deterministic output** - same inputs always produce same outputs

```typescript
// calculate-summary.ts
import type { OrderRow, UserSummary } from "./types";

export function calculateUserSummary(
  userId: string,
  orders: OrderRow[]
): UserSummary {
  return {
    userId,
    totalOrders: orders.length,
    lifetimeValue: orders.reduce((sum, o) => sum + o.total, 0),
  };
}
```

### 4. Create Orchestrator (`compute.ts`)

Compose pure functions with minimal logic:

```typescript
// compute.ts
import { fetchUserData } from "./fetch-data";
import { calculateUserSummary } from "./calculate-summary";
import { formatOutput } from "./format-output";
import type { ComputeResult } from "./types";

export async function computeUserReport(args: {
  ctx: DbContext;
  input: { userId: string };
}): Promise<ComputeResult> {
  // 1. Fetch data (I/O boundary)
  const data = await fetchUserData(args.ctx, args.input);

  if (!data.user) {
    return { users: [], computedAt: Date.now() };
  }

  // 2. Pure transformations
  const summary = calculateUserSummary(data.user.id, data.orders);

  // 3. Format output
  return formatOutput([summary]);
}
```

## Testing Strategy

### Unit Tests for Pure Functions

Test pure functions with static fixtures - no mocking required:

```typescript
// __tests__/calculate-summary.test.ts
import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { calculateUserSummary } from "../calculate-summary";

describe("calculateUserSummary", () => {
  test("returns zero totals for empty orders", () => {
    const result = calculateUserSummary("user-1", []);

    assert.equal(result.totalOrders, 0);
    assert.equal(result.lifetimeValue, 0);
  });

  test("sums order totals correctly", () => {
    const orders = [
      { id: "o1", total: 100, status: "completed" },
      { id: "o2", total: 250, status: "completed" },
    ];

    const result = calculateUserSummary("user-1", orders);

    assert.equal(result.lifetimeValue, 350);
  });
});
```

### Integration Tests for Orchestrator

Test the full pipeline with realistic fixtures:

```typescript
// __tests__/compute.integration.test.ts
import { describe, test, mock } from "node:test";
import { computeUserReport } from "../compute";

describe("computeUserReport integration", () => {
  test("produces expected output for complete user data", async () => {
    const mockDb = createMockDb({
      users: [{ id: "u1", name: "Test", email: "test@example.com" }],
      orders: [{ id: "o1", userId: "u1", total: 500, status: "completed" }],
    });

    const result = await computeUserReport({
      ctx: { db: mockDb },
      input: { userId: "u1" },
    });

    assert.equal(result.users.length, 1);
    assert.equal(result.users[0].lifetimeValue, 500);
  });
});
```

## Analysis Output Format

Before starting refactoring, output your analysis:

```
## Function Analysis: {functionName}

**Location:** {file:line}
**Lines:** {count}
**Cognitive Complexity:** {score} (target: <= 12)

### Identified Concerns
1. {concern-1}: {brief description}
2. {concern-2}: {brief description}
...

### I/O Operations
- {operation-1}: {what it does}
- {operation-2}: {what it does}
...

### Proposed Modules
| File | Purpose | Purity |
|------|---------|--------|
| types.ts | Type definitions | N/A |
| fetch-data.ts | {what I/O it handles} | Impure |
| {concern-1}.ts | {what it computes} | Pure |
| {concern-2}.ts | {what it computes} | Pure |
| {feature}.ts | Orchestrator | Impure |
```

## Common Patterns

### Handling Optional/Nullable Data

Pass through pure functions, handle at boundaries:

```typescript
// Pure function accepts undefined explicitly
export function calculateTotals(
  items: Item[],
  discountRate?: number  // Explicit optional
): Totals {
  const subtotal = items.reduce((s, i) => s + i.price, 0);
  const discount = discountRate ? subtotal * discountRate : 0;
  return { subtotal, discount, total: subtotal - discount };
}
```

### Caching in Orchestrator

Keep cache logic in orchestrator, not pure functions:

```typescript
// compute.ts
export async function compute(args) {
  const cached = cache.get(args.input.key);
  if (cached) return cached;

  const data = await fetchData(args.ctx, args.input);
  const result = pureTransform(data);  // Pure function

  cache.set(args.input.key, result, TTL);
  return result;
}
```

### Date/Time Injection

Pass timestamps as input, don't call `Date.now()` in pure functions:

```typescript
// Orchestrator injects current time
const result = computeReport({
  data,
  nowMs: Date.now(),  // Injected, makes pure function testable
});

// Pure function uses injected time
export function computeReport(args: { data: Data; nowMs: number }) {
  const isExpired = args.data.expiresAt < args.nowMs;
  // ...
}
```

## Execution Steps

When asked to modularize a function:

### Step 1: Analyze
1. Read the function completely
2. Calculate Cognitive Complexity (count control flow patterns)
3. List every distinct concern you find
4. Identify all I/O operations

### Step 2: Plan the Split
Based on your analysis, decide:
- How many pure function modules are needed (one per concern)
- What to name each module (verb + noun, e.g., `calculate-totals`)
- What types need extraction

### Step 3: Execute
1. Create `types.ts` first (enables other files to import types)
2. Create `fetch-data.ts` if any I/O exists
3. Create pure function modules (one concern each)
4. Create orchestrator that composes them
5. Update original file to re-export from new module

### Step 4: Test
1. Write unit tests for each pure function using static fixtures
2. Write integration test for orchestrator
3. Verify same inputs produce same outputs as original

## Success Criteria

After refactoring, verify:

| Check | Target |
|-------|--------|
| Each function's Cognitive Complexity | <= 12 |
| Concerns per function | 1 |
| Pure functions have side effects | None |
| Unit test coverage for pure functions | 100% |
| Behavior change | None (same I/O)
