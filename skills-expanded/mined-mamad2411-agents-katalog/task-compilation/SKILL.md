---
name: task-compilation
description: Compile broad audit goals into structured proof obligations with 9 mandatory fields. Used after decomposition by the Threat Modeler agent.
trigger: After decomposition is complete and passes the Decomposition Gate.
agents: [threat-modeler, judge]
---

# Task Compilation Skill

> **Trigger**: After decomposition completes and passes the Judge's Decomposition Gate.
> **Purpose**: Transform decomposition artifacts into precise, executable proof obligations.

---

## Overview

A task is NOT a checklist item. It is a **proof obligation** — a contract between the system
and the Deep Reasoner that defines exactly what to examine, where to look, what would prove
danger, and what would prove safety. This skill enforces the protocol for creating high-quality
tasks that maximize reasoning efficiency.

---

## The 9 Mandatory Fields

Every task MUST contain all 9 fields. No exceptions. No "TBD" values.

### Field 1: Target
**What**: The exact contract + function(s) under examination.
**Quality Bar**: Must be a specific function, not a vague area.

| ✅ Good | ❌ Bad |
|---------|--------|
| `PnlAccounting.updateState()` | "The accounting system" |
| `Vault.withdraw(uint256, address, address)` | "Vault withdrawal flow" |
| `Router.swap() → Pool.execute()` | "Check the router" |

### Field 2: Execution Path
**What**: The specific call chain being analyzed.
**Quality Bar**: Must trace through specific functions, not hand-wave.

| ✅ Good | ❌ Bad |
|---------|--------|
| `withdraw → _burn → _convertToAssets → totalAssets()` | "The withdrawal path" |
| `deposit → _mint → _convertToShares → previewDeposit` | "How deposits work" |

### Field 3: Relevant State
**What**: All state variables, storage slots, and external dependencies that matter.
**Quality Bar**: Specific variable names with types.

```markdown
- `totalAssets` (uint256) — cached total assets value
- `_balances[msg.sender]` (uint256) — user's share balance
- `lastUpdateTime` (uint256) — timestamp of last oracle update
```

### Field 4: Attacker Capabilities
**What**: What the attacker can realistically do.
**Quality Bar**: Specific about resources and permissions.

| ✅ Good | ❌ Bad |
|---------|--------|
| "Can flash-loan up to 100M USDC. Can call all non-admin external functions. Can frontrun in the same block." | "An attacker" |
| "Owns governance tokens but below quorum threshold. Can propose but not pass." | "Has some governance power" |

### Field 5: Invariant
**What**: The property that MUST hold true. State as a formal condition.
**Quality Bar**: Must be mathematically precise or logically unambiguous.

| ✅ Good | ❌ Bad |
|---------|--------|
| `totalSupply * pricePerShare == totalAssets ± 1 wei` | "Prices should be correct" |
| `balanceOf(vault) >= sum(userDeposits) - sum(userWithdrawals)` | "Vault should be solvent" |

### Field 6: Failure Predicate
**What**: The EXACT condition that proves the invariant is broken.
**Quality Bar**: Must be **falsifiable** — you can write a test that checks this.

| ✅ Good | ❌ Bad |
|---------|--------|
| `totalAssets < totalLiabilities achievable by non-privileged caller in single tx` | "System might become insolvent" |
| `shares_received == 0 when assets_deposited > 0` | "Deposits might not give shares" |

### Field 7: Required Witness
**What**: What concrete evidence is needed to prove the issue.
**Quality Bar**: Specific about the form of evidence.

```markdown
# Good witness requirements:
"Concrete calldata sequence (function calls + parameters + ordering) starting
from a valid protocol state that causes totalAssets < totalLiabilities."

"A specific (amount, timestamp) pair where withdraw() reverts for a user
who should be able to withdraw."
```

### Field 8: Completion Contract
**What**: Binary condition — what counts as DONE. No ambiguity.
**Quality Bar**: Must be binary (done or not done).

```markdown
# Template:
"COMPLETE when EITHER:
(a) A concrete witness is produced that satisfies the failure predicate, OR
(b) Safety is proven with path-exhaustive evidence showing the invariant holds
    on all reachable states along this execution path."
```

### Field 9: Drift Anchors
**What**: 3-5 keywords that anchor the reasoner. The Judge checks output against these.
**Quality Bar**: Specific to this task, not generic.

| ✅ Good | ❌ Bad |
|---------|--------|
| `["share inflation", "first depositor", "rounding"]` | `["security", "vulnerability"]` |
| `["oracle staleness", "price deviation", "TWAP"]` | `["price", "attack"]` |

---

## Task Generation Protocol

### Step 1: Identify Invariants from Decomposition

Read `specs/decomposition/invariant-decomposition.md` and extract all formal invariants.

### Step 2: Map Invariants to Paths

For each invariant, identify which execution paths can affect it:
- Which entrypoints modify the relevant state?
- Which external calls introduce external dependencies?
- Which state transitions touch the invariant's variables?

### Step 3: Generate Tasks (Invariant × Path)

For each (invariant, path) pair where violation seems possible:
1. Fill all 9 fields
2. Assign priority: Critical / High / Medium / Low
3. Assign reasoning depth: Deep / Fast

### Step 4: Cross-Contract Tasks (CRITICAL)

Generate tasks for multi-contract flows:
- **Mint path A + burn path B**: Can different contracts desync accounting?
- **Oracle contract A used by contracts B and C**: Consistent consumption?
- **Liquidation across contracts**: Bad debt creation?
- **Multi-step user journeys**: State corruption across txs?

### Step 5: Deduplication

Check for heavily overlapping tasks. Two tasks overlap if they:
- Target the same function AND the same invariant
- Differ only in attacker capabilities (merge them)
- Are sub-paths of another task (keep the broader one)

---

## Quality Checklist (Judge Uses This)

Per task:
- [ ] All 9 fields present and non-empty
- [ ] Target is a specific function, not a vague area
- [ ] Failure predicate is falsifiable
- [ ] Completion contract is binary
- [ ] Drift anchors are specific (not "security" or "vulnerability")
- [ ] Required witness is concrete
- [ ] Attacker capabilities are realistic

Per task set:
- [ ] No heavily overlapping tasks
- [ ] Business-flow tasks present (cross-contract)
- [ ] Coverage across all identified invariants
- [ ] Priority distribution is reasonable (not everything is Critical)

---

## Common Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| "Check for reentrancy" | No target path, no invariant | Specify exact function, call chain, and what state must be consistent |
| "Look for access control issues" | No failure predicate | Define what unauthorized action specifically could occur |
| "There may be a risk with X" | Not a task, it's a hypothesis | Convert to a 9-field task or discard |
| Overlapping tasks | Wastes reasoning budget | Merge or pick the broader one |
| Missing business-flow tasks | Cross-contract bugs are missed | Generate tasks for multi-step user journeys |
| Generic drift anchors | Reasoner will drift | Use task-specific keywords |

---

## Output

Save tasks to: `specs/tasks/TASK-{number}-{short-name}.md`
Save index to: `specs/tasks/INDEX.md`
