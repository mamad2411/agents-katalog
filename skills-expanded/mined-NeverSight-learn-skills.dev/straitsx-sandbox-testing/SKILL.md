---
name: straitsx-sandbox-testing
description: Walk through a complete StraitsX sandbox integration flow. Generates working code for end-to-end testing — from customer profile creation to payment collection, payout, and webhook/callback integration. Use when the user asks about sandbox testing, integration walkthroughs, webhook testing, or "how do I test the full flow?"
category: setup
parent: straitsx-api
---

# StraitsX Sandbox Testing

## Invoke This Skill When

- User asks "How do I test the full flow?" or "Walk me through sandbox integration"
- User wants to try the API end-to-end in sandbox
- User asks about mock payments, simulating bank transfers, or testing payouts
- User is new to StraitsX and wants a working example
- User asks about testing webhooks/callbacks in sandbox
- User wants to verify callback signatures during sandbox testing

## Prerequisites

- Sandbox API key configured (see the `straitsx-auth-setup` skill)
- `X_XFERS_APP_API_KEY` environment variable set with a sandbox key
- (For webhook testing) `STRAITSX_SIGNING_SECRET` environment variable set with the signing secret from Dashboard
- **Required permissions**: Your sandbox API key must have the necessary endpoint scopes enabled. If you receive `XFE6` (403 Access Denied) on any endpoint, contact StraitsX support at https://support.straitsx.com/hc/en-us/requests/new to request access. Sandbox keys may need explicit scope grants just like production keys.

## Step 1: Ask the User's Integration Model

Before generating code, ask which model they need:

| Model | Use case | What it covers |
|---|---|---|
| **First-Party** | Collect payment from a customer, pay out to the same bank account | CP → Bank Account → VBA → Mock Payment → First-Party Payout |
| **Third-Party** | Collect payment from a customer, pay out to a different recipient | CP → Bank Account → VBA → Mock Payment → Payout Recipient → Third-Party Payout |
| **Regular** | Send money from your business account to any recipient | VBA → Mock Payment → Payout Recipient → Regular Payout |

If the user doesn't specify, default to **First-Party** as it's the most common starting point.

## Step 2: Generate the Flow

Generate a complete, runnable script in the user's preferred language (default to Python if not specified). The script should be sequential — each step depends on the previous one.

### First-Party Flow

```mermaid
sequenceDiagram
    autonumber
    participant You
    participant API as StraitsX Sandbox API

    rect rgb(230, 242, 255)
    Note over You, API: Setup
    You->>API: POST /kyc/customer_profiles (create personal CP)
    API-->>You: customer_profile_id
    You->>API: PUT /sandbox/kyc/customer_profiles/{id} (verify CP)
    You->>API: POST /customer_profile/{id}/bank_accounts (add bank account)
    API-->>You: bank_account_id
    You->>API: PUT /sandbox/.../bank_accounts/{id} (verify bank account)
    end

    rect rgb(230, 255, 230)
    Note over You, API: Collect Payment
    You->>API: POST /payment_methods/virtual_bank_accounts (create VBA)
    API-->>You: virtual_bank_account_id + account_no
    You->>API: POST /sandbox/.../bank_transfer_simulations (mock payment)
    API-->>You: contract_id
    You->>API: PUT /sandbox/.../payments/{contract_id} (complete payment)
    end

    rect rgb(255, 243, 230)
    Note over You, API: Payout
    You->>API: POST /customer_profile/{id}/withdrawals (first-party payout)
    API-->>You: contract_id
    You->>API: PUT /sandbox/.../withdrawals/{contract_id} (complete payout)
    end
```

