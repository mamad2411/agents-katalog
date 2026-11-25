---
name: plaid-finance
description: "Plaid financial data API: bank accounts, transactions, balances, income, assets, identity verification, and ACH payments. Connect to 12,000+ financial institutions for personal finance and lending apps."
tags: [plaid, banking, financial-data, open-banking, fintech, ach, zorai]
---
## Overview

Plaid connects applications to 12,000+ financial institutions for bank accounts, transactions, balances, income, identity verification, and ACH payments. Standard for fintech apps needing secure financial data access.

## Installation

```bash
uv pip install plaid-python
```

## Link Token

```python
import plaid
from plaid.api import plaid_api

config = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={"clientId": "YOUR_CLIENT_ID", "secret": "YOUR_SECRET"},
)
client = plaid_api.PlaidApi(plaid.ApiClient(config))

resp = client.link_token_create(plaid.LinkTokenCreateRequest(
    user={"client_user_id": "user-123"},
    client_name="My App",
    products=["transactions", "auth"],
    country_codes=["US"],
    language="en",
))
print(resp.link_token)
```

## Get Transactions

```python
resp = client.transactions_sync(plaid.TransactionsSyncRequest(access_token=access_token))
for tx in resp.added:
    print(f"{tx.date}: {tx.name} — ${tx.amount:.2f}")
```

## References
- [Plaid API docs](https://plaid.com/docs/api/)
- [Plaid Quickstart](https://plaid.com/docs/quickstart/)