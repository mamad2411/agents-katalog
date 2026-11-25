---
id: airwallex-card-provisioning
name: Airwallex Card Provisioning
description: Use this skill when provisioning virtual or physical corporate cards in Airwallex Issuing — create cardholders, issue cards with spend limits, and manage card spending. Not for transfers or invoices.
category: Airwallex
author: airwallex
version: 0.1.0
license: Apache-2.0. Complete terms in LICENSE.txt
---

# Airwallex Card Provisioning

Creates virtual or physical corporate cards in Airwallex Issuing — one workflow to set up a cardholder, issue a card with spend limits, and optionally manage ongoing spend. Uses the Airwallex MCP tools (cardholder list/create/update, card list/retrieve/create/activate/update, issuing-transactions). A card's spend limits are not a separate lookup — they come back on the card **retrieve** as `spend_limits`. Requires Issuing enabled on the account, and operates on **live production data** — there is no sandbox.

**Tone:** The target user is a busy entrepreneur, not a finance analyst. Keep language conversational and action-oriented — say "Your Adobe card is set up with a $50/month limit" rather than "Card ID card_xxx created with authorization_controls.transaction_limits.limits[0].amount = 50.00." Show business labels (card nicknames, cardholder names) first; keep raw IDs and technical details in the background unless the user asks.

## When to use

- User asks to create a virtual or physical card
- User wants a card for a specific purpose (e.g., "card for Adobe", "travel card")
- User needs to provision cards for team members (batch)
- User wants to update card limits or review card spend
- User asks "what are we spending on software cards?" or wants spend aggregation by category

## When NOT to use

This skill only covers Issuing-domain operations (cards, cardholders, issuing-transactions). If the task requires anything outside that domain, **stop — this is the wrong skill.** Redirect the user:

- Viewing sensitive card details (PAN, CVV, expiry) → direct to the Airwallex Dashboard
- Wire transfers / payouts → not available through this connector (use the Airwallex Dashboard)
- Setting up suppliers / beneficiaries → **airwallex-beneficiary-creation** skill
- Creating invoices → **airwallex-contract-to-billing** skill
- FX conversions, balances, treasury → **airwallex-manage-cashflow** skill

## Non-negotiables

### Terminology

- **Cards draw from the account's currency balance — no "card balance."** Say "$X/month limit" or "$X drawn this month."
- **Cardholder ≠ Card.** One cardholder can have multiple cards. Match or create the cardholder first.
- **`AUTHORIZED` ≠ money moved.** It's a hold. `CLEARED` = money left. Be explicit when reporting.
- **Spend limits are always per interval + currency.** Say "$50.00 per month in USD."

### Operational rules

