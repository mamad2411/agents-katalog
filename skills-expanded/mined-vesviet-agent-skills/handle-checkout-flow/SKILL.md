---
name: handle-checkout-flow
description: Design and implement the end-to-end checkout flow including cart management, tax and shipping calculation, discount/coupon application, and order confirmation. Use when building or fixing any step in the purchase funnel from cart to payment confirmation.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, fetch]
---

# Handle Checkout Flow

Use this skill when the task involves building, extending, or debugging the steps a customer takes from adding an item to cart through to receiving an order confirmation.

## When to Use

- building/fixing the purchase funnel
- cart, tax/shipping, discount/coupon logic
- order confirmation step
- end-to-end checkout from cart to payment
- **agentic checkout under ACP/UCP protocols**
- **Vietnam Decree 248/2026/ND-CP compliance**

## Core Rules

- **Zero Client-Trust Pricing**: recalculate all line items, discounts, taxes, and shipping server-side immediately before creating the payment intent — discard any client-submitted monetary amounts
- **PCI DSS v4.0.1 Script Integrity** (req 6.4.3): all JavaScript executing on payment pages must be inventoried, justified, and loaded with **Subresource Integrity (SRI) hashes** and a strict **CSP nonce** (`script-src 'nonce-...'`); 3DS scripts in iframes exempt due to trust relationship
- **Tamper Detection** (req 11.6.1): an automated mechanism must monitor payment page HTTP headers and client-side scripts at least weekly (or continuously) to detect unauthorized modifications (Magecart/formjacking); SAQ A eligibility updated Jan 2025
- validate inventory availability at checkout submission time, not only at add-to-cart time; use **two-phase atomic hold** (soft reserve with TTL → hard commit on payment success / release on failure)
- apply discounts and promotions server-side only; wrap coupon validation and usage increment in an **atomic transaction with row-level lock** (`SELECT ... FOR UPDATE`) to prevent TOCTOU race conditions under concurrent requests
- ensure checkout submission is idempotent: use idempotency keys on payment intent creation; submitting an order twice must not produce two charges
- protect guest checkout with **cryptographically signed HMAC tokens** — not plain session IDs; enforce strict BOLA checks so each cart/order is accessible only to its owning session or user
- support **EMV 3DS 2.3.1** with 100+ context attributes for frictionless risk-based authentication (> 85% challenge-free); integrate SCA exemption engine (Low-Value, TRA, Trusted Beneficiary)
- **Agentic Checkout (ACP/UCP)**: implement pre-authorization gates and spending limits per agent session/customer ID; define Merchant of Record (MoR) for agentic transactions; support programmatic headless checkout via ACP/UCP structured responses
- **Mandatory Address Validation Lifecycle**: validate shipping address via Google Maps Address Validation, Loqate, or Smarty Streets BEFORE tax calculation or shipping carrier requests; catch errors (missing apartment, invalid ZIP) with precise subcodes
- **Tax Engine Decision Tree**: Stripe Tax (startups/mid-market in Stripe ecosystem), TaxJar (multi-channel, moderate volume, standard ERP), Avalara AvaTax (enterprise, high volume, complex Nexus, custom ERP)
- **Economic Nexus Threshold Monitoring**: track US state-by-state transaction count and sales volume; alert at 80% of threshold (e.g., 160 transactions or $80K sales); auto-registration workflow
- **Vietnam Decree 248/2026/ND-CP Compliance** (effective July 1, 2026): seller identity verification required before platform transactions; platform obligations for rights disclosure, service standards, pricing transparency, affiliate marketing transparency; electronic ID verification for sellers/livestreamers from Jan 1, 2027

## Suggested Process

### 1. Map the Checkout Steps

Define the full funnel before building:

- cart review → shipping address → **address validation (MANDATORY)** → shipping method selection → discount/coupon → payment → order confirmation
- identify which steps are required vs skippable (e.g., digital goods skip shipping)
- confirm whether guest checkout is supported alongside authenticated checkout
- **agentic checkout path**: headless execution via ACP/UCP, pre-authorization gates, MoR assignment

### 2. Implement Cart State Management

- store cart in session (guest) or database (authenticated), syncing on authentication
- calculate line-item totals, subtotal, and item weight server-side
- handle out-of-stock and quantity changes gracefully with clear user messaging

### 3. Implement Address Validation (Mandatory Before Tax/Shipping)

