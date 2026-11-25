---
name: react-modernization-analyzer
audience: team
description: >
  Analyzes legacy React codebases and produces actionable modernization plans. Primary migration
  paths include class components to function components + hooks, Create React App to Vite, React
  16/17 to 18 to 19, JavaScript to TypeScript, Enzyme to React Testing Library, legacy Redux to
  Redux Toolkit / Zustand / Context, and deprecated lifecycle/API removal. Use when assessing or
  planning a React upgrade or legacy-pattern migration before doing it. Does NOT perform the
  migration — assesses, quantifies risk, and plans.
---

# React Modernization Analyzer

> "The best time to modernize was five years ago. The second best time is now."
> -- Adapted from software engineering practice

> "Big bang rewrites fail. Incremental migration succeeds."
> -- Martin Fowler, *Refactoring*

## Core Philosophy

Legacy React codebases accumulate technical debt in predictable patterns: class components with lifecycle
methods that hooks express more clearly, Create React App's unmaintained and slow build, React versions
behind on concurrent features and security patches, untyped JavaScript where TypeScript would catch whole
bug classes, Enzyme tests coupled to implementation, and god-object Redux stores that predate Redux
Toolkit.

This skill assesses, quantifies, and plans — it does NOT perform the migration. The output is a
prioritized modernization plan with risk scores, effort estimates, and a recommended sequence. The plan
is the deliverable; execution is a separate task (often via `react-feature-slice` / `react-app-scaffolder`).

> **Grounding note:** the KB has no React corpus. Use `collection="javascript"` for the JS→TS path and
> cite **react.dev** (upgrade guides) + Vite/RTL docs for version-specific detail. Never invent a `react` collection.

**Non-Negotiable Constraints:**
1. **Assess before acting** — never recommend a migration path without evidence from the codebase
2. **Incremental over big-bang** — every recommendation must be achievable in phases, not a single rewrite
3. **Preserve behavior unchanged** — modernization, not reimplementation; the UI behaves identically after
4. **Dependencies are the real blockers** — a React 19 upgrade blocked by an unmaintained UI library is not viable
5. **Every recommendation must cite evidence** — "this looks like class components" is not evidence; `grep -rn "extends React.Component"` is

**What this skill is NOT:** not a migration execution tool (plan, not code); not a code quality review
(use `react-architecture-checklist`); not a security review (use `react-security-review`).

The ten domain principles and the grounded-KB lookup table live in `references/domain-principles.md`.

## Workflow

### Phase 1: SCAN

**Objective:** Inventory the codebase to understand its current state.

```bash
# React + tooling versions
grep -E '"(react|react-dom|react-scripts|typescript|vite|enzyme|redux|@reduxjs/toolkit)"' package.json

# Class components (class→hooks surface)
grep -rln "extends React.Component\|extends Component\|extends PureComponent" src/ | wc -l

# JavaScript vs TypeScript surface
find src -name "*.jsx" -o -name "*.js" | wc -l        # JS to migrate
find src -name "*.tsx" -o -name "*.ts" | wc -l        # already TS

# Build tooling
grep -l "react-scripts" package.json && echo "CRA — migrate to Vite"

# Deprecated lifecycles / APIs
grep -rn "componentWillMount\|componentWillReceiveProps\|UNSAFE_\|defaultProps" src/ | head

# React Compiler adoption (stable since Oct 2025 — check before recommending manual memoization)
grep -l "babel-plugin-react-compiler" package.json || echo "Compiler not wired — candidate path"

# Test framework
grep -rln "from 'enzyme'\|require('enzyme')" src/ | wc -l      # Enzyme = React 18 blocker
grep -rln "@testing-library/react" src/ | wc -l

# Ad-hoc data fetching
grep -rn "componentDidMount" src/ | wc -l
grep -rn "useEffect" src/ | grep -c "fetch\|axios"
```

### Phase 2: ASSESS

