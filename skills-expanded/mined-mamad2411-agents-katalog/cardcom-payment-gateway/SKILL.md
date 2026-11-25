---
name: cardcom-payment-gateway
description: Not tax or accounting advice. Integrate Cardcom payment processing and Israeli invoice generation into applications, covering Low Profile payments, tokenization, recurring billing, and automatic tax invoice/receipt creation per Israeli law. Use when user asks to accept payments via Cardcom, generate Israeli invoices with payments, set up "slikat ashrai" with hashbonit, handle recurring billing (hora'ot keva), or mentions "Cardcom", "CardCom API", "Low Profile", Israeli payment with invoicing, or needs combined payment plus document generation. Targets the REST API V11. Do NOT use for Tranzila integration (use tranzila-payment-gateway), general accounting, or non-payment queries.
license: MIT
---

# Cardcom Payment Gateway

## Legal notice

This is a free technical integration guide operated by an AI model. It explains how to call the Cardcom API and how the Israeli invoicing rules bear on it. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser, accountant, or lawyer. Nothing here is a tax opinion or professional advice, and an AI model may err, omit data, or present a wrong conclusion.

The documents this integration produces are tax documents. Responsibility for issuing them correctly, for reporting, and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. Whether a given invoice requires an allocation number, and whether input VAT may be deducted, are determinations for your accountant on your actual facts. Have a tax adviser or accountant review the invoicing configuration before you go live, and handle cardholder data in accordance with PCI DSS. All use of this skill's output is the user's sole responsibility.

## Overview

Cardcom is an Israeli payment processor with a unique strength: integrated invoice and receipt generation compliant with Israeli tax law. While other Israeli gateways handle only the payment, Cardcom can automatically generate tax invoices (hashbonit mas) and receipts (kabala) as part of the payment flow, something Israeli businesses are legally required to issue.

This skill covers Cardcom's REST API V11 for payments, tokenization, recurring billing and documents. Endpoint and field names come from the official V11 OpenAPI specification.

**Official docs:** `https://secure.cardcom.solutions/Api/v11/Docs` (interactive API reference with the full OpenAPI schema). V11 is the current API as of 2026; there is no public V12.

**Support center:** `https://support.cardcom.solutions`

**Cardcom in the Israeli landscape:** competes with Tranzila and other Israeli gateways. Cardcom publishes a starting rate of about 1.2% that falls with volume; that is a floor, not a quote, so send the user to Cardcom for an actual figure. The distinguishing feature remains the built-in tax document generation. For Tranzila integration use the `tranzila-payment-gateway` skill instead.

## Instructions

### Step 1: Choose Integration Pattern

| Pattern | Card Data Handling | Best For |
|---------|-------------------|----------|
| **Low Profile (iframe/redirect)** | Cardcom handles card entry | Most integrations, minimal PCI scope (SAQ-A) |
| **Transaction (server-to-server)** | Raw card data or token | Charging stored tokens, recurring billing |
| **CreateDocument (server-to-server)** | No card data | Standalone invoice/receipt generation |

Most Israeli merchants use **Low Profile** for the initial payment plus token creation, then the **Transaction** endpoint with the stored token for recurring charges. All payment flows can auto-generate invoices by attaching a `Document` object.

### Step 2: Set Up Authentication

Cardcom API V11 credentials:
- `TerminalNumber` (integer) -- your terminal ID (`1000` is Cardcom's test terminal, see below)
- `ApiName` (string) -- API username
- `ApiPassword` (string) -- API password. The rule of thumb: **operations that read or act on company-wide data require it; operations that charge a single card do not.** It is required on `Transactions/ListTransactions`, `RefundByTransactionId`, `SpecialTransactions`, `Documents/CreateDocument`, `CancelDoc` and the `Financial/*` reports, among others. It is NOT a top-level field on `LowProfile/Create` or `Transactions/Transaction`, so do not send it there. The set of schemas that require it changes between spec revisions (see Gotchas), so check the `required` array of the endpoint's request schema in the [V11 OpenAPI spec](https://secure.cardcom.solutions/swagger/v11/swagger.json) rather than trusting a list.

**Test environment (Cardcom's own developer test page):**
- Terminal `1000`. The API username and password for it are NOT published: request them from Cardcom support.
- Israeli test card `4580280000000008` (supports installments and credit deals); tourist test card `4580000000000000` (no installments or credit). Any future expiry, CVV `123`, any ID number.
- On the test cards, amounts under 5,000 NIS simulate success and amounts above 5,000 NIS simulate a failure, so a large test charge failing is expected, not a bug.
- Test-terminal transactions run through the full clearing flow without actually charging the card. A REAL card used on the test terminal is not charged but its credit line is held (מסגרת) for three days for the amount, so never test with a customer's card.

**Treat `ApiName`, `ApiPassword` and every stored token as secrets.** `Transactions/Transaction` needs only `TerminalNumber`, `ApiName` and `Amount`, so `ApiName` plus a token can charge a saved card. Keep them in server-only environment variables (in Next.js never `NEXT_PUBLIC_*`), call Cardcom only from server code, and never log a full response (it carries the token and the cardholder's ID number).

### Step 3: Implement the Payment Flow

#### Low Profile Integration (Recommended)

This is a two-step process.

**Step 3a: Create the payment page**

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/Create
Content-Type: application/json

{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "Operation": "ChargeAndCreateToken",
  "ReturnValue": "unique-order-id",
  "Amount": 100.00,
  "SuccessRedirectUrl": "https://example.com/success",
  "FailedRedirectUrl": "https://example.com/failed",
  "WebHookUrl": "https://example.com/webhook",
  "ISOCoinId": 1,
  "Language": "he",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoiceAndReceipt",
    "Name": "Customer Name",
    "Email": "customer@example.com",
    "Products": [
      { "Description": "Product name", "UnitCost": 100.00, "Quantity": 1 }
    ]
  }
}
```

The response is a `CreateLowProfileResponse`: check `ResponseCode == 0` (success), read `Description` on failure. On success it returns `LowProfileId` (save it) and `Url` (redirect the customer there or embed as an iframe). `UrlToBit` and `UrlToPayPal` are also returned when those methods are enabled on your terminal.

The `Operation` field controls behaviour: `ChargeOnly` (default), `ChargeAndCreateToken`, `CreateTokenOnly`, `SuspendedDeal`, `Do3DSAndSubmit`.

**The `Document` lines must add up exactly to `Amount`** (Cardcom: "יש לדאוג שסה\"כ שורות החשבונית שווה לסכום החיוב"), so line prices are entered as the amounts the customer actually pays, VAT included. A mismatch can leave the card charged with no invoice, because Cardcom gives the charge priority.

**Step 3b: Get the results**

After payment completes, Cardcom calls your `WebHookUrl`, or you query:

```
POST https://secure.cardcom.solutions/api/v11/LowProfile/GetLpResult
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "LowProfileId": "id-from-step-3a"
}
```

The response is a `LowProfileResult`, and its top-level `ResponseCode` is NOT the payment result. The spec describes it as "if equel zero then success , else , a develper error" -- it tells you the request was well formed, nothing more. The card result lives in the nested `TranzactionInfo`, which the spec says "Will no be null at operations: ChargeOnly, ChargeAndCreateToken", i.e. it is `null` when the cardholder abandoned the page.

**Before fulfilling anything, all five of these must hold:**

1. HTTP status is 200. A 404 returns `{"Message": "No HTTP resource was found..."}` with no `ResponseCode` at all, so branching on `ResponseCode == 0` alone reads a routing error as `None`.
2. Top-level `ResponseCode == 0`.
3. `TranzactionInfo` is non-null.
4. `TranzactionInfo.ResponseCode == 0` (its own description: "if equal zero then success , 700 and 701 success for J2 and J5 transaction").
5. `TranzactionInfo.Amount` equals the amount you expected, and `ReturnValue` matches your own order id.

Also check `TranzactionInfo.IsRefund` / `DealType`: a refund is a successful transaction and will pass a naive `ResponseCode == 0` test. If you asked for a document, `DocumentInfo` must be non-null too -- a charge that succeeded with `DocumentInfo: null` means you took the money and never issued the tax invoice (Cardcom gives the charge priority when the invoice fails). `scripts/validate_cardcom_response.py --expect charge --amount <n> --return-value <order-id> --with-document` applies all of this and fails closed.

Never fulfil on the browser landing at `SuccessRedirectUrl`, which the customer controls, or on the raw webhook body. `TokenInfo` carries the stored `Token` plus `CardMonth`/`CardYear`; `SuspendedInfo` covers suspended deals.

**The webhook handler (`WebHookUrl` is REQUIRED on `LowProfile/Create`):** the V11 spec defines no signature, shared secret or HMAC for it, and does not document its payload or retry schedule. Treat every hit as an untrusted, possibly repeated "something happened" signal:

1. Look up the `LowProfileId` it names among the ids YOU saved from `LowProfile/Create`. An unknown id is ignored, never fetched.
2. Call `GetLpResult` with your own credentials and apply the five checks above. Never read the amount or status from the webhook body.
3. Make fulfilment idempotent (mark the order fulfilled in the same transaction that checks it), because the same event can arrive more than once. Cardcom's documentation for the older `IndicatorUrl` interface says it re-sends up to 7 times when your server does not answer HTTP 200; assume V11 can repeat too.
4. Write the hit to durable storage, THEN return HTTP 200 (a 200 ends Cardcom's re-sends). Also sweep pending orders with `GetLpResult` instead of waiting for a webhook that may never come; a page code expires 24 hours after creation. More in `references/production-checklist.md`.

#### Alternative Payment Methods

`UrlToBit` and `UrlToPayPal` on the `LowProfile/Create` response are separate URLs you can show alongside the card form; Google Pay and Apple Pay appear as wallet buttons inside the hosted page once enabled on the terminal. **Apple Pay does not support saving a token or standing orders** (Cardcom: the button may show on a standing-order page but the payment cannot complete), so a `ChargeAndCreateToken` subscription page cannot be paid with it, and inside an iframe it needs your domain registered with Apple through Cardcom support. Details: `references/api-endpoints.md`.

### Step 4: Generate Israeli Tax Documents

The document type is set with the **`DocumentTypeToCreate`** field, a STRING enum (not an integer). Common values:

| Value | Hebrew | English | When to Use |
|-------|--------|---------|-------------|
| `Auto` | --- | Auto | Default; uses your admin-panel configuration |
| `TaxInvoiceAndReceipt` | hashbonit mas / kabala | Tax Invoice + Receipt | B2C with payment (most common) |
| `TaxInvoice` | hashbonit mas | Tax Invoice | B2B, when receipt is issued separately |
| `Receipt` | kabala | Receipt | Payment confirmation only |
| `TaxInvoiceAndReceiptRefund` | --- | Tax Invoice + Receipt Refund | Reversing a `TaxInvoiceAndReceipt` |
| `TaxInvoiceRefund` | --- | Tax Invoice Refund | Reversing a `TaxInvoice` |

The full `DocumentToCreate` enum has 25 values, listed in `references/document-types.md`. There is no `QuoteRefund` and no `OrderRefund`, so do not invent a refund variant by appending `Refund`.

**Include a document in a payment flow:**
Add the `Document` object to your Low Profile `Create` or `Transaction` request. Cardcom generates the document automatically when the payment succeeds.

**Standalone document creation:**

```
POST https://secure.cardcom.solutions/api/v11/Documents/CreateDocument
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoice",
    "Name": "Customer Ltd",
    "TaxId": "123456789",
    "Email": "customer@example.com",
    "IsSendByEmail": true,
    "Languge": "he",
    "ISOCoinID": 1,
    "Products": [
      { "Description": "Web development services", "UnitCost": 5000.00, "Quantity": 1 }
    ]
  }
}
```

The response is a `DocumentInfo`: check `ResponseCode == 0`, then read `DocumentType`, `DocumentNumber`, `AccountId`, and `DocumentUrl` (link to the PDF).

Field spellings differ between the three document objects (`Languge` vs `Language`, and `ISOCoinID` exists ONLY on this standalone `Document`, never inside a Low Profile or Transaction document); see the Gotchas and `references/document-types.md` for the full field list. `TaxId` replaces the older `VAT_Number` and `IsSendByEmail` replaces `SendByEmail`.

### Step 4.5: Allocation Numbers (Mispar Haktzaa) on Tax Invoices

**Do not look for an allocation-number field in the document API. There isn't one, and that is
not an omission.** Cardcom's document system is connected to the Tax Authority and requests the
number itself when it issues a tax invoice over the threshold. Neither the `CreateDocument`
request nor the `DocumentInfo` response carries one; the number is printed on the document
under the heading "מספר הקצאה:", so read it from the PDF at `DocumentUrl`.

**It only works after a registration that EXPIRES.** Without a number, your customer cannot
deduct input VAT on an invoice whose pre-VAT amount exceeds the threshold. Cardcom's own guide:

1. The business owner identifies (הזדהות) in the Tax Authority personal area, registering if needed.
2. A company or an איחוד עוסקים completes רישום פרטי תאגיד there.
3. In the Cardcom admin: הגדרות, then מסמכים, then שירות חשבוניות ישראל. Generate a
   verification code (קוד אימות); you are sent to the Tax Authority to identify. Only the
   owner, or someone the owner authorised for digital actions, can do this.
4. Press "בדיקת קבלת מספר הקצאה" to confirm numbers are actually issued.

The code is valid for **three months**. After it lapses, invoices are issued WITHOUT a number;
re-register, then re-print the document to attach one. A scheduled job that issues large
invoices must therefore check the service is active, not assume it. Error `Not Acceptable (406)`
means the identified user has no Tax Authority authority for that business: the owner grants it
under "הרשאות לפעולות דיגיטליות", selecting both subjects "חשבוניות ישראל – אימות מספר הקצאה
בחשבונית ספק" and "חשבוניות ישראל – בקשת מספר הקצאה עבור חשבונית ללקוח".

Cardcom also documents that no number is issued when: the customer's ID / company number
(`TaxId`) is missing; supplier and customer are the same company number; or a tax
invoice-receipt carries no VAT.

**Threshold schedule (pre-VAT; the statute says `עולה על`, EXCEEDS):**

| Effective from | Threshold |
|----------------|-----------|
| May 2024 | 25,000 NIS |
| January 2025 | 20,000 NIS |
| 1 January 2026 | 10,000 NIS |
| 1 June 2026 | **5,000 NIS (in force now)** |

The threshold is keyed to each DOCUMENT's own date; see `references/document-types.md` for
older documents, osek patur and zero-rated invoices. Even when everything is set up, a number
can be withheld: under s.47(a2)(3) the Director may decide not to allocate one on reasonable
suspicion the invoice is improper (a החלטה מקדמית, with a hearing within two business days),
and s.47(a2)(4) lets the dealer request a number after issuing the invoice. Confirm the
number is on the document before relying on it.

### Step 4.6: Idempotency, and Authorize vs Capture

**Send `ExternalUniqTranId` on every `Transactions/Transaction` call.** It is your own
unique id for the charge, and the spec is explicit: "send your uniq trnasaction id to
prevent duplication of transaction. if the same ExternalUniqTranId will be send you will
receive and error code 608". Without it, a cron whose HTTP call times out AFTER Cardcom
charged the card retries and charges the customer twice.

**608 means "this id already got a valid card answer", not "payment failed".** Cardcom's
token-charge guidance says the id is consumed once a call gets a charge (0), J2 (701) or J5
(700) answer, so 608 does not prove money was taken. Never retry it under a new id: after any
608, timeout or ambiguous result, call `POST /api/v11/Transactions/GetTransactionByExternalUniqTran`
and branch on THAT record's `ResponseCode` (0 = charged; 700/701 = only checked or held). A
declined charge does not consume the id, so it can be retried with the same one; wait for a
response (up to 7 seconds) before resending. Give a capture its own id, never the hold's.

**J2 and J5 are not the same thing, and 700/701 do not mean the customer is untouched.**
`JValidateType` applies to the `CreateTokenOnly` and `SuspendedDeal` operations and selects
J2 (a simple card validation, nothing reserved) or J5 (an authorization, which HOLDS the
amount on the cardholder's limit). On `LowProfile/Create` its default is `5`, so a
`CreateTokenOnly` page places a J5 hold for `Amount` unless you send
`AdvancedDefinition.JValidateType: 2`. A J5 is captured by charging the token with `Advanced.ApprovalNumber` set to
the `TokenInfo.TokenApprovalNumber` you received (the spec: "capture an J5 (authoriz)
request"). An authorization that is never captured leaves the customer's money held until it
expires, so if you use J5 you must have a capture step and a release path (Cardcom documents
`MTI=420` with the hold's deal number; the test terminal cannot run J5 at all, see
`references/production-checklist.md`).

### Step 5: Implement Token-Based Recurring Payments

For subscriptions and recurring billing (hora'ot keva), Cardcom supports two flavours:

- **Card-based recurring**, charging a stored credit-card `Token` on a schedule. Covered in this step.
- **MASAV bank standing orders**, debiting the customer's Israeli bank account directly. Managed through the `RecuringPayments` endpoints (`RecuringPayments/GetRecurringPayment`, `GetRecurringPaymentHistory`, `IsBankNumberValid`). Use this when the customer prefers a bank debit over a card charge or when the card is unavailable. The Cardcom dashboard provisions the underlying instruction.

For card-based recurring, first confirm the merchant has Cardcom's tokens module and a terminal that does NOT require CVV (on a CVV-required terminal each token charge needs a single-use J5 approval number), and without the module Cardcom keeps a token for only 6 months, for refunds (`references/production-checklist.md`).

1. **Create a token during the first payment.** Use Low Profile with `Operation: "ChargeAndCreateToken"` (or `"CreateTokenOnly"`). The `LowProfileResult` returns `TokenInfo` with `Token`, `CardMonth`, `CardYear`, and `TokenExDate` (the date the token is purged from Cardcom).

2. **Store the token securely.** Save the `Token` string, card expiry, and last 4 digits. The token is bound to your terminal.

3. **Charge the token** via the Transaction endpoint:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/Transaction
{
  "TerminalNumber": 1000,
  "ApiName": "your-api-name",
  "Token": "token-uuid",
  "CardExpirationMMYY": "1227",
  "Amount": 99.00,
  "ISOCoinId": 1,
  "ExternalUniqTranId": "sub-8841-2026-10",
  "Document": {
    "DocumentTypeToCreate": "TaxInvoiceAndReceipt",
    "Name": "Subscriber Name",
    "Email": "customer@example.com",
    "IsSendByEmail": true,
    "Products": [
      { "Description": "Monthly subscription", "UnitCost": 99.00, "Quantity": 1 }
    ]
  }
}
```

