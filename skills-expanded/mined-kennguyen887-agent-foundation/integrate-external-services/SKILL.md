---
name: integrate-external-services
description: Use when integrating a third-party/external system — calling a vendor API (anti-corruption adapter behind your own interface, resilient HTTP with circuit breaker + retry/backoff, outbound HMAC request signing, idempotency keys), receiving inbound webhooks (raw-body capture, signature verification, idempotent fast-ack-then-enqueue, vendor→internal event mapping), or exposing a partner/public API edge (client-credentials + token introspection + scopes, API-key role guard, client→tenant mapping). NestJS/TS reference, framework-flexible. For service-to-service calls inside your own platform, see integrate-internal-services.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Integrate external services

Integrating systems you don't own — calling vendor APIs, receiving their webhooks, and exposing a
partner/public edge. Examples NestJS/TS, neutral domain; vendors are "Provider A/B", "the payment
gateway", "the identity provider". principle → **▸ Example** → **▸ Other stacks**. For calls between
your own services (RPC, fan-out, cross-service reads), see `integrate-internal-services`.

## Core principle
**An external system is untrusted and unreliable.** Wrap it behind an interface you own (so it's
swappable and your domain never speaks vendor-ese), make every outbound call resilient (timeout +
retry + circuit breaker), and treat every inbound call (webhook, partner request) as hostile until
verified. Never let a vendor's schema, downtime, or duplicate delivery leak into your core.

## 1. Anti-corruption adapter — one interface, many providers
- **Wrap each external system behind a domain interface your code owns.** Each vendor gets an impl
  that translates vendor schema ↔ your DTOs and vendor errors → your errors. A **factory/registry**
  selects the impl by provider type; callers depend on the interface, never on a vendor SDK.
  ```ts
  export interface PaymentGateway {
    getProvider(): ProviderType;
    createPayment(input: CreatePaymentInput): Promise<PaymentResult>;   // your DTOs, not the vendor's
    refund(input: RefundInput): Promise<RefundResult>;
  }
  // providers/index.ts barrels StripeGateway, RapydGateway, CyberSourceGateway, UobGateway…; a factory picks by ProviderType
  const gateway = this.gatewayFactory.for(order.providerType);          // caller is provider-agnostic
  ```
- **Provider selection + fallback:** choose by config/region/capability; on a provider failure, fall
  back to a secondary so one vendor's outage isn't your outage.
- **Route by capability with a method→gateway factory.** Some methods only work on certain gateways, so
  a factory maps **payment-method type → gateway** with precedence (feature-flag > env > default) — e.g.
  Apple Pay / Google Pay → a gateway that accepts device-wallet tokens; WeChat Pay / Alipay → another.
- **Device-wallet payments (Apple Pay / Google Pay):** the wallet returns an **opaque payment token** —
  forward it to the gateway and **never touch raw card data** (PCI scope stays with the wallet +
  gateway). Apple Pay also needs a server **merchant-validation** endpoint to start the session.
- **Same pattern for outbound messaging** — email / SMS / push behind one `send()` facade (e.g. Twilio
  for SMS, an email provider, a push service), the channel chosen at call time; callers don't know which
  vendor delivers. (Channel content rendering — a template + data → subject/html, per locale — sits just
  before `send()`.)
▸ *Other stacks:* hexagonal **ports & adapters**; a Strategy per provider chosen by a factory.
Principle: your interface is the contract; vendors are swappable plugins translated at the boundary.

## 2. Resilient outbound HTTP — circuit breaker + retry + timeout
- **Route every outbound call through one client** that wraps the HTTP lib with a **circuit breaker**
  (open on repeated failure → fail fast → half-open probe → close), **retry with backoff (+ jitter)**,
  a **per-call timeout**, and a **fallback**. Log breaker state transitions. Don't scatter raw
  `axios`/`fetch` + ad-hoc try/catch across services.
  ```ts
  // one breaker per method; recursive retry with growing delay; fallback when the circuit is open
  this.breakers = { GET: new CircuitBreaker(client.get, opts), POST: new CircuitBreaker(client.post, opts) /* … */ };
  breaker.on('open',  () => log.warn('circuit open'));
  breaker.on('close', () => log.info('circuit closed'));
  private async retry(fn, n = 0) {
    try { return await fn(); }
    catch (e) { if (n >= this.maxRetries) throw e; await delay(n + 1); return this.retry(fn, n + 1); }
  }
  ```
