---
name: gap-enforcing-decisions
description: >
  Applies the 10 decision rules, reclassifies confidence and support
  states, sets readiness gates, and generates execution queue entries
  and governor escalations. Use when gap computation and destruction
  are complete and decisions must be enforced.
license: Complete terms in LICENSE.txt
serves: gap-definer
domain: decision-enforcement
affects: register-state-and-readiness
depends-on: none
produces: state-changes-and-queue
---

# Decision Enforcement

Apply the mandatory decision rules to the gap ledger and destruction
outcomes. Produce state changes, readiness gate values, execution
queue entries, and governor escalations.

Every rule must be evaluated. No rule may be skipped. Every block
must have explicit rationale.

---

## Process

### Step 1: Collect Inputs [S]

Gather from prior skill outputs and register state:

1. Gap Ledger (scored and ranked gap records from gap-computing-ledger).
2. Destruction Log (outcomes from gap-running-destruction).
3. Current confidence states for all hypotheses.
4. Current support states for all proposals.
5. Decision deadlines and their statuses.
6. Active blockers.
7. Any governor responses from execution/queue/.

**Gate:** `inputs_collected: bool` -- gap ledger and destruction log both available. If either is missing, halt: "Cannot enforce decisions without gap computation and destruction pass."
- Pass: Step 2.
- Fail: halt. Report which input is missing.

### Step 2: Apply Priority Rule [S]

**Rule:** Always work on the gap with the highest (gap score x blast radius).

1. Read the ranked gap list from gap-computing-ledger.
2. Confirm the #1 gap is the current work priority.
3. If the current execution queue contains tasks not aligned with the top gap, flag them.

**Gate:** `priority_confirmed: bool` -- top gap identified, priority stated.
- Pass: Step 3.
- Fail: re-rank gaps.

### Step 3: Apply Execution Rule [R]

**Rule:** A task is valid only if it reduces a top-3 open gap and produces T1 or T2 evidence.

For each proposed or active task:

| Check | Pass | Fail |
|---|---|---|
| Targets a top-3 gap? | Valid | Reject: "does not reduce a top-3 gap" |
| Produces T1 or T2 evidence? | Valid | Reject: "does not produce qualifying evidence" |

List valid tasks and rejected tasks with rejection reason.

**Gate:** `execution_filtered: bool` -- every task evaluated. Invalid tasks rejected with reason.
- Pass: Step 4.
- Fail: re-evaluate tasks against current top-3 gaps.

### Step 4: Apply Evidence Promotion Rule [R]

**Rule:** T3 evidence cannot directly produce SUPPORTED. T2 can support RESEARCHED, never SUPPORTED.

For each hypothesis currently marked or proposed for SUPPORTED:

| Evidence Profile | Allowed State |
|---|---|
| Has qualifying T1 ground-truth evidence | SUPPORTED allowed |
| Has T1/T2 from public research, no ground truth | RESEARCHED maximum |
| Only T3 or assertions | UNVALIDATED maximum |

If any hypothesis is marked SUPPORTED without qualifying T1, reclassify it.

**Gate:** `promotion_enforced: bool` -- no hypothesis exceeds the confidence ceiling allowed by its evidence.
- Pass: Step 5.
- Fail: reclassify the offending hypotheses. Document the reclassification with rationale.

### Step 5: Apply Kill Rule [R]

**Rule:** If kill condition is met or strong contradictory T1 evidence exists, mark target BROKEN.

For each hypothesis and proposal:

| Check | Outcome |
|---|---|
| Kill condition met (from kill signal audit)? | Mark BROKEN. Document why. |
| Strong contradictory T1 evidence (from destruction log)? | Mark BROKEN. Document the evidence. |
| Neither? | No change. |

**Gate:** `kill_rule_applied: bool` -- every hypothesis checked against its kill condition and contradictory evidence.
- Pass: Step 6.
- Fail: check which hypothesis was missed.

### Step 6: Apply Deadline Rule [R]

**Rule:** Exceeded deadline forces KILL, PIVOT, or COMMIT. No indefinite exploration.

For each decision deadline:

| Status | Action |
|---|---|
| OPEN, within deadline | No action |
| DUE or near due | Flag for immediate attention |
| EXCEEDED | Force disposition: KILL (mark BROKEN), PIVOT (reframe hypothesis), or COMMIT (accept current evidence and advance). Escalate to governor if disposition is a values decision. |

**Gate:** `deadlines_enforced: bool` -- no EXCEEDED deadline without forced disposition.
- Pass: Step 7.
- Fail: force disposition for each exceeded deadline.

### Step 7: Apply Contradiction Rule [R]

**Rule:** Contradictions between hypotheses, architecture, or solution block execution until resolved.

Review contradiction findings from destruction pass:

| Finding | Action |
|---|---|
| Contradiction between hypotheses | Block all execution on both hypotheses. Flag for resolution. |
| Contradiction between hypothesis and architecture | Block architecture-dependent execution. |
| Contradiction between hypothesis and solution | Block solution-dependent execution. |
| No contradictions | Note: "no blocking contradictions detected." |