```
1. Create a personal customer profile
   POST /kyc/customer_profiles
   Body is FLAT (not nested under data.attributes). Required fields include:
   customerName, registrationType ("personal"), registrationIdType, registrationIdCountry,
   registrationId, countryOfResidence, dateOfBirth, nationality (ISO alpha-2 code, e.g. "SG"),
   address (object with street, city, postalCode, state, country).
   Note: address.street only allows letters, numbers, spaces, and / - ? : ( ) . , ' + (no # character).

2. [Sandbox] Verify the customer profile
   PUT /sandbox/kyc/customer_profiles/{customer_profile_id}
   Body: { "data": { "attributes": { "verificationStatus": "verified" } } }

3. Create a customer profile bank account
   POST /customer_profile/{customer_profile_id}/bank_accounts
   Body is FLAT. Required fields: account_holder_name, bank (e.g. "DBS"), account_no,
   bank_account_proof (object with fileUrl — use a direct image URL, e.g. "https://xfers-public.s3.amazonaws.com/sample-bank-statement.png").
   Note: fileUrl must point to a directly accessible image (png/jpg/jpeg/pdf) without query parameters.

4. [Sandbox] Verify the bank account
   PUT /sandbox/customer_profile/{customer_profile_id}/bank_accounts/{bank_account_id}?verification_status=verified
   This endpoint uses a query parameter, NOT a request body. No body needed.

5. Create a virtual bank account (VBA) for the customer profile
   POST /payment_methods/virtual_bank_accounts
   Body uses data.attributes + data.relationships (nested format).

6. [Sandbox] Simulate a bank transfer payment to the VBA
   POST /sandbox/customer_profile/{customer_profile_id}/bank_transfer_simulations
   Body is FLAT. Required fields: destination_bank_account_no (the VBA account_no),
   amount, source_bank_account_holder_name.

7. [Sandbox] Complete the mock payment
   PUT /sandbox/customer_profile/{customer_profile_id}/payments/{contract_id}
   Body: { "data": { "attributes": { "status": "completed" } } }

8. Create a first-party payout (withdraw to the same bank account)
   POST /customer_profile/{customer_profile_id}/withdrawals
   Body is FLAT. Required fields: bank_account_id, amount, idempotency_id (unique UUID).

9. [Sandbox] Complete the mock payout
   PUT /sandbox/customer_profile/{customer_profile_id}/withdrawals/{contract_id}
   Body is FLAT: { "status": "completed" }
```

### Third-Party Flow

```mermaid
sequenceDiagram
    autonumber
    participant You
    participant API as StraitsX Sandbox API

    rect rgb(230, 242, 255)
    Note over You, API: Setup (same as First-Party steps 1–7)
    You->>API: Create CP → Verify → Bank Account → Verify → VBA → Mock Payment → Complete
    end

    rect rgb(255, 243, 230)
    Note over You, API: Payout to Different Recipient
    You->>API: POST /customer_profile/{id}/payout-recipients (create recipient)
    API-->>You: recipient_id
    You->>API: POST /customer_profile/{id}/payouts (third-party payout)
    API-->>You: contract_id
    You->>API: PUT /sandbox/.../payouts/{contract_id} (complete payout)
    end
```

```
Steps 1–7: Same as First-Party Flow

8. Create a payout recipient for the customer profile
   POST /customer_profile/{customer_profile_id}/payout-recipients

9. Create a third-party payout
   POST /customer_profile/{customer_profile_id}/payouts

10. [Sandbox] Complete the mock payout
    PUT /sandbox/customer_profile/{customer_profile_id}/payouts/{contract_id}
    Body: { "data": { "attributes": { "status": "completed" } } }
```

### Regular Flow

```mermaid
sequenceDiagram
    autonumber
    participant You
    participant API as StraitsX Sandbox API

    rect rgb(230, 242, 255)
    Note over You, API: Get Balance (collect a payment first)
    You->>API: POST /payment_methods/virtual_bank_accounts (create VBA)
    API-->>You: account_no
    You->>API: POST /sandbox/.../bank_transfer_simulations (mock payment)
    API-->>You: contract_id
    You->>API: PUT /sandbox/.../payments/{contract_id} (complete payment)
    end

    rect rgb(255, 243, 230)
    Note over You, API: Payout
    You->>API: POST /payout-recipients (create recipient)
    API-->>You: recipient_id
    You->>API: POST /payouts (regular payout)
    API-->>You: contract_id
    You->>API: PUT /sandbox/payouts/{contract_id} (complete payout)
    end
```

```
1. Create a virtual bank account (to collect a payment and get balance)
   POST /payment_methods/virtual_bank_accounts

2. [Sandbox] Simulate a bank transfer payment
   POST /sandbox/virtual_bank_accounts/bank_transfer_simulation

3. [Sandbox] Complete the mock payment
   PUT /sandbox/payments/{contract_id}
   Body: { "data": { "attributes": { "status": "completed" } } }

4. Create a payout recipient
   POST /payout-recipients

5. Create a regular payout
   POST /payouts

6. [Sandbox] Complete the mock payout
   PUT /sandbox/payouts/{contract_id}
   Body: { "data": { "attributes": { "status": "completed" } } }
```

## Step 3: Webhook Integration (Optional but Recommended)

Ask the user if they want to include webhook/callback testing in their sandbox flow. In production, callbacks are the primary way to know when a transaction status changes — so testing them in sandbox is strongly recommended.

### 3a. Configure Webhook URLs

Before running the flow, register your webhook.site URL for the events relevant to the chosen integration model using `PATCH /webhooks`. The API auto-creates the webhook config if one doesn't exist yet, so this works for first-time setup too.

