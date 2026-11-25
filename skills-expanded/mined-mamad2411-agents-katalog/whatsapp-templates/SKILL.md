---
name: whatsapp-templates
description: Create WhatsApp message templates, submit for Meta approval, and send template messages with variables.
---

# WhatsApp Templates

## When to Use

Use this skill when building code to create, manage, or send WhatsApp template messages. Templates are required to initiate conversations outside the 24-hour window.

## When Templates Are Required

```
Has user messaged you in the last 24 hours?
  -> YES: Send free-form message (text, image, buttons, etc.)
  -> NO: Must use template message
Need to send bulk/broadcast messages?
  -> YES: Use template (recommended for consistency)
Want proactive outbound notifications?
  -> YES: Must use template
```

## Template Categories

| Category | Use Case | Examples |
|----------|----------|---------|
| `UTILITY` | Transactional updates | Order confirmations, shipping updates, appointment reminders |
| `MARKETING` | Promotional content | Sales, offers, product announcements |
| `AUTHENTICATION` | OTP/verification codes | Login codes, 2FA, password resets |

## Create Template

```typescript
const template = await zavu.templates.create({
  name: "order_confirmation",
  language: "en",
  body: "Hi {{1}}, your order {{2}} has been confirmed and will ship within 24 hours.",
  whatsappCategory: "UTILITY",
  variables: ["customer_name", "order_id"],
});
console.log(template.id); // tpl_xxx
```

**Python:**
```python
template = zavu.templates.create(
    name="order_confirmation",
    language="en",
    body="Hi {{1}}, your order {{2}} has been confirmed and will ship within 24 hours.",
    whatsapp_category="UTILITY",
    variables=["customer_name", "order_id"],
)
```

**Go:**
```go
template, err := client.Templates.Create(context.TODO(), zavudev.TemplateCreateParams{
    Name:             zavudev.String("order_confirmation"),
    Language:         zavudev.String("en"),
    Body:             zavudev.String("Hi {{1}}, your order {{2}} has been confirmed and will ship within 24 hours."),
    WhatsappCategory: zavudev.String("UTILITY"),
    Variables:        []string{"customer_name", "order_id"},
})
```

**Ruby:**
```ruby
template = client.templates.create(
    name: "order_confirmation",
    language: "en",
    body: "Hi {{1}}, your order {{2}} has been confirmed and will ship within 24 hours.",
    whatsapp_category: "UTILITY",
    variables: ["customer_name", "order_id"],
)
```

**PHP:**
```php
$template = $client->templates->create([
    'name' => 'order_confirmation',
    'language' => 'en',
    'body' => 'Hi {{1}}, your order {{2}} has been confirmed and will ship within 24 hours.',
    'whatsappCategory' => 'UTILITY',
    'variables' => ['customer_name', 'order_id'],
]);
```

## Channel-Specific Bodies

Templates can have different bodies per channel. The default `body` is used for WhatsApp; SMS, Telegram, and Instagram fall back to `body` if no channel-specific body is set.

```typescript
const template = await zavu.templates.create({
  name: "order_confirmation",
  language: "en",
  body: "Hi {{1}}, your order {{2}} has been confirmed and will ship within 24 hours.",
  smsBody: "Order {{2}} confirmed. Ships in 24h.",       // SMS fallback
  telegramBody: "✅ Order {{2}} confirmed for {{1}}.",    // Telegram-specific
  instagramBody: "Order {{2}} confirmed!",               // Instagram-specific
  whatsappCategory: "UTILITY",
  variables: ["customer_name", "order_id"],
});
```

`whatsappCategory` only applies to the WhatsApp `body`. Channel-specific bodies don't require a category.

## Template with Buttons

```typescript
// Quick reply buttons
const template = await zavu.templates.create({
  name: "feedback_request",
  language: "en",
  body: "Hi {{1}}, how was your experience with order {{2}}?",
  whatsappCategory: "MARKETING",
  variables: ["customer_name", "order_id"],
  buttons: [
    { type: "quick_reply", text: "Great!" },
    { type: "quick_reply", text: "Could be better" },
  ],
});

// URL button
const template = await zavu.templates.create({
  name: "track_order",
  language: "en",
  body: "Hi {{1}}, your order {{2}} has shipped!",
  whatsappCategory: "UTILITY",
  variables: ["customer_name", "order_id"],
  buttons: [
    { type: "url", text: "Track Order", url: "https://example.com/track/{{1}}" },
  ],
});

// Phone button
const template = await zavu.templates.create({
  name: "contact_support",
  language: "en",
  body: "Need help? Call our support team.",
  whatsappCategory: "UTILITY",
  buttons: [
    { type: "phone", text: "Call Support", phoneNumber: "+14155551234" },
  ],
});

// Contact info request button — asks the recipient to share their phone number.
// Label is fixed by WhatsApp ("Share Contact Info"), so `text` is not required.
// Useful for contacts who adopted a WhatsApp username (known only by BSUID).
const template = await zavu.templates.create({
  name: "callback_request",
  language: "en",
  body: "Hi {{1}}, we need a phone number to schedule your callback.",
  whatsappCategory: "UTILITY",
  variables: ["customer_name"],
  buttons: [
    { type: "request_contact_info" },
  ],
});
```

## OTP Authentication Templates

