---
name: map-it-out
description: Manually map and resolve a large, uncertain initiative as local decision records, dependencies, frontier, fog, scope, and planning clusters, releasing each resolved decision or completed cluster for planning as soon as it is ready. Use only through explicit start, resume, status, or release commands.
disable-model-invocation: true
---

# Map It Out

Map a large initiative whose route cannot fit safely in one planning context. Store the map and its
decisions as local Markdown, resolve one available decision per resumed session, and stop when the
route to the destination is clear. Plan by default. Do not implement the destination or create build
tasks.

Invoke manually:

```text
/skill:map-it-out start <initiative>
/skill:map-it-out resume <initiative-or-map-path> [decision-name-or-path]
/skill:map-it-out status <initiative-or-map-path>
/skill:map-it-out release <initiative-or-map-path> <decision-name-or-path>
```

Explicit invocation authorizes creation or updates only under the selected decision-map directory
and any specialized planning artifact path approved by this workflow. It does not authorize source
changes, production access, destructive actions, commits, pushes, or implementation planning.

## Ownership boundary

`map-it-out` owns all durable navigation state:

- destination and standing notes;
- decision records and their statuses, types, dependencies, claims, and plannability;
- planning clusters and the record of which of them have been planned;
- the derived frontier;
- decisions already made;
- task-free records and their retirement;
- not-yet-specified areas;
- out-of-scope areas; and
- readiness and the planning handoff.

`talk-it-through` is a stateless decision-resolution engine. Invoke it in embedded-decision mode for
one supplied human decision. It must return a structured result and must not write or update the map.
`research-for-planning` owns authoritative external research artifacts. A configured prototype
workflow owns an approved disposable prototype. `map-it-out` classifies and persists their results.

## Local artifact model

Choose the map directory in this order:

1. a path explicitly supplied by the user;
2. an existing matching directory under `plans/decision-maps/`;
3. `plans/decision-maps/<initiative-slug>/`.

Never create two maps for the same destination. Use this structure:

```text
plans/decision-maps/<initiative>/
  map.md
  clusters/
    <cluster-name>.md
  decisions/
    001-<decision>.md
    002-<decision>.md
    resolved/
      003-<decision>.md
      004-<decision>.md
  research/
    <topic>.md
  prototypes/
    <artifact-or-pointer>
```

The map is a low-resolution index, not a duplicate store. A decision's question, evidence,
alternatives, and resolution live only in its decision file. `map.md` contains only the destination,
standing notes, one-line resolved-decision pointers, fog, scope exclusions, readiness, and the
regenerated handoff list.

Derive every changeable relationship by scanning metadata rather than storing a second copy of it.
The frontier, cluster membership, cluster state, and the handoff list are all derived on every
`resume` and `status`. Store only what cannot be recomputed: a decision's own metadata and
resolution, and the record in a cluster file of which task ordinals `to-plan` already produced.

### Map format

```markdown
# Decision map: <initiative>

**Status:** mapping | active | ready

## Destination
<One or two lines defining what reaching the end of this map means.>

## Notes
<Domain constraints, source documents, standing preferences, and skills later sessions need.>

## Decisions so far
- [<resolved decision name>](decisions/resolved/<file>.md): <one-line result>
- <retired task-free record name>: <one-line result, unlinked once the file is retired>

## Not yet specified
<In-scope areas that matter but cannot yet be stated as precise questions.>

## Out of scope
<Work beyond the destination, with a reason and a link when a decision record exists.>

## Handoff
<Regenerated on every resume and status. Never patched in place.>

Plannable now:
- [<decision or cluster name>](<path>), standalone | cluster of <n> decisions
  /skill:to-plan <path>

Forming:
- <cluster name>, <n> of <m> resolved, waiting on <linked decision names>

Planned:
- <cluster or decision name>, tasks <ordinals>

Retirable task-free records:
- [<task-free record name>](decisions/resolved/<file>.md), every citing decision resolved
```

`Handoff` lists only what the user can act on: handles to plan, clusters still forming, work already
planned, and task-free records they may retire. A task-free record never appears under
`Plannable now`.

### Cluster format

```markdown
# Cluster: <name>

**Planned:** none | tasks <ordinals produced by to-plan>

## Delivers
<The slice of the destination this cluster produces once planned.>

## Why grouped
<Why these decisions cannot be sliced into tasks separately.>
```

