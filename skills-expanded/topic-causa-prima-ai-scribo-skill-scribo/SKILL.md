---
name: scribo
description: Generate EN 16931-compliant e-invoices (XRechnung, ZUGFeRD) or a clean US plain PDF via the public Scribo HTTP API. Factur-X, Peppol BIS UBL, and Spanish Facturae are Phase 2 — coming soon. No signup; the sender's email is the login.
allowed-tools:
  - Read
  - Bash
---

# Scribo — Compliant E-Invoicing

Use Scribo when a user asks to generate, draft, or "create" an invoice. Scribo emits structured machine-readable invoices that satisfy EU mandates (German B2B / Federal B2G) and can also produce a plain US PDF when no XML is needed. French Factur-X, Spanish Facturae, and Belgian/cross-border Peppol BIS UBL are **Phase 2 — coming soon**.

This skill talks to the public Scribo HTTP API at `https://scribo.causaprima.ai` via small `curl` + `jq` helper scripts. No MCP server or npm install required. Override the base URL with `SCRIBO_BASE_URL` for dev/staging.

## When to use

- "Make me an invoice for …"
- "Generate a ZUGFeRD invoice"
- "I need to bill X for Y hours of work"
- "Create an XRechnung for this German B2G client"
- "Draft a Factur-X for my French client" *(Phase 2 — coming soon)*

## When NOT to use

- Reading existing invoices / OCR / extracting data from a PDF — different tool.
- Tax advice. Scribo does **not** infer the right tax category code; it asks the user to pick one (S/Z/E/AE/K/G/O per EN 16931). See `references/tax-codes.md` only if the user is unsure.
- Submitting B2G invoices to portals (ZRE / OZG-RE / Peppol). Scribo emails the invoice to `recipient.contact_email` at issue time and returns a download URL, but portal/Peppol submission is manual — the user uploads the XML themselves.
- Phase 1 supports DE and US senders only. Other sender countries return `unsupported_jurisdiction` — don't attempt to draft.

## Phase 1 limits — surface up front

- **Sender jurisdictions**: DE and US only. Other sender countries return `unsupported_jurisdiction`.
- **DE B2G (XRechnung) is generate-only.** Scribo emits the legally binding XML and a human-readable PDF preview — it does **not** submit to ZRE / OZG-RE / Peppol yet. **Tell the user this before collecting the Leitweg-ID**, so they know they'll deliver the XML themselves (the response includes the upload-portal hint per Leitweg-ID prefix). Direct submission via Peppol is planned for a future release.
- **Credit notes / corrections** aren't supported — total ≤ 0 is rejected. Use a positive invoice with a line `discount` to apply a rebate.

## Workflow

