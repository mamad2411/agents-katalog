---
name: convergence-loop
description: >
  Intra-gate iteration protocol. Bounded convergence with a rising
  severity threshold and narrowing scope. Max 3 passes.
  Triggers when a fix-then-review cycle needs bounded iteration with a rising severity threshold (review verify, spec_board internal); NOT for one-shot reviews.
status: active
relevant_for: ["main-code-agent", "tester"]
invocation:
  primary: sub-skill
  secondary: [workflow-step]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: convergence-loop

## Purpose

Intra-gate iteration protocol: how a gate step iterates internally
instead of running single-pass. Bounded convergence — max 3 passes
with a rising severity threshold and narrowing scope. Not a new
gate; a mechanic inside existing gates (cascade:
`workflows/runbooks/build/WORKFLOW.md` phase Specify / Verify,
`workflows/runbooks/review/WORKFLOW.md` phase Verify).

Detail mechanics (override, fix responsibility, scope narrowing,
analysis patterns, outer-loop bound): `REFERENCE.md`.

## Who and when

Every agent with a gate step that produces findings: board agents
(every `board-*`), Buddy (L1 simulation), `tester` (design / eval
mode). The agent loads this skill in addition to the gate-specific
skill. Full path and standard path alike.

Not applicable: `tester` execution mode (the fix loop in
`main-code-agent`) · pure execution steps (writing code, running
tests).

## The protocol

### Step 0: entry (before pass 1)

1. **Intent paraphrase:** the agent formulates the artifact's
   purpose in one sentence. If paraphrase isn't possible → P1
   problem (self-containedness), immediately a BLOCKER.
2. **Scope declaration:** "full scope" on pass 1. Pass 2-3:
   `affected_scope` from the predecessor.

### Three passes, narrowing analytical lens

Iterations with progressively narrowing scope and rising severity
threshold. Each pass has a different analytical lens that can
surface different findings. They are NOT three chances at the same
work — but they are also not three rigidly-separated phases. The
narrowing lens itself is the load-bearing mechanism.

| Pass | Scope | Severity threshold | What the lens surfaces |
|------|-------|--------------------|------------------------|
| 1 | Full artifact scope | All (BLOCKER + MAJOR + MINOR) | Broad analysis, varied patterns — what's there at full scope |
| 2 | `affected_scope` from pass 1 + direct dependencies | BLOCKER + MAJOR | Second-order effects from pass-1 fixes; the narrower scope + tighter threshold can also surface things the broad lens missed at depth |
| 3 | `affected_scope` from pass 2 | BLOCKER only | Verification of pass-2 fix side-effects AND deeper findings the focused BLOCKER-only lens surfaces that pass 1/2 couldn't see |

Pass 3 surfaces NEW BLOCKERs from multiple legitimate sources:
(a) caused by pass-2 fix side-effects; (b) deeper findings only the
narrow lens reveals; (c) rare pass-1 broad-lens miss. All three are
real outcomes of the narrowing-lens mechanism.

**Mechanical stop after pass 3 (with one conditional pass-4
extension — see §Pass-3 termination).** Sub-workflow overrides
preserved (e.g. `spec-board-convergence.yaml` safety valve at pass 5, →
`REFERENCE.md`).

### Pass-3 termination (and conditional pass-4 extension)

When pass 3 surfaces BLOCKERs, the agent classifies before
terminating:

| Pass-3 result | Decision |
|---------------|----------|
| 0 BLOCKERs | **CONVERGED** (MINORs carried as annex) |
| BLOCKERs are architectural / cross-cutting / require human decision | **ESCALATE immediately** — not iteration territory |
| BLOCKERs are scoped + clearly fixable within current scope without architecture change | **Pass-4 extension** (one focused fix-verify cycle) |

**Pass-4 extension (one-shot, conditional):**
- Scope = the specific pass-3 BLOCKER(s) only
- Threshold = BLOCKER only
- Buddy fixes between pass 3 and pass 4 per normal fix scope
- Pass-4 outcomes: 0 BLOCKERs → CONVERGED; BLOCKERs remain →
  ESCALATE (no further extension)

**Hard mechanical cap at pass 4.**

### Severity definitions (L2 constrained judgment)

| Severity | Definition |
|----------|------------|
| BLOCKER | Artifact unusable as written. The next step cannot start. |
| MAJOR | Usable but with a known defect. Predictably leads to problems / follow-up questions in the next step. |
| MINOR | Improvement, not a defect. The next step's outcome doesn't change. |

Definitions anchored at the next step — mechanically checkable.
Guidance questions: `REFERENCE.md`.

### Fix scope (NON-NEGOTIABLE)

Between passes, **ALL findings** are fixed — not just those above
the current threshold. The threshold determines when CONVERGENCE
is reached, not what gets FIXED. Rationale: high-only fixes
accumulate M/L debt that compounds across passes. Exception: a
`code_review_board` FAIL fixes only the *fix-now set* per its §5
proportionality triage.

Scope narrowing (pass 2+) refers to the ANALYSIS scope of the next
pass, not to the FIX scope.

Before every fix brief from a code review's findings, each finding to be
fixed gets its cause and answer; before fix pass ≥ 2, the §Simplify-before-patch gate first asks why
the passes do not converge, then answers each blocking finding by its cause
(simplification answers a mechanism cause, one of six).

### Test scope between passes (NON-NEGOTIABLE)

