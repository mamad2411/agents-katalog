---
name: backend-service-patterns
description: Applies hexagonal/ports-and-adapters architecture for backend services. Invoked when building a backend service, designing a Go/Node/Rust API, implementing a high-performance service, structuring a domain with ports and adapters, wiring dependency injection in a service, designing transport or persistence adapters, applying DDD in a backend context, validating input with zod, or parsing untrusted data at the adapter boundary. Also invoked when choosing or wiring an HTTP transport adapter — Fastify (Node), Gin (Go), or Axum (Rust) — as the HTTP delivery layer in a ports-and-adapters service. Ties to principles-tdd, principles-ddd, principles-pragmatic-solid, and principles-dry-kiss.
---

# Backend Service Patterns

Hexagonal architecture (ports and adapters): domain core behind interfaces, adapters for transport and persistence. Inject dependencies at the boundary. Measure before optimizing.

> **Stack profile:** the Go/Node/Rust + Gin/Fastify/Axum examples below are defaults. Before building, read `.ai/stack-profile.md` if present (see the `stack-profile` skill). If it names a different language or HTTP framework (e.g. Python/FastAPI), treat the examples as patterns to translate — research that stack's idioms first, then build to the same discipline. **Ports-and-adapters and DI are invariant** — they apply in every language; only the concrete framework changes.

## Process

**Domain core behind interfaces (ports).**
Define the domain as pure business logic with no I/O. Express every external dependency — database, HTTP client, queue, clock — as a narrow interface (port). The domain never imports transport or infrastructure packages. This enforces the boundary that `principles-ddd` requires and makes every port trivially mockable per `principles-pragmatic-solid`.

**Adapters implement ports.**
Write one adapter per external system: HTTP handler, database repository, message-queue publisher, etc. Adapters translate between the domain's types and the external system's wire format. Swapping an adapter (e.g., Postgres → SQLite in tests) costs a single constructor argument. Never let adapter concerns bleed into the domain.

**Inject at the boundary.**
Wire dependencies in `main` (or equivalent entry point), not inside domain logic. Pass interfaces, not concretions. A service constructor that accepts an interface for its repository and its event publisher can be tested without any I/O. See `principles-pragmatic-solid` — inject behind interfaces, no interface-per-class without a second implementation.

**TDD throughout.**
Every domain behavior starts with a failing test. Use test doubles (stubs/fakes) for all ports so tests run in milliseconds with no external services. Commit at green; refactor under green. Name test files by tier: TypeScript — `*.unit.test.ts` (unit), `*.integration.test.ts` (integration); Go — `*_test.go` with no build tag (unit), `*_integration_test.go` + `//go:build integration` header (integration). Use `TestSubject_Scenario_Expectation` naming for all Go test functions. See `principles-tdd` for the full tier conventions including e2e, build-tag gate, testify suite lifecycle hooks, and the required four-hook scaffold.

---

### Go

**Gin as HTTP transport adapter.**
Gin is the HTTP delivery layer — it is an adapter, not part of the domain. Initialize with `gin.New()` (not `gin.Default()`) and register only the middleware you need (`gin.Logger()`, `gin.Recovery()`). Group routes by bounded context with `router.Group("/orders")`. In each handler func, bind and validate immediately — `ctx.ShouldBindJSON(&cmd)` followed by `validate.Struct(&cmd)` (go-playground/validator with struct tags: `validate:"required,uuid4"`) — then call the domain service and map the result to a JSON response. Middleware (`router.Use(...)`) handles cross-cutting concerns: auth, request-id, tracing. Handlers must not contain domain logic; they are the HTTP face of the port.

```go
// internal/adapters/http/orders.go (transport adapter)
func (h *OrderHandler) CreateOrder(ctx *gin.Context) {
    var cmd CreateOrderCommand
    if err := ctx.ShouldBindJSON(&cmd); err != nil {
        ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    if err := h.validate.Struct(&cmd); err != nil {
        ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    order, err := h.orderService.CreateOrder(ctx.Request.Context(), cmd) // domain call
    if err != nil {
        ctx.JSON(http.StatusInternalServerError, gin.H{"error": "internal error"})
        return
    }
    ctx.JSON(http.StatusCreated, order)
}
```

**Interfaces + table-driven tests.**
Define small, behavior-focused interfaces (`Repository`, `Publisher`, `Cache`). Implement with concrete structs. Write table-driven tests for all domain logic — a `[]struct{ name, input, want }` slice makes coverage cheap and exhaustive.

