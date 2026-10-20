---
name: blockchain-web3-core
description: "Shared reference for the blockchain-web3 cluster: the adversarial on-chain threat model (immutable, anyone-can-call, MEV), checks-effects-interactions, oracle-manipulation resistance, token-decimals precision, and the non-advisory stance for trading/prediction-market work. USE WHEN writing, auditing, or reasoning about smart-contract / DeFi / on-chain code — the cross-cutting model every web3 spoke shares."
cluster: blockchain-web3
version: 1.0.0
origin: "affaan-m/ECC (MIT)"
---

# Blockchain / Web3 Core

Shared model for the `blockchain-web3` cluster. On-chain code is **immutable, public, and
adversarial** — once deployed, anyone can call it, read its state, and reorder/observe its
transactions. That single fact drives every rule below.

## 1. The adversarial model (decide everything from here)

- **Anyone can call any external function** in any order, any number of times. Never assume a
  caller, a sequence, or a single invocation.
- **Everything on-chain is public** — "private" variables are readable; no secrets in contract state.
- **Transactions are front-runnable / reorderable (MEV)** — the mempool is visible; assume an
  adversary can sandwich, front-run, or back-run any state-changing call.
- **Deployed code is immutable** (absent an upgrade proxy) — a bug is permanent and exploitable
  for the contract's full TVL. There is no "ship and patch."

## 2. Non-negotiable contract-safety rules

- **Checks-Effects-Interactions (CEI):** validate → update state → *then* make external calls. The
  canonical defense against **reentrancy** (+ a `nonReentrant` guard for value transfers). → `defi-amm-security`
- **Access control:** explicit, least-privilege roles; prefer two-step ownership transfer
  (`Ownable2Step`); never leave an unguarded `selfdestruct`/`delegatecall`.
- **Oracle manipulation:** never price off a spot AMM reserve an attacker can move in one block;
  use TWAP / multiple sources / circuit breakers. → `prediction-market-oracle-research`
- **Integer & decimals precision:** track token `decimals` explicitly; multiply before dividing;
  beware rounding that leaks value; validate the donation/inflation attack on share-based vaults. → `evm-token-decimals`
- **Validate all inputs** (the webview-is-untrusted rule, on-chain edition): the caller is hostile.

## 3. Routing within the cluster

| Concern | Spoke |
|---|---|
| AMM / vault / DeFi security review | `defi-amm-security` |
| Token decimals / precision bugs | `evm-token-decimals` |
| LLM/agent that touches a wallet or trades | `llm-trading-agent-security` |
| Hashing / keccak256 utility | `nodejs-keccak256` |
| Prediction-market oracle / risk research | `prediction-market-oracle-research`, `prediction-market-risk-review` |

## 4. Non-advisory stance (hard guardrail)

The prediction-market and trading spokes produce **research and risk analysis, not
financial advice**. Never present an output as a recommendation to buy/sell, never auto-execute a
trade or move funds, and always surface assumptions + downside/risk. An agent with wallet access
(`llm-trading-agent-security`) must gate every value-moving action behind explicit human confirmation.

## 5. Tooling / version matrix

| Need | Tool |
|---|---|
| Build / test (Solidity) | Foundry (`forge`) or Hardhat |
| Static analysis | Slither, Mythril; `forge` invariant/fuzz tests |
| Standards | OpenZeppelin (audited primitives) over hand-rolled |
| Hashing off-chain | `nodejs-keccak256` (match on-chain `keccak256` exactly) |

## 6. Shared guardrails

- Assume adversarial callers, public state, and MEV — always.
- Checks-Effects-Interactions + reentrancy guards on every external interaction.
- No spot-reserve price oracles; TWAP / multi-source.
- Track decimals explicitly; multiply-before-divide.
- Audited primitives (OpenZeppelin) over bespoke crypto.
- Trading/prediction outputs are non-advisory; never auto-move funds; gate on human confirmation.
- Treat deployed code as permanent — audit + test (fuzz/invariant) before mainnet.
