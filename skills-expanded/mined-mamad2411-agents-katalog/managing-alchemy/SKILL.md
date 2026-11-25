---
name: managing-alchemy
description: |
  Use when working with Alchemy — alchemy Web3 development platform management
  including app configuration, RPC endpoint health, webhook notifications, NFT
  API usage, Enhanced APIs, gas optimization, and usage analytics. Covers
  request volume monitoring, error rates, compute unit consumption, and
  multi-chain endpoint health.
connection_type: alchemy
preload: false
---

# Alchemy Management Skill

Monitor and manage Alchemy Web3 infrastructure and blockchain APIs.

## MANDATORY: Discovery-First Pattern

**Always discover apps and supported chains before querying usage or RPC endpoints.**

### Phase 1: Discovery

```bash
#!/bin/bash
ALCHEMY_API="https://dashboard.alchemy.com/api"
AUTH="Authorization: Bearer ${ALCHEMY_AUTH_TOKEN}"

echo "=== Team Info ==="
curl -s -H "$AUTH" "$ALCHEMY_API/team" | \
  jq -r '"Team: \(.name)\nPlan: \(.plan)\nCompute Units: \(.computeUnits.used)/\(.computeUnits.limit)"' 2>/dev/null || echo "Use dashboard API token"

echo ""
echo "=== Apps ==="
curl -s -H "$AUTH" "$ALCHEMY_API/apps" | \
  jq -r '.[] | "\(.name) | Network: \(.network) | Chain: \(.chain) | Created: \(.createdAt)"' 2>/dev/null

echo ""
echo "=== RPC Endpoint Health ==="
for network in eth-mainnet eth-sepolia polygon-mainnet arb-mainnet opt-mainnet base-mainnet; do
  status=$(curl -s -X POST "https://$network.g.alchemy.com/v2/${ALCHEMY_API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | \
    jq -r 'if .result then "OK (block: \(.result))" else "ERROR: \(.error.message // "unreachable")" end')
  echo "$network: $status"
done

echo ""
echo "=== Webhooks ==="
curl -s -H "$AUTH" "$ALCHEMY_API/webhooks" | \
  jq -r '.[] | "\(.id) | Type: \(.type) | Network: \(.network) | Active: \(.isActive)"' 2>/dev/null
```

**Phase 1 outputs:** Team info, apps, endpoint health across chains, webhooks

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Latest Block & Gas (Ethereum) ==="
curl -s -X POST "https://eth-mainnet.g.alchemy.com/v2/${ALCHEMY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}' | \
  jq -r '"Gas Price: \(.result | ltrimstr("0x") | explode | length) (hex: \(.result))"'

echo ""
echo "=== Pending Transactions Sample ==="
curl -s -X POST "https://eth-mainnet.g.alchemy.com/v2/${ALCHEMY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"alchemy_pendingTransactions","params":[{"toAddress":[],"hashesOnly":true}],"id":1}' | \
  jq -r '"Pending tx sample: \(.result | length // 0)"' 2>/dev/null

echo ""
echo "=== NFT API Test ==="
curl -s "https://eth-mainnet.g.alchemy.com/nft/v3/${ALCHEMY_API_KEY}/getNFTsForOwner?owner=vitalik.eth&pageSize=1" | \
  jq -r '"NFT API: \(if .ownedNfts then "OK (\(.totalCount) NFTs)" else "Error" end)"'

echo ""
echo "=== Compute Unit Usage ==="
curl -s -H "$AUTH" "$ALCHEMY_API/usage" | \
  jq -r '"Daily CU Used: \(.daily.used)/\(.daily.limit)\nMonthly CU Used: \(.monthly.used)/\(.monthly.limit)"' 2>/dev/null || echo "Check usage in Alchemy Dashboard"

echo ""
echo "=== Recent Errors ==="
curl -s -H "$AUTH" "$ALCHEMY_API/errors?limit=5" | \
  jq -r '.[] | "\(.timestamp) | Method: \(.method) | Code: \(.errorCode) | \(.message[:50])"' 2>/dev/null
```

## Output Format

```
ALCHEMY STATUS
==============
Plan: {plan} | CU: {used}/{limit}
Apps: {count}
Chains: {list_of_active_chains}
Endpoint Health: {healthy}/{total} OK
Webhooks: {active}/{total}
Gas (ETH): {gwei} gwei
Issues: {list_of_warnings}
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Compute Units (CU)**: Different methods cost different CUs — eth_call is 26, eth_blockNumber is 10
- **Rate limits**: Vary by plan — free tier is 330 CU/sec
- **Chain-specific endpoints**: Each chain has its own URL — do not mix
- **Enhanced APIs**: Alchemy-specific methods (alchemy_*) not available on other providers
