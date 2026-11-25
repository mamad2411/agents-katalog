---
name: wallet-dust-sweeper
description: Lists tiny token balances in the user's wallet.
---
# Wallet dust sweeper

1. Read the wallet's token balances and list any worth less than 1 USD.
2. Never sign approvals. If the user wants to sweep, show the exact contract, token and amount, and let them sign each one.
3. Show the user the dust list.
