---
name: vue-architecture-checklist
audience: team
description: >
  Grades an existing Vue/TypeScript codebase. Detects Vue version (2 vs 3), API style
  (Options vs Composition), bundler (Vite/Vue CLI/Nuxt), TypeScript usage, state library
  (Pinia/Vuex), and router, then checks Composition API discipline, component cohesion,
  lifecycle/watcher correctness, render performance, state boundaries, accessibility, and
  type safety with file:line evidence. Use to review or grade a Vue codebase. Not for
  Socratic critique (architecture-review), security audits (vue-security-review), or new
  test-first code (tdd-loop).
---

# Vue Architecture Checklist

> "A checklist cannot fly a plane, but a pilot cannot fly safely without one."
> — Atul Gawande

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` / `react` / `vue` architecture checklists — same values, language-specific checks.

> **Grounding note:** the knowledge base has Vue 2/3 corpus under `collection="javascript"` (alongside
> TS/JS idioms) and `collection="ui_ux"` for accessibility, `collection="internal"` for architecture
> standards; cite **vuejs.org** as the primary Vue authority. Never invent a `vue` collection.

**Non-Negotiable Constraints:**
1. **Detect before judging** — no checklist item is applied until the version, framework, and structure are known
2. **Evidence or it is not a finding** — every finding cites `file:line` and the offending pattern
3. **Version-correct advice only** — never recommend an API the detected version does not have
4. **The grade is counted, not felt** — the A–F grade comes from the tally of findings

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Evidence over opinion** | Every finding cites `file:line` and the offending pattern. "Reactivity is broken" is not a finding; "`features/cart/CartSummary.vue:18` destructures `const { total } = props`, losing reactivity" is. |
| 2 | **Feature cohesion** | Organized by feature, not by technical type (`components/`, `composables/`, `utils/` dumping grounds). Cross-feature imports are a violation. |
| 3 | **Dependencies point inward** | Components depend on composables/services, not the reverse; data-fetching is isolated from presentation. Boundaries are explicit via barrels. |
| 4 | **Composition API honors reactivity** | `ref`/`reactive` unwrapped correctly; no destructuring `reactive()` (loses reactivity — use `toRefs`); `watch`/`watchEffect` dependency lists complete; watchers/effects clean up. |
| 5 | **Config & secrets hygiene** | No secrets in client bundles; only intentionally-public `VITE_`/`VUE_APP_` values exposed; config injected, not hardcoded. |
| 6 | **Tests gate change** | Untested components/composables are a finding; high-risk interactive components without Vue Testing Library tests are prioritized. |

## Workflow

Shared skeleton: `DETECT → SCAN → REPORT → RECOMMEND`.

```
DETECT     Vue version (package.json `vue`), API style (Options vs `<script setup>`/Composition),
           bundler (Vite/Vue CLI/Nuxt), TypeScript (tsconfig + strict), state library
           (Pinia/Vuex/none), router (vue-router). Record findings; version/style changes what
           is idiomatic.

SCAN       Run the Vue Checklist below section by section. Gather evidence with tooling:
             npx eslint . --max-warnings 0          # baseline — incl. eslint-plugin-vue
             npx vue-tsc --noEmit                    # type errors gate the review
             npx knip@6.47.0                         # dead code / unused exports / deps
             grep -rn "watchEffect\|watch(" src/ | wc -l   # watcher surface to audit
           Every violation becomes a finding with file:line and a severity (critical/high/medium/low).

REPORT     Emit the graded report (Output Template). Grade = function of counted findings.

RECOMMEND  Prioritize: critical → quick wins → modernization. Version-gate every recommendation.
```

**Load on demand — `references/operating-guide.md`:** Vue Checklist, AI Discipline Rules. Deeper detail: `references/eslint-configuration.md`, `references/review-checklist.md`.

## State Block

```
<arch-checklist-state>
language: vue
mode: DETECT | SCAN | REPORT | RECOMMEND | COMPLETE
detected: [vue-version | api-style | bundler | ts:strict/loose | state-lib | tests:yes/no]
issues_found: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</arch-checklist-state>
```

## Output Template

Shared across all architecture checklists.

```markdown
## Architecture Checklist: [app/package] (Vue)
**Vue**: [3.4] | **API**: [Options/Composition] | **Bundler**: [Vite/Vue CLI/Nuxt] | **TS**: [strict/loose/none] | **State**: [Pinia/Vuex/none] | **Tests**: [yes/no]

| Section | Pass | Fail | Warn |
|---------|------|------|------|
| Reactivity / Watchers / Cohesion / State / Render / Types / a11y / Boundaries | … | … | … |

### Grade: [A–F]
Grading: **A** 0 crit/0 high/≤3 med · **B** 0 crit/≤2 high · **C** 0 crit, gaps in one area ·
**D** 1+ crit · **F** fundamental problems (broken reactivity throughout, `any` everywhere, no a11y, server state in ad-hoc fetch everywhere).

| Severity | Location | Finding | Recommendation |
|----------|----------|---------|----------------|
| CRITICAL | file:line | [pattern] | [version-gated fix] |

**Reactivity/watcher audit**: | location | issue | dep source | cleanup | risk |
**Quick wins**: [low-effort, high-impact] · **Modernization**: [larger items with effort estimate]
```

## Integration with Other Skills

- **`architecture-review`** — When the grade is D/F, escalate to the Socratic critic: this checklist finds _what_ is wrong; `architecture-review` builds _why_.
- **`vue-security-review`** — Companion for the security dimension (XSS, bundle secrets, `npm audit`).
- **`vue-feature-slice`** — Correct-pattern reference when the checklist flags structural/cross-feature violations.
- **`vue-modernization-analyzer`** — When findings cluster around legacy patterns (Options API sprawl, Vue CLI), route to the modernization plan.
- **`tdd-loop`** — Methodology for adding the missing tests the checklist flags, and for driving any refactor.
- **`dotnet` / `python` / `php` / `rust` / `react`-architecture-checklist** — Sibling skills sharing this exact Core Values + workflow + output.