```
PATCH /webhooks
Body:
{
  "data": {
    "attributes": {
      "paymentStatusUpdated": "https://webhook.site/<your-unique-id>",
      "payoutStatusUpdated": "https://webhook.site/<your-unique-id>",
      "cpVerificationStatusUpdated": "https://webhook.site/<your-unique-id>",
      "cpbaVerificationStatusUpdated": "https://webhook.site/<your-unique-id>"
    }
  }
}
```

Alternatively, webhook URLs can also be configured via the StraitsX Dashboard under Developer Tools → API Key Management.

Which events to configure per integration model:

| Event | First-Party | Third-Party | Regular | Description |
|---|---|---|---|---|
| `paymentStatusUpdated` | ✅ | ✅ | ✅ | Fires when a VBA/PayNow payment status changes |
| `payoutStatusUpdated` | ✅ | ✅ | ✅ | Fires when a payout/withdrawal status changes |
| `cpVerificationStatusUpdated` | ✅ | ✅ | — | Fires when a customer profile verification status changes |
| `cpbaVerificationStatusUpdated` | ✅ | ✅ | — | Fires when a CP bank account verification status changes |
| `virtualAccountStatusUpdated` | ✅ | ✅ | ✅ | Fires when a VBA is enabled/disabled |

### 3b. Set Up a Callback Receiver via webhook.site

