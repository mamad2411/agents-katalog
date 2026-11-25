---
name: dos-attack
description: >
  Auto-loaded by logic-auditor agent during Phase 2.
  Provides detection patterns for: gas griefing, unbounded loops, external call failures,
  block gas limit exploitation, storage DoS, and liveness failures.
  Core artifact: Liveness Analysis Map.
user-invocable: false
---

# Denial of Service (DoS) Attack Patterns

**OWASP SC10:2025** - DoS attacks prevent legitimate users from accessing protocol functionality, potentially locking funds permanently.

**2025-2026 Statistics**: DoS vulnerabilities caused protocol freezes affecting $180M+ in locked funds, with gas griefing attacks increasing 45% YoY.

---

## Why DoS Happens (Root Causes)

### Root Cause 1: Unbounded Iteration

Loops without gas limits become unusable as data grows.

```solidity
// VULNERABLE: Unbounded loop
function distributeRewards() external {
    for (uint256 i = 0; i < holders.length; i++) {  // @audit holders can grow unbounded
        token.transfer(holders[i], rewards[holders[i]]);
    }
}
```

**Attacker's view**: "I'll create thousands of tiny positions. Eventually, no one can call this function."

### Root Cause 2: External Call Dependency

Function success depends on external call that attacker can make fail.

```solidity
// VULNERABLE: Relies on external transfer success
function withdrawAll() external {
    for (uint256 i = 0; i < users.length; i++) {
        payable(users[i]).transfer(balances[users[i]]);  // @audit One revert blocks all
    }
}
```

**Attacker's view**: "If I'm in the array and my receive() reverts, nobody gets paid."

### Root Cause 3: Storage Slot Exhaustion

Unlimited storage growth makes operations cost-prohibitive.

```solidity
// VULNERABLE: Unlimited storage growth
mapping(address => uint256[]) public userDeposits;

function deposit() external payable {
    userDeposits[msg.sender].push(msg.value);  // @audit Array grows forever
}

function getTotalDeposits(address user) external view returns (uint256) {
    uint256 total;
    for (uint256 i = 0; i < userDeposits[user].length; i++) {  // @audit View can run out of gas
        total += userDeposits[user][i];
    }
    return total;
}
```

### Root Cause 4: Block Gas Limit Exploitation

Transaction exceeds block gas limit, making it impossible to execute.

```solidity
// VULNERABLE: Can exceed block gas limit
function processAllPending() external {
    while (pendingQueue.length > 0) {
        _processSingle(pendingQueue[0]);
        pendingQueue.pop();
    }
}
```

---

## The Liveness Analysis Map (Core Artifact)

For each critical function, document:

```
Function: withdrawAll()
├── External Calls: N calls to user addresses
├── Loop Bound: users.length (unbounded)
├── Gas Estimate: O(n) where n = users count
├── Failure Mode: Single revert blocks all withdrawals
├── Recovery: None - funds permanently locked
└── Risk: CRITICAL
```

| Function | Dependency | Bound | Failure Impact | Recovery |
|----------|------------|-------|----------------|----------|
| distributeRewards | N transfers | Unbounded | Protocol freeze | None |
| processQueue | Queue size | Bounded (100) | Temporary delay | Retry |
| batchLiquidate | M liquidations | User-controlled | Partial failure | Continue |

---

## Detection Patterns

### Pattern 1: Unbounded Loop DoS

**Root Cause**: Unbounded Iteration

```solidity
// VULNERABLE: Loop over dynamic array
function processAll() external {
    for (uint256 i = 0; i < items.length; i++) {
        _process(items[i]);
    }
}
```

**Attack Flow**:
1. Attacker adds many small items to array
2. Array grows to thousands of entries
3. Gas cost exceeds block limit
4. Function becomes uncallable
5. Funds/operations permanently stuck

**Search Queries**:
```
Grep("for.*\\.length|while.*\\.length", glob="**/*.sol")
Grep("for.*i\\+\\+|for.*i < ", glob="**/*.sol")
```

**Mitigation**:
```solidity
// SECURE: Pagination pattern
function processRange(uint256 start, uint256 end) external {
    require(end <= items.length && end - start <= MAX_BATCH);
    for (uint256 i = start; i < end; i++) {
        _process(items[i]);
    }
}
```

### Pattern 2: External Call Failure DoS

**Root Cause**: External Call Dependency

```solidity
// VULNERABLE: One failure blocks all
function refundAll() external {
    for (uint256 i = 0; i < refundees.length; i++) {
        (bool success,) = refundees[i].call{value: amounts[i]}("");
        require(success, "Refund failed");  // @audit Blocks on any failure
    }
}
```

**Attack Flow**:
1. Attacker enters system with contract that reverts on receive
2. Refund function iterates to attacker's address
3. Attacker's receive() reverts
4. Entire function reverts
5. All refunds blocked

**Search Queries**:
```
Grep("\\.call\\{value.*require\\(success", glob="**/*.sol")
Grep("\\.transfer\\(|send\\(", glob="**/*.sol")
```

**Mitigation**:
```solidity
// SECURE: Pull pattern
mapping(address => uint256) public pendingRefunds;

function withdraw() external {
    uint256 amount = pendingRefunds[msg.sender];
    pendingRefunds[msg.sender] = 0;
    (bool success,) = msg.sender.call{value: amount}("");
    require(success);
}
```

### Pattern 3: Gas Griefing

