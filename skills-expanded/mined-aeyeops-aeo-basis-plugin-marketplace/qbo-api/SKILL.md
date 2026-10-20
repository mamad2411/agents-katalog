---
name: qbo-api
description: >
  Contains verified AccountType/AccountSubType mapping table, batch chunking implementation with
  rate-limit handling, and OAuth 2.0 token lifecycle patterns for the QuickBooks Online REST and
  GraphQL APIs. Covers entity CRUD, SyncToken concurrency, error codes (5010/6210/6140/429),
  query pagination, multipart attachment upload, webhook signature validation, and python-quickbooks
  SDK examples. Consult when writing Python code against the QBO API, diagnosing specific QBO error
  codes, building batch import pipelines from CSV, choosing REST vs GraphQL, uploading documents to
  transactions, resolving OAuth token refresh or invalid_grant errors, or validating Intuit webhook
  signatures.
---

# QBO API

Platform-specific patterns for programmatic interaction with QuickBooks Online via REST
and GraphQL APIs. Covers authentication, entity operations, bulk processing, error recovery,
rate limiting, and document attachment workflows.

## OAuth 2.0 Authentication

QBO uses OAuth 2.0 with short-lived access tokens (1 hour) and long-lived refresh tokens (100 days).
All API calls require a valid Bearer token.

**Setup flow**: Create `AuthClient` with client_id, client_secret, redirect_uri, and environment
(`sandbox` or `production`). Generate auth URL with `Scopes.ACCOUNTING`, redirect user, exchange
auth code for tokens via `auth_client.get_bearer_token(auth_code, realm_id=realm_id)`.

**Token lifecycle**:
- Access token expires in ~60 minutes — refresh proactively or catch 401
- Refresh token expires in 100 days — if `invalid_grant` occurs, full re-authorization required
- Store refresh tokens securely; they are long-lived credentials
- After refresh, rebuild the `QuickBooks` client with the new refresh token

**Environment control**: `QBO_ENVIRONMENT` env var (`sandbox` or `production`) determines base URL
and realm ID. Always verify environment before writes — production writes are irreversible.

| Environment | REST Base URL | GraphQL Endpoint |
|-------------|---------------|------------------|
| Sandbox | `https://sandbox-quickbooks.api.intuit.com` | `https://public.api.intuit.com/2020-04/graphql` |
| Production | `https://quickbooks.api.intuit.com` | `https://public.api.intuit.com/2020-04/graphql` |

## REST API Entity Operations

All entity endpoints follow the pattern: `POST /v3/company/{realmId}/{entity}` for create/update,
`GET /v3/company/{realmId}/{entity}/{id}` for read. Use `?minorversion=65` for latest features.

### AccountRef Resolution

QBO matches entities on `AccountRef.value` (the numeric `Account.Id`), not on name. The `name`
field is informational only. Always resolve Account.Id from a live query before building payloads:

```python
qbo_accounts = Account.all(qb=client)
account_lookup = {a.Name.lower(): {'id': a.Id, 'type': a.AccountType} for a in qbo_accounts}
```

### SyncToken Concurrency

Every QBO entity carries a `SyncToken` that increments on each update. Updates MUST include
the current SyncToken. If another process modified the entity, you get error 5010 (Stale Object).
Resolution: re-fetch the entity, re-apply changes, retry. Max 3 retries is standard.

### AccountType and AccountSubType Validation

Account creation requires a valid `AccountType` + `AccountSubType` pair. Mismatches produce
validation errors. Key pairs for C-corp work:

- **Bank** — Checking, Savings, MoneyMarket, CashOnHand
- **Other Current Asset** — Investments, PrepaidExpenses, UndepositedFunds, LoansToOfficers, LoansToStockholders
- **Fixed Asset** — Buildings, Land, MachineryAndEquipment, FurnitureAndFixtures, AccumulatedDepreciation
- **Other Asset** — Goodwill, IntangibleAssets, OrganizationalCosts, AccumulatedAmortization
- **Equity** — CommonStock, PreferredStock, RetainedEarnings, TreasuryStock, PaidInCapitalOrSurplus, OpeningBalanceEquity
- **Income** — ServiceFeeIncome, SalesOfProductIncome, OtherPrimaryIncome
- **Other Income** — DividendIncome, InterestEarned, OtherInvestmentIncome
- **Expense** — standard operating categories (see `references/api-entities.md` for full list)
- **Other Expense** — Depreciation, Amortization, ExchangeGainOrLoss, PenaltiesAndSettlements
- **Cost of Goods Sold** — CostOfLaborCos, SuppliesMaterialsCogs, OtherCostsOfServiceCos

### Core Entity Patterns

**JournalEntry** — Lines must balance (debits = credits). Each line requires `DetailType: "JournalEntryLineDetail"`,
`Amount`, and `JournalEntryLineDetail` with `PostingType` (Debit/Credit) and `AccountRef`. Use `PrivateNote`
for memo, `DocNumber` for reference numbering.

