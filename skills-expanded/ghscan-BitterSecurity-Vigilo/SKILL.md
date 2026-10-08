---
name: poc
description: >
  Generates and validates Foundry PoC tests from attack scenario documents. Use when:
  (1) Audit Phase 3 invokes Skill(vigilo:poc) for each High/Medium finding,
  (2) A finding at .vigilo/findings/ needs PoC validation,
  (3) Converting attack scenarios into executable Foundry tests.
  Outputs: test/poc/{finding-id}.t.sol, .vigilo/poc/ validation logs.
argument-hint: <finding-path.md>
---

# PoC Generation & Validation

**Input**: $ARGUMENTS (attack scenario file path)

---

# Part 1: PoC Code Generation

## Core Principle

```
1 Attack Scenario = 1 PoC Code
```

## Workflow

### 1. Read Attack Scenario

```
Read(".vigilo/findings/{severity}/{auditor}/{Severity}-{id}-{title}.md")
```

Example: `.vigilo/findings/high/logic/H-01-donation-attack-inflated-collateral.md`

Extract: Finding ID, Bug Class, Preconditions, Attack Steps, Impact, Vulnerable Code

### 2. Generate PoC

**File**: `test/poc/{Severity}-{id}-{title}.t.sol`

Example: `test/poc/H-01-donation-attack-inflated-collateral.t.sol`

**NOTE**: PoC code goes in `test/poc/` (project root), NOT in `.vigilo/` folder.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "forge-std/console2.sol";

contract PoC_{ID}_{BugClass} is Test {
    // State variables, actors

    function setUp() public {
        // Reproduce preconditions
    }

    function test_Exploit_{ID}() public {
        // 1. Log initial state
        // 2. Execute attack steps
        // 3. Log final state
        // 4. Assert impact
    }
}
```

### 3. PoC Checklist

- [ ] setUp(): Fully reproduce preconditions
- [ ] Actor labels: Use `makeAddr()` for all addresses
- [ ] console2.log: Output before/after attack state
- [ ] Attack steps: Follow scenario order exactly
- [ ] **Impact assertion: Directly prove scenario's claimed impact** (required)

### 4. Bug Class Patterns

Detailed templates: [references/poc-templates.md](references/poc-templates.md)

---

# Part 2: Foundry Validation

## Core Principle

```
Test Pass ≠ Vulnerability Validated
```

**Goal**: Verify that the Attack Scenario's claimed Impact actually occurs

## Workflow

### 1. Execute Test

```bash
forge test --match-test "test_Exploit_{ID}" -vvv
```

| Verbosity | Use Case |
|-----------|----------|
| `-vvv` | Default recommended |
| `-vvvvv` | Detailed debugging |

### 2. Analyze Results

| Result | Meaning | Action |
|--------|---------|--------|
| PASS + Impact proven | Vulnerability valid | → Complete |
| PASS + Impact unclear | Insufficient verification | → Strengthen assertions |
| FAIL | Issue occurred | → Fix PoC (max 3 attempts) |

### 3. Impact Verification

```
Scenario Impact → Assertion Mapping
─────────────────────────────────────
"Vault drain"     → assertGt(attackerAfter, attackerBefore)
"Collateral loss" → assertLt(userAfter, userBefore)
"Admin bypass"    → assertTrue(attacker.hasRole(ADMIN))
```

### 4. Modification Workflow

```
Test failure or Impact mismatch
          ↓
    Fix PoC (max 3 attempts)
          ↓
    After 3 failures → Review Attack Scenario
          ↓
    If scenario needs update → Reverse-modify
```

**If PoC validation differs from scenario, update Attack Scenario**:
- Expected profit ≠ actual profit → Update Impact numbers
- Additional precondition needed → Update Preconditions
- Exploit impossible → Downgrade severity or mark Invalid

### 5. Output

**Files** (use same naming format `{Severity}-{id}-{title}`):
```
test/poc/H-01-donation-attack.t.sol            # PoC code (project root)
.vigilo/poc/H-01-donation-attack.md            # Validation log
.vigilo/findings/high/logic/H-01-donation-attack.md  # (Modified) Attack Scenario
```

**Naming Convention**: `{Severity}-{id}-{kebab-case-title}`
- Same format across all three file types
- Makes it easy to track: scenario → PoC code → validation log

---

## Reference Files

| File | When to Load |
|------|--------------|
| [poc-templates.md](references/poc-templates.md) | When writing PoC - Bug class patterns |
| [debugging.md](references/debugging.md) | When test fails - Error resolution |
