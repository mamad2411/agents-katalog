---
id: airwallex-contract-to-billing
name: Airwallex Contract to Billing
description: Use this skill when creating Airwallex invoices or subscriptions from a purchase order, contract, or quote — extract line items and match existing customers, products, and prices.
category: Airwallex
author: airwallex
version: 0.1.0
license: Apache-2.0. Complete terms in LICENSE.txt
---

# Airwallex Contract to Billing

Reads a customer document (PO, contract, quote), extracts line items, and creates a fully populated invoice or subscription in Airwallex Billing. Uses the Airwallex MCP billing tools and operates on **live production data** — there is no sandbox.

## When to use

- User uploads or references a purchase order, contract, quote, or billing document
- User asks to "create an invoice" from a document
- User wants to extract billing details and set up products/prices/customers
- User says "bill this customer" with a document attached

## When NOT to use

This skill covers Billing-domain operations exposed by this connector: invoices (list, retrieve, create, update, finalize, void, mark-as-paid, list line items, add line items), products (list, create), prices (list, create), customers (list, retrieve, create, update), subscriptions (create, list items), coupons (list, create, update), and meters (list, create, update).

**Not exposed by this connector** — direct the user to the Airwallex Dashboard for: line-item update/delete (correct by voiding and re-issuing instead), credit notes, subscription cancellation, payment-source listing, and billing-transaction listing.

If the task requires anything outside the Billing domain, **stop — this is the wrong skill.** Redirect the user:

- Wire transfers / paying suppliers → not available through this connector (use the Airwallex Dashboard)
- Setting up suppliers / beneficiaries → **airwallex-beneficiary-creation** skill
- FX conversions, balances, treasury → **airwallex-manage-cashflow** skill
- Provisioning corporate cards → **airwallex-card-provisioning** skill

## Non-negotiables

### Terminology

- **Invoices = receivables (money in).** Issued BY the user TO their customers. Never say "obligation" for invoices.
- **Invoice lifecycle.** **DRAFT → add line items → finalize → FINALIZED (immutable)**. To correct after finalize: void → create new.
- **Products & prices.** Every invoice line item needs a product. For document-specific ad-hoc fees (shipping, handling, setup fees, tax), always use the **inline price mechanism** (see Path B) with a newly created product rather than matching existing fee products — fee amounts vary per order. Only reuse existing products for the core goods/services sold.
- **Invoice vs Subscription.** One-time quote → Invoice. Recurring terms → Subscription. Choose before creating.
- **ONE_OFF vs RECURRING.** Baked in at price creation — cannot flip later.
- **`collection_method` mapping from document language:**

| Document says | API value |
| --- | --- |
| "send invoice", "bank transfer", "wire transfer", "offline payment", "pay by bank" | `OUT_OF_BAND` |
| "online payment", "checkout", "payment link", "pay online" | `CHARGE_ON_CHECKOUT` |
| "auto-debit", "direct debit", "auto-charge" | `AUTO_CHARGE` |

Never use `SEND_INVOICE`, `MANUAL`, `AUTOMATIC`, or any value not in the exact list: `AUTO_CHARGE`, `CHARGE_ON_CHECKOUT`, `OUT_OF_BAND`. Always ask the user if the document language is ambiguous.

### Operational rules

