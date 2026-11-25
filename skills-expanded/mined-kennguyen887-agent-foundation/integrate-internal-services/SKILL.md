---
name: integrate-internal-services
description: Use when one backend service calls or consumes from another inside the same platform — synchronous RPC (a uniform request/response envelope + server-side message handlers), SNS→SQS event fan-out (one topic → many subscriber queues), async-consumer robustness (ack vs DLQ + lifecycle hooks), cross-service reads (batch + cache, no network N+1), identity/context propagation across hops, and the worker/consumer service shape (no HTTP, graceful drain). NestJS/TS reference, framework-flexible. Complements write-service-code §6 (single producer→consumer events) and §9 (client-proxy lifecycle).
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Integrate internal services

How services in the SAME platform talk to each other — sync RPC, async fan-out, robust consumers,
cross-service reads, context propagation, and the worker shape. Examples NestJS/TS, neutral
`listing`/`order`/`payment` domain; `<Svc>` is a placeholder. principle → **▸ Example** → **▸ Other
stacks**. The *client* side of a call (proxy lifecycle/retries/base `send()`) and the single
producer→consumer event live in `write-service-code` §6/§9 — this skill is the rest of the mesh.
For third-party/vendor systems and inbound webhooks, see `integrate-external-services`.

## When to use
You're exposing an operation for another service to call, fanning one event out to many subscribers,
hardening a queue consumer, resolving data that lives in another service, or building a pure worker.

## 1. Synchronous RPC — server side + a uniform envelope
- **Expose operations via a message-pattern handler** (the reply side); the *client* side (proxy
  lifecycle, retries, base `send()`) is `write-service-code` §9. Keep the handler thin — delegate to
  a command/query bus.
- **Wrap every request and reply in a stable envelope, never bare payloads.** Request carries
  `{ id (correlation), service (caller), pattern, input }`; reply carries
  `{ success, data, message, statusCode }`. One shared **interceptor** builds the success reply + logs
  `id`/`pattern`; one shared **exception filter** maps a thrown error to a failed envelope — so every
  caller gets the same shape and a trace id, always.
  ```ts
  @Controller()
  @UseInterceptors(MicroserviceInterceptor)   // wraps return value → { success:true, data }
  @UseFilters(RpcExceptionFilter)             // maps throw → { success:false, message, statusCode }
  export class ListingRpcController {
    @MessagePattern(LISTING_PATTERNS.getByIds)
    getByIds(req: RpcRequest<GetByIdsInput>): Promise<ListingDto[]> {
      return this.queryBus.execute(new GetListingsByIdsQuery(req.input));
    }
  }
  ```
- **Version the contract** (pattern names are constants in a shared registry); changing a reply shape
  is a breaking change for callers — add a field, don't repurpose one.
▸ *Other stacks:* gRPC (status codes + metadata for correlation), a JSON-RPC envelope, Thrift. The
principle is universal: a versioned, uniform request/response contract with a correlation id and an
explicit error shape, not ad-hoc payloads.

## 2. Async fan-out — one event, many subscribers (topic → queues)
- For **one-to-many**, publish to a **topic**; each subscriber owns its **own queue** subscribed to
  that topic, so subscribers fail/scale/retry independently. (One-to-one producer→consumer + the
  outbound mapped-subset payload is `write-service-code` §6.)
- **A central registry maps topic → its subscriber queue names** — no scattered string literals; the
  producer broadcasts to the topic and never names a subscriber.
  ```ts
  export const TOPICS = { ORDER_CREATED: 'order-created' } as const;
  export const SUBSCRIBERS = {
    [TOPICS.ORDER_CREATED]: {                 // one topic, N independent queues
      grantLoyaltyPoints: 'grant-loyalty-points',
      sendOrderReceipt:   'send-order-receipt',
    },
  };
  await this.events.broadcast({ event: TOPICS.ORDER_CREATED, payload: { orderId } });  // no subscriber knowledge
  ```
▸ *Other stacks:* Kafka topic + consumer groups, Google Pub/Sub topic→subscriptions, RabbitMQ
exchange→queues. Principle: producer → topic, fan-out to independent subscriber queues, names in a
registry, not inline.

