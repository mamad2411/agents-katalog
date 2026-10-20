---
name: managing-infura
description: |
  Use when working with Infura — infura Web3 infrastructure management including
  project configuration, RPC endpoint health, IPFS gateway, usage statistics,
  and multi-chain support. Covers request volume monitoring, error tracking,
  bandwidth usage, and API key security across Ethereum, Polygon, Arbitrum, and
  other networks.
connection_type: infura
preload: false
---

# Infura Management Skill

Monitor and manage Infura blockchain infrastructure and IPFS services.

## MANDATORY: Discovery-First Pattern

**Always check endpoint health and project settings before querying usage data.**

### Phase 1: Discovery

```bash
#!/bin/bash
INFURA_KEY="${INFURA_API_KEY}"

echo "=== RPC Endpoint Health ==="
for network in mainnet sepolia polygon-mainnet arbitrum-mainnet optimism-mainnet linea-mainnet; do
  base_url="https://${network}.infura.io/v3/${INFURA_KEY}"
  result=$(curl -s -X POST "$base_url" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}')
  status=$(echo "$result" | jq -r 'if .result then "OK (block: \(.result))" else "ERROR: \(.error.message // "unreachable")" end')
  echo "$network: $status"
done

echo ""
echo "=== IPFS Gateway Health ==="
curl -s -o /dev/null -w "IPFS Gateway: %{http_code} (%{time_total}s)\n" \
  "https://ipfs.infura.io:5001/api/v0/version" \
  --user "${INFURA_KEY}:${INFURA_SECRET}" 2>/dev/null || echo "IPFS: Check credentials"

echo ""
echo "=== WebSocket Test ==="
echo "WSS endpoints available at wss://{network}.infura.io/ws/v3/${INFURA_KEY}"
curl -s -X POST "https://mainnet.infura.io/v3/${INFURA_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}' | \
  jq -r '"Sync Status: \(.result)"'
```

**Phase 1 outputs:** Endpoint health across chains, IPFS status, WebSocket availability

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Network Stats (Ethereum Mainnet) ==="
curl -s -X POST "https://mainnet.infura.io/v3/${INFURA_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}' | \
  jq -r '"Gas Price (hex): \(.result)"'

echo ""
echo "=== Latest Block ==="
curl -s -X POST "https://mainnet.infura.io/v3/${INFURA_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest",false],"id":1}' | \
  jq -r '.result | "Block: \(.number)\nTimestamp: \(.timestamp)\nTransactions: \(.transactions | length)\nGas Used: \(.gasUsed)"'

echo ""
echo "=== IPFS Stats ==="
curl -s -X POST "https://ipfs.infura.io:5001/api/v0/stats/repo" \
  --user "${INFURA_KEY}:${INFURA_SECRET}" | \
  jq -r '"Repo Size: \(.RepoSize)\nNum Objects: \(.NumObjects)\nStorage Max: \(.StorageMax)"' 2>/dev/null || echo "IPFS stats require authentication"

echo ""
echo "=== Multi-chain Block Heights ==="
for network in mainnet polygon-mainnet arbitrum-mainnet optimism-mainnet; do
  block=$(curl -s -X POST "https://$network.infura.io/v3/${INFURA_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | \
    jq -r '.result')
  echo "$network: $block"
done
```

## Output Format

```
INFURA STATUS
=============
Endpoints: {healthy}/{total} healthy
Chains: {list_of_supported}
Ethereum Gas: {gwei} gwei
IPFS: {status} ({repo_size})
Daily Requests: {count}/{limit}
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

- **Daily request limits**: Free tier is 100K requests/day — monitor to avoid cutoff
- **API key security**: Never expose API key in client-side code — use allowlists
- **IPFS authentication**: Requires project ID and secret as basic auth
- **Archive data**: Historical state requires archive add-on — standard nodes prune old state
