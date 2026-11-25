---
name: take-inspiration
description: Study one specific product or reference through an approved lens, synthesize it against the current design tree, and recommend owner-routed design actions
type: research
version: v0.0
required_conventions: [alignment-page, design-tree-loop]
argument-hint: "<reference product/site/app/pattern> [optional: topic, surface, or lens]"
context_intake: interview
visual_tier: document
invocation: optional-amendment
---

# Take Inspiration

Invoke as `$take-inspiration`.

Reference-specific product-design study for when the user names one product, site, app, workflow, pattern, or visual reference and wants to understand what to adopt, adapt, reject, or route into the design tree. Unlike `$brainstorm-inspirations`, this skill does not survey many candidates. It interrogates why this reference matters, researches it through an approved lens, and synthesizes findings against existing design-tree artifacts.

Follow `DESIGN-TREE-LOOP.md` for design-tree state, approval boundaries, and routing constraints. `take-inspiration` is an optional feeder/amendment skill, **not** a fixed route position. It writes approved evidence into the scoped flow-tree manifest `source_artifacts[]` only; do not add new manifest schema fields.

## Reference-Lens Interrogation

Before research, ask why the user chose the reference. Cover the relevant lenses without forcing all of them:

- visual style, brand identity, color, typography, spacing, illustration, imagery, or motion
- tone, copy, onboarding speed, first-value path, trust cues, or perceived quality
- workflow, support flow, settings, collaboration, permissioning, data display, IA, or navigation
- components, interaction patterns, state handling, empty/loading/error states, or responsive behavior
- what the user explicitly does **not** want to copy

If the user only names a reference and says "use it as inspiration," ask the lens questions before proposing research scope. Do not infer a full design direction from the reference name alone.

## Report-First Approval Gate

Default to scope-first approval. Before synthesized research, inspect enough repository and design-tree context to propose the reference lens, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, make adopt/adapt/reject recommendations, or write working packets or canonical deliverables until final compiled YAML approves the reference-study scope. Minimal pre-approval discovery may identify available files, source categories, reference availability, design-tree state, and open questions; label it as scope evidence, not findings.

After approved scope YAML, research the chosen reference through the approved lens and write only the non-canonical working packet. Then update the `review` alignment page with reference findings, design-tree synthesis, and proposed COAs. Stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, design, task, or alignment files.

## Design-Tree Context

Read current design-tree context before proposing the research scope:

- `design/**/flow-tree-*.yaml`
- `design/user-flow-*.md`, `design/ux-variations-*.md`, `design/ui-*.md`, `design/ui-requirements-*.md`, and scoped equivalents
- existing prototypes, mockups, screenshots, routes, component systems, design-system docs, and relevant research
- approved `design/brainstorm-inspirations-*.md` and `design/take-inspiration-*.md` artifacts when present

Use `research/.progress.yaml` only when the reference study would create or compare a materially different product path or product line. Ordinary UX branch state lives in `design/**/flow-tree-*.yaml`.

## Staged Research Workflow

1. **Stage 1 - Scope discovery and approval.** Interrogate the reference lens, inspect enough design-tree context, and build `alignment/take-inspiration-{topic}-{reference}.html`. The page must render the chosen reference, why the user chose it, approved/denied lenses, available source categories, design-tree inputs, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope.
2. **Stage 2 - Research and artifact review.** Only after approved scope YAML with no unresolved negative feedback, research the chosen reference through the approved lens and write only `research/_working/preliminary-take-inspiration-{topic}-{reference}.md` or `research/{slug}/_working/preliminary-take-inspiration-{topic}-{reference}.md`. Update the alignment page as a structured reference-study board with evidence, screenshots/links when available, source confidence, design-tree synthesis, and COA gates. Raw Markdown may appear only as a supplemental source view after the rendered review UI.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML only when it has no unresolved negative feedback. Apply approved edits first, archive the working packet, remove the active working packet, write the approved canonical artifact to `design/take-inspiration-{topic}-{reference}.md` or `design/{slug}/take-inspiration-{topic}-{reference}.md`, reference that artifact from the scoped flow-tree manifest `source_artifacts[]`, and convert the alignment page to `confirmed` with the approval record preserved.

## Synthesis And COAs

Synthesize the reference against the existing design tree. Recommended courses of action may include:

- adopt a pattern or principle as-is
- adapt a pattern to fit current constraints
- reject a reference aspect and state why
- add a branch
- revise a branch
- prune a branch
- update the design system
- refactor UI/prototype work
- route to a downstream or owning skill

Actual canonical tree mutations still go through the owning design-tree skill and its approval gate. This skill recommends owner-routed actions; it does not directly rewrite user-flow, UX variation, UI, prototype, or spec artifacts except for its own approved reference-study artifact and `source_artifacts[]` link.

## Process

1. **Resolve reference and topic.** Use `$ARGUMENTS` to identify the reference and any topic, surface, product path, UX branch, or lens. Normalize the reference slug for filenames.
2. **Interrogate the why.** Ask focused lens questions until the study scope is explicit enough to research.
3. **Read local context.** Locate relevant flow-tree manifests and design artifacts. Identify locked decisions, open branches, UI/prototype state, and design-system constraints.
4. **Seek scope approval.** Present the reference lens, source plan, output paths, and gates in the Stage 1 alignment page. Stop for approved compiled YAML.
5. **Research the reference.** After approval, gather source evidence for the chosen lens. Use official/product sources, public docs, screenshots, teardowns, support docs, app-store/web listings, or credible third-party analysis as appropriate. Separate observed evidence from inference.
6. **Synthesize against the tree.** Compare the reference to current artifacts and recommend COAs with owner routing, rationale, risk, and confidence.
7. **Finalize after approval.** After final artifact approval, archive the working packet, write the canonical artifact, update `source_artifacts[]`, confirm the alignment page, and route to the owning design-tree skill for any actual mutation.

## Output

Stage 1 output is only `alignment/take-inspiration-{topic}-{reference}.html` in `review` state and a concise request for final compiled YAML approving scope.

Stage 2 output is the working packet, raw search/source log, and updated structured reference-study page.

Stage 3 output is the approved canonical artifact at `design/take-inspiration-{topic}-{reference}.md` or `design/{slug}/take-inspiration-{topic}-{reference}.md`. The artifact must include reference, user-stated lens, design-tree inputs, source evidence, observed-vs-inferred findings, COA recommendations, owner routing, risks, confidence, and `source_artifacts[]` update note. End with:

```md
**Reference:** <product / site / app / pattern>
**Study lens:** <approved lens>
**Flow-tree reference:** <design/**/flow-tree-*.yaml or none>
**Source artifact:** <design/.../take-inspiration-{topic}-{reference}.md>
**Recommended owner:** <owning design-tree skill or none>
```

## Constraints

- **Reference specificity.** Study one primary reference per run. Use `$brainstorm-inspirations` when the user wants a broad candidate survey.
- **Approval before depth.** Do not do deep research before the user approves the reference lens and scope.
- **Structured board required.** The alignment page must render evidence, synthesis, and COA gates as structured HTML, not raw Markdown-only.
- **No copying claim.** Do not claim pixel-perfect reproduction or imply proprietary assets can be copied.
- Do not add this skill to the fixed flow-tree `route` tuple.
- Do not create new flow-tree schema fields for inspirations; use `source_artifacts[]`.
- Do not use `research/.progress.yaml` for ordinary UX branch state.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/take-inspiration-{topic}-{reference}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
