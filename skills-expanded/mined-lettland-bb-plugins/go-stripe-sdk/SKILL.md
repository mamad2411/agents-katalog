---
name: go-stripe-sdk
description: Use when integrating Stripe in Go — checkout sessions, webhooks, signature verification, idempotency keys, test mode, subscriptions.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [go-essentials, go-chi, go-testing, security, observability-essentials]
---

# Go Stripe SDK (stripe-go)

**Iron Law: every webhook handler verifies the signature with `webhook.ConstructEvent` BEFORE reading the body as JSON. Every mutating API call carries an idempotency key. Secret keys load from Vault/env, never literal. Webhook secrets are environment-specific — test-mode and live-mode have different secrets.**

**Versions:** Current `stripe-go/v82` · No LTS series — _Major version per Stripe API version (e.g., v82 ↔ API `2024-12-18.acacia`). The Go SDK major matches the API version it speaks; bumping `v82` → `v83` is also bumping the on-the-wire API and requires reading the upgrade guide._

## Client init (pin both SDK version and API version)

```go
import (
    "github.com/stripe/stripe-go/v82"
    "github.com/stripe/stripe-go/v82/checkout/session"
    "github.com/stripe/stripe-go/v82/webhook"
)

func init() {
    stripe.Key = os.Getenv("STRIPE_SECRET_KEY")           // sk_test_... or sk_live_...
    // Pin the API version explicitly — overrides the account default so a dashboard change
    // never silently shifts response shapes under your code.
    stripe.SetAppInfo(&stripe.AppInfo{Name: "myapp", Version: "1.0.0"})
}
```

Resist initializing `stripe.Key` from a config struct loaded later — Stripe library functions read it as a package-level global. Set it once at startup, fail loud if missing.

| Source                              | Use                                                                                     |
| ----------------------------------- | --------------------------------------------------------------------------------------- |
| `os.Getenv("STRIPE_SECRET_KEY")`    | dev, simple deploys                                                                     |
| **Vault** (`secret/stripe/sk`)      | rotate without redeploy                                                                 |
| AWS/GCP KMS-decrypted env           | encrypt-at-rest, decrypt on container boot                                              |
| **Restricted keys** (`rk_live_...`) | scope to specific resources (e.g., read-only events) for background workers, audit jobs |

## Checkout Sessions vs PaymentIntents

| API                   | Use when                                                                                                                    |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Checkout Session**  | redirect to Stripe-hosted payment page; PCI-DSS scope minimized; subscriptions, one-off, embedded — the default for SaaS    |
| **PaymentIntent**     | you build the UI (Stripe Elements or your own); needed for custom flows, recurring with custom dunning, off-session charges |
| **Subscriptions API** | layered on PaymentIntents; manage via Checkout + customer portal for 95% of needs                                           |

```go
params := &stripe.CheckoutSessionParams{
    Mode: stripe.String(string(stripe.CheckoutSessionModeSubscription)),
    LineItems: []*stripe.CheckoutSessionLineItemParams{
        {Price: stripe.String("price_1Nxxxx"), Quantity: stripe.Int64(1)},
    },
    SuccessURL: stripe.String("https://example.com/billing/success?session_id={CHECKOUT_SESSION_ID}"),
    CancelURL:  stripe.String("https://example.com/billing/cancel"),
    Customer:   stripe.String(stripeCustomerID),          // attach to existing customer
    ClientReferenceID: stripe.String(internalUserID),     // your own user ID, round-trips in events
}
params.SetIdempotencyKey(idempotencyKey)                  // see below
sess, err := session.New(params)
```

`ClientReferenceID` is the field that lets you correlate a Stripe event back to your user. Use it.

## Webhook signature verification (DO NOT SKIP)