- integrate Google Maps Address Validation, Loqate, or Smarty Streets APIs
- standardize raw user inputs into verified, carrier-compliant address structures
- catch validation errors with precise subcodes (missing apartment, invalid ZIP)
- reject tax/shipping calculation if address validation fails

### 4. Implement Tax and Shipping Calculation

- select tax engine per decision tree: Stripe Tax / TaxJar / Avalara based on scale, volume, ERP
- calculate jurisdiction-based tax on final validated shipping address
- call shipping carrier APIs (or flat-rate rules) for options and costs
- recalculate totals whenever address or shipping method changes
- **economic nexus monitoring**: track thresholds per state, alert at 80%, auto-registration workflow

### 5. Implement Discount and Coupon Logic

- validate coupons server-side: check code existence, validity window, usage limits, minimum order value, applicable SKUs
- apply discounts in defined precedence order (item discount → coupon → loyalty points)
- display applied discount breakdown clearly before final payment

### 6. Finalize Order and Confirm Payment

- lock inventory at order-creation time (before charging)
- call `integrate-payment-gateway` to process payment
- on success: persist confirmed order, release inventory lock, send confirmation email, redirect to confirmation page
- on failure: release inventory lock, surface payment error, allow retry without re-entering non-payment data
- **agentic checkout**: headless execution, structured responses, spending limit enforcement

## 2026 Agentic Checkout Patterns

### 2026: Agentic Checkout Architecture (ACP/UCP)

Agentic Checkout enables AI agents to autonomously execute purchase transactions under the Agentic Commerce Protocol (ACP) and Universal Commerce Protocol (UCP):

- **ACP** (OpenAI + Stripe, Sep 2025): Agentic Commerce Protocol, Instant Checkout in ChatGPT, cart/feed/orders/auth/MCP support
- **UCP** (Google + partners, Jan 2026): Universal Commerce Protocol, Apache 2.0, compatible with A2A/AP2/MCP, v2026-08-25 multi-vertical/grocery/3DS2/payment schedules/split payments/loyalty
- **Authorization & Limits**: Pre-authorization gates and spending limits per agent session or customer ID
- **Merchant of Record (MoR)**: Clear MoR assignments for fraud liability, chargebacks, regional taxes
- **Programmatic Checkout**: Headless execution without interactive browser sessions, standardized structured responses

### 2026: Address Validation Lifecycle (Mandatory)

Validating the shipping address is a mandatory, isolated step that must occur BEFORE tax calculation or shipping carrier requests:

- **API Standards**: Google Maps Address Validation, Loqate, Smarty Streets
- **Error Handling**: Precise subcodes for missing apartment number, invalid zip codes
- **Gate**: Reject tax/shipping calls if validation fails

### 2026: Stripe Tax Integration and Decision Tree

Selecting the correct tax calculation service depends on the merchant's scale, transaction volume, and operational context:

- **Stripe Tax**: Startups/mid-market within Stripe ecosystem, quick integration
- **TaxJar**: Multi-channel merchants (Shopify + Custom Web App), moderate volume, standard ERP
- **Avalara AvaTax**: Enterprise, high volume, complex Nexus, custom ERP, localized tax

### 2026: Economic Nexus Threshold Monitoring

Merchants must actively track regional sales thresholds to ensure compliance with local tax registration laws:

- **Nexus Monitoring**: Track US state-by-state transaction count and sales volume programmatically
- **Alerting**: Alert at 80% of any state's economic nexus threshold (e.g., 200 transactions or $100,000 sales)
- **Most states**: $100K sales OR 200 transactions (many dropped transaction count)
- **Auto-registration**: Stripe Tax / TaxJar offer automated registration workflows

### 2026: Vietnam Decree 248/2026/ND-CP Compliance

Effective July 1, 2026 (electronic ID verification from Jan 1, 2027):

- **Seller Verification**: Platform must verify seller identity before allowing transactions
- **Platform Obligations**: Disclose rights/obligations, service standards, pricing, promotions, security, complaints
- **Affiliate Transparency**: All parties disclose roles, links, referral codes, responsibilities
- **Electronic ID Verification**: Sellers and livestream sellers from Jan 1, 2027

## Checklist

