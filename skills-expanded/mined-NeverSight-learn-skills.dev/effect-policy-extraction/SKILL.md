---
name: effect-policy-extraction
description: Refactor complex Effect-based orchestrators and workers into the "Functional Core, Imperative Shell" pattern using pure policy ADTs. Use when asked to "refactor to pure policy", "extract business logic", or clean up a messy worker mixing I/O and business rules in Effect.
---

# Guide: Pure Policy ADT Extraction (Functional Core, Imperative Shell) in Effect

This document details the exact steps an agent must follow to refactor a complex Effect-based
orchestrator or worker into the "Functional Core, Imperative Shell" pattern.

## 1. Context & Goal

Many workers organically grow into a messy, interleaved mix of:

- **I/O & Side Effects:** `yield* db.findUnique`, `yield* fetch(...)`, `yield* Effect.logInfo`,
  `yield* create_manual_review_event`.
- **Business Logic:** Deeply nested `if/else` statements, threshold math, and state disqualifiers.

**The Goal:** Separate the _Business Logic_ (What we should do) from the _Orchestration_ (How we
fetch data and apply side effects).

This makes the domain logic 100% unit-testable without mocking `Prisma` or external APIs, prevents
expensive I/O when early disqualifiers are met, and treats all business outcomes symmetrically
(avoiding the anti-pattern of using `Effect.fail` for expected domain routing).

**When NOT to use this pattern:**
Do not over-engineer simple code. Skip this refactor if the worker is a linear, 3-step pipeline with fewer than 2 branching outcomes. Only apply this when there are distinct business decisions, thresholds, or multiple disqualifying conditions.

## 2. The Architecture

For every refactored workflow, you will create or update two distinct areas:

1. **The Policy File (e.g., `src/modules/domain/my-policy.ts`)**: 100% pure TypeScript. Zero
   `Effect` generators. Contains the `Action` ADT and pure decision functions.
2. **The Imperative Shell (e.g., `src/workers/my-worker.ts`)**: The Effect orchestrator. Gathers
   state, calls the pure policy, and applies side effects using `$match`.

---

## 3. Step-by-Step Implementation Guide

### Step 1: Identify the Business Outcomes (The ADT)

**Incremental Extraction Heuristic:** Do not try to refactor everything at once. Start by reading the existing code and listing *all* terminal outcomes (returns, logged errors, specific side-effects). Once you have listed the outcomes, work backwards to figure out what state is required to reach them.

Define a `Data.TaggedEnum` that represents these outcomes. **Adapt the naming strictly to your target domain.** (e.g., if working on Auth, you might have `LockAccount` or `RequireMFA`).

```typescript
import { Data } from "effect";

// Example for a fulfillment verifier domain:
export type MyDomainAction = Data.TaggedEnum<{
  SkipSimulatedMode: {};
  FlagMissingData: { field: string };
  FlagExternalError: { error: { _tag: string; message: string } };
  OverrideToCompleted: { current: number; expected: number };
  ConfirmFailed: { current: number; expected: number };
}>;

export const MyDomainAction = Data.taggedEnum<MyDomainAction>();
```

_Rule: Do not use the Effect error channel for these outcomes. "Simulated Mode" is a valid business
state, not an infrastructure failure._

### Step 2: Define State Contexts

Identify the data needed to make these decisions. Crucially, separate data that is _already known_
in memory (Early Context) from data that requires _expensive I/O_ (External Context).

```typescript
export interface EarlyDisqualifierContext {
  readonly is_simulated: boolean;
  readonly initial_amount: number | null;
}

export interface ExternalStateContext {
  readonly initial_amount: number; // Safe because early check passed
  readonly ordered_amount: number;
  readonly threshold_percent: number;
  readonly scrape_result:
    | { ok: true; count: number }
    | { ok: false; error: { _tag: string; message: string } };
}
```

### Step 3: Write the Pure Decision Functions

Write pure functions that take the contexts and return an `Action`. **These functions must NEVER use
`yield*`, `Effect`, or perform logging/I/O.**

