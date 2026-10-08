---
name: economic-attack
description: >
  Auto-loaded by flashloan-auditor and defi-auditor agents during Phase 2.
  Provides detection patterns for: spot price manipulation, oracle staleness,
  short TWAP, donation attacks, slippage, flash loan governance.
  Core artifact: Price Flow Map.
user-invocable: false
---

# Economic Attack Vulnerability Analysis

**2025 Statistics**: Flash loans = **83.3% of DeFi exploits**, Oracle manipulation = **+31% YoY**, Price manipulation = **34.3% of MUBs**.

---

## Attacker Mindset: Infinite Capital

**CRITICAL**: With flash loans, attackers have **INFINITE CAPITAL** for one transaction.

```
+------------------------------------------------------------------+
|                  SINGLE ATOMIC TRANSACTION                        |
+------------------------------------------------------------------+
|  1. BORROW    | Flash loan $100M+ from Aave/dYdX (cost: 0.09%)   |
|  2. MANIPULATE| Change any on-chain value (price, balance, ratio) |
|  3. EXPLOIT   | Call target function with manipulated state       |
|  4. PROFIT    | Extract value (mint, borrow, swap at bad rate)   |
|  5. REPAY     | Return flash loan + fee                          |
|  6. KEEP      | Attacker keeps profit, victims lose funds        |
+------------------------------------------------------------------+
```

**Key insight**: If ANY step fails, entire transaction reverts. Attacker loses only gas (~$50).
This means attackers can try complex attacks with zero risk.

---

## Why Economic Attacks Happen (Root Causes)

### Root Cause 1: Single Source Price Dependency

Protocol trusts ONE price source that attacker can manipulate.

```solidity
// VULNERABLE: Single DEX pool as price source
function getPrice() public view returns (uint256) {
    (uint112 r0, uint112 r1,) = uniswapPair.getReserves();
    return uint256(r1) * 1e18 / uint256(r0);  // @audit Flash loan can drain r0
}
```

**Attacker's view**: "I can move this price with enough capital. Flash loan gives me that capital."

### Root Cause 2: Spot Price Trust

Using current-moment values instead of time-averaged values.

```solidity
// VULNERABLE: Current block's reserves
price = reserves[1] / reserves[0];  // @audit Reflects THIS transaction's state

// What attacker sees:
// 1. Swap to move reserves
// 2. Read manipulated price
// 3. Exploit protocol
// 4. Swap back
// All in one tx!
```

**Detection**: Any `getReserves()`, `slot0()`, `balanceOf()` used for pricing is suspect.

### Root Cause 3: Staleness Blindness

Oracle price could be hours or days old, but protocol uses it anyway.

```solidity
// VULNERABLE: No staleness check
(, int256 price,,,) = chainlinkFeed.latestRoundData();
return uint256(price);  // @audit Could be from yesterday!

// Attacker's opportunity:
// - Wait for oracle to become stale during volatility
// - Real price moved 20%, oracle still shows old price
// - Liquidate users at wrong price, or borrow too much
```

**Detection**: `latestRoundData()` without checking `updatedAt` timestamp.

### Root Cause 4: Composability Trust

Protocol blindly trusts external protocol's reported values.

```solidity
// VULNERABLE: Trusting external vault's totalAssets
function getCollateralValue(address user) view returns (uint256) {
    uint256 shares = externalVault.balanceOf(user);
    uint256 pricePerShare = externalVault.totalAssets() / externalVault.totalSupply();
    return shares * pricePerShare;  // @audit totalAssets can be donated to!
}
```

**Attacker's view**: "I can donate to that vault and inflate pricePerShare, then borrow against it."

---

## The Price Flow Map (Core Artifact)

Trace how prices flow through the system:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Price Source   │ ──► │ Reading Function │ ──► │ Critical Decision│
│ (Oracle/DEX)    │     │ (getPrice, etc) │     │ (liquidate,mint)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                                                │
        ▼                                                ▼
   Manipulable?                                   Value Transfer
   - Flash loan?                                  (funds move)
   - Donation?
   - Time window?
