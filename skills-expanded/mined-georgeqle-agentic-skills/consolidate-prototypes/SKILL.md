---
name: consolidate-prototypes
description: Converge evaluated prototype branches into one approved MVP, resolve UAT findings, hand off to post-prototype research, and let spec-interview own production-ready approval
type: planning
version: v0.21
required_conventions: [alignment-page, design-tree-loop, interrogation-page]
argument-hint: "[optional: topic, page, or path to variation specs]"
visual_tier: prototype
---

# Consolidate Prototypes

Invoke as `$consolidate-prototypes`.

Use this skill after the user has built and evaluated prototype branches (typically generated via `$ux-variations --layout-mode`, built via `$build-ui-screens` then `$logic-wiring`, and evaluated via `$uat --variant-evaluation`; if `uat` is not directly available in the active skill list/session, install the providing pack with `npx skillpacks install product-testing`, then run `$uat --variant-evaluation`). This skill compares the source prototypes, interviews the user on what works and what does not in each one, resolves incompatible UAT findings and design choices, and produces a single user-approved consolidated MVP for post-prototype production specification. A single-variant MVP is allowed only when UAT evidence exists and the user explicitly chooses that convergence scope while excluding, deferring, or marking all other approved branches as spec-only references.

**Two-stage consolidation.** Consolidation runs in two stages. **Stage 1 — stitch** assembles the approved canonical screens into coherent end-to-end flows: it reads each variation's built screens and walks the `ui_experiments[].build_ledger[]` entries, and **cherry-picks** screens flagged `cherry_pick_candidate` or left `parked` by `$build-ui-screens` (a strong partial screen worth carrying into the canonical flow even though its source variation was not the winner). It also compares any Platform Fit Workshop `platform_probe` evidence against `platform_fit.recommendation`. **Stage 2 — converge** is the existing pass: interview keep/reject across the stitched flows, resolve conflicts, build the consolidated MVP, write the AFPS graduation document with the recommended platform strategy, and hand off to `$research-roadmap --post-prototype`.

Users with manually built prototypes can also use this skill directly, but consolidation should not happen before the user has reviewed the prototypes and captured evidence.

Follow `DESIGN-TREE-LOOP.md` for prototype-phase routing, state storage, approval boundaries, and task classification. Consolidation requires UAT evidence plus explicit consolidation decisions before writing `prototypes/{topic}/consolidated/`; explicit user readiness cannot bypass a `Not run` result log or unhandled approved but unbuilt/deferred branch.

## Pack Availability Guard

Before routing missing or unreviewed evaluation evidence to `$uat --variant-evaluation`, check whether `uat` is directly available in the active skill list/session. If it is unavailable, identify `uat` as provided by the `product-testing` pack and tell the user to run `npx skillpacks install product-testing`, then `$uat --variant-evaluation`. If `$uat` remains unavailable after install, tell the user to start a fresh Codex CLI session and retry `$uat --variant-evaluation`. Do not tell users to install the `uat` skill directly.

## Design-Tree Flow

This skill runs the unified **5-stage design-tree flow** (`interrogation → research → design → plan → implement(scoped)`) from `DESIGN-TREE-LOOP.md`, converging the validated tree into a cohesive **MVP**. The `## Process` steps below group by stage:

- **Stage 0 — Interrogation**: the stage-zero loop in `## Interrogation Page` / `INTERROGATION-PAGE.md` plus the prototype-selection checkpoint — confirm which evaluated prototype branches to consolidate and the UAT evidence backing each.
- **Stage 1 — Research**: read the built prototypes, platform probes, `design/ux-variations-[topic].md`, `design/ui-requirements-[topic].md`, `design/flow-tree-[topic].yaml`, and the `$uat --variant-evaluation` evidence.
- **Stage 2 — Design**: interview keep/reject per prototype branch, resolve conflicts, and decide the consolidated MVP direction.
- **Stage 3 — Plan**: the keep/reject/resolve matrix is the build-plan slice this run realizes.
- **Stage 4 — Implement (scoped)**: **runnable** — build the consolidated MVP under `prototypes/{topic}/consolidated/`, mark the tree `consolidated`, record the consolidated MVP decisions, and pass the single binding alignment gate before any canonical write.

