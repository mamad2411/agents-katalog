---
name: user-flow-map
description: Turn a high-level product concept, positioned goal, or goal sequence into flow and surface structure with entry points, decisions/actions/states, branches, channels, failure paths, and low-fidelity UI-candidate guidance before UX/UI/spec/prototype work
type: planning
version: v1.8
required_conventions: [alignment-page, design-tree-loop, interrogation-page]
argument-hint: "[optional: product, flow, feature, route, or goal] [--no-chunk]"
context_intake: deep
visual_tier: prototype
invocation: orchestrator
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# User Flow Map

Invoke as `$user-flow-map`.

Use this skill after positioning and before UX/UI/prototype work when a product, feature, or goal sequence needs concrete user-flow structure: entry points, surfaces, channels, actions, decisions, branches, states, failure paths, handoffs, and low-fidelity notes for surfaces that may become UI. Treat the output as the root of a design tree: each mapped user flow can fan out into `$ux-variations [flow]`, where the team explores alternate ways users can progress through that specific flow before any one variation is promoted into `$ui-interview`. After the flow map is approved, the recommended next step is `$state-model [topic]` — an orthogonal sibling that authors the flow-anchored logical domain model (entities, state machines, events, logical contracts) once, so `$ux-variations` and `$ui-interview` re-skin a real substrate rather than inventing the model per presentation. `$state-model` is optional and does not change the flow-tree route; route directly to `$ux-variations` when the domain is trivial.

Use `$user-flow-map --prototype-build-plan [topic]` after `$ui-interview` branch decisions exist to synthesize the approved design tree into one prototype build ledger. This later synthesis mode does not remap the original flows; it reads the flow-tree manifest, branch decisions, UX variation plans, UI branch packets, and any user overrides, then writes `design/prototype-build-plan-[topic].md` as the todo contract for `$logic-wiring`.

Follow `DESIGN-TREE-LOOP.md` for prototype-phase routing, state storage, approval boundaries, and task classification. This skill owns the wireframe-tree root and later build-plan synthesis; it does not use Pattern A selected-framework manifests or `tasks/todo.md` for branch progress.

This skill does not create polished UI, visual styling, production specs, or runnable prototypes. Keep layout and styling out of scope except for wireframe-level structural notes on visual UI candidate surfaces, such as "summary panel beside task list" or "confirmation step before destructive action." For non-visual surfaces, describe the response, event, validation, state, or audit shape at interface level instead of forcing it into a screen. Do not flatten the tree into a single UI requirements path; preserve named user flows as branch roots for downstream variation work.

## Surface Terminology

Use `surface` as the umbrella term for any place where the flow becomes visible, actionable, or inspectable to a human, agent, or system. A surface can be visual or non-visual.

Use `channel` for the delivery or access method for a surface: web UI, MCP response, CLI output, API response, SDK/tool-call result, notification, background event, validation result, or audit record. Treat MCP, CLI, SDK/tool-call, and API variants as channels of the same surface by default. Split them into separate surfaces only when behavior materially differs, such as an interactive CLI repair flow versus a structured MCP error payload.

Use `screen`, `route`, or `region` only for the visual UI realization of a surface. Use `tool response`, `event`, `validation result`, or `audit record` for non-visual realizations. `ui-interview` owns the visual UI candidates; `state-model` owns commands/events, state transitions, channel parity, and logical contracts; `logic-wiring` owns runnable CLI/API/infra behavior when a prototype needs it.

## Design-Tree Flow

This skill runs the unified **5-stage design-tree flow** (`interrogation → research → design → plan → implement(scoped)`) from `DESIGN-TREE-LOOP.md`, and is the **root orchestrator** that creates the design tree. The `## Process` steps below group by stage:

