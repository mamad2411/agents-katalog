---
name: service-layer-style
description: T3 service-layer style — ServiceCtx contract, style decision tree, migration checklist. Explicit-only.
allowed-tools: Read, Glob, Grep
---


# Service-Layer Style (T3 Turbo)

Portable style guide for the `packages/api/src/services/**` layer in T3 Turbo
monorepos (Next.js App Router + tRPC v11 + Drizzle + Neon Postgres). Applies
to any T3 project — not framework-specific. The goal is a service layer that
is **typesafe, testable, observable, and free of `this.x!` traps**.

## Invariant: ServiceCtx

Every service function takes a `ServiceCtx` as its **first argument**. Not
`this`, not a global, not a hidden import. Explicit parameter, typed once.

```ts
// packages/api/src/services/ctx.ts
export interface ServiceCtx {
  db: Database;                // Drizzle client
  logger: Logger;              // pre-scoped with { domain, correlationId, userId }
  userId: string | null;       // null for system/cron callers
  eventSeriesId: string;       // non-null — enforced at tRPC boundary
  eventId: string;             // non-null for event-scoped; use SeriesCtx for series-only
  correlationId: string;
  abortSignal?: AbortSignal;   // for Fluid Compute graceful shutdown
}

export type SeriesCtx = Omit<ServiceCtx, "eventId">;
export type EventCtx = ServiceCtx;
```

**Why this shape:**

- `userId: string | null` — system callers (cron, webhook retries) must be
  first-class. Nullable forces call sites to narrow before auth-sensitive work.
- `eventSeriesId`/`eventId` non-null — the tRPC middleware enforces scoping
  before services run, so services never branch on `if (ctx.eventId)`.
- `logger` pre-scoped — no `console.*`, no re-scoping inside functions. The
  outer middleware attaches `{ domain, correlationId, userId }` exactly once.
- `abortSignal` — Fluid Compute and long-running workflows need cooperative
  cancellation. Pass it to the Drizzle client and fetch/Stripe calls.

**Construction boundary:** `ServiceCtx` is built **once** at the tRPC
middleware layer (or the cron/webhook entry). Services never construct it.
Tests build a fake ctx by hand — that's the whole point.

## Decision Tree — Four Styles

Pick the simplest style that covers the surface area. Escalate only when the
next style genuinely removes duplication.

```
┌─ 1–2 exports, no shared setup?        → Style A (pure functions)
├─ ≥3 methods sharing setup/span/logger? → Style B (factory + closure)
├─ Specialization by object type,
│   ~70% unique workflow?                → Namespace Factory Family
└─ ≥80% shared impl, return type is the
    specialization axis?                 → Type-Routed Generics <T>
```

### Style A — Pure Functions (default)

```ts
// services/badge/get-badge-by-code.ts
import type { ServiceCtx } from "../ctx";
import type { BadgeDto } from "./dto";

export async function getBadgeByCode(
  ctx: ServiceCtx,
  input: { code: string },
): Promise<BadgeDto | null> {
  const row = await ctx.db.query.badges.findFirst({
    where: and(
      eq(badges.eventSeriesId, ctx.eventSeriesId),
      eq(badges.code, input.code),
    ),
  });
  if (!row) return null;
  return toBadgeDto(row);
}
```

Rules:

- 1–2 exports per module. If a third shows up, consider Style B.
- Each function testable by passing a fake `ctx`.
- No free variables outside the function body — no module-level `let`.
- Best for: read/query services, DTO shaping, stateless domain logic.

### Style B — Factory + Closure

When ≥3 methods share setup (scoped logger, Stripe client, OTel span, txn).

```ts
// services/affiliate/auto-payout-service.ts
export function createAutoPayoutService(ctx: ServiceCtx) {
  const logger = ctx.logger.child({ service: "autoPayout" });
  const stripe = getStripeClient(ctx);

  async function processPayouts(input: ProcessInput): Promise<PayoutResult> {
    return withSpan("affiliate.processPayouts", async (span) => {
      const rows = await loadEligibleRows();
      span.setAttribute("rows", rows.length);
      const results = await Promise.all(rows.map(_processSingle));
      return summarize(results);
    });
  }

  // private to closure — not exported
  async function _processSingle(row: EligibleRow): Promise<SingleResult> {
    logger.info({ rowId: row.id }, "processing payout");
    // ...
  }

  async function loadEligibleRows(): Promise<EligibleRow[]> { /* ... */ }

  return { processPayouts };
}
```

Rules:

- Factory returns an **object literal** with only the public surface.
- Private helpers live inside the closure, never exported.
- `ctx` captured once, never re-passed to inner helpers (they read via closure).
- Best for: multi-step workflows, Stripe init, transaction boundaries, any
  service with meaningful setup cost.

### Namespace Factory Family

When specialization by object type is genuine — e.g. checkout for attendee vs
vendor vs sponsor has genuinely different workflows (different Stripe products,
different fulfillment, different notifications).