- [ ] cart totals recalculated server-side before every charge
- [ ] inventory availability re-validated at checkout submission
- [ ] coupon validation is server-side with usage limit enforcement
- [ ] tax and shipping calculated from confirmed shipping address
- [ ] checkout submission is idempotent (double-submit safe)
- [ ] inventory locked before charge, released on failure
- [ ] order confirmation and email sent after successful payment
- [ ] guest and authenticated paths tested independently
- [ ] agentic checkout spending limits and pre-authorization gates enforced
- [ ] Merchant of Record (MoR) assigned for agentic transactions
- [ ] ACP/UCP programmatic checkout supported (headless, structured responses)
- [ ] address validation performed via verified API (Google Maps/Loqate/Smarty) BEFORE tax/shipping
- [ ] address validation errors caught with precise subcodes (missing apartment, invalid ZIP)
- [ ] tax engine selected per decision tree (Stripe Tax / TaxJar / Avalara)
- [ ] economic nexus threshold monitoring at 80% with alerts configured
- [ ] economic nexus auto-registration workflow implemented
- [ ] PCI DSS v4.0.1 req 6.4.3: SRI hashes + CSP nonce on all payment page scripts
- [ ] PCI DSS v4.0.1 req 11.6.1: automated tamper detection (weekly/continuous)
- [ ] Vietnam Decree 248/2026: seller verification gate before transactions
- [ ] Vietnam Decree 248/2026: platform obligations disclosed (rights, standards, pricing, affiliate transparency)
- [ ] Vietnam electronic ID verification for sellers/livestreamers (from Jan 1, 2027)

## Failure Modes

- **Cart abandoned on price mismatch**: the cart shows a different price than checkout. **Mitigation:** re-validate the cart at checkout; surface the price change to the user before charging.
- **Inventory oversell under concurrency**: two channels decrement the same stock in parallel and oversell. **Mitigation:** use atomic SQL or Redis Lua with TTL; reject naive read-then-write sequences.
- **Silent price overwrite**: a price change overwrites historical prices without a version or timestamp. **Mitigation:** store `price`, `compare_at_price`, `effective_from`, and `effective_until`; never silently overwrite.
- **PCI scope drift**: a new endpoint touches card data without being in the PCI scope. **Mitigation:** review the data flow before merge; require a security review for any new card-handling code.
- **Agentic checkout fraud**: unauthorized agent spending beyond limits. **Mitigation:** pre-authorization gates, spending limits per agent session, MoR assignment.
- **Address validation bypass**: tax/shipping calculated on invalid address. **Mitigation:** mandatory validation gate before calculation; reject calls if validation fails.
- **Nexus threshold breach**: unregistered tax collection. **Mitigation:** 80% alerting, auto-registration workflow, compliance monitoring.
- **PCI script injection**: Magecart via unverified third-party scripts. **Mitigation:** SRI + CSP nonce + weekly automated scanning.
- **Vietnam compliance gap**: unverified seller completes transaction. **Mitigation:** seller verification gate enforced before checkout, platform audit trail.

## Output Contracts

When the checkout flow is consumed by storefront, payment, or fulfillment agents, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the checkout endpoints, request/response shapes, auth requirements, agentic commerce interfaces (ACP/UCP pre-auth gates, MoR assignment), address validation contracts, and tax engine integration payloads.
- For human-readable reports, a markdown summary of the flow, the failure modes, and the rollback path.

Skip emission for single-checkout experiments that do not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a checkout request body may try to reframe the order's intent. Validate against the declared cart and pricing.
- **ASI03 Identity & Privilege Abuse**: checkout endpoints must enforce authn/authz; reject anonymous high-value actions.
- **ASI05 RCE Guard**: never construct pricing, tax, or payment payloads from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the checkout contract is consumed by storefront, payment, and fulfillment agents; emit a structured spec so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the flow as "secure" without the inventory hold and PCI scope review; surface the residual risk honestly.

## Related Skills

- **integrate-payment-gateway**: Process the final payment step in the checkout flow
- **manage-product-catalog**: Source product details, pricing, and inventory levels
- **manage-order-fulfillment**: Hand off the confirmed order for packing and shipping
- **add-ui-component**: Build the cart and checkout UI components
- **write-tests**: Write integration tests for the purchase funnel
- Companion reference: `references/pci-dss-v4-and-agentic-checkout-specs.md`
- Companion example: `examples/production-checkout-orchestrator.ts`

Last updated: 2026-11-08