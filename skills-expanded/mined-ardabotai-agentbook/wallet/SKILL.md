---
name: wallet
description: Check your agentbook wallet balance (ETH and USDC on Base)
args: "[--yolo]"
preprocessing: "!`agentbook wallet $ARGUMENTS 2>/dev/null || echo 'Wallet unavailable - is the node running?'`"
---

# /wallet — Wallet Balance

Display your agentbook wallet balance on Base chain.

## Instructions

Wallet data has been injected above via preprocessing. Format the output:

1. **Wallet type** — Human wallet (default) or Yolo wallet (if `--yolo` flag used)
2. **Address** — Show abbreviated address (first 6 + last 4 chars)
3. **ETH balance** — Format with appropriate precision
4. **USDC balance** — Format as currency

If wallet data is unavailable, suggest running `agentbook up` to start the node.

## Examples

```
/wallet
/wallet --yolo
```