## 3. Consumer robustness — ack vs DLQ + lifecycle hooks
- **Segregate failures** — the single most important consumer rule (refines §6's "don't throw"):
  - **Permanent** failure (validation, not-found, malformed payload) → **log + ack/return** so it does
    NOT loop forever.
  - **Transient** failure (downstream down, timeout, deadlock) → **rethrow** so the broker retries and
    eventually routes to a **DLQ**.
  - Never blanket-swallow (you silently lose retriable work) and never blanket-throw (permanent
    failures become poison messages that loop until they expire).
- **Centralize in a base handler (template method):** the subclass implements `execute(payload)`; the
  base parses, runs, and applies the ack-vs-rethrow rule once. Subscribe to **lifecycle events**
  (received / processed / error / timeout) for metrics + replay visibility without touching business code.
  ```ts
  abstract class BaseConsumer {
    abstract execute(payload: unknown): Promise<void>;
    async handleMessage(msg: Message) {
      try { await this.execute(parse(msg.Body)); }
      catch (e) {
        if (e instanceof ValidationError || e instanceof NotFoundError) { this.log.warn('drop', e); return; } // ack
        throw e;                                                                                               // → retry/DLQ
      }
    }
    @ConsumerEvent('processing_error') onError(e: Error, m: Message) { this.log.error('consumer error', { e, m }); }
  }
  ```
▸ *Other stacks:* same — classify exceptions into terminal vs retriable; ack the terminal ones,
nack/redeliver→DLQ the retriable ones; emit metrics on consumer lifecycle.

## 4. Cross-service reads — batch + cache, never N+1 across the network
- **Resolving ids → data from another service in a loop is an N+1 over the network** (latency × N, and
  it amplifies that service's load). Expose and call a **bulk lookup** — send all ids, get all rows in
  one round trip.
- **Cache another service's response locally** (cache-through with a TTL) and **invalidate on the
  source's change event** (subscribe to it). On the hot path you read your own cache/replica, not a
  synchronous hop.
  ```ts
  // bulk, cached, invalidated by the owner's event
  getOrgs(ids: string[]) {
    return this.cache.wrap(`${PREFIX.ORG}:${stableKey(ids)}`,
      () => this.orgClient.send(ORG_PATTERNS.getByIds, { ids }),   // ONE call for all ids
      TTL);
  }
  @EventsHandler(OrgUpdatedEvent) // owner changed → drop our cache
  handle(e) { return this.cache.del(`${PREFIX.ORG}:*`); }
  ```
▸ *Other stacks:* a batch endpoint (GraphQL dataloader, gRPC batch), or a local read-model/replica
fed by events (CQRS read side). Principle: batch the call, cache the result, invalidate on the
source's event — don't synchronously fan out per-row.

## 5. Propagate identity & context across hops
- **Pass the caller's identity + tenant + a correlation/trace id downstream** (in the envelope `id`
  field or a header) so every hop logs the same trace and can enforce tenant scope. A downstream
  service **trusts the gateway/upstream's asserted identity** — a guard reads the injected
  `x-caller`/`x-tenant` header it was given — instead of re-authenticating end-user credentials it
  never received.
  ```ts
  @Injectable() export class CallerGuard implements CanActivate {
    canActivate(ctx: ExecutionContext) {
      const req = ctx.switchToHttp().getRequest();
      if (!req.headers['x-caller']) throw new UnauthorizedException();   // upstream must assert it
      req.caller = JSON.parse(req.headers['x-caller']);                  // { id, tenantId, roles }
      return true;
    }
  }
  ```
- **Pass the minimal claims** the downstream needs (id, tenant/org, roles), not the whole user object.
  Tenant *query*-scoping itself (intersecting the allowed set into the query) is `write-service-code` §9.
▸ *Other stacks:* W3C `traceparent` / OpenTelemetry context propagation; a short-lived signed internal
JWT asserting the caller; gRPC metadata. Principle: forward identity + trace, trust the asserted
context at the edge, scope by tenant downstream.

## 6. Worker / consumer service shape
- **A pure consumer (queue/cron worker) boots WITHOUT request routes.** Create the app, wire the
  microservice/queue consumers, expose **only a minimal health/liveness port** — no controllers, no
  Swagger. (For where files live, this is a structural variant of `structure-a-backend-service`.)
  ```ts
  const app = await NestFactory.create(WorkerModule);
  app.connectMicroservice(config.get(tcpOptions));   // queue/RPC consumers
  await app.startAllMicroservices();
  app.get(ShutdownObserver).setupGracefulShutdown(app);
  await app.listen(PORT);                            // health probe only — no business routes
  ```
- **Drain on shutdown:** flip a shutting-down flag, stop accepting new messages, let in-flight handlers
  finish (`queue.close()`, `clientProxy.close()`), then exit — a deploy must not drop work. The RPC
  interceptor **rejects new requests** (`SERVICE_UNAVAILABLE`) while draining.
▸ *Other stacks:* a Sidekiq/Celery/River worker, a Kafka consumer service, a Cloud Run/Lambda
consumer. Principle: no request server, graceful drain of in-flight work, health probe only.

## Verification
- **Uniform RPC envelope:** every reply is `{ success, data }` or `{ success:false, message, statusCode }`, never a bare payload; `@MessagePattern` handlers delegate to a bus and pattern names are imported constants (no inline string patterns). Call a handler that throws → the caller still gets a `success:false` envelope with a `statusCode` + correlation id.
- **Fan-out is topic→queues:** `grep -rn "broadcast\|TOPICS\." src` — the producer publishes to a topic and names **no** subscriber; the topic→queue registry lists each subscriber's own queue. Take one subscriber offline → the others still receive the event (independent queues).
- **Consumers classify failures:** feed a malformed payload → it's logged + **ack'd** (queue depth doesn't grow); force a transient error (downstream down) → it **rethrows** and lands in the DLQ after retries. `grep -rn "DLQ\|ValidationError\|NotFoundError" src` shows the terminal-vs-retriable split in one base handler.
- **Cross-service reads batched + cached:** id→data lookups send **all** ids in one call — no `.send(` / RPC inside a `.map(` or loop; the result goes through `cache.wrap` and an `@EventsHandler` on the owner's change event invalidates it.
- **Context propagated, worker drains:** a downstream guard rejects a call missing `x-caller`/`x-tenant` (`401`) and the same correlation id appears in logs across hops; the worker app has no business routes (`grep -rn "@Controller" src` ≈ health only) and on SIGTERM stops intake + finishes in-flight work before exit.

## Related
- `write-service-code` — §6 (single producer→consumer event + outbound mapped payload), §9 (client
  proxy lifecycle/retries, tenant query-scoping, transactions + compensation), §7 (logging).
- `background-jobs-and-caching` — Bull queues, Redis cache + idempotency, the cache-through `wrap` used in §4.
- `integrate-external-services` — third-party vendor APIs, inbound webhooks, the partner/public API edge.
- `structure-a-backend-service` — where these files live (the worker is a structural variant).
