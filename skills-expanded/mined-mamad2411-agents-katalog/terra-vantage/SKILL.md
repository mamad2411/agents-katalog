---
name: terra-vantage
description: Order at-home and go-to-lab diagnostic tests and deliver results with the Terra Vantage API. Use when ordering blood tests or DNA tests, integrating at-home test kits, placing diagnostics orders, browsing test products and variants, handling kit activation, tracking fulfillment and shipping, receiving results-status webhooks, fetching FHIR-format lab results, or acknowledging results (a mandatory compliance step before patients can view them). Covers the product-to-order-to-results workflow, HTTP Basic auth, the AT_HOME vs GO_TO_LAB collection methods, webhook events and HMAC signature verification, the sandbox environment, and the manual partner onboarding required to get started.
license: MIT
compatibility: Requires network access to docs.tryterra.co for current endpoint schemas
metadata:
  author: terra
  version: "1.0.0"
---

# Terra Vantage API

The Vantage API is a platform for managing blood test and DNA diagnostic products, processing orders, and delivering test results. It lets healthcare providers, laboratories, and partners embed diagnostic testing directly into their own applications while Terra API handles the operational complexity: kit supplier integrations (no minimum order requirements), logistics and shipping, compliance, and results standardization into FHIR format. The stated goal is to add biological context to the metrics wearables already provide, and to remove the lab agreements, logistics, and compliance work that normally block launching white-label testing.