- **Stage 0 — Interrogation**: the stage-zero loop in `## Interrogation Page` / `INTERROGATION-PAGE.md` plus the **Flow Assumptions Checkpoint** (step 2) — confirm persona, scope, and flow boundaries before mapping.
- **Stage 1 — Research**: **Resolve Context** (step 1) — read idea/research/positioning/journey evidence and existing `design/` artifacts; Product-Path Scope Resolution and the Design Flow Tree Manifest (steps 0/0b) resolve where the tree lives.
- **Stage 2 — Design**: **Map The Flow** (step 3) and the **Flow Coverage Checkpoint** (step 4) — author flow structure, surfaces, channels, states, branches, and low-fidelity notes for visual UI candidates.
- **Stage 3 — Plan**: **Prototype Build-Plan Synthesis Mode** (step 5) — synthesize the approved tree into the `design/prototype-build-plan-[topic].md` slice `$logic-wiring` realizes.
- **Stage 4 — Implement (scoped)**: write the flow doc, initialize the `flow-tree-[topic].yaml` root, grow one user-flow branch per flow, and pass the single binding alignment gate (`## Alignment Page`) before any canonical write.

**Per-branch iteration contract.** Each session cold-starts, reads the flow-tree manifest, resolves the next pending unit (the next unmapped flow, or in build-plan mode the next branch needing a build item), runs the staged flow scoped to it, grows the child nodes on approval, and stops with the handoff in `## Next Work`.

**Modify-back.** Downstream validation can re-open this root's branches: a `modify` decision recorded in the flow-tree `decisions[]` names `targets[]` pointing at a user-flow branch to re-open, returning it to pending so this skill re-runs its flow on that branch and marks descendant branches stale.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, pre-prototype design artifacts under `design/{slug}/`, finalized post-prototype implementation specs under `specs/{slug}/`, and treat top-level `research/*.md` and `design/*.md` files as flat-mode documents or cross-path summaries.

### 0b. Design Flow Tree Manifest

Use `design/flow-tree.schema.json` as the machine-readable contract for the pre-prototype product-design tree.

- Product-path mode writes one scoped manifest at `design/{slug}/flow-tree-{topic}.yaml`.
- Flat mode writes one scoped manifest at `design/flow-tree-{topic}.yaml`.
- Initialize the manifest when writing the flow map. Set `schema_version: v0.4`, `mode`, `topic`, `product_path` when scoped, `route: [user-flow-map, ux-variations, ui-interview, logic-wiring, consolidate-prototypes, spec-interview]`, `source_artifacts`, and one `branches[]` entry per named user-flow branch.
- Only named user-flow branches become `branches[]` entries in the design-tree manifest. Surfaces are supporting flow-map detail unless a downstream UX/UI skill promotes a surface into a UX variation, UI experiment, build item, or model attachment.
- Order `branches[]` by journey progression by default: discovery or activation before first-value, first-value before ongoing-use, recovery and handoff where they actually occur, and ascending `journey_sequence` inside each stage. Use raw authoring order only as a stable tiebreaker after journey sequence and explicit fit/rationale metadata.
- Each user-flow branch must include `journey_stage`, `journey_sequence`, `priority_rationale`, and `progressive_review` metadata. The progressive review entry must name the first value moment, primary task path, and progressive review sequence for reviewers before downstream UX/UI work begins.
- If the user explicitly overrides the default branch order, keep the user-chosen order and explain the override in `priority_rationale`. Persist branch order override metadata in `design/**/flow-tree-*.yaml` with schema-backed `ordered_branch_ids`, `override_rationale`, `recorded_at`, and optional `parent_branch_id` for UX-variation overrides.
- In prototype-build-plan mode, add or update the manifest `prototype_build_plan` object with artifact references and one build item per approved UI experiment that should be prototyped.
- Track user-flow, UX-variation, UI experiment, prototype build item, and approve/reject/retry decision state only in the design manifest. Do not write UX branch state to `research/.progress.yaml`; that file remains product-path/product-line tracking.
- Reference all pre-prototype design artifacts from the manifest using repo-relative paths.
- Do not mirror user-flow, UX variation, UI review, prototype build, or branch decision progress into `tasks/todo.md`.

### 0c. Session model — chunked per-section spec sessions vs. one continuous session

