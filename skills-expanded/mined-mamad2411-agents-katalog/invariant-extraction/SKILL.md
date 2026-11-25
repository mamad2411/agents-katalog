---
name: invariant-extraction
description: Extract mathematical and business invariants from code and documentation. Used during decomposition by the Decomposer agent.
trigger: During decomposition — when the Decomposer performs Dimension 9 (Invariant Decomposition).
agents: [decomposer, threat-modeler]
---

# Invariant Extraction Skill

> **Trigger**: During decomposition — Dimension 9 (Invariant Decomposition).
> **Purpose**: Discover and formalize all properties that MUST hold across all execution paths.

---

## Overview

Invariants are the foundation of the entire audit pipeline. Every task is built around
testing an invariant. If invariants are poorly extracted, the entire downstream pipeline
produces low-value results.

---

## Invariant Categories

### 1. Accounting Invariants
Properties about value conservation and balance consistency.

```bash
# Find totalSupply, totalAssets, balance tracking
grep -rn "totalSupply\|totalAssets\|totalShares\|totalDebt\|totalLiabilities" --include="*.sol"

# Find balance mappings
grep -rn "mapping.*balance\|mapping.*deposit\|mapping.*shares" --include="*.sol"
```

**Common patterns**:
- `totalSupply == sum(balances[i])` for all token holders
- `totalAssets >= totalLiabilities` (solvency)
- `vault.balance >= sum(userDeposits) - sum(userWithdrawals)`
- `shares * pricePerShare == assets ± rounding`

### 2. Access Control Invariants
Properties about who can do what.

```bash
grep -rn "onlyOwner\|onlyRole\|hasRole\|require.*msg.sender" --include="*.sol"
```

**Common patterns**:
- "Only owner can call `setFee()`"
- "Only minter role can call `mint()`"
- "Admin cannot drain user funds directly"

### 3. State Machine Invariants
Properties about legal state transitions.

```bash
grep -rn "enum \|Status\|State\|Phase" --include="*.sol"
grep -rn "require.*status\|require.*state\|require.*phase" --include="*.sol"
```

**Common patterns**:
- "State can only move forward: Pending → Active → Completed"
- "Once finalized, state cannot change"
- "Cooldown period must elapse before transition"

### 4. Ordering Invariants
Properties about temporal and causal ordering.

**Common patterns**:
- "Initialize must be called before any other function"
- "Deposit must precede withdrawal"
- "Oracle update must be within N blocks of current block"
- "Maturity date must be in the future at creation time"

### 5. Capacity Invariants
Properties about bounds and limits.

```bash
grep -rn "MAX_\|MIN_\|_CAP\|_LIMIT\|maxDeposit\|maxWithdraw" --include="*.sol"
```

**Common patterns**:
- `fee <= MAX_FEE` (fee cannot exceed cap)
- `totalDeposits <= depositCap`
- `slippage <= maxSlippage`

### 6. Conservation Invariants
Properties about value not being created or destroyed.

**Common patterns**:
- "Total value in == total value out (minus explicit fees)"
- "Minting shares increases totalSupply by exactly the minted amount"
- "Burning shares decreases totalSupply by exactly the burned amount"

---

## Extraction Protocol

### Step 1: Read Documentation
```bash
# Check for invariant docs, specs, or natspec
find . -name "*.md" -not -path "*/node_modules/*" | head -20
grep -rn "@notice\|@dev\|invariant\|MUST\|ALWAYS\|NEVER" --include="*.sol" | head -50
```

### Step 2: Analyze Assert/Require Statements
```bash
grep -rn "assert(\|require(" --include="*.sol" | grep -v "test\|mock\|node_modules"
```

Each `assert` is an explicit invariant. Each `require` is a precondition that may imply a broader invariant.

### Step 3: Analyze Test Invariants
```bash
grep -rn "invariant_\|assertEq\|assertGe\|assertLe\|assertGt\|assertLt" --include="*.sol" | grep -i "test"
```

Existing tests often encode invariants the developers intended to hold.

### Step 4: Derive Implicit Invariants
Some invariants are never stated but must hold:
- If there's a `deposit()` and `withdraw()`, then `deposited - withdrawn >= 0`
- If there's a share/asset conversion, then the conversion must be consistent
- If there's an oracle, staleness must be bounded

### Step 5: Formalize

For each invariant, produce:

```markdown
## INV-{number}: {Short Name}

**Category**: [Accounting | Access | State Machine | Ordering | Capacity | Conservation]
**Formal Statement**: `{mathematical expression or logical predicate}`
**Source**: [Code reference, documentation, or derived]
**Contracts Involved**: [list]
**State Variables**: [list]
**Entrypoints That Could Violate**: [list]
**Confidence**: [Explicit (from code/docs) | Implicit (derived) | Assumed]
```

---

## Output

Save to: `specs/decomposition/invariant-decomposition.md`

```markdown
# Invariant Decomposition

## Summary
{N} invariants extracted across {M} categories.

## Invariant Catalog
[Full list with formal statements]

## Coverage Gaps
[Areas where invariants SHOULD exist but were not found]

## Key Observations for Threat Modeling
[Which invariants are most likely to be violated and why]
```
