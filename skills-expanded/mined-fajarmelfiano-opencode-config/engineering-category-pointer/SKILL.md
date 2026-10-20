---
name: engineering-category-pointer
description: "Pointer to a library of 21 specialized Engineering skills. Use when working on engineering-related tasks."
risk: none
---

# Engineering Capability Library 🎯

This is a **pointer skill**. The 21 specialized Engineering skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **ai-agent-evaluation-benchmarking** — Autonomous AI agent benchmark evaluation register: task completion rates, planning accuracy, tool invocation precision, and cost benchmarks.
- **ai-agent-tool-routing** — Autonomous AI agent tool router register: schema registration, runtime parameter coercion, idempotency keys, and error recovery policies.
- **ai-code-generation-guardrails** — Autonomous AI code generation safety guardrail register: static AST analysis, forbidden import filters, and zero-day vulnerability checks.
- **ai-prompt-regression-testing** — Prompt engineering regression test matrix register: baseline outputs, semantic drift thresholds, judge evaluations, and golden dataset.
- **cross-chain-relayer-audit** — Cross-chain relayer bridge audit register: message hash verifications, replay protection nonces, validator quorum, and withdrawal proofs.
- **defi-yield-strategy-allocator** — Multi-vault automated yield strategy allocation register: APY benchmarks, impermanent loss risk tiers, and rebalancing triggers.
- **observability-cloud-planning** — Build a cloud, SLO, and incident-readiness register after intake. Use when an SME needs monitoring scope, alert ownership, cost limits, or service planning.
- **smart-contract-formal-verification** — Foundry and Soroban formal invariant verification register: state transition rules, boundary invariant properties, and symbolic execution checks.
- **smart-contract-upgrade-governance** — Soroban WASM upgrade governance register: executable bytecode hash, timelocked migration delays, and multi-sig authorization quorum.
- **soroban-contract-audit** — Soroban smart contract security audit register: authorization checks, panic pathways, integer overflows, and storage footprint verification for Stellar.
- **soroban-liquidity-pool** — Automated market maker liquidity pool register: constant-product invariant curves, swap fee tiers, and LP token shares for Soroban DeFi.
- **soroban-oracle-data-feed-audit** — DeFi price oracle integration and safety audit register: heartbeat bounds, stale price threshold reversion, and TWAP medianizer validation.
- **soroban-storage-ttl-lifecycle** — Soroban ledger state rent and TTL extension register: live state tracking, bump thresholds, rent fee reserves, and archive boundaries.
- **soroban-token-minter** — Soroban SEP-41 token contract architecture register: admin control, supply caps, metadata standard, and transfer event emissions on Stellar.
- **stellar-anchor-integration** — Stellar anchor protocol compliance register: SEP-10 web authentication, SEP-24 interactive deposit and withdrawal, and KYC lifecycle.
- **stellar-asset-clawback-compliance** — Regulated Stellar asset clawback architecture register: issuer authorization flags, claimable balance revocations, and regulatory audit trail.
- **stellar-escrow-timelock** — Decentralized conditional escrow and timelock contract register: multi-signature release conditions, clawback expiry, and settlement triggers.
- **stellar-multisig-threshold-coordinator** — Multi-signature signer and threshold coordination register: weight configurations, master key locks, and cosigner quorum thresholds for Stellar.
- **web3-rate-limiting-circuit-breaker** — On-chain and relayer rate-limiting circuit breaker register: throughput thresholds, emergency pause triggers, and multi-sig recovery.
- **web3-transaction-relayer-pool** — Gasless transaction relayer node pool register: fee sponsorship limits, nonce synchronization, and balance replenishment alerts.
- **zk-proof-verification-pipeline** — Zero-knowledge cryptographic verification pipeline register: proving system, circuit verification keys, public inputs, and gas costs.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/engineering/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/engineering`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
