---
name: restaking
description: >
  Auto-loaded by defi-auditor agent during Phase 2 when analyzing restaking protocols.
  Provides patterns for: EigenLayer AVS integration, slashing propagation, operator risks,
  LST/LRT depeg, withdrawal queues, cross-protocol risk amplification.
  Core artifact: Restaking Risk Matrix.
user-invocable: false
---

# Restaking Protocol Vulnerability Analysis

**2025-2026 Statistics**: Restaking protocols hold $15B+ TVL (EigenLayer alone), with emerging attack vectors around slashing propagation and operator collusion causing significant concern.

---

## Restaking Overview

Restaking allows already-staked ETH (native or LST) to secure additional protocols (AVS - Actively Validated Services) for extra yield, while introducing layered risk.

```
ETH Staker
    ↓ Stake
Ethereum Beacon Chain (32 ETH validator)
    ↓ Restake
EigenLayer (extends security to AVS)
    ↓ Delegate
Operators (run AVS software)
    ↓ Secure
AVS (bridges, oracles, DA layers, etc.)
```

**Key Risk**: Slashing in AVS propagates back to original ETH stake.

---

## Why Restaking Fails (Root Causes)

### Root Cause 1: Cascading Slashing

Single misbehavior triggers slashing across multiple protocols.

```
Operator misbehaves on AVS-A
    ↓ Slashed on AVS-A
    ↓ EigenLayer reduces operator stake
    ↓ All delegators to this operator lose funds
    ↓ Multiple AVS security degraded simultaneously
```

**Attacker's view**: "One compromised operator affects thousands of users across multiple protocols."

### Root Cause 2: Unbounded Operator Trust

Stakers delegate to operators without understanding full risk exposure.

```solidity
// VULNERABLE: No limit on AVS registration
function registerForAVS(address avs) external onlyOperator {
    registeredAVS[msg.sender].push(avs);  // @audit Operator can register for unlimited AVS
    // Staker funds now exposed to all AVS risks
}
```

### Root Cause 3: Withdrawal Queue Manipulation

Long withdrawal periods create opportunities for exploitation.

```solidity
// VULNERABLE: Fixed withdrawal delay
uint256 constant WITHDRAWAL_DELAY = 7 days;

function initiateWithdrawal(uint256 shares) external {
    withdrawalQueue[msg.sender] = Withdrawal(shares, block.timestamp + WITHDRAWAL_DELAY);
    // @audit If slashing occurs during delay, user loses more than expected
}
```

### Root Cause 4: LST/LRT Depeg Risk

Liquid (re)staking tokens can depeg from underlying, causing liquidation cascades.

```
stETH price drops 5% vs ETH
    ↓ Lending protocols see collateral value drop
    ↓ Liquidations trigger
    ↓ More stETH sold
    ↓ Further depeg
    ↓ Cascade continues
```

---

## The Restaking Risk Matrix (Core Artifact)

For each restaking integration, document:

| Component | Risk Type | Exposure | Mitigation | Status |
|-----------|-----------|----------|------------|--------|
| Operator A | Slashing | 3 AVS | Max slashing cap | Partial |
| AVS-Bridge | Corruption | $50M TVL | Fraud proofs | Active |
| stETH collateral | Depeg | 10% of protocol | Circuit breaker | Missing |
| Withdrawal queue | DoS | 7-day delay | Partial withdrawal | None |

---

## Detection Patterns

### Pattern 1: Unbounded Slashing Exposure

**Root Cause**: Cascading Slashing

```solidity
// VULNERABLE: No cap on slashable amount
function slash(address operator, uint256 amount) external onlyAVS {
    operatorStake[operator] -= amount;  // @audit Can slash entire stake
    // No protection for delegators
}

// VULNERABLE: No limit on simultaneous slashing
mapping(address => address[]) public operatorAVS;

function executeSlashing(address operator) external {
    for (uint i = 0; i < operatorAVS[operator].length; i++) {
        IAVs(operatorAVS[operator][i]).slash(operator);
        // @audit Multiple AVS can slash simultaneously
    }
}
```

**Attack Flow**:
1. Operator registers for many AVS
2. Single misbehavior triggers multi-AVS slashing
3. Operator stake completely drained
4. Delegators lose everything
5. AVS security simultaneously compromised

**Search Queries**:
```
Grep("slash|slashing|penalty", glob="**/*.sol")
Grep("operator.*stake|stake.*operator", glob="**/*.sol")
```

