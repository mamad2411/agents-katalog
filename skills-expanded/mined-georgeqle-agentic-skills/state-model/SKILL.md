---
name: state-model
description: Orchestrator — author the flow-anchored logical domain model (entities, state machines, events/commands, read models, policies, logical contracts) from an approved user-flow map, running one domain-modeling framework per session, before UX variation work
type: planning
version: v0.9
required_conventions: [alignment-page, design-tree-loop, interrogation-page]
argument-hint: "[optional: topic, user-flow, or feature] [--synthesize] [--no-chunk]"
context_intake: scoped
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# State Model — Orchestrator

Invoke as `$state-model`.

This is an **orchestrator skill** that authors the **logical** domain/state/logic model anchored to an approved user-flow map, running **one domain-modeling framework per session** and synthesizing their outputs into a proposed domain model plus a `model-tree` manifest for HTML alignment review. It writes the canonical domain model and manifest only after confirmed approval. It sits **after `$user-flow-map`, before `$ux-variations`** in the product-design prototype pipeline.

The model it produces is a property of the *flow*, not of any one UI presentation: UX variations re-skin the same underlying entities, actions, and states, so authoring the logical model once gives `$ux-variations` and `$ui-interview` a real substrate to present, and turns `$spec-interview` into "harden this model to production" rather than "invent it."

**Just-in-time per promoted flow.** `state-model` is **not a route position** — it is invoked from `$user-flow-map`'s handoff, after `$key-moments` ranks the flows. Attach a model **only to flows `key-moments` has promoted**, in proof-priority order; never model a pruned flow. Later flows **extend** the core model rather than restating it — the first promoted flow establishes the shared entities/states, and subsequent flows add only what they introduce. The per-user-flow-branch `branches[].model_ref` remains the **primary** linkage.

**Fast-pass fold.** For a CRUD-trivial domain (the flow is straightforward create/read/update/delete over a small, obvious data shape), fold the full multi-framework session into a single **fast-pass**: a quick data-shape confirmation (entities, key fields, the handful of states) instead of running one framework per session. This is distinct from the existing framework-count (≥3) chunk fold — fast-pass applies when the *domain itself* is trivial, not merely when few frameworks were selected. Still produce the `model-tree` manifest and pass the one binding alignment gate.