For a **large** flow, the step-3 mapping fans out into several heavy per-section work products, and holding them all in one context is the dominant per-session cost. Estimate flow size from the Flow Assumptions Checkpoint's likely surface count (step 2): if the flow is large — **surface inventory ≥ ~6 surfaces** — and `--no-chunk` was not passed, enter **chunked mode**; otherwise run one continuous session exactly as a single pass through steps 1–4 (the common case). Chunked mode follows the **Intra-Skill Substep Chunking + Shared Context Brief** mechanism in `DESIGN-TREE-LOOP.md`: a setup session (steps 1–2 + step-3 sub-steps 1–5) writes a pure-context brief and stops; one spec session per step-3 heavy section (in order: `surface-inventory` → `action-state-matrices` → `failure-recovery` → `handoffs`) authors a single section's intermediate; and a final assemble+approve session (step 4 + deliverables + the one alignment page) assembles the canonical flow map. The units here are more interdependent than `ux-variations` — later sections reference earlier ones — so the brief carries more shared context: persona, goal, happy path, entry points, and decision/branch rules. The progress cursor is intermediate-file existence — the brief carries no step list, and there is no schema change and no `tasks/todo.md` use. Chunking applies to default flow-mapping only; prototype-build-plan synthesis mode (step 5) never chunks. For small flows or when `--no-chunk` is passed, write no brief and no intermediates and behave exactly as v0.8 did.

### 1. Resolve Context

Read available evidence before asking deep questions:

- `.agents/project.json`, `AGENTS.md`, `CLAUDE.md`, `README.md`, and relevant task docs.
- `research/idea-brief.md`, `research/icp.md`, `research/competitive-analysis.md`, `research/journey-map.md`, `research/positioning.md`, and product-path-scoped equivalents.
- Existing `design/`, including `design/user-flow-*.md`, `design/ui-requirements-*.md`, `design/ui-*.md`, `design/ux-variations-*.md`, product-path-scoped equivalents, and `design/**/flow-tree-*.yaml`.
- Existing `specs/` only as finalized post-prototype implementation context.
- Existing route files, component files, app shells, navigation config, screenshots, wireframes, mockups, and design artifacts when present.

If `research/positioning.md` is missing for a business-product flow, recommend `$positioning` first. If `product-design` is not enabled, recommend `npx skillpacks install product-design` from the project shell.

### 2. Flow Assumptions Checkpoint

Before deep probing, present a concise **Flow Assumptions Checkpoint** inline as the final message text of its own turn — never only as mid-turn text in a turn that ends with a tool or command call — then ask the user to confirm, correct, or flag it in the next turn. Tag each assumption with `[from idea]`, `[from research]`, `[from positioning]`, `[from journey]`, `[from spec]`, `[from codebase]`, `[from artifact]`, or `[inferred]`.

Cover:

- Persona, role, and goal.
- Entry points and triggers.
- First success or completion condition.
- Happy path sequence.
- Alternate paths and branch points.
- Decisions the user or system must make.
- Surfaces likely required, with surface type, channels, and visual UI candidate status.
- Actions and states per surface.
- States to represent: empty, loading, error, partial, success, permission-denied, offline, validation, and edge states.
- Failure and recovery paths.
- Cross-role, cross-device, external-system, or manual handoffs.
- Flow boundaries and explicit non-goals.

Do not proceed until the user has reviewed the checkpoint. If the user confirms it as-is, continue. If they correct an assumption, carry the correction into both deliverables.

### 3. Map The Flow

Build the flow map at workflow level, not visual-design level:

**Chunked-mode sessions (step 0c).** When chunked mode is active (large flow, no `--no-chunk`): the setup session runs sub-steps 1–5 below (persona/goal/success, entry points, happy path, alternate paths, decision points), then writes the shared context brief to `design/{slug}/_working/user-flow-map-{topic}-brief.md` (flat mode: `design/_working/user-flow-map-{topic}-brief.md`) containing **pure context only** — persona/role/goal, success condition, entry points, happy path, alternate paths, and decision/branch rules — with **no step list and no status field**, and STOPs with the terminal handoff (below). Each spec session then reads the brief and scans which `{section-id}.md` files exist under `design/{slug}/user-flow-map-{topic}/`, fills the first missing section in order — `surface-inventory` (sub-step 6, with visual UI candidate notes from sub-step 10), `action-state-matrices` (sub-step 7), `failure-recovery` (sub-step 8), then `handoffs` (sub-step 9) — to its intermediate path, appends any cross-section facts to the brief, and STOPs with the terminal handoff. In non-chunked mode, run all sub-steps below in one continuous session as before.

