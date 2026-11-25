---
id: airwallex-beneficiary-creation
name: Airwallex Beneficiary Creation
description: Use this skill when onboarding suppliers or vendors in Airwallex — extract bank details from invoices/documents, validate per-country requirements, and create beneficiaries. Not for money transfers.
category: Airwallex
author: airwallex
version: 0.1.0
license: Apache-2.0. Complete terms in LICENSE.txt
---

# Airwallex Beneficiary Creation

Reads supplier invoices or documents, extracts bank details, validates them against country-specific schemas, and creates beneficiaries in Airwallex. **This skill creates beneficiaries only — money movement (transfers) is not in scope and is not available through this connector.**

This skill uses the Airwallex MCP tools (beneficiary list / schema / create / update / verify). It operates on **live production data** — there is no sandbox. Treat every write as a real production write.

## When to use

- User uploads supplier invoices, contracts, vendor lists, or documents with bank details
- User asks to "set up a supplier", "onboard a vendor", or "add a payee"
- User wants to create beneficiaries from extracted bank information
- User has multiple suppliers to onboard in batch

## When NOT to use

This skill only covers Payouts-domain operations — listing, creating, updating, and verifying beneficiaries, plus beneficiary-schema lookup. If the task requires anything outside this domain, **stop — this is the wrong skill.** Redirect the user:

- Wire transfers / payouts / actually sending money → not available through this connector (use the Airwallex Dashboard)
- Creating invoices (money in) → **airwallex-contract-to-billing** skill
- FX conversions, balances, treasury → **airwallex-manage-cashflow** skill
- Provisioning corporate cards → **airwallex-card-provisioning** skill

## Non-negotiables

### HARD GATE — money-movement requests

If the user's message mentions **transferring, sending, wiring, or paying money** (e.g., "set up and transfer", "send $15K to them", "pay this supplier now"):

1. **The very first sentence of your reply** must state the capability boundary: *"I can set up [name] as a beneficiary, but I can't execute transfers — that must be done in the Airwallex Dashboard after the beneficiary is created."*
2. Do NOT ask for payment amount, payment reason, source balance, or any transfer-related details — these are not inputs to this skill.
3. Do NOT imply that the transfer will happen as part of this workflow or that you will "set up the payment right away."
4. After stating the boundary, proceed normally with the beneficiary-creation workflow.

This gate fires even if the transfer request is mixed with a valid beneficiary-creation request. Acknowledge what you CAN do, clearly state what you CANNOT, then continue with the part you can handle.

### Terminology

- **Beneficiary = first step of the payout workflow.** The full payout flow is: **create beneficiary → (optional) verify bank ownership → initiate transfer (Airwallex Dashboard only)**. This skill covers the first two steps.
- **Beneficiary ≠ transfer.** Creating a beneficiary saves payee details — it does NOT send money. Duplicate beneficiaries waste time later, which is why the skill searches for existing records before creating.
- **LOCAL vs SWIFT.** LOCAL = domestic clearing (cheaper, faster). SWIFT = international wire (costlier). Do NOT silently pick a transfer method — determine the available rails from the document and schema, then present the options to the user with a brief note on cost/speed. If the document states a preferred rail, surface it but still confirm. Only when the document is silent AND the schema shows exactly one supported rail for the country/currency combo may you proceed without asking.
- **COMPANY vs PERSONAL.** COMPANY = business entity. PERSONAL = individual (freelancer). Determines required identity fields.
- **Schema is authoritative but incomplete.** The schema's `required` flag is not always accurate — some fields marked optional are actually required by the API. When in doubt, include every field the country's banking rules list as required, even if the schema says optional, and ask the user rather than guessing.

### Operational rules

