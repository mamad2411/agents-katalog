---
name: concept-exploration
description: Shape a rough product or project idea into an actionable concept brief before ICP, market research, specifications, UX, UI, or implementation planning
type: planning
version: v0.3
argument-hint: "[optional rough idea, product thought, or app scope]"
---

# Concept Exploration

Invoke as `$concept-exploration`.

Use this skill when the user has a half-formed idea and needs it cleaned up enough to enter the normal research and planning workflow. This skill is intentionally pre-ICP: it clarifies the concept, problem hypothesis, beneficiary hypothesis, value wedge, constraints, non-goals, and unknowns, but does not select an ICP, analyze competitors, define UX/UI, choose architecture, or write implementation specs.

## Workflow

1. **Resolve context**
   - Read `.agents/project.json` if it exists.
   - Read README, CLAUDE.md, AGENTS.md, existing `research/`, `specs/`, and task docs when present.
   - Determine whether the current directory is already a bootstrapped project. Treat it as bootstrapped when it has meaningful `README.md` plus `AGENTS.md` or `CLAUDE.md`; treat it as unbootstrapped when those are missing, placeholder-only, or the user is describing an idea outside any project repo.
   - If `$ARGUMENTS` contains a rough idea, use it as the starting draft.
   - If `$ARGUMENTS` names an app that matches `research/{app}/`, use app-scoped output paths. Otherwise use top-level `research/`.
   - Determine the concept identity and a normalized concept slug as soon as either is known from `$ARGUMENTS`, repo context, or the interview. Normalize by lowercasing, removing URL suffix noise, replacing non-alphanumeric runs with `-`, trimming leading/trailing `-`, and dropping only project-wide brand prefixes when the remaining word is the actual scoped concept (for example, `poketo.work` -> `work`; `Poketo Core` -> `poketo-core`).
   - If existing research or the prompt suggests multiple related concepts may exist, prefer slugged output paths over generic filenames. Reserve generic `concept-brief.md` only for a single unambiguous project-level concept.
   - If no rough idea is available from arguments or repo context, ask the user for the idea in plain language.
   - Read `research/.progress.yaml` when present. Treat `active_path` as the current product/app/ICP focus and `product_paths[]` as parked or promoted product-path state, not git branch state.
   - When the prompt, repo context, interview, or pivot history surfaces multiple related concepts, apps, product lines, or future pivots, update or propose updates to `research/.progress.yaml` with product-path entries instead of merging them into one generic concept. Use fields: `id`, `label`, `source_skill`, `scope_path`, `status`, `reason`, `evidence_refs`, `revisit_trigger`, `next_skill`, and `last_touched`.
   - Keep the central concept as `active_path` when it is the current focus. Record related or future concepts as `status: deferred` or `status: revisit_candidate` with a concrete revisit trigger and a likely next skill such as `$icp <path/audience>`.

2. **Keep the boundary clear**
   - Do not run ICP, competitive analysis, journey mapping, UX variation, UI interview, roadmap, or implementation planning inside this skill.
   - Do not validate the market with broad web research. Use light repo/context inspection only; downstream research skills own evidence gathering.
   - Treat every user claim as a hypothesis unless supported by existing project files.

3. **Surface a Concept Assumptions Manifest**
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

## Output

Write:

- For one unambiguous project-level concept only: `research/concept-brief.md` and `research/concept-brief-interview.md`.
- When a concept identity is known, multiple concepts exist or may exist, or a pivot occurs: `research/concept-brief-{slug}.md` and `research/concept-brief-{slug}-interview.md`.
- If `$ARGUMENTS` names an app that matches `research/{app}/`, use the same filenames under `research/{app}/`: `research/{app}/concept-brief-{slug}.md` and `research/{app}/concept-brief-{slug}-interview.md`, or unsuffixed app-scoped files only when that app has one unambiguous concept.
- `research/.progress.yaml` — create or update only when multiple concepts, product paths, product lines, app scopes, or pivots are present. Use `product_paths` terminology instead of branch terminology.

The concept brief must include:

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

Follow the shared Alignment Page convention in CLAUDE.md. Output: `alignment/concept-exploration-{topic}.html`.

## Constraints

- Keep the skill short and pre-research.
- Do not write specs, UX variants, UI specs, roadmap phases, or implementation tasks.
- Do not recommend `$scaffold` unless the user explicitly asks to create a package/app shell before research; normal product flow scaffolds after research, prototype consolidation, spec, roadmap, and phase planning identify the first implementation target.
- Do not update `tasks/todo.md`.
- New files do not need archive snapshots. Before replacing an existing concept brief, including slugged briefs, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-relative-path>`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
