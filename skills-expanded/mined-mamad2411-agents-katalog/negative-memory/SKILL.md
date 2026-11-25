---
name: negative-memory
description: >
  False-positive pattern query protocol. Mandatory check before every task
  generation step. Compares proposed task against known FP patterns in
  memory/negative/false-positives.jsonl. Prevents wasting reasoning budget
  on patterns already proven to be safe.
trigger: Before every task generation by the Threat Modeler. Not optional.
agents: [threat-modeler, judge]
---

# Negative Memory Skill

## Purpose

The negative memory is a growing database of patterns that *look* like
vulnerabilities but are NOT. Every REFUTED finding that wasn't caught by scope
rules should be added here so the harness doesn't make the same mistake twice.

**This is how the harness learns without rewriting its reasoning.**

## Pre-Task-Generation Protocol (Threat Modeler)

Before generating any task, run:

```bash
./scripts/check-negative-memory.sh \
  --function "{proposed_target_function}" \
  --invariant "{proposed_invariant}" \
  --keywords "{comma,separated,key,terms}"
```

### Interpreting Results

```
match_score > 0.8:  FLAG
  → Do not generate this task yet
  → Add note to INDEX.md: "TASK-{N} flagged for human review (FP pattern match)"
  → Document in task's negative_memory_check field: {checked: true, recommendation: flag_for_review}
  → Wait for human operator to approve before proceeding

match_score 0.5–0.8:  CAUTION
  → Generate task but lower priority by one level
  → Add to task: negative_memory_check.recommendation = proceed_with_caution
  → Add to out_of_scope_cases: the matched FP reason

match_score < 0.5:  PROCEED
  → Generate task normally
  → Document: negative_memory_check.match_score = {score}, recommendation = proceed
```

## Post-Refutation Protocol (Judge)

When the Judge marks a task as REFUTED, determine why:

```
Case A: The finding was REFUTED because it matched a known FP pattern
  → The pattern already exists in negative memory. No action.

Case B: The finding was REFUTED for a NEW reason not in negative memory
  → Generate a new FP record and append to memory/negative/false-positives.jsonl
  → Also insert into DB: false_positives table
```

### Writing a New FP Record

```json
{
  "pattern_id": "FP-{YYYYMMDD}-{N}",
  "contract_type": "{ERC4626 | AMM | Lending | Bridge | Governance | any}",
  "target_function": "{function_name}",
  "apparent_vuln": "{what it looks like}",
  "why_false_positive": "{precise technical reason it is NOT a vulnerability}",
  "detection_keywords": ["{keyword1}", "{keyword2}", "{keyword3}"],
  "added_by": "judge",
  "added_at": "{YYYY-MM-DD}",
  "task_id": "TASK-{N}"
}
```

### Quality Rules for FP Records

- **`why_false_positive`** must be technically precise, not vague
  - BAD:  "Not actually vulnerable"
  - GOOD: "CEI pattern is followed — state updated at L142 before external call at L148"

- **`detection_keywords`** must be specific enough to match similar future tasks
  - BAD:  ["withdraw", "token", "balance"]
  - GOOD: ["CEI", "state-before-call", "nonReentrant", "reentrancy-protected"]

- **`contract_type`** helps scope the match — "any" only when the FP is universal

## Seed Patterns (Pre-loaded)

The following patterns are pre-loaded in `memory/negative/false-positives.jsonl`:

| ID | Pattern | Why Safe |
|----|---------|---------|
| FP-SEED-001 | ERC4626 donation attack | Virtual shares offset makes it infeasible |
| FP-SEED-002 | Reentrancy with CEI | State updated before external call |
| FP-SEED-003 | AMM sandwich attack | Protocol design, not a bug |
| FP-SEED-004 | Flash loan governance | Snapshot at creation time, not execution |
| FP-SEED-005 | Initializer front-run | Deploy + init in one tx is safe |

## Growing the Database

After every completed audit:
1. Report Compiler counts REFUTED findings
2. Harness Critic reviews whether each REFUTED finding should become an FP record
3. Evolution Manager reviews the proposed additions
4. Records are added in batch to `memory/negative/false-positives.jsonl`

Over time, this database grows into the harness's institutional memory of
what NOT to chase — making each subsequent audit more precise.

## Immutability Rule

FP records are NEVER deleted. If a pattern is later determined to sometimes be
a real vulnerability, add a new record with:

```json
{
  "pattern_id": "FP-REVISION-{date}",
  "supersedes": "FP-SEED-001",
  "revision_note": "Virtual shares protection only applies to OZ v5+. OZ v4 ERC4626 is still vulnerable.",
  "detection_keywords": ["ERC4626", "virtualShares", "openzeppelin-v5"]
}
```

The old record stays. The revision adds nuance.
