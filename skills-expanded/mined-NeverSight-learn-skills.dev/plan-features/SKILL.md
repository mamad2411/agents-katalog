---
name: plan-features
description: Turn an idea or existing project plan into interactive feature designs, a concise human roadmap, project documentation architecture, and an executable Beads dependency graph.
metadata:
  version: "0.5.9"
allowed-tools: Read Glob Grep Edit Write Bash AskUserQuestion
---

# Purpose

Use this skill to take project intent from discussion to durable design and ordered work. Beads owns live feature/task
state. `design.md` owns detailed feature intent. `planned-features.md` remains a concise human roadmap. Resolve
`<core-dir>` as the installed `../dstack-core` skill directory so feature selection uses its deterministic resolver.

## Inputs

Use the user's request together with:

- `bd prime`, current feature roots, ready work, and blocked work;
- `docs/src/SUMMARY.md` and the pages it links;
- `docs/src/planned-features.md`;
- existing feature designs and implemented-feature records;
- current code, tests, configuration, and architecture evidence when refining an existing project.

## Outputs

Create or update:

- Beads feature roots, lifecycle steps, implementation children, and dependencies;
- `docs/src/planned-features.md`;
- `docs/src/features/<slug>/design.md` for near-term or sufficiently understood features;
- project-specific reader-facing pages needed to establish durable direction;
- `docs/src/SUMMARY.md` when navigation changes.

## Execution

## 1. Load Project State

Run:

```bash
bd prime
bd list --all --type epic --label workflow:feature --json --limit 0
bd ready --json
bd blocked --json
```

Read the documentation table of contents before selecting detailed pages. Read only the project-specific pages relevant
to the planning scope, plus relevant completed-feature records and designs.

## 2. Normalize Planning Input

When planning input includes a transcript, meeting notes, or prior agent session, process decisions chronologically:

- treat later explicit user decisions as authoritative over earlier proposals;
- mark superseded names, payloads, dependencies, and constraints as historical rather than carrying them forward;
- distinguish repository observations from durable product intent;
- copy each durable decision into every affected `design.md`, not only the roadmap;
- record unresolved contradictions as questions instead of selecting a convenient interpretation.

## 3. Run the Design Question Loop

Ask one targeted question at a time. Prioritize questions whose answers change:

- user, operator, integrator, or maintainer outcomes;
- feature boundaries and non-goals;
- ownership, data, state, and lifecycle;
- architecture, integrations, and trust boundaries;
- failure, recovery, support, rollout, or compatibility behavior;
- exact reader-facing documentation pages;
- validation and acceptance;
- dependency order and parallelism.

Continue until every feature receiving implementation tasks has a clear outcome, explicit boundaries, known
dependencies, exact documentation impact, validation strategy, and enough design intent for every task to execute
without choosing product policy. Audit each proposed task explicitly: an implementation agent must be able to satisfy
its acceptance criteria without asking the user to select behavior, schema, UX, compatibility, dependency, ownership, or
rollout policy.

Ask now about every decision that could materially change a task's implementation or acceptance. Record an unknown as a
deferred decision only when it does not block or alter any planned task, and name its owner and trigger for revisiting.
Implementation-ready designs must have no open decision required by their tasks. If the user ends planning before the
loop completes, do not create tasks for the unresolved scope; report planning as incomplete instead.

## 4. Decompose Features

Create independently valuable and reviewable features. Split work when one item combines unrelated outcomes, ownership
boundaries, migrations, or operational risks. Prefer early features that retire architectural uncertainty or unblock
several later features.

Use the lowercase filesystem-safe slug as the stable feature identity. Reject a slug already used by another feature;
documentation and roadmap order are explicit and never encoded in the identity.

Create a durable design and lifecycle when the outcome, boundaries, dependencies, validation, and documentation impact
are known. Keep a feature roadmap-only when those elements remain unresolved, but create no implementation tasks for it.
Native planning must never encode a missing user decision as an implementation blocker; only imported migration work may
temporarily retain such a gap.

