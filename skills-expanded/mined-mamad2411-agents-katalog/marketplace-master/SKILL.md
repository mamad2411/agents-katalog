---
name: marketplace-master
description: >-
  Master hub for building production multi-vendor marketplaces at staff/principal depth
  — product (Amazon/Noon/Etsy), food & quick-commerce (Talabat/Uber-Eats), services, and
  rentals. Covers architecture (the one-cart→many-sub-orders split, double-entry ledger,
  idempotency, outbox, multi-tenant RLS), catalog + buy box, seller mgmt + KYC, cart/
  checkout saga, split payments & payouts (Stripe Connect), delivery dispatch (H3/ETA),
  search & recs (Algolia/OpenSearch), reviews/trust & safety, promotions, and the data
  platform. Bundles 10 specialized skills (in skills/<name>/GUIDE.md). Use for any
  marketplace task.
---

# Marketplace Platforms — Master Hub

Build production multi-vendor marketplaces like **Amazon/Noon** (products), **Talabat/Uber Eats**
(food & delivery), plus services and rentals. These skills are written at staff/principal depth:
real Postgres schemas, TypeScript, verified 2026 APIs (Stripe Connect Accounts v2, Algolia, OpenSearch,
H3 dispatch), edge cases, scale, and MENA/RTL specifics — not surface-level overviews.

## The one idea everything hangs on

**One cart → one payment → many per-seller sub-orders → many payouts.** That fan-out is the
marketplace. Three decisions are load-bearing and hard to retrofit: the **order split**, a
**double-entry ledger you own** (the PSP is a rail, not your books), and **multi-tenant seller
isolation**. Get those right first (start in `marketplace-architecture`); everything else is replaceable.

## How to use this hub

This single skill bundles **all 10 marketplace skills**. Each lives in `skills/<name>/GUIDE.md` (plus
any `scripts/`/`references/`).

**Workflow:**
1. Read **marketplace-architecture** first — the shared data model, the split, the ledger, idempotency, the outbox, and RLS that every other skill builds on.
2. Match the request to the skills below and read their `GUIDE.md` before acting.
3. Combine skills — a real marketplace spans most of them; the GUIDEs cross-reference each other.

## Bundled skills

- **marketplace-architecture** ⭐ — Foundation: marketplace types, bounded contexts, the one-cart→many-sub-orders flow, money as a double-entry ledger, idempotency + transactional outbox, orchestration vs choreography, and Postgres RLS multi-tenancy. **Read first.**  
  → `skills/marketplace-architecture/GUIDE.md`
- **multi-vendor-catalog** — Product↔Offer split + buy box, variants/SKUs, JSONB-vs-EAV facets, oversell-proof inventory (atomic reservation), food menu/modifiers, denormalized search docs, dedup + moderation.  
  → `skills/multi-vendor-catalog/GUIDE.md`
- **seller-vendor-management** — Onboarding + KYC/KYB via Stripe Connect (Accounts v2 / controller properties), capability gating, configurable commission (basis points), payout scheduling + wallet ledger, SLA/defect scoring, multi-branch + staff RBAC, payout-fraud defenses.  
  → `skills/seller-vendor-management/GUIDE.md`
- **cart-checkout-orders** — Multi-vendor cart, the idempotent split-checkout **saga** with compensations, order/sub-order FSMs (product + food), partial fulfillment, returns/RMA, and refunds with proportional clawback.  
  → `skills/cart-checkout-orders/GUIDE.md`
- **marketplace-payments-payouts** — Split payments & payouts via **Stripe Connect** (separate charges & transfers vs destination charges, `transfer_group`/`source_transaction`, escrow via delayed transfers, transfer reversals + commission clawback), the double-entry ledger, negative balances, idempotent webhooks, PCI/SCA.  
  → `skills/marketplace-payments-payouts/GUIDE.md`
- **delivery-logistics-dispatch** — On-demand courier dispatch: **H3** proximity index, DISCO-style batched ETA-weighted assignment, Google Routes ETAs, PostGIS+H3 zones, throttled live tracking, batching, courier/ops apps, COD; plus carrier shipping for products.  
  → `skills/delivery-logistics-dispatch/GUIDE.md`
- **search-discovery-recommendations** — Search as a read model: typo-tolerant faceted search, the **Algolia** ranking pipeline (8 criteria + customRanking + Rules + Dynamic Re-Ranking) and **OpenSearch hybrid** (BM25 + kNN), buy-box surfacing, vector recs + cold start, sponsored-listing auctions.  
  → `skills/search-discovery-recommendations/GUIDE.md`
- **reviews-ratings-trust-safety** — Verified reviews, honest aggregation (**Bayesian + Wilson**, not naive averages), layered moderation (rules→ML/LLM→human), fake-review/fraud-ring detection, buyer/seller protection, dispute FSM + SLA wired to chargebacks, reputation → ranking/payout.  
  → `skills/reviews-ratings-trust-safety/GUIDE.md`
- **marketplace-promotions-pricing** 🆕 — The discount money primitive: discount types + deterministic stacking, and **who funds each discount** (platform/seller/co-funded) posted to the ledger so payouts stay correct; campaign budget pacing, coupon/referral fraud defenses, dynamic/surge pricing, discount↔refund accounting.  
  → `skills/marketplace-promotions-pricing/GUIDE.md`
- **marketplace-data-platform** 🆕 — Scale + measure: OLTP/OLAP split, outbox→CDC→read-models (CQRS), multi-tenant isolation (shared+RLS vs schema/DB/shard-per-tenant), seller-balance/buy-box read models, canonical **GMV / take-rate / liquidity / cohort** definitions, daily ledger↔PSP reconciliation, data-quality SLOs.  
  → `skills/marketplace-data-platform/GUIDE.md`

## Pairs well with
- **payments-master** — PSP-agnostic depth (Adyen, Mangopay, regional MENA gateways: Paymob, Fawry, HyperPay, PayTabs, Tap), PCI scope, 3DS/SCA. `marketplace-payments-payouts` is the marketplace flow-of-funds layer *on top of* it — go there for gateway-level detail.
- **backend-api-master** (auth, MFA, RBAC, Stripe/webhooks, GIS maps, GPS), **business-master** (accounting-finance for the money ledger/close; white-label for multi-brand), **ui-master** (charts-and-dashboards, RTL/Arabic, instant-search UI), **ai-mcp-master** (embeddings/recsys, camera-ai-vision for moderation).

## Note

These bundled skills are intentionally not registered as separate Cursor skills (their files are
`GUIDE.md`, not `SKILL.md`) so only this master appears in the skills list. Read the relevant
`GUIDE.md` on demand.