▸ *Other stacks:* resilience4j (Java), Polly (.NET), opossum/cockatiel (Node), tenacity (Python).
Principle: **timeout + retry-with-backoff + circuit breaker + fallback**, centralized in one client.

## 3. Outbound auth — request signing + idempotency
- **Sign outbound requests when the vendor requires it:** HMAC over a **canonical string** (e.g.
  `method + path + salt + timestamp + body`), with a small **clock-skew buffer** on the timestamp and a
  **fresh random salt** per request; attach the signature + access-key + salt + timestamp headers.
  Credentials come from config, never hard-coded.
  ```ts
  const timestamp = String(Math.floor(Date.now() / 1000) - SKEW);   // small backward buffer
  const salt = randomHex(12);
  const toSign = `${method}${path}${salt}${timestamp}${accessKey}${secretKey}${body}`;
  const signature = base64(hmacSha256(toSign, secretKey));
  ```
- **Send an idempotency key on outbound *mutating* calls** (create-charge, create-refund) so a retry
  after a timeout doesn't double-act — derive it from your own stable id, not a random per-attempt value.
▸ *Other stacks:* the same canonical-string HMAC (AWS SigV4 is this idea); an `Idempotency-Key` header
is widely supported by payment/commerce APIs.

## 4. Inbound webhooks — verify, dedupe, fast-ack, map
- **Capture the RAW body** for the webhook route **before JSON parsing**, so signature verification
  runs over the exact bytes received — re-serialized JSON won't match the vendor's HMAC.
  ```ts
  app.use('/webhooks/stripe', express.raw({ type: 'application/json' }));   // raw bytes for Stripe's constructEvent, before global json parse
  ```
- **Verify in a guard before the handler runs** — recompute the HMAC (e.g. Rapyd: HMAC over
  `url+salt+timestamp+body`) or call the vendor SDK's verifier (e.g. Stripe's `webhooks.constructEvent`)
  and reject on mismatch; optionally enforce a **timestamp window** (replay protection).
  ```ts
  @Injectable() export class WebhookSignatureGuard implements CanActivate {
    canActivate(ctx: ExecutionContext) {
      const { headers, body } = ctx.switchToHttp().getRequest();
      const expected = base64(hmacSha256(canonical(headers, body), this.secret));
      if (expected !== headers.signature) throw new BadRequestException('signature mismatch');
      return true;
    }
  }
  ```
- **Idempotent processing** — dedupe by the **vendor's event id** (a seen-events row or Redis `SET NX`);
  vendors redeliver the same event.
- **Fast-ack-then-enqueue** — verify, hand off to a queue/command, **return 200/204 immediately**; do
  the heavy work async in a worker. A slow webhook handler triggers vendor retries (and duplicates).
  ```ts
  @Post('/webhooks/stripe') @UseGuards(WebhookSignatureGuard) @HttpCode(204)
  handle(@Body() evt: VendorEvent) { return this.commandBus.execute(new EnqueueWebhookCommand(evt)); } // dispatch, don't process inline
  ```
- **Map vendor event type → your internal event/command via a table** — don't `switch` on vendor
  strings deep in business code:
  ```ts
  const VENDOR_TO_INTERNAL = new Map([['payment.completed', EVT.PAYMENT_SETTLED], ['payment.failed', EVT.PAYMENT_FAILED]]);
  ```
▸ *Other stacks:* identical everywhere — raw-body verify, dedupe by event id, ack fast + process async,
translate the vendor event into your own domain event.

## 5. Partner / public API edge (BFF / gateway)
- **Authenticate partners with client-credentials:** client id + secret → issue a token; **introspect /
  validate the token per request and enforce scopes**. **Map the client → an org/tenant id and inject
  it** so every downstream read/write is tenant-scoped (a partner can't reach another's data).
  ```ts
  const claims = await this.idp.introspect(req.headers.authorization);   // delegate to the identity provider (e.g. Keycloak introspection / JWKS)
  req.tenantId = this.clientToTenant(claims.clientId);                   // config-driven mapping
  if (!hasScope(handlerScopes, claims.scopes)) throw new ForbiddenException();
  ```
- **For simpler machine endpoints** (mobile, internal hooks) an **API-key role guard**: a metadata
  decorator declares required roles on the handler; the guard checks `x-api-key` against a configured
  key→roles set.
  ```ts
  @Post('/exists') @UseGuards(ApiKeyGuard) @ApiKeyRoles(Role.MOBILE)
  checkExists(@Query() q: ExistsDto) { /* … */ }
  ```