A cluster file never lists its members. Membership is authoritative in each decision's `Cluster`
field and is found by scanning, so a decision can join a forming cluster without editing two files.

### Decision format

```markdown
# Decision: <name>

**Status:** open | active | resolved | out-of-scope
**Type:** discussion | research | prototype | prerequisite
**Mode:** human | agent
**Plannable:** standalone | cluster | none
**Cluster:** <cluster name when Plannable is cluster, otherwise "none">
**Depends on:** <linked decision names, or "none">
**Claim:** <current invocation marker when active, or "none">

## Question
<One precise question this record resolves.>

## Context
<Only context needed to understand the question.>

## Evidence
<Repository facts and links to research, design, or prototype artifacts.>

## Resolution
- **Decision:** <answer, or "Unresolved">
- **Rationale:** <material reason>
- **Alternatives rejected:** <durable alternatives, or "None">
- **Consequences:** <constraints created by the answer>
- **Non-goals:** <explicit exclusions>
- **Required proof:** <test or acceptance evidence later work must provide>

## Follow-on
- **Newly sharp decisions:** <links, or "None">
- **Still-foggy areas:** <map entries, or "None">
```

Use stable numbered file names, but refer to decisions by linked name in human-facing prose. Never
use a bare number as the decision's human-readable identity.

## Writing quality

A resolved decision record is the durable artifact a human reads later, so it is the only file in the
map that earns a prose audit. When a decision resolves, invoke `write-well` in review mode on that
record, apply every supported fix that preserves meaning, and complete the audit before saving.

Everything else is working navigation state. Open decision files, `map.md`, cluster files, and the
regenerated `Handoff` are written clearly and left alone; do not audit them. Research and prototype
artifacts keep whatever treatment their own skill applies. The single audit outside a resolved
decision is the planning brief described under Handoff and completion, which `write-planning-brief`
produces and audits there.

Keep the `write-well` audit plan in working context and report its pass count. Do not write the audit
plan into the decision map unless the user asks for it.

## Decision states and frontier

A question becomes a decision file when it can be stated precisely, even if another decision blocks
it. Keep an area in `Not yet specified` when the question itself is still unclear. Do not create
speculative decision files merely to empty the fog section.

A decision is available when it is `open`, every linked dependency is `resolved`, and it has no
claim. The frontier is the set of available decisions in file-number order. An `active` decision is
claimed. Never work on it from another invocation. If a claim is stale, require an explicit
`release` invocation before changing it back to `open`.

An out-of-scope decision is closed and never returns to the frontier. Record its one-line reason in
`map.md` and keep it out of `Decisions so far`, which records decisions on the route to the
destination.

## Plannability and clusters

A map releases work for planning as it goes. Do not hold every answer until the whole route is clear.

Every decision carries a `Plannable` value, assigned when the decision is created and revisable while
it is still open:

- `standalone`: resolving it yields a slice a planner can turn into tasks on its own.
- `cluster`: it answers part of one slice, and tasks cannot be cut from it without the rest of its
  named cluster. Set `Cluster` to that cluster's name and create the cluster file if it is new.
- `none`: an audit, prerequisite, or research record that informs other decisions and produces no
  tasks of its own.

### Derived cluster state

Compute a cluster's state by scanning; never store it:

- `forming`: at least one member is not `resolved`, or a member has an unresolved dependency outside
  the cluster.
- `complete`: every member is `resolved`, no member has an unresolved outside dependency, and the
  cluster file records no planned tasks.
- `planned`: the cluster file records task ordinals and no member has resolved since.
- `amended`: the cluster file records task ordinals and members have resolved since.

A `complete` cluster and a resolved `standalone` decision are each a plannable handle. An `amended`
cluster is a plannable handle covering only its decisions resolved after planning. Never re-plan work
that already produced tasks.

Report handles in `Handoff` and stop. The user invokes `to-plan`; this skill never invokes it.

### Moving resolved decisions

Exactly two directories hold decisions, and the split answers one question: is this decided? An open
or active decision lives in `decisions/`. A resolved one lives in `decisions/resolved/`. There are no
`reference/` and no per-cluster subdirectories, because a deeper tree buys nothing a header does not
already state and costs a link rewrite on every session.