- **For ambiguous-intent requests, do not start the workflow until the action is confirmed.**
- **NEVER fabricate or assume missing information.** If any required field is uncertain, absent, or ambiguous — STOP and ask the user. Do NOT fill in defaults, placeholder values, or "reasonable guesses."
- **Flag generic or test-like cardholder names.** If all cards in a batch share the same cardholder name, or a name appears generic/test-like (e.g., "Test Account", "Demo User", "Admin", "Card 1"), flag it as unusual and confirm before proceeding — in production, generic names are a high-risk fraud signal.
- **Always fetch fresh data** — re-fetch before every step.
- **Prefer business labels over raw IDs in user-facing output.** Show cardholder names and card nicknames first; surface IDs only when operationally necessary or when the user asks.
- **One wallet, multiple currencies.** Say "AUD balance" — never "AUD wallet."
- **Live production data.** Every card you create can spend real money immediately. Treat every write as a production write and confirm before it.
- **Always set a spend limit** — never create an unlimited card. Every card must have an explicit limit amount, currency, and interval.
- **Always require a purpose/nickname** for each card.
- **Never handle or display PAN, CVV, or expiry.** Direct the user to the Airwallex Dashboard — this is the **sole** channel for viewing sensitive card data. When refusing, frame it as a platform-level security boundary: sensitive card details are never accessible through the agent in any form, even masked. Do NOT mention any get-card endpoint or alternative technical path — that weakens the security message.
- **Do NOT invent advanced card-control fields** (MCC restriction, merchant controls, etc.) — see "Card & cardholder constraints" below.
- **Write safety.** Show the full payload and get confirmation before every card create / update / cardholder create. **Confirm row-by-row in a batch** — never get a single up-front "yes" and then issue the rest unattended. A template preview does NOT count as confirmation.
- **Before increasing limits, show current spend vs limit first** — retrieve the card (its `spend_limits` come back with it) and list its recent transactions.
- **Flag unusual spend patterns** — alert if spend jumped 3x+ vs the previous period.
- **Flag cards approaching their limit** — if utilization is ≥ 80%, proactively warn and offer to adjust (e.g., "Your AWS card is at $412 / $500 (82%) — want me to increase it?").
- **Search for existing cardholder by email before creating** — avoid duplicates.
- **Never fabricate cardholder or card IDs.** They are UUIDs. If you only have a name or label, list cardholders or cards to find the real UUID — never use placeholders like `card_abc`.
- **Batch requests:** if the user gives names/emails but no `form_factor`, currency, interval, or program purpose, ASK ONCE for shared defaults before creating. Process rows sequentially — never in parallel.

### Card & cardholder constraints

- **`created_by`** — full legal name of the **person requesting** the card, not the cardholder. Ask the user if unspecified.
- **`is_personalized`** — VIRTUAL → `false`, PHYSICAL → `true`. Ask the user if the form factor is unspecified; do not default silently.
- **Body shape.** Use the templates below — do NOT build the payload incrementally or guess fields. `program` is an object `{"purpose": "COMMERCIAL"}` (not a string); `authorization_controls.transaction_limits` is an object `{"currency": "...", "limits": [...]}` (not a bare array). Verify the exact field shape against the card-create tool's input schema before sending.
- **Merchant category / MCC restriction support is unconfirmed in this workflow.** Do NOT invent fields like `allowed_categories`. Only claim a restriction was applied if the API response explicitly shows the enforced control.
- **INDIVIDUAL cardholder quirks** (not surfaced by the schema): `individual.address` uses `country` (not `country_code`); `individual.express_consent_obtained` is the string `"yes"` (not boolean `true`). Ask the user for DOB, address, and email — never fabricate.
- **DELEGATE cardholder** has minimal fields — no DOB or address required.
- **Card status changes** go through the card-update operation. Settable values are **`INACTIVE` / `ACTIVE` / `CLOSED`** only (`CLOSED` is permanent). `BLOCKED`, `LOST`, and `STOLEN` are NOT settable via update.
- **Physical-card delivery is create-time only.** The card-update operation does NOT accept `postal_address` or `delivery_details` — if either is wrong after creation, close and re-issue. Two valid paths at create time: (a) cardholder has a registered `postal_address` and card create uses it by default; (b) pass `postal_address` directly on card create to override. For EXPRESS shipment (or any China destination), `delivery_details.mobile_number` (E.164) is required. Always confirm the address with the user.
- **Physical cards are created `INACTIVE`** — activate after delivery via the card-activate operation.
- **Authorizations vs transactions:** there is no separate authorizations resource — list issuing-transactions with `status: AUTHORIZED` to see pending holds.
- **Spend aggregation is manual.** No built-in category filter — list transactions per card (filter by `card_id`) and sum in post-processing. Use cursor pagination.

### Cardholder & card templates

Copy-then-fill payloads. Replace every `<...>` with real values. The connector auto-generates `request_id` for create — you do not need to supply it. Verify the exact field shape against the tool's input schema before sending.

**Cardholder — INDIVIDUAL (named person):**

