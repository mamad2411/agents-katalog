---
name: data-flow-tracking
description: >
  Source-to-sink analysis for user-controlled data. Track how attacker-controlled
  inputs flow through the system to state-changing operations.
---

# Data Flow Tracking Skill

## Purpose

Track how user-controlled data (function parameters, msg.value, msg.sender, calldata)
flows from external entry points (sources) to state-changing operations (sinks). This
is essential for identifying injection points, unchecked arithmetic, and oracle manipulation.

## When to Use

- During SAST phase and decomposition
- When the Threat Modeler needs to understand what an attacker controls
- When tracing how a manipulated value propagates through computation

## Sources (Attacker-Controlled Inputs)

| Source Type | Examples |
|------------|---------|
| Function parameters | `amount`, `recipient`, `deadline` |
| Transaction context | `msg.sender`, `msg.value`, `block.timestamp` |
| External call returns | `oracle.getPrice()`, `token.balanceOf()` |
| Storage that can be set by user | Allowances, user-set parameters |

## Sinks (Security-Critical Operations)

| Sink Type | Examples |
|----------|---------|
| Token transfers | `transfer()`, `transferFrom()`, `safeTransfer()` |
| State updates | `balances[user] = ...`, `totalSupply += ...` |
| External calls | `address.call{value: amount}("")` |
| Access control decisions | `require(msg.sender == owner)` |
| Mathematical computations | Division (precision loss), multiplication (overflow) |

## Tracking Protocol

### Step 1: Identify all external/public function parameters

```bash
grep -rn "function.*external\|function.*public" --include="*.sol" | grep -v "view\|pure"
```

### Step 2: For each parameter, trace forward through the function body

- Is it validated? (require, if-revert, bounds check)
- Is it used in arithmetic? (potential overflow/precision loss)
- Is it passed to another function? (trace recursively)
- Does it reach a sink without sanitization?

### Step 3: Document tainted paths

```markdown
## Tainted Data Flow: [function]

Source: `amount` parameter in `deposit(uint256 amount)`
Path: amount → _calculateShares(amount) → shares = amount * totalShares / totalAssets
Sink: `balances[msg.sender] += shares` (state update)
Sanitization: require(amount > 0) — but no upper bound check
Risk: If totalAssets is manipulable, shares calculation can be inflated
```

## Output

Save to: `specs/sast/data-dependencies.md`
