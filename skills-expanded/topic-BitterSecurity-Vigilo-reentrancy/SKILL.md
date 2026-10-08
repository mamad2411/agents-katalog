---
name: reentrancy
description: >
  Auto-loaded by reentrancy-auditor agent during Phase 2.
  Provides detection patterns for: CEI violations, cross-function/cross-contract
  reentrancy, read-only reentrancy, token callback exploits (ERC721/777/1155).
  Core artifact: State Timeline map.
user-invocable: false
---

# Reentrancy Vulnerability Analysis

**2025 Statistics**: Reentrancy caused **$350M+** historical losses, OWASP 2025 ranks it **#5**, 2024 attacks include Penpie, Clober, GemPad.

---

## Why Reentrancy Happens (Root Causes)

### Root Cause 1: State Update After External Call

The fundamental CEI (Checks-Effects-Interactions) violation.

```solidity
// VULNERABLE: State update AFTER external call
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    (bool success,) = msg.sender.call{value: amount}("");  // @audit External call
    require(success);
    balances[msg.sender] -= amount;  // @audit State update AFTER!
}
```

**Attacker's view**: "Between the call and the state update, I control execution. I'll call withdraw again before my balance updates."

### Root Cause 2: Execution Flow Transfer

Every external call hands control to potentially hostile code.

```solidity
// Even "safe" patterns can transfer control:
IERC20(token).transfer(recipient, amount);    // Could be ERC777 with hooks!
NFT.safeTransferFrom(from, to, id);           // Triggers onERC721Received!
Token1155.safeTransferFrom(...);              // Triggers onERC1155Received!
```

**Detection**: Any external call is a potential callback. Check what standards the token implements.

### Root Cause 3: Shared State Dependency

Multiple contracts/functions depend on same state variable.

```solidity
// Contract has two functions sharing `balances`
function withdraw() external {
    uint256 amount = balances[msg.sender];
    msg.sender.call{value: amount}("");  // @audit Callback opportunity
    balances[msg.sender] = 0;  // @audit Updated after
}

function transfer(address to, uint256 amount) external {
    require(balances[msg.sender] >= amount);  // @audit Same balance!
    balances[msg.sender] -= amount;
    balances[to] += amount;
}
// During withdraw callback, attacker calls transfer() with STALE balance!
```

**Attacker's view**: "ReentrancyGuard on withdraw() doesn't protect transfer(). I'll call transfer() during withdraw callback."

### Root Cause 4: View Function Exposure

View functions return stale data during callbacks, affecting external protocols.

```solidity
// Contract A (Vault)
function withdraw() external {
    uint256 assets = userAssets[msg.sender];
    msg.sender.call{value: assets}("");  // @audit Callback
    userAssets[msg.sender] = 0;
    totalAssets -= assets;  // @audit Updated after
}

function getTotalAssets() public view returns (uint256) {
    return totalAssets;  // @audit Returns STALE value during callback!
}

// Contract B (Lending) reads from Contract A
function getCollateralValue(address user) view returns (uint256) {
    return vaultA.getTotalAssets() * userShares / totalShares;
    // During withdraw callback, totalAssets is WRONG!
}
```

**Attacker's view**: "The view function shows the old value. External protocols that read this will make wrong decisions."

---

## The State Timeline (Core Artifact)

Every reentrancy finding MUST include a state timeline:

```
T0: balances[attacker] = 100, contract.balance = 1000
T1: withdraw(100) called
T2: call{value: 100}("") → attacker.receive() triggered
T3: [CALLBACK] balances[attacker] STILL = 100! ← INCONSISTENT STATE
T4: Re-enter withdraw(100) with same balance
T5: Another 100 sent
T6: ... repeat until drained
T7: balances[attacker] -= 100 (executed N times, but all see 100)
```

Document each finding:

| Phase | Contract State | Attacker Action | Balance Check |
|-------|---------------|-----------------|---------------|
| T0 | Initial | - | 100 |
| T2 | Sending ETH | receive() callback | 100 (stale) |
| T4 | Re-entered | withdraw again | 100 (stale) |
| T7 | Unwind | - | Multiple decrements fail |

---

## Detection Patterns

### Pattern 1: Classic CEI Violation

**Root Cause**: State Update After External Call

```solidity
// VULNERABLE: Textbook reentrancy
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);  // CHECK
    (bool success,) = msg.sender.call{value: amount}("");  // INTERACTION
    require(success);
    balances[msg.sender] -= amount;  // EFFECT - Wrong order!
}
```

