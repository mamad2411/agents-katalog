---
name: logic-error
description: >
  Auto-loaded by logic-auditor agent during Phase 2.
  Provides detection patterns for: division before multiplication, first depositor
  attacks, precision loss, unchecked blocks, missing slippage, edge cases.
  Core artifact: Calculation Flow Map.
user-invocable: false
---

# Business Logic Vulnerability Analysis

**2025 Statistics**: Logic errors caused **$63.8M+** losses, Input validation = **34.6% of vulnerabilities**, Rounding attacks (Bunni) = **$2.4M-$8.3M**.

---

## Why Logic Bugs Happen (Root Causes)

### Root Cause 1: Integer-Only Arithmetic

Solidity has NO floating point. Every division truncates.

```solidity
// In normal math: 5 / 2 = 2.5
// In Solidity:    5 / 2 = 2  ← Where does 0.5 go?

uint256 fee = amount / 10000 * feeRate;
// If amount = 5000, feeRate = 100:
// 5000 / 10000 = 0  ← Division first!
// 0 * 100 = 0       ← Fee bypassed!
```

**Attacker's view**: "Every time they divide, precision is lost. I'll make sure it's lost to ME."

### Root Cause 2: Operation Order

Division before multiplication destroys precision.

```solidity
// VULNERABLE: Divide first
uint256 result = a / b * c;  // @audit Precision lost!

// SECURE: Multiply first
uint256 result = a * c / b;  // Preserves more precision

// Example with a=100, b=3, c=3:
// Wrong order: 100/3*3 = 33*3 = 99  (lost 1)
// Right order: 100*3/3 = 300/3 = 100 (exact)
```

**Detection**: Any `X / Y * Z` pattern is suspect. Check if `X * Z / Y` is possible.

### Root Cause 3: Rounding Direction Mismatch

Protocol rounds in attacker's favor, not protocol's favor.

```solidity
// VULNERABLE: Rounding favors user on withdraw
function withdraw(uint256 shares) external {
    uint256 assets = shares * totalAssets / totalSupply;  // @audit Rounds DOWN
    // Attacker withdraws many small amounts
    // Each time keeps the rounded-down dust
}

// SECURE: Round against the user
function withdraw(uint256 shares) external {
    uint256 assets = shares * totalAssets / totalSupply;  // Still rounds down
    // But on DEPOSIT, also round down (user gets fewer shares)
    // Protocol never loses from rounding
}
```

**Rule**: Round DOWN on withdraw (user gets less), round DOWN on deposit (user pays more).

### Root Cause 4: Missing Edge Case Handling

Zero, one, max, first, last - all create special behaviors.

```solidity
// VULNERABLE: No zero check
function distribute(uint256 amount, uint256 recipients) external {
    uint256 perPerson = amount / recipients;  // @audit recipients = 0 → revert
    // Or recipients = 1000000 → perPerson = 0
}
```

**Attacker's view**: "What happens at the boundaries? That's where bugs hide."

---

## The Calculation Flow Map (Core Artifact)

Trace every arithmetic operation:

```
Input (amount, shares, etc.)
    ↓
Validation (bounds check? zero check?)
    ↓
Calculation (what order? division when?)
    ↓
Rounding (which direction? who loses?)
    ↓
State Update (invariant preserved?)
    ↓
Output (expected vs actual?)
```

Document each calculation:

| Function | Operation | Order | Rounding | Risk |
|----------|-----------|-------|----------|------|
| mint() | shares = assets * supply / total | Mul first ✓ | Down (protocol wins) | First depositor |
| fee() | fee = amount / 10000 * rate | Div first ✗ | Down → zero | Fee bypass |
| redeem() | assets = shares * total / supply | Mul first ✓ | Down (user loses) | Check |

---

## Detection Patterns

### Pattern 1: Division Before Multiplication

**Root Cause**: Operation Order

```solidity
// VULNERABLE: Precision loss
uint256 fee = amount / 10000 * feeRate;
// If amount < 10000, fee = 0 regardless of feeRate!

uint256 share = deposit / totalAssets * totalSupply;
// Small deposits get 0 shares!
```

**Attack Flow**:
1. Find function with `a / b * c` pattern
2. Input value where `a < b`
3. Result = 0, bypassing intended logic
4. Repeat to accumulate benefit

**Search Queries**:
```
Grep("/.*\\*", glob="**/*.sol")
Grep("\\*/", glob="**/*.sol")
```

**Verification Questions**:
- Can the division result in zero?
- Would reordering to `a * c / b` be safe (no overflow)?
- What's the minimum input that gives non-zero result?

### Pattern 2: First Depositor / Vault Inflation Attack

**Root Cause**: Rounding + Empty State

```solidity
// VULNERABLE: Standard ERC4626 share calculation
function deposit(uint256 assets) external returns (uint256 shares) {
    if (totalSupply == 0) {
        shares = assets;  // @audit First depositor sets the ratio!
    } else {
        shares = assets * totalSupply / totalAssets;
    }
}
```

**Attack Flow** (Inflation Attack):
1. Deposit 1 wei → get 1 share
2. Donate 1,000,000 tokens directly to vault (not via deposit)
3. Now: totalAssets = 1,000,001, totalSupply = 1
4. Victim deposits 999,999 → shares = 999,999 * 1 / 1,000,001 = 0
5. Victim gets 0 shares, loses entire deposit
6. Attacker redeems 1 share → gets everything

**Search Queries**:
```
Grep("totalSupply.*==.*0|totalSupply\\(\\).*==.*0", glob="**/*.sol")
Grep("balanceOf\\(address\\(this\\)\\)", glob="**/*.sol")
Grep("ERC4626|vault|shares", glob="**/*.sol")
```

