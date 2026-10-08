---
name: ERC4626 Vault Patterns
description: >
  Auto-loaded by defi-auditor agent during Phase 2 when analyzing ERC4626 vaults.
  Provides patterns for: share/asset conversion, inflation attack mitigations,
  rounding direction rules, donation attacks. Critical: first depositor attack,
  virtual shares offset, dead shares burning.
user-invocable: false
---

# ERC4626 Vault Patterns

This skill provides comprehensive knowledge for auditing ERC4626 tokenized vaults.

## ERC4626 Overview

ERC4626 standardizes tokenized vaults:
- Deposit assets → receive shares
- Shares represent proportional ownership
- Redeem shares → receive assets

```
shares = assets × totalSupply / totalAssets
assets = shares × totalAssets / totalSupply
```

---

## Inflation Attack (First Depositor Attack)

### The Attack

```
1. Vault is empty (totalSupply = 0, totalAssets = 0)
2. Attacker deposits 1 wei → gets 1 share
3. Attacker donates 1e18 tokens directly to vault
4. Now: totalSupply = 1, totalAssets = 1e18 + 1
5. Victim deposits 2e18 tokens
6. Victim gets: 2e18 × 1 / (1e18 + 1) = 1 share (rounds down!)
7. Attacker and victim each have 1 share
8. Attacker redeems: gets half of 3e18 + 1 = 1.5e18 tokens
9. Attacker profit: ~0.5e18 tokens stolen from victim
```

### Vulnerable Pattern

```solidity
// DANGEROUS: No inflation protection
function deposit(uint256 assets) public returns (uint256 shares) {
    shares = totalSupply() == 0
        ? assets
        : assets * totalSupply() / totalAssets();

    _mint(msg.sender, shares);
    asset.transferFrom(msg.sender, address(this), assets);
}
```

### Mitigation 1: Virtual Shares/Assets

```solidity
// Add virtual offset to prevent manipulation
uint256 constant VIRTUAL_SHARES = 1e3;
uint256 constant VIRTUAL_ASSETS = 1;

function totalSupply() public view override returns (uint256) {
    return super.totalSupply() + VIRTUAL_SHARES;
}

function totalAssets() public view override returns (uint256) {
    return asset.balanceOf(address(this)) + VIRTUAL_ASSETS;
}
```

### Mitigation 2: Dead Shares (Burn on First Deposit)

```solidity
function deposit(uint256 assets) public returns (uint256 shares) {
    shares = _convertToShares(assets);

    if (totalSupply() == 0) {
        // Burn first 1000 shares to dead address
        uint256 deadShares = 1000;
        _mint(address(0xdead), deadShares);
        shares -= deadShares;
    }

    _mint(msg.sender, shares);
    asset.transferFrom(msg.sender, address(this), assets);
}
```

### Mitigation 3: Minimum Deposit

```solidity
function deposit(uint256 assets) public returns (uint256 shares) {
    require(assets >= MIN_DEPOSIT, "Below minimum");
    // ...
}
```

---

## Rounding Direction

### The Rule

| Operation | Round | Reason |
|-----------|-------|--------|
| deposit | shares DOWN | User gets less shares |
| mint | assets UP | User pays more |
| withdraw | shares UP | User burns more |
| redeem | assets DOWN | User gets less |

**Always round in favor of the vault (against the user).**

### Implementation

```solidity
// Round DOWN (default)
function _convertToShares(uint256 assets) internal view returns (uint256) {
    uint256 supply = totalSupply();
    return supply == 0 ? assets : assets * supply / totalAssets();
}

// Round UP
function _convertToSharesRoundUp(uint256 assets) internal view returns (uint256) {
    uint256 supply = totalSupply();
    if (supply == 0) return assets;
    return (assets * supply + totalAssets() - 1) / totalAssets();
}
```

### Vulnerable Pattern

```solidity
// DANGEROUS: Wrong rounding direction
function withdraw(uint256 assets) public returns (uint256 shares) {
    // Should round UP, but rounds DOWN
    shares = assets * totalSupply() / totalAssets();
    // Attacker can withdraw dust repeatedly, extracting value
}
```

