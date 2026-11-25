---
name: brainstorm-inspirations
description: Survey and compare possible product-design inspirations for current design-tree flows, surfaces, UX branches, UI direction, visual language, and product class
type: research
version: v0.4
required_conventions: [alignment-page, design-tree-loop]
argument-hint: "[optional: topic, surface, product class, UX branch, or design question]"
context_intake: scoped
visual_tier: document
invocation: optional-feeder
---

# Brainstorm Inspirations

Invoke as `$brainstorm-inspirations`.

Optional product-design feeder for surveying possible inspiration candidates before or during design-tree work. This skill does **not** pick one reference for deep study; it compares a broad set of possible products, patterns, product classes, UI systems, visual languages, workflow shapes, and anti-patterns against the current design tree so the user can approve a useful inspiration direction.

Follow `DESIGN-TREE-LOOP.md` for design-tree state, approval boundaries, and routing constraints. `brainstorm-inspirations` is an optional feeder/amendment skill, **not** a fixed route position. It writes approved evidence into the scoped flow-tree manifest `source_artifacts[]` only; do not add new manifest schema fields.

## Report-First Approval Gate

Default to scope-first approval. Before synthesized research, inspect only enough repository and visible design context to propose the candidate-survey scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the survey scope. Minimal pre-approval discovery may identify available files, source categories, surface/product-class context, existing design-tree state, and open questions; label it as scope evidence, not findings.

After approved scope YAML, run the candidate survey and write only the non-canonical working packet. Then update the `review` alignment page into a structured inspiration board and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, design, task, or alignment files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language before final artifact approval. The approval request itself is the next action.

## Design-Tree Context

Read current design-tree context before proposing the survey scope:

- `design/**/flow-tree-*.yaml`
- `design/user-flow-*.md` and `design/**/user-flow-*.md`
- `design/ux-variations-*.md` and `design/**/ux-variations-*.md`
- `design/ui-*.md`, `design/ui-requirements-*.md`, and scoped equivalents
- existing prototypes, mockups, screenshots, routes, component systems, design-system docs, and relevant research
- approved `design/brainstorm-inspirations-*.md` and `design/take-inspiration-*.md` artifacts when present

Use `research/.progress.yaml` only when the inspiration work would create or compare a materially different product path or product line. Ordinary UX branch state lives in `design/**/flow-tree-*.yaml`.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, design, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect enough design-tree context to propose the survey scope, candidate categories, source plan, assumptions, output paths, and approval questions. Build `alignment/brainstorm-inspirations-{topic}.html` before synthesized research. The page must render the proposed design-tree inputs, candidate categories, source categories, known constraints, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, design, or task files in Stage 1.
2. **Stage 2 - Research and board review.** Only after approved scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, run the synthesized candidate survey and write only `research/_working/preliminary-brainstorm-inspirations-research.md` or `research/{slug}/_working/preliminary-brainstorm-inspirations-research.md`. Keep a raw search log as supporting evidence. Update the alignment page as a structured HTML board that preserves the working-packet substance as cards, matrices, comparisons, gates, and design-tree redlining. Raw Markdown packet text may appear only as a supplemental source view after the rendered board; the board must not be a raw Markdown-only or source-only page. Stop for feedback-only YAML or final compiled YAML.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML only when it has no unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifact to `design/brainstorm-inspirations-{topic}.md` or `design/{slug}/brainstorm-inspirations-{topic}.md`, reference that artifact from the scoped flow-tree manifest `source_artifacts[]`, and convert the alignment page to `confirmed` with the approval record preserved.

## Structured Inspiration Board

The alignment page is a structured board, not a pixel-perfect moodboard and not a raw text brief. Include these categories when relevant:

- Brand personality
- Brand identity
- Visual style
- Color system
- Typography
- Layout
- UI components
- UX patterns
- Motion
- Illustration and imagery
- Copy and voice
- Information architecture
- Data visualization
- Spacing and rhythm
- Design system implications
- Competitive references
- Design-tree redlining/recommendations

Treat redlining as synthesis against existing artifacts: recommended additions, removals, revisions, or owner-routed follow-up work. Do not treat redlining as a standalone inspiration source category.

## Process

1. **Resolve scope.** Use `$ARGUMENTS` to narrow the topic, surface, product class, UX branch, UI direction, visual language, or design question. Resolve the relevant flow-tree manifest first when one exists.
2. **Read local context.** Gather the design-tree artifacts and adjacent UI/prototype evidence listed above. Identify locked decisions, open branches, existing visual language, and known constraints.
3. **Light scoping interview.** Ask only the focused questions needed to define the survey: what part of the design needs inspiration, what qualities matter, what references or anti-patterns are already known, and whether the user wants breadth across product classes or depth within one class. Accept "surprise me" and proceed.
4. **Seek scope approval.** Present the candidate categories, source plan, output paths, and gates in the Stage 1 alignment page. Stop for approved compiled YAML.
5. **Survey candidates.** After approval, research a broad candidate set across products, UI systems, workflow patterns, category conventions, and anti-patterns. Use enough searches to compare alternatives, not just validate one idea. Separate observed source evidence from inference.
6. **Compare and redline.** Score candidates against the current design tree, constraints, and target surface. Identify which references are useful for visual language, workflow, IA, components, copy, motion, data display, or design-system implications. Recommend additions, removals, revisions, or owner-routed follow-up work.
7. **Finalize after approval.** After final artifact approval, archive the working packet, write the approved canonical artifact, update `source_artifacts[]`, confirm the alignment page, and route only to the owning design-tree skill for any actual tree mutation.

## Output

Stage 1 output is only `alignment/brainstorm-inspirations-{topic}.html` in `review` state and a concise request for final compiled YAML approving scope.

Stage 2 output is the working packet at `research/_working/preliminary-brainstorm-inspirations-research.md` or `research/{slug}/_working/preliminary-brainstorm-inspirations-research.md`, the raw search log, and the updated structured board page.

Stage 3 output is the approved canonical artifact at `design/brainstorm-inspirations-{topic}.md` or `design/{slug}/brainstorm-inspirations-{topic}.md`. The artifact must include scope, design-tree inputs, candidate comparison, evidence/source matrix, confidence notes, structured board summary, design-tree redlining, and owner-routed recommendations. End with:

```md
**Inspiration scope:** <surface / flow / product class>
**Flow-tree reference:** <design/**/flow-tree-*.yaml or none>
**Source artifact:** <design/.../brainstorm-inspirations-{topic}.md>
**Recommended owner:** <owning design-tree skill or none>
```

## Constraints

- **Minimum research depth.** Run at least **6 WebSearch queries** across candidate classes before writing the working packet; log every query and why in the search log.
- **Structured board required.** The alignment page must render a board with comparison cards, matrices, evidence, and approval gates. It must not be raw Markdown-only.
- **Honest scope limit.** This skill captures comparable product and pattern evidence, not pixel-perfect reproduction of external products.
- Do not mutate canonical design-tree branches directly. Recommend owner-routed changes to `$user-flow-map`, `$ux-variations`, `$ui-interview`, `$design-system`, `$build-ui-screens`, `$logic-wiring`, `$consolidate-prototypes`, or `$spec-interview` as appropriate.
- Do not add this skill to the fixed flow-tree `route` tuple.
- Do not create new flow-tree schema fields for inspirations; use `source_artifacts[]`.
- Do not use `research/.progress.yaml` for ordinary UX branch state.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/brainstorm-inspirations-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
