---
name: Aristotle Workflow
description: This skill should be used when the user asks to "prove a theorem", "formalize to Lean", "use Aristotle", "fill sorries", "verify proofs", "verify algorithm", "verify code correctness", "check implementation", "find bugs in code", "work with Lean 4", "VERINA", or needs guidance on theorem proving, code verification, algorithm correctness, Lean formalization, or Aristotle AI integration.
version: 1.1.0
---

# Aristotle: Theorem Proving & Code Verification

## Overview

Aristotle is an AI system from Harmonic with two major capabilities:

1. **Theorem Proving** - Gold-medal IMO 2025 performance (5/6 problems), solved open Erdos problems
2. **Code Verification** - 96.8% accuracy on VERINA benchmark, verifies algorithm correctness

**Key insight**: Aristotle works best with hints. For theorems, provide informal proofs. For code, provide clear pre/postconditions.

---

## Code Verification (VERINA-Style)

Aristotle verifies algorithm implementations against formal specifications. It either proves correctness or finds counterexamples.

### Verification Structure

```lean
-- 1. PRECONDITION: Input constraints
def algorithm_precond (input : Type) : Prop := ...

-- 2. ALGORITHM: Implementation to verify
def algorithm (input : Type) (h : algorithm_precond input) : OutputType := ...

-- 3. POSTCONDITION: Required output properties
def algorithm_postcond (input : Type) (result : OutputType)
    (h : algorithm_precond input) : Prop := ...

-- 4. SPECIFICATION: Verification goal
theorem algorithm_spec_satisfied (input : Type)
    (h : algorithm_precond input) :
    algorithm_postcond input (algorithm input h) h := by
  sorry
```

### Verification Outcomes

- **Proof found**: Algorithm is correct
- **Counterexample**: Bug detected, e.g., `use [4, 1, 2, 1, 4], 2; native_decide`
- **False detected**: Specification or implementation is wrong

### Verified Algorithms (Examples)

Aristotle has verified (from VERINA benchmark):
- Selection sort correctness
- Run-length encoding
- Longest increasing subsequence
- 160+ algorithm implementations

See `references/code-verification.md` for detailed code verification patterns.

---

## Theorem Proving (Erdos-Style Workflow)

Follow this pipeline for best results:

```
1. Research/Understand problem
2. Write proof strategy (natural language)
3. Generate rigorous informal proof
4. Verify proof logic
5. Aristotle: Formalize to Lean ← PRIMARY USE
6. Fix Lean warnings
7. Verify no sorryAx contamination
```

## Step-by-Step Process

### Step 1: Write Informal Proof First

Before invoking Aristotle, write a complete informal proof. Break it into small, provable lemmas.

**Example:**
```
Proof: Let r be a rule with ID n. For r to be its own child,
there must exist an evaluation e that created r, and e must belong to r.
But e can only exist after r fires, which requires r to already exist.
Since rule IDs are assigned sequentially, any child rule created during
r's evaluation would have ID > n. Therefore r cannot reference itself
as a parent. QED
```

### Step 2: Create Lean Scaffold with Hints

Add the informal proof as a docstring with `PROVIDED SOLUTION`:

```lean
/--
Proof: Rule IDs are monotonically increasing. A rule r with ID n can only
create child rules with IDs > n during its evaluation.

PROVIDED SOLUTION
Use monotonicity of nextRuleID. Show that any rule created during an eval
of r has ID > r.id. Apply induction on rule creation sequence.
-/
theorem no_self_child (r : Rule) : ¬isChildOf r.id r.id w := by
  sorry
```

### Step 3: Prepare Standalone File

**Critical**: Aristotle runs in the cloud with Lean 4.24.0 + mathlib 4.24.0. Custom library imports will fail.

For custom libraries, inline type definitions:

```lean
-- aristotle_task.lean (no imports!)

-- Inline minimal type definitions
structure RuleID where
  id : Nat
  deriving BEq, Hashable, Repr

structure Rule where
  id : RuleID
  parent : Option EvalID

/--
PROVIDED SOLUTION
Use induction on rule creation sequence.
-/
theorem rule_parent_strictly_less (r : Rule) :
    r.parent = some evalId → evalId.id < r.id.id := by
  sorry
```

### Step 4: Submit to Aristotle

