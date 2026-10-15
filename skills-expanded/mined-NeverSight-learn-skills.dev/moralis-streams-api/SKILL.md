---
name: moralis-streams-api
description: Real-time blockchain event monitoring with webhooks across EVM, Solana, and Bitcoin. Use when user asks about setting up webhooks, monitoring wallet/program/contract activity, tracking token or NFT transfers as they happen, adding or removing stream addresses, managing Bitcoin xpubs, replaying blocks, or receiving onchain events in real time. NOT for querying historical or current blockchain state - use moralis-data-api instead.
version: 1.5.2
license: MIT
compatibility: Requires curl for API calls. Requires MORALIS_API_KEY env var for authentication.
metadata:
  author: MoralisWeb3
  homepage: https://docs.moralis.com
  repository: https://github.com/MoralisWeb3/onchain-skills
  openclaw:
    requires:
      env:
        - MORALIS_API_KEY
      bins:
        - curl
    primaryEnv: MORALIS_API_KEY
allowed-tools: Bash Read Grep Glob
---

## CRITICAL: Read Rule Files Before Implementing

**The #1 cause of Streams bugs is mixing up stream families or request shapes.**

For EVERY endpoint:
1. Read `rules/{EndpointName}.md`
2. Confirm the family first:
   - EVM: `/streams/evm`
   - Solana: `/streams/solana`
   - Bitcoin: `/streams/bitcoin`
   - Utilities: `/history`, `/settings`, `/stats`
3. Check the HTTP method carefully (`PUT` create, `POST` update/status/replay, `DELETE` delete)
4. Verify stream IDs are UUIDs, not hashes or addresses
5. Use the correct config shape for that family:
   - EVM: `chainIds`, `topic0`, `abi`, `advancedOptions`
   - Solana: `network`, `programIds`, `mintAddresses`, `allAddresses`
   - Bitcoin: `network`, `includeInputs`, `includeOutputs`, `allAddresses`, `xpub`

**Reading order:**
1. This `SKILL.md`
2. The endpoint rule in `rules/`
3. `references/StreamConfiguration.md`
4. Family-specific references for edge cases

---

## Setup

### API Key

**Never ask the user to paste their API key into the chat.** Instead:

1. Check whether `MORALIS_API_KEY` is set:
   ```bash
   [ -n "$MORALIS_API_KEY" ] && echo "API key is set" || echo "API key is NOT set"
   ```
2. If missing, offer to create a local `.env` with `MORALIS_API_KEY=`
3. Tell the user to open `.env` and add the key themselves
4. Explain that without the key, you cannot call or test Moralis Streams

