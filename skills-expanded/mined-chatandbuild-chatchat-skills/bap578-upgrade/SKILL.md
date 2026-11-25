---
id: bap578-upgrade
name: BAP-578 Contract Upgrade
description: Use this skill when planning, implementing, testing, or executing safe BAP-578 contract upgrades with the UUPS proxy pattern, including storage layout discipline, V2 implementations, deployment, and rollback planning.
category: Blockchain
author: community
version: 1.0.0
---

# BAP-578 Contract Upgrade

Use this skill to plan, implement, test, and execute safe upgrades to deployed BAP-578 contracts using the UUPS (Universal Upgradeable Proxy Standard) pattern. This skill covers storage layout discipline, writing V2+ implementations, upgrade testing strategies, deployment procedures, and rollback planning.

---

## When to use this skill

- Adding new features to a deployed BAP-578 contract.
- Fixing bugs in the deployed implementation.
- Understanding how UUPS upgrades work.
- Writing a V2 implementation that preserves existing state.
- Testing upgrades before mainnet execution.
- Planning rollback strategies for failed upgrades.
- Reviewing upgrade safety as part of a security audit.

---

## The Four Identity Questions (Upgrade View)

### 1) Who are you?

The upgrade mechanism is the evolution layer for the contract. It allows the contract logic to change while keeping the same proxy address, the same token IDs, the same balances, and the same metadata. Users interact with the same address before and after an upgrade — their agents, funds, and identities are preserved.

### 2) What do you remember?

Proxy state is preserved across upgrades because storage lives in the proxy contract, not the implementation. All existing data — agent metadata, balances, ownership, free mint records, treasury address — remains intact. The new implementation simply provides updated logic for reading and writing that same storage.

### 3) What can you do?

Upgrades can add new features, fix bugs, optimize gas usage, and extend the contract's capabilities. Specific examples:

- Add new metadata fields (requires storage-safe pattern)
- Add new administrative functions
- Fix discovered vulnerabilities
- Add ERC-2981 royalty support
- Implement dynamic pricing logic
- Add new events for better indexing
- Optimize gas for existing functions

### 4) How can I trust it?

Upgrades are restricted to the contract owner via `_authorizeUpgrade`. Trust is maintained by:

- Owner-only upgrade authorization
- Testnet deployment and verification before mainnet
- Storage layout validation (automated tools available)
- Community review of upgrade code
- Transparent upgrade announcements
- Time-locked upgrades (if implemented)

---

## UUPS Proxy Pattern Explained

### How it works

```
User → Proxy Contract (fixed address) → Implementation Contract (replaceable)
              ↓                                    ↓
        Storage lives here                  Logic lives here
        (never changes address)             (can be swapped)
```

The proxy delegates all calls to the current implementation using `delegatecall`. This means the implementation's code runs in the context of the proxy's storage. When you upgrade, you deploy a new implementation and tell the proxy to point to it.

### Key components

- **Proxy:** holds all storage, delegates calls to implementation
- **Implementation V1:** current logic contract
- **Implementation V2:** new logic contract (deployed separately)
- **`_authorizeUpgrade`:** function that gates who can trigger upgrades

### Why UUPS over Transparent Proxy?

UUPS puts the upgrade logic in the implementation, not the proxy. Benefits:
- Smaller proxy contract (cheaper to deploy)
- Upgrade logic can be removed in future versions if desired
- More gas-efficient for normal operations

---

## Storage Layout Rules

The single most critical rule for safe upgrades:

**NEVER reorder, rename, or remove existing state variables. Only append new variables at the end.**

### Safe storage changes

```solidity
// V1 storage
contract NonFungibleAgentsV1 {
    uint256 private _totalSupply;
    mapping(uint256 => AgentState) private _agents;
    mapping(uint256 => AgentMetadata) private _metadata;
    address private _treasury;
    bool private _paused;
}

// V2 storage — SAFE: only appended new variables
contract NonFungibleAgentsV2 is NonFungibleAgentsV1 {
    // New variables appended after all V1 variables
    uint256 private _royaltyBps;
    mapping(uint256 => uint256) private _agentReputation;
}
```

