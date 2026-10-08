---
name: Staking Protocol Patterns
description: >
  Auto-loaded by defi-auditor agent during Phase 2 when analyzing staking mechanisms.
  Provides patterns for: reward-per-token accumulator (Synthetix style), lock periods,
  multi-reward tokens, boosted staking. Critical: precision loss, first staker advantage,
  late staker dilution, unstake reentrancy.
user-invocable: false
---

# Staking Protocol Patterns

This skill provides comprehensive knowledge for auditing DeFi staking and reward distribution mechanisms.

## Common Staking Patterns

### 1. Simple Staking (No Rewards)

```solidity
contract SimpleStaking {
    mapping(address => uint256) public staked;

    function stake(uint256 amount) external {
        token.transferFrom(msg.sender, address(this), amount);
        staked[msg.sender] += amount;
    }

    function unstake(uint256 amount) external {
        require(staked[msg.sender] >= amount);
        staked[msg.sender] -= amount;
        token.transfer(msg.sender, amount);
    }
}
```

### 2. Reward Per Token Accumulator (Synthetix Style)

```solidity
contract StakingRewards {
    uint256 public rewardPerTokenStored;
    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;

    function rewardPerToken() public view returns (uint256) {
        if (totalSupply == 0) return rewardPerTokenStored;
        return rewardPerTokenStored +
            (rewardRate * (block.timestamp - lastUpdateTime) * 1e18 / totalSupply);
    }

    function earned(address account) public view returns (uint256) {
        return (balanceOf[account] *
            (rewardPerToken() - userRewardPerTokenPaid[account]) / 1e18) +
            rewards[account];
    }

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = block.timestamp;
        if (account != address(0)) {
            rewards[account] = earned(account);
            userRewardPerTokenPaid[account] = rewardPerTokenStored;
        }
        _;
    }
}
```

---

## Reward Distribution Vulnerabilities

### 1. Precision Loss

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Low precision accumulator
function rewardPerToken() public view returns (uint256) {
    // If rewardRate * timeDelta < totalSupply, result is 0!
    return rewardPerTokenStored +
        (rewardRate * (block.timestamp - lastUpdateTime) / totalSupply);
}
```

**Secure Pattern:**
```solidity
// Use high precision (1e18 or 1e27)
function rewardPerToken() public view returns (uint256) {
    return rewardPerTokenStored +
        (rewardRate * (block.timestamp - lastUpdateTime) * 1e18 / totalSupply);
}
```

### 2. First Staker Advantage

**Vulnerable Pattern:**
```solidity
// DANGEROUS: First staker gets all pending rewards
function stake(uint256 amount) external {
    // If totalSupply was 0, rewardPerTokenStored didn't update
    // First staker claims all rewards since lastUpdateTime
    _updateReward(msg.sender);
    // ...
}
```

**Secure Pattern:**
```solidity
function stake(uint256 amount) external {
    _updateReward(msg.sender);
    // If first staker, reset lastUpdateTime
    if (totalSupply == 0) {
        lastUpdateTime = block.timestamp;
    }
    // ...
}
```

### 3. Late Staker Dilution Attack

```
1. Attacker waits for rewards to accumulate
2. Stakes large amount just before reward distribution
3. Claims disproportionate rewards
4. Unstakes immediately

Mitigation: Time-weighted rewards or lock periods
```

### 4. Reward Calculation Overflow

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Can overflow with large values
uint256 pending = balance * rewardPerToken / 1e18;
// If balance and rewardPerToken are both large...
```

**Secure Pattern:**
```solidity
// Use mulDiv to avoid overflow
uint256 pending = FullMath.mulDiv(balance, rewardPerToken, 1e18);
```

---

## Lock Period Vulnerabilities

### 1. Lockup Bypass

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Lock only checked on unstake
function unstake(uint256 amount) external {
    require(block.timestamp >= lockEnd[msg.sender], "Locked");
    // But user can transfer stake tokens!
}
```

**Secure Pattern:**
```solidity
// Non-transferable during lock, or track per-deposit locks
function _beforeTokenTransfer(address from, address to, uint256) internal {
    if (from != address(0) && to != address(0)) {
        require(block.timestamp >= lockEnd[from], "Locked");
    }
}
```

### 2. Lock Extension Manipulation

```solidity
// If lock period extends on additional stake
// User might be tricked into longer lock than expected

