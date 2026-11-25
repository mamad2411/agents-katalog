---
name: vue-modernization-analyzer
audience: team
description: >
  Analyzes legacy Vue codebases and produces actionable modernization plans. Primary
  migration paths include Options API to Composition API, Vue 2 to Vue 3, Vue CLI to Vite,
  JavaScript to TypeScript, Vue Test Utils/Karma/Mocha to Vitest + Vue Testing Library,
  legacy Vuex to Pinia, and removed-in-Vue-3 pattern cleanup (filters, event bus,
  `$listeners`). Use when assessing or planning a Vue upgrade or legacy-pattern migration
  before doing it. Does NOT perform the migration — assesses, quantifies risk, and plans.
---

# Vue Modernization Analyzer

> "The best time to modernize was five years ago. The second best time is now."
> -- Adapted from software engineering practice

> "Big bang rewrites fail. Incremental migration succeeds."
> -- Martin Fowler, *Refactoring*

## Core Philosophy

Legacy Vue codebases accumulate technical debt in predictable patterns: Options API components with
sprawling `methods`/`computed`/`watch` blocks that the Composition API expresses more cohesively, Vue
CLI's unmaintained and slow build, Vue 2 behind on Vue 3's performance and Composition API, untyped
JavaScript where TypeScript would catch whole bug classes, Karma/Mocha + Vue Test Utils suites coupled to
implementation, and a Vuex store that predates Pinia's simpler, typed API.

This skill assesses, quantifies, and plans — it does NOT perform the migration. The output is a
prioritized modernization plan with risk scores, effort estimates, and a recommended sequence. The plan
is the deliverable; execution is a separate task (often via `vue-feature-slice` / `vue-app-scaffolder`).

> **Grounding note:** the KB has a Vue 2/3 corpus under `collection="javascript"` (alongside the JS→TS
> path). Cite **vuejs.org** (migration guide) + Vite/Vitest docs for version-specific detail. Never
> invent a `vue` collection.

**Non-Negotiable Constraints:**
1. **Assess before acting** — never recommend a migration path without evidence from the codebase
2. **Incremental over big-bang** — every recommendation must be achievable in phases, not a single rewrite
3. **Preserve behavior unchanged** — modernization, not reimplementation; the UI behaves identically after
4. **Dependencies are the real blockers** — a Vue 3 upgrade blocked by an unmaintained UI library is not viable
5. **Every recommendation must cite evidence** — "this looks like Options API sprawl" is not evidence; `grep -rln "export default {" src/ | xargs grep -l "methods:"` is

**What this skill is NOT:** not a migration execution tool (plan, not code); not a code quality review
(use `vue-architecture-checklist`); not a security review (use `vue-security-review`).

The ten domain principles and the grounded-KB lookup table live in `references/domain-principles.md`.

## Workflow

### Phase 1: SCAN

**Objective:** Inventory the codebase to understand its current state.

```bash
# Vue + tooling versions
grep -E '"(vue|@vue/cli-service|typescript|vite|vue-test-utils|vuex|pinia)"' package.json

# Options API surface (Options→Composition surface)
grep -rln "export default {" src/ | xargs grep -l "methods:\|data()" | wc -l

# JavaScript vs TypeScript surface
find src -name "*.vue" | xargs grep -L 'lang="ts"' | wc -l   # JS-script SFCs to migrate
find src -name "*.ts" | wc -l                                 # already TS

# Build tooling
grep -l "@vue/cli-service" package.json && echo "Vue CLI — migrate to Vite"

# Deprecated/removed-in-3 patterns
grep -rn "filters:\|Vue.filter\|\$listeners\|\$on(\|\$off(\|\$once(" src/ | head

# Test framework
grep -rln "from '@vue/test-utils'" src/ | wc -l
grep -rln "@testing-library/vue" src/ | wc -l

# Ad-hoc data fetching
grep -rn "created()\|mounted()" src/ | wc -l
grep -rn "onMounted" src/ | grep -c "fetch\|axios"
```

