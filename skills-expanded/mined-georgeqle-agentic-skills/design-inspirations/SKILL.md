---
name: design-inspirations
description: Gather UI/UX design inspiration once via web research — named patterns, interaction/layout conventions, component-library references, and annotated links — into a durable cited brief that feeds the prototype-phase design skills
type: research
version: v0.3
required_conventions: [alignment-page, design-tree-loop]
argument-hint: "[optional: surface, product class, or reference products]"
context_intake: scoped
visual_tier: document
invocation: sub-skill
parent: ui-interview
---

# Design Inspirations

Invoke as `$design-inspirations`.

Single-pass web-research feeder for prototype-phase design work. This is the **one home for web-driven inspiration** in the product-design pack: it gathers named UI/UX patterns, interaction and layout conventions, component-library references, competitor/comparable-product UX writeups, and annotated reference links for a chosen surface or product class, then writes one durable cited brief that `$ui-interview` and `$ux-variations` read as a soft, read-if-exists input. The other design skills stay deliberately local-evidence-driven; this skill keeps web search in exactly one place.

It runs as a single pass (gather → working packet → `review` alignment page → approved canonical write), **not** a multi-session loop — the gathering is one heavy phase with no per-framework decomposition to chunk. Model the staged workflow and search-log artifact on `$customer-discovery`'s WebSearch pattern when `business-research` is installed; if it is not installed, use the staged workflow described below without recommending `$customer-discovery`.

Follow `DESIGN-TREE-LOOP.md` for prototype-phase routing, state storage, approval boundaries, and task classification. The inspiration brief is referenced from the scoped flow-tree manifest `source_artifacts[]` (a free-form artifact path — no schema change); it is a gather-once feeder, not a mandatory branch stage in the `route`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank inspirations, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, surface/product-class context, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the inspiration gather and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with the inspiration brief and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, design, task, or alignment files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language before final artifact approval. The approval request itself is the next action. Only emit consumer routing after the approved canonical inspiration brief has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, design, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope (surface, product class, reference products, anti-patterns to avoid), available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, design, or task files in Stage 1. For this skill, flat mode proposes `research/_working/preliminary-design-inspirations-research.md`; product-path mode proposes `research/{slug}/_working/preliminary-design-inspirations-research.md`.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run the required WebSearch passes, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. For design inspirations, write `research/_working/preliminary-design-inspirations-research.md` or `research/{slug}/_working/preliminary-design-inspirations-research.md`, and keep the raw search log as supporting evidence. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence/source matrix, assumptions/confidence register, source coverage gaps, the honest pixel-limit caveat, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, reference the brief from the scoped flow-tree manifest `source_artifacts[]`, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. For this skill, flat mode writes the approved brief to `design/design-inspirations-{topic}.md` plus the search log `research/design-inspirations-search-log.md`; product-path mode writes `design/{slug}/design-inspirations-{topic}.md` plus `research/{slug}/design-inspirations-search-log.md`. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Design-Tree Role

`design-inspirations` is a **sub-skill** of `ui-interview` (its `parent:`) in the design-tree loop (`DESIGN-TREE-LOOP.md`). It is invoked **inline by the parent** and enters at its own **research stage** — gathering named patterns, conventions, component-library references, and annotated links into the cited brief. It does **no downstream routing**: it returns the brief to the invoking `ui-interview` run, which owns the handoff and the design tree's `source_artifacts[]` reference.

## Process

