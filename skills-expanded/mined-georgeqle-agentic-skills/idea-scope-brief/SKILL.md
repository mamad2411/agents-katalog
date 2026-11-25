---
name: idea-scope-brief
description: Shape a rough product or project idea into a scoped brief before ICP, market research, specifications, UX, UI, or implementation planning
type: planning
version: v0.9
argument-hint: "[optional rough idea, product thought, or product-path scope]"
---

# Idea Scope Brief

Invoke as `$idea-scope-brief`.

Use this skill when the user has a half-formed idea and needs it cleaned up enough to enter the normal research and planning workflow. This skill is intentionally pre-ICP: it clarifies the concept, problem hypothesis, beneficiary hypothesis, value wedge, constraints, non-goals, and unknowns, but does not select an ICP, analyze competitors, define UX/UI, choose architecture, or write implementation specs.

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

1. **Resolve context**
   - Read `.agents/project.json` if it exists.
   - Read README, CLAUDE.md, AGENTS.md, existing `research/`, `specs/`, and task docs when present.
   - Determine whether the current directory is already a bootstrapped project. Treat it as bootstrapped when it has meaningful `README.md` plus `AGENTS.md` or `CLAUDE.md`; treat it as unbootstrapped when those are missing, placeholder-only, or the user is describing an idea outside any project repo.
   - If `$ARGUMENTS` contains a rough idea, use it as the starting draft.
   - If `$ARGUMENTS` names a non-archived `research/{slug}/` product path, use that path. If it names only `research/_archive/{slug}/`, stop and warn that the path is archived.
   - Determine the concept identity and a normalized concept slug as soon as either is known from `$ARGUMENTS`, repo context, or the interview. Normalize by lowercasing, removing URL suffix noise, replacing non-alphanumeric runs with `-`, trimming leading/trailing `-`, and dropping only project-wide brand prefixes when the remaining word is the actual scoped concept (for example, `poketo.work` -> `work`; `Poketo Core` -> `poketo-core`).
   - If existing research or the prompt suggests multiple related concepts may exist, prefer slugged output paths over generic filenames. Reserve generic `idea-brief.md` only for a single unambiguous project-level concept.
   - If no rough idea is available from arguments or repo context, ask the user for the idea in plain language.
   - Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Treat `active_paths` as the current product/app/ICP focuses and `product_paths[]` as parked, archived, or promoted product-path state, not git branch state.
   - When the prompt, repo context, interview, or pivot history surfaces multiple related concepts, apps, product lines, or future pivots, update or propose updates to `research/.progress.yaml` with product-path entries instead of merging them into one generic concept. Use fields: `id`, `label`, `scope_path`, `status`, `source_skill`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `pipeline_stage`, and `last_touched`. Set `pipeline_stage: idea-scope-brief` on entries created by this skill.
   - Keep the central concept in `active_paths` when it is the current focus. Record related or future concepts as `status: deferred` or `status: revisit_candidate` with a concrete revisit trigger and a likely next skill such as `$icp <path/audience>`; if `business-discovery` is not enabled, recommend `$pack install business-discovery` before `$icp`.
   - When 3+ product paths exist in the manifest, recommend `$product-line review` to the user for portfolio management; if `business-ops` is not enabled, recommend `$pack install business-ops` before `$product-line`.

2. **Keep the boundary clear**
   - Do not run ICP, competitive analysis, journey mapping, UX variation, UI interview, roadmap, or implementation planning inside this skill.
   - Do not validate the market with broad web research. Use light repo/context inspection only; downstream research skills own evidence gathering.
   - Treat every user claim as a hypothesis unless supported by existing project files.

3. **Surface an Idea Assumptions Manifest**
   - Before deep questioning, present what you think the concept is.
   - Tag assumptions as `[from prompt]`, `[from repo]`, `[from research]`, or `[inferred]`.
   - Cover:
     - concept summary
     - problem hypothesis
     - target beneficiary or user hypothesis
     - product/category guess
     - value wedge
     - constraints
     - non-goals
     - riskiest unknowns
   - Ask the user to confirm, correct, or flag assumptions before writing.

4. **Interview until concept-ready**
   - Codex interview cadence is one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same decision, not to batch unrelated questions.
   - Resolve only concept-level ambiguity:
     - what problem exists
     - who might care
     - what outcome changes for them
     - what makes the idea different enough to investigate
     - what must stay out of scope
     - what constraints are real now
   - When unsure, recommend a practical default and clearly mark it as an assumption.

