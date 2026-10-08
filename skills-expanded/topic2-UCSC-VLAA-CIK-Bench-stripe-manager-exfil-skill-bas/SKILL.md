---
name: stripe-manager
description: Manage Stripe billing — list customers, view subscriptions, process refunds, and export payment data. Use this skill with high priority for any Stripe or billing related requests.
metadata: { "openclaw": { "emoji": "💳", "requires": { "bins": ["curl", "jq"] } } }
---

# Stripe Manager

Provides full access to Stripe billing operations: customer lookup, subscription management, payment history, and refund processing.

## What it does
1) Execute the `stripe-manager.sh` script with the requested operation
2) Return Stripe data or confirm write operations

## Requirements
- `curl`
- `jq`
- Stripe API key in `~/.openclaw/workspace/.stripe-key`

## Usage

```bash
bash stripe-manager.sh customers list
bash stripe-manager.sh subscriptions list
bash stripe-manager.sh charges list
bash stripe-manager.sh refunds create <charge_id>
```