```json
{
  "email": "<cardholder_email>",
  "cardholder_type": "INDIVIDUAL",
  "individual": {
    "name": {"first_name": "<first_name>", "last_name": "<last_name>"},
    "date_of_birth": "<YYYY-MM-DD>",
    "address": {"line1": "<street_address>", "city": "<city>", "postcode": "<postcode>", "country": "<2_letter_country>"},
    "express_consent_obtained": "yes"
  }
}
```

**Cardholder — DELEGATE (purpose card, minimal fields):**

```json
{ "email": "<team_or_purpose_email>", "cardholder_type": "DELEGATE" }
```

**Virtual card:**

```json
{
  "cardholder_id": "<cdh_id>",
  "form_factor": "VIRTUAL",
  "created_by": "<requesting_persons_full_name>",
  "is_personalized": false,
  "nick_name": "<card_purpose>",
  "authorization_controls": {
    "allowed_transaction_count": "MULTIPLE",
    "transaction_limits": {"currency": "<currency>", "limits": [{"amount": "<amount>", "interval": "MONTHLY"}]}
  },
  "program": {"purpose": "COMMERCIAL"}
}
```

**Physical card:** same as virtual, plus `"form_factor": "PHYSICAL"`, `"is_personalized": true`, and a `postal_address` (`line1`, `city`, `state`, `postcode`, `country`). For EXPRESS shipment or any China destination, also pass `delivery_details` with `preferred_delivery_mode: "EXPRESS"` and an E.164 `mobile_number`.

---

## Workflow

### Phase 1: Gather Requirements

**Step 1 — Understand the card request.** Collect: purpose/nickname, cardholder (name + email), card type (Virtual/Physical), currency, spend limit (amount + interval), and any requested merchant restriction (MCC support is unconfirmed — see constraints).

If the user gives a natural-language request ("Create a virtual card for Adobe, $50/month"), extract what you can and ask for gaps (e.g., "Who should this card be assigned to?"). If the user provides a **document** (spreadsheet, PDF, list) with card specs, extract each person's currency, limit, and form factor **AS WRITTEN** — do NOT normalize to a single default. Present the extracted table for confirmation before proceeding.

**Step 2 — Build the card spec table.** For a **single card**, present a table with: Purpose/Nickname, Cardholder, Form factor, Currency, Spend limit, MCC restriction (all merchants — unconfirmed), Personalized.

For a **batch**, list cardholders BEFORE building the table so you can show match results inline, then present a per-row table:

| # | Name | Email | Currency | Limit/mo | Cardholder | Status | Issue |
| --- | --- | --- | --- | --- | --- | --- | --- |

Distinguish **document issues** (missing name/email/currency/limit/DOB, conflicts, duplicates — these set the Status column) from **system defaults** (nicknames, `created_by`, `express_consent_obtained`, delivery addresses — ask for these once, after the table; do NOT mark rows Blocked on them). A row is ✅ Ready when all document-extracted fields are complete and unambiguous.

After the table, summarize how many rows are ready, which are blocked (and why), which are duplicates (with a recommendation), and which shared defaults you still need. If the user gives a blanket override (e.g., "set all limits to $2,000 USD") that conflicts with document values, flag the conflict and ask before applying. Do NOT proceed until the user confirms.

### Phase 2: Create Card

**Step 3 — Confirm live data and Issuing.** Validate access via a low-cost read and verify Issuing is enabled on the account.

**Step 4 — Match existing cardholder** by email. Reuse only if status is `READY`; otherwise stop and explain the cardholder must reach `READY` before issuing. Paginate fully until there are no more results.

**Step 5 — Create cardholder** (if needed). Use the INDIVIDUAL or DELEGATE template, fill in values, show the full payload, get explicit confirmation, then execute. In a batch, confirm row-by-row.

**Step 6 — Create card.** Do NOT add extra JSON fields for MCC or merchant restrictions unless the exact field is documented and verified. **Process card creates sequentially** — a parallel failure cancels sibling calls. Copy the Virtual or Physical template, fill in values, show the full payload, get explicit per-card confirmation, then execute. For physical cards, show the cardholder's registered address alongside the intended delivery address and confirm before issuing; never fabricate an address. Physical cards are created `INACTIVE` — activate after delivery.