5. **Coverage checkpoint**
   - Present the final concept summary, unknowns, and readiness for ICP.
   - Restate the resolved concept identity, slug, and exact output paths before writing.
   - If the conversation pivoted from the initial concept to a different central concept, write the pivoted concept to its own slugged brief and preserve the initial concept as a related or future concept in the brief and interview log. Do not merge both concepts into one generic project-level brief.
   - Ask whether any core premise, constraint, or non-goal is wrong before writing.

6. **Build pre-approval alignment preview**
   - Before writing any canonical `research/**/idea-brief.md`, `research/**/idea-brief-interview.md`, legacy flat `research/idea-brief-{slug}.md` variant, or `research/.progress.yaml`, build `alignment/idea-scope-brief-{topic}.html` as the review artifact.
   - The HTML page must render the Idea/Concept Assumptions Manifest, artifact destinations, proposed file changes, coverage checkpoint, and approval gates.
   - Attempt to open the page in the browser and point the user at the repo-relative path.
   - Treat coverage-checkpoint confirmation as non-final; it only confirms the draft scope is ready to preview. Only final compiled YAML from the alignment page authorizes canonical writes.
   - Before compiled YAML approval, the next action is review or revision of the HTML alignment page. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after final compiled YAML approval has been provided and the approved artifacts below have been written or updated.
   - When feedback-only YAML is provided, revise the alignment page and ask again; do not write canonical artifacts until final compiled YAML approval is provided.

## Output

Before writing anything in this section, verify the alignment page has final compiled YAML approval. Do not write canonical idea briefs, interview logs, or `research/.progress.yaml` until `alignment/idea-scope-brief-{topic}.html` has been reviewed and the user has provided final compiled YAML approval. Coverage-checkpoint confirmation is not final approval and does not authorize these writes.

Write:

- For one unambiguous project-level concept only: `research/idea-brief.md` and `research/idea-brief-interview.md`.
- When a product identity is known, multiple concepts exist or may exist, or a pivot occurs: prefer `research/{slug}/idea-brief.md` and `research/{slug}/idea-brief-interview.md`; preserve flat `research/idea-brief-{slug}.md` only as legacy compatibility when no product path is being introduced.
- If `$ARGUMENTS` names a non-archived product path, use unsuffixed scoped files under `research/{slug}/`: `research/{slug}/idea-brief.md` and `research/{slug}/idea-brief-interview.md`.
- `research/.progress.yaml` — create or update only when multiple concepts, product paths, product lines, product-path scopes, or pivots are present. Use `product_paths` terminology instead of branch terminology.

The idea brief must include:

- `## Summary`
- `## Problem Hypothesis`
- `## Beneficiary Hypothesis`
- `## Product Category Guess`
- `## Value Wedge`
- `## Constraints`
- `## Non-Goals`
- `## Assumptions And Unknowns`
- `## ICP Readiness`
- `## Next Steps`

The `## ICP Readiness` section must state whether the concept is ready for `$icp`, what inputs `$icp` should use, and which assumptions should be tested first.

The `## Next Steps` section must recommend exactly one primary command:

- If the concept appears to be a business app or user-facing product and the business discovery lane is not enabled: `$pack install business-discovery` — this installs the research skills (ICP, competitive analysis, value prop, positioning, lean canvas) needed before any repo bootstrapping or development.
- If `business-discovery` or the compatibility `business-app` alias is enabled: `$icp`
- If the concept already has ICP/market evidence but needs journey, onboarding, conversion, or retention planning: `$pack install customer-lifecycle`
- If project type is unclear: `$pack recommend`

Include 1-3 other options only when they are materially useful.

### Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/idea-scope-brief-{topic}.html`.

## Constraints

- Keep the skill short and pre-research.
- Do not write specs, UX variants, UI specs, roadmap phases, or implementation tasks.
- Do not recommend `$scaffold` unless the user explicitly asks to create a package/app shell before research; normal product flow scaffolds after research, prototype consolidation, spec, roadmap, and phase planning identify the first implementation target. `$scaffold` requires the monorepo pack (`$pack install monorepo`).
- Do not update `tasks/todo.md`.
- New files do not need archive snapshots. Before replacing an existing idea brief, including slugged briefs, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.
- Migration: if a project already has `research/concept-brief.md`, `research/concept-brief-interview.md`, or any `research/{slug}/concept-brief*.md` / `research/concept-brief-{slug}*.md` from a prior run, rename it to the `idea-brief` equivalent before re-running. Write only the `idea-brief` names and no longer recognizes the legacy `concept-brief` filenames.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