**Goroutine and context discipline.**
Pass `context.Context` as the first argument to every function that does I/O. Propagate cancellation — never launch goroutines that outlive the request without a clear ownership mechanism (done channel, `errgroup`, or `sync.WaitGroup`). Goroutine leaks are subtle performance bugs; context propagation prevents them.

**Validate at the adapter boundary.**
Parse untrusted HTTP input into typed structs before passing to the domain. Use `go-playground/validator` with struct tags (`validate:"required,uuid4"` etc.) and call `validate.Struct(&cmd)` in the transport adapter. Same principle as zod in Node: validation happens at the adapter layer; the domain receives only typed, validated values.

**Error handling.**
Wrap errors with `fmt.Errorf("...: %w", err)` at every layer boundary so callers can `errors.Is`/`errors.As` without losing stack context. Domain errors should be typed values, not strings — callers pattern-match on error type, not message content.

---

### Node / TypeScript

**Fastify as HTTP transport adapter.**
Fastify is the HTTP delivery layer — it is an adapter, not part of the domain. Use Fastify's plugin system (`fastify.register`) to encapsulate routes by bounded context; each plugin owns its route prefix, schema declarations, and local decorators. Register `fastify-type-provider-zod` at the root to use zod schemas directly in route definitions — this provides automatic JSON Schema generation and a fully typed `request.body`/`request.query` without a manual `.parse()` call (ties to the zod validation pattern below). Keep handlers thin: receive the already-validated, typed input, call the domain service, map the result to a reply. Cross-cutting concerns (auth, logging, rate-limiting) go in Fastify hooks (`onRequest`, `preHandler`) or plugins registered at the root — never inside handlers.

```ts
// src/adapters/http/orders.plugin.ts (transport adapter)
import { serializerCompiler, validatorCompiler, type ZodTypeProvider } from 'fastify-type-provider-zod';
import { createOrderSchema } from '../../domain/schemas.js';

export async function ordersPlugin(fastify: FastifyInstance) {
  fastify.setValidatorCompiler(validatorCompiler);
  fastify.setSerializerCompiler(serializerCompiler);

  fastify.withTypeProvider<ZodTypeProvider>().post(
    '/orders',
    { schema: { body: createOrderSchema } },
    async (request, reply) => {
      // request.body is fully typed as z.infer<typeof createOrderSchema>
      const order = await orderService.createOrder(request.body); // domain call
      return reply.status(201).send(order);
    },
  );
}
```

**DI containers or manual injection.**
Prefer explicit constructor injection (manual DI) for services with few dependencies — it is transparent and easy to test. Use a DI container (e.g., `tsyringe`, `inversify`) only when the dependency graph is large enough that manual wiring becomes the bottleneck.

**Strict types throughout.**
Enable `strict: true` in `tsconfig.json`. Model domain types as branded primitives or discriminated unions so invalid states are unrepresentable at compile time. Avoid `any`; use `unknown` and narrow. Keep adapter types (DB row shapes, HTTP request bodies) separate from domain types — map at the adapter boundary.

**Input validation at the adapter boundary (zod).**
Parse untrusted input — HTTP request bodies, query params, message-queue payloads — with a zod schema before it reaches the domain. Use `schema.parse(raw)` to throw on invalid data or `schema.safeParse(raw)` for explicit error handling without exceptions. Derive TypeScript types directly from the schema with `z.infer<typeof schema>` — one definition, no duplication between the schema and the type. The domain core only ever receives validated, typed values; validation logic never leaks into domain functions.

```ts
// src/adapters/http/orders.ts (transport adapter)
import { z } from 'zod';

const createOrderSchema = z.object({
  customerId: z.string().uuid(),
  items: z.array(z.object({ sku: z.string(), qty: z.number().int().positive() })),
});

type CreateOrderCommand = z.infer<typeof createOrderSchema>;

// In the route handler — validate at the boundary, pass typed value to the domain:
const result = createOrderSchema.safeParse(request.body);
if (!result.success) return reply.status(400).send({ errors: result.error.flatten() });
const order = await orderService.createOrder(result.data); // domain receives CreateOrderCommand
```