- **For ambiguous-intent requests, do not start the workflow until the action is confirmed.**
- **NEVER fabricate or assume missing information.** If any required field is uncertain, absent, or ambiguous — STOP and ask the user. Do NOT fill in defaults, placeholder values, or "reasonable guesses".
- **Flag extraction uncertainty with `[?]`** — never guess currencies, quantities, or amounts.
- **Never round or modify extracted amounts.**
- **Always fetch fresh data** — re-fetch before every step.
- **Prefer business labels over raw IDs in user-facing output.** Show customer names and product names first; surface IDs only when operationally necessary or when the user asks.
- **One wallet, multiple currencies.** Say "AUD balance" — never "AUD wallet."
- **Live production data.** Treat every write as a real production write. Show extracted data in five tables and get user confirmation before any API call.
- **Search for existing customers and core products/prices before creating** — avoid duplicates. (Ad-hoc fee products like shipping/handling are exempt — see Terminology.)
- **Always confirm before finalizing** — finalization is **irreversible**.
- **Prices must match target:** **ONE_OFF** for invoice line items, **RECURRING** for subscription items.
- **Infer collection method from the document** using the mapping table. If the document clearly implies a method, use it and note the choice; ask the user when the language is genuinely ambiguous or absent. If the inferred method is `CHARGE_ON_CHECKOUT`, ask for `linked_payment_account_id` — without it the invoice has no checkout link and is unusable.
- **Never claim external payment-gateway setup.** This skill creates Airwallex Billing resources only. If the user also asks for an unsupported extra (e.g., Stripe gateway), complete the Airwallex Billing setup first, then separately state what was not configured and why.
- **Never invent billing automation fields.** If dunning, reminder cadence, or external collection support is unconfirmed, say so plainly and omit guessed JSON fields.
- **Write safety.** Show the full payload and get confirmation before every write — invoice create / line-item add / finalize / void / mark-paid / subscription create. Action commands (finalize / void / mark-paid) need the same confirmation as create/update.

### Invoice & subscription constraints

- **`legal_entity_id`** — **Before creating any invoice or subscription**, ask the user: *"Does your account have multiple legal entities? If so, please provide the `legal_entity_id` (available in the Airwallex Dashboard)."* If the account has multiple legal entities and this field is omitted, the API rejects with `"Need to specify the legal_entity_id in the request"`. This ID is **not discoverable via API**. If the user confirms only one legal entity, omit the field.
- **`collection_method` MUST be set BEFORE finalize** — set at create time or via the invoice update operation.
- **Invoice body shape.** Amounts live in line items (no top-level amount field); customer is `billing_customer_id`; notes go in `memo`. There is no `description` field on invoices.
- **Amounts come from line items, not the invoice create body** — `invoice_items` in the create body is **silently ignored**. Add items via the dedicated add-line-items operation after the draft exists. (Convenience: this connector also accepts `line_items` on the invoice *create* — it creates the draft, attaches the items, and returns the refreshed invoice. If that attach step fails you get the draft back with a `warnings` entry, so always check the returned total before finalizing.)
- **Pick `due_at` OR `days_until_due`** — passing both is rejected.
- **Timestamp format:** include an explicit timezone — bare dates are rejected. Most body fields accept both `+0000` and `Z`. **Tested exception:** the invoice listing only accepts `+0000` — `Z` returns a 400. Do NOT pre-encode the offset to `%2B0000`.
- **Line items body shape.** The add operation wraps the array in `line_items`. Bare arrays are rejected. Line items only accept **ONE_OFF + PER_UNIT/FLAT** prices — RECURRING, VOLUME, GRADUATED are rejected. If the contract has tiered pricing, split into separate PER_UNIT line items per band.
- **Inline price objects do NOT include `currency`** — inherited from the invoice.
- **Verify the draft has items (`total_amount > 0`) before finalize.** A draft with no line items fails to finalize — and `invoice_items` in the create body is silently dropped, so this state is easy to land in by accident.
- **Correcting line items:** this connector exposes add + list line items, but not update or delete. To change a line item on a DRAFT, void the draft and re-create, or direct the user to the Airwallex Dashboard.
- **Discounts:** use coupons (`"discounts": [{"type": "COUPON", "coupon": {"id": "..."}}]`), not negative amounts. **Credit notes** are not exposed by this connector — direct the user to the Airwallex Dashboard.
- **Coupons:** PERCENTAGE vs FLAT are mutually exclusive. PERCENTAGE → `percentage_off` (0–100), no `currency`/`amount_off`. FLAT → `amount_off` + `currency`, no `percentage_off`. `duration_type: CUSTOM` needs a `duration` object with both `period` and `period_unit`.
- **`metadata`** replaces entirely on update — omit to keep existing.
- **Tiered pricing** uses `upper_bound` (not `up_to`); the last tier omits `upper_bound` entirely.
- **Price immutability:** cannot change `currency`, `pricing_model`, `amount`, or `tiers` via update — deactivate the old price and create a new one.
- **`starts_at`** (subscriptions) must be strictly future. Compute dynamically — never hardcode. Omit to default to "now".
- **Subscription `items[*].price_id`** must reference RECURRING prices — ONE_OFF rejected. **`AUTO_CHARGE`** requires `payment_source_id` — ask the user. `legal_entity_id` may also be required on subscription create in multi-entity accounts.
- **Tax handling** — Airwallex Billing has no built-in tax-rate engine. If the document includes GST, VAT, or sales tax, extract the tax amount and create it as an explicit line item (with a dedicated "Tax"/"GST" product) or include the tax-inclusive amount in the unit price. Flag `[?]` if it is unclear whether prices are tax-inclusive or exclusive, and ask. Do NOT silently compute tax.
- **The connector auto-generates `request_id`** for create operations — you do not need to supply it.
- **Pagination:** `page_size` minimum 10 across billing list endpoints. Most billing listings use cursor pagination — pass the returned `page_after` bookmark into the next call. Repeat until the cursor is absent.