**Mitigation**:
```solidity
// Per-AVS slashing cap
mapping(address => uint256) public maxSlashPerAVS;

function slash(address operator, uint256 amount) external onlyAVS {
    uint256 cappedAmount = Math.min(amount, maxSlashPerAVS[msg.sender]);
    operatorStake[operator] -= cappedAmount;
}

// Global slashing cap per time period
mapping(address => uint256) public slashingThisPeriod;
uint256 constant MAX_SLASHING_PER_PERIOD = 10e18; // 10 ETH
```

### Pattern 2: Operator Collusion

**Root Cause**: Insufficient Operator Validation

```solidity
// VULNERABLE: No operator quality checks
function registerAsOperator() external payable {
    require(msg.value >= MIN_STAKE);
    operators[msg.sender] = true;
    // @audit Anyone with MIN_STAKE can become operator
    // No reputation, no KYC, no history check
}

// VULNERABLE: Operators can collude
function validateBlock(bytes calldata blockData) external onlyOperator {
    // @audit Multiple operators from same entity can sign
    // Sybil attack possible
}
```

**Search Queries**:
```
Grep("registerOperator|isOperator|onlyOperator", glob="**/*.sol")
Grep("validateBlock|sign|attest", glob="**/*.sol")
```

### Pattern 3: Withdrawal Queue Exploitation

**Root Cause**: Withdrawal Queue Manipulation

```solidity
// VULNERABLE: No slashing protection during withdrawal
function completeWithdrawal(uint256 withdrawalId) external {
    Withdrawal storage w = withdrawals[withdrawalId];
    require(block.timestamp >= w.unlockTime);
    
    uint256 amount = w.shares * totalAssets() / totalShares();
    // @audit If slashing occurred, totalAssets decreased
    // User receives less than expected
    
    _transfer(msg.sender, amount);
}
```

**Attack Flow**:
1. User initiates withdrawal
2. During 7-day delay, operator gets slashed
3. totalAssets decreases
4. User's share worth less
5. User receives less than when they initiated

**Search Queries**:
```
Grep("withdrawal.*queue|queue.*withdrawal", glob="**/*.sol")
Grep("initiateWithdrawal|completeWithdrawal|unstake", glob="**/*.sol")
```

**Mitigation**:
```solidity
// Lock in exit value at initiation
function initiateWithdrawal(uint256 shares) external {
    uint256 assetsAtInitiation = convertToAssets(shares);
    withdrawals[msg.sender] = Withdrawal({
        shares: shares,
        assets: assetsAtInitiation,  // Lock in value
        unlockTime: block.timestamp + WITHDRAWAL_DELAY
    });
}
```

### Pattern 4: LRT/LST Oracle Manipulation

**Root Cause**: Trusting Manipulable Exchange Rates

```solidity
// VULNERABLE: Using spot exchange rate
function getCollateralValue(address user) external view returns (uint256) {
    uint256 lrtBalance = lrt.balanceOf(user);
    uint256 ethPerLRT = lrt.totalAssets() / lrt.totalSupply();  // @audit Manipulable!
    return lrtBalance * ethPerLRT;
}
```

**Attack Flow**:
1. Attacker donates to LRT vault (inflation attack)
2. ethPerLRT temporarily inflated
3. Borrow against inflated collateral
4. LRT price normalizes
5. Attacker has undercollateralized loan

**Search Queries**:
```
Grep("totalAssets|totalSupply|convertToAssets", glob="**/*.sol")
Grep("exchangeRate|pricePerShare|getRate", glob="**/*.sol")
```

### Pattern 5: AVS Registration Without Stake Verification

**Root Cause**: Unbounded Operator Trust

```solidity
// VULNERABLE: No stake verification for AVS
function registerForAVS(address avs) external {
    require(operators[msg.sender], "Not operator");
    avsOperators[avs].push(msg.sender);
    // @audit No check if operator has enough stake for this AVS
    // @audit No check if operator is already overextended
}
```

**Attack Flow**:
1. Operator with 32 ETH stake
2. Registers for 10 AVS, each expecting 32 ETH security
3. Total "promised" security: 320 ETH
4. Actual security: 32 ETH
5. Single slashing affects all AVS

**Search Queries**:
```
Grep("registerForAVS|registerAVS|joinAVS", glob="**/*.sol")
Grep("minimumStake|requiredStake|stakeRequirement", glob="**/*.sol")
```