## 5. Design the Documentation Structure

Choose concrete pages by reader question:

- **Introduction**: purpose, audience, scope, and boundaries;
- **Architecture**: structure, ownership, interactions, invariants, and durable decisions;
- **Operator's Manual / Usage**: deployment, configuration, observability, operation, maintenance, recovery, and
  troubleshooting where applicable;
- **Development Guide**: build, testing, extension, migration, and maintenance;
- **Reference**: exact commands, configuration, interfaces, schemas, fields, states, defaults, limits, terminology, and
  acceptance contracts.

Reuse a page that already owns the topic. Create a focused page for a new durable reader need. Register every new page
in `docs/src/SUMMARY.md`.

## 6. Create the Feature Design

Create the feature directory and draft `design.md` from:

```text
docs/src/features/_template/design.md
```

Preserve concrete user wording, examples, constraints, rejected directions, and planning decisions. Register each
created design between the feature-design markers in `docs/src/SUMMARY.md` so roadmap and audit links resolve in the
rendered book. In **Documentation Impact**, name exact files and assign each planned change to an implementation bead.

## 7. Create the Beads Lifecycle

For each feature ready for durable design, pour the repository formula:

```bash
bd mol pour dstack-feature \
  --var feature_name="<title>" \
  --var feature_slug=<slug> \
  --var design_path=docs/src/features/<slug>/design.md \
  --var implemented_path=docs/src/features/<slug>/index.md \
  --var base_branch=<base> \
  --json
```

The returned root is the feature epic (a poured molecule is an epic with workflow semantics). Keep exactly one
`workflow:feature` label on that root; lifecycle and implementation tasks remain descendants and use their own labels.
Normalize and record identity immediately. For work implemented in another repository, set `implementation_repository`,
`implementation_path`, and that repository's `base_branch` explicitly:

```bash
bd update <root-id> \
  --type epic \
  --title "<title>" \
  --add-label workflow:feature \
  --spec-id docs/src/features/<slug>/design.md \
  --set-metadata feature_slug=<slug> \
  --set-metadata feature_name="<title>" \
  --set-metadata design_path=docs/src/features/<slug>/design.md \
  --set-metadata implemented_path=docs/src/features/<slug>/index.md \
  --set-metadata base_branch=<base> \
  --set-metadata implementation_repository=<repository> \
  --set-metadata implementation_path=<absolute-or-repo-relative-path>
```

Resolve lifecycle IDs once with `bd mol show <root-id> --json`, then persist them on the root so later agents can load
only `bd show <root-id> --json`:

```bash
bd update <root-id> \
  --set-metadata design_id=<id> \
  --set-metadata review_architecture_id=<id> \
  --set-metadata review_simplicity_id=<id> \
  --set-metadata review_documentation_id=<id> \
  --set-metadata review_execution_id=<id> \
  --set-metadata spec_reconcile_id=<id> \
  --set-metadata implementation_id=<id> \
  --set-metadata docs_reconcile_id=<id> \
  --set-metadata validation_id=<id> \
  --set-metadata review_delivery_id=<id> \
  --set-metadata review_drift_id=<id> \
  --set-metadata delivery_id=<id> \
  --set-metadata workflow_kind=molecule
```

Beads does not substitute formula variables inside structured metadata. After resolving the lifecycle IDs, set concrete
identity and path metadata on every lifecycle task; never retain a `{{variable}}` value:

```bash
for lifecycle_id in \
  <design-id> <review-architecture-id> <review-simplicity-id> <review-documentation-id> <review-execution-id> \
  <spec-reconcile-id> <implementation-id> <docs-reconcile-id> <validation-id> <review-delivery-id> \
  <review-drift-id> <delivery-id>
do
  bd update "$lifecycle_id" \
    --set-metadata feature_slug=<slug> \
    --set-metadata feature_name="<title>" \
    --set-metadata design_path=docs/src/features/<slug>/design.md \
    --set-metadata implemented_path=docs/src/features/<slug>/index.md \
    --set-metadata base_branch=<base>
done
```

