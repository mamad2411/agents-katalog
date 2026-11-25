---
name: gap-computing-ledger
description: >
  Computes desired-current state deltas, quantifies component scores, and
  produces a ranked gap ledger. Use when evaluating hypothesis register
  state to determine where the largest gaps exist between desired and
  current conditions.
license: Complete terms in LICENSE.txt
serves: gap-definer
domain: gap-analysis
affects: gap-ledger-state
depends-on: none
produces: scored-gap-records
---

# Gap Ledger Computation

Compute the distance between desired state and current state for each
hypothesis and proposal in the register. Produce scored, ranked gap
records that drive prioritization.

---

## Process

### Step 1: Extract Desired and Current States [S]

For each hypothesis section (Problem, Segment, Unit Economics, Value
Proposition) and each proposal section (Growth Architecture, Solution
Design, GTM Plan):

1. Read the Desired State block. List every condition under "SUPPORTED means."
2. Read the Current State block. For each condition, record its fulfillment status: MET, PARTIAL, MISSING, or CONTRADICTED.
3. If a section has no Desired State block, mark the entire section as having a gap of type EVIDENCE_STRENGTH with note "no desired state defined."

**Gate:** `states_extracted: bool` -- every register section has a desired/current pair or is flagged as missing.
- Pass: Step 2.
- Fail: flag missing sections and proceed with available data.

### Step 2: Score Each Gap [R]

For each condition that is not MET, compute a gap record using these scales:

**Confidence Gap (0-3):**

| Current Confidence | Desired Confidence | Score |
|---|---|---:|
| unvalidated | supported | 3 |
| researched | supported | 2 |
| supported but thin | supported (robust) | 1 |
| supported | supported | 0 |

**Evidence Weakness (0-3):**

| Evidence Profile | Score |
|---|---:|
| Only T3 / assertion-heavy | 3 |
| Mostly T2 | 2 |
| Mixed T1/T2 but thin | 1 |
| Enough T1 for decision | 0 |

**Pain Uncertainty (0-3):**

| Pain Clarity | Score |
|---|---:|
| Unclear whether pain is real or acute | 3 |
| Partially clear | 2 |
| Mostly clear | 1 |
| Clear | 0 |

**Time Penalty (0-2):**

| Deadline Status | Score |
|---|---:|
| Exceeded | 2 |
| Due or near due | 1 |
| Within deadline | 0 |

**Blast Radius Weight (1-3):**

| Impact If Wrong | Weight |
|---|---:|
| Strategy collapses | 3 |
| One major hypothesis must change | 2 |
| Local revision only | 1 |

**Final Priority Score:**
```
Final Priority = (Confidence Gap + Evidence Weakness + Pain Uncertainty + Time Penalty) x Blast Radius Weight
```

**Gate:** `all_gaps_scored: bool` -- every non-MET condition has all five component scores and a computed final priority.
- Pass: Step 3.
- Fail: identify which gap is missing a score component. Re-evaluate that component.

### Step 3: Assign Gap Dimension [R]

Classify each gap into exactly one dimension:

| Condition | Dimension |
|---|---|
| Hypothesis evidence is weak or missing | EVIDENCE_STRENGTH |
| Problem pain intensity or frequency unclear | PAIN_CLARITY |
| Segment identity or access unclear | SEGMENT_CLARITY |
| Unit economics assumptions unresolved | ECONOMIC_VIABILITY |
| Value proposition clauses untested | VALUE_PROP_VALIDITY |
| Architecture conditions unmet | ARCHITECTURE_READINESS |
| Solution design inadequacy | SOLUTION_ADEQUACY |
| GTM plan feasibility uncertain | GTM_FEASIBILITY |
| Two sections contradict each other | INTERNAL_CONTRADICTION |
| Requires governor input to resolve | GOVERNOR_DECISION_REQUIRED |

**Gate:** `all_gaps_dimensioned: bool` -- every gap has exactly one dimension.
- Pass: Step 4.
- Fail: re-classify ambiguous gaps. If a gap spans two dimensions, split it into two records.

### Step 4: Rank and Select Top 3 [S]

1. Sort all gap records by Final Priority Score descending.
2. Mark the top 3 as the active gap set.
3. If more than 3 gaps exist, mark remaining as deferred (Focus Rule: max 3 active).

**Gate:** `ranked_and_capped: bool` -- gaps are strictly sorted, top 3 identified, no more than 3 active.
- Pass: Step 5.
- Fail: re-sort. If ties exist, break by blast radius weight (higher wins), then by confidence gap (higher wins).

### Step 5: Generate Recommended Action Per Gap [K-grounded]

**Grounded in:** gap dimension, evidence profile, current confidence state, deadline status.

For each active gap, determine:
- **Action Type:** RESEARCH, INTERVIEW, PRESELL, EXPERIMENT, MODEL_REVISION, ESCALATION, HALT, ARCHITECTURE_CHANGE, or SOLUTION_REDESIGN.
- **Description:** what exactly should be done.
- **Expected Output:** what evidence or state change should result.
- **Evidence Target:** which epistemic tier the action should produce (T1 or T2; never recommend T3 as a target).

Selection heuristic:

| Gap Dimension | Default Action Type |
|---|---|
| EVIDENCE_STRENGTH | RESEARCH (if T1/T2 possible) or INTERVIEW (if T3 blocker) |
| PAIN_CLARITY | INTERVIEW or EXPERIMENT |
| SEGMENT_CLARITY | RESEARCH or INTERVIEW |
| ECONOMIC_VIABILITY | MODEL_REVISION or EXPERIMENT |
| VALUE_PROP_VALIDITY | PRESELL or EXPERIMENT |
| ARCHITECTURE_READINESS | ARCHITECTURE_CHANGE or RESEARCH |
| SOLUTION_ADEQUACY | SOLUTION_REDESIGN |
| GTM_FEASIBILITY | RESEARCH or EXPERIMENT |
| INTERNAL_CONTRADICTION | HALT (force resolution) |
| GOVERNOR_DECISION_REQUIRED | ESCALATION |

**Fabrication boundary:** Do not invent specific market data, customer quotes, or quantitative evidence. Actions must describe what to gather, not assert what will be found.

**Gate:** `actions_specified: bool` -- every active gap has an action with all four fields populated. No action targets T3 as evidence output.
- Pass: output.
- Fail: revise action to target T1 or T2 evidence.

---

## Output

Produce:
1. List of scored GapRecords (all gaps, not just top 3).
2. Top-3 priority list with recommended actions.
3. Deferred gaps list (if any, with reason for deferral).
4. Any blockers detected (sections with no desired state, contradictions).

---

## Edge Cases

| Condition | Handling |
|---|---|
| Section has no desired state defined | Create gap record with dimension EVIDENCE_STRENGTH, note "desired state missing -- cannot compute gap precisely" |
| All gaps score 0 | Report: no actionable gaps. Check if register is genuinely complete or if desired states are too weak. |
| More than 10 gaps | Still score all. Top 3 active, rest deferred. Flag to gap-definer that gap count is high. |
| Tie in priority score | Break by blast radius weight (higher first), then confidence gap (higher first), then alphabetical by target. |
| Evidence for a gap is contradictory | Score evidence weakness as 3. Add note about contradiction. |

## Boundaries

**In scope:** Gap computation, scoring, ranking, action recommendation, blocker detection.

**Out of scope:** Running destruction protocol (gap-running-destruction), enforcing decision rules or setting readiness gates (gap-enforcing-decisions), writing to the register (agent handles I/O), conducting research or interviews (strategist skills).
