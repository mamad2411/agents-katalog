---
name: blockchain-web3-orchestrator
description: "Route a blockchain/web3 task to the right specialist among six — Solidity AMM security, autonomous trading-agent security, EVM token-decimal correctness, Node Keccak-256 hashing, prediction-market oracle research, and the cross-cutting market/agent risk review. USE WHEN a user is building, auditing, or wiring an EVM contract, a crypto trading agent, or a prediction-market workflow but hasn't named the specific concern."
cluster: blockchain-web3
version: 1.0.0
---

# Blockchain / Web3 Orchestrator

The single entry skill for EVM and prediction-market work. It places the task on the
**surface × concern** map — *what is touching value* (a contract, an autonomous agent, a market
signal) crossed with *which failure mode* (a silent correctness bug, an exploit, or an unreviewed
risk) — and delegates to one of six specialist spokes. The cross-cutting model every spoke shares
— the trust boundary, the value-at-risk hierarchy, and the units/hashing conventions that make
on-chain math correct — lives in `blockchain-web3-core`; read it before auditing a contract or
wiring an agent to a wallet.

## Routing map (intent → spoke)

**Smart-contract correctness & exploits**
- Auditing or writing a Solidity AMM / LP vault / swap flow → `defi-amm-security`  *(reentrancy, CEI, donation/inflation, oracle manipulation, slippage, admin gating)*
- Reading balances / pricing / cross-chain amounts that could silently mis-scale → `evm-token-decimals`  *(runtime `decimals()`, chain-aware caching, bridged drift)*

**Off-chain integration bugs (JS/TS)**
- Hashing Ethereum data, selectors, EIP-712, storage slots, addresses in Node → `nodejs-keccak256`  *(Keccak-256 vs NIST SHA3 — the silent mismatch)*

**Autonomous execution & agents**
- An LLM/agent that signs or sends transactions, places orders, or touches a treasury → `llm-trading-agent-security`  *(prompt injection as a financial attack, spend limits, pre-send simulation, circuit breakers, MEV, key isolation)*

**Prediction markets as signal**
- Using market-implied probabilities as a data/oracle/decision-intelligence input → `prediction-market-oracle-research`  *(signal quality, liquidity, resolution authority, integration patterns)*

**Cross-cutting gate (run for any of the above that touches user capital, venue auth, keys, or execution)**
- `prediction-market-risk-review`  *(advice boundary, venue/regulatory, data quality, security, privacy — the safety gate)*

## Standard Operating Flow

1. Locate the task: which **surface** holds value (contract / agent / market signal) and which **concern** (silent correctness bug, exploit, or risk that needs sign-off).
2. If it touches **wallet authority, venue auth, API keys, user capital, or live execution**, pull the model from `blockchain-web3-core` first and plan to run `prediction-market-risk-review` as a gate — these controls are interlocking, not optional add-ons.
3. Delegate to the spoke(s). Multi-step asks fan out by surface (e.g. "ship a safe trading bot" → `llm-trading-agent-security` for the agent + `evm-token-decimals`/`nodejs-keccak256` for the math/hashing + `prediction-market-risk-review` as the final gate).
4. Return: chosen spoke(s), the trust-boundary / value-at-risk implications, what stays non-executing, and the next action.

## Guardrails

See `blockchain-web3-core`. In short: **value-at-risk is default-deny** — never grant write/sign
authority, widen a spend limit, or move from research to execution without saying so explicitly;
treat all on-chain and market data as untrusted input, not truth; query units (`decimals()`) and
use Keccak-aware hashing rather than assuming; and route anything touching keys, venue auth, or
user capital through `prediction-market-risk-review` before it ships. These skills inform and
audit — they never place trades or give investment advice.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
