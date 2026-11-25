---
name: ult-engineer
description: Default router for the ult-engineer plugin. Routes TypeScript, React, Node.js, JavaScript, debugging, refactoring, code review, health audits, testing, and tech-debt work to the matching specialist skill(s). Use when writing, fixing, improving, refactoring, reviewing, or debugging TS/JS/React/Node code, or when the request spans more than one engineering area. Also use for /ult-engineer.
license: MIT
metadata:
  author: ult-engineer
  version: "1.0.0"
  category: software-engineering
---

# Ult Engineer router

Load this skill first. Then load only the specialist skills the table names. Do not stay in the router after routing.

This plugin assists coding agents while they write, fix, improve, refactor, review, and debug TypeScript / React / Node.js / JavaScript. Debugging and health work is built on the AVR Debug evidence loop: hypotheses first, runtime proof before a fix.

## Route

Match the user request. Load every matching specialist. Ambiguous "help with this code" / "make this better" uses the default row.

| Request | Load | Then |
|---------|------|------|
| New feature, implement, scaffold, write TS/React/Node | `write` | Detect stack, then load `typescript` / `react` / `nodejs` / `javascript` / `test` as needed |
| Bug, crash, exception, wrong output, "why is this broken", reproduce, root cause | `debug` | Classify failure; load `debugging-code`, `debug-agent`, `typescript-debugging`, `web-performance`, or `debugging-methodology` |
| Refactor, clean up logic, extract, DRY, SOLID, simplify, restructure | `refactor` | Load `code-refactor`, `dry-consolidation`, `code-complexity` when the shape of the work matches |
| Review this, PR review, is this safe, nits + architecture | `review` | Load `code-review`, `code-review-checklist`, `code-antipatterns`, `semgrep-scan` as needed |
| Health sweep, audit the repo, dead code, hidden failures, lint everything | `health` | Follow its dimension order; do not edit during the sweep |
| Types, generics, `any`, tsconfig, inference, migrate to TypeScript | `typescript` | Load `effective-typescript`, `typescript-expert`, `typescript-strict` for depth |
| React components, hooks, RSC, UI states, re-renders, `/doctor` | `react` | Load `react-patterns`, `react-ui-patterns`, `react-doctor`, `improve-react`, `react-runtime` as named |
| Node API, Express/Fastify/Nest/Hono, auth, jobs, websockets | `nodejs` | Load `nodejs-best-practices`, `nodejs-development` for decisions vs tooling |
| ES6+, promises, modules, modernize JS | `javascript` | Load `modern` patterns in that skill; pair with `refactor` if behavior must stay |
| Tests, Vitest, Jest, Testing Library, TDD, flaky tests | `test` | Pair with `code-test-quality` when auditing existing tests |
| Tech debt, dependency CVE/license audit, upgrade path | `debt` | Load `code-dep-audit`, `knip-dead-code` for measured inventory |
| Comments only, professionalize, no logic change | `code-polish` | Stay non-semantic |
| Default (broad or mixed) | `write` + `review` | Add `debug` if something is failing; add `refactor` if the ask is cleanup not a new feature |

If two specialists disagree, runtime evidence wins on bugs; the existing test suite wins on refactors; the project's current patterns win on style.

## Hard rules

1. **Do not guess a bug fix.** Form 3–5 falsifiable hypotheses and gather runtime or first-divergence evidence before editing. Cite the observation that convicts one hypothesis.
2. **Preserve behavior on refactors.** No feature work mixed into a refactor. Keep diffs reviewable. Run the project's tests after each slice.
3. **Match the repo, not a blog post.** Read `package.json`, `tsconfig.json`, and neighboring files before choosing a framework, linter, test runner, or state library.
4. **Do not invent toolchain output.** Scanner grades, CVE counts, complexity scores, and type-coverage numbers come from commands you actually ran — or are labeled hypothesis.
5. **Minimal change.** A bug fix does not need a cleanup pass. A simple feature does not need extra configurability. Three similar lines beat a premature abstraction.
6. **Verify before claiming done.** Run the checks that cover the change (`typecheck`, tests, lint). If you could not run them, say so.
7. **Load, don't paste.** Open the named specialist `SKILL.md`. Do not dump every checklist into context.

## Stack detection (always first)

Before writing or routing past the table, read:

- `package.json` / lockfile — runtime, framework, test runner, React vs Next vs Vite vs Node
- `tsconfig.json` — `strict`, `moduleResolution`, project references
- Neighboring source — import style, state library, error-handling idiom

Then adapt. Prefer existing project scripts (`npm test`, `pnpm typecheck`) over raw `tsc` / `vitest`.

## Output

```markdown
## Route
- specialist(s) loaded
- stack detected (runtime, framework, test runner)

## Evidence
| Signal | Scope | Result | Source |
|--------|-------|--------|--------|
| failing test | `src/foo.test.ts` | assertion X | lab |

## Findings or changes
- **[skill]** Item. File: `path:line`
  - Why:
  - Evidence: runtime | test | scanner | source-read | hypothesis
  - Action:

## Verification
- commands run, exit codes, what was not run

## Next specialist
- skill-name — why
```

## Specialists

| Skill | Path |
|-------|------|
| write | `../write/SKILL.md` |
| debug | `../debug/SKILL.md` |
| refactor | `../refactor/SKILL.md` |
| review | `../review/SKILL.md` |
| health | `../health/SKILL.md` |
| typescript | `../typescript/SKILL.md` |
| react | `../react/SKILL.md` |
| nodejs | `../nodejs/SKILL.md` |
| javascript | `../javascript/SKILL.md` |
| test | `../test/SKILL.md` |
| debt | `../debt/SKILL.md` |
| code-polish | `../code-polish/SKILL.md` |

Deeper AVR / scanner skills (load only when the specialist names them):

| Skill | Path |
|-------|------|
| debugging-code | `../debugging-code/SKILL.md` |
| debug-agent | `../debug-agent/SKILL.md` |
| debugging-methodology | `../debugging-methodology/SKILL.md` |
| typescript-debugging | `../typescript-debugging/SKILL.md` |
| typescript-strict | `../typescript-strict/SKILL.md` |
| typescript-sentry | `../typescript-sentry/SKILL.md` |
| web-performance | `../web-performance/SKILL.md` |
| code-review | `../code-review/SKILL.md` |
| code-review-checklist | `../code-review-checklist/SKILL.md` |
| code-antipatterns | `../code-antipatterns/SKILL.md` |
| code-hidden-failures | `../code-hidden-failures/SKILL.md` |
| code-lint | `../code-lint/SKILL.md` |
| code-complexity | `../code-complexity/SKILL.md` |
| code-dead-code | `../code-dead-code/SKILL.md` |
| code-dep-audit | `../code-dep-audit/SKILL.md` |
| code-test-quality | `../code-test-quality/SKILL.md` |
| code-docs-quality | `../code-docs-quality/SKILL.md` |
| code-refactor | `../code-refactor/SKILL.md` |
| dry-consolidation | `../dry-consolidation/SKILL.md` |
| ast-grep-search | `../ast-grep-search/SKILL.md` |
| knip-dead-code | `../knip-dead-code/SKILL.md` |
| semgrep-scan | `../semgrep-scan/SKILL.md` |
| react-doctor | `../react-doctor/SKILL.md` |
| improve-react | `../improve-react/SKILL.md` |
| react-runtime | `../react-runtime/SKILL.md` |
| effective-typescript | `../effective-typescript/SKILL.md` |
| typescript-expert | `../typescript-expert/SKILL.md` |
