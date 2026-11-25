---
name: effect-context-witness
description: Decide between Context.Service witness and capability patterns for dependency injection, understanding coupling trade-offs
---

# Context Witness Pattern

Choose between witness (existence) and capability (behavior) patterns for Context.Service definitions.

Baseline: **effect@4.1.0 stable**. Inspect `Context.ts`, `Layer.ts`, and
`Effect.ts` with `git show effect@4.1.0:packages/effect/src/<Module>.ts` in the
Effect reference repository; a newer main checkout is not the release contract.

## Coupling: Hard vs Soft

**Some coupling is necessary and good** - but move it from hard to soft coupling.

### Hard Coupling (Schema)

Field exists in the schema - tightly coupled to domain model:

<!-- typecheck -->
```typescript
import { Schema } from 'effect';

// ❌ HARD COUPLING - Serial is part of the schema
export class PaymentIntent extends Schema.Class<PaymentIntent>('PaymentIntent')({
	id: Schema.String,
	serial: Schema.String, // In schema = hard coupled
	amount: Schema.BigInt
}) {}

// Every PaymentIntent MUST have a serial
// Serialization/validation requires serial
// Cannot create without providing serial
// Schema change needed to remove/change serial
```

### Soft Coupling (Witness)

Field **removed from schema**, only injected in code:

<!-- typecheck -->
```typescript
import { Schema, Context, Effect } from 'effect';

declare const generateId: Effect.Effect<string>;

// ✅ SOFT COUPLING - Serial not in schema
export class PaymentIntent extends Schema.Class<PaymentIntent>('PaymentIntent')({
	id: Schema.String,
	amount: Schema.BigInt
	// No serial field!
}) {}

// Serial is a witness - required but injected via Context
class Serial extends Context.Service<Serial, string>()('Serial') {}

const createPaymentIntent = (amount: bigint) =>
	Effect.gen(function* () {
		const serial = yield* Serial; // Injected from context

		// Use serial in business logic, logging, etc.
		// but it's not part of the persisted data
		yield* Effect.logInfo(`Creating payment intent ${serial}`);

		return new PaymentIntent({ id: yield* generateId, amount });
	});

// Type: Effect<PaymentIntent, never, Serial>
```

**Key insight:** `schema (hard coupling) => witness (soft coupling)`

By removing the field from the schema and injecting it only where needed, you:

- Keep domain models minimal
- Avoid unnecessary persistence
- Easy to test (provide test serial)
- Easy to remove/change (just change injection)
- Explicit dependencies in type signature

**When to use witnesses:**

- Correlation IDs (for tracing, not persistence)
- Request IDs (for logging, not data)
- Transaction contexts (for coordination, not storage)
- Tenant/Region markers (for routing, not schema)

Context injection is not proof of authorization: only a trusted boundary should
provide a verified witness. Keep durable tenant/owner identity in persisted
domain values when isolation, audit, or replay requires it, and carry it explicitly
across process/serialization boundaries. A context marker does not replace it.

## Witness: Existence Only

Use when you only need to know something **exists** in the environment:

<!-- typecheck -->
```typescript
import { Schema, Context, Effect } from 'effect';

class PaymentIntent extends Schema.Class<PaymentIntent>('PaymentIntent')({
	id: Schema.String,
	serial: Schema.String,
	amount: Schema.BigInt
}) {}

// Witness - a serial number exists
export class Serial extends Context.Service<Serial, string>()('Serial') {}

const createPaymentIntent = Effect.gen(function* () {
	const serial = yield* Serial; // Pull from environment
	return new PaymentIntent({ id: 'payment-1', serial, amount: 100n });
});

// Type: Effect<PaymentIntent, never, Serial>
```

## Capability: Behavior

Use when you need **operations**:

<!-- typecheck -->
```typescript
import { Schema, Context, Effect } from 'effect';

class PaymentIntent extends Schema.Class<PaymentIntent>('PaymentIntent')({
	id: Schema.String,
	serial: Schema.String,
	amount: Schema.BigInt
}) {}

// Capability - can generate/validate
export class SerialService extends Context.Service<
	SerialService,
	{
		readonly next: Effect.Effect<string>;
		readonly validate: (s: string) => boolean;
	}
>()('SerialService') {}

const createPaymentIntent = Effect.gen(function* () {
	const svc = yield* SerialService;
	const serial = yield* svc.next; // Effectful generation
	return new PaymentIntent({ id: 'payment-1', serial, amount: 100n });
});

// Type: Effect<PaymentIntent, never, SerialService>
```