```bash
# Standalone file (custom libraries)
uvx --from aristotlelib aristotle prove-from-file theorem.lean \
  --no-validate-lean-project --no-auto-add-imports

# Mathlib project
cd /path/to/project
uvx --from aristotlelib aristotle prove-from-file lib/File.lean

# With context folder
uvx --from aristotlelib aristotle prove-from-file FILE.lean \
  --context-folder lib/ --no-auto-add-imports
```

Expect 3-6 minutes queue time (QUEUED → IN_PROGRESS → Complete).

### Step 5: Verify Proofs

**Critical verification step**—always check for sorryAx contamination:

```lean
#print axioms my_theorem
-- Should NOT show: 'my_theorem' depends on axioms: [sorryAx]
```

If `sorryAx` appears, the proof exploited an upstream sorry and is invalid.

## Writing Effective Hints

Aristotle's policy conditions on informal proof. Add `PROVIDED SOLUTION` in docstrings:

**Good hint patterns:**
- Reference specific lemmas: "apply Nat.add_comm"
- Describe strategy: "by induction on n"
- Mention key insights: "since HashMap.get? is deterministic"
- Break into steps: sequence of small claims

**Example:**
```lean
/--
Prove that the queue is empty after convergence.

PROVIDED SOLUTION
Use induction on queue length. Each step processes one item,
reducing queue size. When size reaches 0, we're converged.
Apply convergeN_decreases_queue and Nat.lt_wfRel.
-/
theorem converge_empties_queue (w : World) : ... := by
  sorry
```

## Critical Limitations

### 1. Cloud Environment
- Lean 4.24.0 + mathlib 4.24.0
- Custom libraries don't compile
- Solution: Create standalone files with inlined definitions

### 2. Upstream Sorries Contaminate Proofs
If your codebase has sorries, Aristotle may "prove" theorems by exploiting them. The proof compiles but is logically unsound.

**Always verify:**
```lean
#print axioms theorem_name
```

### 3. Aristotle Detects False Theorems
Aristotle correctly identifies false statements and provides counterexamples:
```lean
/-
Aristotle found this block to be false.
Here is a proof of the negation:
-/
theorem false_claim_neg : ¬ (false_claim) := by
  use ⟨0⟩; aesop  -- counterexample
```

### 4. Queue Time
Expect 3-6 minutes. Use `--no-wait` for fire-and-forget:
```bash
uvx --from aristotlelib aristotle prove-from-file FILE.lean --no-wait
```

## Iteration Strategy

When Aristotle fails:

1. **Break into smaller lemmas** - Finer decomposition helps
2. **Provide alternative proof strategy** - Different approach may work
3. **Add intermediate claims** - More stepping stones for formalization

Aristotle internally decomposes proofs into lemmas and iterates with formal feedback.

## CLI Quick Reference

```bash
# Basic usage
uvx --from aristotlelib aristotle prove-from-file FILE.lean

# Standalone file (no project validation)
uvx --from aristotlelib aristotle prove-from-file FILE.lean \
  --no-validate-lean-project --no-auto-add-imports

# With context files
uvx --from aristotlelib aristotle prove-from-file FILE.lean \
  --context-folder ./lib --no-auto-add-imports

# Save to specific output
uvx --from aristotlelib aristotle prove-from-file FILE.lean \
  --output-file my_proofs.lean

# Fire and forget
uvx --from aristotlelib aristotle prove-from-file FILE.lean --no-wait
```

## What NOT to Do

- **Trust proofs without checking `#print axioms`**
- **Run on files with upstream sorries**
- **Use custom library imports directly**
- **Expect instant results** (3-6 min queue)
- **Submit huge files** - use `admit` to focus
- **Expect proof discovery from scratch** - provide informal proof
- **Write monolithic hints** - break into small lemmas

## Additional Resources

### Reference Files

For detailed patterns and techniques, consult:
- **`references/architecture.md`** - Aristotle's internal architecture
- **`references/advanced-workflows.md`** - Complex proof strategies
- **`references/code-verification.md`** - VERINA-style code verification
- **`references/troubleshooting.md`** - Common issues and solutions

### Example Files

Working examples in `examples/`:
- **`standalone-theorem.lean`** - Standalone file template
- **`mathlib-theorem.lean`** - Mathlib project example
- **`selection-sort-verification.lean`** - Algorithm verification example

### Scripts

Utilities in `scripts/`:
- **`verify-proof.sh`** - Verify proof doesn't depend on sorryAx
- **`create-standalone.sh`** - Help create standalone theorem files
