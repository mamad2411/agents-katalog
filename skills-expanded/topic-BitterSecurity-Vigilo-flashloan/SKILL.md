---
name: flashloan
description: >
  Auto-loaded by flashloan-auditor agent during Phase 2.
  Provides detection patterns for: price manipulation, governance manipulation,
  collateral manipulation, reward manipulation, oracle manipulation via flash loans.
  Core artifact: Flash Loan Attack Flow diagram.
user-invocable: false
---

# Flash Loan Attack Patterns

This skill provides comprehensive knowledge for identifying flash loan attack vulnerabilities in smart contracts.

## Overview

Flash loans provide unlimited capital for a single transaction. Any logic that depends on current state (balances, prices, voting power) without proper protection is potentially vulnerable.

## Attack Categories

### 1. Price Manipulation Attacks

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Spot price from AMM
function getPrice() public view returns (uint256) {
    (uint112 reserve0, uint112 reserve1,) = pair.getReserves();
    return reserve1 * 1e18 / reserve0;
}

function liquidate(address user) external {
    uint256 price = getPrice(); // Manipulable!
    uint256 collateralValue = collateral[user] * price;
    require(debt[user] > collateralValue, "Healthy");
    // Liquidate...
}
```

**Attack Flow:**
```
1. Flash loan large amount of token0
2. Dump into AMM → reserve1/reserve0 crashes
3. Call liquidate() at manipulated price
4. Buy back token0 cheap
5. Repay flash loan
6. Profit from unfair liquidation
```

**Detection:**
```
Grep("getReserves|slot0\\(\\)|sqrtPriceX96", glob="**/*.sol")
```

---

### 2. Governance Manipulation

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Balance-based voting
function castVote(uint256 proposalId, bool support) external {
    uint256 votes = token.balanceOf(msg.sender); // Flash loanable!
    _recordVote(proposalId, msg.sender, votes, support);
}
```

**Secure Pattern:**
```solidity
// Use snapshot at proposal creation
function castVote(uint256 proposalId, bool support) external {
    uint256 snapshotBlock = proposals[proposalId].snapshotBlock;
    uint256 votes = token.getPastVotes(msg.sender, snapshotBlock);
    _recordVote(proposalId, msg.sender, votes, support);
}
```

**Detection:**
```
Grep("balanceOf.*vote|vote.*balanceOf", glob="**/*.sol")
Grep("propose|castVote|delegate", glob="**/*.sol")
```

---

### 3. Collateral Manipulation

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Instant collateral increase
function borrow(uint256 amount) external {
    uint256 collateralValue = getCollateralValue(msg.sender);
    require(amount <= collateralValue * LTV, "Insufficient collateral");
    // Borrow...
}

function getCollateralValue(address user) public view returns (uint256) {
    return token.balanceOf(address(this)) * userShare[user] / totalShares;
    // ↑ Can be inflated with flash loan deposit
}
```

**Attack Flow:**
```
1. Flash loan tokens
2. Deposit as collateral → inflate collateralValue
3. Borrow maximum amount
4. Withdraw collateral
5. Repay flash loan (but keep borrowed funds)
```

---

### 4. Reward Manipulation

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Balance-based rewards
function claimRewards() external {
    uint256 share = token.balanceOf(msg.sender) * 1e18 / token.totalSupply();
    uint256 reward = pendingRewards * share;
    // Distribute reward...
}
```

**Detection:**
```
Grep("reward.*balanceOf|balanceOf.*reward", glob="**/*.sol")
Grep("claim|harvest|distribute", glob="**/*.sol")
```

---

### 5. Oracle Manipulation

**Vulnerable Pattern:**
```solidity
// DANGEROUS: On-chain oracle from DEX
function updatePrice() external {
    uint256 spotPrice = dex.getSpotPrice(token0, token1);
    lastPrice = spotPrice; // Can be manipulated!
}
```

**Mitigation:**
- Use TWAP with sufficient period (>= 30 minutes)
- Use manipulation-resistant oracles (Chainlink)
- Add price deviation checks

---

## Flash Loan Protection Patterns

### 1. Snapshot/Checkpoint Pattern
```solidity
// Record state at specific block
mapping(address => mapping(uint256 => uint256)) private _checkpoints;

function getPastBalance(address account, uint256 blockNumber)
    public view returns (uint256)
{
    require(blockNumber < block.number, "Future lookup");
    return _checkpoints[account][blockNumber];
}
```

### 2. Time-Weighted Average
```solidity
// TWAP resists single-block manipulation
function getTWAP(uint32 period) public view returns (uint256) {
    require(period >= MIN_TWAP_PERIOD, "Period too short");
    (int56[] memory tickCumulatives,) = pool.observe([period, 0]);
    int56 tickDelta = tickCumulatives[1] - tickCumulatives[0];
    return uint256(int256(tickDelta) / int256(uint256(period)));
}
```

### 3. Same-Block Check
```solidity
// Prevent same-block manipulation
mapping(address => uint256) private lastActionBlock;

modifier notSameBlock() {
    require(lastActionBlock[msg.sender] < block.number, "Same block");
    lastActionBlock[msg.sender] = block.number;
    _;
}
```

### 4. Minimum Lock Period
```solidity
// Require time commitment
mapping(address => uint256) private depositTime;

function withdraw() external {
    require(block.timestamp >= depositTime[msg.sender] + MIN_LOCK, "Locked");
    // Process withdrawal...
}
```

---

## Flash Loan Audit Checklist

- [ ] No balance-based voting without snapshots
- [ ] No spot price usage from AMMs
- [ ] Collateral changes have time delay or checks
- [ ] Reward distribution uses checkpoints
- [ ] TWAP period is sufficient (>= 30 min)
- [ ] Same-block price changes detected
- [ ] Governance has proposal delay

## Flash Loan Sources

| Protocol | Max Amount | Fee |
|----------|------------|-----|
| AAVE V3 | Pool liquidity | 0.05% |
| dYdX | Pool liquidity | 0% |
| Balancer | Pool liquidity | 0% |
| Uniswap V3 | Pool liquidity | Pool fee |
| Maker | DAI supply | 0% |

## Severity Classification

### Critical
- Balance-based governance without snapshot
- Spot price for liquidations
- Unbounded collateral manipulation

### High
- TWAP period < 10 minutes
- No same-block protection for sensitive ops
- Reward distribution manipulation

### Medium
- Flash loan callback allows arbitrary calls
- Incomplete snapshot coverage
