---
name: backend-integrations
description: "Calling other services and being called by them: one typed client per service, timeouts per call, retries with backoff and jitter only when safe, circuit breakers, provider rate limits and pagination, sandbox and live keys, receiving webhooks (raw-body signatures, replay windows, idempotent, fast, unordered), sending webhooks (signing, retries, delivery logs, disabling), payments with Stripe as the example, transactional email and deliverability, AI APIs, storage. Read before integrating a third-party API, a payment provider, an email service or webhooks."
---

# Other services

The generated integration calls the provider's URL from five places with no
timeout, retries a payment `POST` until it charges twice, trusts a webhook
nobody signed, marks an order paid because the browser came back to
`/success`, and sends email inside the request. One part of the backend; the
whole is in the `backend` skill.

## 1. One client per service

- Each service gets one module (`integrations/xendit.ts`,
  `payments/midtrans.py`) that builds requests, signs them, parses replies
  into your own types and maps the provider's errors to yours. The rest of
  the code calls that module, never the provider's URLs directly.
- The provider's official SDK when it is maintained; otherwise the project's
  HTTP client. Not a second HTTP library.
- Typed methods named for what the app needs (`createInvoice(order)`), the
  reply validated at the edge so a changed field fails loudly in one place,
  and the provider's ids stored beside yours.

```ts
export async function quote(req: QuoteRequest): Promise<Quote> {
  const res = await fetch(`${cfg.courier.baseUrl}/v2/quotes`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${cfg.courier.apiKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify(toCourierQuote(req)),
    signal: AbortSignal.timeout(10_000),
  });
  const status = res.status;
  if (status === 429 || status >= 500) throw new ProviderUnavailable("courier", status);
  if (!res.ok) throw new ProviderRejected("courier", status, await res.text()); // log only
  return fromCourierQuote(CourierQuote.parse(await res.json()));
}
```

## 2. Every call has limits

- A timeout on every outbound request: a few seconds to connect, 10 to 30
  seconds in total unless the provider documents longer. A call with no
  timeout can hold a request, a worker and a connection forever. Defaults do
  not save you: Go's `http.DefaultClient` and Python's `requests` wait
  forever, Node's `fetch` for minutes; httpx stops at 5 seconds. Set it:
  `AbortSignal.timeout(10_000)`, `httpx.Timeout(10.0, connect=3.0)`,
  `http.Client{Timeout: 10 * time.Second}` with the request's context.
- Inside a request, the call's timeout fits in what is left of the request's
  own deadline.
- Retry only what is safe and may succeed: a timeout, a lost connection,
  `429` and `5xx`, with exponential backoff and jitter, honouring
  `Retry-After`, three attempts in a request and more in a job. A `POST` is
  retried only with an idempotency key the provider honours.
- Retry at one layer. An SDK that retries (the OpenAI and Anthropic SDKs
  retry twice by default) inside your retry inside a job's retry turns one
  outage into dozens of calls per request.
- A circuit breaker for a dependency called often: after repeated failures
  (half of the last 20 calls, say) fail fast for 30 seconds, then let one
  call test it. opossum (Node), resilience4j (Java), Polly or
  `Microsoft.Extensions.Http.Resilience` (.NET), sony/gobreaker, pybreaker.
- A request does not wait on a slow provider when it need not: queue the
  call (`backend-jobs`) and let the client see the state.
- When a provider is down, the rest of the app keeps working, and the
  feature that needs it says so clearly.

## 3. The provider's limits and pages