`ExternalUniqTranId` is one id per subscriber per billing cycle, so a retry of the same cycle is blocked (608) while next month's charge goes through. The response is a `TransactionInfo`: only `ResponseCode == 0` is a charge (`700`/`701` are J2/J5 validation answers, where nothing was charged), then read `TranzactionId`, `Token`, `DocumentNumber`, and `DocumentUrl`. Each token charge can automatically generate and email an invoice when a `Document` object is attached; if `DocumentNumber` is missing, the card was charged but the invoice was not issued, so issue it with `CreateDocument` rather than re-charging.

### Step 6: Process Refunds

Refund a transaction by its Cardcom transaction id:

```
POST https://secure.cardcom.solutions/api/v11/Transactions/RefundByTransactionId
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "TransactionId": 219282004,
  "PartialSum": 100.00,
  "CancelOnly": false,
  "AllowMultipleRefunds": false
}
```

`ApiPassword` is required for refunds. `PartialSum` refunds part of the transaction (omit it to refund the full amount). `CancelOnly: true` voids a transaction before it is deposited. The response is a `RefundByTransactionIdResp`: check `ResponseCode == 0`, then read `NewTranzactionId` (the id of the refund transaction).

To issue the matching credit document, call `Documents/CreateDocument` with a refund `DocumentTypeToCreate` such as `TaxInvoiceAndReceiptRefund` or `TaxInvoiceRefund`, and link it to the REFUND transaction through `DealNumbers: [{"DealNumber": <NewTranzactionId>}]`, not to the original charge. Cardcom's refund guidance for its older interface states this explicitly: after a refund you call the document API again and cross it to the refund deal. Do not also call `Documents/CancelDoc` for the same refund: its spec summary is "Cancel document and refund credit card", it takes `ApiName`, `ApiPassword`, `DocumentNumber` and an INTEGER `DocumentType`, and returns a `NewDocumentNumber`, so combining it with `RefundByTransactionId` risks refunding twice. For a FULL refund of a sale that has a document, `CancelDoc` on its own is the document-linked alternative; `AllowMultipleRefunds` (default `false`) is your guard against refunding the same transaction twice.

