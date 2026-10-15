---
name: ethereum-token-verification
description: "Use this skill when you need to verify Ethereum or EVM token contracts for security. User cases: checking token legitimacy, scanning for rug pulls, detecting hidden taxes, assessing liquidity risks, analysing holder distribution, evaluating tokens before purchase or investment, or gate-checking tokens in automated pipelines. Works with 44+ blockchain explorers across all major EVM networks."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# Ethereum Token Verification

Verify EVM token contracts for security risks via Cybercentry ACP.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> ethereum-token-verification --requirements '{"chain_id": 1, "platform_id": 1, "contract_address": "0x..."}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Description |
|-----------|------|-------------|
| `chain_id` | Number | Chain ID from the table below |
| `platform_id` | Number | Platform ID from the table below |
| `contract_address` | String | Contract address (e.g., `0x4ee38aa8d7449a177119e983610D73e9ace932dA`) |

### Chain IDs (EVM Standard)

| Blockchain | `chain_id` |
|-----------|-----------|
| Ethereum Mainnet | `1` |
| BSC Mainnet | `56` |
| Polygon Mainnet | `137` |
| Avalanche C-Chain | `43114` |
| Cronos Mainnet | `25` |
| Celo Mainnet | `42220` |
| Aurora Mainnet | `1313161554` |
| Arbitrum One | `42161` |
| OP Mainnet | `10` |
| XDC Network | `50` |
| Fuse Mainnet | `122` |
| Base Mainnet | `8453` |
| Linea | `59144` |
| 5ire Chain | `995` |
| opBNB | `204` |
| Sonic | `250` |
| Blast | `81457` |
| Abstract | `2741` |
| Ape Chain | `33139` |
| Berachain | `80085` |
| BitTorrent Chain | `199` |
| Fraxtal | `252` |
| Gnosis | `100` |
| Mantle | `5000` |
| Scroll | `534352` |
| zkSync Era | `324` |
| Moonbeam | `1284` |

### Platform IDs

| Platform | `platform_id` |
|----------|---------------|
| etherscan.io | 1 |
| bscscan.com | 2 |
| polygonscan.com | 3 |
| snowtrace.io | 4 |
| cronoscan.com | 6 |
| celoscan.io | 7 |
| aurorascan.dev | 8 |
| arbiscan.io | 9 |
| buildbear | 10 |
| optimism | 11 |
| xdc | 12 |
| reefscan.io | 13 |
| explorer.fuse.io | 15 |
| blockscout.com | 16 |
| basescan | 17 |
| routescan | 18 |
| tronscan.org | 19 |
| Lineascan | 21 |
| 5irechain | 22 |
| subscan | 23 |
| opbnb | 24 |
| sonicscan | 25 |
| blastscan | 27 |
| abstract | 28 |
| apechain | 29 |
| berachain | 30 |
| bittorrent | 31 |
| fraxtal | 32 |
| gnosis | 33 |
| hyperevm | 34 |
| katana | 35 |
| mantle | 36 |
| memecore | 37 |
| monad | 38 |
| scroll | 39 |
| sei | 40 |
| stable | 41 |
| swellchain | 42 |
| taiko | 43 |
| unichain | 44 |
| world | 45 |
| zksync | 47 |
| moonscan | 48 |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `scan_url` | String | Plain | Scan URL |

## Gotchas

- `chain_id` and `platform_id` are numbers, not strings - do not quote them
- `contract_address` must include the `0x` prefix