**Invoice/Bill/Payment** — Use `CustomerRef`/`VendorRef` with entity Id. Invoices use `SalesItemLineDetail`
with `ItemRef`, Bills use `AccountBasedExpenseLineDetail` with `AccountRef`. Payments link to invoices
via `LinkedTxn` array with `TxnId` and `TxnType`.

**Transfer/Deposit** — Transfer uses `FromAccountRef`/`ToAccountRef`. Deposits can link to existing
payments via `LinkedTxn` or take direct deposit lines.

### Query Syntax

REST queries use a SQL-like dialect: `SELECT * FROM Entity WHERE field operator value`.
Operators: `=`, `!=`, `<`, `>`, `<=`, `>=`, `IN (...)`, `LIKE 'pattern%'`.
Pagination: `STARTPOSITION n MAXRESULTS m` (max 1000 per page). Always paginate large result sets.

## Batch Operations

Batch API sends up to 30 operations in a single `POST /v3/company/{realmId}/batch` call.
Supported operations: `create`, `update`, `delete`, `query`. Each item needs a unique `bId`
for correlating responses.

**Constraints**:
- Max 30 items per batch request
- Max 40 batch requests per minute
- 5-minute timeout per batch call

**Processing pattern**:
1. Validate all entries before batching (missing fields, balance checks)
2. Chunk into groups of 30 using `chunk_list(entries, 30)`
3. Execute each chunk with rate limiting (1.5s pause between chunks)
4. Correlate results by `bId` — separate successes from faults
5. On batch-level failure, fall back to individual requests per item

**Batch IDs**: Use descriptive IDs that aid debugging (e.g., `je-2024-01-div-aapl`), not
sequential numbers.

**SDK shortcut**: `python-quickbooks` provides `batch_create` and `batch_delete` that handle
chunking internally.

## GraphQL API

Single endpoint for both environments: `https://public.api.intuit.com/2020-04/graphql`.
Uses the same OAuth 2.0 tokens as REST.

**When to use GraphQL over REST**:
- Need related data in a single request (invoice + customer + payments)
- Want field selection to minimize data transfer
- Complex filtering with rich filter syntax
- Building dashboards or reports

**When to use REST instead**:
- Batch operations (GraphQL has no batch support)
- Simple CRUD on single entities
- Existing REST integration

**Pagination**: GraphQL uses cursor-based pagination with `pageInfo.hasNextPage` and
`pageInfo.endCursor`. Pass `pagination: { first: N, after: cursor }`.

**Filtering**: Supports `equals`, `greaterThan`, `lessThan`, `between` operators.
Combine filters within a single `filter` argument. Date ranges use
`between: [$startDate, $endDate]`.

**Mutations**: Available for entity creation/update (e.g., `createCustomer`, `updateInvoice`).
Schema is type-safe with dedicated input types.

**Inline fragments**: Use `... on Invoice`, `... on Bill`, `... on JournalEntry` for
polymorphic transaction queries.

## Error Handling

### HTTP Status Codes

- **400** — Bad request: check field values, required fields, type/subtype combos
- **401** — Token expired: refresh access token, rebuild client
- **403** — Insufficient scopes or permissions
- **404** — Entity ID does not exist
- **429** — Rate limit exceeded: back off exponentially
- **500/503** — Transient server error: retry with exponential backoff

### Critical Error Codes

- **2010 (Object Not Found)** — Referenced entity ID does not exist. Verify ID with a query first.
- **5010 (Stale Object)** — SyncToken mismatch. Re-fetch entity, re-apply changes, retry.
- **6000 (Business Validation)** — Generic validation failure. Check field constraints.
- **6130 (Required Line Missing)** — Transaction requires at least one line item.
- **6140 (Invalid Reference)** — Referenced entity is inactive or does not exist.
- **6210 (Duplicate Name)** — Entity name must be unique within its type. Query for existing entity first with `create_or_get` pattern.

### Token Error Decision Tree

1. `expired_token` / HTTP 401 — Call `auth_client.refresh()`, rebuild client, retry
2. `invalid_grant` — Refresh token expired (>100 days). Full re-authorization flow required.
3. `invalid_client` — Wrong client_id or client_secret. Check credentials.
4. `access_denied` — User denied authorization at consent screen.

### Retry Strategy

Use exponential backoff with jitter for transient errors (429, 500, 502, 503, 504).
`tenacity` library pattern: `stop_after_attempt(5)`, `wait_exponential(multiplier=1, min=2, max=60)`.
Non-retryable errors (400, 403, 404, business logic) should fail immediately.

## Rate Limiting

| Endpoint Type | Limit | Window |
|---------------|-------|--------|
| Standard (CRUD/query) | 500 requests | Per minute |
| Batch | 40 requests | Per minute |
| Reports | 10 requests | Per minute |

