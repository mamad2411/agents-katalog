---
name: stall-market-data
description: Use The Stall's live paid market-data and research capabilities over HTTP x402.
version: 3.0.0
author: IntuiTek¹ (W. Kyle Million)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Stocks, Finance, Market, Crypto, Research, x402]
    category: finance
    requires_toolsets: [terminal]
    config:
      stall.endpoint:
        default: "https://the-stall.intuitek.ai"
        description: "STALL API base URL"
---

# STALL market data

Use the hosted STALL catalog for current capability names, schemas, and prices.
Prices in cached documentation are not authoritative.

## Procedure

1. Fetch `https://the-stall.intuitek.ai/catalog`.
2. Select the capability and validate its current input schema.
3. Make an unsigned request to obtain the current x402 challenge.
4. Give the challenge to the operator's payment-capable buyer, which must check
   its own budget, network, asset, recipient, resource, and authorization window.
5. After one authorized attempt, reconcile settlement before considering any
   retry.

The helper script lists the catalog and surfaces HTTP `402` challenges. It does
not hold a wallet key or silently authorize payment.

```bash
python3 scripts/stall_client.py caps
python3 scripts/stall_client.py quote market-breadth
```

For native MCP, connect to `https://the-stall.intuitek.ai/mcp` and use an x402
MCP client for paid calls.