**Root Cause**: Unchecked Gas Forwarding

```solidity
// VULNERABLE: Forwards all gas to untrusted call
function executeCallback(address target, bytes calldata data) external {
    (bool success,) = target.call(data);  // @audit Attacker can consume all gas
    require(success);
}
```

**Attack Flow**:
1. Attacker creates contract with expensive fallback
2. Callback executes, consuming all forwarded gas
3. Parent transaction fails or behaves unexpectedly
4. Griefing attack succeeds

**Search Queries**:
```
Grep("\\.call\\(|\\.delegatecall\\(", glob="**/*.sol")
Grep("gasleft\\(\\)", glob="**/*.sol")
```

**Mitigation**:
```solidity
// SECURE: Limit gas forwarded
(bool success,) = target.call{gas: 50000}(data);
// OR use try/catch
try ICallback(target).callback{gas: 50000}(data) {} catch {}
```

### Pattern 4: Block Stuffing

**Risk**: Attacker fills blocks to prevent time-sensitive operations

```solidity
// VULNERABLE: Time-sensitive operation
function claimAuction() external {
    require(block.timestamp >= auctionEnd, "Auction ongoing");
    require(!claimed, "Already claimed");
    claimed = true;
    // Transfer winning bid...
}
```

**Attack Flow**:
1. Attacker sees they're losing auction
2. Before auction ends, attacker submits many high-gas transactions
3. Blocks become full, legitimate claimAuction() can't execute
4. Attacker extends effective auction time
5. Eventually claims at manipulated state

**Mitigation**:
- Add grace periods for time-sensitive operations
- Use commit-reveal for auctions
- Allow partial execution

### Pattern 5: Storage Collision DoS

**Root Cause**: Unlimited Mapping/Array Growth

```solidity
// VULNERABLE: Unlimited storage per user
function addOrder(uint256 amount) external {
    userOrders[msg.sender].push(Order(amount, block.timestamp));
}

function cancelAllOrders() external {
    delete userOrders[msg.sender];  // @audit Gas increases with array size
}
```

**Attack Flow**:
1. Attacker creates millions of tiny orders
2. Tries to cancel all (or system tries to process)
3. Gas exceeds limits
4. Operations blocked

**Search Queries**:
```
Grep("push\\(|delete.*\\[", glob="**/*.sol")
Grep("mapping.*\\[\\]|address.*=>.*\\[\\]", glob="**/*.sol")
```

### Pattern 6: Return Bomb Attack

**Root Cause**: Unbounded Return Data

```solidity
// VULNERABLE: Copies all return data
function executeCall(address target, bytes calldata data) external returns (bytes memory) {
    (bool success, bytes memory result) = target.call(data);  // @audit result can be huge
    require(success);
    return result;
}
```

**Attack Flow**:
1. Attacker creates contract returning massive data (e.g., 1MB)
2. Memory expansion costs explode
3. Transaction runs out of gas
4. Call fails unexpectedly

**Mitigation**:
```solidity
// SECURE: Limit return data or use assembly
assembly {
    let success := call(gas(), target, 0, add(data, 32), mload(data), 0, 0)
    // Only copy limited return data if needed
}
```

---

## DoS Prevention Checklist

### Loop Safety
- [ ] All loops have bounded iterations
- [ ] Maximum batch size enforced
- [ ] Pagination available for large datasets
- [ ] Gas estimation includes worst case

### External Call Safety
- [ ] Pull pattern over push pattern
- [ ] Individual call failures don't block others
- [ ] Gas limits on external calls
- [ ] Fallback handling for failed transfers

### Storage Safety
- [ ] No unbounded arrays per user
- [ ] Cleanup mechanisms exist
- [ ] View functions handle large data

### Time Safety
- [ ] Grace periods for time-sensitive ops
- [ ] No strict time windows attackers can exploit
- [ ] Block stuffing resistance

---

## Search Query Reference

```
# Find unbounded loops
Grep("for.*\\.length|while.*length", glob="**/*.sol")
Grep("for.*i\\+\\+.*\\{", glob="**/*.sol")

# Find external calls
Grep("\\.call\\{|\\.transfer\\(|\\.send\\(", glob="**/*.sol")
Grep("require\\(success", glob="**/*.sol")

# Find storage patterns
Grep("push\\(|pop\\(|delete", glob="**/*.sol")
Grep("mapping.*\\[\\]", glob="**/*.sol")

# Find time dependencies
Grep("block\\.timestamp|block\\.number", glob="**/*.sol")
```

---

## Severity Classification

### Critical
- Funds permanently locked
- Core protocol functions uncallable
- No recovery mechanism

### High
- Temporary protocol freeze possible
- Significant gas griefing impact
- User funds at risk

### Medium
- View functions can fail
- Minor operations blockable
- Recovery exists but costly

---

## Rationalization Table (Reject These Excuses)

| Excuse | Reality |
|--------|---------|
| "Array won't grow that large" | Attackers WILL grow it. Assume worst case. |
| "Users won't create malicious contracts" | Attackers absolutely will. Every address is suspect. |
| "Gas is cheap" | Block gas limit is fixed. 30M gas max per block. |
| "We can upgrade if needed" | Funds may be locked BEFORE you can upgrade. |
| "This is theoretical" | Akropolis, SpankChain, and others lost millions to DoS. |
| "View functions don't matter" | External protocols depend on your views. DoS spreads. |
