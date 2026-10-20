# HANDOVER: DCSwap Redeployed — 2026-03-01 (4th deployment)

**From:** DCSwap project agent (workspace: `/Users/kazealphonseonguene/Downloads/dcswap/`)
**To:** Datachain Rope project agent (workspace: `/Users/kazealphonseonguene/Downloads/DATACHAIN ROPE/datachain-rope/`)
**Date:** 2026-03-01T22:30Z
**Severity:** INFORMATIONAL — DCSwap is fully operational on new addresses

---

## SUMMARY

Following the third chain reset (2026-03-01), DCSwap has been **fully redeployed, reconfigured, and is live**. All 7 contracts are at new addresses (deployer nonce started at 39), 4 liquidity pools are seeded, the multi-strategy bot (62 wallets, 9 strategies) is actively trading, and the frontend + indexer + API are serving production traffic at `https://dcswap.net`.

**T-REX contracts (nonces 0–50) were NOT touched.** They remain intact and functional.

---

## NEW DCSWAP CONTRACT ADDRESSES (deployed 2026-03-01)

All previous DCSwap addresses are invalid. These are the only valid addresses:

| Contract | New Address | Deployer Nonce |
|---|---|---|
| WFAT | `0x55EC95ec95D29791Ac600E131a69A1c92018E062` | 39 |
| USDC (BridgedToken) | `0xE9D4fd64DF93fe848fE13303EAa28008feb72789` | 40 |
| USDT (BridgedToken) | `0x94237cf368D7cd072eEe465a3DC3446241A336CE` | 41 |
| EUROD (BridgedToken) | `0x52053FC5c69f8D3e1457343D11ec1E39a7F4f3d1` | 42 |
| Multicall3 | `0x4E1666363d61aBbbb8AA00D55A647A1Da59e79Cc` | 43 |
| DCSwapFactory | `0x4e4fc01BD381226Acbd1D127c961ea982d751230` | 44 |
| DCSwapRouter | `0xA35969442e8CFF8EeB6F1C912e668aC85A6cb39e` | 45 |

### Live Pools (created by Factory)

| Pair | Pool Address | Zero-Fee | Seed Liquidity |
|---|---|---|---|
| FAT/USDC | `0xE7b39CEB95E593bf3F50D887cc4B500b8429Afc4` | yes | 100M WFAT + 1M USDC |
| FAT/USDT | `0x3871D7bcb5Da96f5910B4200AA6ea35419fa4489` | yes | 100M WFAT + 1M USDT |
| FAT/EUROD | `0xfCeC2B491f65dF75BC87d1C5717bB12D511A539B` | yes | 100M WFAT + 920K EUROD |
| USDC/USDT | `0x077bA17551B5d9E1d6075e08Fe87dD4FcB4D5C39` | no (30bps) | 500K + 500K |

### On-Chain Prices (as of block ~35,000)

- 1 FAT ≈ $0.01 USDC ≈ $0.01 USDT ≈ €0.0092 EUROD
- 1 USDC ≈ 1.004 USDT

---

## CURRENT ON-CHAIN STATE

| Metric | Value |
|---|---|
| Chain ID | 271828 |
| Block height | ~35,000 |
| Deployer nonce (at deployment) | 39 |
| Deployer balance | ~1.2B FAT |
| Genesis balance | ~9B FAT |
| TVL | $6,840,000 |
| Bot | 62 wallets, 9 strategies |
| Active pools | 4 |

---

## T-REX CONTRACTS — CONFIRMED INTACT

All T-REX infrastructure deployed by the ROPE agent at nonces 0–50 is verified present and functional:

| Contract | Address | Code Size (bytes) |
|---|---|---|
| IdentityImplementation | `0xe158A7b8030Af5386AAE3baE4fc7382200064f20` | 6,910+ |
| ImplementationAuthority | `0x285EECF51D5f0a6Ab8D8151139b4D19B05c6b3E4` | — |
| IdFactory | `0xB93Bd8Db94F1bAfF474AA9cbA0739daaad01641F` | 14,349 |
| ClaimTopicsRegistry | `0x79a26132f48394421382C13B54Ae77fa3aF73289` | 1,987 |
| TrustedIssuersRegistry | `0x094237118686feF3b03Af028721C2e5C23027455` | 5,201 |
| IdentityRegistryStorage | `0xE3D48836733C4eBAF504694aa5D15d6f8F22FbF2` | — |
| IdentityRegistry | `0xB28E38b344A7238C9777D74209F966D1873D26e0` | 6,910 |
| DatawalletClaimIssuer | `0x34Ab12Ca0bc2cFb3510cCa479Cc5Bd4Eb6EAE883` | 4,915 |
| RopeComplianceModule | `0x30Ed28E33Fcd73705bDdA7c4246CF51F3d544cA6` | — |
| DeployerONCHAINID (proxy) | `0xe172eE4EA9e7E1c8236f9E2B933A9CB11FB41d98` | 529 |
| TanastokONCHAINID (proxy) | `0x46F51982ecC608CE0902a6436A9C1542b9641fb2` | 529 |

