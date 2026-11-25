---
name: solidity-decomposition
description: Solidity-specific decomposition - storage layout, inheritance tree, modifier chains, event emissions, error paths. Used during project ingestion by the Decomposer agent.
trigger: Project ingestion — when the Decomposer begins Stage 1 analysis of a new Solidity codebase.
agents: [decomposer, sast-integrator]
---

# Solidity Decomposition Skill

> **Trigger**: Project ingestion — when the Decomposer analyzes a new Solidity project.
> **Purpose**: Extract Solidity-specific structural facts that feed the 10-dimension decomposition.

---

## Overview

This skill provides protocols for extracting Solidity-specific structural information that
generic decomposition misses. It covers: inheritance hierarchies, storage layout analysis,
modifier chains, event/error catalogs, external call enumeration, and library usage patterns.

---

## Protocol

### 1. Inheritance Tree Extraction

Map the full inheritance hierarchy. Identify diamond inheritance, virtual overrides,
and shadowed functions.

```bash
# Extract all inheritance declarations
grep -rn "contract\|is " --include="*.sol" | grep " is "

# Identify interfaces vs abstract contracts vs concrete contracts
grep -rn "^interface \|^abstract contract \|^contract " --include="*.sol"

# Check for diamond inheritance (same base in multiple paths)
# Slither can produce this automatically:
slither . --print inheritance-graph 2>/dev/null
```

#### Output Table

| Contract | Inherits From | Type | Virtual Functions | Overrides |
|----------|--------------|------|-------------------|-----------|
| Vault | ERC4626, Ownable, ReentrancyGuard | Concrete | - | deposit, withdraw |

### 2. Storage Layout Analysis

Map all state variables with their storage slots. Critical for proxy/upgrade patterns.

```bash
# Foundry storage layout inspection
forge inspect {ContractName} storage-layout --pretty 2>/dev/null

# Manual state variable extraction
grep -rn "^\s*\(uint\|int\|address\|bool\|bytes\|string\|mapping\|struct\)" --include="*.sol" | grep -v "function\|event\|error\|//\|memory\|calldata"

# Identify immutable and constant variables (not in storage)
grep -rn "immutable\|constant" --include="*.sol"
```

#### Output Table

| Contract | Variable | Type | Slot | Offset | Notes |
|----------|----------|------|------|--------|-------|
| Vault | totalAssets | uint256 | 0 | 0 | - |
| Vault | _balances | mapping(address => uint256) | 1 | 0 | Inherited from ERC20 |

### 3. Modifier Chain Analysis

Catalog all modifiers and which functions use them. Missing modifiers = missing access control.

```bash
# Extract all modifier definitions
grep -rn "modifier " --include="*.sol"

# Extract all function declarations with modifiers
grep -rn "function.*\(onlyOwner\|nonReentrant\|whenNotPaused\|onlyRole\)" --include="*.sol"

# Find external/public functions WITHOUT access control modifiers
grep -rn "function.*\(external\|public\)" --include="*.sol" | grep -v "view\|pure\|onlyOwner\|onlyRole\|nonReentrant\|whenNotPaused\|internal\|private\|override"
```

#### Output Table

| Contract | Modifier | Applied To | Purpose |
|----------|----------|-----------|---------|
| Vault | onlyOwner | setFee, pause | Admin access control |
| Vault | nonReentrant | deposit, withdraw | Reentrancy protection |

### 4. Event Emission Catalog

Events are the protocol's audit trail. Missing events = missing observability.

```bash
# Extract all event definitions
grep -rn "event " --include="*.sol" | grep -v "//"

# Extract all event emissions
grep -rn "emit " --include="*.sol"

# Find state-changing functions that DON'T emit events
# (Compare external/public non-view functions against emit locations)
```

#### Output Table

| Contract | Event | Emitted In | Parameters |
|----------|-------|-----------|------------|
| Vault | Deposit | deposit() | sender, assets, shares |
| Vault | Withdraw | withdraw() | sender, receiver, assets, shares |

### 5. Error Path Analysis

Catalog all revert conditions. Missing reverts = missing validation.

```bash
# Custom errors
grep -rn "error " --include="*.sol" | grep -v "//"

# Require statements
grep -rn "require(" --include="*.sol"

# Revert statements
grep -rn "revert " --include="*.sol" | grep -v "//"

# Assert statements (should be rare — invariant checks only)
grep -rn "assert(" --include="*.sol"
```

### 6. External Call Enumeration

Every external call is a potential trust boundary crossing.

```bash
# Low-level calls
grep -rn "\.call\|\.delegatecall\|\.staticcall" --include="*.sol"

# High-level external calls (interface calls)
grep -rn "I[A-Z].*\." --include="*.sol" | grep -v "import\|//\|event\|error"

# Token transfers
grep -rn "\.transfer\|\.transferFrom\|\.safeTransfer\|\.safeTransferFrom" --include="*.sol"

# Approvals
grep -rn "\.approve\|\.safeApprove\|\.forceApprove" --include="*.sol"
```

### 7. Library Usage

Libraries change execution context (delegatecall vs internal).

```bash
# Library declarations
grep -rn "^library " --include="*.sol"

# Using-for directives
grep -rn "using .* for" --include="*.sol"
```

---

## Output Format

Save all structural facts to `specs/decomposition/solidity-structure.md`:

```markdown
# Solidity Structure Decomposition

## Inheritance Hierarchy
[Inheritance tree with diamond detection]

## Storage Layout
[Per-contract slot mapping]

## Modifier Coverage
[Functions × Modifiers matrix, highlighting unprotected externals]

## Event Coverage
[State-changing functions × Events, highlighting silent mutations]

## Error Conditions
[Validation catalog: requires, custom errors, asserts]

## External Call Map
[All outbound calls with trust level annotations]

## Library Usage
[Using-for directives and execution context]
```

---

## Key Observations to Surface

For the Threat Modeler, always highlight:
1. **Unprotected external functions** — public/external without access control
2. **State changes after external calls** — potential reentrancy
3. **Missing events on state changes** — observability gaps
4. **Complex inheritance** — function resolution order issues
5. **Storage gaps in upgradeable contracts** — slot collision risks
6. **Unchecked return values** — silent failures