**Attack Flow**:
1. Attacker calls withdraw(100)
2. Contract sends ETH via call{value}
3. Attacker's receive() callback triggers
4. In callback: call withdraw(100) again (balance still 100!)
5. Repeat until contract drained
6. All state updates execute with wrong values

**Search Queries**:
```
Grep("\\.call\\{value", glob="**/*.sol")
Grep("transfer\\(|send\\(", glob="**/*.sol")
```

**Verification Questions**:
- Is state updated BEFORE external call?
- Is there a reentrancy guard?
- Can callback reach this function again?

### Pattern 2: Cross-Function Reentrancy

**Root Cause**: Shared State Dependency

```solidity
// Both functions use same `balances` mapping
function withdraw() external nonReentrant {  // Has guard
    uint256 amount = balances[msg.sender];
    msg.sender.call{value: amount}("");  // @audit Callback
    balances[msg.sender] = 0;
}

function transfer(address to, uint256 amt) external {  // NO guard!
    require(balances[msg.sender] >= amt);  // @audit Same state!
    balances[msg.sender] -= amt;
    balances[to] += amt;
}
```

**Attack Flow**:
1. Attacker calls withdraw() with 100 balance
2. During callback, attacker calls transfer(accomplice, 100)
3. transfer() sees balances[attacker] = 100 (not yet updated!)
4. Attacker "transfers" 100 to accomplice
5. withdraw() completes, sets balances[attacker] = 0
6. Accomplice has 100 tokens created from nothing

**Search Queries**:
```
Grep("nonReentrant", glob="**/*.sol")
Grep("ReentrancyGuard", glob="**/*.sol")
```

**Verification Questions**:
- Does guard cover ALL functions sharing this state?
- Can other functions be called during callback?
- What state do they depend on?

### Pattern 3: Cross-Contract Reentrancy

**Root Cause**: ReentrancyGuard Only Protects Single Contract

```solidity
// Contract A
function withdraw() external nonReentrant {
    uint256 shares = userShares[msg.sender];
    msg.sender.call{value: shares}("");  // @audit Callback
    userShares[msg.sender] = 0;  // @audit Updated after
}

// Contract B (different contract, NO shared guard!)
function borrow() external {
    uint256 collateral = contractA.userShares(msg.sender);  // @audit Stale!
    require(collateral >= minCollateral);
    // Borrow against stale collateral value
}
```

**Attack Flow**:
1. Attacker has 1000 shares in Contract A
2. Call withdraw() on Contract A
3. During callback, call borrow() on Contract B
4. Contract B reads userShares = 1000 (not yet zeroed!)
5. Attacker borrows against 1000 collateral
6. withdraw() completes, sets shares = 0
7. Attacker has borrowed funds + no collateral

**Search Queries**:
```
Grep("external.*view.*returns", glob="**/*.sol")
Grep("\\.balanceOf\\(|\\.userShares\\(", glob="**/*.sol")
```

**Verification Questions**:
- Do other contracts read this contract's state?
- Are those reads during callback windows?
- Is there cross-contract reentrancy protection?

### Pattern 4: Read-Only Reentrancy

**Root Cause**: View Function Returns Stale Data

```solidity
// Vault contract
function withdraw() external {
    uint256 assets = userAssets[msg.sender];
    msg.sender.call{value: assets}("");  // @audit Callback
    totalAssets -= assets;  // @audit Updated AFTER
}

function pricePerShare() public view returns (uint256) {
    return totalAssets * 1e18 / totalSupply;  // @audit Stale totalAssets!
}
```

**Attack Flow** (dForce $3.7M exploit):
1. Attacker withdraws from Curve pool
2. During callback, Curve's get_virtual_price() returns stale value
3. dForce protocol reads this wrong price for collateral
4. Attacker borrows more than collateral allows
5. Profit from price discrepancy

**Search Queries**:
```
Grep("view.*returns|external.*view", glob="**/*.sol")
Grep("getPrice|pricePerShare|totalAssets", glob="**/*.sol")
```

**Verification Questions**:
- Do view functions depend on state updated after external calls?
- Do external protocols use these view functions?
- Is there a "read-only reentrancy" lock?

### Pattern 5: Token Callback Reentrancy

**Root Cause**: Hidden Callbacks in Token Standards

```solidity
// VULNERABLE: ERC721 safeTransferFrom triggers callback
function stake(uint256 tokenId) external {
    nft.safeTransferFrom(msg.sender, address(this), tokenId);  // @audit Callback!
    userStake[msg.sender] += 1;  // @audit After callback
}

// ERC777 tokensReceived hook
function deposit(uint256 amount) external {
    token.transferFrom(msg.sender, address(this), amount);  // @audit ERC777 hook!
    userDeposit[msg.sender] += amount;  // @audit After callback
}

// ERC1155 onERC1155Received callback
function mint(uint256 id, uint256 amount) external {
    _mint(msg.sender, id, amount, "");  // @audit Triggers onERC1155Received!
    totalMinted += amount;  // @audit After callback
}
```