Use [webhook.site](https://webhook.site) as the callback receiver — no code or infrastructure needed:

1. Open https://webhook.site — a unique URL is generated automatically (e.g., `https://webhook.site/abc-123-...`)
2. Copy the unique URL
3. Use it in the `PATCH /webhooks` call from step 3a (or paste it into the Dashboard under Developer Tools → API Key Management)
4. After running the flow, check webhook.site to inspect incoming callback payloads, headers (`Xfers-Signature`), and timing

### 3c. Callback Events During the Flow

When the sandbox flow runs, these callbacks fire at each step:

**First-Party / Third-Party Flow:**

| Flow step | Callback event fired |
|---|---|
| Verify customer profile (sandbox) | `cpVerificationStatusUpdated` |
| Verify bank account (sandbox) | `cpbaVerificationStatusUpdated` |
| Complete mock payment (sandbox) | `paymentStatusUpdated` |
| Complete mock payout (sandbox) | `payoutStatusUpdated` |

**Regular Flow:**

| Flow step | Callback event fired |
|---|---|
| Complete mock payment (sandbox) | `paymentStatusUpdated` |
| Complete mock payout (sandbox) | `payoutStatusUpdated` |

### 3d. Verify Callback Signatures

Every callback includes an `Xfers-Signature` header (HMAC-SHA256 hex digest). The generated code should verify it using the signing secret from the Dashboard.

For signature verification logic, defer to the `straitsx-webhook-verification` skill — do not generate cryptographic code from scratch.

**Required environment variable:** `STRAITSX_SIGNING_SECRET` (from Dashboard > Platform Tools > Callback URLs > Signing Key Section)

### 3e. Resend Callbacks

If a callback was missed or the listener wasn't running, use the resend endpoint:

```
POST /webhooks/{contractId}/resend
```

Or for multiple contracts at once:

```
POST /webhooks/resend
Body: { "data": { "attributes": { "contractIds": ["contract_...", "contract_..."] } } }
```

Note: Resend is primarily a production feature but useful to mention for completeness.

## Code Generation Rules

1. **Always look up the endpoint** in the OpenAPI spec ([`references/openapi-spec.json`](references/openapi-spec.json)) for the exact request body schema, required fields, and parameter formats. **Do not assume `data.attributes` nesting** — many endpoints use flat request bodies. Check the spec for each endpoint.
2. **Use sandbox base URL**: `https://api-sandbox.straitsx.com/v1`
3. **Include the API key header**: `X-XFERS-APP-API-KEY` from environment variable.
4. **Chain responses**: Extract IDs from each response to use in the next request (e.g., `customer_profile_id` from step 1 feeds into step 2).
5. **Add status checks**: After each request, check the HTTP status and print the response. Stop on errors.
6. **Use realistic test data**: Generate plausible names, registration IDs, addresses — not placeholder strings. For `nationality` and country fields, use ISO alpha-2 codes (e.g. `"SG"`, not `"SINGAPOREAN"`). For `address.street`, only use allowed characters: letters, numbers, spaces, and `/ - ? : ( ) . , ' +` (no `#`).
7. **Add comments**: Explain what each step does and what to expect.
8. **Print a summary**: At the end, print a summary of all created resources with their IDs.
9. **Webhook setup (if requested)**: Prepend the flow with a `PATCH /webhooks` call to register the user's webhook.site URL for the relevant events.
10. **Callback verification**: When the user wants to verify signatures locally (beyond webhook.site inspection), defer to the `straitsx-webhook-verification` skill's golden code. Never roll custom crypto.
11. **Rate limiting**: Insert a short delay (200–300ms) between each API call to stay within the sandbox 5 TPS rate limit. Without delays, sequential requests will trigger `STXE-9000` (429 Too Many Requests).
12. **Handle re-runs gracefully**: Before creating any resource (customer profile, bank account, VBA), check if it already exists using the corresponding GET/list endpoint and reuse it if found. Most resources cannot be deleted. Use `GET /kyc/customer_profiles?filter[registration_id]=...` for CPs, `GET /customer_profile/{id}/bank_accounts` for bank accounts, and create VBAs with a new unique `referenceId` each run.
13. **Bank account proof**: When creating a CP bank account (`POST /customer_profile/{id}/bank_accounts`), include `bank_account_proof` with a `fileUrl` pointing to a directly accessible image (png/jpg/jpeg/pdf) without query parameters. For sandbox, use a simple public image URL like `"https://www.w3.org/Graphics/PNG/nurbcup2si.png"`.

## Sandbox-Specific Notes

| Note | Detail |
|---|---|
| Sandbox API key | Must be a sandbox key, not production. Get it from Dashboard > Developer Tools in sandbox mode. |
| Mock payments | Sandbox payments don't move real money. Use the simulation endpoints to trigger payment events. |
| Verification | In sandbox, you manually set verification status via sandbox endpoints. In production, StraitsX handles verification. |
| Balance | In sandbox, collect a payment first (via VBA or PayNow mock) to get balance in your business account before testing payouts. |
| Callbacks | Sandbox sends real callbacks to your configured webhook URL. Use a tool like ngrok if testing locally. |
| Signing secret | Required for callback verification. Get it from Dashboard > Platform Tools > Callback URLs > Signing Key Section. Store as `STRAITSX_SIGNING_SECRET` env var. |
| Callback retries | Failed callbacks retry every 5 minutes, up to 20 times. Return `200 OK` from your listener to acknowledge receipt. |
| Rate limit | Sandbox enforces a 5 TPS (transactions per second) rate limit. Add a ~300ms delay between requests to avoid 429 errors. |
| Re-runs | Most resources (customer profiles, bank accounts) cannot be deleted. On re-runs, check if the resource already exists via the GET/list endpoint and reuse it instead of creating a duplicate. |
| Permissions | Sandbox API keys may need explicit scope grants. If you get `XFE6` (403), contact StraitsX support to request endpoint access. |

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `STXE-1000` on any request | Invalid or missing API key. Check `X_XFERS_APP_API_KEY` is set and is a sandbox key. |
| `XFE6` (403 Access Denied) | Your API key is missing required scopes. Contact StraitsX support at https://support.straitsx.com/hc/en-us/requests/new to request access to the relevant endpoints. Sandbox keys may need explicit scope grants. |
| `STXE-4000 Resource Object Not Verified` | Customer profile or bank account not verified. Run the sandbox verification step first. |
| `STXE-4000 Insufficient Balance` | Business account has no balance. Collect a payment first via VBA or PayNow mock flow. |
| `STXE-5000 Record Not Found` | Wrong ID passed. Check you're using the ID from the previous step's response. |
| `STXE-7000 Duplicated Idempotency Key` | Reusing an idempotency key. Generate a new UUID for each request. |
| `STXE-9000 Rate Limit Reached` (429) | Too many requests per second. The sandbox enforces a 5 TPS limit. Add a ~300ms delay between API calls. |
| `XFE16 Customer profile already exists` | A CP with the same `registrationId` already exists. Use `GET /kyc/customer_profiles?filter[registration_id]=...` to find and reuse it. |
| `XFE16 Customer profile bank account already exists` | A bank account with the same details already exists for this CP. Use `GET /customer_profile/{id}/bank_accounts` to find and reuse it. |
| `XFE16 Invalid file url provided` | The `bank_account_proof.fileUrl` is invalid. Use a direct URL to a png/jpg/jpeg/pdf file without query parameters. |
| Payout fails with "bank account not verified" | The CP bank account needs to be verified via sandbox endpoint before creating a payout. |
| `registrationType is missing` or similar field errors | The request body format is wrong. Check the OpenAPI spec — many endpoints use flat bodies, not `data.attributes` nesting. |
