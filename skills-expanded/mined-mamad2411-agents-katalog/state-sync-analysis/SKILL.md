---
name: state-sync-analysis
description: >
  Auto-loaded by reentrancy-auditor agent during Phase 2 for state sync analysis.
  Framework: "When can state become inconsistent? How can that gap be exploited?"
  Identifies state inconsistency windows during external calls, CEI violations,
  read-only reentrancy, cross-contract state manipulation.
user-invocable: false
---

# State Sync Analysis Framework

## Purpose

**"When can state become inconsistent? How can that gap be exploited?"**

Identify state inconsistency windows that occur during external calls and analyze attack vectors.

---

## 1. State Synchronization Dependencies

### 1.1 Same-Contract Dependencies

```solidity
// Dependencies between variables
uint256 totalSupply;       // A
uint256 totalAssets;       // B
// Invariant: B >= A * minRatio

// Risk: Inconsistency if A, B update order differs
```

### 1.2 Cross-Contract Dependencies

```solidity
// Contract A depends on Contract B state
function getCollateralValue() external view returns (uint256) {
    return token.balanceOf(address(this)) * oracle.getPrice();
    //     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^
    //     Contract A state                   Contract B state
}
```

### 1.3 View Function Dependencies

```solidity
// External protocol depends on our view function
function totalAssets() public view returns (uint256) {
    return s_depositedAssets + s_assetsInAMM;
}
// Other protocol: ourVault.totalAssets() to calculate collateral value
```

---

## 2. State Inconsistency Windows

### 2.1 State Timeline During External Call

```
Time T0: Initial state
├── s_depositedAssets = 1000
├── s_assetsInAMM = 500
└── totalAssets() = 1500

Time T1: withdraw() called → state updated
├── s_depositedAssets -= 100  ← Updated
└── s_assetsInAMM = 500

Time T2: External call (token.safeTransfer)
└── ⚠️ Callback possible!

Time T2.5: During callback (INCONSISTENCY WINDOW)
├── s_depositedAssets = 900 (updated)
├── Actual tokens: Not yet transferred (1000)
└── totalAssets() = 900 + 500 = 1400 ← WRONG!
    (Actual: 1000 + 500 = 1500)

Time T3: Transfer complete
└── State consistency restored
```

### 2.2 Inconsistency Window Types

| Type | Description | Risk Level |
|------|-------------|------------|
| **Pre-Update** | External call before state update | Critical |
| **Partial Update** | External call after partial state update | High |
| **Post-Update** | External call after all state updates | Low |

### 2.3 CEI Pattern and Inconsistency

```solidity
// SAFE: Checks → Effects → Interactions
function withdraw(uint256 amount) external {
    // Checks
    require(balances[msg.sender] >= amount);

    // Effects (state updates first)
    balances[msg.sender] -= amount;
    totalAssets -= amount;

    // Interactions (external calls last)
    token.safeTransfer(msg.sender, amount);
}

// DANGER: Checks → Interactions → Effects
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    token.safeTransfer(msg.sender, amount);  // @audit State inconsistent!
    balances[msg.sender] -= amount;          // Too late!
}
```

---

## 3. Timing Attack Patterns

### 3.1 Read-Only Reentrancy

```solidity
// Contract A (victim)
function totalAssets() public view returns (uint256) {
    return s_depositedAssets + s_assetsInAMM;
}

function withdraw(uint256 assets) external {
    s_depositedAssets -= assets;  // State updated

    // External call - callback occurs
    token.safeTransfer(msg.sender, assets);

    // During callback: totalAssets() returns stale value!
}

// Contract B (exploited by attacker)
function liquidate(address user) external {
    uint256 collateral = vaultA.totalAssets();  // @audit Manipulated!
    // If called during callback, gets lower collateral than actual
}
```

### 3.2 Cross-Contract State Race

```solidity
// When two contracts depend on same state
// Contract A: uses oracle.getPrice()
// Contract B: uses oracle.getPrice()

// Attack:
// 1. Call A.function() → reads oracle → external call
// 2. In callback, manipulate oracle
// 3. Call B.function() → reads manipulated oracle
// 4. A.function() returns → already corrupted
```

### 3.3 Flash Loan Timing

```solidity
// State manipulation within single transaction
flashLoanProvider.flashLoan(amount)
    → onFlashLoan() callback
        → manipulate pool reserves
        → call vulnerable function (sees manipulated state)
        → restore reserves
    → repay flash loan
```

---

## 4. State Dependency Graph Template

```
┌──────────────────────────────────────────────────┐
│              State Dependency Graph              │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────┐      reads       ┌─────────────┐   │
│  │ Vault   │ ───────────────► │ Price Oracle │   │
│  │ .sol    │                  └─────────────┘   │
│  └────┬────┘                         ▲          │
│       │                              │ manipulate│
│       │ callback                     │          │
│       ▼                        ┌─────┴─────┐    │
│  ┌─────────┐      reads       │ Attacker  │    │
│  │ Token   │ ◄──────────────  │ Contract  │    │
│  │ .sol    │                  └───────────┘    │
│  └─────────┘                                    │
│                                                  │
│  Risk Path: Vault → callback → Attacker → Oracle│
│            → Vault reads manipulated Oracle     │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 5. Output Format

```markdown
## State Sync Analysis Results

### State Dependencies

| Contract | Function | Dependent State | External Source |
|----------|----------|-----------------|-----------------|
| Vault | getCollateralValue | totalAssets | Oracle.getPrice |
| Pool | swap | reserves | Token.balanceOf |

### Inconsistency Windows

| Location | Function | External Call | Inconsistent Variable | CEI Compliant |
|----------|----------|---------------|----------------------|---------------|
| Vault.sol:142 | withdraw | safeTransfer | s_deposited | ❌ |
| Pool.sol:89 | deposit | transferFrom | userShares | ⚠️ |

### Timing Attack Scenarios

#### Read-Only Reentrancy via totalAssets()
```
T0: Vault.withdraw(100) called
T1: s_depositedAssets = 1000 → 900
T2: token.safeTransfer() → callback
T3: [CALLBACK] ExternalProtocol.liquidate() called
    → Vault.totalAssets() = 900 + 500 = 1400 (actual: 1500)
    → Liquidation with incorrect collateral valuation
T4: Transfer complete
```

- **Impact**: Incorrect collateral valuation in external protocol
- **Risk Level**: High
```

---

## 6. Search Queries

```
# Find external calls
Grep("\\.call\\{|\\.transfer\\(|safeTransfer", glob="**/*.sol")

# Find state updates after external calls (DANGER)
Grep("transfer.*\\n.*-=|safeTransfer.*\\n.*-=", glob="**/*.sol")

# Find view functions (read-only reentrancy risk)
Grep("view.*returns.*totalAssets|view.*returns.*totalSupply", glob="**/*.sol")

# Find token callbacks
Grep("tokensReceived|onERC721Received|onERC1155Received", glob="**/*.sol")
```

---

## 7. Attacker Mindset

- "What state can be read during callbacks?"
- "If read state differs from actual, what can I gain?"
- "Does an external protocol trust our view functions?"
- "Can I sandwich the state inconsistency window?"