- Stay under its rate limit on purpose: one limiter shared by every instance
  (a token bucket in Redis, or the queue's limiter in `backend-jobs`), an
  eye on its `X-RateLimit-Remaining` or equivalent, and a `429` answered by
  waiting for `Retry-After`. Its batch endpoints instead of a thousand
  single calls.
- Lists followed page by page with its cursor (`starting_after`,
  `next_page_token`, `Link: rel="next"`) or the SDK's auto-pagination, with a
  stop condition and a maximum.
- A long sync keeps its cursor (and an `updated_since` mark for the next
  run) in a table, so it resumes after a crash instead of starting over.

## 4. Keys and sandboxes

- Keys and endpoints from config (`backend-observability`), with the sandbox
  in development and tests and the live one only in production; a live key
  never in the repository, a test, or a log.
- The process refuses to start with a live key outside production, or a test
  key in it, where the prefix tells (`sk_live_`, `sk_test_`).
- Restricted keys with only the permissions used (Stripe's `rk_` keys, scoped
  tokens elsewhere), one per environment and service, so each can be rotated
  or revoked alone.
- Tests never call the real provider: fake it at the HTTP layer (MSW, respx,
  WireMock, `httptest`) with responses recorded from the sandbox
  (`backend-testing`).

## 5. Receiving webhooks

- Verify the signature on the raw body, before parsing, with the provider's
  method (an HMAC with the shared secret, compared in constant time), and
  refuse a timestamp older than about five minutes. An unsigned or invalid
  call gets `400` or `401` and does nothing.
- Deduplicate by the event id: providers deliver at least once, often twice.
  Store the ids handled, and do nothing for one already seen.
- Answer `2xx` within a few seconds, then do the work in a job. A slow
  handler gets retried and runs twice.
- Do not trust the payload's amounts or state blindly for anything that
  matters: fetch the object from the provider's API, or compare with your own
  records.
- The endpoint takes no session, cookie or CSRF check (the signature is the
  check), and is rate-limited like the rest.
- Order is not guaranteed: `updated` can come before `created`, an old event
  after a new one. Compare the event's time or the object's version with
  what you stored and drop older ones, or fetch the current object.
- Answer `2xx` to duplicates and to types you do not handle, or they are
  retried for days. Store the raw event first (an inbox table, unique on its
  id) so a failed job can be replayed.

```ts
import { createHmac, timingSafeEqual } from "node:crypto";

app.post("/webhooks/courier", async (c) => {
  const raw = Buffer.from(await c.req.arrayBuffer()); // the exact bytes, unparsed
  const ts = c.req.header("x-timestamp") ?? "";
  if (!(Math.abs(Date.now() / 1000 - Number(ts)) <= 300)) return c.body(null, 400);
  const expected = createHmac("sha256", cfg.courier.webhookSecret)
    .update(`${ts}.`)
    .update(raw)
    .digest();
  const given = Buffer.from(c.req.header("x-signature") ?? "", "hex");
  const valid = given.length === expected.length && timingSafeEqual(given, expected);
  if (!valid) return c.body(null, 401);
  const event = JSON.parse(raw.toString("utf8"));
  if (await inbox.insertNew(event.id, event)) await jobs.add("courier-event", { id: event.id });
  return c.body(null, 204); // duplicates too, so the sender stops retrying
});
```

- Per provider: Stripe's `stripe.webhooks.constructEvent(raw, signature,
  secret)`; the Standard Webhooks libraries for Svix-style senders; Midtrans
  by its `signature_key` (SHA-512 of order id, status code, gross amount and
  server key) and then its status API; Xendit by the `x-callback-token`
  header. The raw body: `express.raw()` on that route, `await req.text()` in
  Next.js, `await request.body()` in FastAPI, `$request->getContent()`,
  `request.raw_post`.

## 6. Sending webhooks

- Sign each delivery (an HMAC of the timestamp and body in a header), include
  an event id and type, retry with backoff for a day or so, and let the
  receiver see and replay failed deliveries.
- Never deliver to an address a user entered without the SSRF checks in
  `backend-security`.
- Use the Standard Webhooks format rather than inventing one: `webhook-id`,
  `webhook-timestamp` and `webhook-signature` headers (`v1,` then the base64
  HMAC-SHA256 of `id.timestamp.body`), a secret per endpoint, and a rotation
  period in which both secrets sign.
- The body is `{ "id", "type": "order.paid", "created", "data" }`, with the
  object's id and a small snapshot; the receiver fetches the rest from your
  API.
- Delivered from a queue per endpoint, so one slow receiver holds up no
  other: a 10 to 15 second timeout, redirects not followed, any `2xx` a
  success, retries at growing gaps (5 s, 5 min, 30 min, 2 h, 5 h, 10 h).
- A delivery log the customer sees (time, event, status, duration, the start
  of the response) with a replay button. An endpoint failing for days is
  disabled and its owner emailed. Svix or Hookdeck sell all of this.

## 7. Payments

- The provider's hosted checkout or SDK; card numbers never touch your
  server. With Stripe's Checkout or Elements the site stays in the lightest
  PCI scope (SAQ A); you store its customer, payment method and intent ids,
  at most the brand and last four digits.
- Amounts in the smallest unit, in the currency the provider expects, created
  on the server from your own prices, never from the client's total.
- The order is paid when the provider's webhook (verified, section 5) or an
  API check says so, not when the browser returns to a "success" page.
- An idempotency key on every create or capture, so a retry cannot charge
  twice.
- With Stripe: a PaymentIntent (or Checkout Session) created on the server
  per payment attempt, its id stored on the order, confirmed in the browser
  with the Payment Element and its `client_secret`; fulfilled on
  `payment_intent.succeeded` (or `checkout.session.completed` with
  `payment_status` `paid`, plus `checkout.session.async_payment_succeeded`
  for slower methods); `payment_intent.payment_failed`, `charge.refunded`
  and `charge.dispute.created` handled as well.

```ts
const intent = await stripe.paymentIntents.create(
  { amount: order.totalMinor, currency: order.currency, metadata: { orderId: order.id } },
  { idempotencyKey: `order-${order.id}-attempt-${order.paymentAttempt}` },
);
```

- Refunds, captures and disputes go through the same module, each with an
  idempotency key and an entry in your ledger (`backend-data`).
- Test with the provider's test cards and events: `stripe listen
  --forward-to localhost:3000/webhooks/stripe`, then `stripe trigger
  payment_intent.succeeded`.

## 8. Email

- A transactional provider (Resend, Postmark, SES, Mailgun) through its SDK,
  sent from a job, never inside the request.
- Templates with the text through i18n (the `i18n` skill) in the recipient's
  language, a plain-text part, and the sender's domain set up with SPF, DKIM
  and DMARC.
- In development, a catcher (Mailpit, the provider's sandbox), never real
  inboxes.
- The DNS: SPF including the provider (`v=spf1 include:amazonses.com ~all`),
  DKIM with 2048-bit keys from the provider's records, DMARC starting at
  `v=DMARC1; p=none; rua=mailto:dmarc@example.com` and tightened to
  `quarantine`, then `reject`, once the reports are clean. Gmail and Yahoo
  require all three from bulk senders, and for marketing a one-click
  unsubscribe (RFC 8058) and a spam rate under 0.3%.
- Transactional and marketing mail from separate subdomains or streams
  (`mail.example.com`, `news.example.com`), so a campaign's complaints never
  delay a password reset.
- Bounces and complaints arrive by webhook: a hard bounce or a complaint
  puts the address on a suppression list checked before every send.
- Links are built from the configured base URL, never the request's `Host`
  header; tokens in them are single use (`backend-auth`).

## 9. AI model APIs

- The key on the server, the model id in config; streamed to the client for
  long answers (`backend-realtime`), with a timeout on the first token (30
  to 60 seconds) and on the whole, `max_tokens` on every call, and the input
  bounded before it is sent.
- Retries on `429`, `5xx` and overload responses (Anthropic's `529`),
  honouring `retry-after`, counted with the SDK's own two.
- Cost: the `usage` of each response logged per user and tenant, a spend cap
  per user per day, an alert on the daily total; prompt caching where the
  provider has it.
- The output is untrusted input: checked against a schema when it should be
  structured, never run as code, SQL or a shell command, never a URL fetched
  without the SSRF checks.
- Prompt injection: text from users, web pages, emails and files can carry
  instructions. Tools the model calls get the least power the feature needs,
  act as the user (never as an admin), and wait for a person before anything
  destructive or costly.
- Prompts and answers hold personal data: not logged in full, kept only as
  long as needed, and sent only to providers whose data terms the product
  accepts.

## 10. Files

- Files in object storage (S3, R2, GCS, Supabase Storage) with uploads and
  downloads through short-lived signed URLs; the app keeps the key and the
  metadata, not the bytes. The details are in `backend-files`.

## Check it

- Every outbound call you added has a timeout: list them with
  `rg -n 'fetch\(|axios|requests\.|httpx\.|http\.(Get|Post|NewRequest)' src`.
- Against a fake: a `503` retries with backoff, a `400` does not, a hang
  ends at the timeout.
- A webhook with a bad signature gets `401`, an old timestamp `400`, and the
  same event twice is processed once.
- A payment with test keys turns the order paid only when the webhook
  arrives; the email lands in Mailpit with both parts and working links.

## Avoid

Provider URLs called from all over the code; a call with no timeout;
retrying a payment `POST` with no idempotency key; a webhook handled without
checking its signature, handled twice, or handled slowly inside the request;
"payment successful" from the redirect alone; live keys in tests; an email
sent inside the request; retries stacked at three layers; webhooks parsed
before the signature check; a webhook sent to a user's URL unchecked; model
output run as code; full prompts with personal data in the logs.