### Step 6.5: Query Transactions for Reporting

To pull a date range of transactions (reconciliation, monthly reports, dashboards):

```
POST https://secure.cardcom.solutions/api/v11/Transactions/ListTransactions
{
  "ApiName": "your-api-name",
  "ApiPassword": "your-api-password",
  "FromDate": "01062026",
  "ToDate": "30062026",
  "TranStatus": "Success",
  "Page": 1,
  "Page_size": 100
}
```

`ApiPassword`, `FromDate`, `ToDate` (`DDMMYYYY` strings, so `01062026` is 1 June 2026), `Page` (from 1) and `Page_size` (10 to 2000) are all required. There is no `TerminalNumber` field; scope to a terminal with `LimitForTerminal`.

The response is a `GetTranzactionsResp`: check `ResponseCode == 0`, then read `Tranzactions` (an array of `TransactionInfo`), plus the echoed `Page` and `Page_size`. Keep requesting the next page until a page returns fewer rows than `Page_size`.

`Transactions/SpecialTransactions` is a READ endpoint despite its name (see `references/api-endpoints.md`).

### Step 7: Suspended Deals (Deferred Charges)

A suspended deal authorizes a payment intent without an immediate charge:

1. Create a Low Profile session with `Operation: "SuspendedDeal"`.
2. The `LowProfileResult` returns `SuspendedInfo` with a `SuspendedDealId`.
3. Charge it later in the Cardcom admin panel or with `POST /api/v11/SuspendedDeals/Charge`, whose only fields (all required, `additionalProperties: false`) are `TerminalNumber`, `ApiName` and `SuspendedDealID`. **Note the casing:** the result object spells it `SuspendedDealId`, the request `SuspendedDealID`; send the request spelling. `SuspendedDeals/Cancel` and `GetSuspendedDealInfo` take the same three fields; the group also has `GetSuspendedDeals` and `UpdateSuspendedDealInfo`.

