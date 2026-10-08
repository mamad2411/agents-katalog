---
name: asset-flow-analysis
description: >
  Auto-loaded by explorator (Phase 1) and sub-auditors (Phase 2) for asset mapping.
  Framework: "Where's the money? How does it move? Where can it leak?"
  Maps asset storage locations, movement paths, leakage points. Answers attacker's
  first question about protocol funds.
user-invocable: false
---

# Asset Flow Analysis Framework

## Purpose

**"Where is the money? How does it move? Where can it leak?"**

Systematically map asset storage, movement paths, and potential leakage points within a protocol.

---

## 1. Asset Storage Identification

### 1.1 ETH Storage

```solidity
// Direct balance
address(this).balance

// Wrapped ETH
WETH.balanceOf(address(this))
```

### 1.2 ERC20 Token Storage

```solidity
// Token balance
IERC20(token).balanceOf(address(this))

// Internal accounting variables
mapping(address => uint256) balances;
uint256 totalDeposited;
```

### 1.3 Share/LP Tokens

```solidity
// Minted amount
uint256 totalSupply;
mapping(address => uint256) shares;

// LP tokens
IUniswapV2Pair(pair).totalSupply();
IUniswapV2Pair(pair).balanceOf(address(this));
```

### 1.4 Asset Storage by Protocol Type

| Protocol Type | Asset Storage Pattern | Key Variables |
|---------------|----------------------|---------------|
| **Vault** | ERC20 balance + internal shares | totalAssets, totalSupply |
| **AMM/DEX** | reserve0, reserve1 | Token pair balances |
| **Lending** | deposits mapping + borrowed funds | totalDeposits, totalBorrowed |
| **Staking** | staked tokens + reward pool | totalStaked, rewardPool |
| **Bridge** | locked tokens | lockedAmount, pendingTransfers |

---

## 2. Asset Flow Mapping

### 2.1 Deposit Paths (Inflow)

```
[User Wallet] ──deposit()──► [Protocol Contract]
                                    │
                                    ▼
                              shares issued
```

| Function | Description | Risk |
|----------|-------------|------|
| `deposit()` | Asset deposit | Entry point |
| `stake()` | Staking | Entry point |
| `supply()` | Supply | Entry point |
| `mint()` | LP mint | Entry point |

### 2.2 Withdrawal Paths (Outflow)

```
[Protocol Contract] ──withdraw()──► [User Wallet]
         │
         ▼
    shares burned
```

| Function | Description | Risk |
|----------|-------------|------|
| `withdraw()` | Asset withdrawal | **Exit point** |
| `unstake()` | Unstaking | **Exit point** |
| `redeem()` | Redemption | **Exit point** |
| `burn()` | LP burn | **Exit point** |

### 2.3 Transfer Paths (Internal)

```
[Pool A] ──swap()──► [Pool B]
            │
            ▼
       price calculation
```

| Function | Description | Risk |
|----------|-------------|------|
| `swap()` | Exchange | Price manipulation |
| `transfer()` | Transfer | Permission verification |
| `liquidate()` | Liquidation | Oracle dependency |

### 2.4 Privileged Paths

```
[Admin] ──emergencyWithdraw()──► [Admin Wallet]
                                 ⚠️ High risk
```

| Function | Description | Risk |
|----------|-------------|------|
| `emergencyWithdraw()` | Emergency withdrawal | **Rug Pull** |
| `skim()` | Surplus collection | Asset leakage |
| `sweep()` | Token recovery | Unintended withdrawal |
| `rescue()` | Rescue | Potential abuse |

---

## 3. Leakage Path Exploration

### 3.1 Unvalidated Withdrawal

```solidity
// DANGER: No access control
function withdraw(uint256 amount) external {
    token.transfer(msg.sender, amount);  // @audit Anyone can withdraw!
}
```

### 3.2 Calculation Error Leakage

```solidity
// DANGER: Precision loss
function withdraw(uint256 shares) external {
    uint256 amount = shares / totalSupply * totalAssets;  // @audit Division first!
    // Multiple withdrawals accumulate rounding gains
}
```

### 3.3 Callback Bypass Leakage

```solidity
// DANGER: Reentrancy through callback
function withdraw(uint256 amount) external {
    token.transfer(msg.sender, amount);  // @audit Callback occurs
    balances[msg.sender] -= amount;      // State update too late
}
```

### 3.4 Economic Attack Leakage

```solidity
// DANGER: Price manipulation
function liquidate(address user) external {
    uint256 price = oracle.getPrice();  // @audit Spot price can be manipulated
    if (collateral[user] * price < debt[user]) {
        // Liquidation with manipulated price
    }
}
```

---

## 4. Asset Flow Diagram Template

```
┌─────────────────────────────────────────────────┐
│                  Asset Flow Diagram             │
├─────────────────────────────────────────────────┤
│                                                 │
│   [User Wallet]                                 │
│        │                                        │
│        │ deposit()/stake()                      │
│        ▼                                        │
│   ┌─────────────┐      ┌─────────────┐         │
│   │  Protocol   │◄────►│   Oracle    │         │
│   │  Contract   │      │  (Price)    │         │
│   └─────────────┘      └─────────────┘         │
│        │ │                                      │
│        │ │ withdraw()/swap()                    │
│        │ ▼                                      │
│   [User Wallet]    [Admin] ◄── emergencyWithdraw│
│                         │                       │
│                         ▼                       │
│                    ⚠️ Leakage Risk              │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 5. Output Format

```markdown
## Asset Flow Analysis Results

### Asset Storage

| Contract | Asset Type | Storage Variable | Location |
|----------|------------|------------------|----------|
| Pool | ETH | address(this).balance | Pool.sol:45 |
| Pool | ERC20 | token.balanceOf | Pool.sol:67 |
| Pool | Shares | totalSupply | Pool.sol:23 |

### Flow Paths

#### Deposit (Inflow)
```
User → deposit() → Pool
       ├── amount validation
       ├── token transfer
       └── shares issued
```

#### Withdrawal (Outflow)
```
Pool → withdraw() → User
       ├── shares validation
       ├── shares burned
       └── token transfer
```

### Leakage Risk Points

| Location | Path | Risk Level | Description |
|----------|------|------------|-------------|
| Pool.sol:142 | withdraw() | High | Insufficient access control |
| Pool.sol:200 | skim() | Medium | Admin-only unverified |

### Attack Scenarios

1. **First Depositor Attack**
   - Path: deposit → donate → next user deposit
   - Leakage: Subsequent depositor funds
   - Risk Level: High
```

---

## 6. Search Queries

```
# Find asset storage
Grep("balanceOf\\(address\\(this\\)\\)|address\\(this\\)\\.balance", glob="**/*.sol")
Grep("totalSupply|totalAssets|totalDeposited", glob="**/*.sol")

# Find deposit functions
Grep("function.*deposit|function.*stake|function.*supply", glob="**/*.sol")

# Find withdrawal functions
Grep("function.*withdraw|function.*redeem|function.*unstake", glob="**/*.sol")

# Find privileged functions
Grep("emergencyWithdraw|sweep|rescue|skim", glob="**/*.sol")
```

---

## 7. Attacker Mindset

- "Where is the money stored?" → Asset storage
- "Who can move the money?" → Access permissions
- "What paths can leak money?" → Leakage points
- "Can I manipulate the flow?" → Price/calculation attacks