Placement follows one rule: **a decision moves to `decisions/resolved/` in the same step that records
its resolution, whatever its `Plannable` value and whatever state its cluster is in.** A user who
lists `decisions/` sees what is still undecided. A user who lists `decisions/resolved/` sees what is
settled. Never leave a resolved record sitting beside open ones, and never hold one back waiting on a
sibling.

Plannability stays in the record rather than in the path. A `Plannable: none` record is resolved like
any other and moves like any other; its header is what keeps it out of `Handoff` and out of any
`to-plan` invocation. A cluster member moves the moment it resolves, and cluster membership is still
found by scanning `Cluster` headers, which is unaffected by which directory the file sits in.

Any move rewrites both directions of every affected link in the same step that records the
resolution: inbound references from `map.md`, from cluster files, and from decision files outside the
moved set, and the moved file's own outbound links, whose relative depth has changed. After a move,
verify that every link in the map still resolves against the filesystem before reporting the session
complete.

### Retiring a task-free record

A `Plannable: none` record is scaffolding with a lifespan. It exists to carry a fact into decisions
that were not yet made, and once every one of those decisions is resolved, the fact lives in their
`Evidence` and `Consequences` and the record is dead weight.

Such a record is retirable when every decision that links to it is `resolved` or `out-of-scope`.
Report retirable records in `status` and at the end of `resume`, then wait. Retiring is the user's
call, never automatic, because only they know whether the audit still has a reader.

To retire one, work in this order:

1. Read each inbound citation. Where a citing record leans on the reference for a fact it does not
   state itself, write that fact into the citing record's `Evidence` in the same step. A citation
   that survives retirement as a broken link means the fact was never carried over.
2. Delete the reference file.
3. Replace its line in `Decisions so far` with the same one-line result as plain unlinked text, so
   the map still records what the audit established.

Never retire a record with a live inbound link from an `open` or `active` decision, and never retire
one whose facts no surviving record states.

## Start mode

Use when the user supplies a loose initiative.

1. Inspect relevant repository facts and source documents. Use an isolated read-only subagent for broad
   reconnaissance when available.
2. Invoke `talk-it-through` in embedded-decision mode to establish one precise destination and its
   scope boundary. Do not ask it to map the initiative.
3. Explore breadth-first across actors, behavior, state, interfaces, dependencies, safety, proof,
   and external facts. Identify precise open questions without resolving them. Keep unclear future
   areas as fog.
4. If there is no material fog and the whole discussion fits one bounded planning context, do not
   create a map. Recommend standalone `/skill:talk-it-through <topic>` and stop.
5. Otherwise create `map.md` and the decision files that can be stated precisely now. Create every
   file before adding dependency links so references are valid.
6. Classify each decision by type and mode. Discussion and prototype decisions are human-led.
   Research is agent-led. A prerequisite may be agent-led only when it is safe, local, and exists
   solely to unblock a decision.
7. Classify each decision by plannability and create a cluster file for every cluster named. Record a
   question that is already settled as a `resolved` `standalone` decision under `decisions/resolved/`
   rather than as an out-of-scope line, whenever it produces work the user will want to plan later.
   Reserve `Out of scope` for work the destination excludes and for work that cannot be built at all.
   Chart an audit or other task-free record as `Plannable: none`, and name in its `Question` the
   decisions it is meant to inform, since those citations are what later make it retirable.
8. Run independent external research decisions in parallel through `research-for-planning` when
   doing so cannot depend on another open decision. Store each artifact under `research/`, record
   its result in the owning decision, and update the map. Do not resolve human decisions during
   charting.
9. Regenerate `Handoff`, return the map path, the derived frontier, and every plannable handle, then
   stop. Charting writes open decision files, which are not audited; audit a record only when this
   step charts one as already `resolved`.

## Resume mode

Resolve at most one non-research decision per invocation.

1. Resolve the map path. Read `map.md` and only the metadata headers of decision files first. Derive
   the frontier without loading every decision body.
2. If the user names a decision, verify that it is open, unblocked, and unclaimed. Otherwise choose
   the first frontier decision. If none is available, report blocked and active decisions by linked
   name and explain what prevents progress.
3. Set the selected decision to `active` and add the claim before doing work. Preserve an active
   claim if the invocation is interrupted.