```typescript
export function check_early_disqualifiers(
  ctx: EarlyDisqualifierContext,
): MyDomainAction | null {
  if (ctx.is_simulated) return MyDomainAction.SkipSimulatedMode();
  if (ctx.initial_amount === null)
    return MyDomainAction.FlagMissingData({ field: "initial_amount" });
  return null;
}

export function determine_action(ctx: ExternalStateContext): MyDomainAction {
  if (!ctx.scrape_result.ok) {
    return MyDomainAction.FlagExternalError({ error: ctx.scrape_result.error });
  }

  const current = ctx.scrape_result.count;
  const expected =
    ctx.initial_amount + ctx.ordered_amount * (ctx.threshold_percent / 100);

  if (current >= expected) {
    return MyDomainAction.OverrideToCompleted({ current, expected });
  }

  return MyDomainAction.ConfirmFailed({ current, expected });
}
```

### Step 4: Test the Pure Functions (Zero Mocks)

Because the policy is 100% pure, you can test complex business thresholds instantly without mocking `Prisma` or `Effect` environments. When asked to write tests, use this pattern:

```typescript
import { describe, expect, it } from "vitest";

describe("determine_action", () => {
  it("overrides to completed when threshold is met", () => {
    const action = determine_action({
      initial_amount: 100,
      ordered_amount: 50,
      threshold_percent: 90,
      scrape_result: { ok: true, count: 145 }, // 100 + (50 * 0.9) = 145
    });
    expect(action).toStrictEqual(MyDomainAction.OverrideToCompleted({ current: 145, expected: 145 }));
  });
});
```

### Step 5: Create the Action Applier (The Imperative Matcher)

Back in the worker/orchestrator file, create a function that takes the `Action` ADT and executes the
exact side effects required for that outcome using `$match`.

```typescript
// src/workers/my-worker.ts
const apply_action = Effect.fn("my_worker.apply_action")(function* (
  order_id: number,
  action: MyDomainAction,
) {
  return yield* MyDomainAction.$match(action, {
    SkipSimulatedMode: () =>
      Effect.gen(function* () {
        yield* Effect.logInfo("Skipping in simulated mode", { order_id });
        return { skipped: true };
      }),
    FlagMissingData: (a) =>
      Effect.gen(function* () {
        yield* create_manual_review_event(order_id, `Missing ${a.field}`);
        return { flagged: true };
      }),
    // ... implement all other branches, moving existing Effect.logs and db.updates here
  });
});
```

### Step 6: Refactor the Main Handler

Replace the messy, interleaved logic with a clean pipeline:

```typescript
handler: (data, payload) =>
  Effect.gen(function* () {
    // 1. Gather Early State
    const initial_amount = payload.order.initial_amount;
    const is_simulated = process.env.SIMULATED_MODE === "true";

    // 2. Early Policy Check (Saves expensive I/O!)
    const early_action = check_early_disqualifiers({
      is_simulated,
      initial_amount,
    });
    if (early_action) {
      return yield* apply_action(payload.order.id, early_action);
    }

    // 3. Gather External State (The expensive I/O)
    const scrape_either = yield* Effect.either(
      get_engagement_count(payload.order),
    );
    const config = yield* MyDomainConfig;

    // 4. Late Policy Check
    const action = determine_action({
      initial_amount: initial_amount as number,
      ordered_amount: payload.amount,
      threshold_percent: config.thresholdPercent,
      scrape_result: Either.match(scrape_either, {
        onLeft: (error) => ({ ok: false as const, error }),
        onRight: (count) => ({ ok: true as const, count }),
      }),
    });

    // 5. Apply Action
    return yield* apply_action(payload.order.id, action);
  });
```

---

## 4. Crucial Rules for the Agent

1. **No I/O or Logging in the Policy:** The policy file must be 100% pure TypeScript. If you need to
   log a decision, log it inside the `Action.$match` block in the worker shell.
2. **Be Precise with Context:** Do not pass massive Prisma objects (e.g., the entire `fulfillment`
   row) into the pure policy functions. Pass only the exact scalar values required to make the
   decision (e.g., `initial_amount`, `ordered_amount`).
3. **Map `Either` to Plain Objects for the Policy:** Pure functions shouldn't deal with
   `Effect.Either` if possible. Map `Either` results to simple
   `{ ok: true, data } | { ok: false, error }` discriminators before passing them into the policy,
   keeping the policy decoupled from Effect primitives.
4. **Don't use `Effect.fail` for Domain Routing:** Use the `Action` ADT to handle expected business
   outcomes. Reserve `Effect.fail` or typed errors specifically for infrastructural failures (like
   network timeouts or `PrismaError`).
5. **Keep `$match` Return Types Consistent:** Ensure every branch of your `Action.$match` block returns a compatible type. If one branch returns `Effect<void>` and another returns `Effect<{ flagged: boolean }>`, the TypeScript compiler will throw an error.