Useful for pre-authorizations and services billed after delivery. `JValidateType` also applies here and defaults to `5` (J5) on `LowProfile/Create`, so a suspended deal normally holds the amount on the card: cancel the ones you will not charge.

### Step 8: Handle Errors

Every endpoint this skill uses returns a `ResponseCode` integer and a `Description` string (a few others, such as `GetTransactionInfoById` and the `CompanyOperations` lookups, return bare arrays or booleans instead). `ResponseCode == 0` means success; any non-zero value is a developer/transaction error and `Description` carries the human-readable reason.

```python
import requests

BASE = "https://secure.cardcom.solutions/api/v11"
payload["ExternalUniqTranId"] = order_id  # same id on every retry of THIS charge

try:
    r = requests.post(f"{BASE}/Transactions/Transaction", json=payload, timeout=30)
except requests.RequestException:
    r = None  # outcome unknown: the card MAY have been charged

if r is None or r.status_code != 200:
    # Never re-charge blind. Ask Cardcom whether the charge went through.
    q = requests.post(f"{BASE}/Transactions/GetTransactionByExternalUniqTran",
                      json={"TerminalNumber": payload["TerminalNumber"],
                            "ApiName": payload["ApiName"],
                            "ExternalUniqTranId": order_id}, timeout=30)
    resp = q.json() if q.status_code == 200 else None
else:
    resp = r.json()

code = resp.get("ResponseCode") if resp else None
if code == 0:
    deal_id = resp["TranzactionId"]
elif code == 608:
    mark_for_lookup(order_id)  # id already answered: look the record up, never re-charge
else:
    log_error(f"Cardcom error {code}: {resp.get('Description') if resp else 'no response'}")
```

