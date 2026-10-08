---
name: LSD Token Integration Patterns
description: >
  Auto-loaded by token-auditor agent during Phase 2 when LSD tokens are detected.
  Provides patterns for: stETH rebasing (use shares), wstETH wrapping, rETH/cbETH
  exchange rates, sfrxETH (ERC4626). Critical: caching rebasing balances, 1:1
  ratio assumption, 1-2 wei transfer rounding.
user-invocable: false
---

# LSD Token Integration Patterns

This skill provides knowledge for auditing Liquid Staking Derivative token integrations.

## LSD Token Overview

| Token | Protocol | Type | Key Issue |
|-------|----------|------|-----------|
| stETH | Lido | Rebasing | Balance changes daily |
| wstETH | Lido | Non-rebasing | Wrapped stETH |
| rETH | Rocket Pool | Non-rebasing | Exchange rate varies |
| cbETH | Coinbase | Non-rebasing | Exchange rate varies |
| sfrxETH | Frax | Non-rebasing | Yield-bearing |
| frxETH | Frax | 1:1 pegged | No yield |

---

## stETH (Lido) Integration

### Rebasing Behavior

stETH balance increases daily when staking rewards are distributed.

```solidity
// Day 1: User deposits 100 stETH
// Day 2: Balance is now 100.01 stETH (after rebase)
// Day 3: Balance is now 100.02 stETH (after rebase)
```

### Vulnerable Pattern

```solidity
// DANGEROUS: Caches rebasing token balance
contract VulnerableVault {
    mapping(address => uint256) public deposits;

    function deposit(uint256 amount) external {
        stETH.transferFrom(msg.sender, address(this), amount);
        deposits[msg.sender] = amount; // WRONG: Amount will be stale!
    }

    function withdraw() external {
        uint256 amount = deposits[msg.sender];
        stETH.transfer(msg.sender, amount);
        // User loses rebase rewards!
    }
}
```

### Secure Pattern: Use Shares

```solidity
contract SecureVault {
    mapping(address => uint256) public shares;

    function deposit(uint256 stEthAmount) external {
        // Transfer stETH
        uint256 balanceBefore = stETH.balanceOf(address(this));
        stETH.transferFrom(msg.sender, address(this), stEthAmount);
        uint256 received = stETH.balanceOf(address(this)) - balanceBefore;

        // Track shares, not amounts
        uint256 sharesReceived = stETH.getSharesByPooledEth(received);
        shares[msg.sender] += sharesReceived;
    }

    function withdraw() external {
        uint256 userShares = shares[msg.sender];
        shares[msg.sender] = 0;

        // Convert shares back to stETH amount
        uint256 stEthAmount = stETH.getPooledEthByShares(userShares);
        stETH.transfer(msg.sender, stEthAmount);
    }
}
```

### stETH-Specific Functions

```solidity
interface IStETH {
    // Convert stETH amount to shares
    function getSharesByPooledEth(uint256 _ethAmount)
        external view returns (uint256);

    // Convert shares to stETH amount
    function getPooledEthByShares(uint256 _sharesAmount)
        external view returns (uint256);

    // Transfer using shares (avoids rounding)
    function transferShares(address _recipient, uint256 _sharesAmount)
        external returns (uint256);

    // Get shares balance
    function sharesOf(address _account) external view returns (uint256);
}
```

### stETH Transfer Issues

```solidity
// ISSUE: 1-2 wei rounding error on transfers
uint256 balanceBefore = stETH.balanceOf(address(this));
stETH.transferFrom(user, address(this), 1 ether);
uint256 received = stETH.balanceOf(address(this)) - balanceBefore;
// received might be 0.999999999999999998 ether (1-2 wei less)

// SOLUTION: Use transferShares for exact amounts
stETH.transferShares(recipient, sharesAmount);
```

---

## wstETH (Wrapped stETH)

### Why Use wstETH?

wstETH is non-rebasing, making it DeFi-compatible:
- Balance stays constant
- Value increases as stETH/wstETH rate changes
- Easier to integrate than stETH

### Conversion Functions

```solidity
interface IWstETH {
    // Wrap stETH to wstETH
    function wrap(uint256 _stETHAmount) external returns (uint256);

    // Unwrap wstETH to stETH
    function unwrap(uint256 _wstETHAmount) external returns (uint256);

    // Get stETH amount for wstETH
    function getStETHByWstETH(uint256 _wstETHAmount)
        external view returns (uint256);

    // Get wstETH amount for stETH
    function getWstETHByStETH(uint256 _stETHAmount)
        external view returns (uint256);

    // Current exchange rate
    function stEthPerToken() external view returns (uint256);
}
```

