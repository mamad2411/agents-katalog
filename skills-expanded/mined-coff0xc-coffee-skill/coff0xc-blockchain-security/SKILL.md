---
name: coff0xc-blockchain-security
description: "Use when the user requests blockchain, smart contract, DeFi/Web3, or multi-chain security: Solidity/EVM, Solana, Cosmos, Substrate, Cairo/StarkNet, TON, Algorand, AMM, oracle, bridge, token/NFT, Foundry/Hardhat/Slither, asset flows, and permissions. Manual trigger: Use coff0xc-blockchain-security."
---

# coff0xc-blockchain-security

<!-- skill-id: cs-bcs-d2a58f13 -->

## Quick Rules (read this first for everyday tasks)
> **[Asset flow first]** Look first at permissions, fund flows, state machines, price sources, external calls, and upgrade/governance paths.
> **[Evidence gate]** Tie every finding to a contract/function/line number, preconditions, affected assets, and a verifiable test.
> **[Fix loop]** Prefer minimal patches, property/unit tests, simulated attacks, and deployment/migration risk notes.
> **[Hard boundary]** Confirm first for mainnet transactions, private keys, real funds, unauthorized contract interaction, public disclosure, and MEV operations.

Follow this section first for ordinary on-chain/contract audits; expand the full workflow only for mainnet response, cross-chain incidents, or full economic-model review.

## Capability
Security-audit capability for blockchain, smart contracts, DeFi, and multi-chain projects. The focus is fund flows, permissions, state transitions, oracles, cross-chain behavior, and test coverage.

## What It Can Deliver
- Contract entry-point and permission-model inventory
- Asset-flow, state-machine, price-source, and external-call risks
- Vulnerability findings, impact, PoC ideas, and remediation recommendations
- Foundry/Hardhat/chain-specific test or audit checklists

## What Input It Can Take
- Solidity/Rust/CosmWasm/Cairo/TON/Algorand contracts
- Tests, deployment scripts, whitepapers, economic models, audit reports
- Transaction samples, event logs, configuration, and permission notes

## Safe-Use Boundaries
- Handle only authorized code and test/local-chain verification
- Real on-chain operations, private keys, fund movement, and public exploits must be confirmed first or refused
- Do not treat a theoretical vulnerability as verified fund risk
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Identifies asset and permission boundaries first
- Applies the matching security checks per chain and framework
- Every finding states reachability, impact, and test recommendations

## Typical Usage
```text
Use coff0xc-blockchain-security to audit this Solidity contract's permissions, asset flow, and price sources.
Use coff0xc-blockchain-security to check this Solana program's PDA, signer, and CPI risks.
Use coff0xc-blockchain-security to review this DeFi protocol and propose Foundry tests.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