### Pattern 6: Reward Distribution Manipulation

**Root Cause**: Imbalanced Reward/Risk Distribution

```solidity
// VULNERABLE: Operator takes rewards, delegators take risk
function distributeRewards(address operator) external {
    uint256 rewards = pendingRewards[operator];
    uint256 operatorCut = rewards * operatorFee / 10000;
    
    payable(operator).transfer(operatorCut);  // Operator gets rewards immediately
    // @audit But slashing affects delegators first
}
```

**Search Queries**:
```
Grep("distribute.*reward|reward.*distribute", glob="**/*.sol")
Grep("operatorFee|commission|operatorCut", glob="**/*.sol")
```

---

## EigenLayer-Specific Patterns

### Strategy Manager Integration

```solidity
// Check for proper integration
interface IStrategyManager {
    function depositIntoStrategy(
        IStrategy strategy,
        IERC20 token,
        uint256 amount
    ) external returns (uint256 shares);
    
    function queueWithdrawal(
        uint256[] calldata strategyIndexes,
        IStrategy[] calldata strategies,
        uint256[] calldata shares,
        address withdrawer
    ) external returns (bytes32);
}
```

**Key Checks**:
- Withdrawal delay enforced
- Slashing conditions documented
- Operator delegation limits

### Delegation Manager

```solidity
// Check delegation safety
interface IDelegationManager {
    function delegateTo(address operator) external;
    function undelegate(address staker) external;
}
```

**Key Risks**:
- Delegating to malicious operator
- Undelegation timing during slashing events

---

## Restaking Audit Checklist

### Slashing
- [ ] Maximum slashing cap per AVS
- [ ] Maximum slashing cap per time period
- [ ] Slashing affects operator before delegators
- [ ] Slashing insurance fund exists

### Operators
- [ ] Minimum stake requirements
- [ ] Maximum AVS registration limit
- [ ] Operator reputation tracking
- [ ] Operator exit conditions

### Withdrawals
- [ ] Value locked at initiation
- [ ] Partial withdrawal supported
- [ ] Emergency withdrawal path
- [ ] Slashing during delay handled

### LRT/LST Integration
- [ ] Oracle manipulation resistant
- [ ] Depeg circuit breakers
- [ ] Liquidation cascade protection
- [ ] TWAP or manipulation-resistant pricing

### AVS Integration
- [ ] AVS risk disclosure
- [ ] Stake requirements per AVS
- [ ] Cross-AVS risk correlation considered

---

## Search Query Reference

```
# Find restaking patterns
Grep("restake|restaking|EigenLayer|AVS", glob="**/*.sol")
Grep("operator|delegate|delegator", glob="**/*.sol")

# Find slashing
Grep("slash|slashing|penalty|punish", glob="**/*.sol")
Grep("freeze|frozen|pause", glob="**/*.sol")

# Find withdrawal patterns
Grep("withdrawal|withdraw|unstake|exit", glob="**/*.sol")
Grep("queue|delay|cooldown", glob="**/*.sol")

# Find LST/LRT
Grep("stETH|rETH|cbETH|LRT|LST", glob="**/*.sol")
Grep("liquid.*staking|restaking.*token", glob="**/*.sol")

# Find strategy patterns
Grep("strategy|strategyManager|depositIntoStrategy", glob="**/*.sol")
```

---

## Severity Classification

### Critical
- Unbounded slashing drains delegators
- Operator collusion enables theft
- LRT manipulation enables bad debt

### High
- Withdrawal queue slashing exposure
- AVS over-registration without stake
- Reward/risk imbalance exploitation

### Medium
- Insufficient operator vetting
- Missing slashing caps
- Depeg protection gaps

---

## Rationalization Table (Reject These Excuses)

| Excuse | Reality |
|--------|---------|
| "Operators are trusted" | Operators can be hacked, bribed, or act maliciously. |
| "Slashing is rare" | One slashing event affects thousands. Plan for it. |
| "Withdrawal delay protects us" | Delay WITHOUT slashing protection = user loss. |
| "LSTs are stable" | stETH depegged 5%+ in 2022. It CAN happen. |
| "EigenLayer handles security" | Your integration creates new attack surfaces. |
| "AVS are audited" | AVS risk compounds with each registration. |
| "Users understand the risk" | Protocol MUST enforce safety. Users can't evaluate operator risk. |
