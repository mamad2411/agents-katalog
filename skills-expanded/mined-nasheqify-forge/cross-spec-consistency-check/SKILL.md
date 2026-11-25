---
name: cross-spec-consistency-check
description: >
  Pre-authoring conflict detection across the specs in a build's source-grounding
  set — API naming drift, double authority, schema drift, authority overlap.
  Triggers when a build run has 2+ source specs to check before authoring (build
  specify); NOT for a greenfield spec with no source set.
status: active
relevant_for: ["main-code-agent", "buddy"]
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: cross-spec-consistency-check

## Purpose

Conflict detection between specs in the source-grounding set, **before** a NEW spec is written that builds on inconsistent predecessors. Prevents double authority and drift inheritance from leaking into the NEW spec output.

Executed in the build workflow BEFORE the `interview` step. Block on high-severity conflicts.

## Who executes

Buddy as orchestrator. Optionally a `board-impact` sub-agent for cross-spec diff. Triage decisions are substance, not delegated.

## Input

| Parameter | Type | Required | Description |
|---|---|---|---|
| build_id | string | yes | Current build-workflow run identifier |
| parent_task | int | yes | Build task ID |
| source_grounding_set | list[str] | yes | List of spec paths read as input for the current authoring |

**Source-grounding set:** the project's own spec-consumed list for the current build scope, plus any existing outputs from earlier build iterations that may compete with the current build in substance. Concrete sources are a consumer convention (e.g., spec-map index, feature map, plan authority).

## Procedure

### Step 1: Assemble the source-grounding set

Buddy + author identify which spec files are relevant as input for the current build. Typical sources:
- Spec index with consumed/consumer columns
- Feature or capability map
- Outputs of earlier build iterations (NEW specs that already exist)
- Architecture authority stub if present

### Step 2: Conflict identification

Per spec pair (i, j) in the source-grounding set: identify the diff. Four pattern classes:

- **API naming drift:** the same identifier in two specs with a different signature or semantics
- **Concept double authority:** the same concept in two specs with different descriptions
- **Schema drift:** the same data structure in two specs with different definitions
- **Authority overlap:** both specs declare authority for the same aspect

Methods: Buddy direct, manual, or sub-agent delegation. Script-based pattern detection (same identifier via grep + AST comparison) is a phase-2 improvement, not mandatory.

### Step 3: Write drift-list-cross.md

Output path: `docs/build/<build-id>/drift-list-cross.md`

Format:

```markdown
# Cross-Spec-Drift-List

**Build:** {build-id}
**Generated:** YYYY-MM-DD
**Source-Grounding-Set:** [list of specs]
**Total Conflicts:** {N}

## Conflicts

### CSC-{build-id}-001
- **Specs involved:** {spec-a}.md §X.Y ↔ {spec-b}.md §A.B
- **Description:** {conflict description}
- **Severity:** high | medium | low
- **Resolution-Path:** patched-existing-spec | decision-in-new-spec | council-triggered
- **Resolved-by:** {commit-sha or PENDING}
- **Resolution-Note:** {rationale}
```

### Step 4: Severity triage

| Severity | Definition | Block behaviour |
|---|---|---|
| **high** | Conflict blocks authoring (the author cannot decide which authority applies) | Block — must be resolved before authoring |
| **medium** | Conflict resolvable in the NEW spec (decision lock there), source patch optional | Warn |
| **low** | Naming drift, cosmetic | Warn |

### Step 5: Resolution

Per high-severity conflict, three resolution paths:
- (a) **patched-existing-spec:** the existing spec is patched immediately (co-evolution)
- (b) **decision-in-new-spec:** the NEW spec declares explicitly which authority it overrides (§Authority-Conflicts block in the spec body)
- (c) **council-triggered:** Council with 3+ members, ADR output

Severity medium/low: resolution during the subsequent authoring step or post-Specify.

## Contract

### INPUT
- **Required:** build_id, parent_task, source_grounding_set
- **Context:** source-grounding-set files (read-only)

### OUTPUT
**DELIVERS:**
- `docs/build/<build-id>/drift-list-cross.md`
- Resolution commits for high severity (before the next step)

**DOES NOT DELIVER:**
- Spec authoring (that is `spec_authoring`)
- Source-spec reduction (that is `source_spec_reduce`)
- ADR writing (manual when council-triggered)

**ENABLES:**
- Clear authority layers during spec authoring
- Cross-build-iteration consistency (sequential builds build on each other without drift inheritance)

### DONE
- drift-list-cross.md written
- High-severity conflicts resolved
- Medium/low documented with resolution path

### FAIL
- **Retry:** after an existing-spec patch or council trigger
- **Escalate:** conflict outside the four pattern classes -> user escalation
- **Abort:** > 5 high-severity conflicts -> stop, mandatory substance audit (signal of a structural problem)

## Skip eligibility

Skip-eligible when the current build-workflow run has no source-grounding set (greenfield spec without an existing spec predecessor or without intersecting specs from earlier builds). Skip reason as a one-sentence note in the `--skip` invocation.

## Anti-patterns

- **DO NOT** check all existing specs in the repo against each other (combinatorial explosion). INSTEAD: only the source-grounding set of the current build. Why: conflicts outside the current scope are not build-relevant.
- **DO NOT** write without severity triage. INSTEAD: an explicit classification per conflict. Why: without severity, the file is useless for a block/warn decision.
- **DO NOT** misuse this as a pre-project audit for all specs. INSTEAD: incremental per build. Why: bulk audit waves have historically failed under load.

## Enforcement

- `workflows/runbooks/build/workflow.yaml` step `cross-spec-consistency-check` — pre-interview, on_fail: block
- The consumer project defines its own spec-lifecycle policy authority (e.g., ADR) for when skip eligibility applies and when source-reduction end state is reached. This skill is the generic mechanism; project-specific triggers are a consumer convention.
