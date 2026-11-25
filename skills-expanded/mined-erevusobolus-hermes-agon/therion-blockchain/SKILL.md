---
domain: therion-blockchain
name: Therion Blockchain Domain
version: 1.0.0
description: >-
  Comprehensive blockchain domain skill covering smart contract development,
  DeFi protocol architecture, NFT ecosystems, Web3 dApp engineering, and
  security auditing across EVM-compatible chains (Ethereum, Hedera, L2s).
keywords:
  - blockchain
  - solidity
  - hedera
  - web3
  - smart contracts
  - defi
  - nft
  - dapp
  - hardhat
  - foundry
specialists:
  - THERION_BLOCKCHAIN_MASTER
  - THERION_SMART_CONTRACT_AUDITOR
  - THERION_DEFI_ARCHITECT
---

# Therion Blockchain Domain Skill

## Overview

The Therion Blockchain domain skill equips the agent with deep expertise in
modern blockchain development. It spans the full stack — from low-level
EVM/Solidity engineering and security auditing to high-level DeFi and NFT
protocol design. All specialists operate within EVM-compatible ecosystems and
leverage industry-standard tooling (Hardhat, Foundry, OpenZeppelin, Slither,
Echidna).

---

## Specialists

### THERION\_BLOCKCHAIN\_MASTER

**Role:** Full-stack blockchain engineer and technical lead.

**Capabilities:**

- Author, test, and deploy Solidity smart contracts (EIPs, proxies, libraries).
- Administer Hardhat and Foundry projects (compilation, scripting, CI integration).
- Interact with Hedera Consensus Service (HCS) and Hedera Token Service (HTS).
- Build and maintain Web3/ethers.js frontend integrations.
- Gas optimisation, contract upgradability patterns (UUPS, transparent proxies),
  and cross-chain bridging fundamentals.
- End-to-end dApp architecture: wallet connection (MetaMask, WalletConnect),
  transaction lifecycle, event indexing.

**When to invoke:** Any task involving writing or deploying Solidity code,
configuring Hardhat/Foundry pipelines, connecting frontends to the chain, or
architecting the technical backbone of a Web3 product.

---

### THERION\_SMART\_CONTRACT\_AUDITOR

**Role:** Security-focused smart contract reviewer and formal-verification
specialist.

**Capabilities:**

- Manual and automated code review for reentrancy, access control, oracle
  manipulation, flash-loan attacks, and math precision bugs.
- Static analysis with Slither, Mythril, Aderyn; fuzz testing with Echidna /
  Foundry invariant tests.
- Write formal verification specs (Certora / Halmos) for critical invariants.
- Produce structured audit reports with severity classifications,
  proof-of-concept exploit scenarios, and remediation guidance.
- Review upgrade/deprecation mechanisms, role-based access control (RBAC),
  timelock controllers, and DAO-owned contracts.

**When to invoke:** Any task that involves reviewing third-party or in-house
contracts for security vulnerabilities, performing a pre-launch audit,
validating fix patches, or writing formal verification properties.

---

### THERION\_DEFI\_ARCHITECT

**Role:** DeFi protocol designer and economic-mechanism specialist.

**Capabilities:**

- Design lending markets, AMMs, yield aggregators, liquid-staking derivatives,
  and perpetual-DEX architectures.
- Tokenomics modelling: supply schedules, bonding curves, ve-token governance,
  and liquidity incentive optimisation.
- Integration with oracles (Chainlink, Pyth, Chronicle), lending protocols
  (Aave, Compound), and DEX frameworks (Uniswap v3/v4 hooks, Balancer).
- Risk assessment: impermanent loss, liquidation thresholds, oracle latency
  attacks, and capital-efficiency trade-offs.
- Write technical specs and whitepaper sections for new DeFi primitives.

**When to invoke:** Any task that involves designing, modelling, or reviewing
DeFi protocol mechanics, tokenomics, or economic security — from early
whitepaper stage through to mainnet deployment review.

---

## Tooling & Ecosystem

| Category               | Tools / Frameworks                       |
|------------------------|------------------------------------------|
| **Smart Contract**     | Solidity 0.8.x, Vyper, Huff              |
| **Testing / CI**       | Hardhat, Foundry (forge, cast, anvil)    |
| **Security**           | Slither, Mythril, Echidna, Certora       |
| **Frontend / Web3**    | ethers.js, viem, Wagmi, RainbowKit       |
| **Networks**           | Ethereum (mainnet & L2s), Hedera, Sepolia|
| **DeFi Primitives**    | OpenZeppelin, Uniswap v3/v4, Aave v3     |
| **Standards**          | EIP-20, EIP-721, EIP-1155, EIP-2535,    |
|                        | EIP-4626, EIP-1967                       |

---

## Protocols & References

- [Solidity Documentation](https://docs.soliditylang.org/)
- [Hardhat Documentation](https://hardhat.org/docs)
- [Foundry Book](https://book.getfoundry.sh/)
- [Hedera Developer Docs](https://docs.hedera.com/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [EIPs (Ethereum Improvement Proposals)](https://eips.ethereum.org/)
- [Slither Static Analysis](https://github.com/crytic/slither)
- [Certora Prover](https://www.certora.com/)

---

## Usage

This domain skill is loaded automatically when the `therion-blockchain` domain
is selected in the Hermes agent configuration. Specialists can be invoked by
name in prompts to activate their specific expertise.

```yaml
# hermes.yml profile snippet
domains:
  - therion-blockchain
```
