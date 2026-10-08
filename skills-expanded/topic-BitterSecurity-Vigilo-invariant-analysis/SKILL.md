---
name: invariant-analysis
description: >
  Auto-loaded by logic-auditor agent during Phase 2 for invariant extraction.
  Framework: "What conditions must ALWAYS be true? How can they be violated?"
  Extracts protocol invariants from code/docs, systematically explores violation
  paths. Types: balance, state, accounting, access invariants.
user-invocable: false
---

# Invariant Analysis Framework

## Purpose

**"What conditions must ALWAYS be true? How can they be violated?"**

Systematically extract protocol invariants and explore violation paths where these conditions can be broken.

---

## 1. Invariant Types

### 1.1 Explicit Invariants

Directly verifiable in code:

```solidity
// require/assert conditions
require(totalSupply() == sum(balances), "Supply mismatch");
require(debt <= collateral * LTV / 100, "Undercollateralized");

// Documented conditions (NatSpec)
/// @invariant totalAssets >= totalSupply
/// @invariant userDebt[user] <= userCollateral[user] * LTV
```

### 1.2 Implicit Invariants

Must be inferred from code flow:

| Pattern | Implicit Invariant |
|---------|-------------------|
| `shares = deposit * totalSupply / totalAssets` | totalAssets > 0 when totalSupply > 0 |
| `balance[from] -= amount` | balance[from] >= amount |
| `rewardPerToken += reward / totalStaked` | totalStaked > 0 when reward > 0 |
| `collateralValue / debtValue >= LTV` | debtValue > 0 when loan exists |

### 1.3 Core Invariants by Protocol Type

| Protocol Type | Invariant Example |
|---------------|-------------------|
| **Vault** | `totalShares == 0 ↔ totalAssets == 0` |
| **AMM** | `reserveX * reserveY >= k` |
| **Lending** | `totalBorrowed <= totalDeposited * utilizationCap` |
| **Staking** | `sum(userStakes) == totalStaked` |
| **Bridge** | `mintedOnL2 == lockedOnL1` |

---

## 2. Invariant Extraction Process

### Step 1: Collect Explicit Conditions

```
Grep("require\\(|assert\\(|revert.*if", glob="**/*.sol")
Grep("@invariant|@notice.*must|@dev.*always", glob="**/*.sol")
```

### Step 2: Analyze State Variable Relationships

For each state variable:
1. Where is it modified? (setter functions)
2. Where is it read? (getter, calculation functions)
3. What relationships does it have with other variables?

| Variable | Modification Functions | Read Functions | Relationship |
|----------|----------------------|----------------|--------------|
| totalSupply | mint, burn | deposit, withdraw | == sum(balances) |
| totalAssets | deposit, withdraw, fee | convertToShares | >= totalSupply value |

### Step 3: Infer Implicit Conditions

Code flow analysis:

```solidity
// This code implicitly requires amount <= balance[from]
function transfer(address to, uint256 amount) {
    balance[from] -= amount;  // ← Reverts on underflow
    balance[to] += amount;
}
```

---

## 3. Violation Path Exploration

### 3.1 Single Function Violation

```
deposit(0) → shares = 0 * totalSupply / totalAssets = 0
→ User fund loss (asset deposited, no shares received)
```

### 3.2 Multi-Function Combination Violation

```
1. deposit(1 wei) → shares = 1
2. Direct asset transfer (donate) → totalAssets increases, totalSupply unchanged
3. Next user deposit(X) → shares = X * 1 / (1 + donated) ≈ 0
→ First depositor attack
```

### 3.3 State Transition Order Violation

```
Normal: initialize() → setOracle() → deposit()
Attack: deposit() (oracle not set) → price = 0 → infinite mint
```

### 3.4 Edge Case Violation

Test values:
- `0` - Zero value handling
- `1` - Minimum value
- `type(uint256).max` - Overflow
- `totalSupply == 0` - Initial state
- `balance == 0` - Empty account

---

## 4. Output Format

```markdown
## Invariant Analysis Results

### Extracted Invariants

| ID | Condition | Type | Maintenance Points |
|----|-----------|------|-------------------|
| INV-01 | totalSupply == sum(balances) | Explicit | mint, burn, transfer |
| INV-02 | totalAssets >= totalShares (by value) | Implicit | deposit, withdraw |
| INV-03 | userDebt <= userCollateral * LTV | Explicit | borrow, repay, liquidate |

### Potential Violation Paths

| Invariant | Violation Scenario | Risk Level |
|-----------|-------------------|------------|
| INV-02 | First depositor attack via donation | High |
| INV-03 | Oracle manipulation → forced liquidation | Critical |

### Detailed Analysis

#### INV-02 Violation: First Depositor Attack
- **Condition**: totalAssets / totalShares ratio can be manipulated
- **Path**: deposit(1) → donate(1M) → next user deposit results in shares = 0
- **Impact**: Subsequent depositor fund loss
- **Verification**: Check deposit() function
```

---

## 5. Search Queries

```
# Find explicit invariants
Grep("require\\(|assert\\(", glob="**/*.sol")
Grep("@invariant|must.*always|never.*allow", glob="**/*.sol")

# Find state variables
Grep("mapping.*=>.*uint|uint256.*public|uint256.*private", glob="**/*.sol")

# Find modification points
Grep("\\+=|-=|\\*=|/=|=", glob="**/*.sol")
```

---

## 6. Attacker Mindset

- "If this invariant breaks, can I steal funds?"
- "What function combination can bypass this invariant?"
- "Does this invariant hold in initial state (empty pool)?"
- "Can I force division by zero or overflow?"