If they need a key, point them to [admin.moralis.com/register](https://admin.moralis.com/register).

### Verify Your Key

```bash
curl "https://api.moralis-streams.com/streams/evm?limit=10" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

---

## Base URL

```text
https://api.moralis-streams.com
```

All requests require `X-API-Key: $MORALIS_API_KEY`.

---

## Stream Families

| Family | Core filters | Extras | Notes |
|--------|--------------|--------|-------|
| EVM | `chainIds`, `topic0`, `abi`, stream addresses | `advancedOptions`, `includeContractLogs`, `includeNativeTxs`, `includeInternalTxs`, `triggers`, `getNativeBalances` | Use hex chain IDs like `0x1`, `0x89` |
| Solana | `network`, `programIds`, `mintAddresses`, stream addresses | `allAddresses`, block replay helpers | No `chainIds`, no `topic0`, no EVM ABI decoding |
| Bitcoin | `network`, stream addresses, `allAddresses` | `includeInputs`, `includeOutputs`, xpub endpoints, block replay helpers | Address and xpub monitoring instead of contract topics |
| Utilities | history, replay, settings, stats | account-level operations | Shared across all stream families |

### EVM

Use EVM streams for contract events, ERC20 / ERC721 / ERC1155 transfers, approvals, native transactions, and internal transactions on supported EVM mainnet chains.

Stream types:

| Type | Description |
|------|-------------|
| `tx` | Native transactions |
| `log` | Contract event logs |
| `erc20transfer` | ERC20 token transfers |
| `erc20approval` | ERC20 approvals |
| `nfttransfer` | NFT transfers |
| `internalTx` | Internal transactions |

### Solana

Use Solana streams when the user wants program, mint, or address activity on `mainnet` or `devnet`.

- Primary filters are `programIds` and `mintAddresses`
- `network` is an array such as `["mainnet"]` or `["devnet"]`
- There is no EVM-style `topic0`, `abi`, or `chainIds`
- Solana addresses are base58 and case-sensitive; never lowercase them
- Solana payloads use `transactions[].signature`, `accountKeys`, `instructions`, `innerInstructions`, and pre/post token balances instead of EVM event arrays

See [references/SolanaStreams.md](references/SolanaStreams.md).

### Bitcoin

Use Bitcoin streams for address-based or xpub-based monitoring.

- Primary filters are watched addresses or xpubs
- `network` is an array
- `includeInputs` and `includeOutputs` control payload detail
- The live swagger currently exposes `mainnet` and `testnet`, while the narrative Bitcoin overview still documents `["mainnet"]` as the stable default

Default to `["mainnet"]` unless the user explicitly needs something else and the endpoint rule confirms it.

See [references/BitcoinStreams.md](references/BitcoinStreams.md).

---

## Quick Reference

### Stream ID Format

```typescript
// WRONG
"0x1234567890abcdef"

// CORRECT
"YOUR_STREAM_ID"
```

### EVM Chain IDs

```typescript
"0x1"     // Ethereum
"0x89"    // Polygon
"0x38"    // BSC
"0xa4b1"  // Arbitrum
"0xa"     // Optimism
"0x2105"  // Base
```

### Solana Networks

```json
["mainnet"]
["devnet"]
```

### Bitcoin Networks

```json
["mainnet"]
```

If the endpoint rule shows `testnet`, treat it as swagger-exposed behavior and verify before depending on it.

### Status Values

```typescript
"active"
"paused"
"error"
"terminated"
```

Only send `active` or `paused` in update requests.

---

## Delivery Model

- Moralis sends a mandatory **test webhook** on create and update. Your endpoint must return `2xx`.
- Streams are **at-least-once delivered**. Build idempotent consumers.
- EVM and Solana webhook flows use `confirmed: false` then `confirmed: true`.
- Bitcoin can deliver up to three lifecycle notifications for one `txid`: mempool (`block.hash: "mempool"`, `block.height: "0"`), in-block but unconfirmed (`confirmed: false`), then reorg-safe (`confirmed: true`) after the 2-block confirmation depth.
- Streams can enter `error` and then `terminated` if webhook delivery keeps failing.

See [references/DeliveryGuarantees.md](references/DeliveryGuarantees.md), [references/ErrorHandling.md](references/ErrorHandling.md), and [references/WebhookSecurity.md](references/WebhookSecurity.md).

---

## EVM-Only Features

These are for EVM streams only:

- `triggers`
- `advancedOptions`
- `includeContractLogs`
- `includeNativeTxs`
- `includeInternalTxs` (supported EVM mainnet chains only; not testnets)
- `includeAllTxLogs` (available on Pro plans and higher)
- `getNativeBalances`
- `filterPossibleSpamAddresses`
- `topic0` / ABI-based filtering

See [references/UsefulStreamOptions.md](references/UsefulStreamOptions.md), [references/Triggers.md](references/Triggers.md), and [references/ListenToAllAddresses.md](references/ListenToAllAddresses.md).

---

## Quick Troubleshooting

| Issue | Likely cause | Fix |
|-------|--------------|-----|
| `400 Bad Request` | Mixed request shape | Re-check the family-specific fields in the endpoint rule |
| `404 Not Found` | Wrong stream ID | Use a UUID stream ID |
| `Method Not Allowed` | Wrong method | Create with `PUT`, update/status/replay with `POST` |
| `Missing limit` | List endpoint | Add `?limit=100` |
| Stream never activates | Test webhook failed | Return `2xx` from the webhook endpoint |

---

## Endpoint Catalog

Complete list of all 45 Streams API endpoints across EVM, Solana, Bitcoin, and shared utilities.

### EVM Streams

Create, update, delete, and simulate EVM streams, including block replay helpers.

| Endpoint | Description |
|----------|-------------|
| [CreateStream](rules/CreateStream.md) | Create stream |
| [DeleteStream](rules/DeleteStream.md) | Delete stream |
| [DuplicateStream](rules/DuplicateStream.md) | Duplicate stream |
| [GetStream](rules/GetStream.md) | Get a specific evm stream. |
| [GetStreamBlockDataByNumber](rules/GetStreamBlockDataByNumber.md) | Get webhook data returned on the block number with provided stream config |
| [GetStreamBlockDataToWebhookByNumber](rules/GetStreamBlockDataToWebhookByNumber.md) | Send webhook based on a specific block number using stream config and addresses. |
| [GetStreams](rules/GetStreams.md) | Get streams |
| [UpdateStream](rules/UpdateStream.md) | Update stream |
| [UpdateStreamStatus](rules/UpdateStreamStatus.md) | Update stream status |

### EVM Addresses

Manage address lists for EVM streams.

| Endpoint | Description |
|----------|-------------|
| [AddAddressToStream](rules/AddAddressToStream.md) | Add address to stream |
| [DeleteAddressFromStream](rules/DeleteAddressFromStream.md) | Delete address from stream |
| [GetAddresses](rules/GetAddresses.md) | Get addresses by stream |
| [ReplaceAddressFromStream](rules/ReplaceAddressFromStream.md) | Replaces address from stream |

### Solana Streams

Create, update, delete, and simulate Solana streams, including block replay helpers.

| Endpoint | Description |
|----------|-------------|
| [solanaBlockToWebhook](rules/solanaBlockToWebhook.md) | Send Solana webhook data by block number |
| [solanaGetBlockByNumber](rules/solanaGetBlockByNumber.md) | Get Solana webhook data by block number |
| [solanaStreamsCreate](rules/solanaStreamsCreate.md) | Create Solana stream |
| [solanaStreamsDelete](rules/solanaStreamsDelete.md) | Delete Solana stream |
| [solanaStreamsGet](rules/solanaStreamsGet.md) | Get Solana stream by ID |
| [solanaStreamsGetAll](rules/solanaStreamsGetAll.md) | Get Solana streams |
| [solanaStreamsUpdate](rules/solanaStreamsUpdate.md) | Update Solana stream |
| [solanaStreamsUpdateStatus](rules/solanaStreamsUpdateStatus.md) | Update Solana stream status |

### Solana Addresses

Manage address lists for Solana streams.

| Endpoint | Description |
|----------|-------------|
| [solanaStreamsAddAddresses](rules/solanaStreamsAddAddresses.md) | Add address to Solana stream |
| [solanaStreamsDeleteAddresses](rules/solanaStreamsDeleteAddresses.md) | Delete address from Solana stream |
| [solanaStreamsGetAddresses](rules/solanaStreamsGetAddresses.md) | Get addresses by Solana stream |

### Bitcoin Streams

Create, update, delete, and simulate Bitcoin streams, including block replay helpers.

| Endpoint | Description |
|----------|-------------|
| [bitcoinBlockToWebhook](rules/bitcoinBlockToWebhook.md) | Send Bitcoin webhook data by block number |
| [bitcoinGetBlockByNumber](rules/bitcoinGetBlockByNumber.md) | Get Bitcoin webhook data by block number |
| [bitcoinStreamsCreate](rules/bitcoinStreamsCreate.md) | Create Bitcoin stream |
| [bitcoinStreamsDelete](rules/bitcoinStreamsDelete.md) | Delete Bitcoin stream |
| [bitcoinStreamsGet](rules/bitcoinStreamsGet.md) | Get Bitcoin stream by ID |
| [bitcoinStreamsGetAll](rules/bitcoinStreamsGetAll.md) | Get Bitcoin streams |
| [bitcoinStreamsUpdate](rules/bitcoinStreamsUpdate.md) | Update Bitcoin stream |
| [bitcoinStreamsUpdateStatus](rules/bitcoinStreamsUpdateStatus.md) | Update Bitcoin stream status |

### Bitcoin Addresses

Manage address lists for Bitcoin streams.

| Endpoint | Description |
|----------|-------------|
| [bitcoinStreamsAddAddresses](rules/bitcoinStreamsAddAddresses.md) | Add address to Bitcoin stream |
| [bitcoinStreamsDeleteAddresses](rules/bitcoinStreamsDeleteAddresses.md) | Delete address from Bitcoin stream |
| [bitcoinStreamsGetAddresses](rules/bitcoinStreamsGetAddresses.md) | Get addresses by Bitcoin stream |

### Bitcoin Xpub

Manage Bitcoin xpubs attached to a stream.

| Endpoint | Description |
|----------|-------------|
| [bitcoinStreamsAddXpub](rules/bitcoinStreamsAddXpub.md) | Add xpub to Bitcoin stream |
| [bitcoinStreamsDeleteXpub](rules/bitcoinStreamsDeleteXpub.md) | Delete xpub from Bitcoin stream |
| [bitcoinStreamsGetXpubs](rules/bitcoinStreamsGetXpubs.md) | Get xpubs by Bitcoin stream |

### Project Settings

Read and update project-level stream settings.

| Endpoint | Description |
|----------|-------------|
| [GetSettings](rules/GetSettings.md) | Get project settings |
| [SetSettings](rules/SetSettings.md) | Set project settings |

### Stats

Inspect global and per-stream statistics.

| Endpoint | Description |
|----------|-------------|
| [GetStats](rules/GetStats.md) | Get project stats |
| [GetStatsByStreamId](rules/GetStatsByStreamId.md) | Get project stats by Stream ID |

### History

List delivery history, logs, and replay failed webhook deliveries.

| Endpoint | Description |
|----------|-------------|
| [GetHistory](rules/GetHistory.md) | Get history |
| [GetLogs](rules/GetLogs.md) | Get logs |
| [ReplayHistory](rules/ReplayHistory.md) | Replay history |


## Example: Create EVM ERC20 Transfer Monitor

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "Monitor ERC20 transfers",
    "tag": "erc20-monitor",
    "topic0": ["Transfer(address,address,uint256)"],
    "allAddresses": true,
    "chainIds": ["0x1", "0x89"],
    "advancedOptions": [
      {
        "topic0": "Transfer(address,address,uint256)",
        "includeNativeTxs": true
      }
    ]
  }'
```

## Example: Create Solana Program Stream

```bash
curl -X PUT "https://api.moralis-streams.com/streams/solana" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "Monitor Solana program activity",
    "tag": "solana-monitor",
    "network": ["mainnet"],
    "programIds": ["YOUR_SOLANA_PROGRAM_ID"],
    "mintAddresses": ["YOUR_SOLANA_MINT"],
    "allAddresses": false
  }'
```

## Example: Create Bitcoin Address Stream

```bash
curl -X PUT "https://api.moralis-streams.com/streams/bitcoin" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "Monitor Bitcoin transactions",
    "tag": "bitcoin-monitor",
    "network": ["mainnet"],
    "includeInputs": true,
    "includeOutputs": true,
    "allAddresses": false
  }'
```

## Example: Add Bitcoin Xpub

```bash
curl -X POST "https://api.moralis-streams.com/streams/bitcoin/YOUR_STREAM_ID/xpub" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "xpub": "YOUR_XPUB"
  }'
```

## Pagination

List endpoints use cursor pagination:

```bash
# First page
curl "...?limit=100" -H "X-API-Key: $MORALIS_API_KEY"

# Next page
curl "...?limit=100&cursor=<cursor>" -H "X-API-Key: $MORALIS_API_KEY"
```

---

## Supported Chains

- EVM Streams: 40+ supported EVM chains. Use hex IDs. See [references/StreamConfiguration.md](references/StreamConfiguration.md).
- Solana Streams: `mainnet`, `devnet`
- Bitcoin Streams: default to `mainnet`; verify any non-mainnet use against the endpoint rule before relying on it

The live Moralis docs also publish a dedicated supported-chains page for EVM Streams.

---

## Reference Documentation

- [references/BitcoinStreams.md](references/BitcoinStreams.md) - Bitcoin stream config, xpubs, payload caveats
- [references/SolanaStreams.md](references/SolanaStreams.md) - Solana network, program, mint, and address stream guidance
- [references/StreamConfiguration.md](references/StreamConfiguration.md) - Cross-family request-shape reference
- [references/CommonPitfalls.md](references/CommonPitfalls.md) - Common mistakes and debugging checklist
- [references/DeliveryGuarantees.md](references/DeliveryGuarantees.md) - Delivery, confirmation, retries
- [references/ErrorHandling.md](references/ErrorHandling.md) - Error states, recovery, replay workflows
- [references/FAQ.md](references/FAQ.md) - Streams FAQ
- [references/FilterStreams.md](references/FilterStreams.md) - EVM filter expressions
- [references/ListenToAllAddresses.md](references/ListenToAllAddresses.md) - EVM all-address monitoring
- [references/MonitorMultipleAddresses.md](references/MonitorMultipleAddresses.md) - Address-list patterns
- [references/ReplayFailedWebhooks.md](references/ReplayFailedWebhooks.md) - Replay failed webhook deliveries
- [references/ReliabilityAndLifecycle.md](references/ReliabilityAndLifecycle.md) - Confirmation, idempotency, lifecycle, rate limits, and re-org handling
- [references/Triggers.md](references/Triggers.md) - EVM read-only contract call enrichment
- [references/Tutorials.md](references/Tutorials.md) - Real-world examples
- [references/UsefulStreamOptions.md](references/UsefulStreamOptions.md) - EVM-only advanced options
- [references/WebhookResponseBody.md](references/WebhookResponseBody.md) - Webhook payload structure
- [references/WebhookSecurity.md](references/WebhookSecurity.md) - Signature verification

---

## See Also

- Endpoint rules: `rules/*.md`
- Data API: `@moralis-data-api` for historical or current blockchain state