```go
func handleWebhook(w http.ResponseWriter, r *http.Request) {
    const maxBody = 1 << 20                               // 1 MiB cap; protects against memory attacks
    body, err := io.ReadAll(http.MaxBytesReader(w, r.Body, maxBody))
    if err != nil { http.Error(w, "read body", http.StatusBadRequest); return }

    // Verify FIRST. ConstructEvent checks signature AND timestamp tolerance (5 min default).
    event, err := webhook.ConstructEvent(
        body,
        r.Header.Get("Stripe-Signature"),
        os.Getenv("STRIPE_WEBHOOK_SECRET"),               // whsec_..., per-environment
    )
    if err != nil {
        slog.WarnContext(r.Context(), "webhook signature invalid", "err", err)
        http.Error(w, "signature", http.StatusBadRequest); return
    }

    // Only now is `event` trustworthy. Dispatch by type.
    switch event.Type {
    case "checkout.session.completed":           handleCheckoutCompleted(r.Context(), event)
    case "customer.subscription.updated":        handleSubUpdated(r.Context(), event)
    case "invoice.paid":                         handleInvoicePaid(r.Context(), event)
    case "payment_intent.payment_failed":        handlePaymentFailed(r.Context(), event)
    }
    w.WriteHeader(http.StatusOK)                          // ACK fast; do heavy work async
}
```

