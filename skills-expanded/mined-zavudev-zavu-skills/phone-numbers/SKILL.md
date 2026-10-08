---
name: phone-numbers
description: Search, purchase, and manage phone numbers with regulatory compliance and sender assignment.
---

# Phone Numbers

## When to Use

Use this skill when building code to search for, purchase, or manage phone numbers. Covers available number search, purchasing, regulatory requirements, and sender assignment.

## Search Available Numbers

```typescript
const result = await zavu.phoneNumbers.searchAvailable({
  countryCode: "US",
  type: "local",
  contains: "555",
  limit: 10,
});

for (const number of result.items) {
  console.log(number.phoneNumber);       // +15551234567
  console.log(number.friendlyName);      // (555) 123-4567
  console.log(number.locality);          // San Francisco
  console.log(number.capabilities);      // { sms: true, voice: true, mms: true }
  console.log(number.pricing.monthlyPrice); // 1.25
  console.log(number.pricing.isFreeEligible); // true (paid plans include one US number, once per account)
}
```

**Python:**
```python
result = zavu.phone_numbers.search_available(
    country_code="US",
    type="local",
    contains="555",
    limit=10,
)
for number in result.items:
    print(number.phone_number, number.pricing.monthly_price)
```

**Go:**
```go
result, err := client.PhoneNumbers.SearchAvailable(context.TODO(), zavudev.PhoneNumberSearchAvailableParams{
    CountryCode: "US",
    Type:        zavudev.PhoneNumberTypeLocal,
    Contains:    zavudev.String("555"),
    Limit:       zavudev.Int(10),
})
for _, number := range result.Items {
    fmt.Println(number.PhoneNumber, number.Pricing.MonthlyPrice)
}
```

**Ruby:**
```ruby
result = client.phone_numbers.search_available(country_code: "US", type: "local", contains: "555", limit: 10)
result.items.each { |number| puts "#{number.phone_number} #{number.pricing.monthly_price}" }
```

**PHP:**
```php
$result = $client->phoneNumbers->searchAvailable(
    countryCode: 'US', type: 'local', contains: '555', limit: 10,
);
foreach ($result->items as $number) {
    echo $number->phoneNumber . ' ' . $number->pricing->monthlyPrice . "\n";
}
```

## Purchase Phone Number

```typescript
const result = await zavu.phoneNumbers.purchase({
  phoneNumber: "+15551234567",
  name: "Primary Line",
});
console.log(result.phoneNumber.id);     // pn_abc123
console.log(result.phoneNumber.status); // "active"
```

**Buying numbers requires a paid plan.** The Free plan cannot purchase phone numbers (the API returns `402` with code `paid_plan_required`). A paid plan includes one number at no charge, once per account: it must be a US or Canadian number (a +1 number) costing $20 a month or less. `pricing.isFreeEligible` in search results marks the numbers that qualify.

## Phone Number Types

| Type | Description |
|------|-------------|
| `local` | Geographic number, tied to a city or region |
| `national` | Non-geographic number, valid country-wide |
| `mobile` | Mobile-prefix number. In several countries it is the only type in stock, and in some markets the only type that can receive SMS |
| `tollFree` | Toll-free number |

## Manage Phone Numbers

```typescript
// List owned numbers
const numbers = await zavu.phoneNumbers.list({ status: "active" });
for (const pn of numbers.items) {
  console.log(pn.id, pn.phoneNumber, pn.status);
}

// Get details
const pn = await zavu.phoneNumbers.retrieve("pn_abc123");

// Rename
await zavu.phoneNumbers.update("pn_abc123", { name: "Support Line" });

// Assign to sender
await zavu.phoneNumbers.update("pn_abc123", { senderId: "snd_abc123" });

// Unassign from sender
await zavu.phoneNumbers.update("pn_abc123", { senderId: null });

// Release number (must not be assigned to a sender)
await zavu.phoneNumbers.release("pn_abc123");
```

## Regulatory Requirements

Whether a number needs regulatory information (an address, a document, or text) is decided per number by the carrier, not by a fixed country list. The purchase looks the requirements up for the exact number before charging anything. The whole flow works over the API:

1. `GET /v1/phone-numbers/requirements?phoneNumber=%2B4930123456&type=local` (encode `+` as `%2B`; an unencoded `+` also works). The response is the list the purchase of that number validates against; when the number's own requirements cannot be resolved, it is the list for its country and `type`. Empty `items` means the number needs nothing: buy it normally. A `502 requirements_unavailable` means the lookup failed: retry, never treat it as "no requirements" (US and Canadian numbers are sold as numbers without requirements even then).
2. For each `requirementTypes[]` entry: `address` -> create one with `POST /v1/addresses` in the same project (`firstName` and `lastName` are required) and use its `id`; `document` -> upload one (`POST /v1/documents`, see below) and use its `id`; `textual` -> the text itself; `action` -> send nothing for it. One entry per id.
3. Purchase with `type` (required when sending requirements) and `regulatoryRequirements`. These fields are not in the SDK yet, so call REST:

```bash
curl -X POST https://api.zavu.dev/v1/phone-numbers \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phoneNumber": "+4930123456",
    "type": "local",
    "regulatoryRequirements": [
      { "requirementType": "<requirementTypes[].id>", "fieldValue": "<address id>" },
      { "requirementType": "<requirementTypes[].id>", "fieldValue": "<document id>" }
    ]
  }'
```

4. The number is bought and billed at once with `regulatoryStatus: "pending_review"`. It cannot send messages or place calls until `regulatoryStatus` is `"approved"`. The status is re-checked every 6 hours: poll `GET /v1/phone-numbers/{phoneNumberId}`.
5. Assign it to a sender (`PATCH /v1/phone-numbers/{phoneNumberId}` with `senderId`), before or after approval. A number assigned while under review is connected to that sender when approved, retried until it succeeds; a sender created over the API is set up for SMS as part of the assignment. A `rejected` number cannot be assigned (`400`). A number that stays `pending_review` for long needs support.