## Decision Framework

| Need                     | Pattern    |
| ------------------------ | ---------- |
| Just presence/value      | Witness    |
| Operations/generation    | Capability |
| Precondition marker      | Witness    |
| Side effects             | Capability |
| Multiple implementations | Capability |
| Mocking behavior         | Capability |
| Correlation ID           | Witness    |
| Transaction context      | Witness    |
| Logger                   | Capability |
| Database                 | Capability |

## When to Use Witness

Good fits:

- **Request ID** - must exist for tracing
- **Transaction context** - must be established
- **Tenant/Region** - required for data boundary
- **Pre-validated tokens** - already verified

## When to Use Capability

Good fits:

- **Serial generation** - create/validate operations
- **Clock** - `now()` operation
- **Logger** - structured logging methods
- **Database** - query/transact operations
- **HTTP clients** - fetch/post operations

## Testing Implications

Witnesses are trivial to provide:

<!-- typecheck -->
```typescript
import { Context, Effect } from 'effect';

declare const myProgram: Effect.Effect<unknown, never, Serial>;
class Serial extends Context.Service<Serial, string>()('Serial') {}

const test = myProgram.pipe(Effect.provideService(Serial, 'test-serial-123'));
```

Capabilities need implementation:

<!-- typecheck -->
```typescript
import { Context, Effect } from 'effect';

declare const myProgram: Effect.Effect<unknown, never, SerialService>;
class SerialService extends Context.Service<
	SerialService,
	{
		readonly next: Effect.Effect<string>;
		readonly validate: (s: string) => boolean;
	}
>()('SerialService') {}

const test = myProgram.pipe(
	Effect.provideService(SerialService, {
		next: Effect.succeed('test-serial-123'),
		validate: () => true
	})
);
```

## Coupling Strategy

**Rule of thumb**: Remove non-essential fields from schema, inject via witness instead.

**Ask yourself:** Does this need to be persisted/serialized?

- **No** → Remove from schema, inject via witness
- **Yes** → Keep in schema

<!-- typecheck -->
```typescript
import { Schema, Context, Effect, Clock } from 'effect';
import * as Arr from 'effect/Array';

class LineItem extends Schema.Class<LineItem>('LineItem')({
	price: Schema.BigInt,
	quantity: Schema.Int
}) {}
declare const generateId: Effect.Effect<string>;
const calculateTotal = (items: ReadonlyArray<LineItem>) =>
	Arr.reduce(items, 0n, (total, item) => total + item.price * BigInt(item.quantity));

// ✅ Domain model - only persisted data
export class Order extends Schema.Class<Order>('Order')({
	id: Schema.String,
	items: Schema.Array(LineItem),
	total: Schema.BigInt
	// No correlationId - not persisted!
	// Persist a creation timestamp here too if audit/replay needs it.
}) {}

// Witnesses for runtime context
class CorrelationId extends Context.Service<CorrelationId, string>()(
	'CorrelationId'
) {}
class RequestId extends Context.Service<RequestId, string>()('RequestId') {}

// Use in code, not in data
const createOrder = Effect.fn('Order.create')(function* (items: ReadonlyArray<LineItem>) {
	const correlationId = yield* CorrelationId; // For tracing
	const requestId = yield* RequestId; // For logging
	const timestamp = yield* Clock.currentTimeMillis; // For timestamp

	yield* Effect.logInfo({
		message: 'Creating order',
		correlationId, // Used for tracing
		requestId, // Used for logging
		timestamp
	});

	// Data only contains what's persisted
	return new Order({
		id: yield* generateId,
		items,
		total: calculateTotal(items)
	});
});

// Type: Effect<Order, never, CorrelationId | RequestId>
```

**Benefits:**

- Minimal schemas (only persisted data)
- Context values available when needed
- Easy to test with different context
- Can add/remove context without schema changes
- Explicit dependencies in type signatures

Choose witness for simplicity, capability for flexibility.