### Phase 2: ASSESS

**Objective:** Score each migration path by effort, risk, and blocker potential.

| Path | Tool / Signal | Assessment Method |
|------|---------------|-------------------|
| Options → Composition API | `methods:`/`data()` block count | Count Options API components; weight by watcher/computed complexity |
| Vue CLI → Vite | `@vue/cli-service` present | Check `vue.config.js` customizations; map env vars (`VUE_APP_` → `VITE_`) |
| Vue 2 → Vue 3 | `vue` major version | Map breaking changes (filters, `$listeners`, global API); check every dep's Vue 3 support; find Vue Test Utils v1 |
| JS → TS | `.vue` files without `lang="ts"` count | Gradual adoption viability; per-file conversion |
| Vue Test Utils v1/Karma → Vitest + Vue Testing Library | `@vue/test-utils` v1 import count | Test-by-test; Vue 2 test tooling is a hard blocker for Vue 3 |
| Vuex → Pinia | store module count | Per-module migration; separate server-state extraction |
| Ad-hoc fetch → query layer | `created()`/`mounted()`+fetch count | Identify fragile fetching with no caching/dedupe |

Use `references/migration-risk-matrix.md` for scoring guidance and `references/vue-version-migration.md`
for per-version breaking-change detail.

### Phase 3: PLAN

**Objective:** Produce a prioritized, phased modernization plan.

1. **Phase 0: Prerequisites** — component tests characterizing current behavior, CI, Node/version pinning (if missing)
2. **Phase 1: Tooling wins** — Vue CLI → Vite; introduce TypeScript per-file
3. **Phase 2: Test framework** — Vue Test Utils v1/Karma → Vitest + Vue Testing Library (unblocks the version bump)
4. **Phase 3: Version** — Vue 2 → Vue 3, fixing breaking changes (filters, `$listeners`, global API)
5. **Phase 4: Components** — Options API → Composition API, slice by slice
6. **Phase 5: State & data** — Vuex → Pinia; ad-hoc fetch → query layer
7. **Phase 6: Types** — finish JS → TS, turn on `strict`

### Phase 4: REPORT

**Objective:** Deliver the plan with evidence, risk scores, and effort estimates.
Use the template in `references/assessment-output-template.md` and the risk scoring table in
`references/migration-risk-matrix.md`.

## State Block

```xml
<vue-modernization-state>
  phase: SCAN | ASSESS | PLAN | REPORT | COMPLETE
  vue_version: [2 / 3 / unknown]
  bundler: vue-cli | vite | webpack-custom | nuxt | unknown
  language: js | mixed | ts
  ts_strict: true | false | n/a
  options_api_components: [count]
  test_framework: vtu-v1 | vitest-rtl | mixed | none
  state_lib: vuex | pinia | none
  migration_paths_identified: 0
  blockers_identified: 0
  last_action: [description]
  next_action: [description]
</vue-modernization-state>
```

## Output Template

The Modernization Assessment Summary — paths table, blockers table, and phased plan — is in
`references/assessment-output-template.md`. The AI discipline rules (evidence before recommendation,
quantify before scoring, incremental plans only), the anti-patterns catalog, and the error-recovery
procedures live in `references/discipline-and-recovery.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `vue-app-scaffolder` | When the plan includes Vue CLI → Vite, scaffold the target Vite + TS skeleton and migrate into it. |
| `vue-feature-slice` | Modernized components are reorganized into feature slices; use during the component phase. |
| `vue-architecture-checklist` | Run after modernization to verify the new structure meets quality gates. |
| `vue-security-review` | Run after the upgrade — new Vue/deps have different security characteristics. |
| `react-modernization-analyzer` / `python-modernization-analyzer` / `rust-migration-analyzer` | Sibling analyzers; identical assess-don't-execute philosophy, different stacks. |
