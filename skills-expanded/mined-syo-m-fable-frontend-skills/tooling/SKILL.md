---
name: tooling
description: Lint and enforcement configuration — ESLint, Stylelint, tsconfig flags, env validation, dead-code checks; maps project rules to the tools that enforce them. Use when configuring linters, tsconfig, or when a convention should be automated instead of remembered. 日本語の依頼例:「ESLint/Lint設定」「tsconfig設定」「ルールを自動で強制したい」「Stylelint」「CIで弾きたい」。
---

# Tooling — enforce rules with machines, not memory

Every mechanical rule in this rule-set should be backed by a tool so `lint`/CI catches violations regardless of who (or what) wrote the code. When setting up or auditing a project, wire these:

## tsconfig

- `strict: true`, plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `verbatimModuleSyntax`.

## ESLint — rule → enforcement map

| Convention (source) | ESLint rule / plugin |
|---|---|
| No `any` (CLAUDE.md) | `@typescript-eslint/no-explicit-any` |
| `@ts-expect-error` needs reason, `@ts-ignore` banned (CLAUDE.md) | `@typescript-eslint/ban-ts-comment` with `ts-expect-error: 'allow-with-description'` |
| Hooks rules + complete effect deps (react-patterns) | `eslint-plugin-react-hooks` (`rules-of-hooks`, `exhaustive-deps`) — suppression comments banned |
| No array-index keys (react-patterns) | `react/no-array-index-key` |
| Named exports only, with exceptions (react-patterns) | `import/no-default-export` + overrides allowing `app/**`, `pages/**`, `src/pages/**`, `*.stories.*`, `*.config.*`, `.storybook/**` |
| No inline styles (CLAUDE.md) | `react/forbid-dom-props` (`style`) |
| No `dangerouslySetInnerHTML` / eval family (frontend-security) | `react/no-danger`, `no-eval`, `no-implied-eval`, `no-new-func` |
| Semantic HTML, labels, keyboard, no positive tabindex (a11y) | `eslint-plugin-jsx-a11y` (recommended config, as errors) |
| Testing Library discipline (testing-vitest) | `eslint-plugin-testing-library` (`prefer-user-event`, `prefer-find-by`, `no-container`, `no-node-access`, `no-wait-for-side-effects`) |
| Playwright bans (testing-playwright) | `eslint-plugin-playwright` (`no-wait-for-timeout`, `no-networkidle`, `missing-playwright-await`, `no-element-handle`) |
| Awaited play interactions (storybook) | `eslint-plugin-storybook` (`await-interactions`, `use-storybook-expect`) |
| Server-only module isolation (nextjs) | `server-only` package + `import/no-restricted-paths` |
| Feature-boundary imports (vite-react) | `eslint-plugin-boundaries` or `dependency-cruiser` in CI |

## Stylelint (CSS Modules)

- `stylelint-declaration-strict-value`: require `var()` for `color`, `background-color`, `z-index`, `transition-duration`, spacing properties — enforces the tokens rule from `css-modules`.
- `declaration-property-value-disallowed-list`: ban raw `z-index` integers outside `tokens.css`.

## Type-safe CSS Modules

- Editor: `typescript-plugin-css-modules`. CI: generated `.d.ts` (`typed-css-modules` or the bundler's typegen) so a renamed class fails typecheck, not production.

## Env validation

- `@t3-oss/env-nextjs` / `@t3-oss/env-core` (zod-based): typed, validated env access; fails fast on missing vars; statically separates server/client vars.

## Dead code & deps

- `knip` in CI: unused files, exports, and dependencies.

## Honor-system rules — cannot be tool-enforced, review for these explicitly

zod at every boundary, per-resource authorization (IDOR), webhook signature verification, mock-at-the-boundary policy, "measure before optimizing", small focused diffs, manual keyboard walks (a11y). Lint cannot catch these. The shipped `templates/.semgrep/` heuristics backstop webhook-missing-verification, SSRF, secret exposure, and unsanitized HTML (flags for review, not proof); zod-at-boundary and IDOR have no reliable static rule and stay review-only. All of them still require human/AI code review.