// Always show clear lock end time before stake
```

---

## Unstaking Vulnerabilities

### 1. Unstake Reentrancy

**Vulnerable Pattern:**
```solidity
// DANGEROUS: Reward sent before state update
function unstake(uint256 amount) external {
    uint256 reward = earned(msg.sender);
    rewardToken.transfer(msg.sender, reward); // External call!
    balances[msg.sender] -= amount; // State update after
}
```

**Secure Pattern:**
```solidity
function unstake(uint256 amount) external nonReentrant {
    uint256 reward = earned(msg.sender);
    balances[msg.sender] -= amount; // State first
    rewards[msg.sender] = 0;
    rewardToken.transfer(msg.sender, reward);
    stakedToken.transfer(msg.sender, amount);
}
```

### 2. Dust Stuck in Contract

```solidity
// Rounding can leave tiny amounts stuck
// Ensure users can withdraw their full balance

function unstake(uint256 amount) external {
    if (amount == type(uint256).max) {
        amount = balances[msg.sender];
    }
    // ...
}
```

---

## Multi-Reward Token Patterns

### Multiple Reward Accumulators

```solidity
contract MultiRewards {
    struct Reward {
        uint256 rewardPerTokenStored;
        uint256 rewardRate;
        uint256 lastUpdateTime;
    }

    mapping(address => Reward) public rewardData;
    mapping(address => mapping(address => uint256)) public userRewardPerTokenPaid;

    function earned(address account, address rewardToken)
        public view returns (uint256)
    {
        // Similar to single reward but per token
    }
}
```

### Vulnerability: Different Update Frequencies

```solidity
// If reward tokens update at different times
// Can lead to incorrect calculations

// Always update ALL reward tokens together
modifier updateRewards(address account) {
    for (uint i = 0; i < rewardTokens.length; i++) {
        _updateReward(rewardTokens[i], account);
    }
    _;
}
```

---

## Boosted Staking

### veToken / Gauge Patterns

```solidity
// Boost based on lock duration
function getBoost(address user) public view returns (uint256) {
    uint256 lockDuration = lockEnd[user] - block.timestamp;
    return 1e18 + (lockDuration * maxBoost / maxLockDuration);
}

function earned(address user) public view returns (uint256) {
    uint256 boost = getBoost(user);
    return baseEarned(user) * boost / 1e18;
}
```

### Boost Manipulation

```solidity
// Attacker repeatedly extends lock to maintain boost
// While others with same stake earn less

// Mitigation: Time-averaged boost or snapshot boost
```

---

## Staking Audit Checklist

### Reward Calculation
- [ ] High precision used (1e18 minimum)
- [ ] No overflow in multiplication
- [ ] Division before multiplication avoided
- [ ] Zero totalSupply handled

### First/Late Staker
- [ ] First staker doesn't get all pending rewards
- [ ] Late staker can't dilute existing stakers unfairly
- [ ] Rewards accrue correctly when totalSupply changes

### Lock Periods
- [ ] Lock enforced on transfers (not just unstake)
- [ ] Lock extension clearly communicated
- [ ] No lock bypass via stake token transfer

### Reentrancy
- [ ] CEI pattern followed
- [ ] nonReentrant modifier on sensitive functions
- [ ] State updated before external calls

### Edge Cases
- [ ] Zero stake amount handled
- [ ] Full unstake (max amount) works
- [ ] Dust doesn't get stuck
- [ ] Reward period end handled

### Multi-Reward
- [ ] All reward tokens update together
- [ ] Adding/removing reward tokens safe
- [ ] Different decimals handled

## Severity Classification

### Critical
- Reentrancy on unstake/claim
- First staker steals all rewards
- Precision loss loses significant value

### High
- Lock bypass possible
- Late staker dilution attack
- Reward overflow

### Medium
- Dust stuck in contract
- Boost manipulation
- Reward token update desync
