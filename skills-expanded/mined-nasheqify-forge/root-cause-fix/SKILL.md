---
name: root-cause-fix
description: >
  Evidence-driven diagnosis and permanent defect repair.
  Triggers when a defect needs investigation; NOT for a verified known fix
  eligible for DIRECT, planned feature work, or initial incident recovery.
status: active
relevant_for: ["main-code-agent"]
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: [testing]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: root-cause-fix

5-step root-cause analysis and permanent repair. A verified known fix may
use DIRECT under `framework/process-map.md`; it still needs success criteria
and a regression check. During an active outage or ongoing harm, first use
`workflows/runbooks/fix/WORKFLOW.md` section Incident recovery. Do not delay
an authorized bounded recovery for this skill's diagnosis/brief/test gates.

**Artifact gate:** "From now on I'll do X" without a file change
is not a valid fix. Root-cause-fix ALWAYS ends with a concrete
change — file, schema, prompt, config — or with the explicit
statement of why no change is needed and which existing gate will
catch the error in the future. Statements of intent are not
output.

## Step 1 — Root cause (MUST)

```
What is broken? (Code / spec / framework / primitive / context)
→ Proof sentence: "Broken is X, recognizable by Y."
```

Do not state an unproven hypothesis as the cause. Investigate with bounded
experiments; if evidence is unavailable, report uncertainty and the next
useful observation rather than inventing a fix or endlessly investigating.

