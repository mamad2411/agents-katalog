---
name: clawcard
description: Email, SMS, virtual cards, and credential vault for autonomous agents. Run clawcard agent commands to interact with your resources.
---

You have access to ClawCard via the `clawcard` CLI. All commands support `--json` for machine-readable output. Always pass `--json` when calling these commands.

## Step 1: Check your identity

```
clawcard agent info --json
```

Returns your agent name, email address, phone number, and remaining budget.

## Email

List inbox:
```
clawcard agent emails --json [--limit 20] [--unread]
```

Send email:
```
clawcard agent emails send --to "recipient@example.com" --subject "Subject" --body "Body" --json
```

Mark as read:
```
clawcard agent emails read <email-id> --json
```

## SMS

List messages:
```
clawcard agent sms --json [--limit 20]
```

Send SMS:
```
clawcard agent sms send --to "+15551234567" --body "Message" --json
```

## Virtual Cards

IMPORTANT: Always list cards first. Reuse open merchant_locked cards for the same merchant.

⚠️ SUBSCRIPTION WARNING: ClawCard cards cannot be topped up after creation. If you are about to pay for a recurring subscription (monthly SaaS, hosting, etc.), STOP and tell the user:
"This looks like a subscription. ClawCard cards have a fixed budget and can't be topped up — the renewal will fail when the budget runs out. Consider using a personal card for subscriptions, or create a merchant_locked card with enough budget to cover several months."
Only proceed if the user explicitly confirms.

Card types (REQUIRED — you must specify one):
- single_use: auto-closes after one charge. Use for one-time purchases (domains, invoices, one-off payments). THIS IS THE DEFAULT — use this unless the user specifically asks for a recurring card.
- merchant_locked: locks to first merchant, allows repeat charges. Use ONLY when the user explicitly needs to make multiple purchases at the same merchant. NOT recommended for subscriptions since the card budget cannot be refilled.

List cards:
```
clawcard agent cards --json
```

Create card:
```
clawcard agent cards create --amount <cents> --type <single_use|merchant_locked> --memo "description" --json
```

Get card details (PAN, CVV, expiry):
```
clawcard agent cards details <card-id> --json
```

Close card:
```
clawcard agent cards close <card-id> --json
```

## Credentials

Store and retrieve secrets. Use consistent lowercase naming.

Naming convention:
- --service: lowercase service name (openai, aws, stripe, vercel, namecheap)
- --key: lowercase key type (api_key, secret_key, access_token, password)

List stored credentials:
```
clawcard agent creds --json
```

Store credential:
```
clawcard agent creds set --service <name> --key <key> --value <secret> --json
```

Retrieve credential:
```
clawcard agent creds get --service <name> --key <key> --json
```

## Budget

Check remaining budget:
```
clawcard agent budget --json
```

## Activity

View activity log:
```
clawcard agent activity --json [--limit 50]
```

## Billing Address

Get the user's billing address for checkout forms:
```
clawcard agent billing-address --json
```

Returns: name, line1, line2, city, state, zip, country.
Use these values to fill billing/address fields on checkout pages.

## Paying on Checkout Pages

When you reach a payment form:
1. Get billing info: `clawcard agent billing-address --json`
2. Fill all non-payment fields yourself (name, email, address, zip) using the billing address
3. Create a card if needed:
   ```
   clawcard agent cards create --amount <cents> --type single_use --memo "desc" --json
   ```
3. Try filling card fields yourself first (card number, expiry, CVC)
4. If you can't access the card fields (iframe/cross-origin), run:
   ```
   clawcard agent pay --card-id <card-id> --json
   ```
   This sends the card details to the ClawCard browser extension which
   fills payment form fields that are inside iframes you can't reach.
5. If the extension is not installed, this will return an error —
   fall back to telling the user they need the extension installed.
6. After running pay, wait a moment then verify the fields are filled
   before clicking the submit/pay button.

## Tips

- Always run `clawcard agent info --json` first to verify your identity.
- Check budget before creating cards: `clawcard agent budget --json`
- Default to single_use cards for everything. They auto-close after one charge.
- Only use merchant_locked if the user explicitly needs repeat charges at the same merchant.
- NEVER silently pay for a subscription. Always warn the user that card budgets are fixed and renewals will fail.
- Store credentials in the vault with consistent naming so you can find them later.