Always check both the HTTP status (200 means the request was received) AND `ResponseCode` (0 means the operation succeeded). Keep `ApiName`/`ApiPassword` server-side only; none of these calls may run from browser JavaScript. The official docs at `https://secure.cardcom.solutions/Api/v11/Docs` carry the full numeric error reference; do not hardcode error-code-to-message mappings, read `Description` instead. See `references/api-responses.md` for the handling pattern.

## Examples

### Example 1: E-commerce Checkout with Invoice
User says: "I need to accept payments on my Israeli e-commerce site and generate tax invoices automatically"
Actions:
1. Choose Low Profile with `DocumentTypeToCreate: "TaxInvoiceAndReceipt"`.
2. Create the Low Profile page via `LowProfile/Create` with product details in the `Document` object.
3. Implement a `WebHookUrl` handler that calls `LowProfile/GetLpResult`.
Result: Customer pays and receives an automatic hashbonit mas/kabala emailed as a PDF.

### Example 2: Monthly SaaS Subscription
User says: "I run a SaaS product, I need to charge users 149 NIS monthly and send them invoices"
Actions:
1. First payment: `LowProfile/Create` with `Operation: "ChargeAndCreateToken"`.
2. Store the `Token`, `CardMonth`, `CardYear` from `TokenInfo`.
3. Monthly cron: `Transactions/Transaction` with the token, a fresh `ExternalUniqTranId` per billing cycle, and a `Document` object.
Result: Automated recurring billing with monthly invoice generation.