**Never** parse the body before `ConstructEvent`. **Never** skip the timestamp check (`ConstructEvent` enforces it; `ConstructEventWithOptions` lets you tune, don't widen it past 5 min). **Never** trust `event.Type` from a payload you haven't verified — that's the whole point.

`webhook.ConstructEvent` requires the raw request body bytes — middleware that consumes/decodes the body before your handler (logging, body parsers) breaks signature verification. Mount the webhook route OUTSIDE any body-mutating middleware AND outside any middleware that reads `r.Body` without its own size cap (otherwise an attacker-sized body OOMs the process before `MaxBytesReader` runs).

## Idempotency keys (mandatory for mutations)

```go
key := fmt.Sprintf("checkout-%s-%s", internalUserID, planID)   // deterministic per intent
params := &stripe.CheckoutSessionParams{...}
params.SetIdempotencyKey(key)
sess, err := session.New(params)
```

Stripe stores the response for 24 hours. Retries with the same key get the same response — no double-charging, no duplicate subscriptions. **Always set it on POST-equivalent calls** (`New`, `Update`, `Cancel`). Reads (`Get`, `List`) don't need it.

Key construction:

- Deterministic from the user's intent (`charge-${orderID}` not `charge-${time.Now()}`)
- Scoped enough to allow legitimate retries but not so wide it collides across customers
- 24h TTL — for longer-running workflows, key on a job ID stored in your DB

## Test mode vs live mode

| Concern         | Test (`sk_test_...`, `whsec_test_...`)                               | Live (`sk_live_...`, `whsec_live_...`) |
| --------------- | -------------------------------------------------------------------- | -------------------------------------- |
| Cards           | `4242 4242 4242 4242` + family; never real cards                     | real cards only                        |
| Webhooks        | use `stripe listen --forward-to localhost:8080/webhook` (Stripe CLI) | configure endpoint in Dashboard        |
| Webhook secret  | unique per-endpoint, per-environment — not interchangeable           | unique per-endpoint, per-environment   |
| Data isolation  | test-mode customers, products, prices live in a separate store       | completely separate                    |
| Restricted keys | available; use for sandboxed integrations + CI                       | use for prod background workers        |

Wire env-detection at boot: `if strings.HasPrefix(stripe.Key, "sk_live_") && env != "production" { log.Fatal("live key in non-prod") }`. Cheap defense against credential mix-ups.

## Subscription lifecycle events worth handling

| Event                                  | What it means                               | Action                                             |
| -------------------------------------- | ------------------------------------------- | -------------------------------------------------- |
| `customer.subscription.created`        | new sub                                     | grant access; record price + status                |
| `customer.subscription.updated`        | plan change, trial ended, status flip       | reconcile entitlements                             |
| `customer.subscription.deleted`        | sub canceled (immediately or at period end) | revoke at `current_period_end` (read from payload) |
| `invoice.paid`                         | renewal succeeded                           | extend period, send receipt                        |
| `invoice.payment_failed`               | renewal failed (dunning starts)             | notify user; revoke after retry exhaustion         |
| `payment_intent.payment_failed`        | one-off charge failed                       | retry path; surface to user                        |
| `customer.subscription.trial_will_end` | 3 days before trial ends                    | nudge user to add card                             |
| `charge.refunded`                      | refund processed                            | reverse entitlement; ledger entry                  |

Source of truth is Stripe — your DB is a projection. On a webhook, fetch the full object (`sub.Get(...)`) if the payload is stale or you need fields not in the event.

## Refund flow

```go
import "github.com/stripe/stripe-go/v82/refund"

params := &stripe.RefundParams{
    PaymentIntent: stripe.String(pi),
    Amount:        stripe.Int64(amountCents),             // omit for full refund
    Reason:        stripe.String(string(stripe.RefundReasonRequestedByCustomer)),
}
params.SetIdempotencyKey("refund-" + orderID)
r, err := refund.New(params)
```

Refunds emit `charge.refunded` and `refund.updated` events. Reconcile your ledger on the event, not on the API response — partial refunds for large amounts may go through Stripe's async path.

## Common security mistakes

- Logging the raw webhook body or `event.Data.Raw` at INFO — payloads contain PII (email, address); redact
- `stripe.Key` set from a request-scoped header — opens secret-injection vector; always startup-only
- Webhook handler behind a CSRF middleware that requires a session token — Stripe doesn't send one; mount on a path excluded from CSRF
- Exposing `sk_*` in a frontend bundle or env var prefixed with `NEXT_PUBLIC_` / `VITE_` — that's pk territory only
- Storing card numbers anywhere — you're now PCI-DSS Level 1; let Stripe hold them via Checkout
- Trusting `event.Livemode` for branching — verify the secret key prefix at boot, not per-request
- Reusing the same webhook secret across environments — rotate per environment, store in Vault

## Anti-patterns

- Skipping signature verification "just for dev" — habit forms; ship it once and it ships to prod
- Parsing the body before verifying — `ConstructEvent` needs the raw bytes, and you've now trusted unverified JSON
- No idempotency key on `New` calls — a network retry double-creates the subscription
- Blocking the webhook handler with heavy work — Stripe retries after 30s timeout; ACK fast, enqueue
- Treating `customer.subscription.deleted` as "revoke now" — read `cancel_at_period_end` first; user paid for the rest of the period
- Polling `sub.Get` in a loop to detect state changes — that's what webhooks are for
- Storing the webhook secret in `application.yaml` — env or Vault only
- Hard-coding `price_xxx` IDs in tests — tests then depend on Stripe state; mock the client interface instead

## Red flags

| Thought                                                 | Reality                                                                                                         |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| "Just one webhook without signature — it's behind auth" | Stripe is the only sender; signature IS the auth                                                                |
| "I'll log everything for debugging"                     | PII + secrets in logs; redact `event.Data.Raw` and customer fields before logging                               |
| "I'll add idempotency keys later"                       | First duplicate charge teaches you why "later" was wrong                                                        |
| "Test mode acts like live mode"                         | Mostly. Dunning, capture timing, and some error codes differ; smoke-test live with a $0.50 charge before launch |

## Hand-off

For mounting the webhook route on chi outside body-mutating middleware: `Skill(go-chi)`. For testing webhook signature verification with table-driven payloads: `Skill(go-testing)`. For secret loading from Vault/KMS and PII redaction in logs: `Skill(security)`. For tracing Stripe API calls + metric instrumentation (latency, error rate per event type): `Skill(observability-essentials)`. For Go idioms, error wrapping, modules: `Skill(go-essentials)`.