Every chunked STOP (setup and each spec session) must emit the **Terminal handoff format** from `DESIGN-TREE-LOOP.md`: state the intermediate just written, name the next missing section in **plain English** — never only the internal `{section-id}` (e.g. write "Next section: **action–state matrices** — the per-surface matrix of actions, navigation, validation, channel behavior, and state coverage for each surface in the inventory," not "continue with `action-state-matrices`") — and give the **exact** resolved next tool or command call with `{slug}`/`{topic}` filled to literal values, e.g. `$user-flow-map alignment-page-review` writing into `design/alignmeant/user-flow-map-alignment-page-review/action-state-matrices.md`. The setup STOP names the first section (`surface-inventory`) and its command. When the section just written was the last one (`handoffs`), the handoff points to the assemble+approve session instead of another spec session. Continue-vs-stop framing follows that convention's Routing Rules — do not restate it.

1. Define the primary persona, goal, success condition, and triggering context.
2. List every entry point and precondition.
3. Write the happy path as ordered steps with the surface and channel used by each step.
4. List alternate paths, including optional setup, skip paths, backtracking, cancellation, save-for-later, review/edit, and escalation.
5. List decision points and branch rules. Distinguish user decisions, system decisions, permissions decisions, and external/manual decisions.
5a. Order `branches[]` by journey progression by default when turning named flows into manifest branches. Record any explicit user branch-order override before writing deliverables.
6. Create a Surface Inventory with purpose, surface type, channels, visual UI candidate, inputs, outputs, source evidence, and downstream destination.
7. For each surface, list required actions, available navigation or channel affordances, disabled/blocked rules, validation rules, channel-specific behavior, state coverage, and audit/observability needs.
8. Map failures and recovery: invalid input, no data, permissions, lost connection, backend failure, timeouts, interrupted work, and contradictory user choices.
9. Map handoffs across roles, devices, systems, documents, notifications, approvals, payments, support, or manual operations.
10. Add low-fidelity wireframe notes only for visual UI candidate surfaces: rough regions, primary/secondary content, key controls, data groupings, progressive disclosure, and fixed/sticky elements only when structurally necessary. For non-visual surfaces, capture response, event, validation, or audit-record shape instead.

### 4. Coverage Checkpoint

**Chunked-mode assemble+approve session (step 0c).** When chunked mode is active, begin this session only once every section's `{section-id}.md` intermediate exists under `design/{slug}/user-flow-map-{topic}/`. Assemble those per-section intermediates plus the brief into the canonical flow map (the deliverables below), run this coverage checkpoint over the whole assembled flow, and build the **one** alignment page. On approval, update the scoped flow-tree manifest branch state and archive the brief and per-section intermediates per the convention's archive-at-canonical-write timing. There is exactly one alignment gate for the whole flow, not one per section.

Before writing deliverables, present a **Flow Coverage Checkpoint** inline as the final message text of its own turn (never only as mid-turn text before a tool or command call):

- Persona and goal covered.
- Entry points covered.
- Happy path covered.
- Branches and decision points covered.
- Surface inventory covered.
- Actions, states, and channel behavior per surface covered.
- Required states covered.
- Failure/recovery paths covered.
- Handoffs covered.
- Visual UI candidate notes or non-visual response/event/audit shapes covered.
- Layout/styling non-goals preserved.

In the next turn, ask whether any flow branch, state, or handoff is missing before writing.

### 5. Prototype Build-Plan Synthesis Mode

When invoked with `--prototype-build-plan`, "prototype build plan", "prototype todo", or equivalent wording, run this mode after the normal flow/UX/UI branch work exists:

1. Read the scoped `design/**/flow-tree-*.yaml`, `design/user-flow-*.md`, `design/ux-variations-*.md`, and `design/ui-*.md` artifacts.
2. Identify every user-flow branch, UX variation branch, and UI experiment branch with an approved or retryable decision.
3. Create one prototype build item for each approved UI experiment that should be made tangible in `$logic-wiring`.
4. Mark rejected branches as dropped and do not include them as buildable items unless the user explicitly overrides.
5. Mark out-of-scope, expensive, or low-confidence branches as deferred when the user chooses not to prototype them now.
6. Mark branches that need design or UI correction before prototyping as needs-revision.
7. Preserve user overrides, including building from a concept-only root when the user explicitly bypasses missing research.
8. Produce a build sequence that keeps the work lightweight and independently reviewable; each item should be small enough for `$logic-wiring --variant N` to build or rebuild.