### Example 3: Standalone Invoice Without Payment
User says: "I need to generate a tax invoice for a bank transfer payment I already received"
Actions:
1. Use `Documents/CreateDocument` (no payment processing).
2. Set `DocumentTypeToCreate: "TaxInvoice"`.
3. Include `Name`, `TaxId`, `Products[]`, set `IsSendByEmail: true` with the customer email.
Result: Tax invoice generated and emailed without credit card processing.

### Example 4: Process a Refund with Credit Note
User says: "Customer wants a refund for order #5678, need to issue a credit note too"
Actions:
1. Call `Transactions/RefundByTransactionId` with `TransactionId` and `ApiPassword`.
2. Check `ResponseCode == 0` and read `NewTranzactionId`.
3. Call `Documents/CreateDocument` with `DocumentTypeToCreate: "TaxInvoiceAndReceiptRefund"` and `DealNumbers: [{"DealNumber": <NewTranzactionId>}]`.
Result: Refund processed and the matching credit document generated.

### Example 5: Accept Bit, Apple Pay, and Google Pay
User says: "I want to let customers pay with Bit, Apple Pay, and Google Pay in addition to credit cards"
Actions:
1. Enable each method on the terminal, then create the Low Profile page as usual.
2. Show `UrlToBit` beside the card form; Apple Pay and Google Pay appear inside the page (Apple Pay on one-off charges only, not on a token-creating page).
Result: Customers choose a payment method; same webhook flow.

