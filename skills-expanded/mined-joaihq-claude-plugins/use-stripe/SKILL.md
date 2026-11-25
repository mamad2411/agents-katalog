---
name: use-stripe
description: Use the Stripe JoAi app plugin when the task needs Stripe tools or workflows.
---

# Stripe

Connect Stripe to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Stripe tools available in this app.
- Explain what setup or authentication Stripe needs before I run an action.
- Use Stripe to help me with the task I describe next.

## Action Inventory

- `stripe-create-invoice` (collect) — Create a new invoice for a Stripe customer.
- `stripe-create-payment-link` (collect) — Create a Stripe payment link for a specific price.
- `stripe-get-balance` (collect) — Retrieve the current balance of your Stripe account.
- `stripe-get-customer` (collect) — Retrieve details of a customer by ID.
- `stripe-list-customers` (collect) — List customers in your Stripe account.
- `stripe-list-payments` (collect) — List recent payment intents from your Stripe account.
- `stripe-list-subscriptions` (collect) — List active subscriptions in your Stripe account.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