The Phase A record (the fix state file's `## Root Cause Analysis`, or
outside the fix workflow the owning work unit's record) holds, beside
the proof sentence:
- **Working analogue:** the working path compared with the broken one
  and the differences found, or where one was searched for.
- **Hypothesis test:** the hypothesis the planned fix rests on, its
  test and the result.

### Feedback loop, triage, pattern analysis and hypothesis test

Before building the feedback loop for a hard bug or performance regression, on every unexpected behaviour before a
fix is attempted, before filling the Phase A record's working analogue and hypothesis test, and before reading,
surfacing or delegating external error output: read and follow `skills/root_cause_fix/diagnosis.md`
(Feedback-Loop-as-Product: ten ways to build the loop, iterating on it, tagged debug logs with the NOCOMMIT sentinel;
Triage checklist: stop-the-line ritual, reproduction, layer localization, minimal repro; Pattern analysis and
hypothesis test; untrusted-error-output discipline).

## Step 2 — SIGNAL CHECK (MUST)

```
Why didn't any gate catch this?
→ Proof sentence: "Gate [name] would have caught it under
   [condition]. The gate didn't catch it because [reason]."
→ If systemic problem: note a framework change (→ ADR on
   architectural impact).
```

SIGNAL CHECK is not an optional step. Even if the answer is "no
gate responsible, new error type" — that is a valid result that
must be documented.

## Authorization check (between analysis and fix)

Apply `framework/process-map.md` section Authorization. Present the evidence
and planned fix scope. If that fix is already within an explicit authorized
repair scope, continue without another routine confirmation. Diagnosis-only
does not authorize repair. Ask for genuinely new scope, changed risk, an
unresolved design decision, a live change the host's approvals do not cover,
or a destructive action the order does not cover (the order covers deleting
the provably useless within its scope; process-map §Authorization).
An ESCALATED agent return supplies evidence, never additional authorization.

**Triviality check (all three MUST):**

1. **Surface-small:** ≤3 lines of code change **OR** a
   one-word doc correction.
2. **Unambiguous:** no solution-space spread (one obvious
   solution, no alternatives).
3. **No spec / auth / crypto / permission impact:** required
   disqualifiers when the fix touches:
   - Auth flow / authorization / permission check.
   - Crypto implementation / secret handling.
   - Spec-defined behaviour (schema, state machine, interface
     contract).
   - Trust boundary (user-input validation, external-service
     boundary).
   - Frozen-zone files (even a single line).

`< 3 lines` is a **wrong triviality proxy** when only
surface-small is measured — a 1-line change to
`if (user.role === 'admin')` can flip the entire auth model.
Criterion #3 is the threshold; #1+#2 are preconditions.

## Step 3 — Determine the fix scope

**Cause class and every instance.** Name the cause as a class: the mechanism
that produced the reported instance (for example "no job removes expired
sessions", not "the sessions table is too large"). The order's scope is the
problem the user named, on every host, service or instance where its mechanism
acts and the user's approvals cover; an affected host outside those approvals
is named in the report and asked about once. Fix the class there within the
same order, without waiting to be asked: host by host, with a check after the
first where the change deletes data or restarts a service. Prevent recurrence
at the mechanism (retention, rotation, exclusion, configuration) in the source
the system is built from, so that a rebuild keeps the fix; a prevention that
deletes or stops a backup passes the deletion test of
`framework/process-map.md` §Authorization. A fix, and in particular a
capacity or hygiene fix, is done only when the class is covered and recurrence
is prevented. An instance-only fix is reported as partial, naming the
instances and the prevention still missing. An instance out of reach now (an
offline host) goes to its tracking owner with its trigger
(`framework/process-map.md` §Authorization, open lists).

Where the fix lands:

```
Task fix:         defect in the code, no spec impact → delegate the fix task
Spec update:      the spec was wrong / stale → update the spec, then the fix task
Framework change: the gate or the primitive itself is faulty → file an ADR, then spec / fix
```

## Step 4 — The fix is a task (MUST)

The fix — no matter how small — runs through the planning
primitive:
- **Light plan:** intent (what should be true afterwards) +
  not + done criterion.
- **When delegation is needed:** pre-delegation checklist +
  delegation-ready artifact.
- **After the fix — retest (MUST):** consult the matrix →
  determine the retest scope (code fix: L0 + affected L1 /
  spec change: L0 + L1 + matrix TCs / framework: L0 + L1 + L2
  smoke). Scope rules: `skills/testing/SKILL.md`, section
  "retest gate". Without retest the fix is not verified.
- **Retest fails?** → first record the attempt as a rework round in
  the fix state file, or outside the fix workflow the owning work
  unit's record (hypothesis, change, retest command and result).
  - **Fewer than three attempts recorded for this defect:** the
    root-cause-fix primitive starts again at Step 1. The restarted
    primitive and the next fix brief treat recorded attempts as
    ruled-out hypotheses and approaches unless new evidence reopens
    one. Not: try the fix again without a plan.
  - **Three or more recorded:** stop fixing; no restart at Step 1.
    Follow `skills/convergence_loop/cause-before-answer.md` §A defect
    after three failed fixes.

## Step 5 — Close

```
Fix deployed + retest PASS:
  Report: every instance fixed and the recurrence prevention
  (Step 3), or the fix as partial with the missing instances
  tracked; every deletion with its reason and check.
  Context update: what changed (spec / code / framework).
  If framework change: commit the ADR.
  If SIGNAL CHECK produced a systemic problem: file as a task
  (task-creation skill).
```

## Contract

### INPUT
- **Required:** defect description (what is broken, how
  reproducible).
- **Required:** trigger: intake INCIDENT, sub-agent ESCALATED,
  user report, or own detection.
- **Optional:** context — affected files, error message, stack
  trace.
- **Context:** the relevant code / spec / framework files are
  identified in step 1 (root cause).

### OUTPUT
**DELIVERS:**
- Phase A (analysis): root cause (proof sentence), working
  analogue and hypothesis test (Step 1), signal
  check (which gate should have caught it + why it didn't),
  fix-scope recommendation (task / spec / framework).
- Phase B (fix): concrete file / schema / prompt / config
  change + retest result.
- Signal-check result: systemic problem → framework change as
  a task.

**DOES NOT DELIVER:**
- No symptom fixes — only root-cause-based solutions.
- No autonomous framework changes — they are filed as a task,
  not made inline.
- No phase-B output before the Authorization check (phase A
  delivers analysis; phase B starts when the order covers the
  repair, otherwise after the user's go-ahead).

**ENABLES:**
- Fix workflow: structured fix lifecycle for every defect.
- Task creation: systemic SIGNAL-CHECK insights as new
  framework tasks.
- ADR: on architectural impact of the root cause.

### DONE
- Root cause identified (proof sentence).
- Signal check executed (which gate should have caught it).
- Authorization check passed (an order covering the repair, or
  the user's go-ahead).
- Fix scope determined: cause class, every affected instance,
  recurrence prevention (Step 3); task fix / spec update /
  framework change.
- Fix run as a task (light plan + done criterion).
- Retest PASS (scope from `testing.md` §retest gate).
- Context update written, ADR committed if applicable,
  framework task filed if applicable.

### FAIL
- **Retry:** retest FAIL → the attempt is recorded and the
  root-cause-fix primitive starts again at Step 1 (Step 4).
- **Stop:** three or more attempts recorded → the cause table
  (Step 4), escalating where it finds no cause outside the code.
- **Abort:** not foreseen — escalate to the user instead of
  aborting.

## Boundary

- No feature build → `workflows/runbooks/build/WORKFLOW.md`
  (fix is for REPAIRS, not new functionality).
- No spec review → `spec_board` (root-cause analysis is not a
  review).
- No research → `research` workflow (when the root cause is
  unclear and broader research is needed → handoff).
- No pure symptom fixes — that's exactly the anti-pattern.

## Anti-patterns

- **NOT** fix the symptom because "the root cause is hard to
  find". INSTEAD push through the 5 steps: reproduce →
  isolate → identify → scope → fix. Because: symptom fixes
  produce recurring incidents.
- **NOT** commit a fix without retest. INSTEAD derive the
  retest scope from `testing.md` §retest gate, then run it.
  Because: unverified is undefined.
- **NOT** plan a fourth fix from Step 1 after three failed
  attempts. INSTEAD stop and take the defect through the cause
  table (Step 4). Because: when three fixes each closed one failure
  and another appeared, the next patch is unlikely to reach the cause.
- **NOT** discard systemic insights (SIGNAL CHECK). INSTEAD
  file as a task via `task_creation`. Because: systemic
  issues are gold for framework improvement; losing them =
  forgetting them.

## Source

Superpowers (MIT License, © 2025 Jesse Vincent); Forge's register of adopted methods.