- **For ambiguous-intent requests, do not start the workflow until the action is confirmed.** If the user has not clearly confirmed the exact write action, stop before schema reads or other workflow setup that materially advances execution.
- **NEVER fabricate or assume missing information.** If any required field is uncertain, absent, or ambiguous — STOP and ask the user. Keep asking until you have every parameter needed. Do NOT fill in defaults, placeholders, or "reasonable guesses." The only data you may fill in yourself is `nickname` — beneficiary calls take no `request_id`, so never invent one.
- **NEVER echo back unverified field names from the user.** If the user mentions routing types, code names, or bank-detail parameters that you have not confirmed via a schema fetch, do NOT include them in your response as if they were real API fields. Instead: (1) acknowledge what the user asked for, (2) fetch the beneficiary schema for that country/currency/transfer-method combo, (3) reply with only the fields the schema actually requires — and flag any user-mentioned terms that do not map to a schema field. Parroting an unverified parameter name back — even just to ask for its value — treats it as a real field and is a form of hallucination.
- **Even when the user says "use example data"** — STOP and list the concrete fields needed. Offer to create a JSON template for them to fill in.
- **Flag any extraction uncertainty** — never guess at bank details.
- **Always fetch fresh data** — re-fetch before every step.
- **Prefer business labels over raw IDs in user-facing output.** Show beneficiary names first; surface IDs only when operationally necessary or when the user asks.
- **Live production data.** Every beneficiary you create is a real payee record. Show the full payload and get explicit confirmation before every create / update / verify.
- **There is no payload-validation API — check before you create.** Safety comes from the two things you actually can do: cross-check every field against the beneficiary schema client-side, and (where supported) run `verify` on the candidate bank details before creating. Only create once both pass AND the user confirms.
- **Search for existing beneficiaries by name before creating** — duplicate beneficiaries clutter the payout workflow.

### Beneficiary constraints

The create/update body takes its fields at the **top level**, with bank fields nested inside `bank_details`. Do NOT wrap the payload in a `{ "beneficiary": {…} }` envelope. Verify exact field names against the beneficiary schema (the `getSchema` action) before sending:

```json
{
  "bank_details": {
    "account_name": "...",
    "account_number": "...",
    "account_routing_type1": "sort_code",
    "account_routing_value1": "123456",
    "bank_country_code": "GB",
    "account_currency": "GBP"
  },
  "entity_type": "COMPANY",
  "company_name": "Acme Ltd",
  "address": {
    "city": "London", "country_code": "GB",
    "postcode": "EC1A 1BB", "street_address": "123 Main St"
  },
  "transfer_methods": ["LOCAL"],
  "nickname": "Acme supplier"
}
```

- **Fetch the schema for EVERY unique country/currency/transfer-method/entity-type combo before building ANY JSON.** Use the `getSchema` action with `bank_country_code`, `account_currency` (not `currency`), `transfer_method`, and `entity_type`. When the schema does not surface valid values for routing types, state formats, or fields like `bank_account_category`, ask the user — do not guess.
- **`transfer_method` vs `transfer_methods`.** Schema fetch and `verify` use the singular `transfer_method`. The create/update body uses the plural array (`"transfer_methods": ["LOCAL"]`). Mixing the two causes API rejection.
- **Top-level vs nested fields.** `transfer_methods` is a top-level array. `bank_country_code` and `account_currency` live inside `bank_details`. The schema-fetch call takes singular `transfer_method` plus `bank_country_code` and `account_currency` as top-level parameters — do not confuse the two shapes.
- **`account_name`** inside `bank_details` is required for most countries even when the schema does not mark it required.
- **SWIFT uses `swift_code`, not routing** — do NOT put a BIC in `account_routing_type1` (LOCAL routing only). IBAN countries may still require both `iban` and `swift_code` on SWIFT.
- **LOCAL routing keys vary by country** (`sort_code`, `aba`, `bsb`, etc.) — use the schema, never hardcode.
- **`bank_account_category`** — required for **US/USD/LOCAL** (both COMPANY and PERSONAL) and some personal accounts (e.g., BR). Valid values: **`"Checking"` / `"Savings"`** (note the `s`). The schema may omit this field — always include it for US beneficiaries and ask the user for the value.
- **SE/SEK/LOCAL** — the schema marks `account_routing_type1`, `account_routing_value1`, and `account_number` as optional — **they are actually required**. IBAN alone is NOT enough. Include `account_routing_type1` (`bank_code`), `account_routing_value1` (clearing number, 4–5 digits), and `account_number`. Ask the user for these values.
- **`entity_type` drives required name fields.** COMPANY uses `company_name`; PERSONAL uses `first_name` + `last_name`, plus `additional_info` for tax IDs (`personal_id_type` and `personal_id_number`). The schema does not always surface the conditional `additional_info` requirement.
- **List search uses `name` (PERSONAL) / `company_name` (COMPANY)** — there is no `first_name` filter. Use the actual filter names exposed by the listing operation; do not invent filters from JSON body field names.
- **Do NOT decompose IBANs into bank_code + account_number yourself** — if the schema requires separate routing and account fields but the document only provides an IBAN, tell the user exactly which fields are needed and ask them to provide the values. IBAN BBAN structures vary by country; guessing the split causes validation failures.
- **Preserve original values during extraction; normalize only when building the JSON payload.** In the extraction table, show bank details **AS WRITTEN** in the document (e.g., "Agência: 1234-5", "Conta Corrente: 1234567-8") and explicitly label the API field mapping. Do NOT strip formatting during extraction.
- **Strip formatting to match a schema `pattern` only when constructing the payload.** Check the field's `pattern` regex first, then strip only characters that prevent a match. E.g., GB sort code pattern `^[0-9]{6}$` → strip hyphens from `20-32-06` to get `203206`. If the pattern already allows the characters, preserve the original value. **Always show the before→after transformation** so the user can verify.
- **`address.state` uses ISO 3166-2 codes** with country prefix (e.g., `CA-ON`, `AU-NSW`, `IN-KA`). Do NOT use a bare abbreviation.
- **Account number errors (`066`, `086`)** mean wrong length or invalid format — ask the user, never pad or truncate.
- **`verify` ≠ `create`** — `verify` only checks the candidate bank details, it does NOT create the beneficiary. There is no separate payload-validation operation on this connector, so your pre-flight is the schema cross-check plus `verify`; then confirm with the user and create.
- **Multiple banking options in one document** — if a document lists more than one bank account or transfer method (e.g., LOCAL SEK + SWIFT EUR), surface ALL options and ask which to use. Follow the document's stated preference if one exists. Do NOT silently pick one.
- **Pagination:** use `page_num` (0-based) + `page_size`; increment until there are no more results.

