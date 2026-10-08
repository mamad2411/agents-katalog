---
name: contacts-management
description: Manage multi-channel contacts with channel operations, search, merging, phone introspection, and email validation.
---

# Contacts Management

## When to Use

Use this skill when building code to create, update, or manage contacts and their communication channels. Covers the multi-channel contact model, search, merge operations, phone number introspection, and email address validation.

## Contact Model

Contacts are multi-channel: one contact can have multiple channels (SMS, WhatsApp, Email, Telegram, Instagram, Messenger, Voice), each with its own identifier and delivery metrics. Top-level fields expose primary identifiers for quick access.

```
Contact (John Doe)
├── primaryPhone: +14155551234           (E.164)
├── primaryEmail: john@example.com
├── profileName: "John D."               (WhatsApp profile name, if available)
├── verified: true
├── countryCode: "US"
└── Channels:
    ├── SMS: +14155551234 (primary)
    ├── WhatsApp: +14155551234 (primary)
    ├── Email: john@example.com (primary)
    ├── Email: john.work@company.com (label: "work")
    ├── Telegram: @johndoe
    └── Voice: +14155551234
```

> **Note:** The legacy `phoneNumber` field on Contact is deprecated — use `primaryPhone` instead.

Valid contact channel types: `sms`, `whatsapp`, `email`, `telegram`, `instagram`, `messenger`, `voice` (note: `auto` and `sms_oneway` are message-send routing options, not contact channel types).

## Auto-Creation

Contacts are automatically created when you send a message to a new recipient. No explicit creation needed for basic messaging.

## Create Contact

```typescript
const contact = await zavu.contacts.create({
  displayName: "John Doe",
  channels: [
    { channel: "sms", identifier: "+14155551234", isPrimary: true },
    { channel: "whatsapp", identifier: "+14155551234", isPrimary: true },
    { channel: "email", identifier: "john@example.com", isPrimary: true },
  ],
  metadata: { source: "import", plan: "enterprise" },
});
console.log(contact.id);
```

**Python:**
```python
contact = zavu.contacts.create(
    display_name="John Doe",
    channels=[
        {"channel": "sms", "identifier": "+14155551234", "isPrimary": True},
        {"channel": "email", "identifier": "john@example.com", "isPrimary": True},
    ],
)
```

**Go:**
```go
contact, err := client.Contacts.Create(context.TODO(), zavudev.ContactCreateParams{
    DisplayName: zavudev.String("John Doe"),
    Channels: []zavudev.ContactChannelParam{
        {Channel: "sms", Identifier: "+14155551234", IsPrimary: zavudev.Bool(true)},
        {Channel: "email", Identifier: "john@example.com", IsPrimary: zavudev.Bool(true)},
    },
})
```

**Ruby:**
```ruby
contact = client.contacts.create(
    display_name: "John Doe",
    channels: [
        { channel: "sms", identifier: "+14155551234", is_primary: true },
        { channel: "email", identifier: "john@example.com", is_primary: true },
    ],
)
```

**PHP:**
```php
$contact = $client->contacts->create([
    'displayName' => 'John Doe',
    'channels' => [
        ['channel' => 'sms', 'identifier' => '+14155551234', 'isPrimary' => true],
        ['channel' => 'email', 'identifier' => 'john@example.com', 'isPrimary' => true],
    ],
]);
```

## Get & List Contacts

```typescript
// Get by ID
const contact = await zavu.contacts.get({ contactId: "ct_abc123" });

// Get by phone number
const contact = await zavu.contacts.getByPhone({
  phoneNumber: "+14155551234",
});

// List with filters
let cursor: string | undefined;
do {
  const result = await zavu.contacts.list({
    phoneNumber: "+14155551234",
    limit: 50,
    cursor,
  });
  for (const contact of result.items) {
    console.log(contact.id, contact.displayName, contact.availableChannels);
  }
  cursor = result.nextCursor ?? undefined;
} while (cursor);

// Search by name, phone, or email
const found = await zavu.contacts.list({ search: "marta", limit: 25 });
```

`search` is case- and accent-insensitive, and matches a trailing fragment of a
phone number, so `5551234` finds `+14155551234`. It matches the contact's
`displayName` and WhatsApp profile name as well as its identifiers.

Contacts created automatically from an inbound message have no `displayName`,
so they are only findable by their identifier until you name one — see
**Update Contact**.

Two things to know before paginating a search: results come back in relevance
order rather than newest-first, and `cursor` is opaque in both modes. Pass back
exactly what the previous response returned, and start a fresh pagination run
whenever the search term changes.

## Tags

Flat labels on a contact, for grouping an audience you send to more than once.
Many-to-many, no hierarchy, no colours.

```typescript
// Contacts carrying a tag
const { items } = await zavu.contacts.list({ tag: "vip" });

// Repeat the parameter for AND — carrying BOTH tags, not either
// GET /v1/contacts?tag=vip&tag=chile
```

Tags are matched by name, case-insensitively. An unknown tag returns `400`
rather than being ignored: a typo that silently matched every contact would be a
worse answer than an error.

Creating, renaming and assigning tags is done in the dashboard. There is no tag
CRUD in the API yet — do not tell a user they can create one from code.

## Channel Operations

