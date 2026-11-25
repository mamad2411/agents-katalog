---
name: feature-interview
description: Interview a feature idea with evidence-backed alignment, then decide whether to create/update docs, specs, roadmap, or tasks
type: planning
version: v0.7
required_conventions: [alignment-page]
argument-hint: "[feature idea or tasks/ideas.md entry]"
context_intake: deep
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Feature Interview

Invoke as `$feature-interview`.

Use this skill when the user has a feature idea, brainstorm suggestion, research gap, bug-shaped improvement, or implementation direction that needs evidence-backed alignment before deciding whether to write or update research docs, journey docs, specs, roadmap entries, task queues, or route directly to another planning skill. This skill is also the primary entry point for post-ship feature work, where scope determines the re-entry depth into the pipeline.

This is narrower than `$spec-interview`: it performs the same assumption surfacing and deep interview needed for human/agent alignment, but it does not assume the output must be a full new implementation spec. It borrows `$investigate`'s evidence discipline for claims, codebase fit, and technical gotchas, but it does not fix bugs or implement the feature.

Use `$feature-interview` especially after a production spec already exists and the user wants to add, adjust, or triage a smaller feature. In post-spec use, treat existing specs as the baseline contract: prefer a scoped add-on spec or a tightly bounded update to an existing spec over re-running `$spec-interview` for the whole product. Only route to `$spec-interview` when the existing spec is absent, obsolete, or too incomplete to support the new feature decision.

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

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

1. Resolve the feature input:
   - If `$ARGUMENTS` names or quotes an idea, use it as the seed.
   - If `$ARGUMENTS` references `tasks/ideas.md`, read matching entries and ask the user to choose one when multiple entries match.
   - If no feature is provided, read `tasks/ideas.md` and present the top unspecced candidates; ask the user which one to interview.
