---
name: shape-backlog
description: "Turn the requirement register into the epic and feature spine, in dependency order, coded and published to the tracker. Stops before stories."
disable-model-invocation: true
---

# Shape Backlog

Build the **spine**: the Epics and Features that every story will hang from.

This skill deliberately stops before stories. The spine is a structural decision made once across the whole scope, and it is cheap to argue about while it is thirty rows in a table and expensive once three hundred stories are attached to it. Getting the axis wrong is the single most costly error in the chain.

Read `docs/delivery/requirements.md`, `docs/agents/backlog-conventions.md` and `docs/agents/delivery-tracker.md` first. Missing register means `/ingest-requirements`; missing conventions means `/setup-delivery`.

## Process

### 1. Choose the epic axis

An Epic is a **body of work large enough to be a project on its own**. Everything at this level is a slicing choice, and there are only three honest candidates:

| Axis | Epics look like | Choose it when |
|---|---|---|
| **Surface** | Driver App, Fleet Portal, Operator Console | The product is several distinct applications with different users. Most delivery engagements. |
| **Capability** | Wallet, Telemetry, Settlement | One application, several deep domains. |
| **Journey** | Onboarding, Fuelling, Reconciliation | The value is in end-to-end flows crossing every surface. |

Mixing axes is the failure. Epics named `Driver App`, `Wallet`, and `Onboarding` in one backlog guarantee that some stories have two plausible parents and land under whichever the author thought of first, and after that nothing rolls up.

Pick one axis and hold it. Then add the exception every engagement needs:

**`E0` is always foundations**, on any axis: environments, pipelines, identity scaffolding, the tracer-bullet slice that proves the stack. It is the work that has no user and blocks everything, and it is the epic teams forget to create and then do in the margins of other stories, where it is invisible and unestimated.

### 2. Number in dependency order

Epic numbers run in **dependency order, not board order**. What everything else needs comes first. The numbering is doing real work: `/plan-release` reads it as the first approximation of the route, and a human reading `E4` assumes `E1` is behind it.

Present the axis and the ordering to the user before going further. This is a decision, not a step.

### 3. Decompose each Epic into Features

A Feature is a **coherent capability** a stakeholder would recognise and ask about by name. The sizing test is downstream: a Feature should decompose into three to five stories. One that would produce one story is a story wearing a Feature's title; one that would produce twelve is two or three Features.

Two conventions from `backlog-conventions.md` bear repeating because they are broken constantly at this level:

- A Feature title never repeats its Epic's name.
- A Feature title names a capability, not a screen.

### 4. Map coverage, both ways

Build the matrix of requirement ID against Feature, and read it in both directions. The two readings catch different failures and an agent will do only the first:

- **Requirement with no Feature: an orphan.** Contracted scope with nowhere to live. Every `Must` in the register needs at least one Feature, and non-functional requirements are where the orphans cluster, because they belong to no screen.
- **Feature with no requirement: gold-plating.** Work with nothing behind it. Sometimes it is genuinely needed and the register is thin, in which case it belongs in the register as an Inferred requirement, agreed with the client. Sometimes it is invention, and it is unbilled.

Both readings go to the user. Neither is a thing to quietly fix.

### 5. Quiz the user

Present the spine as a table: code, title, the requirements it covers, and the rough story count you expect. Ask:

- Is the axis right, and is anything sitting under the wrong Epic?
- Does the dependency ordering match how they intend to build?
- Which Features are thin enough to merge, and which are fat enough to split?

Iterate until they approve. Publish nothing before then: republishing a spine means reparenting everything under it.

### 6. Publish

Create the Epics and Features on the tracker using the `create` operation from `docs/agents/delivery-tracker.md`, parents first. Titles carry hierarchy codes. Tag each item with the dimensions the conventions define, using the `tag` operation and honouring what it says about merge versus replace.

Where the tracker needs labels to exist before they are applied, create the dimension's full vocabulary first.

Leave every item in the backlog. Scheduling is `/plan-release`'s job, and doing it here is guessing before the estimates exist.

Report the publish as counts per level, then only what failed or needed a decision. The board and the map in step 7 are the record; listing every item back is a copy of a copy.

### 7. Write the map

Write `docs/delivery/backlog-map.md`: the spine as a tree, each row carrying its hierarchy code, its tracker identifier, and the requirement IDs it covers. This is what `/groom-stories` reads to find its work, and what lets a later session resolve a code to an identifier without re-querying the whole board.

## Done when

- One axis, held across every Epic, with `E0` carrying foundations.
- Every Feature has a hierarchy code, a parent, and tags.
- Coverage is mapped in both directions and both lists went to the user.
- The user approved the spine before anything was published.
- `docs/delivery/backlog-map.md` resolves every code to a tracker identifier.
- No stories exist yet.

## Hand off

Tell the user: **`/groom-stories`** next, one Epic at a time, clearing context between Epics.