## Community Libraries

- **@tsdiapi/cardcom** (TypeScript/Node.js) -- community V11 client, not reviewed by us. `npm install @tsdiapi/cardcom`
- **CardCom/OpenFields-FrontEnd-React** and **CardCom/OpenFields-Backend-Node** -- Cardcom's official OpenFields examples (links below).

## Reference Links

| Resource | URL |
|----------|-----|
| V11 API documentation (OpenAPI reference) | `https://secure.cardcom.solutions/Api/v11/Docs` |
| Cardcom support center | `https://support.cardcom.solutions` |
| OpenFields React example | `https://github.com/CardCom/OpenFields-FrontEnd-React` |
| OpenFields Node.js example | `https://github.com/CardCom/OpenFields-Backend-Node` |

## Bundled Resources

### References
- `references/api-endpoints.md` -- Cardcom REST API V11 endpoint reference: LowProfile, Transactions, Documents, RecuringPayments, Financial, and CompanyOperations paths with their key request/response fields. Consult when building API integrations.
- `references/api-responses.md` -- the V11 `ResponseCode` + `Description` response pattern, the per-operation response objects, and the recommended error-handling flow. Consult when debugging failed API calls.
- `references/document-types.md` -- the `DocumentTypeToCreate` string enum, the `Document` object field list, and VAT handling per Israeli tax law. Consult when determining which document type to generate.
- `references/production-checklist.md` -- subscription preconditions, document totals, J5 release, webhook state, idempotency and secrets. Read before going live.
- `references/domain-checklist.md` -- the coverage checklist this skill is reviewed against.

### Scripts
- `scripts/validate_cardcom_response.py` -- Validates a Cardcom V11 API response, either a `LowProfileResult` or a flat response (`Transaction`, `CreateDocument`, `RefundByTransactionId`). `--expect {charge,token,document,refund,validation}` fails closed when the expected result is missing, `--amount` and `--return-value` reconcile against your order, and `--with-document` fails a charge whose invoice was not issued. Only `ResponseCode` 0 counts as success; 700/701 are rejected unless you pass `--validation-only`, because they mean a J2/J5 card check passed and nothing was charged. 608 is reported as a blocked duplicate. Run: `python scripts/validate_cardcom_response.py --help`