**Availability and onboarding.** Vantage is available in the United Kingdom and the USA, with Germany, Spain, and France listed as coming soon. Onboarding is manual, not self-service: contact Terra API to receive credentials (see [Account Setup and API Keys](https://docs.tryterra.co/vantage-api-docs/account-setup-and-api-keys)). Credentials work in the sandbox first; production credentials are issued later.

## Authentication

Every request uses HTTP **Basic authentication** with your client ID and secret, base64-encoded as `CLIENT_ID:CLIENT_SECRET` in the `Authorization` header. This differs from other Terra API products, which use `dev-id` and `x-api-key` headers. Do not reuse that pattern here.

```
Authorization: Basic <base64(CLIENT_ID:CLIENT_SECRET)>
Content-Type: application/json
```

Base URLs:

| Environment | Base URL                              |
| ----------- | ------------------------------------- |
| Production  | `https://vantage.tryterra.co`         |
| Sandbox     | `https://vantage-sandbox.tryterra.co` |

All API paths below are under `/api/v1`. Some reference pages abbreviate paths (for example `/orders` instead of `/api/v1/orders`); the full prefix is shown in the getting-started and sandbox docs.

## Order-to-Results Workflow

An integration walks a test from catalog to acknowledged result. Products are a three-level catalog (**product types** hold **products**, which hold **variants**), and a variant is the exact thing a recipient receives.

```
1  GET  /api/v1/products                     -> list product types (e.g. Blood Test, DNA Test)
2  GET  /api/v1/products/{product_type_id}    -> products within a type
3  GET  /api/v1/products/{product_id}/variants-> variants of a product
4  POST /api/v1/orders                        -> place order (variant_id + quantity + recipient)
5  (webhooks)                                 -> fulfillment + results status changes
6  GET  /api/v1/results/{order_item_id}       -> presigned FHIR download URL
7  POST /api/v1/results/{order_item_id}/acknowledge -> MANDATORY before the patient sees results
```

Placing an order returns an `order_id`, a `recipient_id`, and one `order_item_id` per item. The order starts at `order_status: "order.payment_processing"` and each item starts at `results_status: "results.awaiting_sample"`. Track everything downstream by `order_item_id`, since results, activation, and acknowledgment are all per-item.

[references/api-reference.md](references/api-reference.md) maps each goal to its endpoint and to the live doc page carrying the current request/response schema; read it before implementing any endpoint call, and fetch the linked `.md` page when building a request body (field lists change as the product evolves, so the live page is authoritative).

## Collection Methods

Each order sets a `collection_type` that determines how the sample is taken and which address field applies:

| `collection_type` | Meaning                                                                         | Address field           |
| ----------------- | ------------------------------------------------------------------------------- | ----------------------- |
| `AT_HOME`         | Kit shipped to the recipient; they self-collect and follow the kit instructions | `shipping_address`      |
| `GO_TO_LAB`       | Mobile phlebotomy; a registered nurse collects the sample at a lab              | `requested_lab_address` |

For `GO_TO_LAB`, the requested lab address is used as a proxy to route the order to the closest available lab; the resolved lab comes back as `confirmed_lab_address`. A variant advertises which methods it supports in `availableCollectionTypes`, so confirm support before offering a method to a user; note this field is an array of integer enum codes (int32), not the `AT_HOME`/`GO_TO_LAB` strings used in the order request, so do not compare it against those strings.

## Kit Activation

Some suppliers require the end user to activate the kit themselves (for example by scanning a QR code on the packaging) before the lab will process it. Activation is end-user facing: `GET /activate?kit_id=...` serves an HTML activation form, and the form submits to `POST /activate/kit` with the test-taker's details. A successful activation emits a `results.kit_activated` webhook. See [references/api-reference.md](references/api-reference.md) for the activation request body.

## Acknowledging Results (Mandatory)

Acknowledging results is **not optional**. Per the docs, all results, from low to high clinical escalation, must be explicitly acknowledged before patients can access them. Acknowledgment records that your organization has reviewed the outcome and takes responsibility for communicating the appropriate severity to the end user.

```
POST /api/v1/results/{order_item_id}/acknowledge?test_taker_id={id}
```

Two consequences are called out for leaving results unacknowledged:

- **Liability transfers to you.** Failure to acknowledge "initiates a chain of liability that transfers responsibility directly to you," and your organization assumes full liability for adverse outcomes from delayed or unacknowledged results.
- **Suppliers may contact patients directly.** If results stay unacknowledged, test suppliers and medical teams are authorized to reach out to patients directly to ensure they receive critical health information.

Build acknowledgment into the flow: fetch the result, present it, and acknowledge as part of delivering it to the user. FHIR result structure and the fetch/acknowledge endpoints are detailed in [references/results.md](references/results.md); read it when building result retrieval or the acknowledgment step.

## Webhooks

Terra API delivers order and result progress to the webhook URL you configure at onboarding (updatable via `PATCH /api/v1/clients/webhook-url`). There are two `event_type` families: `order.status_changed` for fulfillment progress and `order_item.results_status_change` for per-item result progress. Webhooks are HMAC-SHA256 signed via the `X-Terra-Signature` header; verify every request before trusting it.

Result-status lifecycle (per item):

```
results.awaiting_sample -> results.kit_activated -> results.sample_processing_in_lab -> results.results_ready
                                                                         \-> results.sample_rejected
                                                                         \-> results.escalation_raised
```

Every event type, its full payload, the status enums, and the signature verification steps are in [references/webhooks.md](references/webhooks.md). Read it when building or verifying a webhook handler.

## Working with the Sandbox

The sandbox at `https://vantage-sandbox.tryterra.co` receives the same webhooks as production, with a few simulation aids:

- **Activation is a browser flow, not an API call.** For suppliers that use end-user kit activation, the kit's QR code embeds an activation URL. To stand in for the user scanning it, open `https://vantage-sandbox.tryterra.co/api/v1/orders/activate?kit_id={supplier_item_id}` in a browser (the `supplier_item_id` arrives on the sandbox webhook) and complete the activation form it redirects to. The same URL exists in production; only the manual navigation is the sandbox stand-in.
- **Sandbox webhooks add `supplier_item_id`.** This field is present in sandbox payloads and not in production.
- **Results are auto-generated.** After a successful activation, the sandbox sends two webhooks 1 to 2 minutes apart: `results.sample_processing_in_lab`, then `results.results_ready`. You may instead receive `results.sample_rejected` to exercise the failure path.

## Gotchas

- **Acknowledgment gates patient access and shifts liability.** Patients cannot see results until you acknowledge, and skipping it transfers liability to you. Treat it as a required step, not a cleanup task.
- **Auth is Basic, not `dev-id`/`x-api-key`.** Other Terra API products use header keys; Vantage uses base64 Basic auth. Wiring the wrong scheme yields `401`.
- **Track by `order_item_id`, not `order_id`.** One order can hold multiple items, and results, activation, and acknowledgment are all per item.
- **Presigned result URLs expire in 15 minutes.** `GET /api/v1/results/{order_item_id}` mints a fresh time-limited `download_url`; re-fetch to re-mint rather than caching the URL.
- **`test_taker_id` is required to read or acknowledge results.** Both the fetch and acknowledge endpoints take it as a query parameter.
- **Verify the webhook signature.** Validate `X-Terra-Signature` (HMAC-SHA256, 5-minute timestamp tolerance) before parsing any webhook body.
- **Collection type dictates the address field.** Send `shipping_address` for `AT_HOME` and `requested_lab_address` for `GO_TO_LAB`; do not mix them up.
- **Sandbox credentials come first.** Your keys work only in sandbox until production credentials are issued during onboarding.

## Live Documentation

Append `.md` to any page URL for markdown. If the terra-docs MCP server (`https://docs.tryterra.co/~gitbook/mcp`) is connected, use its tools to search and fetch these pages instead.

- [What is Vantage API?](https://docs.tryterra.co/vantage-api-docs/readme)
- [Account Setup and API Keys](https://docs.tryterra.co/vantage-api-docs/account-setup-and-api-keys)
- [Ordering Your First Test](https://docs.tryterra.co/vantage-api-docs/getting-started/ordering-your-first-test)
- [Webhooks](https://docs.tryterra.co/vantage-api-docs/documentation/webhooks)
- [Test Collection Methods](https://docs.tryterra.co/vantage-api-docs/documentation/test-collection-methods)
- [Results](https://docs.tryterra.co/vantage-api-docs/documentation/results)
- [Acknowledging Results](https://docs.tryterra.co/vantage-api-docs/important-information/acknowledging-results)
- API reference: [activation](https://docs.tryterra.co/vantage-api-reference/core-resources/activation), [clients](https://docs.tryterra.co/vantage-api-reference/core-resources/clients), [orders](https://docs.tryterra.co/vantage-api-reference/core-resources/orders), [products](https://docs.tryterra.co/vantage-api-reference/core-resources/products), [results](https://docs.tryterra.co/vantage-api-reference/core-resources/results)
