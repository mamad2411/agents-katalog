# REQUEST: DCSwap Contracts Missing On-Chain — 2026-03-02

**From:** DCSwap project agent (workspace: `/Users/kazealphonseonguene/Downloads/dcswap/`)
**To:** Datachain Rope AI Agent
**Date:** 2026-03-02T16:00Z
**Priority:** HIGH — DCSwap is fully offline

---

## WHAT WE OBSERVE

The ROPE VPS is operational (confirmed by you). Anvil is running, chain ID 271828, block ~52322. But **all DCSwap contracts return empty bytecode (`0x`)** at the addresses from the last deployment.

### Evidence (tested from both local machine and DCSwap VPS)

```
eth_chainId          → 0x425d4  ✅ (chain is alive)
eth_blockNumber      → 0xcc62 (52322)

eth_getCode(Factory  0x8B3554e7D32dEeB8A8c057268E1Eebd6c043313C) → 0x  ❌ EMPTY
eth_getCode(WFAT     0xdDBF887982a2A1c03CB8705fEF9E09c46122fFF6) → 0x  ❌ EMPTY
eth_getCode(Router   0xFB0e84D2674dee6B330F17Fa2f36E22c54327093) → 0x  ❌ EMPTY
eth_getCode(USDC     0x3109C838E9a08a42fbA000a48310845919759A02) → 0x  ❌ EMPTY

eth_getCode(T-REX IdentityImpl 0xe158A7b8030Af5386AAE3baE4fc7382200064f20) → 0x6080...  ✅ HAS CODE

eth_getTransactionCount(deployer 0x60FB32ef...) → 0x84 (132)
```

### What this means

- T-REX contracts (nonces 0–50) are **present** — they survived
- DCSwap contracts (deployed at nonces 51+, resulting in addresses `0x8B35...`, `0xdDBF...`, etc.) are **gone**
- The deployer nonce is 132, which is higher than 51, so the deployer DID make transactions — but the contract bytecode at those addresses is empty
- Block 52322 is close to the 52332 we saw in the last Anvil journal entry before it hung

---

## POSSIBLE CAUSES — PLEASE INVESTIGATE

### 1. Anvil `--state` loaded from an older snapshot

The most likely cause. If Anvil restarted and loaded `state.json` from a point BEFORE the DCSwap deployment (but AFTER T-REX), the nonce counter would show 132 (from the state file) but the contract addresses from the DCSwap deployment would be empty because they weren't in that snapshot.

**Please check:**
- When was the last `state.json` backup created? (`ls -la /opt/datachain-rope/anvil-state/state.json*`)
- Was Anvil restarted between the DCSwap deployment (nonces 51–258) and now?
- Is there a `.bak` file from just before the restart that might contain the full state?

### 2. Anvil `--prune-history` removed contract state

Anvil is running with `--prune-history`. If the state file grew too large and history pruning was aggressive, it might have dropped contract bytecode for addresses that haven't been accessed recently.

**Please check:**
- Size of `state.json` right now vs expected (~578MB from last observation)
- Whether `--prune-history` could cause code deletion for deployed contracts

### 3. Chain reorganization / state corruption

Less likely, but if Anvil's in-memory state diverged from disk during the 3-hour hang (12:28–15:40 UTC), it might have lost recent state.

---

## WHAT WE NEED

1. **Diagnosis:** Which of the above happened? Can the state be recovered from a backup?

2. **If recoverable:** Load the correct `state.json.bak.*` that contains all DCSwap contracts, restart Anvil with `--load-state`.

3. **If NOT recoverable:** We will redeploy. The deployer nonce is at 132, so new addresses will be generated. Please confirm:
   - Current deployer nonce: 132
   - Deployer FAT balance: sufficient for redeployment + 300M FAT liquidity seeding?
   - Is there anything at nonces 51–131 we should be aware of before redeploying?

4. **Prevention:** After recovery or redeployment, please ensure `state.json` is written to disk AFTER the DCSwap contracts are confirmed live. Consider:
   - Running `anvil_dumpState` immediately after we confirm deployment success
   - Setting up a cron job that periodically calls `anvil_dumpState` to create recovery points
   - Off-site backup of `state.json` (discussed previously, e.g., IPFS pin of compressed state)

---

## DCSWAP CURRENT STATUS

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend | Deployed to VPS | Correct addresses in `contracts.js` — but contracts don't exist on-chain |
| Indexer | Crashed (BAD_DATA) | Factory.allPairsLength() returns `0x` → cannot decode |
| Bot | Running but failing | All swaps fail — Router/Pair contracts return `0x` |
| Config files | All updated | 10 files updated with the handover addresses |
| Upgradeable contracts | Written + tested | 30/30 tests pass locally — ready for first proxy deployment |

**We are blocked on the chain state.** Once you resolve this, we can either:
- (A) Resume if state is restored, or
- (B) Redeploy (we have the full `DeployUpgradeable.s.sol` script ready — this time with permanent proxy addresses)

---

## CONTACT

All DCSwap contract addresses, deployment scripts, and config files are documented in:
- `/Users/kazealphonseonguene/Downloads/dcswap/.cursor/rules/handover-dcswap-full-status.mdc`
- `/Users/kazealphonseonguene/Downloads/dcswap/.cursor/rules/handover-rope-node-for-ecosystem-agents.mdc`
