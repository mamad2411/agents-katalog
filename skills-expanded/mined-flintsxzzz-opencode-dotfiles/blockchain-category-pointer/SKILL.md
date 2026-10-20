---
name: blockchain-category-pointer
description: "Pointer to a library of 7 specialized Blockchain skills. Use when working on blockchain-related tasks."
risk: none
---

# Blockchain Capability Library 🎯

This is a **pointer skill**. The 7 specialized Blockchain skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **blockchain-developer** — Build production-ready Web3 applications, smart contracts, and decentralized systems. Implements DeFi protocols, NFT platforms, DAOs, and enterprise blockchain integrations.
- **crypto-bd-agent** — Production-tested patterns for building AI agents that autonomously discover, > evaluate, and acquire token listings for cryptocurrency exchanges.
- **defi-protocol-templates** — Implement DeFi protocols with production-ready templates for staking, AMMs, governance, and lending systems. Use when building decentralized finance applications or smart contract protocols.
- **lightning-architecture-review** — Review Bitcoin Lightning Network protocol designs, compare channel factory approaches, and analyze Layer 2 scaling tradeoffs. Covers trust models, on-chain footprint, consensus requirements, HTLC/PTLC compatibility, liveness, and watchtower support.
- **lightning-channel-factories** — Technical reference on Lightning Network channel factories, multi-party channels, LSP architectures, and Bitcoin Layer 2 scaling without soft forks. Covers Decker-Wattenhofer, timeout trees, MuSig2 key aggregation, HTLC/PTLC forwarding, and watchtower breach detection.
- **lightning-factory-explainer** — Explain Bitcoin Lightning channel factories and the SuperScalar protocol — scalable Lightning onboarding using shared UTXOs, Decker-Wattenhofer trees, timeout-signature trees, MuSig2, and Taproot. No soft fork required.
- **web3-testing** — Master comprehensive testing strategies for smart contracts using Hardhat, Foundry, and advanced testing patterns.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/blockchain/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/blockchain`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
