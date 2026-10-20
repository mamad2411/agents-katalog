---
name: eslint-security-plugin
description: >
  Install, configure, and triage eslint-plugin-security for JavaScript/TypeScript:
  detect-object-injection, detect-eval-with-expression, child_process and fs path
  patterns, flat vs legacy ESLint config, CI gates, and justified suppressions.
  Use when security/detect-* rules or wiring the plugin into eslint.config.js.
---

# ESLint Security Plugin

## Scope And Authorization

- **In scope:** JS/TS repos you own.
- **Out of scope:** Running linters against third-party codebases without agreement as an attack.
- Lint is a guardrail—not proof of security absence.
- Suppressions require comments and periodic review.
- Pair with `typescript-style-and-eslint` and `code-quality-standards`.

## When To Use

- Adding `eslint-plugin-security` to Node or fullstack apps.
- CI gate for eval, child_process, unsafe regex, object injection patterns.
- Triaging noisy rules (especially `detect-object-injection`).
- Flat config (`eslint.config.js`) migration with security plugin.
- Baseline vs ratcheting severities.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Express middleware hardening | `express-middleware-security` |
| esbuild trust | `esbuild-loader-trust` |
| Full SAST/DAST | org security tooling |
| Implementation quality baseline | `code-quality-standards` |
| Pure style/format | prettier/eslint style skills |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Rules | `plugin:security/recommended` as start |
| Object injection | High noise—fix or carefully allowlist |
| eval / Function | Error severity |
| child_process | Review every hit |
| CI | `eslint .` fails merge |
| Suppress | `eslint-disable-next-line` + reason |

## Workflow

### 1. Confirm scope and success criteria

1. ESLint major, flat vs eslintrc, TS or not.
2. Success: plugin on; critical rules error; CI green after triage.

### 2. Inventory ESLint setup

```bash
ls eslint.config.* .eslintrc* 2>/dev/null
npm ls eslint eslint-plugin-security 2>/dev/null | head
```

### 3. Install and enable

```bash
npm i -D eslint-plugin-security
```

```js
// eslint.config.js (flat, illustrative)
import security from 'eslint-plugin-security';

export default [
  {
    plugins: { security },
    rules: {
      ...security.configs.recommended.rules,
      'security/detect-object-injection': 'off', // often too noisy; review case-by-case
      'security/detect-eval-with-expression': 'error',
      'security/detect-child-process': 'error',
      'security/detect-non-literal-fs-filename': 'warn',
      'security/detect-unsafe-regex': 'error',
    },
  },
];
```

### 4. Baseline and triage

```bash
npx eslint . -f unix | tee eslint-security.txt | wc -l
```

| Rule | Typical action |
| --- | --- |
| detect-eval-with-expression | Remove eval; use parsers |
| detect-child-process | Validate args; avoid shell |
| detect-non-literal-require | Static imports |
| detect-object-injection | Map allowlists / Map structure |
| detect-unsafe-regex | Rewrite regex; ReDoS tests |

1. Fix high-severity first.
2. Do not mass-disable without recording residual risk.

### 5. CI gate

```yaml
- run: npx eslint . --max-warnings 0
```

1. Optionally run security rules only on `src/server/**` if frontend noise dominates.
2. Cache ESLint results carefully—don’t skip on changed rules.

### 6. Verify with evidence

1. PR introducing `eval(req.body.x)` fails CI.
2. Document justified suppressions count.
3. Pair with dependency audit (`npm audit`) separately.

### 7. Hand off

1. Team guide for common false positives.
2. Quarterly rule severity review.
3. Link Express hardening for runtime controls.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| eval | Banned | `eslint-disable` on whole file |
| CI | Required check | Lint optional warning |
| Noise | Tuned paths/rules | 5k object-injection ignores |
| Fixes | Remove sink | Suppress and ship |
| Scope | App code | node_modules linted |

## Output Checklist

- [ ] Plugin installed and configured
- [ ] Critical rules at error
- [ ] Baseline triaged
- [ ] CI fails on violations
- [ ] Suppression policy documented
- [ ] Intentional eval/child_process sinks reviewed
- [ ] Residual risk noted

## Rules

- Lint complements secure coding—does not prove safety.
- Prefer fixing sinks over disable.
- Keep configs reviewed via CODEOWNERS.
- Owned repos only.
- Runtime HTTP hardening → `express-middleware-security`.
