---
name: cli-audit-drift
metadata:
  author: clement
description: >
  Detect silent semantic drift between intended behavior (CONTRACTS.md) and actual implementation.
  Scans code against functional contracts, invariants, and known drift history to catch behavioral
  changes that compile and run but violate the original intention. Use when reviewing code changes,
  before commits, auditing behavioral conformity, or saying 'check drift', 'contract check',
  'intention vs implementation', 'semantic drift', 'is this still correct', 'does this match the spec',
  'behavioral regression', 'silent bug', 'autophagy scan'. Also triggers on 'CONTRACTS.md',
  'invariant check', 'intention audit', 'contract violation'.
argument-hint: "[file-or-directory-or-function-name]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output (reports, files, documentation), detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit Drift — Semantic Conformity Scanner

Detect silent behavioral drift between what code **was supposed to do** (intention) and what it **actually does** (implementation). The most dangerous bugs are not crashes — they are functions that still run, still return values, but no longer honor their original contract.

> "The New Caledonian crow does not merely endure its environment — it identifies the mismatch between what it intended to do and what actually happened. Not a noisy error. A result that does not match the intention."

## Core Principle — Three biological mechanisms

| Organism / mechanism | What it does in nature | What it does in this skill |
|----------------------|------------------------|----------------------------|
| **New Caledonian crow** | Detects the gap between intention and result | Compares CONTRACTS.md (intention) against code (behavior). Names the gap precisely. Asks if intentional or accidental |
| **Cellular autophagy** | Continuous surveillance, isolates damaged components | Scans all contracted functions, isolates non-conforming code, proposes minimal correction or contract update |
| **Protein folding + chaperones** | A 1D amino-acid sequence folds into a 3D functional structure; chaperones (HSP60/70) detect misfolds and force a clean re-fold from scratch | Contract (intent, 1D) "folds" into code (behavior, 3D); detected drift triggers a *minimal re-derivation from the contract*, never a patch on top of the drifted state. Removed contracts trigger explicit code deletion (ubiquitin tag) |

### Why folding is the unifying frame

A protein's amino-acid sequence is its **intention** (linear, source-of-truth). What the protein *does* in the cell depends on its **folded structure** (3D, emergent). The two are linked by physical laws but the link is not automatic — proteins can misfold and **still exist**. A misfolded protein takes up space, consumes ATP, and silently fails to do its job. It does not crash. It does not throw. It just no longer matches its intent.

That is exactly what semantic drift looks like in code. The contract (CONTRACTS.md) is the sequence. The implementation is the folded structure. Drift is misfolding — and like misfolding, it is invisible to compilation, type checking, and "the tests still pass".

The cell handles misfolding with two mechanisms that map directly onto this skill:

1. **Chaperones (HSP60/HSP70)** detect misfolding and force a *complete unfold and re-fold from a clean state*. They never patch a partially-misfolded protein in place — patching is impossible because the misfolding is structural, not local. → **Skill rule:** when drift is detected, propose a *minimal correct fix that re-derives the code from the contract*, never a patch on top of the drifted state. This is the ground truth behind rule #3 ("Minimal fixes only"): you are not repairing a wound, you are re-folding a polypeptide.

2. **Ubiquitin tagging + proteasome** is the explicit "to be destroyed" tag the cell posts on proteins that fail re-folding. The cell does not rely on reference counting — it actively marks for destruction, and the proteasome digests anything carrying the tag. → **Skill rule:** when a contract is removed but its implementation lingers, flag it as **Orphan code** — the code equivalent of an unubiquitinated misfolded protein — and propose explicit deletion. Without active tagging, orphan code accumulates as toxic tech debt that no garbage collector will ever reclaim.

The deep takeaway: **a working protein matches its sequence's intent; a working function matches its contract's intent**. Drift is misfolding, and the only sustainable response is the cell's response — detect early, reset cleanly, mark explicitly. Patching never works in biology, and it does not work in code either.

## Mitosis — Scale to scope

| Scope | Tier | Behavior |
|-------|------|----------|
| Single function | **S** | Scan that function against its contract only |
| File or small directory (<10 contracted functions) | **M** | Full scan, all contracts in scope |
| Entire project (>10 contracted functions) | **L** | Sample top 15-20 highest-risk contracts (most recent changes, most dependencies) |

