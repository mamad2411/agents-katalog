---
name: manage-order-fulfillment
description: Implement and manage the post-purchase order lifecycle including order status management, packing, shipping label generation, carrier tracking, and refund or return processing. Use when building or maintaining fulfillment workflows after a successful payment.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, fetch]
---

# Manage Order Fulfillment

Use this skill when the task involves the operations and engineering required to move a confirmed order through packing, shipping, delivery tracking, and post-delivery actions (returns, refunds, exchanges).

## When to Use

- building post-purchase order lifecycle
- packing, shipping labels, carrier tracking
- refund or return processing
- fulfillment after successful payment
- **orchestration-based Saga (Temporal/AWS Step Functions)**
- **Vietnamese carrier webhook integrations (GHN/GHTK/GrabExpress)**
- **Vietnam Decree 248/2026/ND-CP compliance**

## Core Rules

- treat order data as `confidential` — customer PII (address, phone) must never appear in logs or public API responses
- **Event-Sourced State Machine (MANDATORY)**: model order status as an **append-only, immutable event log** (`order_placed`, `payment_captured`, `fulfillment_started`, `packed`, `shipped`, `delivered`, `returned`); derive current status by projecting the event stream — direct mutable status field updates are FORBIDDEN
- enforce state transitions via an **orchestration-based Saga** (Temporal / AWS Step Functions) with explicit compensating branches (`payment_failed`, `allocation_failed`, `cancelled`, `return_requested`, `refunded`); compensation order: reverse of success (Shipping → Inventory → Payment)
- refunds must always reference the original payment transaction ID — never issue a refund without a verified charge; refund amount must not exceed the captured total
- shipping label generation is irreversible and billable — validate carrier and shipping address before requesting a label; address validation is a mandatory step before tax/shipping calculations
- **Restock Inspection Gate (Enhanced)**: returned inventory must NOT be added back to sellable stock until a physical warehouse inspection event (Grade A confirmed) is logged — automatic restock on RMA creation is FORBIDDEN; event-sourced: `return_received` → `inspection_completed` (Grade A) → `restocked`
- validate agent-initiated fulfillment requests for a `fulfillment_authorized: true` JWT claim cryptographically scoped to the specific order ID before allocating inventory
- prefer **webhook callbacks** over polling for Vietnamese last-mile carriers (GHN, GHTK, Grab Express, Viettel Post, J&T Express); normalize all carrier status codes to unified internal milestones: `label_created` → `picked_up` → `in_transit` → `out_for_delivery` → `exception` / `delivered`
- **Vietnam Decree 248/2026/ND-CP Compliance** (effective July 1, 2026): seller identity verification required before fulfillment; platform obligations for rights disclosure, service standards, pricing transparency, affiliate marketing transparency; electronic ID verification for sellers/livestreamers from Jan 1, 2027

## Suggested Process

### 1. Define the Event-Sourced Order State Machine

Map the full lifecycle as immutable event log before implementing:

```
order_placed → payment_captured → fulfillment_started → packed → shipped → delivered → completed
                                                            ↘ return_requested → returned → refunded
pending → cancelled (only before shipped)
```

- enforce state transitions in code — reject invalid transitions with a clear error
- **derive current status by projecting event stream** — NO mutable status field updates
- emit an event or webhook on each state change for downstream systems (warehouse, email, analytics)
- **Temporal/Step Functions Saga**: compensating branches for each failure mode, durable retries, automatic compensation registration

### 2. Implement Order Processing

- on payment confirmation: create the order record, decrement inventory, send confirmation email
- assign the order to a fulfillment queue (warehouse team, 3PL, or automated picker)
- allow operations team to view and manage orders through an admin interface
- **Temporal patterns**: declarative states with guards in config, pure decider owns decisions; derived UI steps via `deriveStep()`; price integrity with `reviewedCartVersion`; reservation management with TTL

### 3. Implement Shipping Label Generation

- integrate with carrier API (EasyPost, Shippo, DHL API, GHTK for Vietnam) to generate shipping labels
- validate the shipping address before requesting a label (reduce carrier correction fees)
- store the label URL and tracking number against the order record
- mark order as `shipped` after label is generated and send tracking info to customer