### Unsafe storage changes

```solidity
// V2 storage — DANGEROUS: reordered variables
contract NonFungibleAgentsV2 {
    bool private _paused;           // MOVED — was 5th, now 1st
    uint256 private _totalSupply;   // SHIFTED — storage slot changed
    // This will corrupt ALL existing data
}
```

### Storage gap pattern

Reserve storage slots for future use in the base contract:

```solidity
contract NonFungibleAgentsV1 {
    uint256 private _totalSupply;
    mapping(uint256 => AgentState) private _agents;
    // ... other variables

    // Reserve 50 slots for future upgrades
    uint256[50] private __gap;
}
```

When adding new variables in V2, reduce the gap:

```solidity
contract NonFungibleAgentsV2 is NonFungibleAgentsV1 {
    uint256 private _royaltyBps;
    // Gap reduced by 1 (from 50 to 49)
    uint256[49] private __gap;
}
```

---

## Writing a V2 Implementation

### Step-by-step process

**1. Inherit from V1:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./NonFungibleAgentsV1.sol";

contract NonFungibleAgentsV2 is NonFungibleAgentsV1 {
    // New state variables (appended only)
    uint256 private _royaltyBps;

    // New events
    event RoyaltyUpdated(uint256 newBps);

    // Reinitializer for V2-specific setup
    function initializeV2(uint256 royaltyBps) external reinitializer(2) {
        _royaltyBps = royaltyBps;
    }

    // New functions
    function setRoyalty(uint256 bps) external onlyOwner {
        require(bps <= 1000, "Max 10%");
        _royaltyBps = bps;
        emit RoyaltyUpdated(bps);
    }

    function getRoyalty() external view returns (uint256) {
        return _royaltyBps;
    }

    // Override existing functions if needed
    // Always call super for inherited behavior
}
```

**2. Use reinitializer (not initializer):**

The `initializer` modifier can only be called once (for V1). For subsequent versions, use `reinitializer(version)`:

```solidity
function initializeV2(uint256 param) external reinitializer(2) {
    // V2-specific initialization
}

function initializeV3(uint256 param) external reinitializer(3) {
    // V3-specific initialization
}
```

**3. Disable initializers in constructor:**

```solidity
constructor() {
    _disableInitializers();
}
```

---

## Testing Upgrades

### Testing strategy

1. **Unit test V2 functions** — test new features independently.
2. **Upgrade test** — deploy V1, populate state, upgrade to V2, verify state.
3. **Storage validation** — verify all V1 data is intact after upgrade.
4. **Access control test** — verify `_authorizeUpgrade` is still owner-only.
5. **Regression test** — run full V1 test suite against V2.

### Example upgrade test

```js
const { ethers, upgrades } = require("hardhat");
const { expect } = require("chai");

describe("Upgrade V1 → V2", function () {
  let nfa, nfaV2, owner, user;

  beforeEach(async function () {
    [owner, user] = await ethers.getSigners();

    // Deploy V1
    const V1 = await ethers.getContractFactory("NonFungibleAgentsV1");
    nfa = await upgrades.deployProxy(V1, [
      "Non-Fungible Agents",
      "NFA",
      owner.address, // treasury
    ], { kind: "uups" });

    // Create an agent in V1
    await nfa.createAgent(
      user.address,
      ethers.ZeroAddress,
      "ipfs://metadata",
      {
        persona: '{"name":"Test"}',
        experience: "Test agent",
        voiceHash: "",
        animationURI: "",
        vaultURI: "",
        vaultHash: ethers.ZeroHash,
      }
    );

    // Upgrade to V2
    const V2 = await ethers.getContractFactory("NonFungibleAgentsV2");
    nfaV2 = await upgrades.upgradeProxy(nfa.target, V2, {
      call: { fn: "initializeV2", args: [250] }, // 2.5% royalty
    });
  });

  it("preserves V1 state after upgrade", async function () {
    // Token still exists
    expect(await nfaV2.ownerOf(1)).to.equal(user.address);

    // Metadata intact
    const meta = await nfaV2.getAgentMetadata(1);
    expect(meta.experience).to.equal("Test agent");

    // Total supply unchanged
    expect(await nfaV2.getTotalSupply()).to.equal(1);
  });

  it("new V2 functions work", async function () {
    expect(await nfaV2.getRoyalty()).to.equal(250);

    await nfaV2.setRoyalty(500);
    expect(await nfaV2.getRoyalty()).to.equal(500);
  });

  it("V1 functions still work", async function () {
    // Can still mint
    await nfaV2.createAgent(
      user.address,
      ethers.ZeroAddress,
      "ipfs://metadata2",
      {
        persona: '{"name":"Test2"}',
        experience: "Another agent",
        voiceHash: "",
        animationURI: "",
        vaultURI: "",
        vaultHash: ethers.ZeroHash,
      }
    );
    expect(await nfaV2.getTotalSupply()).to.equal(2);
  });

  it("only owner can upgrade", async function () {
    const V2Again = await ethers.getContractFactory("NonFungibleAgentsV2", user);
    await expect(
      upgrades.upgradeProxy(nfaV2.target, V2Again)
    ).to.be.reverted;
  });
});
```

### Storage layout validation

Use Hardhat's upgrade plugin to validate storage compatibility:

```bash
npx hardhat run scripts/validate-upgrade.js
```

```js
const { upgrades } = require("hardhat");

async function main() {
  const V1 = await ethers.getContractFactory("NonFungibleAgentsV1");
  const V2 = await ethers.getContractFactory("NonFungibleAgentsV2");

  // This will throw if storage layout is incompatible
  await upgrades.validateUpgrade(V1, V2, { kind: "uups" });
  console.log("Storage layout is compatible ✓");
}
```

---

## Deployment Procedure

### Pre-upgrade checklist

- [ ] V2 code reviewed and tested
- [ ] All V1 tests pass against V2
- [ ] Storage layout validated (no collisions)
- [ ] `_authorizeUpgrade` is still owner-only in V2
- [ ] Reinitializer version is correct
- [ ] Testnet upgrade successful
- [ ] State verified on testnet after upgrade

### Mainnet upgrade steps

```bash
# 1. Deploy new implementation
npx hardhat run scripts/deploy-v2.js --network bsc

# 2. Verify on explorer
npx hardhat verify --network bsc NEW_IMPL_ADDRESS

# 3. Execute upgrade (via script or multisig)
npx hardhat run scripts/upgrade-to-v2.js --network bsc
```

### Post-upgrade verification

- [ ] Proxy address unchanged
- [ ] New implementation address recorded
- [ ] `owner()` returns correct address
- [ ] Existing agents queryable with correct data
- [ ] New V2 functions accessible
- [ ] Total supply unchanged
- [ ] Treasury address unchanged
- [ ] Test mint succeeds on upgraded contract

---

## Rollback Planning

### If upgrade fails on testnet

Simply redeploy V1 as a new implementation and upgrade back.

### If upgrade fails on mainnet

1. **Pause the contract** immediately (if possible).
2. **Deploy a V2-fix** implementation that corrects the issue.
3. **Upgrade to V2-fix** via the standard upgrade path.
4. **Unpause** after verification.

### If owner key is compromised

This is a critical scenario. Mitigations:

- Use a multisig as the contract owner.
- Implement a time-lock on upgrades (requires V2 feature).
- Monitor for unexpected `Upgraded` events.

---

## Common Upgrade Scenarios

### Scenario: Adding ERC-2981 Royalty Support

```solidity
contract NonFungibleAgentsV2 is NonFungibleAgentsV1, IERC2981 {
    uint256 private _royaltyBps;
    address private _royaltyReceiver;

    function initializeV2(address receiver, uint256 bps) external reinitializer(2) {
        _royaltyReceiver = receiver;
        _royaltyBps = bps;
    }

    function royaltyInfo(uint256, uint256 salePrice) external view returns (address, uint256) {
        uint256 royaltyAmount = (salePrice * _royaltyBps) / 10000;
        return (_royaltyReceiver, royaltyAmount);
    }

    function supportsInterface(bytes4 interfaceId) public view override returns (bool) {
        return interfaceId == type(IERC2981).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

Storage impact: 2 new variables appended. Safe.

### Scenario: Adding Dynamic Pricing

```solidity
contract NonFungibleAgentsV2 is NonFungibleAgentsV1 {
    uint256 private _tier1Fee;
    uint256 private _tier2Fee;
    uint256 private _tier1Threshold;

    function initializeV2(uint256 t1Fee, uint256 t2Fee, uint256 threshold) external reinitializer(2) {
        _tier1Fee = t1Fee;
        _tier2Fee = t2Fee;
        _tier1Threshold = threshold;
    }

    function getMintFee() public view returns (uint256) {
        if (getTotalSupply() < _tier1Threshold) return _tier1Fee;
        return _tier2Fee;
    }
}
```

Storage impact: 3 new variables appended. Safe.

### Scenario: Adding New Events

Adding events requires no storage changes — events are log entries, not state. Simply add the event declaration and emit it in the appropriate function:

```solidity
event AgentBurned(uint256 indexed tokenId, address indexed owner);

function burnAgent(uint256 tokenId) external {
    require(ownerOf(tokenId) == msg.sender, "Not token owner");
    require(getAgentState(tokenId).balance == 0, "Withdraw funds first");
    _burn(tokenId);
    emit AgentBurned(tokenId, msg.sender);
}
```

Storage impact: None. Safe.

### Scenario: Bug Fix

If a bug is found in an existing function, create V2 that overrides the function with the fix:

```solidity
contract NonFungibleAgentsV2 is NonFungibleAgentsV1 {
    function initializeV2() external reinitializer(2) {}

    // Override the buggy function with the fix
    function withdrawFromAgent(uint256 tokenId, uint256 amount) external override nonReentrant {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        require(amount > 0, "Amount must be > 0"); // NEW: added zero check
        AgentState storage agent = _agents[tokenId];
        require(amount <= agent.balance, "Insufficient balance");
        agent.balance -= amount;
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
        emit AgentWithdraw(tokenId, msg.sender, amount);
    }
}
```

---

## Upgrade Governance Patterns

### Timelock pattern

For production deployments, add a timelock to prevent instant upgrades:

1. Owner proposes an upgrade with a new implementation address.
2. A waiting period (e.g., 48 hours) must pass.
3. After the timelock expires, the upgrade can be executed.
4. During the waiting period, the community can review the new implementation.

This can be implemented via OpenZeppelin's TimelockController as the contract owner.

### Multisig pattern

Use a multisig wallet (e.g., Safe) as the contract owner:

- 2-of-3 or 3-of-5 signer threshold
- Upgrade proposals require multiple approvals
- Provides accountability and prevents single-key compromise

### Upgrade announcement protocol

Before any mainnet upgrade:

1. Publish the V2 source code for community review.
2. Deploy V2 implementation to testnet and verify.
3. Run full test suite against testnet upgrade.
4. Announce upgrade timeline with at least 48 hours notice.
5. Execute upgrade during low-activity period.
6. Verify immediately after upgrade.
7. Publish post-upgrade report.

---

## Troubleshooting Upgrades

### "Initializable: contract is already initialized"

The initializer was already called. Use `reinitializer(version)` for V2+ initialization.

### "ERC1967Upgrade: new implementation is not UUPS"

The new implementation doesn't inherit UUPSUpgradeable or doesn't implement `_authorizeUpgrade`. Verify the V2 contract inherits correctly.

### Storage layout incompatible

The OpenZeppelin upgrade plugin detected a storage collision. Review the variable ordering in V2 and ensure it matches V1 with only appended variables.

### "Only proxy can call this function"

Attempted to call an upgrade function on the implementation directly. Always interact via the proxy address.

---

## Output Format

When asked for upgrade help, respond with:

1. **Change summary** (what's being added/fixed)
2. **Storage layout notes** (what's safe, what's risky)
3. **Complete V2 code** (compilable Solidity)
4. **Test plan** (upgrade tests + regression)
5. **Deployment steps** (testnet → mainnet)
6. **Rollback strategy** (what to do if something goes wrong)

---

## Related Skills

- `bap578`
- `bap578-testing`
- `bap578-security-audit`