**Attack Flow** (Omni $1.43M exploit):
1. Attacker calls stake() with malicious NFT receiver
2. safeTransferFrom triggers onERC721Received callback
3. In callback, attacker re-enters stake() or other functions
4. State manipulated before original stake() completes

**Token Standards with Callbacks**:

| Standard | Callback Function | Trigger |
|----------|------------------|---------|
| ERC721 | onERC721Received | safeTransferFrom, safeMint |
| ERC777 | tokensReceived, tokensToSend | transfer, transferFrom |
| ERC1155 | onERC1155Received | safeTransferFrom, mint |
| ERC1363 | onTransferReceived | transferAndCall |

**Search Queries**:
```
Grep("safeTransferFrom|safeMint|safeTransfer", glob="**/*.sol")
Grep("onERC721Received|onERC1155Received|tokensReceived", glob="**/*.sol")
Grep("ERC777|ERC1155|ERC1363|ERC721", glob="**/*.sol")
```

**Verification Questions**:
- What token standard is used?
- Does the standard have callbacks?
- Is state updated before the token transfer?

---

## ReentrancyGuard Analysis

### Check Guard Coverage

```
Grep("nonReentrant|ReentrancyGuard|_locked", glob="**/*.sol")
```

### Verify Protection Scope

| Protection Level | Coverage | Bypass |
|-----------------|----------|--------|
| Single function | Only that function | Cross-function |
| Single contract | All functions in contract | Cross-contract |
| Cross-contract | Multiple contracts | Complex dependency |

### Common Guard Mistakes

```solidity
// VULNERABLE: Guard on wrong function
contract Vault {
    function deposit() external nonReentrant { ... }  // Guarded
    function withdraw() external { ... }  // NOT guarded! ← BUG
}

// VULNERABLE: Internal function not protected
function _transfer() internal {  // No guard
    msg.sender.call{value: amount}("");
}
function publicTransfer() external nonReentrant {
    _transfer();  // Guard bypassed via other entry point
}
```

---

## CEI Pattern Verification Checklist

For each function with external calls:

1. **Identify all external calls**
   - Low-level calls (.call, .delegatecall)
   - Token transfers (especially safe* variants)
   - External contract calls

2. **Map state dependencies**
   - Which state variables are read before call?
   - Which state variables are modified after call?

3. **Verify ordering**
   ```
   ✓ CORRECT: checks → state update → external call
   ✗ WRONG: checks → external call → state update
   ```

4. **Check cross-function**
   - Can other functions be called during callback?
   - Do they share the same state?

---

## Search Query Reference

```
# Find external calls
Grep("\\.call\\{|transfer\\(|send\\(", glob="**/*.sol")
Grep("safeTransfer|safeMint|safeTransferFrom", glob="**/*.sol")

# Find callbacks
Grep("receive\\(\\)|fallback\\(\\)", glob="**/*.sol")
Grep("onERC721Received|onERC1155Received|tokensReceived", glob="**/*.sol")

# Find reentrancy guards
Grep("nonReentrant|ReentrancyGuard|_locked", glob="**/*.sol")

# Find view functions (read-only reentrancy)
Grep("view.*returns.*uint|external.*view", glob="**/*.sol")
Grep("totalAssets|pricePerShare|getPrice", glob="**/*.sol")

# Find token standards with hooks
Grep("ERC777|ERC1155|ERC721|ERC1363", glob="**/*.sol")
```

---

## Rationalization Table (Reject These Excuses)

| Excuse | Attacker's Reality |
|--------|-------------------|
| "We have ReentrancyGuard" | Guard only protects single contract. Cross-contract reentrancy bypasses it. |
| "We use SafeERC20" | SafeERC20 doesn't prevent callbacks, only handles return values. ERC777 still has hooks. |
| "The token is standard ERC20" | Verify on-chain. Many tokens implement ERC777 hooks silently. |
| "State is updated first" | Check cross-function. Other functions might read stale state during callback. |
| "It's just a view function" | Read-only reentrancy cost dForce $3.7M. View functions expose stale state. |
| "External call is to trusted contract" | Trusted contracts can have callbacks to untrusted. Trace the full call chain. |
| "Nobody would do this" | Automated MEV bots scan for reentrancy 24/7. If it's exploitable, it will be exploited. |