For tier **L**: prioritize contracts whose implementation files appear in `git log --since="2 weeks ago"`.

## Input

`$ARGUMENTS` is the target to scan:

- **Function name** (`mask`, `calculate_price`): scan that specific function against its contract
- **File or directory** (`src/core/`, `lib.rs`): scan all contracted functions found in that scope
- **Empty**: scan the entire project against all contracts in CONTRACTS.md

## Workflow

### Step 0 — Locate or bootstrap CONTRACTS.md

1. Search for `CONTRACTS.md` at project root, then `docs/CONTRACTS.md`, then `contracts/`
2. If found: read it, proceed to Step 1
3. If NOT found: switch to **Bootstrap Mode** (see below)

**Step 0b — Verify drift surveillance instructions:**

1. Search for drift surveillance instructions in: `CONTRIBUTING.md`, `.claude/settings.json`, or project docs
2. If missing: append a drift surveillance section to the report as a recommended update to `CONTRIBUTING.md`
3. If outdated (references functions no longer in CONTRACTS.md): propose an update

### Step 1 — Parse contracts

For each contracted function/endpoint, extract:
- **Intention**: what it should do (natural language)
- **Invariants**: properties that must always hold (formal-ish)
- **Known drifts**: historical drift log with dates
- **Red flags**: specific code patterns that indicate drift

Read `references/invariant-patterns.md` for common invariant categories.

### Step 2 — Locate implementations

For each contracted function:
1. Find its definition (grep for function signature, method, endpoint)
2. Read the full implementation
3. If the function calls other contracted functions, note the chain

### Step 3 — Scan for drift (Crow)

For each contracted function, check:

**Invariant violations:**
- Does the implementation honor every listed invariant?
- Are there conditional branches that break uniformity invariants?
- Are there side effects not declared in the contract?

**Red flag detection:**
- Does the code contain any pattern listed in "Red flags"?
- Are there special cases for values that should be treated uniformly?

**Behavioral divergence:**
- Does the function's actual behavior match the stated intention?
- Could a reasonable input produce output that violates the intention?
- Has a recent change (git diff) introduced a divergence?

Read `references/drift-detection-rules.md` for detailed detection heuristics.

### Step 4 — Classify findings (Autophagy)

For each detected drift:

| Classification | Meaning | Action |
|---------------|---------|--------|
| **Miss** | Unintentional deviation from contract | Propose minimal fix (re-fold from contract, do not patch) |
| **Evolution** | Intentional change, contract not updated | Propose contract update + alert stakeholders |
| **Ambiguity** | Contract is vague, implementation chose one interpretation | Propose contract clarification |
| **Stale contract** | Contract references code that no longer exists | Propose contract cleanup |
| **Orphan code** | Code implements behavior whose contract has been removed (the contract was deleted from CONTRACTS.md but the implementation lingers) | Propose explicit deletion — the ubiquitin tag. If the code is still load-bearing, the contract must be re-introduced; otherwise it is dead protein and must be digested |

### Step 5 — Generate report

Use the output format below.

### Step 6 — Update drift history

If drifts were found, propose additions to the "Known drift history" section of each affected contract.

## Bootstrap Mode

When no CONTRACTS.md exists, the skill switches from audit to generation:

1. **Discover critical functions**: Scan the codebase for functions that are:
   - Public API endpoints
   - Core business logic (domain layer)
   - Functions with complex invariants (state machines, calculators, validators)
   - Functions that have had bugs (check git log for fix commits)

2. **Infer intentions**: For each function, read:
   - The function's docstring/comments
   - Its test cases (what do tests assert?)
   - Its git history (what was it supposed to fix/add?)
   - Its callers (what do consumers expect?)

3. **Generate CONTRACTS.md**: Read `references/contracts-template.md` for the template. Generate contracts for the top 5-10 critical functions.

4. **Propose CONTRIBUTING.md additions**: Read `references/drift-surveillance-template.md` for the drift surveillance instructions to add to the project's `CONTRIBUTING.md` (section "Drift Surveillance").

5. **Output**: deliver CONTRACTS.md + CONTRIBUTING.md snippet, explain how to use them.

## Output Format