---

## Workflow

### Phase 1: Extract

**Step 1 — Get the document.** Accept local files (`.pdf` `.docx` `.txt` `.md` `.png` `.jpg` `.webp`) or pasted text. If the host cannot read a PDF/image reliably, do **not** pretend it was read — ask the user to re-upload, paste the text, or provide a readable format before extracting.

**Step 2 — Extract billing details.** Read the **entire** document. Distinguish the **product catalog** (all products/pricing defined in the contract) from the **current order** (specific items being billed now). Identify: customer (name, address, email), document reference, currency, payment terms, all products and pricing, fees, and subscription terms if applicable.

**Step 3 — Build five tables** (always structured tables, not prose; show a table marked `N/A` if a section does not apply):

1. **Products** — name, description, unit, active, in current order?
2. **Prices** — product, unit price, currency, frequency, pricing model, tiers
3. **Customers** — name, email (required), location
4. **Subscriptions** — only if the document has recurring terms (N/A otherwise)
5. **Invoices & Fees** — shipping, setup fees, tax (rate and whether prices are tax-inclusive or exclusive), reference, payment terms, due date

**Step 4 — Validate and confirm.** Cross-check against API requirements. List all gaps explicitly. Accept natural-language corrections and loop until the user approves. Do NOT proceed to any create/finalize call until every required field is complete and the user confirms.

### Phase 2: Match & Create

**Step 5 — Confirm live data.** Validate required fields for all planned operations.

**Step 6 — Match existing resources.** Search customers by `email` (filter on the customers list). The products list has **no name filter** — paginate fully and match by name client-side. Search prices by `product_id`. Present matches and get confirmation. **Only match core goods/services.** Do NOT match existing products for per-order ad-hoc fees (shipping, handling, setup) — always create fresh products for these and use inline prices in line items.

**Step 7 — Create missing resources.** Create ALL missing products and needed prices from the contract (full catalog), not just the current order. Price type: N/A (Table 4) → ONE_OFF; has subscription data → RECURRING. Pricing model: FLAT (fixed), PER_UNIT (per-seat), VOLUME/GRADUATED (tiered).

**Step 7b — Confirm collection method.** Use the method inferred from the document; if ambiguous or silent, ask now. If `CHARGE_ON_CHECKOUT`, require `linked_payment_account_id` from the user — do not guess.

**Step 8 — Route based on Table 4:**

