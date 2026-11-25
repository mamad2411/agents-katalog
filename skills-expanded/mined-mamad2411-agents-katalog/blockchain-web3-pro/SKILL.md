---
name: blockchain-web3-pro
description: "Smart contracts, dApps, DeFi, NFT, testing, security, gas optimization. Use when building or auditing Web3 or blockchain projects."
---

# Blockchain & Web3 Pro

## Purpose

Build secure, efficient blockchain applications. Covers Solidity smart contracts, dApp architecture, DeFi patterns, gas optimization, testing, and security auditing.

## When to Use

**Use this when:**
- Writing or reviewing Solidity smart contracts, dApp frontends, or DeFi protocol integrations
- Designing token economics, NFT minting mechanics, or on-chain governance systems
- Setting up a Hardhat/Foundry project with testing, deployment scripts, and Etherscan verification

**Use this ESPECIALLY when:**
- Any contract holds or transfers user funds — reentrancy, access control, and CEI pattern compliance are non-negotiable
- Gas costs are a product concern (high-frequency interactions, mass minting, batch operations)
- The contract will be upgraded post-deployment and a proxy pattern must be chosen and audited

**Don't skip when:**
- Integrating with external DeFi protocols (Uniswap, Aave, Chainlink) where price oracle manipulation or flash-loan attacks are realistic
- Deploying to mainnet for the first time and a formal Slither/Mythril audit has not been run
- The frontend relies on wallet connections and on-chain reads that need correct ABI and chain-ID handling

## Core Patterns

### 1. Smart Contract Structure (Solidity)

```solidity
// contracts/ProjectToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract ProjectToken is ERC20, Ownable, ReentrancyGuard {
    uint256 public constant MAX_SUPPLY = 1_000_000 * 10**18;
    mapping(address => uint256) public lastClaimed;

    event TokensClaimed(address indexed user, uint256 amount);

    constructor() ERC20("ProjectToken", "PRJ") Ownable(msg.sender) {}

    function claim() external nonReentrant {
        require(lastClaimed[msg.sender] == 0, "Already claimed");
        require(totalSupply() + 100 * 10**18 <= MAX_SUPPLY, "Exceeds max supply");

        lastClaimed[msg.sender] = block.timestamp;
        _mint(msg.sender, 100 * 10**18);
        emit TokensClaimed(msg.sender, 100 * 10**18);
    }

    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        (bool sent,) = owner().call{value: balance}("");
        require(sent, "Transfer failed");
    }
}
```

### 2. Gas Optimization

```solidity
// ❌ Expensive
function sumArray(uint[] memory arr) public pure returns (uint) {
    uint sum = 0;
    for (uint i = 0; i < arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}

// ✅ Cheaper (cache array length, unchecked increments)
function sumArray(uint[] calldata arr) public pure returns (uint) {
    uint sum = 0;
    uint len = arr.length;
    for (uint i = 0; i < len; ) {
        sum += arr[i];
        unchecked { i++; }
    }
    return sum;
}
```

### 3. Security Patterns

```solidity
// ✅ Checks-Effects-Interactions pattern (prevents reentrancy)
function withdraw() external nonReentrant {
    uint256 amount = balances[msg.sender];
    require(amount > 0, "No balance");

    // 1. Effects (state change first)
    balances[msg.sender] = 0;

    // 2. Interactions (external calls after)
    (bool sent,) = msg.sender.call{value: amount}("");
    require(sent, "Transfer failed");
}

// ✅ Access control
modifier onlyRole(bytes32 role) {
    require(hasRole(role, msg.sender), "Unauthorized");
    _;
}

// ✅ Emergency stop (circuit breaker)
bool public paused;
modifier whenNotPaused() { require(!paused, "Paused"); _; }
function pause() external onlyOwner { paused = true; }
function unpause() external onlyOwner { paused = false; }
```

### 4. Testing (Hardhat)

```typescript
import { expect } from 'chai'
import { ethers } from 'hardhat'

describe('ProjectToken', () => {
  it('should mint tokens on claim', async () => {
    const [owner, user] = await ethers.getSigners()
    const token = await ethers.deployContract('ProjectToken')

    await token.connect(user).claim()
    const balance = await token.balanceOf(user.address)
    expect(balance).to.equal(ethers.parseEther('100'))
  })

  it('should prevent double claim', async () => {
    const [_, user] = await ethers.getSigners()
    const token = await ethers.deployContract('ProjectToken')

    await token.connect(user).claim()
    await expect(token.connect(user).claim()).to.be.revertedWith('Already claimed')
  })

  it('should respect max supply', async () => {
    // Test edge case: minting at supply limit
  })
})
```

### 5. dApp Architecture

```
dapp/
  contracts/          ← Solidity source
  test/               ← Hardhat tests
  scripts/            ← Deployment scripts
  frontend/
    app/
      wallet/         ← Wagmi / Web3Modal
      contracts/
        hooks.ts      ← useProjectToken
        abi/          ← Generated ABIs
      components/
        ConnectWallet.tsx
        ClaimTokens.tsx
    lib/
      wagmi.ts        ← Chain config
  hardhat.config.ts
```

### Checklist

- [ ] OpenZeppelin contracts used (audited base)
- [ ] Checks-Effects-Interactions pattern in all mutating functions
- [ ] ReentrancyGuard on all value-transfer functions
- [ ] Access control (Ownable, AccessControl)
- [ ] Circuit breaker (pause/unpause)
- [ ] Gas optimization: calldata, unchecked, custom errors
- [ ] Slither / Mythril analysis passed
- [ ] Test coverage > 90% for all contracts
- [ ] Deployment script with verification (Etherscan)
- [ ] Upgradeability pattern (UUPS / Transparent proxy) documented
- [ ] Frontend: WalletConnect integration, transaction status UI

## Related Skills

- **security-reviewer** — broad application security for the off-chain backend and API layer that supports your dApp
- **frontend-senior-engineer** — React/Next.js dApp frontend patterns; pair when building the wallet-connected UI
- **backend-senior-engineer** — Node/Go indexer services, event listeners, and off-chain API that complement on-chain logic
- **code-reviewer** — RPC and REST API design for your dApp backend, event webhooks, and subgraph endpoints
- **test-engineer** — unit and integration test strategies; for contracts this means Hardhat/Foundry test suites and fork-testing against mainnet state
- **cloud-security-auditor** — secrets management for deployer private keys, node provider API keys, and multisig signer credentials
- **devops-release-engineer** — CI/CD pipelines that compile, test, and deploy contracts across testnets and mainnet with staged promotion
- **performance-engineer** — gas profiling, calldata compression, and batching strategies for high-throughput on-chain interactions