Implement a sliding-window rate limiter that tracks request timestamps. For batch pipelines,
enforce 40/minute at the batch level and add inter-chunk delays. Report endpoints are the most
constrained — cache results when possible.

## Attachment Management

### Upload Flow

`POST /v3/company/{realmId}/upload` with `multipart/form-data`. Include `file_content_0` (binary)
and `file_metadata_0` (JSON with `FileName` and optional `AttachableRef` for immediate linking).

**Supported files**: Images (jpg, png, gif, bmp, tiff), documents (pdf, doc/x, xls/x, txt, rtf),
data (csv, xml). Max 20 MB per file.

**Link-on-upload**: Include `AttachableRef` with `EntityRef.type` and `EntityRef.value` in metadata
to link the file to a transaction in a single call. Supported entity types: Invoice, Bill,
JournalEntry, Payment, BillPayment, Deposit, Transfer, SalesReceipt, CreditMemo, Estimate,
PurchaseOrder, VendorCredit, Customer, Vendor, Employee, Item.

### Post-Upload Operations

- **Query**: `SELECT * FROM Attachable WHERE AttachableRef.EntityRef.Type = '{type}' AND AttachableRef.EntityRef.value = '{id}'`
- **Download**: Fetch `TempDownloadUri` from Attachable metadata, then stream binary content
- **Delete**: `POST /v3/company/{realmId}/attachable?operation=delete` with `Id` and `SyncToken`
- **Batch upload**: Use `ThreadPoolExecutor` with max 5 workers for concurrent uploads; each
  upload is an independent HTTP call (not the batch API endpoint)

### Attachment Use Cases

- Brokerage statements linked to dividend/investment JEs
- Tax documents (1099-DIV, 1099-INT, K-1) linked to relevant transactions or standalone
- Vendor PDF invoices linked to Bills
- Bank statements linked to reconciliation JEs

## Webhook Signature Validation

Verify incoming webhook payloads using HMAC-SHA256 with the verifier token:
`hmac.new(verifier_token.encode(), payload_bytes, hashlib.sha256)`. Compare
base64-encoded digest to the `intuit-signature` header using `hmac.compare_digest`
(constant-time comparison to prevent timing attacks).

## Supporting References

Read these for implementation details, code examples, and edge cases:

- `references/quickbooks-online-integration.md` — Full integration starter: OAuth setup, Python SDK client creation, environment configuration, journal entry creation patterns, year-end close behavior, CSV import conventions, account name identity resolution. Read when setting up a new QBO integration from scratch or understanding the overall integration architecture.
- `references/api-entities.md` — Complete REST entity reference for Account, JournalEntry, Invoice, Bill, Payment, Customer, Vendor, Deposit, Transfer. Includes full AccountType/AccountSubType mapping table, HTTP request/response examples, Python SDK code, and query operation syntax with pagination. Read when you need exact field names, valid type combinations, or entity-specific code examples.
- `references/error-codes.md` — HTTP status codes, OAuth token errors, validation error codes (2010, 5010, 6000, 6130, 6140, 6210), rate limit details, retry patterns with `tenacity`, batch error handling, and troubleshooting guide for common failures. Read when diagnosing specific API errors or implementing error recovery logic.
- `references/batch-patterns.md` — Batch request/response format, chunking implementation, rate limit handling for batch endpoint, validation-before-batch pattern, result correlation by bId, retry with fallback to individual requests, and complete CSV bulk import example. Read when building batch import pipelines or processing bulk operations.
- `references/graphql-patterns.md` — GraphQL endpoint, authentication, query examples (company info, invoices, accounts, customers), filtering syntax, cursor-based pagination helper, mutations, inline fragments for polymorphic queries, REST vs GraphQL decision matrix. Read when building GraphQL queries or deciding between REST and GraphQL.
- `references/attachments-upload.md` — Upload endpoint, supported file types/sizes, multipart form-data format, link-to-transaction pattern, upload-and-link single-step operation, note creation without file upload. Read when implementing file upload workflows.
- `references/attachments-management.md` — Query attachments by entity, download via TempDownloadUri, delete with SyncToken, concurrent batch upload with ThreadPoolExecutor, use cases for brokerage statements and tax documents. Read when querying, downloading, or managing existing attachments.

## Cross-Plugin References

For platform-agnostic accounting concepts:
- Invoke `accounting-foundation:chart-of-accounts` for COA design principles, account type taxonomy, numbering conventions, and Form 1120 tax-line mapping independent of QBO
- Invoke `accounting-foundation:categorization-rules` for transaction-to-account routing logic

For QBO-specific COA implementation:
- Invoke `qbo-integration:qbo-coa` for QBO account creation, detail types, special QBO accounts, and QBO-specific COA pitfalls

## Cross-Plugin Consumers

- `bookkeeping:transaction-processing` — batch API patterns for bulk transaction import
- `tax-prep:form-1120-prep` — API-driven data extraction for tax return preparation
- `firm-operations:engagement-management` — OAuth setup and initial API connectivity