| Table 4 | Action |
| --- | --- |
| Has subscription data | → Create subscription |
| N/A (one-time) | → Create invoice |
| Both | → Subscription for recurring + invoice for one-time fees |

#### Path A: Subscription

Create a subscription with `billing_customer_id`, `currency`, `collection_method`, and `items` (RECURRING prices). Verify after creation. **Receivables note:** remind the user this subscription generates recurring invoices (expected money in). Mention the subscription ID, currency, billing interval, and next billing date so they can cross-reference with the **airwallex-manage-cashflow** skill. (Note: this connector cannot cancel subscriptions — direct cancellation requests to the Airwallex Dashboard.)

#### Path B: Invoice

**Create draft** with `billing_customer_id`, `currency`, `collection_method`, optional `days_until_due`/`due_at`, and `memo`.

**Add line items** with the dedicated add operation after the draft exists. For an existing price: `{"price_id": "...", "quantity": N}`. For ad-hoc fees, use an inline price: `{"price": {"product_id": "...", "pricing_model": "FLAT", "flat_amount": 350.00, "description": "Shipping"}, "quantity": 1}`. Do NOT include `currency` in an inline price. Convert tiered pricing into invoice-compatible PER_UNIT/FLAT line items per band.

**Finalize** — confirm with the user first. Show a summary: resources created/reused, total, due date, `pdf_url`, `hosted_url`. **Receivables note:** after finalize, remind the user this invoice is now a receivable (expected money in). Mention the invoice ID, amount, currency, and due date. For a batch, also show a one-line aggregate of total outstanding per currency (e.g., "3 invoices totalling 47,200 GBP outstanding") so the cash-position impact is immediately visible.

### Phase 3: Share with Customer (opt-in only)

Must be explicitly requested. After finalize, present:
- **`pdf_url`** — direct link to the PDF (always available on finalized invoices).
- **`hosted_url`** — online checkout page. Only available when `collection_method` is `CHARGE_ON_CHECKOUT`. For `OUT_OF_BAND` invoices, `hosted_url` may be absent — share the `pdf_url` and instruct the customer on bank transfer details.

Airwallex Billing has **no API to email invoices directly** — the agent cannot send on the user's behalf. Offer to draft a payment email the user can copy and send themselves.

---

## Error handling

| Situation | Action |
| --- | --- |
| Document unreadable | Ask for the content another way and stop |
| Ambiguous extraction | Flag with `[?]`, ask the user, do not guess |
| `legal_entity_id` required (missed pre-check) | Account has multiple legal entities. Ask which `legal_entity_id` to use (not discoverable via API), include it in the body, and retry |
| Draft fails to finalize | Verify `total_amount > 0` — the draft likely has no line items; add them via the add-line-items operation first |
| User requests external gateway setup | Explain it is outside this skill's scope; continue with Airwallex Billing only if the user still wants that |
| Credit note / line-item edit / subscription cancel requested | Not exposed by this connector — direct the user to the Airwallex Dashboard |
| Auth expired | The connector refreshes tokens automatically; if a tool keeps failing on auth, ask the user to re-authorize the Airwallex connection |

---

## Workflow summary

```
Phase 1: Extract
  get document → read → extract → build 5 tables → validate → user confirms

Phase 2: Match & Create
  confirm live data → match existing → user confirms → create missing
    → confirm collection method
      → if recurring: subscription → if one-time: invoice → finalize
      → receivables note (cross-ref with airwallex-manage-cashflow)

Phase 3: Share (opt-in)
  present URLs (pdf_url + hosted_url) → draft email if requested
```

---

## Attribution

Adapted from Airwallex's official AgentOS `contract-to-billing` skill, licensed under the Apache License 2.0 (see LICENSE.txt). Modified for the ChatChat Airwallex connector: CLI-specific instructions and external URLs removed, supporting reference files inlined, workflow steps aligned to the operations this connector actually exposes, and unsupported operations redirected to the Airwallex Dashboard.