**Per-screen `model_ref`.** When a single approved UI experiment screen needs its own model slice (a screen-local sub-model distinct from the flow's), `state-model` may attach a per-screen `model_ref` on the `ui_experiment` node (flow-tree v0.4), as the screen-level counterpart to the user-flow branch's `model_ref`.

**Logical only.** This skill owns entities, value objects, aggregates, state machines, events, commands, read models, policies, and logical command/query contracts (request/response/error *shapes*). It does **not** own physical concerns — storage engines, real endpoints/URLs, authentication, migrations, indexes, or deployment. Those stay owned by `$spec-interview` downstream. See Constraints.

Follow `DESIGN-TREE-LOOP.md` for prototype-phase routing, state storage, approval boundaries, and task classification. This skill is a prototype-phase orchestrator: its live loop cursor is **filesystem existence of per-framework intermediates**, not a Pattern A selected-framework run manifest. It does not use `tasks/todo.md` for framework progress.

## Architecture — Orthogonal Sibling To The Flow Tree

`state-model` is an **orthogonal sibling** of the flow tree, not a stage inside it:

- The flow-tree `route` array stays a locked six-step sequence (`user-flow-map, ux-variations, ui-interview, prototype, consolidate-prototypes, spec-interview`). This skill does **not** appear in or modify that array. Ordering is enforced by next-step recommendations, not the route enum.
- This skill owns its own `design/model-tree-{topic}.yaml` manifest, a domain-shaped sibling to `design/flow-tree-{topic}.yaml`.
- On approval it attaches the model to its user-flow branch via `branches[].model_ref` (the **primary** flow-tree write) and additionally writes the **optional** top-level `model_tree_ref` pointer as backward-compatible discovery metadata. The top-level pointer is never required; the per-branch `model_ref` is authoritative. Neither write touches the `route` array.
- **Flow bindings are authoritative in the model-tree only.** Every model element records `flow_bindings[]` pointing at flow-tree nodes. These bindings are never duplicated into the flow tree, to prevent drift.

## Prerequisites

- **Hard**: an approved `design/flow-tree-{topic}.yaml` (or `design/{slug}/flow-tree-{topic}.yaml`) and its companion `design/user-flow-{topic}.md` user-flow doc must exist. If they do not, stop and recommend `$user-flow-map [topic]` first — the logical model anchors to named flow nodes, so there must be a flow to anchor to.
- **Soft**: read these if they exist:
  - `research/positioning.md`, `research/journey-map.md`, `research/icp.md` — domain language and lifecycle context.
  - Existing `design/ux-variations-*.md`, `design/ui-requirements-*.md` — only as supplementary domain evidence; the model must not encode any single UI presentation.
  - `research/glossary.md` (or scoped) — existing ubiquitous-language terms.

## Execution Model — Prototype Session Loop (intra-skill substep chunking)

This orchestrator runs as a **prototype-phase intra-skill substep loop** per `DESIGN-TREE-LOOP.md` (Intra-Skill Substep Chunking + Shared Context Brief). Each invocation starts cold, resolves its state from the filesystem, runs **one heavy phase**, and stops. The user advances the loop by clearing context and re-invoking `$state-model` with the same topic argument.

Three-tier state, exactly as the convention defines it:

| Tier | Store | Role |
|---|---|---|
| Machine cursor | `design/model-tree-{topic}.yaml` (committed, **post-approval** synthesized manifest) | Authoritative model state. Written **only** at synthesis, never as a live run-manifest. |
| Shared context brief | `design/{slug}/_working/state-model-{topic}-brief.md` (flat: `design/_working/...`) | **Pure context, no step list**: confirmed scope/assumptions, the flow nodes in play, the planned framework set + run order with each framework's thesis, ubiquitous-language seeds, carried cross-framework decisions. |
| Per-framework intermediates | `design/{slug}/state-model-{topic}/{framework}.md` (flat: `design/state-model-{topic}/...`) | One framework's logical findings each. **Their existence IS the cursor** — the next pending framework is the first planned framework whose intermediate file does not yet exist. |

`pending = planned-frameworks − existing-intermediates`. The brief carries no status field and is never a rival ledger. There is **no `design/flow-tree.schema.json` change** for the cursor and **no `tasks/todo.md` use**.

### Per-session shape

```
setup session       §0 scope → §1 run-order detection → §2 load flow context
                    → present the Domain Modeling Scope Checkpoint inline → on confirm,
                      write the brief (pure context) → STOP
   → framework       read brief + scan which {framework}.md intermediates exist
   sessions          → run the first pending framework inline → write its intermediate
   (one per fw)      → append cross-framework facts to the brief → STOP / re-invoke
      → assemble+approve session   when all planned intermediates exist (or --synthesize):
                                   §4 assemble proposed domain model + model-tree manifest
                                   for the alignment page
                                   → ONE alignment-page review → confirmed gate
                                   → on approval write canonical doc + manifest + flow-tree
                                     model_tree_ref back-pointer + archive brief/intermediates
```

### State resolution (resolve the first match)

| State | Detected when | Heavy phase this session | Emits / stops with |
|---|---|---|---|
| **A — done** | canonical `design/domain-model-{topic}.md` and `design/model-tree-{topic}.yaml` exist | — | done; emit next-skill route (§5) |
| **B — synthesize** | brief exists, all planned framework intermediates exist, no canonical domain model (also forced by `--synthesize`) | **synthesis + assemble+approve** (§4) | the single domain-model alignment page |
| **C — run framework** | brief exists, ≥1 planned framework pending | **run next pending framework inline** (§3) | framework intermediate written, re-invoke handoff |
| **E — setup** | no brief and no canonical (cold start, after the hard prerequisite is satisfied) | scope → run-order detection → load context → Scope Checkpoint → write brief (§0–§2) | Domain Modeling Scope Checkpoint, then brief written |

**Fold for small domains.** When run-order detection plans **fewer than 3** frameworks (or `--no-chunk` is passed), do **not** spend fresh-context round-trips per framework: run setup, all framework passes, and synthesis straight through in one session, writing no brief and no intermediates, exactly as a single pass through §0–§4. Chunk only when the planned framework count is ≥ 3.

**Approval: exactly one final gate.** The framework sessions are pre-approval `_working/`-band drafting — they write intermediates, not canonical artifacts, so no checkpoint inside them authorizes a canonical write. The Domain Modeling Scope Checkpoint (setup) and any per-framework coverage checkpoints are confirmations, not approvals. The single binding alignment-page `review → confirmed` gate is in the assemble+approve session and approves the whole model at once.

### Required Progress Handoff Block

Every chunked stop (setup, each framework, and the synthesis-ready handoff) must start `## Next Work` with the Progress Handoff Block from `DESIGN-TREE-LOOP.md`. The block must include:

- `**Progress Handoff — state-model/<topic-or-branch>**` as the first line.
- `Completed: <completed framework count> / <planned framework count>.`
- `Durable cursor: checked design/{slug}/_working/state-model-{topic}-brief.md and design/{slug}/state-model-{topic}/.`
- `Current phase complete: <setup | framework name | synthesis preparation> is complete.`
- `Next phase: <plain-English framework purpose or assemble+approve work>.`
- `Why repeat this command: the repeated command is intentional; $state-model cold-starts, reads the durable cursor, and advances the next pending framework or synthesis.`
- `Session guidance: continue in a fresh session — clear context (/clear), then run the Exact next command below; $state-model cold-starts and reads the durable cursor. Pasting the ## Invoke With YAML block alongside the command gives the fresh agent its routing context (optional — the command alone resolves state from the cursor). Staying in this session is allowed only if enough context remains.`
- `Exact next command: $state-model <literal topic-or-branch>.`

Use the same `$state-model` command for setup → first framework, framework → next framework, and final framework → synthesis; explain that the repeated command is intentional because filesystem existence is the cursor. The `Session guidance` line is an action directive (clear context, re-run the command in a fresh session), not a passive recommendation.

**Setup-stop one-time tradeoff note.** At the **setup** stop only (the Domain Modeling Scope Checkpoint handoff), additionally state once that the user *can* run the whole loop in one continuous session (or pass `--no-chunk`), but later frameworks/synthesis risk poorer quality and higher token cost from context bloat as the session fills, so a fresh session per phase is recommended. Do not repeat this note at the per-framework or synthesis stops.

---

## Design-Tree Flow

This skill runs the unified **5-stage design-tree flow** (`interrogation → research → design → plan → implement(scoped)`) from `DESIGN-TREE-LOOP.md`, scoped to the **per-user-flow-branch model attachment** it owns (`branches[].model_ref`). The `## Process` steps below group by stage:

- **Stage 0 — Interrogation**: the stage-zero loop in `## Interrogation Page` / `INTERROGATION-PAGE.md` plus the **Domain Modeling Scope Checkpoint** (§2) — confirm the framework set/order, domain boundaries, and the logical-only line.
- **Stage 1 — Research**: **Run-Order Detection** (§1) and **Load Flow Context** (§2) — read the approved flow tree and soft prerequisites, then plan which domain-modeling frameworks run.
- **Stage 2 — Design**: **Run Next Pending Framework** (§3) — author the per-framework logical intermediates with their `flow_bindings`.
- **Stage 3 — Plan**: the confirmed framework set + run order is the build-plan slice; it folds into setup for fewer-than-3-framework domains.
- **Stage 4 — Implement (scoped)**: **Synthesis + Assemble & Approve** (§4) — assemble the proposed `design/domain-model-{topic}.md` and `model-tree-{topic}.yaml` content for the alignment page, then after confirmed approval write the canonical artifacts and attach the model to the branch via `branches[].model_ref` (legacy top-level `model_tree_ref` stays back-compat).

**Per-branch iteration contract.** Each session cold-starts, reads the flow-tree manifest, resolves the **first user-flow branch with no confirmed `model_ref`** (honoring any explicit branch argument), runs the staged flow scoped to that branch, attaches the model on approval, and stops with the handoff in `## Next Work`.

**Modify-back.** A downstream `modify` decision whose `targets[]` names this branch's `model_ref` returns the attachment to pending, so this skill re-runs its flow on that branch; descendant UX/UI branches below it are marked stale for re-validation.

## Process

### 0. Product-Path Scope Resolution

Resolve scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint.

When product path `{slug}` is active, read and write pre-prototype design artifacts under `design/{slug}/` and treat top-level `design/*.md` files as flat-mode documents. The topic slug derives from the flow-tree `topic` being modeled.

### 1. Run-Order Detection

Inspect the approved flow tree and user-flow doc to plan **which of the six domain-modeling frameworks run, and in what order**. All six are available; the engagement determines the set and sequence the way `journey-map` detects mode.

The six frameworks:

- `event-modeling` — timeline of events/commands/read-models across the flow; best first when the flow is workflow-heavy and temporal.
- `event-storming` — big-picture domain-event discovery; best first when the domain is novel or vocabulary is unsettled.
- `domain-model` — DDD entities, value objects, aggregates, and aggregate boundaries.
- `state-machine` — statecharts for each stateful subject (states, transitions, events, guards, actions).
- `data-model` — logical ERD: entities, attributes, relationships, cardinalities (logical, never physical storage).
- `contract-map` — logical command/query contracts: request/response/error shapes per action (logical I/O, never real endpoints).

Detection signals (read from the flow tree and user-flow doc):

- **Domain novelty / unsettled vocabulary** → lead with `event-storming`, then `domain-model`.
- **Workflow/temporal complexity (many ordered steps, handoffs, async waits)** → lead with `event-modeling`.
- **High stateful-entity count (many statuses, lifecycles, approval/retry transitions)** → ensure `state-machine` runs and weight it early.
- **High entity/relationship count (rich data with many associations)** → ensure `data-model` runs.
- **Many distinct user/system actions per screen** → ensure `contract-map` runs.
- **Simple domains** (few entities, one or two flows, settled vocabulary) → plan a reduced set (e.g. `domain-model` + `state-machine`, or add `data-model`) and fold per the Execution Model.

Always include `domain-model` (the DDD spine). Order the rest by the dominant signal; `data-model` and `contract-map` typically run after the conceptual frameworks so they can reference settled entities and states. Record the planned set, order, and the one-line rationale per framework.

### 2. Load Flow Context + Domain Modeling Scope Checkpoint (setup session)

- Read the approved `design/{flow-tree, user-flow}-{topic}` artifacts: flow nodes, screens/routes, actions, decisions, branches, states, failure paths, handoffs.
- Read soft prerequisites (positioning, journey, glossary) for domain language.
- Identify the candidate ubiquitous-language seeds the flow already implies.

Present a **Domain Modeling Scope Checkpoint** inline as the final message text of its own turn (never only as mid-turn text in a turn that ends with a tool call). Cover:

- The flow nodes in play and the topic being modeled.
- The detected framework set + run order, with the one-line rationale per framework.
- Confirmed assumptions about domain boundaries and explicit non-goals (especially the logical-only boundary — no storage/endpoints/auth/migrations).
- Candidate ubiquitous-language seeds.

Ask the user to confirm, correct, or adjust the framework set/order in the next turn. This checkpoint is a confirmation, not a final approval. On confirmation, write the **shared context brief** to `design/{slug}/_working/state-model-{topic}-brief.md` (flat: `design/_working/state-model-{topic}-brief.md`) containing **pure context only** — confirmed scope/assumptions, the flow nodes in play, the planned framework set + order with each framework's thesis, ubiquitous-language seeds, and carried decisions — with **no step list and no status field**. Then STOP and emit the **Terminal handoff format** from `DESIGN-TREE-LOOP.md` plus the required Progress Handoff Block: state the brief was written, name the **first** pending framework to run in **plain English** (what that framework models, never only its internal `{framework-slug}`), explain why the same `$state-model` command is repeated, and give the **exact** resolved next tool or command call with `{topic}` filled in, e.g. `$state-model alignment-page-review`, so the first framework runs in its own cold spec session (§3). Because this is the **setup** stop, also include the one-time single-session tradeoff note (the Setup-stop one-time tradeoff note under Required Progress Handoff Block): the user may run the whole loop in one session or with `--no-chunk`, but later phases risk poorer quality and higher token cost from context bloat — fresh-per-phase is recommended. (Unless folding per the Execution Model, in which case continue directly to §3.)

### 3. Run Next Pending Framework (framework session)

Each framework session resolves its work purely from the filesystem: read the brief, scan which `{framework}.md` intermediates already exist under `design/{slug}/state-model-{topic}/`, and run the **first planned framework whose intermediate does not yet exist**.

Run that one framework inline against the flow context in the brief, producing **logical** findings only, and write them to `design/{slug}/state-model-{topic}/{framework}.md`. Each intermediate must, where the framework applies:

- Name the model elements it introduces or refines (entities/value-objects/aggregates, states/transitions, events, commands, read models, policies, contracts).
- Record each element's `flow_bindings` — which flow node(s) it reads, writes, triggers, displays, or transitions — using flow-tree node references.
- Map state-machine states to UI states (`maps_to_ui_state`) where a flow state exists, so UX variations can present them.
- Flag any term that belongs in the ubiquitous-language glossary.
- Keep strictly to logical concerns; defer every physical concern to `$spec-interview` with an explicit note rather than inventing storage/endpoint/auth detail.

Append any cross-framework facts (renamed entities, merged aggregates, newly discovered events) to the brief so later frameworks inherit them. Then STOP and emit the **Terminal handoff format** from `DESIGN-TREE-LOOP.md` plus the required Progress Handoff Block. After writing, recalculate `pending`: if frameworks remain, the handoff states the intermediate just written, names the next pending framework in **plain English** (what it models, never only its internal `{framework-slug}`), explains why the same `$state-model` command is repeated, and gives the **exact** resolved next tool or command call with `{topic}` filled in, e.g. `$state-model alignment-page-review`; if none remain, the handoff points to the synthesis session (§4) and gives its exact command, e.g. `$state-model alignment-page-review`. Continue-vs-stop framing follows that convention's Routing Rules.

### 4. Synthesis + Assemble & Approve (assemble session)

Enter when the brief exists, **all** planned framework intermediates exist, and no canonical domain model exists yet (also forced by `$state-model --synthesize [topic]`).

Assemble the per-framework intermediates plus the brief into proposed review content for the alignment page:

1. **Proposed domain model doc content** for `design/domain-model-{topic}.md` (flat) or `design/{slug}/domain-model-{topic}.md`, with sections: ubiquitous-language glossary, entities (with kind, attributes, relationships), state machines (states, transitions, `maps_to_ui_state`), events, commands, read models, policies, logical contracts, an evidence/flow-binding matrix, assumptions/confidence, and explicit physical-concern deferrals to `$spec-interview`.
2. **Proposed synthesized manifest content** for `design/model-tree-{topic}.yaml` (flat) or `design/{slug}/model-tree-{topic}.yaml`, per the `design/model-tree.schema.json` contract and the shape below.

Build the **one** alignment page (`alignment/state-model-{topic}.html`) rendering the full proposed domain model, the flow-binding matrix, the state-machine/ERD diagrams (visual tier), assumptions/confidence, the proposed file changes, the glossary-additions gate, and the approval gate. Stop for compiled YAML.

On approval (compiled YAML with no unresolved negative feedback):

- Write `design/domain-model-{topic}.md` and `design/model-tree-{topic}.yaml`.
- Attach the branch-scoped model via `branches[].model_ref` in the flow-tree manifest.
- Write the optional top-level `model_tree_ref` pointer into the flow-tree manifest (`design/{flow-tree}-{topic}.yaml`), pointing at the new model-tree path. Do **not** touch the flow-tree `route` array or duplicate any binding into the flow tree.
- Append only user-approved glossary terms to the target glossary per the glossary write-forward convention.
- Archive the brief and per-framework intermediates under `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>` (archive-at-canonical-write timing).
- Emit the downstream next-step route (§5).

### 5. Next Steps (after synthesis only)

After the canonical domain model and model-tree are written, recommend the **first** match:

1. **Default** → check `.agents/project.json.enabled_packs` for `product-design`; if enabled, recommend `$ux-variations [specific-user-flow]` — the variation work now has a real logical substrate to present. Name the specific user flow from the flow tree.
2. If `product-design` is not enabled, recommend `npx skillpacks install product-design` from the project shell first.
3. **Never** recommend `$spec-interview` here — it is many steps downstream and owns the physical-model hardening pass.

Do not emit cross-skill routing before synthesis is approved and written. While a framework or the synthesis page is pending, the only continuation route is re-invoking `$state-model` with the same topic argument.

## Output

- Setup session: the Domain Modeling Scope Checkpoint (inline) + the shared context brief.
- Framework session: one `design/{slug}/state-model-{topic}/{framework}.md` intermediate per planned framework.
- Assemble session: proposed `design/domain-model-{topic}.md` and `design/model-tree-{topic}.yaml` content rendered into the `alignment/state-model-{topic}.html` review page; after approval, the canonical doc, manifest, branch `model_ref`, flow-tree `model_tree_ref` back-pointer, glossary additions, and archive cleanup are written.

### `model-tree-{topic}.yaml` shape

Same envelope as `design/flow-tree.schema.json` (`schema_version`, `topic`, `mode`/`product_path`, `source_artifacts`, kebab `id` pattern, `additionalProperties:false`, status enum `proposed|confirmed|rejected|deferred`). Body:

- `flow_tree_ref` (binding anchor) + `frameworks[]` (record of which frameworks were run/synthesized).
- `entities[]` — `kind: entity|value-object|aggregate-root`; attributes, relationships with cardinality, `lifecycle_ref` to a state machine.
- `state_machines[]` — subject, states (each with optional `maps_to_ui_state`), transitions (event/guard/action).
- `events[]`, `commands[]`, `read_models[]`, `policies[]`.
- `contracts[]` — `kind: command|query`; request/response/error shapes, **logical only**.
- Every element carries `flow_bindings[]: {flow_node_ref, access: reads|writes|triggers|displays|transitions}`. Bindings live in the model-tree only and are never duplicated into the flow tree.

## Interrogation Page

Before producing research, run the stage-zero interrogation loop following `INTERROGATION-PAGE.md` in this skill's directory. Build one HTML page per round at `interrogation/state-model-r{N}-{branch}.html`, starting with the assumptions manifest as round 1, and loop until the confidence gate passes. This skill **cannot advance to stage one until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. Each round page must contain at least one genuinely open input (`data-open-input`).

## Next Work

**Next work:** after the domain model is approved and attached, grow the first unresolved user-flow branch's variations with `$ux-variations [specific-user-flow]` — the variation work now has a real logical substrate to present. If user-flow branches remain without a model, the next work is re-invoking `$state-model [topic]` for the next branch.

**Recommended next command:** `$ux-variations [specific-user-flow]`.

## Invoke With YAML

Emit the `agent_routing` payload with the exact resolved next-invocation command, `{slug}`/`{topic}`/branch filled to literal values: `$ux-variations [specific-user-flow]` once every user-flow branch carries a confirmed model; otherwise `$state-model [topic]` for the next unmodelled branch.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/state-model-{topic}.html`.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical design document (`design/**/*.md`, `design/**/*.yaml`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly; do not edit it after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.

## Constraints

- **Logical only.** Do not specify storage engines, databases, real endpoints/URLs, authentication/authorization mechanisms, migrations, indexes, deployment, or any physical architecture. When a physical concern arises, record it as an explicit deferral to `$spec-interview`, not as a decision. The model captures *what* the domain is, not *how* it is stored or served.
- **Anchor to the flow, not to a UI.** The model is a property of the user flow. Do not encode any single UX variation or UI presentation. UX variations re-skin the same entities/actions/states.
- **Bindings are authoritative in the model-tree only.** Never duplicate `flow_bindings` into the flow tree; never modify the flow-tree `route` array. The flow-tree writes are the per-branch `branches[].model_ref` attachment (primary) plus the optional top-level `model_tree_ref` back-compat pointer.
- **One heavy phase per session.** Run setup, one framework, or synthesis per invocation; advance by re-invoking `$state-model`. Fold to a single session only for fewer-than-3-framework domains or `--no-chunk`. Do not queue framework work in `tasks/todo.md` or hand it to `$exec`.
- **Synthesis requires at least one framework intermediate.** Do not synthesize from zero evidence.
- The live cursor is per-framework intermediate existence; the model-tree is written only at synthesis as the post-approval manifest, never as a live run-manifest.
- Present the model before writing canonical artifacts; exactly one binding alignment gate, at synthesis.
- When recommending a skill from another pack, verify pack availability through `.agents/project.json.enabled_packs`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
