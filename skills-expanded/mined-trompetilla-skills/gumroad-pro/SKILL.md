---
name: gumroad-pro
description: "Comprehensive Gumroad merchant management including product catalogs, sales intelligence, recurring subscription oversight, license key management, and financial payout tracking. Use when you need to: (1) Check sales volume or revenue reports, (2) Manage product availability and pricing, (3) Create or edit discount offer codes, (4) Verify or rotate license keys, (5) Audit payout history and upcoming deposits, or (6) Configure automated webhooks for store events."
---

# Gumroad Pro

Advanced merchant dashboard for managing your digital empire. Supports both interactive UI (buttons/numbered lists) and direct CLI commands.

## Setup

The skill requires a Gumroad Access Token. This can be stored as either `GUMROAD_ACCESS_TOKEN` in the environment or as `apiKey` (which maps to `API_KEY`) in the skill configuration.

### Option 1 (Recommended): Simple API Key
```json
"skills": {
  "entries": {
    "gumroad-pro": {
      "apiKey": "your_token_here"
    }
  }
}
```

### Option 2: Environment Variable
```json
"skills": {
  "entries": {
    "gumroad-pro": {
      "env": {
        "GUMROAD_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Commands

### Interactive Dashboard
- `/gp`, `/gumroad`, `/gumroad-pro`, or `/gumroad_pro`: Opens the main control hub. This uses an adaptive UI that provides buttons on supported platforms (Telegram, Discord) and numbered lists on others (WhatsApp, Signal).

### Technical Reference (Core CLI)

#### Product Management
- `gp products list`: List all assets with IDs and stats.
- `gp products details --id <id>`: View full specifications and metadata.
- `gp products create --name <name> --price <cents> [--description <text>] [--url <custom_link>] [--taxable <bool_string>] [--currency <iso>]`
- `gp products update --id <id> [--name <name>] [--price <cents>] [--description <text>] [--url <link>]`
- `gp products enable/disable --id <id>`: Toggle store visibility.
- `gp products delete --id <id>`: Permanent removal.

#### Sales & Revenue Intelligence
- `gp sales list [--after YYYY-MM-DD] [--before YYYY-MM-DD] [--page <key>] [--product_id <id>] [--email <addr>] [--order_id <id>]`
- `gp sales details --id <id>`: Customer data, custom fields, and shipping status.
- `gp sales refund --id <id> [--amount <cents>]`: Default is full refund.
- `gp sales resend-receipt --id <id>`: Resends the purchase receipt.
- `gp sales mark-shipped --id <id> --tracking <url_or_number>`

#### License & Subscriber Deep-Dive
- `gp licenses verify/enable/decrement/rotate --product <id> --key <key>`
- `gp subscribers list --product <id>`: List all recurring subscribers.
- `gp subscribers details --id <sub_id>`: Check subscription health and billing.

#### Revenue & Payout Logistics
- `gp payouts list [--after YYYY-MM-DD] [--before YYYY-MM-DD] [--page <key>] [--upcoming <false|true>]`
- `gp payouts details --id <id>`: Processing timestamps and processor info.

#### Product Customization (Variants & Categories)
- `gp variant-categories list/create/update/delete --product <id> [--title <name>] [--id <cat_id>]`
- `gp variants list/create/update/delete --product <id> --category <cat_id> [--name <name>] [--price <diff_cents>] [--limit <max>] [--id <var_id>]`

#### Custom Checkout Fields
- `gp custom-fields list/create/update/delete --product <id> [--name <name>] [--required <true|false>]`

#### Automation (Webhooks)
- `gp subscriptions list [--type <event>]`
- `gp subscriptions create --url <url> --type <event_type>`
- `gp subscriptions delete --id <id>`

## LLM Guidance & Operational Protocols

### CLI Execution Protocol
- **Shell Pattern**: Use `node skills/gumroad-pro/scripts/gumroad-pro.js <command> <subcommand> [flags]`.
- **Flag Sensitivity**: Boolean flags (like `--upcoming` or `--required`) must be passed as strings (e.g., `"false"` or `"true"`).
- **Price Handling**: All price inputs are in **cents** (e.g., $10.00 = `1000`). Always clarify this during creation workflows.

### User Interface Interaction
- **CRITICAL:** On Telegram and Discord, you **MUST** use the `message` tool with `buttons` for the Main Menu and all sub-menus. **NEVER** output a raw text list or CLI output directly to the user on these platforms.
- **Adaptive Rendering**: Use `buttons` + `edit` for Telegram/WebChat; `numbered lists` + `send` for WhatsApp/Signal.
- **State Capture**: Multi-step inputs (e.g., creating a discount) should use the `pending_input.json` state pattern in `handler.js`.
- **Proactive Verifications**: When viewing sales, if a `license_key` is present, always offer a "Check License" action.

### Safety & Integrity
- **Confirmation Requirement**: Mandatory "Ask" state before `delete` or `refund`.
- **ID Integrity**: Always use IDs exactly as returned by `list` commands; they are case-sensitive.
- **Error Transparency**: If a `502` or `401` occurs, advise the user to check their `GUMROAD_ACCESS_TOKEN`.