**Gate:** `contradictions_resolved_or_blocked: bool` -- every contradiction either resolved or blocking execution.
- Pass: Step 8.
- Fail: identify unaddressed contradictions.

### Step 8: Apply Architecture Validity Rule [R]

**Rule:** Architecture-dependent work is blocked if required conditions are unmet.

1. Read Growth Architecture required conditions.
2. Check each condition against current register state.
3. If any required condition is unmet, block architecture-dependent execution and mark architecture support state as BLOCKED.

Examples:
- PLG without self-serve capability: blocked.
- Sales-led without identified budget owner: blocked.
- Network without collaboration mechanism: blocked.

**Gate:** `architecture_validated: bool` -- architecture conditions checked, blocks applied if needed.
- Pass: Step 9.
- Fail: check which conditions were not evaluated.

### Step 9: Apply Solution Contamination Rule [R]

**Rule:** If validation tests are solution-led rather than problem-led, invalidate the test.

Review evidence items and any proposed validation activities:

| Check | Pass | Fail |
|---|---|---|
| Test asks "does the customer have this problem?" | Valid | -- |
| Test asks "does the customer like our solution?" | Invalid | Invalidate. Require neutral re-test. |
| Test presents solution before establishing problem | Invalid | Invalidate. Require problem-first protocol. |

**Gate:** `contamination_checked: bool` -- all evidence and proposed tests evaluated for solution bias.
- Pass: Step 10.
- Fail: flag contaminated tests.

### Step 10: Apply Readiness Gate Rule [R]

**Rule:** Downstream systems may proceed only if gate predicate passes.

Evaluate sell_ready:

| Condition | Status |
|---|---|
| Problem >= RESEARCHED | {pass/fail} |
| Segment >= RESEARCHED | {pass/fail} |
| No HIGH-blast unresolved blocker | {pass/fail} |
| No architecture contradiction | {pass/fail} |

`sell_ready = true` only if ALL four conditions pass.

Evaluate scale_ready:

| Condition | Status |
|---|---|
| Problem = SUPPORTED | {pass/fail} |
| Segment = SUPPORTED | {pass/fail} |
| Unit Economics = SUPPORTED | {pass/fail} |
| Value Proposition >= RESEARCHED | {pass/fail} |
| sell_ready = true | {pass/fail} |

`scale_ready = true` only if ALL five conditions pass.

**Gate:** `readiness_evaluated: bool` -- both gates evaluated with explicit pass/fail per condition.
- Pass: Step 11.
- Fail: re-evaluate. Every condition must have a clear pass/fail.

### Step 11: Apply Focus Rule [S]

**Rule:** Maximum 3 active gaps at any time.

1. Count active gaps (those with status OPEN or IN_PROGRESS).
2. If count > 3, defer lowest-priority gaps until active count = 3.
3. Document what was deferred and why.

**Gate:** `focus_enforced: bool` -- active gap count <= 3.
- Pass: Step 12.
- Fail: defer gaps until count <= 3.

### Step 12: Generate Outputs [S]

Compile all rule application results into:

1. **State changes:** list of confidence/support state reclassifications with rationale.
2. **sell_ready / scale_ready flags** with per-condition breakdown.
3. **Execution queue:** top-3 gap-reduction tasks (valid per execution rule).
4. **Governor escalations:** for values decisions, judgment calls, and ground-truth blockers that the system cannot resolve. Each escalation must include: decision needed, decision type, why system cannot decide, options with consequences, recommendation if any, what is at stake.
5. **Blocks:** list of blocked execution paths with rationale.

**Gate:** `outputs_complete: bool` -- all five output categories populated (even if empty with "none").
- Pass: output.
- Fail: identify which output category is missing.

---

## Edge Cases

| Condition | Handling |
|---|---|
| No gaps exist (all conditions met) | sell_ready and scale_ready may both be true. Verify by checking readiness gate directly -- do not assume from gap count alone. |
| Governor escalation already exists for same decision | Do not duplicate. Reference existing escalation. Note if deadline has changed urgency. |
| Deadline exceeded but disposition is a values decision | Escalate to governor with deadline pressure noted. Do not force a values decision autonomously. |
| Kill rule and deadline rule conflict (deadline says commit, evidence says kill) | Kill rule takes precedence. Evidence contradicting the claim overrides deadline disposition. |
| All hypotheses are BROKEN | Report: strategy space appears non-viable. Escalate to governor with options: pivot problem space, pivot segment, or halt. |

## Boundaries

**In scope:** Decision rule application, confidence/support state reclassification, readiness gate evaluation, execution queue generation, governor escalation generation, block enforcement.

**Out of scope:** Computing gap scores (gap-computing-ledger), running destruction protocol (gap-running-destruction), conducting research (strategist skills), writing to the register (agent handles I/O).