### 4. Implement Vietnamese Carrier Tracking (Webhook Callbacks)

**GHN (Giao Hang Nhanh)**: `ready_to_pick`, `delivering`, `delivered` webhooks; COD callback URL for real-time COD status; automated sortation system
**GHTK**: G1 Open API — sorting code, create/cancel/tracking/big bag order endpoints
**GrabExpress**: on-demand same-city courier, real-time courier tracking, webhook updates over delivery lifecycle
**Viettel Post**: government-backed, nationwide coverage
**J&T Express**: regional Southeast Asia coverage

- **Webhook callbacks OVER polling** for all carriers
- **Normalize carrier codes** to unified milestones: `label_created` → `picked_up` → `in_transit` → `out_for_delivery` → `exception` / `delivered`
- verify webhook signatures (HMAC) and carrier allowlist to prevent spoofing

### 5. Implement Refund and Returns

- create a `ReturnRequest` with reason, items, and quantity
- validate return eligibility: within return window, original order in `completed` or `delivered` state
- on approval: initiate refund via `integrate-payment-gateway` using original transaction ID
- **Restock Inspection Gate**: `return_received` → `inspection_completed` (Grade A) → `restocked`; automatic restock on RMA creation FORBIDDEN
- emit a `refund_issued` event for accounting systems

### 6. Agent-Initiated Fulfillment Authorization

- verify agent JWT contains `fulfillment_authorized: true` claim
- claim must be cryptographically verified and scoped to specific order ID
- verify BEFORE inventory lock or allocation routines
- reject unauthorized agent fulfillment requests

### 7. Vietnam Decree 248/2026/ND-CP Compliance

- **Seller Verification Gate**: verify seller identity before `fulfillment_started` event
- **Platform Obligations**: disclose rights/obligations, service standards, pricing, promotions, security, complaints
- **Affiliate Transparency**: roles, links, referral codes, responsibilities disclosed
- **Electronic ID Verification**: sellers and livestream sellers from Jan 1, 2027

## 2026 Fulfillment Architecture Patterns

### Event-Sourced Fulfillment (Mandatory)
- Immutable append-only event log: `order_placed`, `payment_captured`, `fulfillment_started`, `packed`, `shipped`, `delivered`, `returned`
- Derive status by projection — direct mutable status updates FORBIDDEN
- Benefits: audit trails, time-travel debugging, compliance evidence

### Orchestration-Based Saga (Temporal / AWS Step Functions)
- Replace choreography with orchestration: explicit compensating branches
- Temporal: durable execution, automatic retries, built-in compensation registration
- Step Functions: state machine with Lambda compensations
- Compensation order: reverse of success (Shipping → Inventory → Payment)

### Agent-Initiated Authorization
- JWT claim required: `fulfillment_authorized: true`, cryptographically scoped to order ID
- Verify BEFORE inventory lock or allocation

### Vietnamese Carrier Webhook Integrations
- **GHN**: `ready_to_pick`, `delivering`, `delivered`, COD callback
- **GHTK**: G1 Open API: sorting code, create/cancel/track/big bag
- **GrabExpress**: real-time courier tracking, delivery lifecycle
- **Normalize all** to unified milestones: `label_created` → `picked_up` → `in_transit` → `out_for_delivery` → `exception` / `delivered`

### Vietnam Decree 248/2026/ND-CP
- Seller verification before fulfillment; platform obligations; affiliate transparency; electronic ID from Jan 1, 2027

### Restock Inspection Gate (Enhanced)
- Physical inspection mandatory: Grade A before restock
- Event-sourced: `return_received` → `inspection_completed` (Grade A) → `restocked`
- Automatic restock on RMA creation FORBIDDEN

### Temporal E-Commerce Patterns
- Checkout workflow IS the saga; `updateWithStart` for atomic create-or-update
- Declarative states with guards; `deriveStep()` for UI; price integrity via `reviewedCartVersion`
- Reservation renewal at start, TTL release on timeout, confirmation on success