---

## Donation Attack

### The Attack

```
1. Attacker deposits normally, gets shares
2. Attacker donates assets directly to vault (not through deposit)
3. Share price increases
4. Attacker has fewer shares but same value
5. Other share calculations become incorrect
```

### Vulnerable Scenarios

```solidity
// If vault uses asset balance directly
function totalAssets() public view returns (uint256) {
    return asset.balanceOf(address(this)); // Manipulable!
}

// If reward distribution based on balance
function distribute() external {
    uint256 rewards = asset.balanceOf(address(this)) - lastBalance;
    // Donated amount included in rewards!
}
```

### Mitigations

```solidity
// Track assets internally
uint256 internal _totalAssets;

function deposit(uint256 assets) public {
    // ...
    _totalAssets += assets;
}

function totalAssets() public view returns (uint256) {
    return _totalAssets; // Not manipulable
}
```

---

## Share Calculation Edge Cases

### Zero Total Supply

```solidity
function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    // Handle first deposit
    return supply == 0 ? assets : assets * supply / totalAssets();
}
```

### Zero Total Assets

```solidity
// Can happen after total withdrawal or loss event
function convertToAssets(uint256 shares) public view returns (uint256) {
    uint256 assets = totalAssets();
    // Avoid division by zero
    return assets == 0 ? shares : shares * assets / totalSupply();
}
```

### Very Small Amounts

```solidity
// 1 wei deposit might get 0 shares due to rounding
uint256 shares = 1 * totalSupply / totalAssets; // Could be 0!

// Mitigation: Minimum deposit requirement
require(shares > 0, "Deposit too small");
```

---

## maxDeposit / maxWithdraw

### Standard Implementation

```solidity
function maxDeposit(address) public view returns (uint256) {
    // Consider:
    // - Deposit caps
    // - Available capacity
    // - User-specific limits
    return type(uint256).max; // Or actual limit
}

function maxWithdraw(address owner) public view returns (uint256) {
    // Consider:
    // - Owner's balance
    // - Available liquidity
    // - Withdrawal limits
    return convertToAssets(balanceOf(owner));
}
```

### Vulnerabilities

```solidity
// DANGEROUS: maxDeposit doesn't account for cap
function maxDeposit(address) public view returns (uint256) {
    return type(uint256).max; // But there's actually a cap!
}

// User calls deposit with max, expecting it to work
// Transaction reverts unexpectedly
```

---

## Yield Source Integration

### External Yield Vaults

```solidity
contract YieldVault is ERC4626 {
    IYieldSource public yieldSource;

    function totalAssets() public view override returns (uint256) {
        // Include yield from external source
        return asset.balanceOf(address(this)) +
               yieldSource.balanceOf(address(this));
    }

    // Risk: External yield source could be manipulated
    // Risk: External protocol could pause/fail
}
```

---

## ERC4626 Audit Checklist

### Inflation Attack
- [ ] Virtual shares/assets implemented
- [ ] OR dead shares burned on first deposit
- [ ] OR minimum deposit enforced
- [ ] First depositor cannot profit from donation

### Rounding
- [ ] deposit: shares round DOWN
- [ ] mint: assets round UP
- [ ] withdraw: shares round UP
- [ ] redeem: assets round DOWN
- [ ] All conversions favor vault

### Edge Cases
- [ ] Zero totalSupply handled
- [ ] Zero totalAssets handled
- [ ] Very small deposits handled
- [ ] Very small withdrawals handled

### Limits
- [ ] maxDeposit returns accurate limit
- [ ] maxMint returns accurate limit
- [ ] maxWithdraw considers liquidity
- [ ] maxRedeem considers liquidity

### Integration
- [ ] totalAssets cannot be manipulated
- [ ] Donations don't break accounting
- [ ] External yield properly accounted

## Severity Classification

### Critical
- First depositor inflation attack
- Wrong rounding direction
- totalAssets manipulable

### High
- Donation breaks reward distribution
- maxDeposit/maxWithdraw incorrect
- Zero supply/assets crashes

### Medium
- Minimum deposit not enforced
- Edge case precision loss
- Missing slippage protection
