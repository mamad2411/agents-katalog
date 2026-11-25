---
name: react-architecture-checklist
audience: team
description: >
  Grades an existing React/TypeScript codebase. Detects React version, bundler (Vite/CRA/Next),
  TypeScript usage, state library, and router, then checks hooks discipline, component cohesion,
  effect correctness, render performance, state boundaries, accessibility, and type safety with
  file:line evidence. Use to review or grade a React codebase. Not for Socratic critique
  (architecture-review), security audits (react-security-review), or new test-first code (tdd-loop).
---

# React Architecture Checklist

> "A checklist cannot fly a plane, but a pilot cannot fly safely without one."
> — Atul Gawande

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` / `react` architecture checklists — same values, language-specific checks.

> **Grounding note:** the knowledge base has no React corpus. Use `collection="javascript"` for TS/JS
> idioms, `collection="ui_ux"` for accessibility, and `collection="internal"` for architecture standards;
> cite **react.dev** as the primary React authority. Never invent a `react` collection.

**Non-Negotiable Constraints:**
1. **Detect before judging** — no checklist item is applied until the version, framework, and structure are known
2. **Evidence or it is not a finding** — every finding cites `file:line` and the offending pattern
3. **Version-correct advice only** — never recommend an API the detected version does not have
4. **The grade is counted, not felt** — the A–F grade comes from the tally of findings

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Evidence over opinion** | Every finding cites `file:line` and the offending pattern. "Too many re-renders" is not a finding; "`features/cart/Cart.tsx:31` recreates `onAdd` every render, breaking the memoized `<Row>`" is. |
| 2 | **Feature cohesion** | Organized by feature, not by technical type (`components/`, `hooks/`, `utils/` dumping grounds). Cross-feature imports are a violation. |
| 3 | **Dependencies point inward** | UI components depend on hooks/services, not the reverse; data-fetching is isolated from presentation. Boundaries are explicit via barrels. |
| 4 | **Hooks honor the rules** | Hooks called unconditionally at the top level; effect dependency arrays complete; effects clean up. A lint suppression of `react-hooks/exhaustive-deps` is a finding. |
| 5 | **Config & secrets hygiene** | No secrets in client bundles; only intentionally-public `VITE_`/`NEXT_PUBLIC_` values exposed; config injected, not hardcoded. |
| 6 | **Tests gate change** | Untested components/hooks are a finding; high-risk interactive components without RTL tests are prioritized. |

## Workflow

Shared skeleton: `DETECT → SCAN → REPORT → RECOMMEND`.

```
DETECT     React version (package.json `react`), bundler (Vite/CRA/Next.js), TypeScript (tsconfig +
           strict), state library (Redux/RTK/Zustand/Context/none), router, and whether the React
           Compiler is wired (`babel-plugin-react-compiler` / Next.js `experimental.reactCompiler`).
           Record findings; version and compiler presence both change what is idiomatic.

SCAN       Run the React Checklist below section by section. Gather evidence with tooling:
             npx eslint . --max-warnings 0          # baseline — incl. eslint-plugin-react-hooks
             npx tsc --noEmit                        # type errors gate the review
             npx knip@6.47.0                         # dead code / unused exports / deps
             grep -rn "useEffect" src/ | wc -l       # effect surface to audit
           Every violation becomes a finding with file:line and a severity (critical/high/medium/low).

REPORT     Emit the graded report (Output Template). Grade = function of counted findings.

RECOMMEND  Prioritize: critical → quick wins → modernization. Version-gate every recommendation.
```

**Load on demand — `references/operating-guide.md`:** React Checklist, AI Discipline Rules. Deeper detail: `references/eslint-configuration.md`, `references/review-checklist.md`.

## State Block

```
<arch-checklist-state>
language: react
mode: DETECT | SCAN | REPORT | RECOMMEND | COMPLETE
detected: [react-version | bundler | ts:strict/loose | state-lib | tests:yes/no]
issues_found: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</arch-checklist-state>
```

## Output Template

Shared across all architecture checklists.

```markdown
## Architecture Checklist: [app/package] (React)
**React**: [19] | **Bundler**: [Vite/CRA/Next] | **Compiler**: [wired/absent] | **TS**: [strict/loose/none] | **State**: [RTK/Zustand/Context] | **Tests**: [yes/no]

| Section | Pass | Fail | Warn |
|---------|------|------|------|
| Hooks / Effects / Cohesion / State / Render / Types / a11y / Boundaries | … | … | … |

### Grade: [A–F]
Grading: **A** 0 crit/0 high/≤3 med · **B** 0 crit/≤2 high · **C** 0 crit, gaps in one area ·
**D** 1+ crit · **F** fundamental problems (conditional hooks, `any` everywhere, no a11y, server state in effects throughout).

| Severity | Location | Finding | Recommendation |
|----------|----------|---------|----------------|
| CRITICAL | file:line | [pattern] | [version-gated fix] |

**Hooks/effects audit**: | location | issue | dep array | cleanup | risk |
**Quick wins**: [low-effort, high-impact] · **Modernization**: [larger items with effort estimate]
```

## Integration with Other Skills

- **`architecture-review`** — When the grade is D/F, escalate to the Socratic critic: this checklist finds _what_ is wrong; `architecture-review` builds _why_.
- **`react-security-review`** — Companion for the security dimension (XSS, bundle secrets, `npm audit`).
- **`react-feature-slice`** — Correct-pattern reference when the checklist flags structural/cross-feature violations.
- **`react-modernization-analyzer`** — When findings cluster around legacy patterns (class components, CRA), route to the modernization plan.
- **`tdd-loop`** — Methodology for adding the RTL tests the checklist flags as missing, and for driving any refactor.
- **`dotnet` / `python` / `php` / `rust`-architecture-checklist** — Sibling skills sharing this exact Core Values + workflow + output.