```

Document each price dependency:

| Function | Price Source | Manipulable? | Impact if Manipulated |
|----------|--------------|--------------|----------------------|
| liquidate() | Chainlink ETH/USD | Staleness only | Unfair liquidations |
| borrow() | Uniswap reserves | Flash loan | Undercollateralized borrow |
| mint() | vault.totalAssets() | Donation | Steal other users' deposits |

---

## Detection Patterns

### Pattern 1: Spot Price Dependency (Most Critical)

**Root Cause**: Single Source + Spot Price Trust

```solidity
// VULNERABLE: Direct reserve ratio
function getTokenPrice() public view returns (uint256) {
    (uint112 r0, uint112 r1,) = pair.getReserves();
    return uint256(r1) * 1e18 / uint256(r0);  // @audit Instant manipulation
}
```

**Attack Flow**:
1. Flash loan large amount of token0
2. Swap to drain token0 from pool → price spikes
3. Call victim function that reads this price
4. Profit at inflated price
5. Swap back, repay flash loan

**Search Queries**:
```
Grep("getReserves|slot0|observe", glob="**/*.sol")
Grep("reserve0|reserve1|liquidity", glob="**/*.sol")
```

**Verification Questions**:
- Is this price used for critical decisions?
- Can flash loan move this price significantly?
- Is there enough liquidity to resist manipulation?

### Pattern 2: Oracle Staleness

**Root Cause**: Staleness Blindness

```solidity
// VULNERABLE: No freshness validation
function getPrice() external view returns (uint256) {
    (, int256 price,,,) = priceFeed.latestRoundData();
    return uint256(price);  // @audit Could be stale!
}

// Attack opportunity:
// During high volatility, oracle updates lag
// Real ETH = $3000, Oracle still says $2500
// Attacker borrows at $2500 collateral value
// Immediately has undercollateralized position
```

**Search Queries**:
```
Grep("latestRoundData|latestAnswer", glob="**/*.sol")
Grep("updatedAt|answeredInRound", glob="**/*.sol")
```

**Verification Questions**:
- Is `updatedAt` checked against a max staleness?
- What's the heartbeat of this oracle?
- What happens during oracle downtime?

### Pattern 3: Short TWAP Window

**Root Cause**: Insufficient time averaging

```solidity
// VULNERABLE: 1 minute TWAP
uint32[] memory secondsAgos = new uint32[](2);
secondsAgos[0] = 60;   // @audit Only 60 seconds!
secondsAgos[1] = 0;
(int56[] memory tickCumulatives,) = pool.observe(secondsAgos);
```

**Attacker's view**: "I can maintain manipulated price for 60 seconds across multiple blocks if I'm a validator, or use multiple flash loans."

**Safe TWAP windows**:
- Minimum: 30 minutes (1800 seconds)
- Recommended: 1-4 hours for high-value decisions

**Search Queries**:
```
Grep("observe|consult|TWAP|twap", glob="**/*.sol")
Grep("secondsAgo|period|window", glob="**/*.sol")
```

### Pattern 4: Donation Attack / Share Inflation

**Root Cause**: Composability Trust + Spot Value

```solidity
// VULNERABLE: totalAssets includes donations
function totalAssets() public view returns (uint256) {
    return token.balanceOf(address(this));  // @audit Donatable!
}