**Per-branch iteration contract.** Each session cold-starts, reads the flow-tree manifest, resolves the validated variation set ready to converge, runs the staged flow, writes the consolidated MVP on approval, and stops with the handoff in `## Next Work`.

**Modify-back.** When consolidation surfaces a flaw in an upstream node, record a `modify` decision whose `targets[]` re-opens that `model_ref`, `platform_fit`, or user-flow branch; convergence resumes once the re-opened node is re-approved.

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

When product path `{slug}` is active, read research under `research/{slug}/`, read pre-prototype design artifacts under `design/{slug}/`, write prototype output under `prototypes/{topic}/`, and treat top-level `research/*.md` and `design/*.md` files as flat-mode documents or cross-path summaries.

1. **Resolve context**
   - Read `.agents/project.json` if it exists.
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `research/`, route files, component directories, and design artifacts when present.
   - Locate the prototype branch plan: `design/ui-layout-variations-[topic].md`, `design/ux-variations-[topic].md`, or equivalent prototype-branch plan.
   - Locate the content requirements: `design/ui-requirements-[topic].md` or equivalent content contract.
   - Locate the flow-tree manifest: `design/flow-tree-[topic].yaml` or `design/{slug}/flow-tree-{topic}.yaml` when present.
   - Read `platform_fit` and any `prototype_build_plan.items[].platform_probe` evidence from the flow-tree manifest and build plan.
   - Locate variant evaluation evidence: `research/uat-variant-evaluation-[topic].md`, product-path-scoped equivalents, `research/uat-plan.md` result logs, screenshots, notes, recordings, or explicit user-provided review notes.
   - Locate built implementations: scan route files, component directories, and any prototype-specific directories or branches.
   - If the prototype branch plan or implementations cannot be found, ask the user to point to them.

2. **Evidence gate**
   - If no evaluation evidence exists and the user has not explicitly said they already reviewed the variants and is ready to converge, stop and recommend the Pack Availability Guard handoff: if `uat` is not directly available in the active skill list/session, run `npx skillpacks install product-testing` from the project shell, then run `$uat --variant-evaluation`; if `$uat` remains unavailable after install, start a fresh Codex CLI session and retry `$uat --variant-evaluation`.
   - Stop if `research/uat-variant-evaluation-[topic].md` or a product-path equivalent says `not ready`, includes unchecked items in the "Ready for `$consolidate-prototypes`?" checklist, or contains only `Not run`, skipped, deferred, or spec-only result logs with no captured evidence.
   - Stop while any built MVP-scope branch has `Status: Not run`; route back to manual UAT/evidence capture through `$uat --variant-evaluation`.
   - Do not infer a winner from specs alone. Built variants need hands-on review evidence before consolidation.
   - If approved UX/UI variants are unbuilt or deferred, require an explicit user decision before consolidation: exclude/defer them from MVP scope, build/evaluate them first, or include them only as spec references.
   - If no explicit decision exists for approved unbuilt/deferred branches, use the conservative default: stop and route back to the next approved unbuilt UX branch, for example `$ui-interview uxv-alignment-page-review-change-first-revision-workspace`, or to the specific next branch named by the flow-tree manifest.
   - If some prototype branches are unreviewed, ask whether to exclude them, evaluate them first via the Pack Availability Guard handoff (`npx skillpacks install product-testing` if `uat` is not directly available, then `$uat --variant-evaluation`; fresh Codex CLI session and retry if `$uat` remains unavailable), or include them as spec-only references.

