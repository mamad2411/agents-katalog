# JavaScript/TypeScript Stack Practices

## Summary

**One-sentence:** Produces a JS/TS project baseline: strict tsconfig, ESLint flat config + Prettier, Vitest, exports map, ESM-only, type-checked CI step.

**One-paragraph:** Modern JS/TS baseline: tsconfig.json with strict=true + noUncheckedIndexedAccess; ESLint flat config (typescript-eslint, no-unused-vars as error, import/order); Prettier with project-wide config; Vitest as the unit test runner; package.json type=module + exports map; CI runs tsc --noEmit + lint + test + build. The artefact is the project metadata; the validator checks the canonical fields are present.

**Ефективно для:**

- New JS/TS library or app being scaffolded.
- Brownfield project upgrading from CommonJS to ESM.
- Adding a strict tsconfig + ESLint flat config to a legacy repo.
- Wiring CI to enforce tsc --noEmit + lint + test on every push.

## Applies If (ALL must hold)

- Node.js >= 18 (ESM stable).
- TypeScript 5.x.
- Project is greenfield OR willing to flip type=module + adopt ESM imports.
- Test runner is Vitest or Jest (configured in this methodology to Vitest).

## Skip If (ANY kills it)

- React Native projects that pin to Metro+CommonJS.
- Legacy projects refusing ESM migration.
- Pure HTML+vanilla JS without a build step.
- Deno-native projects (different defaults; out of scope).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Node.js >= 18 | binary on PATH | developer machine |
| Package manager | pnpm | npm | yarn | team decision |
| Test scope | unit-only | unit+e2e | test plan |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[pnpm-package-management]] | package manager defaults — pnpm preferred |
| [[testing-js-ts-frontend]] | Vitest conventions for UI work |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `emit-tsconfig` | haiku | strict tsconfig template render |
| `emit-eslint-flat` | sonnet | flat config tuned to project shape |
| `emit-ci` | sonnet | tsc --noEmit + lint + test + build pipeline |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.json` | Strict TS config for ESM Node.js + library output |
| `templates/eslint.config.js` | Flat ESLint config with typescript-eslint + prettier disabling overlap |
| `templates/.prettierrc` | Prettier baseline matching most public OSS settings |
| `templates/ci.yml` | GitHub Actions workflow with discrete typecheck step |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-practices-js-ts-stack.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[pnpm-package-management]]
- [[testing-js-ts-frontend]]
- [[practices-frontend-components]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
