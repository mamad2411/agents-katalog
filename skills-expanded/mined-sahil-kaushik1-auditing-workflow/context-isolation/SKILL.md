---
name: context-isolation
description: >
  Enforce that untriggered knowledge is not loaded and irrelevant context
  is excluded. Three types: trigger, responsibility, and per-task isolation.
  v2: adds hierarchical decomposition protocol and per-task token budget enforcement.
---

# Context Isolation Skill v2

## Purpose

> "If it is not triggered, do not read it. If it is irrelevant, do not place it in
> the current context."

Splitting prompts into files is NOT real isolation if the agent still reads all of them.
This skill enforces actual isolation at three levels plus a **budget enforcement layer**.

---

## Three Isolation Types

### 1. Trigger Isolation
Skills are loaded ONLY when their trigger condition is met.

| Skill | Trigger | When NOT to load |
|-------|---------|-----------------|
| `foundry-harness` | During verification | During decomposition |
| `defi-patterns` | During threat modeling | During verification |
| `drift-detection` | During reasoning | During decomposition |
| `economic-modeling` | Economic Analyst stage | All other stages |
| `fuzzing-integration` | task.phase = 5/6/7 | All other phases |
| `flow-compilation` | Flow Mapper stage | All other stages |

**Rule**: If a skill's trigger condition is not met, the agent MUST NOT read it.

### 2. Responsibility Isolation
Each agent sees ONLY its role-relevant artifacts.

| Agent | Can See | Cannot See |
|-------|---------|------------|
| Deep Reasoner | Task file, context package, target code | Verifier conclusions, other task reasoning |
| Verifier | Task file, `claim.md` ONLY (stripped) | Full reasoning chain-of-thought |
| Judge | Both reasoner and verifier outputs | Nothing restricted |
| Decomposer | Source code headers first, SAST facts | Previous audit findings (anchoring bias) |
| Threat Modeler | Flow slices, decomposition summary | Individual contract source code |
| Skeptic | Reasoning output, task file | Verifier output, Economic Analyst output |

**Rule**: Agents MUST NOT consume artifacts outside their responsibility boundary.

### 3. Per-Task Context Isolation
The Context Builder (and `slice-context.sh`) provides ONLY task-relevant context.

For a task targeting `Vault.withdraw()`:
- ✅ Include: `Vault.sol`, imported interfaces, ERC20 token contract
- ✅ Include: State variables listed in the task's `Relevant State` field
- ✅ Include: Functions transitively called by `withdraw()` (depth ≤ 2)
- ❌ Exclude: `Governance.sol` (unless the task involves governance)
- ❌ Exclude: Frontend config, test files, deployment scripts
- ❌ Exclude: Contracts not reachable from the target function

**Rule**: Context packages MUST document what was excluded and why.

---

## Hierarchical Decomposition Protocol (Large Codebases)

For protocols with > 10 contract files, context MUST be loaded hierarchically.
This is the primary mitigation for context window overflow.

### Pass 1 — Header Scan (low token cost)
Load ONLY the structural header of every contract:
```bash
# For each .sol file:
grep -E "^(pragma|contract|abstract|interface|library|    function|    event|    error|    struct|    mapping|    uint|    address)" TargetContract.sol | head -40
```

This gives you: contract name, all function signatures, all state variable types.
**Do NOT load function bodies in Pass 1.**

Token cost per contract: ~200-500 tokens (vs 5,000-20,000 for full file).
For 30 contracts: ~6,000-15,000 tokens total (fits in context easily).

### Pass 2 — Priority Deep-Read (targeted)
From Pass 1 results, identify the top-priority contracts:
- Contracts holding user funds (balances, deposits, stakes)
- Contracts callable by untrusted users
- Contracts with known high-risk patterns (upgradeable, oracle-reading, fee-collecting)

**Deep-read only these contracts** (full function bodies).
Typical result: 3-7 contracts, ~15,000-40,000 tokens total.

### Pass 3 — Dependency Pull (on demand)
As specific tasks are assigned, use `slice-context.sh` to pull:
- The target function's body
- Its direct callees (depth 1-2)
- Relevant state variables
- Required interfaces

**Per-task budget**: respect `context.max_tokens_per_task` from `audit.config.yml`.

---

## Token Budget Enforcement

The Context Builder MUST enforce budget caps before handing off to Reasoners.

| Severity | Max Context Tokens | Action if Over Budget |
|----------|-------------------|-----------------------|
| Critical | 8,000 | Re-slice with depth=1 |
| High     | 6,000 | Re-slice with depth=1 |
| Medium   | 4,000 | Header scan only |
| Low      | 2,000 | Function signature only |

If re-slicing still exceeds budget:
1. Keep: target function body + direct callees only (depth=0)
2. Append: summary header of excluded files ("These files were excluded due to budget: ...")
3. Document in task: `context_budget_warning: true`

---

## Enforcement

1. **Context Builder** runs `slice-context.sh` for every task before assigning to Reasoner
2. **Orchestrator** verifies `specs/context/TASK-{N}-context.md` exists before dispatching
3. **Judge** checks that reasoning outputs don't reference excluded context
   (would indicate isolation violation or the agent loaded extra files)
4. **Harness Critic** reviews isolation violations in the evolution cycle

## Why This Matters

Without real isolation:
- One huge prompt becomes several smaller prompt fragments (same problem)
- Irrelevant context dilutes attention on the actual task
- Anchoring bias from previous findings prevents fresh analysis
- Context overload causes the model to take shortcuts (vulnerability drift)
- 30-contract codebases become impossible to fully analyze in a single pass

With hierarchical + per-task isolation:
- Every Reasoner gets a focused, ~4,000-8,000 token package
- Full 50+ contract protocols become analyzable without context truncation
- Reasoning quality improves because signal-to-noise is higher