## Gotchas
- The V11 success check is `ResponseCode == 0`, NOT `DealResponse == 0`. `DealResponse` does not exist in V11; agents trained on older Cardcom examples invent it. The endpoints in this skill return `ResponseCode` plus a `Description` string.
- `DocumentTypeToCreate` (on `Document` objects) and `DocumentType` on `CreateDocumentUrl` are STRING enums (`"TaxInvoiceAndReceipt"`, `"TaxInvoice"`, ...). But several V11 document endpoints take an INTEGER type: `CancelDoc.DocumentType`, `SendAllDocumentsToEmail.DocumentType`, `GetReport.DocType` and the `CrossDocument` fields. The spec does not publish the integer-to-name mapping, so take the value from Cardcom (or from a document you already hold) rather than guessing.
- The `TerminalNumber` must be sent as an integer, not a string. Agents commonly wrap it in quotes.
- **The `ApiPassword` list drifts between spec revisions, so never answer from memory.** This skill once said `Documents/ExternalShopCreateDocument` had no `ApiPassword`; the current spec requires it, and a `TapTransactions` path it cited is gone. Read the endpoint's schema. The reverse case: `ApiPassword` is not a top-level field of `LowProfile/Create` or `Transactions/Transaction`, but it IS required inside `Advanced` / `AdvancedDefinition` when you set `IsRefund` / `IsRefundDeal` (the token-or-card refund path, when you have no original `TransactionId`).
- **The webhook is not authenticated.** There is no signature or secret field anywhere on `LowProfile/Create`, and `WebHookUrl` is a required field, not an optional one. Anyone who learns the URL can POST to it, so it must only ever trigger a `GetLpResult` lookup for a `LowProfileId` you created (Step 3b).
- The reporting endpoints `ListTransactions` and `SpecialTransactions` do NOT accept `TerminalNumber`, and neither schema lists it (both are marked `additionalProperties: false`), so do not send it. Scope to a terminal with `LimitForTerminal` on `ListTransactions`. Their dates are `DDMMYYYY` strings, and `ListTransactions` additionally requires `Page` plus a `Page_size` between 10 and 2000.
- Watch the real V11 field spellings: `ISOCoinID` / `ISOCoinId`, `IsSendByEmail` (not `SendByEmail`), `TaxId` (not `VAT_Number`). **The language field is spelled differently depending on which document object you are in, and each schema lists only its own spelling (`additionalProperties: false`), so the other spelling is at best ignored:** `Document` (standalone `CreateDocument`) and `DocumentTran` (`Transaction`) use the misspelled `Languge`, while `DocumentLP`, the document you attach to `LowProfile/Create`, uses the correctly spelled `Language`. Applying `Languge` everywhere means the Low Profile document language is not set as you intended.
- The current Israeli VAT rate is 18% (effective January 2025; it was 17% before that, so a document reissued for an earlier period must use the rate in force on ITS date). Cardcom calculates VAT server-side, so document amounts are treated per the `IsVatFree` flag.
- **PCI scope**: hosted Low Profile keeps you in SAQ-A. Server-to-server `Transaction` with raw `CardNumber`/`CVV2` lands in SAQ-D. The current standard is PCI DSS v4.0.1; its 51 future-dated requirements have been in force since 31 March 2025. Prefer Low Profile or tokens unless you have a real reason to touch raw card data.
- **Settlement timing** is configured on the terminal, not per request, and is not settable via the API. Cardcom publishes monthly, weekly and bi-monthly cycles (dates in `references/api-endpoints.md`); confirm the cycle configured on the merchant's terminal before promising a specific day.

## Troubleshooting

### Error: a non-zero `ResponseCode` on `LowProfile/Create`
Cause: a validation or authentication problem with the request.
Solution: Read the `Description` string in the response, it names the exact issue. Verify `TerminalNumber` is an integer and `ApiName` is correct. The full numeric error reference is at `https://secure.cardcom.solutions/Api/v11/Docs`.

### Error: "Low Profile page loads but payment fails"
Cause: on the test terminal, test-card amounts above 5,000 NIS are simulated as failures (Cardcom's test page). Otherwise the card result is in `TranzactionInfo.Description`; this skill has not verified other causes.
Solution: Test below 5,000 NIS, then read `TranzactionInfo.ResponseCode` and `Description` from `GetLpResult`. Cardcom's documentation asks for external (not localhost) HTTPS redirect and notify URLs, so use a tunnel in development.

### Error: "Refund returns a non-zero `ResponseCode`"
Cause: `ApiPassword` missing, or the transaction is already deposited and you sent `CancelOnly: true`.
Solution: Include `ApiPassword` on every refund request. Use `CancelOnly: true` only before deposit; after deposit, send a real refund (omit `CancelOnly` or set it `false`).

### Error: "Invoice created but not emailed"
Cause: `IsSendByEmail` explicitly set to `false` (its default is `true`), or the `Email` is missing or invalid.
Solution: Leave `IsSendByEmail` at `true` and include a valid `Email` in the `Document` object. Check spam folders, Cardcom sends from its own domain.

### Error: `ResponseCode` 608 on a token charge
Cause: the same `ExternalUniqTranId` was already used by a call that got a valid card answer, a charge or a J2/J5 check (spec: "if the same ExternalUniqTranId will be send you will receive and error code 608").
Solution: do not re-charge with a new id. Call `Transactions/GetTransactionByExternalUniqTran` and branch on that record's `ResponseCode`: 0 means the customer was already charged, 700/701 mean the earlier call was only a J2/J5 check.

### Error: "Token charge succeeds but no invoice"
Cause: `Document` object missing from the `Transaction` request.
Solution: Include the full `Document` object with `DocumentTypeToCreate`, `Name`, and `Products` in every token charge. Document generation is opt-in per transaction.