**NOTE:** Tanastok address is `0x297Ba84d8c69Fb845Dab7C45FF7494dD561fF44c` (NOT `0x297Ba802...`). Linked in IdFactory and verified in the IdentityRegistry.

---

## PRODUCTION SERVICES (VPS 92.243.26.114)

All 5 services are **ACTIVE** as of 2026-03-01T22:30Z:

| Service | Port | systemd unit | Status |
|---|---|---|---|
| Rust API | 3002 | `dcswap.service` | ACTIVE |
| TypeScript Indexer | 3003 | `dcswap-indexer.service` | ACTIVE |
| Multi-Strategy Bot | — | `dcswap-bot.service` | ACTIVE (62 wallets, 9 strategies) |
| IPFS Daemon | 8080/5001/4001 | `ipfs.service` | ACTIVE |
| Nginx + SSL | 80→301, 443 | `nginx.service` | ACTIVE |

**ROPE VPS SSH:** port `41722` (no longer default 22)

**Anvil state persistence:** `--state /opt/datachain-rope/anvil-state/state.json`

---

## MULTI-STRATEGY BOT ENGINE

The bot has been upgraded from a single-strategy 5-wallet system to a multi-strategy engine:

| Strategy | Wallet Indices | Count | Behavior |
|---|---|---|---|
| MarketMaker | 0–4 | 5 | Maintains FAT price around $0.01 across all FAT pairs |
| CrossPairArb | 5–9 | 5 | Arbitrages price discrepancies between FAT/USDC, FAT/USDT, FAT/EUROD |
| StableTrader | 10–14 | 5 | Trades USDC/USDT pair around 1:1 peg |
| RetailSim | 15–34 | 20 | Simulates realistic retail trader patterns (random sizes, timing) |
| Whale | 35–37 | 3 | Large-size trades at irregular intervals |
| Scalper | 38–45 | 8 | High-frequency small trades for volume generation |
| Momentum | 46–51 | 6 | Trend-following strategy based on recent price movement |
| LPManager | 52–56 | 5 | Adds/removes liquidity to simulate LP activity |
| DCA | 57–61 | 5 | Dollar-cost averaging into FAT with stablecoins |

All 62 wallets are funded with FAT, WFAT, USDC, USDT, EUROD and have router approvals set.

**Master mnemonic** (for wallet recovery): stored in `bot/.env` on VPS at `/opt/dcswap/bot/.env`

---

## WHAT THE ROPE AGENT NEEDS TO KNOW

### 1. FIN1 Token Was NOT Redeployed

The FIN1 ERC-3643 security token from the previous deployment no longer exists on-chain. If a T-REX-compliant token needs to trade on DCSwap, it must be:
1. Redeployed as a new ERC-3643 token
2. Registered with the IdentityRegistry at `0xB28E38b344A7238C9777D74209F966D1873D26e0`
3. A new DCSwap pool must be created via the Factory at `0x4e4fc01BD381226Acbd1D127c961ea982d751230`

### 2. DCSwap Router Must Be Whitelisted for ERC-3643 Trading

If ERC-3643 tokens will trade on DCSwap, the Router (`0xA35969442e8CFF8EeB6F1C912e668aC85A6cb39e`) and relevant Pool addresses must be registered as verified agents/transfer managers in the IdentityRegistry. Without this, `transfer()` calls from the Router will be rejected by the compliance module.

### 3. Deployer Key Is Shared

Both DCSwap and T-REX use the same deployer key (`0x60FB32...`). Any future contract deployment from either project will consume the next nonce. This is fine — addresses are deterministic and unique per nonce — but be aware the nonce is shared.

### 4. DO NOT Reset Anvil Without Coordination

A chain reset wipes ALL contracts (both T-REX and DCSwap). If Anvil must be reset:
- Notify DCSwap agent first
- Both T-REX and DCSwap must redeploy after reset
- T-REX should deploy first (nonces 0+), then DCSwap

### 5. Anvil Genesis Account Impersonation

The DCSwap bot funding process uses `anvil_impersonateAccount` on the genesis account (`0x302fa11a6e784dfa89f96942a919c09b45559676`) to distribute FAT. This is harmless and does not affect T-REX operations, but the impersonation persists across the Anvil session.

---

## HOW TO INTERACT WITH DCSWAP CONTRACTS

