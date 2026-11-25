---
name: task-creation
description: >
  Create a new, self-contained task (acceptance criteria + duplicate /
  dependency check). Use when actionable work needs tracking as a new
  task — at intake, as a fix-task, or from spec decomposition;
  reach for it instead of free-flow-adding a task by hand. NOT for editing
  an existing task (use task_status_update) or a fix you can just do now.
status: active
invocation:
  primary: user-facing
  secondary: [workflow-step]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: task-creation

Structured, high-quality task creation. Self-contained tasks with
clear ACs, a derived `intent_chain`, and no duplicates. Task quality
sets the upper bound on downstream work quality.

Triggers: intake gate ACTIONABLE, root-cause-fix step 4, user
"create a task for X", spec decomposition.

## Input

- **problem:** what is broken / missing / wanted? (raw)
- **context** (optional): defect info, incident, conversation.
- **source** (optional): `intake` | `root-cause-fix` | `user` |
  `decomposition`.

## The 5 steps

### 1. Duplicate, bundling + dependency check (MUST)

Single scan over `docs/tasks/` and the sibling tasks the same
request would file (a council's or plan's step list):

**(a) Duplicate + bundling check** — same goal (semantic, not title
match), subset of existing, or makes existing obsolete?
- Duplicate → no new task, reference the existing one.
- Subset → fold the problem into the existing task as an AC /
  comment.
- Obsolescence-maker → supersede the existing one (via
  `task_status_update`), the new task is the successor.
- No duplicate → do the new task and a pending / in_progress or
  sibling task serve one deliverable? They do when one result decides
  the other's shape, one is the other's acceptance (a probe, a spike,
  a cold run), they change the same files, or they need the same
  install window.
  - One deliverable, and they differ in owner (who builds, or who
    decides if the rest happens at all), timing, authorization
    or safety floor → keep them apart and record that reason in the
    MD body; (b) and (c) apply between them.
  - One deliverable otherwise → fold them into one task: a part whose
    result decides the rest becomes a step whose failure stops the
    task before the rest, an acceptance part becomes an AC, the
    parts' order becomes the task's step order, and (b) runs for the
    receiving task. An existing task takes the new part as steps or
    ACs. Detail: `REFERENCE.md` §1a.
  - Not one deliverable → continue.

**(b) Cross-task dependency check (required, not optional)** — for
every pending / in_progress task that stays separate after (a), is
there a logical dependency in **either** direction?

- New task needs result of existing → new task gets
  `blocked_by: [NNN]`.
- Existing task needs result of new → **edit the existing YAML**
  and add the new task ID to its `blocked_by`. Mandatory.

Yes on any → record; document rationale in the MD body as a
`## Dependency: blocked_by N` block (why, direction, order). No on
all → `blocked_by: []`.

Trigger questions + worked example: `REFERENCE.md`.

**(c) Split-gap check (MUST when this task comes from a split).** When
a capability is split and the gate / proof / validation half moves to a
sibling task, the other half ships an ungated surface. In the SAME
change as the split:
- add the gate sibling to `blocked_by` of **every** producer and
  consumer task of the ungated half (not only of the ungated task
  itself) — list them from the spec's producer / consumer surface;
- give the ungated half an AC that it **fails closed** at its edge
  (rejects or downgrades the privileged value) until the gate sibling
  lands.
The same applies when a council or verdict rules a split: the ruling
names the gate half, its producers / consumers and the fail-closed edge.

**Lifecycle symmetry:** closure of the `blocked_by` graph is
`task_status_update` Step 4 (`REFERENCE.md` §1b).

### 1.5. Value floor (MUST)

What operational impact does NOT doing this have?

- **Nothing breaks** — no contract violation, no one blocked, no
  behaviour change → `accept`, no task. Optional record where
  natural (forge-feed for lessons, ADR for decision-drivers).
- **Cosmetic only** — SoT-link tidiness, placeholder fills, "nice
  to have" docs → `accept`.
- **Real impact** — defect, blocker, contract gap, user-visible
  bug, measurable downstream cost → continue to step 2.

Applies regardless of trigger. Symmetric with `code_review_board`
LOW-hard-floor.

**User-override:** if trigger=user AND the floor says `accept`,
surface the outcome before proceeding —
*"Value-floor says accept (Grund X) — really file?"*. Explicit
yes overrides; otherwise: no task.

### 1.6. Claim verification (MUST when trigger formulations present)

If the task body uses any of: `supersedes`, `reuses existing`,
`already implemented`, `wraps existing`, `delivered in Task`,
`existing-code verifications confirm` — each claim MUST be paired
with a `C-VERIFY` block (claim text + verbatim `grep -rn` command
+ verbatim output + `CONFIRMED|FALSIFIED` disposition). The canonical
trigger set — incl. the spec-citation and cross-producer
dedup/collision/reconcile classes — lives in
`agents/code-architect-lens.md` §Claim-Verifications; a task that
locks a reconcile/dedup premise triggers the cross-producer class
(verify producer key-assignment co-location, not mere existence).
`[DISCIPLINE]` — this is an authoring rule applied by the agent, NOT
a hook (why: `REFERENCE.md` §Claim verification).

### 1.7. Critical-path placement (MUST)

`milestone` + `priority` encode **path-position**, not topic-fit.
Before writing (§4), read `plan_engine.py --boot` (critical path +
milestone gates + next-actions) and place the task against the path,
not by subject-matter resemblance:

- **Milestone by dependency, not topic.** Pick the `milestone` where
  the task's dependencies actually sit, not the topically-nearest
  one. `--critical-path` shows where the target runs and which
  milestone gates it.