- **Keep the external contract stable and decoupled from internal models** — version it, map to
  internal DTOs at the edge, and **rate-limit per client**. Don't expose internal entity shapes to partners.
▸ *Other stacks:* OAuth2 client-credentials at any gateway (Kong, Apigee, API Management); API keys +
scopes. Principle: authenticate the client, resolve its tenant, enforce scope, serve a stable
versioned contract.

## 6. Bulk delivery tolerates partial failure
- **Sending to many recipients/targets uses settle-all fan-out, not fail-fast** — collect successes,
  log + retry the failures, report which failed; one bad recipient must not abort the batch. **Chunk +
  pace** large batches (N at a time + a small delay) so you don't trip the vendor's rate limit.
  ```ts
  const results = await Promise.allSettled(recipients.map((r) => this.notifier.send(r)));
  const failed = results.filter((x) => x.status === 'rejected');   // log + schedule retry, don't throw
  ```
  (Large data imports → `import-data-from-csv`; in-process queues → `background-jobs-and-caching`.)
▸ *Other stacks:* `Promise.allSettled` / `errgroup` collecting per-item errors / `asyncio.gather(return_exceptions=True)`.

## Vendor recipes (step-by-step)
The sections above are the reusable *pattern*. Concrete **step-by-step implementation guides** for
specific providers live in [`references/`](./references/) and load **on demand** — they don't add to
this skill's always-on cost. Each recipe is "how to wire *this* vendor" for the patterns above, with
its steps mapped back to the section numbers.
- [`references/stripe.md`](./references/stripe.md) — card + wallet payments (PaymentIntents), webhooks, testing, gotchas.
- [`references/rapyd.md`](./references/rapyd.md) — card + PayNow via Rapyd Collect; HMAC-signed requests; hosted card tokenization; webhook HMAC.
- [`references/cybersource.md`](./references/cybersource.md) — card + tokenization (microform / Secure Acceptance) + 3-D Secure; signed-JWT (P12) auth.
- [`references/uob.md`](./references/uob.md) — PayNow QR collection; mutual-TLS + JWS-signed requests; encrypted + signed webhooks.
- [`references/twilio.md`](./references/twilio.md) — Twilio SMS behind the notification facade; send via a Messaging Service; status webhook (`X-Twilio-Signature`).

## Verification
- **Vendors behind your interface:** `grep -rn "from 'stripe'\|@rapyd\|cybersource\|new Twilio" src --include='*.ts' | grep -v "/providers/"` → empty (vendor SDKs live only in adapter/provider files); callers resolve an impl via the factory, typed to your own `PaymentGateway`/facade interface.
- **One resilient outbound client:** `grep -rn "axios\.\|fetch(" src --include='*.ts' | grep -vE "http-client|resilient|breaker"` → empty (no scattered raw calls); `grep -rn "CircuitBreaker" src` present. Point a call at a dead URL → after N failures the breaker **opens** (logs `circuit open`) and calls fail fast (< the per-call timeout) instead of hanging. Mutating calls send an `Idempotency-Key`.
- **Webhooks verify → ack-fast → async:** POST with a tampered body/signature → `400/401` (guard rejects; raw body captured — `grep -n "express.raw\|rawBody" src`); a valid one returns `204` immediately; redeliver the same vendor event id twice → the side effect runs **once**.
- **Partner edge is scoped:** call with no/expired token → `401`; valid token but missing scope → `403`; valid → `200` and the result is the caller's tenant only (a second client can't read the first's rows).
- **Bulk tolerates partial failure:** `grep -rn "allSettled" src` (settle-all fan-out, not `Promise.all` fail-fast); send a batch with one bad recipient → the batch completes, the failure is logged/retried, the rest succeed.

## Related
- `integrate-internal-services` — the worker that processes the enqueued webhook job; the service mesh.
- `write-service-code` — §9 (client-proxy lifecycle for internal calls; transactions + compensation),
  §7 (logging — **mask vendor creds + PII**), §3 (nullability).
- `background-jobs-and-caching` — the queue behind fast-ack; Redis `SET NX` for webhook dedupe.
- `import-data-from-csv` (bulk ingest) · `release-safety` (don't break the partner contract) · `code-conventions`.
