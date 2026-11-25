---
name: source-spec-reduce
description: >
  Post-authoring source-spec reduction — cut each absorbed section, leave a
  pointer stub, archive the source when fully dissolved. Triggers when a source
  spec's sections have been absorbed and need pointer-stub reduction (build
  specify); NOT for a greenfield spec with no source predecessor.
status: active
relevant_for: ["main-code-agent", "buddy"]
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: [task_creation]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: source-spec-reduce

## Purpose

Reduce source specs (existing specs whose content is overlaid by a
NEW spec). Per source section a 3-way triage. Prevents
double-authority between the old source spec and the new
capability / foundation spec.

Runs in the build workflow AFTER `spec-write` and BEFORE `board`.
Block on skip — source reduction is the definition-of-done of the
specify phase.

## Who runs it

Buddy as orchestrator. Triage decisions are substance (Buddy
direct). Mechanical cut + pointer-stub writing can be delegated to
`main-code-agent`.

## Input

| Parameter | Type | Required | Description |
|---|---|---|---|
| build_id | string | yes | Current build-workflow run identifier |
| parent_task | int | yes | Build task ID |
| new_specs | list[str] | yes | List of NEWLY written specs from the `spec-write` step |
| source_specs | list[str] | yes | List of existing specs overlaid by `new_specs` |

## Flow

### Step 1: section mapping per source spec

Per source spec: list every section (header `##` / `###`
structure). Per section determine:

- **Absorbed:** content is covered by a NEW spec (completely or
  with extension).
- **Drift:** content is NOT covered by any NEW spec → triage
  needed.

### Step 2: 3-way triage per drift section

| Decision | Definition | Action |
|---|---|---|
| `existing-task` | Section is absorbed by an existing active task (the plan already knows it) | Set target-task-id; the section stays in the source until the target task is done |
| `new-task` | Real plan gap — a new task is required | Trigger the `task_creation` skill, set target-task-id; the section stays in the source until the new task is done |
| `die` | Section is obsolete, covered by a NEW spec AC, or outdated | The section dies with the source. When the source is fully dissolved, archive it. |

Triage effort per build: scales with source-spec volume (rule of
thumb 30-60 min Buddy direct for medium-sized source specs).
Substance, not delegated.

### Step 3: source-spec patch per absorbed / die section

**Absorbed section** is replaced by a pointer-stub block:

```markdown
## §X.Y Section title

> **MIGRATED to `<new-spec>.md` §A.B** (per spec-lifecycle
> policy, build {build-id}).
> Authority: <new-spec>. This section remains as a pointer for
> historical cross-refs.
```

**Die section:** cut completely; no pointer stub.

### Step 4: write drift-items.yaml

Output path: `docs/build/<build-id>/drift-items.yaml`.

Schema (template:
`workflows/templates/drift-items.yaml`):

```yaml
build_id: {build-id}
parent_task: {task-id}
source_spec: {source-spec-path}
generated: YYYY-MM-DD
source_loc_pre: {LOC before reduction}
source_loc_post: {LOC after reduction}
fully_dissolved: false   # true when the source has only pointer stubs left
items:
  - section_ref: "§X.Y Section title"
    decision: existing-task | new-task | die
    target: {task-id | null}
    rationale: "{short rationale}"
```

Multiple `source_specs` per build: separate YAML files
(`drift-items-<source-name>.yaml`) OR multi-document YAML (`---`
separated).

### Step 5: source-dissolution check

If the source spec post-reduction consists of pointer stubs only
(no own authority body):
- `git mv docs/specs/<source>.md docs/specs/archive/<source>.md`.
- Pointer stub at the old path with "ARCHIVED — see
  `<new-spec>.md` as the authority replacement".
- Update the spec index / SPEC-MAP to status `archive (pointer
  stub)`.

Set `fully_dissolved: true` in `drift-items.yaml` when this
happens.

### Step 6: verification in the next step

In the subsequent `board` step, `spec_board` checks
post-reduction:
- Pointer stubs reference existing targets.
- Drift items are 3-way-decided + plausible.
- No section double-authority (the source carries only pointer
  stubs + drift).
- Cross-refs in other specs aren't degraded (grep check).

## Contract

### INPUT
- **Required:** `build_id`, `parent_task`, `new_specs`,
  `source_specs`.
- **Context:** the spec-write step must be done (the NEW specs
  exist).

### OUTPUT
**DELIVERS:**
- Source-spec patches (pointer stubs + section removals).
- `docs/build/<build-id>/drift-items.yaml` (required artifact).
- New tasks via `task_creation` (on `decision=new-task`).
- Source archival when the end state is reached.

**DOES NOT DELIVER:**
- Spec authoring (`spec_authoring`).
- Cross-spec conflict resolution
  (`cross_spec_consistency_check`, pre-specify).
- Code implementation.

**ENABLES:**
- Single source-of-truth per concept (source section absorbed
  into the NEW spec).
- Drift-items authority (plan gaps become mechanically visible).
- Source dissolution across sequential builds.

### DONE
- Per absorbed / die section: source spec patched.
- `drift-items.yaml` written (every drift section with a
  decision).
- On `decision=new-task`: new tasks created.
- On a fully dissolved source: archived + pointer stub at the
  old path.

### FAIL
- **Retry:** re-run after correcting the section mapping (step
  1).
- **Escalate:** a source section doesn't fit any of the three
  triage classes → escalate to the user.
- **Abort:** drift-items volume > 30 → STOP, build scope is too
  big, sub-build decomposition required.

## Skip eligibility

Skip eligible when the current build doesn't overlay any source
specs (greenfield NEW spec without an existing predecessor).
Provide the skip reason as a one-sentence `--skip` argument.

## Anti-patterns

- **NOT** cut a section without a pointer stub (not even on
  "absorbed"). INSTEAD set the pointer stub for cross-ref
  stability.
- **NOT** skip triage ("decide later"). INSTEAD every drift
  section gets a decision in this step. Because: the
  lifecycle policy is mechanical only when triage is a
  blocking obligation.
- **NOT** archive the source without the step-5 check
  (fully dissolved). INSTEAD the source stays active as long
  as even one authority section exists. Because: premature
  archival points nowhere.
- **NOT** write drift items as Markdown. INSTEAD YAML format
  per the schema template. Because: machine readable for the
  plan-engine validation phase 2.

## Enforcement

- `workflows/runbooks/build/workflow.yaml` step
  `source-spec-reduce` — post-spec-write, pre-board, on_fail:
  block.
- `task_creation` skill — delegated on `decision=new-task`.
- The consumer project defines its own spec-lifecycle-policy
  authority (e.g. an ADR) for skip-eligibility conditions and
  archival conventions.