```typescript
// Copy code button
const template = await zavu.templates.create({
  name: "login_otp",
  language: "en",
  body: "Your verification code is {{1}}. Do not share this code.",
  whatsappCategory: "AUTHENTICATION",
  variables: ["otp_code"],
  addSecurityRecommendation: true,
  codeExpirationMinutes: 5,
  buttons: [
    { type: "otp", text: "Copy Code", otpType: "COPY_CODE" },
  ],
});

// One-tap autofill (Android)
const template = await zavu.templates.create({
  name: "login_otp_autofill",
  language: "en",
  body: "Your verification code is {{1}}.",
  whatsappCategory: "AUTHENTICATION",
  variables: ["otp_code"],
  addSecurityRecommendation: true,
  codeExpirationMinutes: 10,
  buttons: [
    {
      type: "otp",
      text: "Autofill",
      otpType: "ONE_TAP",
      packageName: "com.example.app",
      signatureHash: "abc123hash",
    },
  ],
});
```

## Submit for Meta Approval

Templates must be approved by Meta before use:

```typescript
// Submit template for review
const submitted = await zavu.templates.submit({
  templateId: "tpl_abc123",
  senderId: "snd_abc123",
  category: "UTILITY",
});
console.log(submitted.status); // "pending"
```

Track approval via webhooks (`template.status_changed` event) or polling:

```typescript
const template = await zavu.templates.get({ templateId: "tpl_abc123" });
console.log(template.status); // draft | pending | approved | rejected
```

## Category Is Meta's, Not Yours

The category you submit is a request. Meta decides the one that counts, and it
can reassign it — most often `UTILITY` to `MARKETING` — either at approval or
months later on a template that is already live. That reassignment changes what
every send on that template costs.

`template.category` reports the category **Meta currently assigns**, so read it
rather than assuming the one you submitted is still in force:

```typescript
const template = await zavu.templates.get({ templateId: "tpl_abc123" });
console.log(template.category); // UTILITY | MARKETING | AUTHENTICATION
```

A recategorization arrives as a `template.status_changed` webhook carrying
`data.category`. It fires even when the approval status did not move, so a
recategorization shows up as an event whose `previousStatus` and `currentStatus`
are identical — branch on `category`, not only on `currentStatus`:

```typescript
if (event.type === "template.status_changed") {
  const { templateId, currentStatus, category } = event.data;
  if (category !== myStoredCategory(templateId)) {
    // Meta moved the billing category. Reprice before the next send.
  }
}
```

To reconcile templates that drifted before you were listening, run
`POST /v1/templates/sync` — see below.

## Sync Templates from WhatsApp

A template created outside Zavu — in Meta Business Manager, or by another tool —
does not exist in Zavu until you import it. If a `template.status_changed`
webhook is missed, a template stays `pending` forever. And a template Meta
recategorized while nothing was listening keeps reporting its old category.
`POST /v1/templates/sync` fixes all three: it imports Meta templates Zavu does
not have (or links them to an existing template with the same name) and
refreshes both the status and the category of the ones it does.

A template whose category changed but whose status did not is still counted in
`updated` — that is the case worth running this for.

Not generated in the SDK yet — call it over REST:

```bash
# Sync every WhatsApp sender in the project
curl -X POST https://api.zavu.dev/v1/templates/sync \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'

# Or scope it to one sender's WhatsApp Business Account
curl -X POST https://api.zavu.dev/v1/templates/sync \
  -H "Authorization: Bearer $ZAVU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"senderId": "snd_abc123"}'
```

```json
{
  "accountsSynced": 1,
  "imported": 2,
  "linked": 1,
  "updated": 3,
  "skipped": 12,
  "errors": []
}
```

- The call is synchronous: it waits for Meta, so it can take a few seconds per
  account. List templates right after to see the result.
- `skipped` counts Meta templates left alone — already linked, or rejected /
  disabled on Meta (those are never imported).
- A non-empty `errors` with a 200 means one account failed; the rest still synced.
- Returns 400 when no sender in the project has a WhatsApp Business Account.

## Send Template Message

```typescript
await zavu.messages.send({
  to: "+14155551234",
  messageType: "template",
  content: {
    templateId: "tpl_abc123",
    templateVariables: { "1": "John", "2": "ORD-12345" },
  },
});
```

**Python:**
```python
zavu.messages.send(
    to="+14155551234",
    message_type="template",
    content={
        "templateId": "tpl_abc123",
        "templateVariables": {"1": "John", "2": "ORD-12345"},
    },
)
```

## Template Lifecycle

```
draft -> pending (submitted to Meta) -> approved (ready to use)
                                     -> rejected (edit and resubmit)
```

## Other Operations

```typescript
// List templates
const templates = await zavu.templates.list({ limit: 50 });
for (const tpl of templates.items) {
  console.log(tpl.id, tpl.name, tpl.status);
}

// Get template
const tpl = await zavu.templates.get({ templateId: "tpl_abc123" });

// Delete template (draft only)
await zavu.templates.delete({ templateId: "tpl_abc123" });
```

## Constraints

- Template names: lowercase, underscores only (e.g., `order_confirmation`)
- Variables use positional format: `{{1}}`, `{{2}}`, `{{3}}`
- Max 3 buttons per template
- Button text: max 25 characters (not used for `request_contact_info` — WhatsApp fixes its label)
- OTP `ONE_TAP` requires Android `packageName` and `signatureHash`
- `addSecurityRecommendation` only for AUTHENTICATION templates
- `codeExpirationMinutes`: 1-90, only for AUTHENTICATION
- Meta approval typically takes minutes to hours, but can take up to 24h
- Rejected templates can be edited and resubmitted