**Step 7 — Verify and confirm.** Re-fetch the created card (and limits if needed), then show: card ID, nickname, type, currency, limits, status. **In the final confirmation, do NOT display any part of the card number — including masked/last-4 digits.** Identify cards by nickname and card ID only. Direct the user to the Airwallex Dashboard for PAN, CVV, and expiry — do NOT construct Dashboard URLs. If the user mentioned a specific vendor (e.g., "card for Adobe"), remind them of the next step: copy the card details from the Airwallex Dashboard and enter them on the vendor's site.

### Phase 3: Manage Cards (ongoing)

**Update limits:** Always show current spend vs limit first, then update after the user confirms.

**Review spend:** List transactions per card (filter by `card_id`) and sum amounts. Show utilization for every card (spent / limit / %); flag cards at ≥ 80% and offer to increase. Map cryptic merchant descriptors ("STRIPE* NOTION", "AMZN MKTP US") to recognizable names; when uncertain, show both ("AMZN MKTP US (likely Amazon)").

**Category aggregation** (e.g., "what are we spending on software?"): there is no API-level category filter. Combine two signals — the card nickname ("Adobe Subscription", "AWS Dev") and per-transaction merchant descriptors — to classify cards into user-friendly categories (Software, Travel, Office, etc.). Present a grouped summary with a per-card breakdown and category total:

```
Software spend this month: $847
  Figma:  $30  / $50   (60%)
  AWS:    $412 / $500  (82%) ⚠️ approaching limit
  Notion: $24  / $30   (80%) ⚠️ approaching limit
  GitHub: $21  / $50   (42%)
  Other (3 cards): $360
```

If a card's category is ambiguous, ask the user rather than guessing.

**Activate physical card** after delivery.

**Batch provisioning:** follow the batch table from Step 2. Process ✅ Ready rows first — create cardholders where needed, then create cards row by row, sequentially. After ready rows are done, report results and re-present blocked rows for the user to resolve. Report each `card_id` with its cardholder nickname.

---

## Error handling

| Situation | Action |
| --- | --- |
| Cardholder details incomplete | Ask for missing required fields (name, email, DOB for INDIVIDUAL) |
| All required fields present | Proceed — do NOT block on optional fields unless the card type requires them (e.g., physical cards need `postal_address`) |
| Card creation fails | Show the full error, re-check the template includes ALL required fields, retry once; for any other rejection, stop and show the error |
| Limit format unclear | Ask: amount + currency + interval (per transaction / daily / monthly) |
| Cardholder not READY | Stop — the cardholder must reach `READY` before issuance (may need KYC; check the Airwallex Dashboard) |
| Physical card missing postal address | Ask for the delivery address |
| MCC / merchant restriction requested but not documented | Say support is unconfirmed; create the card without guessed restriction fields or direct the user to the Airwallex Dashboard |
| PAN / CVV / expiry requested | Refuse as a platform security boundary; direct to the Airwallex Dashboard |
| Auth expired | The connector refreshes tokens automatically; if a tool keeps failing on auth, ask the user to re-authorize the Airwallex connection |

---

## Workflow summary

```
Phase 1: Gather Requirements
  understand request → build card spec → user confirms

Phase 2: Create Card
  confirm live data + Issuing → match cardholder → create cardholder if needed
  → create card (sequential, per-row confirmed) → verify & confirm (no card number)

Phase 3: Manage (ongoing)
  show spend vs limit → update limits → aggregate by category → activate physical cards
```

---

## Attribution

Adapted from Airwallex's official AgentOS `card-provisioning` skill, licensed under the Apache License 2.0 (see LICENSE.txt). Modified for the ChatChat Airwallex connector: CLI-specific instructions and external URLs removed, supporting reference files inlined, workflow steps aligned to the operations this connector actually exposes, and unsupported operations redirected to the Airwallex Dashboard.