```typescript
// Add channel
const channel = await zavu.contacts.channels.add({
  contactId: "ct_abc123",
  channel: "email",
  identifier: "john.work@company.com",
  label: "work",       // optional
  countryCode: "US",   // optional, 2-letter ISO
});

// Update channel
await zavu.contacts.channels.update({
  contactId: "ct_abc123",
  channelId: "ch_xyz789",
  label: "personal",
  verified: true,
});

// Set as primary
await zavu.contacts.channels.setPrimary({
  contactId: "ct_abc123",
  channelId: "ch_xyz789",
});

// Remove channel (cannot remove the last channel)
await zavu.contacts.channels.remove({
  contactId: "ct_abc123",
  channelId: "ch_xyz789",
});
```

## Update Contact

Updatable fields: `displayName`, `defaultChannel`, `metadata`.

```typescript
await zavu.contacts.update({
  contactId: "ct_abc123",
  displayName: "John Doe",
  defaultChannel: "whatsapp",
  metadata: { plan: "premium", region: "US" },
});

// Clear a field by passing null
await zavu.contacts.update({
  contactId: "ct_abc123",
  displayName: null,      // falls back to the contact's identifier
  defaultChannel: null,
});
```

Contacts created automatically from an inbound message have no `displayName` —
they show as their phone number or email until you set one. Naming them is what
makes them findable by name via `contacts.list({ search })`.

To change a contact's phone number or email address, add or remove a channel
(see **Channel Operations**) rather than updating the contact.

## Merge Contacts

Merge one contact into another. Every channel on the source moves to the target,
the target's primary phone and email are recomputed, and the source is marked as
merged and stops appearing in listings.

```typescript
const merged = await zavu.contacts.merge({
  contactId: "ct_target123",        // survives
  sourceContactId: "ct_source456",  // absorbed
});
console.log("Merged channels:", merged.channels.length);
```

Merging is not reversible — check the two contacts are the same person first.

**Zavu does not detect duplicates for you.** There is no merge suggestion: decide
which contacts to merge from your own data. A practical way to find candidates is
to list contacts and group them by a shared identifier or a normalized name.

## Phone Introspection

Validate phone numbers and check carrier info:

```typescript
const result = await zavu.introspect.phone({
  phoneNumber: "+14155551234",
});
console.log(result.validNumber);      // true
console.log(result.countryCode);       // "US"
console.log(result.nationalFormat);    // "(415) 555-1234"
console.log(result.lineType);         // "mobile" | "landline" | "voip" | "toll_free"
console.log(result.carrier?.name);    // "Verizon Wireless"
console.log(result.availableChannels); // ["sms", "whatsapp", "voice"]
```

**Python:**
```python
result = zavu.introspect.phone(phone_number="+14155551234")
print(result.valid_number)
print(result.line_type)
print(result.carrier.name if result.carrier else "Unknown")
```

**Go:**
```go
result, err := client.Introspect.Phone(context.TODO(), zavudev.PhoneIntrospectionParams{
    PhoneNumber: zavudev.String("+14155551234"),
})
fmt.Println(result.ValidNumber, result.LineType, result.Carrier.Name)
```

**Ruby:**
```ruby
result = client.introspect.phone(phone_number: "+14155551234")
puts result.valid_number, result.line_type, result.carrier&.name
```

**PHP:**
```php
$result = $client->introspect->phone(['phoneNumber' => '+14155551234']);
echo $result->validNumber, $result->lineType, $result->carrier?->name;
```

## Email Validation

Validate email addresses before sending to keep your bounce rate low. Catches invalid syntax, dead domains (no MX/A records), disposable inboxes, role-based addresses (`info@`, `contacto@`, `sales@`), and addresses already on your project's suppression list. No SMTP mailbox probe is performed: `deliverable` means no negative signal was found, not a delivery guarantee.

Not yet generated in the SDKs — use the REST endpoint directly:

```bash
# Single address
curl -X POST https://api.zavu.dev/v1/introspect/email \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "maria@example.com"}'

# Batch (max 100 per request)
curl -X POST https://api.zavu.dev/v1/introspect/email \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["maria@example.com", "info@deaddomain.example", "not-an-email"]}'
```

Response:

```json
{
  "results": [
    {
      "email": "maria@example.com",
      "normalized": "maria@example.com",
      "domain": "example.com",
      "verdict": "deliverable",
      "reasons": []
    },
    {
      "email": "info@deaddomain.example",
      "normalized": "info@deaddomain.example",
      "domain": "deaddomain.example",
      "verdict": "undeliverable",
      "reasons": ["domain_not_found", "role_address"]
    },
    {
      "email": "not-an-email",
      "normalized": null,
      "domain": null,
      "verdict": "undeliverable",
      "reasons": ["invalid_syntax"]
    }
  ],
  "summary": { "total": 3, "deliverable": 1, "risky": 0, "undeliverable": 2 }
}
```

Verdicts:

- `deliverable` — no negative signal found.
- `risky` — sendable, but a signal predicts elevated bounce/complaint odds: `role_address`, `disposable_domain`, `domain_no_mx` (domain resolves but has no MX records), or `suppressed_soft_bounce`.
- `undeliverable` — drop these: `invalid_syntax`, `domain_not_found`, or suppressed after a hard bounce/complaint (`suppressed_hard_bounce`, `suppressed_complaint`, `suppressed_manual`, `suppressed_unsubscribe`).

Typical flow before a broadcast: validate the list, drop `undeliverable`, review `risky`, then add only the clean recipients.

## Constraints

- Max 20 channels per contact
- Channel labels: max 50 characters
- Display name: max 200 characters
- Cannot remove the last channel from a contact
- Cannot merge a contact with itself
- Phone numbers must be E.164 format
- Duplicate identifiers across contacts are rejected (use merge instead)