2. Gather context before asking deep questions:
   - Read `.agents/project.json`, CLAUDE.md or AGENTS.md, README, package config, and key source files relevant to the idea.
   - Read `research/.progress.yaml` when present. Treat product-path entries as product/app/ICP divergence state, not git branches.
   - Read `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, `tasks/recurring-todo.md`, `tasks/history.md`, and `tasks/ideas.md` when they exist.
   - Read existing specs from `specs/`, `spec.md`, or `docs/specifications/`, plus relevant research docs such as ICP, journey map, competitive analysis, customer feedback, metrics, and MVP gap artifacts.
   - Read git evidence (`git log`, `git diff`, `git blame`) only where it can confirm related prior decisions, recent regressions, ownership, or why the current system shape exists.
   - Avoid re-interviewing on facts already covered by current concept, research, journey, UX, UI, or spec docs.
3. Run an evidence-backed intake pass before deciding what to ask:
   - Extract the user's explicit claims, hypotheses, constraints, and desired outcomes. Do not treat a desired outcome as a factual claim.
   - Validate factual claims against code, docs, research, task state, and git history. Classify each as `confirmed`, `partially supported`, `not supported`, or `unknown / needs user context`.
   - Identify likely technical gotchas: architecture fit, shared modules, data model, API/contracts, migrations, security/privacy, permissions, performance, observability, tests, rollout, external dependencies, and backwards compatibility.
   - Identify how the feature fits into the user story, customer journey, developer workflow, game loop, or other project-specific journey artifact. If no credible journey exists for user-facing work, flag that as a planning gap.
   - For new user-facing product, SaaS, marketplace, dashboard, internal tool, product-experience work, or substantial new feature work, add a prototype-first gate to the intake: default the first build artifact to a clickable local/static prototype with fake, fixture, or in-memory data unless the user explicitly opts into production infrastructure or the core interaction cannot be tested without it. Treat durable storage, auth, payments, analytics, deployment, admin tooling, multi-tenancy, and production observability as deferred infrastructure decisions until the prototype calibrates taste, feel, workflow density, and one accepted journey.
   - When the feature direction is uncertain, recommend multiple route-based experiments instead of one over-specified implementation. Name the routes or route pattern, such as `/experiments/table-first`, `/experiments/board-first`, or the project's equivalent, and identify the hypothesis each route tests.
   - If those route experiments imply materially different products, apps, ICPs, or product lines rather than alternative UX for the same product path, record them in `research/.progress.yaml` as `product_paths[]` with `id`, `label`, `source_skill: feature-interview`, `scope_path`, `status: deferred` or `status: revisit_candidate`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `pipeline_stage: feature-interview`, and `last_touched`.
   - Identify whether research docs, journey docs, specs, roadmap, or task queues need a durable update if the feature proceeds.
4. Match the feature against existing planning artifacts:
   - Identify whether the repo is in a post-spec state: one or more credible `specs/*.md`, `spec.md`, or `docs/specifications/*.md` files already define the product or area this feature extends.
   - Identify whether the feature is already fully represented in an existing spec, partially represented in a spec, should become a scoped add-on spec, is only present as an idea/research gap, or is already sequenced in the roadmap.
   - In post-spec state, default to `update existing spec` or `new smaller-scope add-on spec` as the planning destination. Do not discard the existing spec baseline or route back to full `$spec-interview` unless the existing spec is stale, contradicted, or missing the product area needed to make the decision.
   - If it duplicates planned work, stop and recommend the existing route (`$roadmap`, `$plan-phase N`, `$exec`, or `$ship`) with evidence.
5. Present a **Feature Evidence Brief + Assumptions Manifest** before probing:
   - Evidence sources: files, docs, research artifacts, task docs, and git history consulted.
   - Claim validation: verdict for each factual claim or hypothesis, with concise evidence.
   - Technical gotchas: likely integration risks, operational risks, unknowns, and what would break if each assumption is wrong.
   - Journey placement: where this feature belongs in the user story, journey map, workflow, or loop; note missing or conflicting journey evidence.
   - Documentation destination: likely `new spec`, `update existing spec`, `update research/journey docs`, `roadmap/task update`, `interview log only`, `run another planning/research skill first`, or `no action`.
   - Source context: idea/research/spec/roadmap inputs used.
   - Human intent: what outcome the user appears to want and who benefits.
   - Agent interpretation: the concrete capability or change the agent would plan from the input.
   - Existing-system fit: code paths, specs, tasks, and research artifacts likely affected.
   - Post-spec fit: whether the feature extends an existing spec, needs a smaller-scope add-on spec, updates research/journey docs first, or is already covered.
   - Planning destination: likely `update existing spec`, `new smaller-scope add-on spec`, `new full spec`, `roadmap/task update`, `research/design skill first`, or `no new planning needed`.
   - Priority hypothesis: recommended priority relative to current roadmap/todo, with dependency and risk rationale.
   - Implementation shape: product behavior, design/UX needs, data model, APIs/contracts, migrations, tests, operations, and rollout surface as far as they can be inferred.
   - Prototype-first gate for product and feature work: state whether the next artifact should be `multiple route experiments`, `single clickable prototype`, `production implementation`, or `research/spec only`. If there is no accepted prototype or user-approved infrastructure opt-in, recommend route experiments or a clickable prototype and explicitly defer database/storage, auth, payments, analytics, deployment, admin tooling, multi-tenancy, and production observability.
   - Risks and unknowns: ambiguity, integration risk, user-facing risk, external dependencies, and what breaks if the assumption is wrong.
   Tag each assumption with `[from idea]`, `[from spec]`, `[from codebase]`, `[from research]`, `[from roadmap]`, `[from git]`, or `[inferred]`.
   Deliver the brief and manifest inline as the final message text of their own turn; ask the step 6 confirmation in the next turn. Never emit the brief only as mid-turn text in a turn that ends with a tool or command call — harness rendering does not guarantee mid-turn text is shown.
6. In the turn after the brief is shown, ask the user to confirm, correct, or flag the evidence brief, claim verdicts, assumptions, journey placement, documentation destination, and priority hypothesis before continuing. Do not proceed past this checkpoint until the user has reviewed it. A confirmation question must never reference content the user has not been shown.
7. Interview in focused passes. Codex interview cadence is one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same decision, not to batch unrelated questions. If the session is already in Plan mode and there are 2-3 concrete options for the current decision, prefer `request_user_input`; otherwise ask one concise direct question.
8. Cover only the areas needed to choose and prepare the planning destination:
   - Intent and success criteria.
   - Target users, jobs, and journey/design implications.
   - Feature behavior and scope boundaries.
   - Existing spec fit: whether to create a new spec, update an existing spec, or split the work.
   - Implementation constraints: architecture, data model, API/contract surface, migrations, security, privacy, performance, observability, test strategy, and rollout.
   - Research and journey implications: whether canonical research, journey, UX, UI, or customer/developer docs need updates.
   - Roadmap coupling: dependencies, phase fit, priority, ordering, parallelization, manual blockers, and the smallest useful implementation slice.
9. Research and recommend by default. Use codebase evidence, existing docs, and web search when the decision depends on current external facts. Present options with pros/cons, state a recommendation, and ask the user to approve, adjust, or override.
10. Before concluding, present a **Planning Destination + Priority Checkpoint**:
   - Decision: update existing spec, create a new smaller-scope add-on spec, create a new full spec, update research/journey docs, update roadmap/tasks only, run another named planning/research skill first, interview log only, or no action.
   - Target artifact path(s).
   - Existing spec relationship: the parent spec or product-area spec this feature extends, supersedes, or leaves unchanged.
   - Journey/workflow placement to record.
   - Scope to include now and explicitly defer.
   - For user-facing product or feature work, confirm the prototype-first decision: what users can click through first, whether multiple experiments should live on separate routes, what data can be fake or fixture-backed, which infrastructure is intentionally deferred, and what evidence would justify promoting one deferred infrastructure item into a later production phase.
   - Scope triage for post-ship features:
     - Small (config, copy, toggle) → `$spec-interview` + `$exec` directly
     - Medium (new component, screen, workflow) → single-variation mini-prototype (`$prototype --variant 1`)
     - Large (new product area, major redesign) → full pipeline starting at `$ux-variations`
   - Priority decision: user-confirmed priority, dependencies, and whether the feature should interrupt, follow, or remain parked relative to current roadmap/todo work.
   - Roadmap/task impact and recommended next command.
   Deliver the checkpoint inline as the final message text of its own turn; in the next turn, ask: "Does this destination, priority, and scope match what you want?"

## Deliverables

After confirmation, write the minimum durable artifact needed:

- New spec: write `specs/[topic].md` using the `$spec-interview` canonical section headings.
- Add-on spec: write `specs/[parent-topic]-[feature-topic].md` or the repo's equivalent scoped path. State the parent spec it extends, the inherited assumptions, what is intentionally out of scope because the parent spec already owns it, and the exact integration points back to the parent.
- Existing spec update: archive the existing canonical spec first, then update only the relevant sections.
- Research or journey update: archive the existing canonical research/journey document first when replacing or substantively rewriting sections, then make the smallest scoped update. If the missing research requires a named skill, write the interview log and recommend that skill instead of inventing unsupported research.
- Roadmap/task-only change: update `tasks/roadmap.md`, `tasks/todo.md`, `tasks/record-todo.md`, or `tasks/manual-todo.md` only when no spec/research change is needed and the user has confirmed priority.
- Upstream planning/research needed: write an interview log and recommend the named skill instead of inventing a placeholder spec.
- No action: write an interview log explaining why the idea is already covered, duplicate, deferred, or intentionally parked.
- Product path divergence: update `research/.progress.yaml` with `id`, `label`, `source_skill`, `scope_path`, `status`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `pipeline_stage`, and `last_touched`; do not force all divergent paths through downstream research.

Always write an interview log to `specs/[topic]-feature-interview.md` (or `docs/specifications/[topic]-feature-interview.md` if that is the repo's canonical spec location). Include:

- Artifact path: the exact path of this interview log.
- The Feature Evidence Brief and Assumptions Manifest with user corrections.
- Claim validation verdicts and evidence.
- Technical gotchas, mitigations, and unresolved unknowns.
- Journey/user-story/workflow placement and any research or journey doc changes needed.
- Questions asked and answers received.
- Options and recommendations presented.
- Planning Destination + Priority Checkpoint and confirmed decision.
- Post-spec relationship: parent spec, add-on spec path, or updated spec section, including why this path is smaller and safer than re-running full `$spec-interview`.
- The exact next command for sequencing.

When replacing or substantively rewriting an existing canonical research/spec document (`research/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>` before editing it.

### Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/feature-interview-{topic}.html`.

## Constraints

- Do not default to a new spec when an existing spec should be updated.
- Do not route post-spec feature additions back to full `$spec-interview` by default. Use `$feature-interview` to create a scoped add-on spec or update the existing spec unless the baseline spec is missing or unfit.
- Do not update roadmap or task sequencing until the planning destination and priority are confirmed by the user.
- Do not produce a full implementation spec unless the interview proves a new or rewritten spec is the right destination.
- Do not route brainstorm ideas directly to `$spec-interview`; use `$feature-interview` for triage unless the user explicitly asks for a full spec.
- Do not implement fixes or feature code from this skill. If the evidence pass uncovers a bug, route to `$investigate`; if it uncovers buildable planned work, route through `$roadmap`, `$plan-phase`, or `$exec`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