1. **Resolve scope.** Use `$ARGUMENTS` to narrow the surface (dashboard, onboarding, editor, settings, checkout, etc.), product class, reference products, or product path. Run Product-Path Scope Resolution: if a non-archived `research/{slug}/` product path is in scope, use product-path output locations; otherwise use flat output locations. Read `.agents/project.json`, `README.md`, `CLAUDE.md`, existing `design/user-flow-*.md`, `design/ux-variations-*.md`, `design/ui-*.md`, and any scoped flow-tree manifest for the surface being designed.
2. **Light scoping interview.** This skill declares `context_intake: scoped` — ask only the focused questions needed to scope the gather, not a full interview: what surface or page class, what product class/category, any reference products the user admires, and any patterns or anti-patterns explicitly off the table. Accept "none"/"surprise me" and proceed; do not block on reference input.
3. **Gather signals via WebSearch.** After Stage 1 approval, run a broad inspiration gather using a numbered query-strategy menu (choose the strategies that fit the surface; aim for breadth):
   1. Named-pattern searches — "[surface] UI patterns", "[surface] design patterns"
   2. Interaction/layout convention searches — "[surface] layout conventions", "[task] interaction patterns"
   3. Component-library searches — "[surface] components shadcn / Radix / Material", "[pattern] component examples"
   4. Competitor/comparable teardown searches — "[product class] UX teardown", "[reference product] design review"
   5. Gallery/showcase searches — "[surface] design inspiration gallery", "best [product class] UI examples"
   6. Accessibility/responsive convention searches — "[pattern] accessibility", "[surface] responsive patterns"
   7. Anti-pattern searches — "[surface] UX mistakes", "[pattern] anti-patterns"
   8. Trend searches — "[product class] UI trends 2025 2026", "modern [surface] design"
4. **Filter for relevance.** Keep patterns, conventions, and references that fit the resolved surface, product class, and any locked constraints; drop off-target or low-signal hits. Separate observed evidence (what a source shows or states) from inference (why it might fit here).
5. **Write the working packet.** For the resolved surface, capture in the Stage 2 working packet: named patterns and conventions with when/why-used notes, component-library references, competitor/comparable UX notes, annotated reference links (what to look at in each), accessibility/responsive convention notes, anti-patterns to avoid, and a source/confidence note per item. Keep the raw query log in the search-log artifact.
6. **Rank inspirations.** Order patterns and references by fit to the resolved surface and constraints, and flag a small recommended starting set. State the honest scope limit plainly: this brief captures named patterns, conventions, and links — not a rendered pixel-level moodboard.
7. **Finalize after approval.** After final artifact approval, archive the working packet, write the approved canonical inspiration brief and search log, reference the brief from the flow-tree manifest `source_artifacts[]`, confirm the alignment page, and then route to the consumer skills.

## Output

Stage 1 output is only the scope-review alignment page and a concise request for final compiled YAML approving scope.

Stage 2 output is the working packet at `research/_working/preliminary-design-inspirations-research.md` or `research/{slug}/_working/preliminary-design-inspirations-research.md`, the raw search log, plus the updated artifact-review alignment page.

Stage 3 output is the approved canonical inspiration brief at `design/design-inspirations-{topic}.md` or `design/{slug}/design-inspirations-{topic}.md`, plus the search log at `research/design-inspirations-search-log.md` or `research/{slug}/design-inspirations-search-log.md`. The brief must include scope and source evidence, the named-pattern/convention coverage, component-library references, competitor/comparable UX notes, annotated reference links, accessibility/responsive convention notes, anti-patterns, a source/confidence matrix, the honest pixel-limit caveat, and a recommended starting set. End the final approved brief with:

```md
**Inspiration scope:** <surface / product class>
**Next work:** feed this brief into UI/UX design for the surface
**Recommended next command:** $ui-interview [specific-ux-variation]
```

## Constraints

- **Minimum research depth.** Run at least **6 WebSearch queries** across the strategy menu before writing the working packet; log every query and why in the search log.
- **Honest scope limit.** This skill gathers named patterns, conventions, and links — **not a rendered pixel-level moodboard**. Do not claim to faithfully reproduce the visual design of gallery screenshots; capture textual + linked inspiration only, and state this limit in the brief and the alignment page.
- Separate observed source evidence from inference; do not present a pattern as validated for this product without a fit rationale.
- Do not run paid API calls or external account actions.
- Do not write canonical inspiration briefs, design files, tasks, or next-command routing before final artifact approval.
- This is a soft feeder: do not require it before `$user-flow-map`, `$ux-variations`, or `$ui-interview`; those skills read the brief only if it exists.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, recommend `npx skillpacks install <pack-name>` from the project shell, before the target skill.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/design-inspirations-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