**Verification Questions**:
- What happens when totalSupply = 0?
- Is there virtual shares/assets offset?
- Is there minimum deposit requirement?
- Can assets be donated without minting shares?

### Pattern 3: Unchecked Return Values

**Root Cause**: Silent Failure Assumption

```solidity
// VULNERABLE: USDT returns false instead of reverting
IERC20(token).transfer(recipient, amount);  // @audit Return not checked!
// If transfer fails, execution continues with wrong state

// SECURE: Use SafeERC20
SafeERC20.safeTransfer(IERC20(token), recipient, amount);
```

**Search Queries**:
```
Grep("\\.transfer\\(|\\.transferFrom\\(", glob="**/*.sol")
Grep("safeTransfer|SafeERC20", glob="**/*.sol")
```

### Pattern 4: Integer Overflow in Unchecked Blocks

**Root Cause**: Bypassing Solidity 0.8+ Safety

```solidity
// VULNERABLE: Intentional unchecked can overflow
unchecked {
    balance += amount;  // @audit Can wrap to 0 if balance + amount > MAX
    counter--;          // @audit Can wrap to MAX if counter = 0
}
```

**Search Queries**:
```
Grep("unchecked\\s*\\{", glob="**/*.sol")
Grep("assembly\\s*\\{", glob="**/*.sol")
```

**Verification Questions**:
- Why is unchecked used here?
- Can inputs cause overflow/underflow?
- Is the unchecked block necessary?

### Pattern 5: Missing Slippage Protection

**Root Cause**: No Minimum Output Enforcement

```solidity
// VULNERABLE: User accepts any output
function swap(uint256 amountIn) external {
    uint256 amountOut = calculateOutput(amountIn);
    token.transfer(msg.sender, amountOut);  // @audit No minimum check!
}

// SECURE: Enforce minimum
function swap(uint256 amountIn, uint256 minAmountOut) external {
    uint256 amountOut = calculateOutput(amountIn);
    require(amountOut >= minAmountOut, "Slippage");
    token.transfer(msg.sender, amountOut);
}
```

**Search Queries**:
```
Grep("amountOutMin|minAmountOut|minOut|slippage", glob="**/*.sol")
Grep("swap|exchange|trade", glob="**/*.sol")
```

### Pattern 6: Missing Zero/Address Validation

**Root Cause**: Missing Input Validation

```solidity
// VULNERABLE: Zero address bricks contract
function setAdmin(address newAdmin) external onlyOwner {
    admin = newAdmin;  // @audit address(0) = no admin forever
}

// VULNERABLE: Division by zero
function distribute(uint256 total, uint256 count) external {
    uint256 each = total / count;  // @audit count = 0 → revert
}

// VULNERABLE: Zero amount wastes gas or causes issues
function deposit(uint256 amount) external {
    // @audit amount = 0 → user gets 0 shares, wasted gas
}
```

**Search Queries**:
```
Grep("address.*=|= address", glob="**/*.sol")
Grep("require.*!=.*0|require.*>.*0", glob="**/*.sol")
```

---

## Edge Case Testing Matrix

For EVERY value-handling function:

| Edge Case | Test Value | Common Bug | What to Check |
|-----------|------------|------------|---------------|
| **Zero** | `0` | Division by zero, empty transfer | Does it revert or return 0? |
| **One** | `1` | Rounds to zero, off-by-one | Minimum meaningful input? |
| **Max** | `type(uint256).max` | Overflow, gas exhaustion | Does unchecked wrap? |
| **First user** | Empty state | Ratio manipulation | Who sets initial ratio? |
| **Last user** | Only remaining | Stuck funds, dust | Can final user withdraw all? |
| **Boundary** | Just above/below limit | Off-by-one, `<` vs `<=` | Fencepost errors? |

---

## Invariant Verification Checklist

| Invariant | How to Verify | Common Violation |
|-----------|--------------|------------------|
| `totalSupply == sum(balances)` | Trace all mint/burn | Donation attack |
| `totalAssets >= totalDebt` | Check after each action | Flash loan attack |
| `shares * pricePerShare >= deposit` | Rounding check | Precision loss |
| `sum(rewards) <= rewardPool` | Trace all claims | Over-distribution |

---

## Search Query Reference

```
# Find arithmetic operations
Grep("/.*\\*|\\*/", glob="**/*.sol")
Grep("mulDiv|wadMul|rayMul|FullMath", glob="**/*.sol")

# Find potential overflow
Grep("unchecked\\s*\\{", glob="**/*.sol")
Grep("assembly\\s*\\{", glob="**/*.sol")

# Find share calculations
Grep("totalSupply|totalAssets|pricePerShare", glob="**/*.sol")
Grep("ERC4626|vault|shares", glob="**/*.sol")

# Find missing checks
Grep("\\.transfer\\(|\\.transferFrom\\(", glob="**/*.sol")
Grep("require.*!=|require.*>", glob="**/*.sol")

# Find slippage
Grep("amountOutMin|minAmount|slippage", glob="**/*.sol")
```

---

## Rationalization Table (Reject These Excuses)

| Excuse | Attacker's Reality |
|--------|-------------------|
| "It's just rounding" | Bunni lost $2.4M-$8.3M to rounding. Repeated calls accumulate. |
| "Users won't send dust" | Attackers absolutely will. Dust inputs are the exploit. |
| "Math is too complex" | MEV bots automate arbitrarily complex calculations. |
| "First depositor is trusted" | First depositor attack is #1 vault exploit in 2025. |
| "Frontend validates" | On-chain must be secure standalone. |
| "This edge case is unlikely" | Every edge case is an attacker's opportunity. |
| "Solidity 0.8 prevents overflow" | Unchecked blocks and assembly bypass this. |