```markdown
# Semantic Drift Audit — {project-name}

**Date:** {date}
**Scope:** {what was scanned}
**Contracts loaded:** {N} functions from CONTRACTS.md
**Drifts detected:** {N} ({misses} misses, {evolutions} evolutions, {ambiguities} ambiguities)

## Drift Report

### {function-name} — {drift-classification}

**Contract says:** {quoted intention from CONTRACTS.md}
**Implementation does:** {observed behavior}
**Gap:** {precise description of the divergence}
**Evidence:** `{file}:{line}` — {code snippet showing the drift}
**Invariant violated:** {which invariant, if applicable}

**Recommendation:**
- {action: fix / update contract / clarify / ask PO}
- {minimal code change if miss}

---
(repeat for each drift)

## Contract Health Summary

| Function | Status | Last verified | Drifts found |
|----------|--------|--------------|-------------|
| mask(data, fields) | DRIFT | {date} | 1 miss |
| calculate_price() | CLEAN | {date} | 0 |
| ... | | | |

## Proposed CONTRACTS.md Updates

(diff-style additions to the drift history section)

## Drift Surveillance Status

**Instructions in CONTRIBUTING.md:** {PRESENT / MISSING / OUTDATED}
{if MISSING or OUTDATED: proposed additions below}

### Proposed CONTRIBUTING.md additions

(copy-pasteable block with drift surveillance instructions)
```

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| Contract or review exposes optimization intent but no semantic candidate has been mapped | `/cli-audit-xray` | X-Ray names candidate rewrites and the invariants they would require |
| Contracted functions have god-level complexity | `/cli-audit-tangle` | Topology suggests extraction before contract can be enforced |
| Drift caused by dependency update | `/cli-forge-infra` | Check version compatibility |
| No tests covering contracted behavior | `/cli-audit-test` | Test the invariants |
| Performance invariant present in CONTRACTS.md (« p95 < 100 ms ») but no bench enforces it | `/cli-forge-perf` | Translate the perf invariant into an executable A/B bench gate via the protocol catalogue + native harness routing |
| Drift changes schema meaning, transaction boundaries, lifecycle transitions, or persistent invariants | `/cli-audit-data` | Verify the database consequence under migration and concurrency |

**Rule:** Recommend, don't auto-execute.

## Rules for the Scanner

1. **Never auto-fix silently.** Name the gap, classify it, propose the fix — but always ask. The crow identifies inadequacy before acting.
2. **Contract is truth until proven intentionally outdated.** If code disagrees with the contract, the code is suspect — not the contract. Only the human decides to update the contract.
3. **Minimal fixes only.** Don't refactor. Don't improve. Fix the exact drift, nothing more.
4. **Check recent changes first.** `git diff` and `git log` on contracted functions are the first place drift appears.
5. **Invariants > intentions.** A vague intention is hard to audit. A formal invariant is machine-checkable. Prioritize invariant violations.
6. **Chain awareness.** If `process()` calls `mask()` and `mask()` has drifted, `process()` is also affected. Report the chain.
7. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-audit-xray` | Extracts missing invariants from optimization candidates. cli-audit-drift verifies or records them as behavioral contracts |
| `cli-audit-test` | D13 audits whether drift detection **tools** exist. cli-audit-drift **is** the drift detection |
| `cli-audit-code` | Scores code quality. cli-audit-drift checks **behavioral conformity** to intentions |
| `cli-audit-sync` | Checks doc-code coherence. cli-audit-drift checks **contract-code coherence** |
| `cli-forge-doc` | Can generate documentation. cli-audit-drift generates **CONTRACTS.md** (a different artifact) |
| `cli-cycle` | Should call cli-audit-drift as part of the full project review; emit `.claude/cli-audit-drift.json` per `../shared/result-schema.md` for orchestrator aggregation |
| `cli-audit-data` | Supplies persistent invariants and migration semantics; drift verifies their intended meaning |

## What this skill does NOT do

- **Does not run tests** — it reads code and contracts
- **Does not replace tests** — it complements them (tests check examples, contracts check intentions)
- **Does not auto-fix** — it proposes, the human decides
- **Does not generate test code** — it generates contract documents
- **Does not check compilation** — it checks semantic conformity
