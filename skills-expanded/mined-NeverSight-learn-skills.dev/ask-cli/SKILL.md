---
name: ask-cli
description: Query App StoreKit APIs using the ask CLI. Use when working with in-app purchases, subscriptions, transaction history, or when the user mentions StoreKit, in-app purchase, subscription status, or ask.
---

# App StoreKit CLI

Query App StoreKit APIs using the `ask` command-line tool.

## Prerequisites

```bash
ask --version
export ASK_ISSUER_ID='your-issuer-id'
export ASK_PRIVATE_KEY_PATH='/path/to/key.p8'
ask auth status
```

## Authentication

- Issuer ID and private key from App Store Connect
- Environment variables: `ASK_ISSUER_ID`, `ASK_PRIVATE_KEY_PATH`
- Or: `ask auth login` for interactive setup

## In-App Purchases

### Products

```bash
ask products list --app APP_ID
ask products get PRODUCT_ID --app APP_ID
ask products history --app APP_ID --product PRODUCT_ID
```

### Subscriptions

```bash
ask subscriptions list --app APP_ID
ask subscriptions get SUBSCRIPTION_ID --app APP_ID
ask subscriptions groups list --app APP_ID
ask subscriptions status --app APP_ID --customer CUSTOMER_ID
```

## Transactions

```bash
ask transactions history --app APP_ID --customer CUSTOMER_ID
ask transactions verify --app APP_ID --transaction-id TX_ID
ask transactions refund --app APP_ID --transaction-id TX_ID --reason "Customer request"
```

## Consumption & Status

```bash
ask consumption report --app APP_ID --date 2024-06-01
ask status --app APP_ID --customer CUSTOMER_ID --product PRODUCT_ID
ask entitlements --app APP_ID --customer CUSTOMER_ID
```

## Notifications & Events

```bash
ask notifications list --app APP_ID --days 7
ask events list --app APP_ID --type SUBSCRIBED --days 30
```

## Agent Best Practices

1. **Customer IDs**: Use anonymized identifiers
2. **Pagination**: Use `--cursor` for large result sets
3. **Date ranges**: Limit queries to needed timeframe
4. **Sandbox**: Use `--sandbox` for testing environment