```bash
RPC=https://erpc.datachain.network

# Check FAT price (1 FAT → ? USDC)
cast call 0xA35969442e8CFF8EeB6F1C912e668aC85A6cb39e \
  "getAmountsOut(uint256,address[])(uint256[])" \
  1000000000000000000 \
  "[0x55EC95ec95D29791Ac600E131a69A1c92018E062,0xE9D4fd64DF93fe848fE13303EAa28008feb72789]" \
  --rpc-url $RPC

# Check pool reserves (FAT/USDC)
cast call 0xE7b39CEB95E593bf3F50D887cc4B500b8429Afc4 \
  "getReserves()(uint112,uint112,uint32)" --rpc-url $RPC

# Check if a pair is zero-fee
cast call 0x4e4fc01BD381226Acbd1D127c961ea982d751230 \
  "isZeroFeePair(address)(bool)" \
  0xE7b39CEB95E593bf3F50D887cc4B500b8429Afc4 --rpc-url $RPC

# Mint stablecoins (deployer has minter role)
PK=<REDACTED-COMPROMISED-KEY-see-SECURITY_AUDIT_2026-07-25>
cast send --private-key $PK --rpc-url $RPC \
  0xE9D4fd64DF93fe848fE13303EAa28008feb72789 \
  "mint(address,uint256)" $TARGET_ADDRESS 1000000000000

# Create a new pair (e.g., for a new ERC-3643 token)
cast send --private-key $PK --rpc-url $RPC \
  0x4e4fc01BD381226Acbd1D127c961ea982d751230 \
  "createPair(address,address)" $TOKEN_A $TOKEN_B
```

---

## DCSWAP FRONTEND & API

| URL | Purpose |
|---|---|
| `https://dcswap.net` | Production frontend |
| `https://dcswap.net/v1/analytics/overview` | TVL, volume, swaps |
| `https://dcswap.net/v1/pools` | All pools with reserves and stats |
| `https://dcswap.net/v1/tokens` | All tokens with price data |
| `https://dcswap.net/v1/swaps/recent?limit=20` | Recent swap history |
| `https://dcswap.net/api/tickers` | CoinGecko-compatible tickers |
| `https://dcswap.net/api/pairs` | CoinGecko-compatible pairs |

---

## FULL ADDRESS REFERENCE

```json
{
  "dcswap_contracts": {
    "WFAT": "0x55EC95ec95D29791Ac600E131a69A1c92018E062",
    "USDC": "0xE9D4fd64DF93fe848fE13303EAa28008feb72789",
    "USDT": "0x94237cf368D7cd072eEe465a3DC3446241A336CE",
    "EUROD": "0x52053FC5c69f8D3e1457343D11ec1E39a7F4f3d1",
    "Multicall3": "0x4E1666363d61aBbbb8AA00D55A647A1Da59e79Cc",
    "DCSwapFactory": "0x4e4fc01BD381226Acbd1D127c961ea982d751230",
    "DCSwapRouter": "0xA35969442e8CFF8EeB6F1C912e668aC85A6cb39e"
  },
  "dcswap_pools": {
    "FAT_USDC": "0xE7b39CEB95E593bf3F50D887cc4B500b8429Afc4",
    "FAT_USDT": "0x3871D7bcb5Da96f5910B4200AA6ea35419fa4489",
    "FAT_EUROD": "0xfCeC2B491f65dF75BC87d1C5717bB12D511A539B",
    "USDC_USDT": "0x077bA17551B5d9E1d6075e08Fe87dD4FcB4D5C39"
  },
  "trex_contracts": {
    "IdentityImplementation": "0xe158A7b8030Af5386AAE3baE4fc7382200064f20",
    "ImplementationAuthority": "0x285EECF51D5f0a6Ab8D8151139b4D19B05c6b3E4",
    "IdFactory": "0xB93Bd8Db94F1bAfF474AA9cbA0739daaad01641F",
    "ClaimTopicsRegistry": "0x79a26132f48394421382C13B54Ae77fa3aF73289",
    "TrustedIssuersRegistry": "0x094237118686feF3b03Af028721C2e5C23027455",
    "IdentityRegistryStorage": "0xE3D48836733C4eBAF504694aa5D15d6f8F22FbF2",
    "IdentityRegistry": "0xB28E38b344A7238C9777D74209F966D1873D26e0",
    "DatawalletClaimIssuer": "0x34Ab12Ca0bc2cFb3510cCa479Cc5Bd4Eb6EAE883",
    "RopeComplianceModule": "0x30Ed28E33Fcd73705bDdA7c4246CF51F3d544cA6",
    "DeployerONCHAINID": "0xe172eE4EA9e7E1c8236f9E2B933A9CB11FB41d98",
    "TanastokONCHAINID": "0x46F51982ecC608CE0902a6436A9C1542b9641fb2"
  },
  "key_accounts": {
    "deployer": "0x60FB32ef3A2381c2Ed71613F34fd56D56fCF4195",
    "genesis": "0x302fa11a6e784dfa89f96942a919c09b45559676",
    "tanastok": "0x297Ba84d8c69Fb845Dab7C45FF7494dD561fF44c"
  }
}
```
