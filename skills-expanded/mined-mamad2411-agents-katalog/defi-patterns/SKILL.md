---
name: defi-patterns
description: DeFi-specific vulnerability patterns catalog - reentrancy, flash loans, oracle manipulation, MEV, sandwich attacks. Used during threat modeling.
trigger: During threat modeling — when the Threat Modeler generates tasks for DeFi protocols.
agents: [threat-modeler, deep-reasoner, hypothesis-generator]
---

# DeFi Patterns Skill

> **Trigger**: During threat modeling for DeFi/financial smart contracts.
> **Purpose**: Catalog of DeFi-specific vulnerability patterns with detection heuristics and task templates.

---

## Pattern Catalog

### 1. Reentrancy Patterns

**Variants**: Same-function, cross-function, cross-contract, read-only reentrancy.

**Detection Heuristics**:
```bash
# External calls before state updates
grep -rn "\.call\|\.transfer\|\.send" --include="*.sol" | grep -v "test\|mock"
# Check if state updates happen AFTER these calls
```

**Task Template**:
```markdown
Target: {contract}.{function}()
Invariant: State is consistent before and after external calls
Failure Predicate: Re-entry allows double-spend or stale-state exploitation
Drift Anchors: ["reentrancy", "external call", "state update", "callback"]
```

### 2. Flash Loan Attack Patterns

**Variants**: Price manipulation, governance attack, collateral inflation, liquidity drain.

**Detection Heuristics**:
```bash
# Spot price usage (manipulable via flash loans)
grep -rn "getReserves\|balanceOf.*pair\|slot0\|observe" --include="*.sol"
# Large value operations without flash-loan guards
grep -rn "flashLoan\|flash\|onFlashLoan" --include="*.sol"
```

**Task Template**:
```markdown
Attacker Capabilities: Can flash-loan up to pool TVL in a single tx
Invariant: Protocol accounting is correct regardless of transaction-local liquidity
Failure Predicate: Attacker profits at protocol/user expense via same-block borrow+repay
Drift Anchors: ["flash loan", "price manipulation", "same-block", "liquidity"]
```

### 3. Oracle Manipulation Patterns

**Variants**: Spot price manipulation, TWAP manipulation, stale oracle, oracle failure.

**Detection Heuristics**:
```bash
# Oracle usage
grep -rn "latestRoundData\|latestAnswer\|getPrice\|getRate\|consult\|observe" --include="*.sol"
# Staleness checks
grep -rn "updatedAt\|timestamp\|heartbeat\|sequencerUp" --include="*.sol"
```

**Task Template**:
```markdown
Invariant: Oracle price reflects true market value ± acceptable deviation
Failure Predicate: Stale/manipulated oracle causes incorrect liquidation, mispricing, or fund loss
Drift Anchors: ["oracle", "price feed", "staleness", "manipulation"]
```

### 4. First Depositor / Share Inflation

**Detection Heuristics**:
```bash
# Share/asset conversion
grep -rn "convertToShares\|convertToAssets\|previewDeposit\|previewMint" --include="*.sol"
# Division operations in conversion
grep -rn "totalSupply.*==.*0\|totalAssets.*==.*0" --include="*.sol"
```

**Task Template**:
```markdown
Invariant: shares * pricePerShare == assets ± 1 wei for all depositors
Failure Predicate: First depositor can inflate share price to steal from subsequent depositors
Drift Anchors: ["share inflation", "first deposit", "rounding", "ERC4626"]
```

### 5. Sandwich / MEV Patterns

**Detection Heuristics**:
```bash
# Slippage parameters
grep -rn "minAmount\|slippage\|deadline\|amountOutMin" --include="*.sol"
# Swaps without slippage protection
grep -rn "swap\|exchange" --include="*.sol" | grep -v "slippage\|minAmount"
```

**Task Template**:
```markdown
Attacker Capabilities: Can front-run and back-run target tx in same block
Invariant: User receives fair execution price regardless of block ordering
Failure Predicate: Attacker extracts value via sandwich (front-run + back-run)
Drift Anchors: ["MEV", "sandwich", "frontrun", "slippage"]
```

### 6. Liquidation Patterns

**Detection Heuristics**:
```bash
grep -rn "liquidat\|healthFactor\|collateralRatio\|isUndercollateralized" --include="*.sol"
grep -rn "badDebt\|shortfall\|deficit" --include="*.sol"
```

**Task Template**:
```markdown
Invariant: Protocol remains solvent after every liquidation; no bad debt created
Failure Predicate: Liquidation creates bad debt or leaves protocol underwater
Drift Anchors: ["liquidation", "collateral", "bad debt", "solvency"]
```

### 7. Accounting Desync Patterns

**Detection Heuristics**:
```bash
# Internal vs external balance tracking
grep -rn "totalAssets\|totalSupply\|_totalShares\|internalBalance" --include="*.sol"
# Multiple update paths for the same variable
grep -rn "totalAssets\s*[+\-=]" --include="*.sol"
```

**Task Template**:
```markdown
Invariant: Internal accounting matches actual token balances at all times
Failure Predicate: Internal tracking diverges from actual balances, enabling theft or DoS
Drift Anchors: ["accounting", "desync", "balance tracking", "totalAssets"]
```

### 8. Governance / Timelock Bypass

**Detection Heuristics**:
```bash
grep -rn "propose\|execute\|queue\|cancel\|votingDelay\|votingPeriod\|quorum" --include="*.sol"
grep -rn "timelock\|TimelockController\|delay" --include="*.sol"
```

### 9. Precision Loss / Rounding

**Detection Heuristics**:
```bash
# Division operations (potential rounding)
grep -rn " / \| \\* \|mulDiv\|fullMulDiv\|muldiv" --include="*.sol" | grep -v "test\|mock\|//"
# Casting operations
grep -rn "uint128\|uint96\|uint64\|uint32\|uint16\|uint8" --include="*.sol" | grep -v "event\|error"
```

### 10. Donation Attack / Direct Transfer

**Detection Heuristics**:
```bash
# Balance-based accounting (can be inflated via direct transfer)
grep -rn "address(this).balance\|balanceOf(address(this))" --include="*.sol"
```

---

## Cross-Pattern Combinations

The most dangerous vulnerabilities combine multiple patterns:

| Combination | Example |
|------------|---------|
| Flash loan + Oracle manipulation | Borrow → manipulate price → liquidate → repay |
| Reentrancy + Accounting desync | Re-enter during withdrawal → double-count assets |
| Sandwich + Precision loss | Frontrun to manipulate rounding direction |
| Governance + Flash loan | Flash-loan tokens → vote → execute → repay |
| First deposit + Donation | Donate to inflate share price before others deposit |

---

## Output

When this skill is active, the Threat Modeler should:
1. Check each pattern's detection heuristics against the target codebase
2. For each match, generate a task using the pattern's task template
3. Note cross-pattern combinations that apply