```ts
// services/payment/checkout/index.ts
import { createAttendeeCheckoutService } from "./attendee";
import { createVendorCheckoutService } from "./vendor";
import { createSponsorCheckoutService } from "./sponsor";

export const PaymentCheckout = {
  forAttendee: createAttendeeCheckoutService,
  forVendor: createVendorCheckoutService,
  forSponsor: createSponsorCheckoutService,
} as const;
```

Each factory returns a **concrete typed service** — no union return types, no
discriminated branching at call sites. Cross-cutting logic (fee calc, tax,
invoice numbering) lives in shared modules that all three factories import.

Heuristic: ~70% specialized / ~30% shared. If it tips past 80% shared, collapse
to Style B with a discriminator input. If it tips past 80% specialized, you
don't have a family — you have three services that happen to share a word.

Best for: attendee/vendor/sponsor branching, B2B vs B2C flows, internal vs
external webhooks.

### Type-Routed Generics `<T>` — cross-cutting only

Valid only for **cross-cutting modules** that all specializations consume:

```ts
// services/payment/fee-calculator.ts
export function calculateFees<T extends FeeContext>(
  ctx: ServiceCtx,
  subtotal: number,
  context: T,
): FeeBreakdown<T> {
  // ≥80% shared implementation; return type specializes on T
}
```

Use when ALL hold:

1. ≥80% shared implementation body.
2. Symmetric operation across inputs.
3. Return type is the specialization axis (not just input routing).

Examples: `fee-calculator`, `refund-policy`, `invoice-numbering`,
`notification-sender`.

**NOT for** specialized workflows. If the function branches on `T` via a big
`switch`, you wanted Namespace Factory Family.

## Forbidden Patterns

### `extends BaseService`

```ts
// ❌ DO NOT
class VendorInvoiceService extends BaseService {
  async list() {
    return this.db!.select().from(invoices).where(eq(invoices.eventId, this.eventId!));
  }
}
```

Retire this pattern. `this.db!` and `this.eventId!` are non-null asserts that
hide runtime guards from the type system. When the base class is constructed
without those fields, the error surfaces deep in a query builder, not at the
call site. `ServiceCtx` threaded as a parameter makes the invariant **type-checked
by the compiler**, not enforced by a constructor you hope was called correctly.

### `Promise<typeof table.$inferSelect>` in exported returns

```ts
// ❌ Leaks persistence columns to clients
export async function getBadge(ctx, id): Promise<typeof badges.$inferSelect> { ... }

// ✅ Explicit DTO
export async function getBadge(ctx, id): Promise<BadgeDto> { ... }
```

Exporting `$inferSelect` means `deletedAt`, `internalNotes`, `stripeSecretRef`,
and every future column you add are automatically part of the public API.
Clients start depending on them; removing them becomes a breaking change.
**Define an explicit DTO and a `toDto()` mapper.** The mapper is the single
place that decides what leaves the service.

### Silent-swallow catches

```ts
// ❌ Hides failures — "why is the list empty?"
try { return await loadRows(); } catch { return []; }
try { return await countFoo(); } catch { return { count: 0 }; }
```

Log + throw, or return a typed `Result<T, DomainError>`. Silent empty returns
make bugs invisible in both UI and observability. If the caller needs a fallback,
it should be explicit at the call site (`?? []`).

### `as any` / `: any` in service signatures

```ts
// ❌
export function process(ctx, input: any): any { ... }
```

Reifies a type hole. Use `z.unknown()` + Zod narrowing, or a proper
discriminated union. `any` in a service signature propagates to every caller
and defeats the purpose of having a typed service layer.

### Multi-channel logger confusion

One domain channel per service file:

```ts
// ✅ services/badge/*.ts — always badgeLogger
const logger = ctx.logger.child({ service: "badge" });

// ❌ services/vendor-invoice/create.ts — caller happens to be a webhook
const logger = ctx.logger.child({ service: "webhook" }); // WRONG
```

The logger channel tracks the **domain the service operates on**, not who
called it. `correlationId` already carries caller context. Mixing channels
shreds log-based dashboards.

### Functions >60 LOC

Extract private helpers inside the closure (Style B) or as module-private
functions (Style A). A 200-LOC function is a workflow pretending to be a
function.

### `Sentry.captureException` in a `DomainError` catch

```ts
// ❌ Double-capture
try { ... } catch (e) {
  Sentry.captureException(e);
  throw new DomainError(...);
}
```

The tRPC error pipeline captures `DomainError` at the outer boundary. Adding
a `captureException` in the service creates duplicate Sentry issues with
different stack traces — the issue queue fills with phantoms.

## Exemplars & Anti-Exemplars

Point new code at the exemplar. Never at the anti-exemplar.