4. Read that decision and only directly related resolved records or evidence.
5. Route by type:
   - `discussion`: invoke `talk-it-through` in embedded-decision mode with the destination,
     question, context, resolved dependencies, constraints, and expected result.
   - `research`: invoke `research-for-planning` and store its cited artifact under `research/`.
   - `prototype`: state the single uncertainty a disposable artifact would answer and obtain user
     approval before invoking an available prototype workflow. Otherwise leave it open.
   - `prerequisite`: perform only safe planning-enablement work. Require explicit approval for
     external accounts, credentials, destructive actions, real data, or trust-boundary changes.
6. Persist the result in the selected decision. On resolution, set it to `resolved`, clear the
   claim, and append one linked one-line result to `Decisions so far`.
7. Treat `talk-it-through` follow-on outputs as proposals. Create decision files only for questions
   now precise enough to state. Put unclear areas in `Not yet specified`. Add dependencies after new
   files exist. Move anything beyond the destination to `Out of scope`.
8. Assign plannability to every new decision. A new decision may join a cluster that is `forming` or
   `complete`. It may not join one that is `planned`; give it the same cluster name only when the
   user wants an amendment, which the derived state then reports separately.
9. Move the resolved decision into `decisions/resolved/`, rewriting inbound and outbound references in
   the same step. A resolution that supersedes what a citing decision recorded about the same fact
   updates that citation too, so no record keeps a stale claim.
10. Recompute every cluster's state, regenerate `Handoff` from scratch, and name any handle that
    became plannable this session. Recompute which task-free records are now retirable, and retire one
    only if the user says so.
11. If a decision resolved this session, audit that record alone through `write-well` in review mode.
    Return the updated frontier, fog, plannable handles, and any retirable task-free records, then
    stop.

Independent research decisions may be delegated in parallel. Their results can close more than one
research record in a session, but no second human decision may be resolved.

## Status and release modes

`status` reads the map, cluster, and decision metadata without changing files. Return destination,
readiness, resolved-decision count, frontier by linked name, the dependency tree rendered from
`Depends on` links, every cluster with its derived state and outstanding members, plannable handles
with their `to-plan` commands, blocked decisions and dependencies, active claims, fog, out-of-scope
count, and every task-free record with the citing decisions it still waits on. Render the tree rather
than storing it in `map.md`.

`release` resets one `active` decision to `open` and clears its claim only after confirming that no
resolution was recorded. It changes metadata only. Never release a claim merely because another
invocation wants the decision.

## Handoff and completion

Planning is released per handle, not once at the end.

A resolved `standalone` decision is its own handle. Record its path in `Handoff` under
`Plannable now` with the command `/skill:to-plan <decision-path>`. A resolved `Plannable: none`
record sits in `decisions/resolved/` like any other settled decision but is never a handle, so it
never appears in `Handoff` under `Plannable now` and is never an argument to `to-plan`.

A `complete` or `amended` cluster is a handle whose path is its cluster file. When the cluster is
small enough that a planner can read its members directly, point `to-plan` at the cluster file. When
the members are numerous or interdependent enough that they must be read as one argument, invoke
`write-planning-brief` with the cluster file, its member decisions, and the related research, design,
and prototype artifacts. Then invoke `write-well` in review mode on the resulting brief, apply
supported fixes, complete its full audit, and record the brief path as the handle instead.

Recommend the product-facing route when a PRD adds value:

```text
/skill:write-a-prd <handle-path>
```

Otherwise:

```text
/skill:to-plan <handle-path>
```

Never invoke either automatically. When the user reports that a handle has been planned, record the
resulting task ordinals in the cluster file, or in the decision's `Resolution` for a standalone
handle, so the derived state becomes `planned`.

The map itself is `ready` only when:

- no decision is `open` or `active`;
- every dependency is resolved or explicitly out of scope without leaving a broken route;
- no cluster is `forming`;
- `Not yet specified` contains no material in-scope fog;
- every task-free record has been retired or the user has explicitly kept it, since at readiness they
  are all retirable by definition; and
- the destination has enough behavioral, state, interface, safety, and proof detail for its stated
  handoff.

Readiness closes the map. It is not the trigger for planning, which has already been happening handle
by handle. If the destination is a final decision or another artifact rather than planning input,
record that completed artifact in `Handoff` and stop.