### Integration Pattern

```solidity
contract WstETHVault {
    IERC20 public wstETH;

    function deposit(uint256 amount) external {
        // wstETH is non-rebasing, simple tracking works
        wstETH.transferFrom(msg.sender, address(this), amount);
        balances[msg.sender] += amount;
    }

    function getValueInETH(address user) public view returns (uint256) {
        // Convert wstETH balance to ETH value
        uint256 wstBalance = balances[user];
        uint256 stEthAmount = IWstETH(address(wstETH))
            .getStETHByWstETH(wstBalance);
        // stETH is ~1:1 with ETH
        return stEthAmount;
    }
}
```

---

## rETH (Rocket Pool)

### Exchange Rate Behavior

rETH value increases relative to ETH as rewards accrue.

```solidity
interface IRocketTokenRETH {
    // Get ETH value of rETH amount
    function getEthValue(uint256 _rethAmount)
        external view returns (uint256);

    // Get rETH amount for ETH value
    function getRethValue(uint256 _ethAmount)
        external view returns (uint256);

    // Current exchange rate (ETH per rETH)
    function getExchangeRate() external view returns (uint256);
}
```

### Integration Considerations

```solidity
// rETH rate only increases, never decreases (no slashing... yet)
// But rate can be slightly stale

// Getting current value
uint256 ethValue = rETH.getEthValue(rethBalance);

// CAUTION: Exchange rate can be manipulated via Rocket Pool deposits
// Use oracle for price if security-critical
```

---

## cbETH (Coinbase)

### Exchange Rate

```solidity
interface ICbETH {
    // Exchange rate: cbETH per ETH
    function exchangeRate() external view returns (uint256);
}

// Get ETH value
uint256 ethValue = cbEthAmount * cbETH.exchangeRate() / 1e18;
```

### Known Issues

- Exchange rate updated by Coinbase (centralized)
- Rate can be briefly stale
- Consider oracle for critical valuations

---

## sfrxETH (Frax)

### Exchange Rate

```solidity
interface ISfrxETH {
    // ERC4626 vault style
    function convertToAssets(uint256 shares)
        external view returns (uint256);

    function convertToShares(uint256 assets)
        external view returns (uint256);

    function pricePerShare() external view returns (uint256);
}
```

### Integration

sfrxETH follows ERC4626 standard, making integration straightforward.

```solidity
// Get frxETH value
uint256 frxEthValue = sfrxETH.convertToAssets(sfrxEthBalance);
```

---

## Common LSD Vulnerabilities

### 1. Hardcoded 1:1 Ratio

```solidity
// DANGEROUS: Assumes 1 LSD = 1 ETH
function getCollateralValue(address user) public view returns (uint256) {
    return lstToken.balanceOf(user); // Wrong!
}

// CORRECT: Use exchange rate
function getCollateralValue(address user) public view returns (uint256) {
    uint256 balance = lstToken.balanceOf(user);
    return balance * getExchangeRate() / 1e18;
}
```

### 2. Rebasing Token in DeFi Protocol

```solidity
// DANGEROUS: AMM with rebasing token
// Rebase adds tokens but not LP shares
// LPs lose rebase rewards to arbitrageurs
```

### 3. Withdrawal Queue Ignorance

```solidity
// stETH withdrawals have a queue!
// Can't assume instant withdrawal

// Check queue status
interface IWithdrawalQueue {
    function getLastRequestId() external view returns (uint256);
    function getLastFinalizedRequestId() external view returns (uint256);
}
```

---

## LSD Audit Checklist

### stETH Specific
- [ ] Uses shares instead of balances
- [ ] Handles 1-2 wei transfer rounding
- [ ] Accounts for daily rebases
- [ ] Uses transferShares when possible

### General LSD
- [ ] Exchange rate used (not 1:1)
- [ ] Rate source is reliable
- [ ] Withdrawal queue considered
- [ ] Depeg scenario handled
- [ ] Oracle used for price-critical operations

### DeFi Integration
- [ ] Compatible with rebasing (or wrapped)
- [ ] Slippage accounts for rate changes
- [ ] Liquidation uses proper valuation

## Severity Classification

### Critical
- Ignoring exchange rate (1:1 assumption)
- Caching rebasing token amounts
- Wrong valuation in liquidations

### High
- Transfer rounding errors accumulated
- No slippage protection on rate changes
- Stale exchange rate usage

### Medium
- Missing withdrawal queue handling
- No depeg protection
- Centralized rate source