function pricePerShare() public view returns (uint256) {
    return totalAssets() * 1e18 / totalSupply();  // @audit Inflatable!
}
```

**Attack Flow**:
1. Deposit 1 wei → get 1 share (first depositor)
2. Donate 1M tokens directly to vault (not via deposit)
3. pricePerShare = 1M / 1 = 1M per share
4. Victim deposits 999K → gets 0 shares (rounds down)
5. Attacker redeems 1 share → gets everything

**Search Queries**:
```
Grep("balanceOf\\(address\\(this\\)\\)", glob="**/*.sol")
Grep("totalAssets|totalSupply", glob="**/*.sol")
Grep("pricePerShare|exchangeRate", glob="**/*.sol")
```

### Pattern 5: Missing Slippage Protection

**Root Cause**: No minimum output enforcement

```solidity
// VULNERABLE: amountOutMin = 0
router.swapExactTokensForTokens(
    amountIn,
    0,  // @audit Sandwich target!
    path,
    msg.sender,
    block.timestamp
);
```

**Attack Flow** (Sandwich):
1. See victim's pending swap in mempool
2. Front-run: buy token, raise price
3. Victim's swap executes at worse price
4. Back-run: sell token at higher price
5. Profit from victim's slippage

**Search Queries**:
```
Grep("amountOutMin|minAmountOut|minOut", glob="**/*.sol")
Grep("swapExact|swap\\(", glob="**/*.sol")
```

### Pattern 6: Flash Loan Governance

**Root Cause**: Snapshot at call time

```solidity
// VULNERABLE: Current balance for voting power
function propose(bytes calldata action) external {
    uint256 votes = token.balanceOf(msg.sender);  // @audit Current!
    require(votes >= proposalThreshold);
    // Attacker: flash loan tokens → propose → return
}

function vote(uint256 proposalId, bool support) external {
    uint256 votes = token.balanceOf(msg.sender);  // @audit Current!
    proposals[proposalId].votes += votes;
    // Attacker: flash loan → vote → return
}
```

**Search Queries**:
```
Grep("balanceOf.*vote|vote.*balanceOf", glob="**/*.sol")
Grep("propose|quorum|threshold", glob="**/*.sol")
```

---

## Flash Loan Exploitability Checklist

For each value used in critical decisions:

- [ ] Can this value be changed within one transaction?
- [ ] Does flash loan provide enough capital to move it significantly?
- [ ] Is the value read and used in the same transaction?
- [ ] Is there a time delay between read and use?
- [ ] Are there circuit breakers for extreme values?

---

## Price Source Risk Matrix

| Source Type | Manipulation Risk | Attack Vector |
|-------------|-------------------|---------------|
| DEX Spot (getReserves) | **CRITICAL** | Flash loan swap |
| Uniswap V3 slot0 | **CRITICAL** | Flash loan swap |
| TWAP < 10 min | **HIGH** | Multi-block or validator |
| TWAP 10-30 min | **MEDIUM** | Validator collusion |
| TWAP > 30 min | **LOW** | Expensive sustained attack |
| Chainlink (no staleness) | **HIGH** | Wait for stale price |
| Chainlink (with staleness) | **LOW** | Limited window |
| balanceOf(this) | **HIGH** | Direct donation |

---

## Search Query Reference

```
# Find price sources
Grep("getReserves|slot0|observe|latestRoundData", glob="**/*.sol")
Grep("getPrice|price\\(\\)|oracle", glob="**/*.sol")

# Find manipulable values
Grep("balanceOf\\(address\\(this\\)\\)", glob="**/*.sol")
Grep("totalAssets|totalSupply|pricePerShare", glob="**/*.sol")

# Find flash loan interactions
Grep("flashLoan|flash\\(|executeOperation", glob="**/*.sol")
Grep("onFlashLoan|IERC3156", glob="**/*.sol")

# Find vulnerable swaps
Grep("amountOutMin.*=.*0|minAmount.*=.*0", glob="**/*.sol")
Grep("swapExact|swap\\(", glob="**/*.sol")

# Find governance
Grep("propose|vote|quorum|snapshot", glob="**/*.sol")
```

---

## Rationalization Table (Reject These Excuses)

| Excuse | Attacker's Reality |
|--------|-------------------|
| "Flash loans are expensive" | 0.09% fee on $100M = $90K. Profit can be millions. |
| "Pool has high liquidity" | Higher liquidity = need bigger flash loan. Still doable. |
| "TWAP protects us" | Short TWAP < 10min is still manipulable. Check the window. |
| "No one would do this" | MEV bots automate attacks 24/7. They're already looking. |
| "Chainlink is always accurate" | Chainlink can be stale. Always check `updatedAt`. |
| "This is theoretical" | Cetus ($223M), Euler ($197M), Mango ($114M), KiloEx ($117M) |
| "Attack would cost too much" | Flash loan cost is near zero. Only gas at risk. |