| Kind | Canonical path pattern | Notes |
|------|------------------------|-------|
| Exemplar (Style B) | `services/<domain>/<domain>-service.ts` with `withSpan`, explicit DTO, typed result, private helpers in closure | Short file (<400 LOC), one public factory, clear DTO export |
| Anti-exemplar | class-based service with `extends BaseService`, silent `catch { return [] }`, mixed class+fn, >2000 LOC | Refactor before extending |

When reviewing a PR that touches a service, ask: "Does this file look more like
the exemplar or the anti-exemplar?" If anti-, pause and apply the migration
checklist below.

## Per-Service Migration Checklist

Portable across projects. Run top-to-bottom per service:

```
[ ] Classify: current style (class / free fn / mixed) → target style (A / B / family / generic)
[ ] Define DTO types — delete $inferSelect from exported returns
[ ] Convert BaseService class → factory function or pure fns
[ ] Thread ServiceCtx as first arg (drop this.x! non-null asserts)
[ ] Replace console.* / ad-hoc logger with domain logger channel
[ ] Wrap cross-domain workflows in withSpan()
[ ] Replace catch-empty-returns with log+throw or typed Result
[ ] Remove as any / z.any() from signatures
[ ] Split any fn >60 LOC into private helpers
[ ] Update callers (tRPC routers + sibling services)
[ ] Drop @ts-nocheck on tests; import canonical DTO/schema
[ ] Delete Sentry.captureException calls in catches that already throw DomainError
```

Ship one service per PR when possible. Large classes with 15 methods may split
across 2–3 PRs — that's fine, just don't half-migrate a file.

## Testing

```ts
// Build a fake ctx by hand — that's the whole point of the pattern
function makeCtx(overrides: Partial<ServiceCtx> = {}): ServiceCtx {
  return {
    db: fakeDb,
    logger: silentLogger,
    userId: "user_test",
    eventSeriesId: "series_test",
    eventId: "event_test",
    correlationId: "corr_test",
    ...overrides,
  };
}

test("getBadgeByCode returns null when missing", async () => {
  const ctx = makeCtx();
  const result = await getBadgeByCode(ctx, { code: "does-not-exist" });
  expect(result).toBeNull();
});
```

No `jest.mock("../db")`. No `vi.mock("@/lib/logger")`. The ctx **is** the
seam — fake it directly.

## Observability

- **OTel spans** — cross-domain workflows wrap in `withSpan("<domain>.<op>", fn)`.
  Single-query services don't need spans (Drizzle + Neon already instrument).
- **Log shape** — every log line carries `{ service, correlationId, userId, eventId }`.
  The middleware scopes the logger; service functions add call-specific fields.
- **Error flow** — throw `DomainError` with `{ code, userMessage, retryable }`.
  The tRPC formatter passes these to the client verbatim. No `TRPCError` inside
  services.

## Anti-FAQ

**"What about `BaseService`? It centralizes the db/logger binding."**

That's exactly the problem. The binding happens in a constructor that the
compiler can't prove ran with valid inputs, so every method ends up with
`this.db!` / `this.eventId!`. Parameters are centralization — they're just
centralized **in the type system**, where the compiler can enforce them.

**"What about provider abstraction / dependency injection frameworks?"**

Not needed. `ServiceCtx` is the DI container, the factory closure is the
scope, and the tRPC middleware is the composition root. Adding Nest/InversifyJS
adds a runtime graph to solve a problem the type system already solves.

**"Can I use a class if it doesn't extend BaseService?"**

Yes, but you'll re-invent the factory closure with extra syntax and no benefit.
Factory functions compose better (you can `pipe` them, `Promise.all` them,
and partially apply them). Reach for a class only if you need instance
identity (caching by reference) — which is almost never.

**"Where does transaction management go?"**

At the service boundary, inside the factory method:

```ts
async function transferBadge(input: TransferInput) {
  return ctx.db.transaction(async (tx) => {
    const txCtx: ServiceCtx = { ...ctx, db: tx };
    await debitSource(txCtx, input.fromId);
    await creditTarget(txCtx, input.toId);
  });
}
```

A fresh `ServiceCtx` is cheap. Threading `tx` as the new `db` keeps every
nested service call inside the transaction with zero special-casing.

**"What if I need to call service X from service Y?"**

Just call it. `await createOtherService(ctx).doThing(input)` or
`await otherPureFn(ctx, input)`. The ctx flows through. Resist the urge to
build a "service registry" — the import graph is the registry.

**"How big should a service file get before splitting?"**

~400 LOC is comfortable. ~800 LOC is a smell. >1500 LOC means there are at
least two services hiding in one file — split by public-method cluster.

## Summary

- **ServiceCtx first arg, always.** It's the DI container, the auth scope,
  and the test seam in one type.
- **Style A → B → Namespace Family → Generics,** in that escalation order.
  Don't skip levels.
- **DTOs out, `$inferSelect` never.** The service boundary is a public API.
- **Log + throw; never silent-swallow.** Observability beats defensive empty
  returns every time.
- **Classes optional, BaseService forbidden.** Factory closures carry the
  same weight with fewer footguns.