---

## Workflow

### Phase 1: Extract

**Step 1 — Get the document(s).** Accept one or more supplier invoices, contracts, vendor lists, or bank-detail documents. Batch supported.

**Step 2 — Extract supplier and bank details.** Identify: supplier name, entity type, bank name, bank country, currency, account number/IBAN, routing code(s), address (all five components: `street_address`, `city`, `state`, `postcode`, `country_code`), contact info. Documents may be in any language — extract bank details regardless of language, keep company/entity names in their original language, and present the extracted summary in English for confirmation.

**Step 2b — Verify user-supplied field names against the schema.** If the user's request mentions routing types or bank-detail parameters you cannot confirm exist, **do NOT echo them back as required fields.** Proceed to the schema fetch (Step 5) first, then return with only the fields the schema actually requires — and call out any user-mentioned terms that don't correspond to real API fields.

**Step 3 — Clarify intent before proceeding.** Present the extracted summary and explicitly ask what the user wants:
- **Create new** beneficiary — proceed to the schema check and creation.
- **Update existing** — search first, show matches, then update.
- **Check for duplicates only** — search and report without creating.
- **Something else** — clarify before committing to a path.

Do NOT assume "create new" by default. If the request is ambiguous (e.g., "set up this supplier" could mean create or update), ask. If more than one possible supplier/payee exists in the attachment or context and the user's wording does not unambiguously identify which records to act on, present the candidate list and ask which specific record(s) they mean before any schema check or API call.

**Step 4 — Confirm you are working on live production data.** Confirm access via a low-cost read (e.g., list beneficiaries).

**Step 5 — Fetch the country-specific schema.** For EVERY unique country/currency/transfer-method/entity-type combo, run the `getSchema` action to get the required fields and patterns. When the schema is silent on valid enum values, routing formats, or extra field requirements, ask the user — do not fabricate.

**Step 6 — Build a beneficiary table:**

| # | Company/Name | Entity Type | Bank Country | Currency | Transfer Method | Key Bank Fields | State | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Fill `State` with an ISO 3166-2 code or `n/a`. Mark incomplete rows with `[?]`.

**Step 7 — Check and confirm.** Cross-check every row against the schema fetched in Step 5. Do NOT proceed until every row passes and the user confirms.

### Phase 2: Check & Create

**Step 8 — Completeness check.** Before the first write, cross-check each planned payload against its schema: every required field present, every value matching the schema's `pattern`. List any gaps and resolve them with the user.