3. **Present prototype inventory**
   - List each source prototype branch with a one-line summary of its approach.
   - Note build status for each: built and reviewed, built but unreviewed, partially built, spec-only.
   - Note evidence status for each: result log present, user notes present, no evidence.
   - Note scope handling for every approved branch: evaluated in MVP scope, explicitly excluded from MVP, deferred from MVP, spec-only reference, or build/evaluate first.
   - Note platform-probe status for each serious platform candidate: built and evidenced, built but unevaluated, missing, deferred, rejected.
   - Confirm which prototype branches the user wants to consolidate.

4. **Interview per prototype branch**
   - For each reviewed prototype branch, ask one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same branch decision, not to batch unrelated questions:
     - What works well in this prototype? Name specific elements, regions, or interactions.
     - What does not work? What feels wrong, cluttered, sparse, or confusing?
     - Any specific component, region, or interaction to keep in the final design?
     - Anything to explicitly reject and never use?
   - Record responses as structured annotations per source prototype:
     - **Keep**: elements the user wants in the final MVP, with source prototype
     - **Reject**: elements the user never wants, with source prototype
     - **Neutral**: elements the user has no strong opinion on

5. **Cross-prototype synthesis**
   - Present a **Consolidation Matrix** showing each design dimension and which prototype branch's approach the user preferred:

   | Design Element | Prototype A | Prototype B | Prototype C | Winner |
   |---|---|---|---|---|
   | Container pattern | card grid | data table | list + detail | ? |
   | Detail view | modal | sidebar | full-page | ? |
   | Navigation | top nav | side nav | tabs | ? |

   - Fill in winners based on UAT evidence and interview responses.
   - Mark conflicts where preferred choices from different dimensions are incompatible.
   - For each conflict, present the tension, offer 2-3 resolution options with tradeoffs, state a recommendation, and ask the user to resolve it.
   - Continue until every row in the matrix has a winner and all conflicts are resolved.

5a. **Platform-probe synthesis**
   - Compare Platform Fit Workshop candidates, `platform_fit.recommendation`, and any platform-probe evidence.
   - Confirm the platform strategy as `primary`, optional `companion[]`, `defer[]`, and `reject[]`.
   - If platform-probe evidence contradicts the current recommendation, either update the recommendation in the flow-tree manifest or record a `modify` decision targeting `platform_fit` and route back to `$user-flow-map`.
   - Do not graduate with unresolved platform risks that materially affect production architecture, permissions, distribution, monetization, or adoption path.

6. **Build consolidated prototype**
   - Merge the best elements from source prototypes into a single runnable artifact at `prototypes/{topic}/consolidated/`.
   - Build only after UAT evidence and user consolidation decisions identify which elements to keep, reject, or resolve.
   - The consolidated prototype must reflect:
     - Layout skeleton: regions, proportions, scroll behavior
     - Primary content pattern
     - Detail view pattern
     - Navigation pattern and placement
     - Action placement
     - Density and spacing approach
     - Responsive behavior at mobile, tablet, and desktop breakpoints
     - States rendering
   - Ask the user to confirm the consolidated design before building the prototype.

7. **Coverage checkpoint**
   - Verify every content requirement from `design/ui-requirements-[topic].md` has a UI home in the consolidated prototype.
   - Verify every user action has a placement: button, menu item, keyboard shortcut, or gesture.
   - Verify all states are accounted for: empty, loading, error, partial, full, offline, permission-denied.
   - Flag any gaps and resolve them before writing.

8. **Production-ready handoff boundary**
   - Write the required AFPS graduation document at `design/afps-graduation-{topic}.md` in flat mode or `design/{slug}/afps-graduation-{topic}.md` in product-path mode.
   - Record final MVP decisions, rejected alternatives, UAT evidence, platform-probe evidence, recommended platform strategy, unresolved risks, stale-research cleanup needs, and production-spec readiness in the consolidation interview log, AFPS graduation document, and alignment page.
   - The recommended next route must name `$research-roadmap --post-prototype`, then `$spec-interview`.
   - The Production Ready Approval gate is owned by `$spec-interview` and follows `docs/production-ready-approval.md`.

## Deliverables