**Objective:** Score each migration path by effort, risk, and blocker potential.

| Path | Tool / Signal | Assessment Method |
|------|---------------|-------------------|
| Class → function + hooks | `grep extends Component` count | Count class components; weight by lifecycle complexity |
| CRA → Vite | `react-scripts` present | Check custom webpack/ejected config; map env vars (`REACT_APP_` → `VITE_`) |
| React 16/17 → 18 → 19 | `react` version | Map breaking changes; check every dep's peer range; find Enzyme |
| JS → TS | `.js/.jsx` count | Gradual adoption viability; `allowJs` staging |
| Enzyme → RTL | `enzyme` import count | Test-by-test; hard blocker for React 18 |
| Legacy Redux → RTK / Zustand | store/reducer count | Per-slice migration; separate server-state extraction |
| Ad-hoc fetch → query cache | `useEffect`+fetch / `componentDidMount` count | Identify fragile fetching under concurrent React |
| Adopt React Compiler | `babel-plugin-react-compiler` absent from `package.json` | Requires React 17+ (via `react-compiler-runtime` on <19); count hand-written `memo`/`useMemo`/`useCallback` as the payoff surface |

Use `references/migration-risk-matrix.md` for scoring guidance and `references/react-version-migration.md`
for per-version breaking-change detail.

### Phase 3: PLAN

**Objective:** Produce a prioritized, phased modernization plan.

1. **Phase 0: Prerequisites** — RTL characterization tests, CI, Node/version pinning (if missing)
2. **Phase 1: Tooling wins** — CRA → Vite; introduce TypeScript with `allowJs`
3. **Phase 2: Test framework** — Enzyme → RTL (unblocks the version bump)
4. **Phase 3: Version** — React 17 → 18 (then → 19), fixing breaking changes
5. **Phase 4: Components** — class → hooks, slice by slice
6. **Phase 5: State & data** — legacy Redux → RTK/Zustand; ad-hoc fetch → query cache
7. **Phase 6: Types** — finish JS → TS; turn on `strict`
8. **Phase 7: Compiler** — wire React Compiler once the version bump lands; strip hand-written `memo`/`useMemo`/`useCallback` the compiler now subsumes

### Phase 4: REPORT

**Objective:** Deliver the plan with evidence, risk scores, and effort estimates.
Use the template in `references/assessment-output-template.md` and the risk scoring table in
`references/migration-risk-matrix.md`.

## State Block

```xml
<react-modernization-state>
  phase: SCAN | ASSESS | PLAN | REPORT | COMPLETE
  react_version: [16 / 17 / 18 / 19 / unknown]
  bundler: cra | vite | webpack-custom | next | unknown
  language: js | mixed | ts
  ts_strict: true | false | n/a
  class_components: [count]
  test_framework: enzyme | rtl | mixed | none
  state_lib: legacy-redux | rtk | zustand | context | none
  compiler_wired: true | false
  migration_paths_identified: 0
  blockers_identified: 0
  last_action: [description]
  next_action: [description]
</react-modernization-state>
```

## Output Template

The Modernization Assessment Summary — paths table, blockers table, and phased plan — is in
`references/assessment-output-template.md`. The AI discipline rules (evidence before recommendation,
quantify before scoring, incremental plans only), the anti-patterns catalog, and the error-recovery
procedures live in `references/discipline-and-recovery.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `react-app-scaffolder` | When the plan includes CRA → Vite, scaffold the target Vite + TS skeleton and migrate into it. |
| `react-feature-slice` | Modernized components are reorganized into feature slices; use during the component phase. |
| `react-architecture-checklist` | Run after modernization to verify the new structure meets quality gates. |
| `react-security-review` | Run after the upgrade — new React/deps have different security characteristics. |
| `python-modernization-analyzer` / `rust-migration-analyzer` | Sibling analyzers; identical assess-don't-execute philosophy, different stacks. |