**Step 9 — Match existing beneficiaries.** Search by `name`/`company_name`. Paginate fully. If a match exists, the user decides: skip, update, or create new.

**Step 10 — Pre-flight with `verify` (recommended).** `verify` takes a candidate `bank_details` payload and needs no existing beneficiary record, so it catches country-specific bank-detail errors *before* you create anything. **Process one at a time, sequentially** — do NOT parallelize (a parallel failure cancels sibling calls). Show each result. If `verify` is unsupported for that country/transfer method, say so and rely on the Step 8 schema cross-check.

**Step 11 — Confirm before writes.** Re-state to the user that these are live production records. Wait for explicit approval before proceeding.

**Step 12 — Create.** **HARD GATE: NEVER attempt `create` for a row with missing or schema-mismatched fields, or one whose `verify` came back `INVALID`.** Fix it first (ask the user for corrected data) or skip that row entirely. Retrying create with the same bad payload wastes turns and will fail identically. **Process one at a time, sequentially.** Create only checked, unmatched rows. Wait for each creation to succeed before starting the next. Report each result immediately.

**Step 13 — Summary & next steps.** Show the final summary: created / skipped / failed. Then advise:
- **Verify** — offer bank account ownership verification if the country supports it (Phase 3).
- **Transfer** — remind the user that transfers must be initiated in the Airwallex Dashboard (this connector cannot move money).
- **Cashflow impact** — if the user plans to pay these suppliers soon, note that each payout will reduce their currency balance. Suggest the **airwallex-manage-cashflow** skill to check whether current balances cover the planned payments and whether any FX conversion is needed first.

### Phase 3: Verify bank account (standalone or post-create)

Bank account ownership verification confirms the account belongs to the named beneficiary. This is the same `verify` operation as Step 10 — run it as a pre-flight before creating, or here on its own. Not all countries or transfer methods support it.

**Step 14 — Check verify eligibility.** Confirm the verify action is available. If the verify call rejects with an unsupported-country or unsupported-method error, explain and suggest the Airwallex Dashboard as a fallback.

**Step 15 — Submit verification.** The verify action takes a candidate `bank_details` payload — **NOT a beneficiary ID** — so you can verify before the beneficiary record exists. Body shape: `entity_type`, `transfer_method` (singular), `bank_details`. No `request_id`. Show the verification status to the user. Possible responses include `VERIFIED`, `INVALID`, `CANNOT_VERIFY`, and `EXTERNAL_SERVICE_UNAVAILABLE`; if the call is rejected outright, suggest the Airwallex Dashboard.

---

## Error handling

| Situation | Action |
| --- | --- |
| Required field missing or ambiguous | STOP, list the gaps, ask the user |
| Document unreadable | Ask for the content another way |
| Extraction ambiguous | Mark `[?]`, ask the user, do not guess |
| Bank country unclear | Ask the user — a wrong country cascades to wrong fields |
| Required bank field missing | Show which field is missing for which country schema |
| Schema fetch fails | Try the alternate transfer method (LOCAL → SWIFT) |
| `verify` returns `INVALID`, or create is rejected | Show the exact API error, ask the user to correct |
| `066` / `086` account errors | Ask the user to verify account format/length; never pad or truncate |
| Duplicate detected | Show details, let the user choose |
| Partial completion | Report what succeeded (with IDs) and what failed |
| Auth expired | The connector refreshes tokens automatically; if a tool keeps returning an auth error, the grant may have been revoked — ask the user to re-authorize the Airwallex connection |

---

## Workflow summary

```
Phase 1: Extract
  get document(s) → extract bank details → clarify intent
    → confirm live data + access → fetch country schema
      → build table → schema cross-check → user confirms

Phase 2: Check & Create
  completeness check → match existing → verify bank details (pre-flight)
    → confirm before writes → create → summary & next steps

Phase 3: Verify bank account (standalone / post-create)
  check eligibility → submit verification → show status
```

---

## Attribution

Adapted from Airwallex's official AgentOS `beneficiary-creation` skill, licensed under the Apache License 2.0 (see LICENSE.txt). Modified for the ChatChat Airwallex connector: CLI-specific instructions and external URLs removed, supporting reference files inlined, workflow steps aligned to the operations this connector actually exposes, and unsupported operations redirected to the Airwallex Dashboard.