1. **Detect the invoice type early.** If the user mentions a German public-sector recipient, a Leitweg-ID, or specifically asks for XRechnung, immediately tell them: *"Scribo generates the XRechnung XML (plus a PDF preview) but doesn't submit it for you yet — you'll upload the XML manually to xrechnung.bund.de (federal) or your Land's OZG-RE portal, keyed by the Leitweg-ID. Direct Peppol submission is on the roadmap."* Confirm they're OK with this before proceeding.
2. **Collect the required fields** from the user in a brief conversational pass:
   - **Sender business name** — legal entity name.
   - **Sender address** — street (`address_line1`), `postcode`, `city`, `country_code` (ISO 3166 alpha-2 — reserved codes like `XX` / `ZZ` are rejected).
   - **Sender tax / VAT ID + contact email** — tax ID with country prefix (e.g. `DE123456788`). The email doubles as the user's login for return visits. **German Kleinunternehmer § 19 UStG** senders don't have a VAT ID — pass the **Steuernummer** as `sender.tax_registration_id` (e.g. `9999/999/9999`) instead so the EN 16931 BR-CO-26 constraint is still satisfied. Both fields can also be supplied side-by-side when both are issued (BT-31 + BT-32).
   - **Recipient name** — legal entity name.
   - **Recipient address** — street, postcode, city, country code. Add `leitweg_id` if it's a German federal B2G recipient — that field alone **auto-selects XRechnung UBL** (broadest Peppol AccessPoint compatibility; force `xrechnung_cii` via `format_override` only if a portal specifically requires the CII syntax). **Reminder**: Scribo generates the XML and a PDF preview but does not submit — the response includes a `submission` hint pointing at the right manual-upload portal.
   - **Recipient email** — `recipient.contact_email`. **Required** — Scribo refuses to draft without it. This is the accounts-payable / billing email. Recipient `tax_id` is optional in general but required for intra-EU reverse charge (`AE`).
   - **Line items + currency** — per line: description, quantity, unit price, tax rate (percent — must be `[0, 100]`; quantity capped at 999,999.999), tax category code. Optional line-level `discount` (`{ type: 'percent' | 'amount', value, reason }`; `reason` is **required** by EN 16931 BR-41). Currency is ISO 4217.
   - **`tax_exemption_code`** (per line) — **REQUIRED when `tax_category_code === "E"`** per EN 16931 BR-E-10. Pass a VATEX code matching the legal basis (`VATEX-EU-79-C` for Kleinunternehmer § 19 UStG, `VATEX-EU-132` for Art. 132 health/education, etc.). **AE / K / G / O auto-emit their well-known VATEX codes server-side** (VATEX-EU-AE / -IC / -G / -O) — only include this for category E unless you want to override a default.
   - **`payment_means`** (top-level) — **REQUIRED for XRechnung** (any invoice with `recipient.leitweg_id`, or an explicit `format_override` of `xrechnung_ubl` / `xrechnung_cii`). Shape: `{ "type": "credit_transfer", "iban": "DE89…", "bic"?: "…", "account_name"?: "…" }`. XRechnung BR-DE-1 enforces this. Ask the user "on which account?" if you don't have the IBAN yet — never invent one.

   *Optional extras:* `jurisdiction` override, `format_override`, `notes` (≤ 1000 chars), `idempotency_key` (if not supplied, the script auto-mints one from a SHA-256 of the payload so accidental retries don't double-bill), `tax_exemption_reason` (per-line free-form BT-120 note to the buyer).
3. **If the user is unsure of the tax category code**, read `references/tax-codes.md` once and offer the right pick. Never guess.
4. **Build the JSON payload** and invoke `scripts/create_invoice.sh` (passes payload on stdin).
5. **Verify email ownership the first time** — see the **Verification** section below. The first `create_invoice.sh` for a sender email prints `status: "verification_required"` with a `challenge_id` (exit 10); Scribo emails a 6-digit code to `sender.contact_email`. Ask the user for the code, redeem it for a `verification_token` with `scripts/redeem_verification.sh`, then re-run the create with the token. One token is good for ~30 minutes of invoices for the same sender.
6. **Hand the user the result** — `download_url` (durable; re-fetchable any time), the resolved `format`, and **what was emailed**: when `recipient_email_sent` is `true`, tell the user the invoice was emailed straight to `recipient.contact_email`; when it is `false`, warn them the recipient email could not be sent and they should deliver the download link or PDF themselves; when the field is absent (idempotent replay — no email is re-sent), say nothing about it. Also mention that a magic link was emailed to the sender so they can come back later. For XRechnung output the legally binding file is the **UBL XML** (or CII XML if you forced `xrechnung_cii`); for ZUGFeRD it's a **PDF/A-3** with `factur-x.xml` embedded; for US it's a plain PDF. For XRechnung the response also carries a `preview_url` to the PDF visualisation (same content, human-readable) and a `submission` object describing how the user should deliver the XML (manual portal upload today). Surface both URLs and the submission hint to the user.
7. **On a 4xx/5xx response**, surface the `error.code` and `error.message` from the response envelope. Read `references/troubleshooting.md` if the error is one of: `email_verification_required`, `verification_email_mismatch`, `verification_invalid`, `rate_limited`, `idempotency_key_mismatch`, `validator_failed`. A bare `HTTP 403` with **no** JSON `error` envelope is the exception — it was blocked upstream (a sandbox network-egress proxy or a WAF), not by Scribo; see `references/troubleshooting.md`. Common gotchas: missing `tax_exemption_code` for an E line, missing `payment_means` on an XRechnung path, reserved `country_code`, `tax_rate > 100`.

## Verification (required before the first invoice)

Scribo proves the caller owns `sender.contact_email` **before** it generates anything (Scribo-03). You orchestrate it: call create, get told to verify, ask the user for the code, redeem, retry.

> **Email language.** The verification email (and the confirmation page its link opens) is English by default. To send it in the language you're speaking with the user, set `SCRIBO_LOCALE` to the BCP-47 tag before calling `create_invoice.sh` / `request_verification.sh` — e.g. `export SCRIBO_LOCALE=de-DE`. This also localizes the later "invoice ready" notification email. Unsupported values fall back to English, so it's safe to set whenever the language is clear. UI-language only — it does **not** affect the invoice content, currency, or jurisdiction.

**Canonical sequence:**

1. Build the payload and call `scripts/create_invoice.sh`. With no token it does **not** create the invoice; it requests a challenge (Scribo emails a 6-digit code to the sender) and prints:
   ```json
   {
     "status": "verification_required",
     "challenge_id": "9b1d…",
     "email_hint": "a***@e***.com",
     "expires_at": "…",
     "next_step": "Ask the user for the 6-digit code emailed to a***@e***.com, then run: redeem_verification.sh 9b1d… <code> …"
   }
   ```
   The script exits with code `10`.
2. Tell the user: *"I've sent a verification email to a***@e***.com. Please paste the 6-digit code from your inbox."* The code is 6 characters from `{2,3,4,5,6,7,8,9}` (no 0/1, no letters).
3. When the user gives you the code, run `scripts/redeem_verification.sh <challenge_id> <code>`. It prints `{ "verification_token": "…", "expires_at": "…" }`.
4. Re-run the create with the token (same payload). Prefer the environment variable so the token doesn't land in the process list or shell history:
   ```sh
   SCRIBO_VERIFICATION_TOKEN=<verification_token> \
     cat payload.json | scripts/create_invoice.sh
   ```
   The token is reusable for ~30 minutes, so one `export SCRIBO_VERIFICATION_TOKEN=…` covers several invoices for the same sender. The `--verification-token <token>` flag does the same thing if you prefer it.

If the code is wrong, `redeem_verification.sh` exits `11` with `verification_invalid`. Ask the user to re-check and try again. After 5 wrong attempts the challenge is revoked — re-run `create_invoice.sh` (no token) to mint a fresh one.

> **Unattended / batch use:** every tokenless `create_invoice.sh` call sends a verification email and exits `10`. For scripted runs, verify once and `export SCRIBO_VERIFICATION_TOKEN=…` so subsequent calls go straight through. (The server caps sends to 1 per 30 s and 5 per hour per email, so an accidental retry loop can't flood an inbox.)

### Worked example

User: *"Issue an invoice to Acme GmbH for 1 day of consulting at €1000, my email is alice@example.com."*

1. `cat payload.json | scripts/create_invoice.sh` → `{ "status": "verification_required", "challenge_id": "9b1d…", "email_hint": "a***@e***.com" }` (exit 10).
2. Reply: *"I've sent a verification email to a***@e***.com. Please paste the 6-digit code."*
3. User: *"234567"*
4. `scripts/redeem_verification.sh 9b1d… 234567` → `{ "verification_token": "vtok…" }`.
5. `SCRIBO_VERIFICATION_TOKEN=vtok… ; cat payload.json | scripts/create_invoice.sh` → `{ invoice_id, download_url, format, … }`.
6. Reply to the user with the download URL.

## Tools

### `scripts/create_invoice.sh` — POST `/api/v1/invoices`

Reads a JSON payload on stdin (or via `--from FILE`).

**Example — DE B2B ZUGFeRD COMFORT** (the simplest happy path):

```sh
cat <<'JSON' | skills/scribo/scripts/create_invoice.sh
{
  "sender": {
    "legal_name": "Causa Prima Germany GmbH",
    "country_code": "DE",
    "address_line1": "Example Allee 1",
    "postcode": "10115",
    "city": "Berlin",
    "tax_id": "DE123456788",
    "contact_email": "billing@causaprima.ai"
  },
  "recipient": {
    "legal_name": "Acme GmbH",
    "country_code": "DE",
    "address_line1": "Hauptstrasse 1",
    "postcode": "10117",
    "city": "Berlin",
    "tax_id": "DE136695976",
    "contact_email": "ap@acme.example"
  },
  "line_items": [
    {
      "description": "Consulting, 3 days",
      "quantity": "3",
      "unit_code": "DAY",
      "unit_price": "1200.00",
      "tax_rate": "19",
      "tax_category_code": "S"
    }
  ],
  "currency": "EUR"
}
JSON
```

**Example — DE B2G XRechnung UBL** (Leitweg-ID + payment_means + supplier contact phone for BR-DE-5/6):

```jsonc
{
  "sender": {
    "legal_name": "Acme GmbH", "country_code": "DE",
    "address_line1": "Musterstr. 1", "postcode": "10115", "city": "Berlin",
    "tax_id": "DE123456788", "contact_email": "billing@acme.de",
    "contact_name": "Erika Beispiel", "contact_phone": "+49 30 1234567"
  },
  "recipient": {
    "legal_name": "Bundesamt für Beispiele", "country_code": "DE",
    "address_line1": "Wilhelmstr. 1", "postcode": "10117", "city": "Berlin",
    "contact_email": "rechnung@bund.de",
    "leitweg_id": "991-12345-67"
  },
  "line_items": [
    { "description": "Consulting", "quantity": "3", "unit_code": "DAY",
      "unit_price": "1200.00", "tax_rate": "19", "tax_category_code": "S" }
  ],
  "currency": "EUR",
  "payment_means": {
    "type": "credit_transfer",
    "iban": "DE89370400440532013000",
    "account_name": "Acme GmbH"
  }
}
```

**Example — Kleinunternehmer § 19 UStG** (category E + VATEX-EU-79-C; pass Steuernummer as `tax_registration_id` since there's no VAT ID — BR-CO-26 needs one or the other):

```jsonc
{
  "sender": {
    "legal_name": "Friedrich Beratung", "country_code": "DE",
    "address_line1": "Musterstr. 1", "postcode": "10115", "city": "Berlin",
    "tax_registration_id": "26/750/12345",
    "contact_email": "f@example.de"
  },
  "recipient": { /* ... */ },
  "line_items": [
    {
      "description": "Beratung", "quantity": "5", "unit_code": "HUR",
      "unit_price": "80.00", "tax_rate": "0",
      "tax_category_code": "E",
      "tax_exemption_code": "VATEX-EU-79-C"
    }
  ],
  "currency": "EUR"
}
```

Returns `{ invoice_id, document_id, format, download_url, download_url_expires_at, validator_summary, magic_link_sent, recipient_email_sent }`. The download URL is durable — re-fetchable any time from any device. The magic link arrives at the sender's email and lets them sign back in. `recipient_email_sent` reports the recipient-facing email: `true` = the invoice was emailed to `recipient.contact_email`, `false` = the best-effort send failed (tell the user to deliver the PDF themselves), absent = idempotent replay of an older response (no email re-sent — claim nothing).

Format is picked from the priority chain (`format_override` → Leitweg-ID → `jurisdiction` → sender country → sender tax-ID prefix → recipient country → recipient tax-ID prefix). See `references/jurisdictions.md` for the full table.

Pass the email `verification_token` via the `SCRIBO_VERIFICATION_TOKEN` env var (preferred — keeps it out of the process list and shell history) or the `--verification-token <token>` flag; it is sent as the `X-Email-Verification-Token` header. **Without a token the script requests a verification challenge and prints `status: "verification_required"` (exit 10) instead of creating the invoice** — see the **Verification** section above.

### `scripts/request_verification.sh EMAIL` — POST `/api/v1/scribo/email-verifications`

Requests an email-ownership challenge; Scribo emails a magic link **and** a 6-digit code to `EMAIL`. Returns `{ challenge_id, expires_at, next_request_allowed_at }`. You normally don't call this directly — `create_invoice.sh` requests the challenge for you when no token is present. Set `SCRIBO_LOCALE` (e.g. `de-DE`) to control the email + confirmation-page language — see the **Verification** section.

### `scripts/redeem_verification.sh CHALLENGE_ID CODE` — POST `/api/v1/scribo/email-verifications/:id/redeem`

Exchanges the 6-digit code the user copied from the email for a `verification_token` (reusable ~30 min). All failures (wrong/expired/revoked code) return a uniform `verification_invalid` (exit 11).

### `scripts/get_invoice.sh INVOICE_ID` — GET `/api/v1/invoices/:id`

Fetch metadata + a fresh signed download URL for a previously generated invoice. Tenant-scoped (the caller's session must own it).

### `scripts/download_invoice.sh INVOICE_ID [-o FILE]` — GET `/api/v1/invoices/:id/download`

Streams the PDF bytes to `-o FILE` (default `invoice-<id>.pdf`).

### `scripts/list_jurisdictions.sh` — GET `/api/v1/jurisdictions`

Returns `[{ jurisdiction, formats, default_format }]`. Useful to confirm a country is supported before collecting recipient data.

## Tax category codes (EN 16931)

User picks; Scribo never infers. One-liners only — read `references/tax-codes.md` for when each applies and which schematron rules it triggers.

- `S` — Standard rated
- `Z` — Zero rated
- `E` — Exempt (statutory) — **requires `tax_exemption_code`** (VATEX-EU-79-C for § 19 UStG Kleinunternehmer, VATEX-EU-132 for Art. 132 health/education, etc.)
- `AE` — Reverse charge (intra-EU B2B services AND § 13b UStG domestic — construction, scrap, mobile-phone wholesale, etc.). Auto-emits `VATEX-EU-AE`.
- `K` — Intra-community supply of goods. Auto-emits `VATEX-EU-IC`.
- `G` — Free export. Auto-emits `VATEX-EU-G`.
- `O` — Services outside the scope of VAT. Auto-emits `VATEX-EU-O`. (All-O invoices are rejected for XRechnung — BR-DE-14 unrepresentable; use AE or G instead.)

## Format defaults (quick reference)

| Sender→Recipient | Default format |
|---|---|
| DE → DE B2B | ZUGFeRD COMFORT |
| DE → DE B2G (Leitweg-ID present) | **XRechnung UBL** (auto-selected; force `xrechnung_cii` via `format_override` if the recipient portal specifically requires CII) |
| FR → \* | Factur-X *(Phase 2 — coming soon)* |
| ES → \* | Facturae *(Phase 2 — coming soon)* |
| BE → \* | Peppol BIS UBL *(Phase 2 — coming soon)* |
| US → \* | Plain PDF |

Full table and priority chain in `references/jurisdictions.md`.

## XRechnung output is XML, not PDF

For any XRechnung-resolved invoice (Leitweg-ID present or `format_override=xrechnung_*`), `scripts/download_invoice.sh` streams the **legally binding UBL/CII XML**, not the PDF preview the workflow also generates. KoSIT, Peppol AccessPoints, and the German federal procurement portals all consume the XML. For ZUGFeRD output you get a PDF/A-3 with `factur-x.xml` embedded inside (the PDF *is* the legal artifact in that case).

## Limits

- One generated invoice per call.
- ≤ 500 line items.
- Plain PDF output only for US, IT, MX, BR, and other jurisdictions where the regulatory submission path isn't yet supported (those receive a banner: "this country requires submission via certified provider").
- Negative line amounts → use `discount` instead.
- Total ≤ 0 → rejected (credit notes are a separate document type, deferred).
- Email verification is required before the first invoice for any sender email (see **Verification**). The `verification_token` is reusable for ~30 min; after that, the next create re-runs the challenge.
- Rate limits: 50 invoices/24h per tenant, 200/hour per IP. Verification requests are separately capped (per email: 1 send / 30 s and 5 / hour; per IP: 10 / min). This headless skill is out of scope for CAPTCHA — Turnstile gates the web chat only, and the `/api/v1/*` endpoints these scripts call are never CAPTCHA-gated. A bare `HTTP 403` with **no** JSON `error` envelope is not Turnstile and not a verification problem — it means the request was blocked upstream (a sandbox network-egress proxy, or a WAF in front of the API), so re-verifying or visiting the web UI won't help. See `references/troubleshooting.md`.

## Setup

End-user install instructions live in `README.md`. Three methods: `/plugin install` (Claude Code), a `.zip` upload via Settings → Customize → Skills (Claude.ai, Claude Desktop, Cowork), and `git clone` + copy of the inner `skills/scribo` directory (Codex CLI, manual Claude Code, Cowork repo-baked).