## Checklist

- [ ] order state machine modeled as immutable append-only event log
- [ ] current status derived by projecting event stream (no mutable status field)
- [ ] orchestration-based Saga with Temporal or AWS Step Functions
- [ ] explicit compensating branches for all failure modes
- [ ] Agent JWT contains `fulfillment_authorized: true` claim scoped to order ID
- [ ] cryptographic verification of agent authorization before inventory allocation
- [ ] GHN webhook integration: `ready_to_pick`, `delivering`, `delivered`, COD callback
- [ ] GHTK webhook integration: G1 Open API endpoints, status normalization
- [ ] GrabExpress webhook integration: real-time courier tracking, delivery lifecycle
- [ ] carrier status codes mapped to unified milestones (`label_created` → `delivered`)
- [ ] webhook signature verification (HMAC) and carrier allowlist
- [ ] Vietnam Decree 248/2026: seller verification workflow before `fulfillment_started`
- [ ] affiliate marketing transparency: roles, links, codes disclosed
- [ ] restock inspection gate: `return_received` → `inspection_completed` (Grade A) → `restocked`
- [ ] automatic restock on RMA creation forbidden
- [ ] declarative state transitions with guards in configuration
- [ ] price integrity: stale cart version aborts with `CART_CHANGED`
- [ ] inventory reservation renewal at fulfillment start, TTL release on timeout
- [ ] customer PII not in logs or non-admin API responses
- [ ] state change events emitted for downstream systems

## Failure Modes

- **Order fulfilled twice**: idempotency key on every fulfillment call; reject duplicates.
- **Inventory not decremented**: enforce decrement in same transaction; reject without it.
- **Tracking ID not propagated**: require notification step on every fulfillment.
- **Carrier mismatch**: validate carrier against destination at fulfillment time.
- **Agent fulfillment spoofing**: JWT `fulfillment_authorized: true` claim verification scoped to order ID.
- **Event log corruption**: DB constraint forbidding direct status updates, audit trigger.
- **Saga compensation failure**: Temporal durable retries, dead letter queue for manual intervention.
- **Carrier webhook spoofing**: webhook signature verification (HMAC), carrier allowlist.
- **Vietnam compliance gap**: Decree 248/2026 verification gate before `fulfillment_started` event.
- **Restock without inspection**: mandatory `inspection_completed` event with Grade A before `restocked`.

## Output Contracts

When the fulfillment workflow is consumed by warehouse, shipping, or support agents, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the fulfillment endpoints, the request/response shapes, and the state transitions.
- Inline JSON deliverables for the event-sourced order log (event + projection shapes), the saga workflow definition (Temporal/Step Functions, compensation order), and the restock inspection gate.
- Inline specs for JWT `fulfillment_authorized` claim verification and carrier webhook normalization (GHN/GHTK/GrabExpress), plus a markdown state-machine summary for human reviewers.

Skip emission for single-order experiments that do not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a fulfillment request may try to reframe the order's state. Validate against the declared order id and the state machine.
- **ASI03 Identity & Privilege Abuse**: fulfillment endpoints must enforce role-based access; reject unscoped calls.
- **ASI05 RCE Guard**: never construct shipping labels, tracking IDs, or webhook payloads from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the fulfillment contract is consumed by warehouse and support agents; emit a structured spec so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present fulfillment as "automated" without the actual state transition evidence; surface the residual risk.

## Related Skills

- **integrate-payment-gateway**: Issue refunds against original payment transactions
- **handle-checkout-flow**: Creates the order that this skill fulfills
- **manage-product-catalog**: Decrements inventory and restocks on returns
- **add-event-handler**: Handle carrier tracking webhooks and order state events
- **add-api-endpoint**: Expose fulfillment status and return endpoints
- **incident-report**: Escalate lost packages, carrier failures, and refund disputes
- Companion reference: `references/event-sourced-fulfillment-and-carrier-webhooks.md`
- Companion example: `examples/temporal-fulfillment-saga.ts`

Last updated: 2026-11-08