- Write the consolidated prototype to `prototypes/{topic}/consolidated/`.
- Write the consolidation interview log to `design/consolidate-prototypes-[topic]-interview.md` in flat mode or `design/{slug}/consolidate-prototypes-[topic]-interview.md` in product-path mode.
- Write the AFPS graduation document to `design/afps-graduation-{topic}.md` in flat mode or `design/{slug}/afps-graduation-{topic}.md` in product-path mode. Include the approved MVP scope, prototype evidence, platform-probe evidence, recommended platform strategy, keep/reject decisions, unresolved risks, stale-research cleanup status, and whether the project is ready for `$research-roadmap --post-prototype` and `$spec-interview`.
- Update the scoped flow-tree manifest to mark consolidated branches as `consolidated` or `promoted-to-prototype` when applicable.

### Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/consolidate-prototypes-{topic}.html`.

## Next Work

**Next work:** after the consolidated MVP and AFPS graduation document are approved, run the post-prototype research pass (`$research-roadmap --post-prototype`) and then formalize the MVP into a production spec with `$spec-interview`. The Production Ready Approval gate is owned by that spec handoff; do not create a separate production-readiness state file or lifecycle registry here.

**Recommended next command:** `$research-roadmap --post-prototype`.

## Invoke With YAML

Emit the `agent_routing` payload with the exact resolved next-invocation command, `{slug}`/`{topic}` filled to literal values: `$research-roadmap --post-prototype`, then `$spec-interview`.

## Constraints

- Do not proceed without UAT evidence, and do not treat explicit readiness as sufficient when the UAT file says not ready, has unchecked readiness items, or contains only `Not run`/deferred/spec-only logs.
- Do not proceed while approved UX/UI variants remain unbuilt or deferred unless the user explicitly excludes or defers them from MVP scope, chooses to build/evaluate them first, or includes them only as spec references.
- Do not proceed with a single-variant MVP unless the user explicitly chooses single-variant convergence from the current built set and records how every other approved branch is excluded, deferred, or treated as spec-only.
- Do not pick winners without user input. Present the matrix and let the user decide.
- Do not ignore conflicts. If two preferred choices are spatially or functionally incompatible, surface the tension and resolve it explicitly.
- The consolidated prototype must preserve the approved UI branch detail from `$ui-interview`, carry the recommended platform strategy from AFPS graduation, and be concrete enough for `$spec-interview` to extract production implementation requirements and own the Production Ready Approval described in `docs/production-ready-approval.md`.
- Do not lose content requirements. Every data field, action, and state from the requirements spec must appear in the final design.
- Do not bias toward the first or last variation reviewed. Present them neutrally and let the user's feedback and evaluation evidence drive the outcome.
- Do not use `tasks/todo.md` for consolidation branch progress or human review. Human evaluation belongs in `tasks/manual-todo.md`; implementation fixes may enter `tasks/todo.md` only after human evidence exists.

## Archive-First Replacement Policy

- Before replacing or substantively rewriting an existing canonical research/design/spec document (`research/**/*.md`, `design/**/*.md`, `specs/**/*.md`, or `docs/specifications/**/*.md`), copy the current file to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Preserve the archived snapshot exactly as it existed before the change; do not edit the archived copy after creating it.
- After the archive snapshot exists, write the updated document to the original canonical path.
- Report both the archive path and the updated canonical path in the final output.
- New files do not need archive snapshots. Append-only updates do not need archive snapshots unless an existing section is regenerated or rewritten.

## Interrogation Page

Follow the shared interrogation-page convention via the packaged convention resolver; output path is `interrogation/consolidate-prototypes-r{N}-{branch}.html`. Before producing research, run the stage-zero interrogation loop, starting with the assumptions manifest as round 1, and loop until the confidence gate passes. This skill **cannot advance to stage one until** the confidence gate passes with at least one completed interrogation round and every interview area covered or waived. Each round page must contain at least one genuinely open input (`data-open-input`).

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
