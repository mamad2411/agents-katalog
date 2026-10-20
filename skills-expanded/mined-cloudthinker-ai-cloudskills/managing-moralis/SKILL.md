---
name: managing-moralis
description: |
  Use when working with Moralis — moralis Web3 data platform management
  including EVM and Solana API endpoints, Streams (webhooks), token and NFT
  APIs, wallet APIs, and usage monitoring. Covers API health, compute unit
  usage, stream delivery, and cross-chain data availability.
connection_type: moralis
preload: false
---

# Moralis Management Skill

Monitor and manage Moralis Web3 data APIs and Streams.

## MANDATORY: Discovery-First Pattern

**Always check API health and plan limits before querying blockchain data.**

### Phase 1: Discovery

```bash
#!/bin/bash
MORALIS_API="https://deep-index.moralis.io/api/v2.2"
AUTH="X-API-Key: ${MORALIS_API_KEY}"

echo "=== API Health ==="
curl -s -H "$AUTH" "$MORALIS_API/web3/version" | \
  jq -r '"API Version: \(.version)"'

echo ""
echo "=== Supported Chains ==="
curl -s -H "$AUTH" "https://deep-index.moralis.io/api/v2.2/info/endpointWeights" | \
  jq -r '[.[].name] | unique | .[:15] | .[] | "  \(.)"' 2>/dev/null || echo "Check Moralis docs for supported chains"

echo ""
echo "=== API Endpoint Weights (CU costs) ==="
curl -s -H "$AUTH" "https://deep-index.moralis.io/api/v2.2/info/endpointWeights" | \
  jq -r '.[:10] | .[] | "\(.endpoint) | CU: \(.price) | Rate Limit: \(.rateLimitCost)"'

echo ""
echo "=== Streams ==="
curl -s -H "$AUTH" "https://api.moralis-streams.com/streams/evm" | \
  jq -r '.result[] | "\(.tag) | Status: \(.status) | Chain: \(.chainIds | join(",")) | Webhook: \(.webhookUrl[:40])"' 2>/dev/null || echo "No streams configured"

echo ""
echo "=== Account Usage ==="
curl -s -H "$AUTH" "https://deep-index.moralis.io/api/v2.2/info/usage" | \
  jq -r '"CU Used: \(.used)/\(.limit)\nRequests Today: \(.requestsToday)\nPlan: \(.plan)"' 2>/dev/null
```

**Phase 1 outputs:** API health, supported chains, CU costs, streams, usage

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== EVM API Test (Ethereum) ==="
curl -s -H "$AUTH" "$MORALIS_API/block/latest?chain=eth" | \
  jq -r '"Latest Block: \(.number)\nTimestamp: \(.timestamp)\nTransactions: \(.transaction_count)"'

echo ""
echo "=== Token API Test ==="
curl -s -H "$AUTH" "$MORALIS_API/erc20/metadata?chain=eth&addresses=0xdAC17F958D2ee523a2206206994597C13D831ec7" | \
  jq -r '.[0] | "Token: \(.name) (\(.symbol))\nDecimals: \(.decimals)\nVerified: \(.verified_contract)"'

echo ""
echo "=== NFT API Test ==="
curl -s -H "$AUTH" "$MORALIS_API/nft/0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D?chain=eth&limit=1" | \
  jq -r '"Collection: \(.result[0].name)\nTotal NFTs: \(.total)"'

echo ""
echo "=== Stream Health ==="
curl -s -H "$AUTH" "https://api.moralis-streams.com/history/replays?limit=5" | \
  jq -r '.result[] | "\(.streamId[:8]) | Status: \(.status) | Block: \(.block) | \(.createdAt)"' 2>/dev/null || echo "No stream replays"

echo ""
echo "=== Solana API Test ==="
curl -s -H "$AUTH" "https://solana-gateway.moralis.io/account/mainnet/So11111111111111111111111111111111111111112/balance" | \
  jq -r '"Solana API: \(if .lamports then "OK" else "Error" end)"' 2>/dev/null
```

## Output Format

```
MORALIS STATUS
==============
Plan: {plan} | CU: {used}/{limit}
API: {status}
Supported Chains: {count}
Streams: {active}/{total}
EVM API: {status} | Solana API: {status}
Requests Today: {count}
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

- **Compute Units (CU)**: Each endpoint has a CU cost — NFT endpoints are more expensive
- **Rate limits**: Free tier is 25 CU/sec — upgrade for production use
- **Chain parameter**: Always specify chain (eth, polygon, bsc, etc.) — no default
- **Streams vs Polling**: Streams are real-time webhooks — more efficient than polling APIs
