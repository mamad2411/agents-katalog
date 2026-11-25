---
name: storage-layout-analysis
description: >
  Proxy patterns, slot collisions, upgrade safety. Used during decomposition
  to identify storage-related vulnerabilities in upgradeable contracts.
---

# Storage Layout Analysis Skill

## Purpose

Analyze storage slot assignments, proxy patterns, and upgrade safety. Storage collisions
and uninitialized proxy implementations are among the highest-severity bugs in DeFi.

## When to Use

- During decomposition when the project uses proxies (UUPS, Transparent, Beacon)
- When analyzing upgradeable contracts
- When checking for storage packing issues or slot collision risks

## Extraction Protocol

### Step 1: Identify Proxy Patterns

```bash
# Check for proxy-related imports
grep -rn "Proxy\|UUPSUpgradeable\|TransparentProxy\|Initializable\|ERC1967" --include="*.sol"

# Check for delegatecall
grep -rn "delegatecall" --include="*.sol"

# Check for initializer pattern (vs constructor)
grep -rn "function initialize\|modifier initializer" --include="*.sol"
```

### Step 2: Extract Storage Layout

```bash
# Foundry storage layout inspection
forge inspect {ContractName} storage-layout --pretty

# Slither variable ordering
slither . --print variable-order 2>/dev/null
```

### Step 3: Analyze for Risks

| Risk | What to Check |
|------|--------------|
| **Slot collision** | Does the implementation's storage overlap with proxy admin slots? |
| **Uninitialized implementation** | Can `initialize()` be called on the implementation directly? |
| **Storage gap missing** | Are `__gap` variables present for future upgrade safety? |
| **Inheritance order change** | Does re-ordering base contracts shift slot assignments? |
| **Immutable vs storage** | Are constants/immutables used where storage would be safer for upgrades? |

### Step 4: Cross-Version Comparison (if upgrading)

Compare storage layouts between V1 and V2:
- Same slot → same variable? (no collision)
- New variables appended at end? (safe)
- New variables inserted in middle? (COLLISION — critical)

## Output

```markdown
# Storage Layout Analysis

## Proxy Pattern
[UUPS / Transparent / Beacon / None]

## Storage Slots
| Slot | Variable | Type | Contract |
|------|----------|------|----------|
| 0 | owner | address | Ownable |
| 1 | totalSupply | uint256 | ERC20 |

## Risks Identified
[List any collisions, missing gaps, uninitialized implementations]

## Upgrade Safety
[Assessment of whether the contract can be safely upgraded]
```

Save to: `specs/decomposition/storage-layout-analysis.md`