Lifecycle creation is complete when `bd show <root-id> --json` reports an epic, contains every required lifecycle ID,
each ID resolves to the intended child, and no root or lifecycle metadata value contains a formula placeholder. Confirm
that the human selector resolves back to that root:

```bash
uv run <core-dir>/scripts/resolve-feature.py <slug> --json
```

Do not use an opaque Beads hash as the primary feature reference in roadmap recommendations or user-facing workflow
commands. Preserve the root ID in metadata, reports, and commit evidence where auditability requires it.

Migrated legacy roots may be ordinary epics rather than molecules. Their importer stores the same lifecycle ID metadata,
so downstream skills use one interface for both shapes.

## 8. Create Implementation Beads

Create bounded tasks beneath the lifecycle implementation coordinator. Each task contains:

- one concrete outcome and bounded scope;
- acceptance criteria that require no new user decision;
- relevant design sections;
- exact documentation ownership;
- validation commands or evidence;
- true prerequisites;
- parallelism metadata where useful;
- a practical commit boundary.

Choose the narrowest useful Beads type: `task` for ordinary bounded work, `bug` for a known defect, `spike` for
timeboxed implementation fact-finding with explicit exit criteria, and `chore` for maintenance. Record a `decision`
during planning when an explicit architecture or product choice must be resolved before `spec-reconcile`; never defer
that choice into an implementation-ready child. Use `story` only for an explicitly managed user-story backlog and do not
use `milestone` as executable work.

Use `parent-child` for hierarchy and `blocks` for actual prerequisites. Independent siblings remain parallel. Every
implementation child must depend on the lifecycle `spec-reconcile` step so implementation cannot become ready before
specification review. Name bounded tasks for recognition outside a tree view:

```text
<feature-slug> <task-key> — <concrete outcome>
```

Store `feature_slug` and `feature_name` on every lifecycle and implementation task. The feature epic remains the single
parent/container; the implementation coordinator is a task gate with bounded tasks beneath it, not a second feature epic
or a milestone.

Before completing the graph, reject or rewrite any native task containing `TBD`, unresolved alternatives, "decide",
"choose", or research whose result selects required product behavior. Research tasks may gather implementation facts
only when every possible result fits an already-decided contract.

## 9. Complete Planning State

Close the lifecycle design step when the draft design and implementation graph exist:

```bash
bd close <design-step-id> --reason "Planning Q&A complete; draft design and implementation graph created"
```

Leave the four isolated review steps ready for `/start-feature`.

Update `docs/src/planned-features.md` with concise roadmap narrative, canonical `<slug>` feature reference, Beads root
ID for auditability, dependencies, design link, sequencing rationale, and status snapshot. Keep detailed intent in
`design.md` and live state in Beads.

Commit planning documentation when downstream worktrees need it. Include the feature root ID in the commit message.

## Completion Criteria

Planning is complete when the roadmap is coherent, each feature is one human-named Beads epic with lifecycle/tasks
beneath it, near-term features have stable slugs and designs, implementation is decomposed into bounded work, exact
documentation changes and validation are assigned, and every native implementation task is executable without another
user decision. Unresolved decision blockers are permitted only on work imported by `/migrate-workflow` and must carry
explicit reconciliation provenance.

Select the recommended feature from Beads rather than manually copying a hash:

```bash
uv run <core-dir>/scripts/resolve-feature.py --next --json
```

Return the helper's `recommended_command`, such as `/start-feature conduit-rest-list-response-validation`, together with
the human feature name and root ID. Never append characters to a Beads ID or recommend an opaque ID when the canonical
slug or exact feature name is available.