**Async discipline.**
All I/O is `async/await`. Never mix raw Promises and async/await in the same call chain. Use `AbortSignal` / request-scoped cancellation for long-running operations. Handle errors at a single boundary (global middleware or a top-level `try/catch`) rather than swallowing them inside adapters.

---

### Rust

**Axum as HTTP transport adapter.**
Axum is the HTTP delivery layer — it is an adapter, not part of the domain. Build a `Router`, nest sub-routers by bounded context (`Router::new().nest("/orders", orders_router())`), and share domain services via `State<Arc<AppState>>`. Handlers are plain async functions with typed extractors: `Json<T>` deserializes the request body and returns 422 on parse failure; `State<Arc<AppState>>` injects the shared service graph. After extraction, validate immediately with `.validate()?` (the `validator` crate with `#[validate(...)]` field annotations). Handlers return `impl IntoResponse` — map domain `Result` variants to `StatusCode` + `Json`. Layer cross-cutting concerns with `tower` middleware (`TraceLayer`, `TimeoutLayer`) on the `Router`. No domain logic inside handlers.

```rust
// src/adapters/http/orders.rs (transport adapter)
use axum::{extract::State, http::StatusCode, response::IntoResponse, Json};
use validator::Validate;

async fn create_order(
    State(state): State<Arc<AppState>>,
    Json(cmd): Json<CreateOrderCommand>,
) -> impl IntoResponse {
    if let Err(e) = cmd.validate() {
        return (StatusCode::UNPROCESSABLE_ENTITY, Json(e.to_string())).into_response();
    }
    match state.order_service.create_order(cmd).await { // domain call
        Ok(order) => (StatusCode::CREATED, Json(order)).into_response(),
        Err(_) => StatusCode::INTERNAL_SERVER_ERROR.into_response(),
    }
}
```

**Traits as interfaces.**
Define a trait per port (`Repository`, `EventBus`, `Clock`). Implement for concrete types (`PgRepository`, `KafkaEventBus`). For tests, implement the trait on a simple in-memory struct. Use `async_trait` (or manual `Pin<Box<dyn Future>>`) for async methods on `dyn`-dispatched traits, since `async fn` in traits is not yet object-safe for dynamic dispatch.

**Ownership-aware design.**
Prefer `Arc<dyn Trait>` for shared service handles injected across async tasks. Avoid `Rc` in multi-threaded code. Use `tokio::sync::Mutex` sparingly — structure data access to minimize lock scope. Design the domain so owned types flow naturally; reach for shared references only at the boundary.

**Validate at the adapter boundary.**
Derive `serde::Deserialize` and `validator::Validate` on HTTP input structs, then call `.validate()?` immediately after deserialization and before passing to the domain. The `validator` crate with field-level constraints (`#[validate(email)]`, `#[validate(length(min = 1))]`) is the Rust equivalent of zod: untrusted data is rejected at the adapter layer; the domain core only ever handles valid, typed values.

**Error handling.**
Define a domain `Error` enum (or use `thiserror`) and `Result<T, Error>` at every domain function. Adapters convert external errors (`sqlx::Error`, `reqwest::Error`) into domain error variants at the adapter boundary — domain code never leaks infrastructure error types.

---

### Performance practices

**Measure first.**
Profile before optimizing. Guessing at bottlenecks wastes time and produces unmaintainable code. Add structured metrics/tracing (Prometheus, OTEL) from day one so you know where time is spent. See `principles-dry-kiss` — the simplest correct implementation wins until measurements say otherwise.

**Optimize at the boundary, not the core.**
Connection pooling, batching, caching, and serialization choices belong in adapters. Domain logic stays simple. A cache adapter wrapping a repository is a clean swap; cache logic scattered through domain functions is a maintenance hazard.

**Avoid speculative performance work.**
N+1 queries, missing indexes, and blocking I/O on a hot path are worth fixing immediately when measured. Micro-optimizations to hot loops, SIMD, or memory layout are worth investigating only after profiling shows them to be the bottleneck. See `principles-pragmatic-solid` — no premature abstraction; the same discipline applies to performance.

## Cross-references

- `principles-tdd` — TDD rhythm, test doubles for ports, commit-at-green discipline.
- `principles-ddd` — domain core isolation, bounded contexts, ubiquitous language.
- `principles-pragmatic-solid` — interface/DI discipline, interface segregation at ports, no interface-per-class without substitution need.
- `principles-dry-kiss` — measure before optimizing; no speculative abstractions; simplest correct implementation wins.