- **On-path vs off-path.** If the task is NOT on the critical path to
  the target, say so in the MD body. Off-path work defaults
  `priority` **away from `high`** unless a *named active consumer*
  demands it (same L→G→C floor as §1.5, applied to placement, not
  filing).
- **Priority semantics.** Name which the `priority:` field means:
  critical-path-priority (gates the path) vs user-value-priority
  (valuable but off-path). A high-user-value off-path task is not
  `priority: high`.
- **Forward blast radius.** When the new task blocks or unblocks
  existing work, `plan_engine.py --after <id>` shows what unblocks
  downstream — set `blocked_by` edges deliberately from that, not
  pairwise guesses alone.

The result feeds §4: `milestone` + `priority` justified against
path-position, not topic. Placing the task into an agreed programme ahead of its
next task is an order change: it needs the user's confirmation
(`agents/buddy/coordinating-sessions.md` §Programme order).

### 2. Triage (MUST)

Fix immediately or create a task? Criteria: effort, reversibility,
dependencies, context, interruption. All "fix immediately" criteria
met → light plan, no task; **steps 3-5 are skipped**. Otherwise →
continue. Triage table: `REFERENCE.md`.

### 3. Derive the intent_chain (MUST)

Derive from the active context. Required on delegation; optional in
direct user conversation. Format + rules (build + life variants):
`framework/intent-tree.md` §intent_chain.

### 4. Write the task file (MUST)

Format: `docs/tasks/<NNN>.yaml` + `<NNN>.md`. Schema SoT:
`framework/task-schema.yaml`. Body SoT: `framework/task-format.md`.

**ID selection (MUST):** `NNN` = highest numeric basename across **both**
`docs/tasks/*.yaml` AND `docs/tasks/archive/*.yaml`, + 1. Archived IDs are
retired, never recycled — scanning only the top-level silently collides
with an archived task and breaks the WORM archive move at close. §5
`--validate` flags a live↔archive collision (`ID_REUSED_FROM_ARCHIVE`)
as the safety net.

YAML field names + value vocab live in the schema, not here. New
tasks are open → MUST carry `effort` (`S|M|L|XL`) and `priority`
(`high|medium|low`) alongside the always-required fields (`id`,
`title`, `status`, `milestone`, `blocked_by`, `created`, `updated`).

**`milestone`** MUST be a key from `docs/plan.yaml` milestones.
Pick the milestone that fits the task **inhaltlich** (read the
content, don't default to the last-used one). If no existing
milestone fits, read and follow `REFERENCE.md` §No milestone fits
before continuing.

**`spec_ref`** required when the task implements an existing spec
(`null` only when no spec exists).

**Dependency-spike check:** new external dependency with >1
integration point → it gets a spike (PoC / eval). When the spike
needs its own decision or authorization (the user decides from its
result if the dependency is adopted at all, or it needs a
permission the build does not), it is a
separate spike task, `blocked_by` ahead of the build. Otherwise the
spike is the task's first step, with a stop point before the build:
a failed spike stops the task and reports instead of building.
Detail: `REFERENCE.md`.

**MD content quality** — problem (why understandable?), intent
(goal not path?), description (self-contained?), priority
(plausible?), area (fits?). FAIL criteria: `REFERENCE.md`.

**Optional but always check:** `context_manifest`,
`workflow_template` (decision / research). Detail: `REFERENCE.md`.

**`## Not yet`** block required — empty is invalid. No exclusion
from the user → ask actively.

### 5. Validation (MUST)

`python3 $FRAMEWORK_DIR/scripts/plan_engine.py --validate`. The new
task must appear without an ERROR (milestone exists in plan.yaml,
blocked_by refs existing tasks, no cycle, schema conformance).

**FAIL →** correct the task file (milestone vs `docs/plan.yaml`,
blocked_by IDs vs `docs/tasks/`) and re-validate. Repeated FAIL →
delete the task files; escalate to the user (NNN is reused).

**Field vocabulary (schema-aware — MUST).** Draw field names from
`framework/task-schema.yaml`. On a `SCHEMA_UNKNOWN_FIELD` WARN, read
and follow `REFERENCE.md` §Field vocabulary before writing on.

## Output

```
Task creation: [NNN] [title]
Duplicate check: no duplicate / duplicate of [NNN] / subset of [NNN]
Bundling: none / folded [NNN|sibling] in / kept apart from [NNN|sibling] — [owner|timing|authorization|safety floor]
Triage: fix immediately / create task — [rationale]
milestone: [key from plan.yaml]
File: docs/tasks/<NNN>.yaml + <NNN>.md
Validate: plan_engine --validate PASS
```

## Anti-patterns

- **NOT** skip the duplicate check ("my task is certainly new") —
  always scan; duplicates arise from slightly different wording.
- **NOT** set `blocked_by: []` without running step 1b
  substantively — parallel tasks with implicit dependency produce
  rework (B documents while A changes the state, B redoes).
- **NOT** skip triage and always create a task — backlog bloat from
  5-minute tasks that could be done directly.
- **NOT** accept an empty `## Not yet` block — ask actively; scope
  drift across the lifecycle when boundaries are unstated.
- **NOT** `spec_ref: null` on implementing tasks — assign a spec
  or hold the task. Breaks `consistency_check` spec coverage
  (exception: REFERENCE_SPECS).
- **NOT** fill required fields with "see above" / "current
  conversation" — tasks are picked up later without session
  context.
- **NOT** embed build-workflow route decisions in task notes
  (`--route sub-build`) — route-determination at workflow-start
  time per `workflows/runbooks/build/WORKFLOW.md` based on current
  task properties. Stale hints in notes anchor toward outdated
  paths.