Between passes, MCA fixes findings (per `Fix scope` above). Each fix
pass runs the **selected set** for its changes, plus the RED skeleton
of a cross-pass-binding test, the class witness when the fix brief
carries one (§Simplify-before-patch, `same_class: yes`), and L0 (ruff +
mypy) on touched files only. A broad run, where one is due at all, comes after the last pass,
not per fix-phase. Scope and timing: `skills/testing/run-strategy.md` §Test
selection. Failure attribution below remains binding.

### Net-new failures from the full-suite sweep

A new full-suite failure remains an unresolved verification result until
attributed. Isolation is diagnostic: isolated green cannot rule out an introduced
order-dependent regression. Compare the same relevant test sequence and environment
against the pre-change baseline, retain failure output, and reproduce the
state/order interaction sufficiently to identify whether changed production or
test code caused it. Fixture pollution or singleton state describes the mechanism,
not when it was introduced.

A change-introduced regression, including new fixture pollution, blocks completion
and must be repaired. A failure reproduced unchanged on the relevant baseline may
be recorded and routed under existing defect policy, with its evidence and limits;
do not claim it was fixed. Missing baseline, nondeterministic reproduction or changed
environment leaves attribution unresolved and cannot support "no new regressions."
Retain the obligation or escalate under existing policy.

For example, B passing alone while A→B fails after the change does not establish
historical failure. If the baseline passes A→B and the candidate fails it, the
sequence demonstrates an introduced regression. If both reproduce the same cause,
that supports a qualified historical attribution; no baseline leaves it unknown.

### Termination (general)

| Situation | Decision |
|-----------|----------|
| Mechanism with an owner-approved exit criterion (before every other row, §Pass-3 termination's too) | **CONVERGED** only when every part holds (`derive-and-exit.md`); zero findings above the threshold is not enough |
| Pass N (pass 1 included) has 0 findings above the threshold | **CONVERGED** — proceed to the next gate |
| Finding requires an architecture decision | **ESCALATE immediately** — not an iteration problem (any pass) |
| Pass 3 BLOCKERs | see §Pass-3 termination (and conditional pass-4 extension) |
| Pass 4 (extension) BLOCKERs remain | **ESCALATE** — no further extension |

ESCALATE signals "this needs architect / human judgment, not more
agent iteration".

Pass counts and the pass-4 extension count per mechanism across review
owners, workflows and tasks (`simplify-before-patch.md` §Simplify-before-patch gate, Counting). Apply `agents/buddy/delegation.md` §Delegation
hygiene (cumulative effort) before any extension.

### Simplify-before-patch gate (before every fix pass ≥ 2, MUST)

For any code-review fix brief (pass 1 included) and when the implementer pushes back or marks a finding unclear, read
`skills/convergence_loop/cause-before-answer.md` (causes, rulings, spec gaps and re-deriving). At the re-review limit
read `skills/convergence_loop/at-the-cap.md` (cause and ruling for each open finding).

After two failed reviews at the same role transition, ask which interface governs it and who owns it before the
next disposition (owner: skills/convergence_loop/simplify-before-patch.md §Record).

Before a fix brief from pass 2 on, an owner change or an extension, read
`skills/convergence_loop/simplify-before-patch.md` (counting, inventory, model-first record, decision and witness).
When the gate answers with a drill or records `same_class: yes`, and on a mechanism with an owner-approved exit
criterion, read `skills/convergence_loop/derive-and-exit.md`.

## State format between passes

```
## Convergence Pass {N} — {gate name}
### Scope: {pass 1: full scope; pass 2+: affected_scope from N-1}
### Findings
- F{N}.{X}: [{BLOCKER|MAJOR|MINOR}] {description}
  Root cause: {...} | Affected scope: {...}
### Below-threshold: {findings under the threshold — annex}
### Termination: CONTINUE → pass {N+1} | CONVERGED | ESCALATE
```

CONVERGED: annex with below-threshold findings from every pass.
ESCALATE: concrete reason + question ("BLOCKER F3.1 needs a
decision: {...}"), not "there are problems".

## Integration into gate steps

The gate skill = **lens** (what is being checked). The convergence
loop = **iteration** (how often, which scope, when to stop).
Agents load it in addition to their gate skill: step 0 → pass 1
with varied patterns → fixes → pass 2 `affected_scope` → fixes →
pass 3 → CONVERGED / ESCALATE. Varied patterns per gate type +
fix responsibility: `REFERENCE.md`.

## Boundary

- **Not** the fix loop in `main-code-agent` · **not** the gate
  cascade itself (the cascade decides which gates run).
- **Not** the review protocol (replaced by Spec Board).
- **Not** alternatives evaluation — divergent thinking belongs in
  council / solution-expert.
- **Not** execution steps (writing code, running tests) — only
  analytical / validating gates.

## Anti-patterns

- **NOT** fix only findings above the threshold between passes.
  **INSTEAD** fix ALL findings — the threshold determines
  convergence, not fix scope. Because: MINOR accumulation compounds
  across passes.
- **NOT** treat pass 2 / 3 as fix verification. **INSTEAD** every
  pass is a fresh analysis. Because: anchoring bias — tainted
  passes miss high findings a fresh look catches.
- **NOT** iterate over architecture findings. **INSTEAD**
  ESCALATE immediately. Because: architecture is not an
  iteration problem.
- **NOT** set severity abstractly. **INSTEAD** anchor it at the
  next step ("can the next step proceed?"). Because: only that
  is mechanically checkable.
- **NOT** force CONVERGED at pass 3 to avoid ESCALATE or skip the
  pass-4 extension. **INSTEAD** classify pass-3 BLOCKERs honestly:
  architectural → ESCALATE; scoped + fixable → pass-4 extension;
  none → CONVERGED. Because: deadline framing produces premature
  CONVERGED + severity-downgrade.