Before writing the build plan, present a **Prototype Build Plan Checkpoint** as the final message text of its own turn. Include:

- Build items to prototype now.
- Items that need revision before prototyping.
- Items deferred or dropped, with rationale.
- Source user-flow branch, UX variation, and UI experiment IDs for each item, including the manifest `ui_experiment_id`.
- Expected prototype path for each buildable item.
- Any user overrides or research gaps carried into the plan.

Ask the user to confirm, correct, defer, or drop items before writing the build plan.

## Deliverables

Write:

- `design/user-flow-[topic].md` in flat mode or `design/{slug}/user-flow-[topic].md` in product-path mode.
- `design/user-flow-[topic]-interview.md` in flat mode or `design/{slug}/user-flow-[topic]-interview.md` in product-path mode.
- `design/flow-tree-[topic].yaml` in flat mode or `design/{slug}/flow-tree-[topic].yaml` in product-path mode.

In prototype-build-plan mode, write instead:

- `design/prototype-build-plan-[topic].md` in flat mode or `design/{slug}/prototype-build-plan-[topic].md` in product-path mode.
- Update `design/flow-tree-[topic].yaml` in flat mode or `design/{slug}/flow-tree-[topic].yaml` in product-path mode with `prototype_build_plan.artifacts[]` and `prototype_build_plan.items[]`.

The user-flow spec must include:

- Scope, source evidence, and assumptions checkpoint.
- Persona, goal, and success condition.
- Entry points and preconditions.
- Happy path.
- Alternate paths and branches.
- Decision-point table.
- Surface Inventory with `surface type`, `channels`, and `visual UI candidate`.
- Action/state matrix by surface.
- Failure and recovery paths.
- Handoffs and external/manual dependencies.
- Low-fidelity wireframe notes for visual UI candidate surfaces, plus response/event/audit-shape notes for non-visual surfaces.
- Open questions, risks, and explicit non-goals.
- Downstream handoff choices for `$ux-variations [specific-user-flow]`.
- Flow-tree manifest branch IDs and artifact references.
- Ordered branch table showing journey stage, journey sequence, priority rationale, first value moment, primary task path, and progressive review sequence for each `branches[]` entry.
- Record explicit user branch-order overrides in `design/user-flow-[topic].md`, including the requested order, rationale, affected branch IDs, and whether the override changes first-value or activation review order.

The interview log must include:

- Evidence consulted.
- The Flow Assumptions Checkpoint and user corrections.
- Questions asked, options presented, recommendations, and user responses.
- Flow Coverage Checkpoint and remaining gaps.
- Record explicit user branch-order overrides in `design/user-flow-[topic]-interview.md`, including the question or checkpoint where the override was captured and any rejected default ordering.

The prototype build plan must include:

- Scope, source evidence, and user overrides.
- Build item table with `id`, source user-flow branch, source UX variation, source UI experiment, `ui_experiment_id`, status, expected prototype path, and rationale.
- Status definitions: `pending`, `built`, `needs-revision`, `deferred`, and `dropped`.
- Build sequence and chunking notes for `$logic-wiring --variant N`.
- Revision/defer/drop rationale for branches not ready to build.
- Flow-tree manifest build item IDs and artifact references.

After approved files are written, hand off instead of auto-running or auto-invoking the next skill. How you hand off depends on how the approval YAML was consumed:

- **Same session that built the page** (the page-building conversation is still in context): present a two-option choice — (1) Stop here so the user can clear context and run `$state-model [topic]` (recommended) or `$ux-variations [specific-user-flow]` in a fresh session, or (2) Continue immediately in this session with `$state-model [topic]` to author the logical domain model before variation work, or `$ux-variations [specific-user-flow]` for the first unresolved user-flow branch when the domain is trivial.
- **Already-fresh session** (the page-building conversation is not in context — e.g. the user cleared context and pasted the compiled approval YAML to start this session): there is no accumulated build context to shed, so do not present or recommend another context clear. Default to continue-now — invoke `$state-model [topic]` (recommended) to author the logical domain model before variation work, or `$ux-variations [specific-user-flow]` for the first unresolved user-flow branch when the domain is trivial, and immediately enter its first required interaction gate. The user may still choose to stop.

After approved prototype-build-plan files are written, route to `$logic-wiring [topic]` or `$logic-wiring [topic] --variant N` for the first pending build item. Do not route to `$logic-wiring` before the build plan exists unless the user explicitly accepts an untracked ad hoc prototype run.

If the user chooses to continue immediately, the next skill must still execute its own required interaction gates. `user-flow-map` approval authorizes the wireframe-tree root and provides source evidence; it does not approve any UX variation branch, visual mockup, UI proposal, or implementation path, and it does not count as `ui-interview` interview completion.

## Interrogation Page

Before producing research, run the stage-zero interrogation loop following `INTERROGATION-PAGE.md` in this skill's directory. Build one HTML page per round at `interrogation/user-flow-map-r{N}-{branch}.html`, starting with the assumptions manifest as round 1, and loop until the confidence gate passes. This skill **cannot advance to stage one until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. Each round page must contain at least one genuinely open input (`data-open-input`).

## Next Work

**Next work:** after the flow map is approved, author the flow-anchored logical domain model with `$state-model [topic]` (optional sibling), or grow the first unresolved user-flow branch with `$ux-variations [specific-user-flow]` when the domain is trivial. In prototype-build-plan mode, the next work is the first pending build item via `$logic-wiring [topic]`. Name the next pending branch in plain English in the handoff; never route by internal `{branch-id}`.

**Recommended next command:** `$state-model [topic]` (or `$ux-variations [specific-user-flow]`).

## Invoke With YAML

Emit the `agent_routing` payload with the exact resolved next-invocation command, `{slug}`/`{topic}`/branch filled to literal values:

- Default: `$state-model [topic]`, then `$ux-variations [specific-user-flow]`.
- Build-plan mode: `$user-flow-map --prototype-build-plan [topic]` → `$logic-wiring [topic]`.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/user-flow-map-{topic}.html`.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/design/spec document (`research/**/*.md`, `design/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.

## Constraints

- Keep this skill before UX variation, UI layout, and prototype work in the AFPS route.
- Do not produce high-fidelity mockups, component styling, color palettes, design systems, production architecture, database schemas, or implementation plans.
- Do not collapse branches or states into generic "standard flow" language. Name each branch/state or mark it explicitly out of scope.
- Do not route directly to `$ui-interview` from an approved flow map unless the user explicitly bypasses variation exploration for a named flow. The normal route is `$user-flow-map` -> `$state-model [topic]` (optional sibling) -> `$ux-variations [specific-user-flow]` -> `$ui-interview [specific-ux-variation]`. `$state-model` authors the flow-anchored logical domain model and writes only an optional `model_tree_ref` pointer into the flow tree; it never alters the flow-tree `route` array.
- Do not write pre-prototype flow maps to `specs/`. `design/` is the canonical home for flow maps, UX variation plans, UI branch packets, branch decisions, mockup references, and flow-tree manifests.
- Do not auto-run or auto-invoke downstream skills after approval. When consuming the approval YAML in the same session that built the page, present the stop/clear-context versus continue-now choice; when consuming it in an already-fresh session (no build context to shed), default to continue-now without prompting another context clear. Either way, preserve the next skill's required gates — continue-now means invoking the next skill and immediately entering its own interaction gates under user control, not running it unattended.
- Do not treat `design/ux-variations-*.md` as the prototype todo list once branch decisions exist. Use prototype-build-plan mode to create the explicit ledger before `$logic-wiring`.
- Do not use `tasks/todo.md` for design/prototype branch progress. Human prototype evaluation belongs in `tasks/manual-todo.md`; implementation fixes may enter `tasks/todo.md` only after human evidence exists.
- When recommending a skill from another pack, verify pack availability through `.agents/project.json.enabled_packs`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