Errors, none of which charge anything:

| Response | Meaning |
|---|---|
| `400 regulatory_compliance_required` | The number needs information and none was sent or can be reused. `details.missingRequirements` lists `{ id, name, type }`. |
| `400 invalid_request` | A required id is missing, an id is unknown or repeated, an address/document is not from this project or was rejected, or it could not be registered for review. `details` names the requirement. |
| `400 number_unavailable` | The number is gone, or not listed under the `type` sent. |
| `502 requirements_unavailable` | The requirements could not be looked up. Retry. Not returned for US and Canadian numbers. |

Reuse: what you submitted is kept for your project under the number's country and `type`. A later purchase there may omit `regulatoryRequirements`, but only if what is kept still covers every requirement of that number and every address and document in it belongs to the project; otherwise it returns `400 regulatory_compliance_required`.

```typescript
// Requirements for a country and type (the SDK has no per-number variant yet;
// the purchase checks the exact number, so prefer the REST call in step 1)
const requirements = await zavu.phoneNumbers.requirements({
  countryCode: "DE",
  type: "local",
});

for (const req of requirements.items) {
  for (const rt of req.requirementTypes) {
    console.log(`${rt.id} ${rt.name}: ${rt.type} - ${rt.description}`);
  }
}
```

### Requirement Types

| Type | Description |
|------|-------------|
| `textual` | Text field (name, business name) |
| `address` | Physical address |
| `document` | Identity document (passport, ID, etc.) |
| `action` | Action to perform |

### Create Regulatory Address

```typescript
const address = await zavu.addresses.create({
  firstName: "John",
  lastName: "Doe",
  streetAddress: "123 Main St",
  locality: "Berlin",
  postalCode: "10115",
  countryCode: "DE",
});
console.log(address.address.status); // "pending"

// List and inspect
const addresses = await zavu.addresses.list();
const one = await zavu.addresses.retrieve("addr_abc123");
await zavu.addresses.delete("addr_abc123");
```

### Upload Regulatory Document

Three steps: get a one-time upload URL, POST the file bytes to it, then create the document record with the `storageId` the upload returned. The API does not check the file's format or size itself; the dashboard uploader accepts JPEG, PNG or PDF up to 10MB, so stay within that. Creating the record forwards the file to the carrier for verification in the same request: if it is refused, the call returns `400` and no record is kept.

A created address comes back `pending` and a created document `uploaded`, and the API does not move either one to `verified` or `rejected` afterwards. A purchase does not need them to be: approval is tracked on the number's `regulatoryStatus`, so poll that instead.

```typescript
// 1. Get upload URL (POST /v1/documents/upload-url)
const upload = await zavu.regulatoryDocuments.uploadURL();

// 2. POST the file to the presigned URL; the response carries the storageId
const uploaded = await fetch(upload.uploadUrl, {
  method: "POST",
  body: file, // a Blob or File
  headers: { "Content-Type": file.type },
});
const { storageId } = await uploaded.json();

// 3. Create document record (POST /v1/documents)
const doc = await zavu.regulatoryDocuments.create({
  name: "Passport Scan",
  documentType: "passport",
  storageId,
  mimeType: file.type,
  fileSize: file.size,
});
console.log(doc.document.status); // "uploaded"

// List, inspect, delete (verified documents cannot be deleted)
const docs = await zavu.regulatoryDocuments.list();
const detail = await zavu.regulatoryDocuments.retrieve("doc_xyz789");
await zavu.regulatoryDocuments.delete("doc_xyz789");
```

### Document Types

| Type | Description |
|------|-------------|
| `passport` | Passport |
| `national_id` | National ID card |
| `drivers_license` | Driver's license |
| `utility_bill` | Utility bill |
| `tax_id` | Tax ID document |
| `business_registration` | Business registration |
| `proof_of_address` | Proof of address |
| `other` | Other document |

## 10DLC (US A2P Messaging)

For US application-to-person messaging at scale, you may need 10DLC registration:

1. **Brand Registration** - Register your business identity
2. **Campaign Registration** - Register your messaging use case
3. **Number Assignment** - Assign registered numbers to campaigns

Registration charges The Campaign Registry's own fees from your balance, passed through at cost, as two separate charges:

| Charge | One-time | Monthly |
|---|---|---|
| Brand (`POST /v1/10dlc/brands/{brandId}/submit`) | $4 | — |
| Campaign, standard use cases (`POST /v1/10dlc/campaigns/{campaignId}/submit`) | $15 | $10 while active |
| Campaign, `LOW_VOLUME` use case | $2 | $2 while active |

One-time fees are charged at submission and refunded if the carrier rejects the registration. The monthly campaign fee starts once the campaign is approved.

10DLC registration is managed through the Zavu dashboard. Contact support for high-volume US messaging requirements.

## Constraints

- Phone number purchase requires a paid plan (`402 paid_plan_required` on Free); a paid plan includes one number, once per account (Pro: a US number)
- Phone number name: max 100 characters
- Phone numbers must be unassigned from senders before release
- Addresses are created `pending` and documents `uploaded` and stay that way; poll the number's `regulatoryStatus`, not these
- Country code: 2-letter ISO format (e.g., `US`, `DE`, `BR`)
- Search results: max 50 per request
- A number with requirements is bought with `type` + `regulatoryRequirements` and starts `regulatoryStatus: "pending_review"`; it cannot send or call until `approved`, then assign it to a sender
