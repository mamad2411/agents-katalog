# JS/TS Frontend Testing

## Summary

**One-sentence:** Produces frontend component tests using @testing-library + Vitest (or Jest), querying by accessible role/label/text, explicit imports from 'vitest' (or globals:true), no snapshot-by-default, and runner-pinned mock APIs.

**One-paragraph:** Frontend testing under Vitest or Jest: queries by getByRole/getByLabelText/getByText (CSS class queries are last resort), explicit `import { describe, it, expect, vi } from 'vitest'` (or globals: true configured), no `jest.fn()` in vitest projects (and vice versa), no snapshot tests for components by default (reviewable diffs only), and userEvent for interactions. The artefact is the test file metadata; the validator enforces the canonical fields.

**Ефективно для:**

- Component test in a React/Vue/Svelte project on Vitest or Jest.
- Refactoring container.querySelector('.btn') style tests to getByRole.
- Auditing snapshot-heavy suites and replacing them with explicit assertions.
- Aligning mock API (vi.* vs jest.*) with the project's actual runner.

## Applies If (ALL must hold)

- Frontend framework component test (React / Vue / Svelte / Angular).
- Vitest or Jest is the configured runner.
- @testing-library/* + user-event installed.
- Project has TypeScript or PropTypes for typed components.

## Skip If (ANY kills it)

- Browser E2E tests — use playwright-automation.
- Pure utility / non-component logic — plain Vitest unit test is fine without testing-library.
- Backend unit tests — use testing-backend-languages / testing-django-pytest.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component under test | file path | task brief |
| Test runner | vitest | jest | package.json |
| Accessible attributes | role/label/text available on the component | design or component code |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[practices-frontend-components]] | the component being tested follows the practices methodology |
| [[practices-js-ts-stack]] | TS strict + ESLint flat config + Vitest configured |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-runner-imports` | haiku | decide vitest / jest imports based on project |
| `emit-component-test` | sonnet | render Testing Library test querying by role/label/text |
| `audit-snapshot-creep` | haiku | scan existing tests for default snapshot creation |

## Templates

| File | Purpose |
|------|---------|
| `templates/Component.test.tsx` | Vitest + Testing Library + userEvent + jest-axe |
| `templates/vitest-config.ts` | Sample vitest.config.ts toggling globals + jsdom env |
| `templates/vitest-setup.ts` | Vitest setup file adding jest-axe matcher |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-js-ts-frontend.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[practices-frontend-components]]
- [[practices-js-ts-stack]]
- [[playwright-automation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
