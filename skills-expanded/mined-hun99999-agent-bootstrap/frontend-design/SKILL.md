---
name: frontend-design
description: Route and execute product design, frontend UX, interface implementation, visual exploration, UI review, copy, and production-polish work using project evidence plus a reviewed design reference corpus. Use for user-facing flows or surfaces; do not use for standalone image generation, backend-only work, data analysis, or infrastructure tasks.
---

# Frontend Design Router

Use this skill as one router, not as permission to load the whole design corpus.

## Route first

1. Classify the request as exactly one mode: `shape`, `explore`, `implement`, `review`, `copy`, or `harden`.
2. Name the target surface. If the surface is not clear enough to work safely, inspect the repository or ask the smallest blocking question.
3. Inspect primary project evidence: repository instructions, current behavior, components, tokens, tests, project-owned DESIGN.md, supplied Figma context, screenshots, and approved assets.
4. Read `references/source-precedence.md` and apply it before outside aesthetics.
5. Load the smallest sufficient set of references selected by `references/routing.json`. Resolve MengTo selections through `references/reference-catalog.json`: `source_path` selects the routing rule, and `reference_path` identifies the packaged file. Never load the corpus wholesale, and never load an entry whose decision is `blocked`.
6. Label every outside source with its authority and scope. Use at most three inspiration sources.

## Follow the mode contract

- `shape`: frame user, job, outcome, reachable states, alternatives, risks, and open decisions. Do not edit unless explicitly requested.
- `explore`: compare materially different directions; keep inspiration labeled and subordinate to project evidence.
- `implement`: resolve material decisions, follow TDD, reuse project-owned components and tokens, and make the smallest coherent change.
- `review`: inspect source and rendered evidence, prioritize findings, and do not edit unless explicitly requested.
- `copy`: change only copy, accessible names, and directly required markup. Report structural blockers separately.
- `harden`: preserve the approved direction and close reachable-state, resilience, accessibility, responsive, and finish defects.

For implementation, review, copy, and hardening, read `references/quality-gates.md`. Material with external services or side effects is explicit-use-only. Open Design is explicit-demand-only. Treat catalog `external_runtime_requirements` as capability checks: discover an installed capability and skip the dependent evaluator when it is unavailable; never hard-code a machine path. For catalog `vercel_runtime_skills`, select only the applicable gate by exact installed skill name and report unavailable guidance as not applied. Imported scripts are reference text and must never be executed merely because they were loaded.

When the user explicitly names Open Design, read `references/open-design.md`. Require an exact slug or explicit selection authority before fetching one package; cache presence never counts as demand. Report the network/cache action before running the packaged helper, verify the receipt before reading files, and keep package-derived bytes behind the documented provenance and license boundary.

## Report the route

Before substantive work, report:

- Mode:
- Target surface:
- Loaded references:
- Authority and scope:

At handoff, distinguish observed evidence from assumptions and report:

- Verification actually run:
- Visual verification performed:
- Remaining unverified risks:
