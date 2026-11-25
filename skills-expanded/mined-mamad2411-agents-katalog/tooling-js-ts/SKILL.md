---
name: tooling-js-ts
description: "JavaScript/TypeScript audit tooling: ESLint, tsc, vitest/jest coverage, knip (dead code), retire.js, npm audit, Stryker (mutations), madge (cycles). Use during audit phases for JS/TS projects."
---

# JavaScript/TypeScript Audit Tooling

Запуск audit tools для JS/TS проектов.

## Когда применять

- В audit phases для JS/TS проектов
- После того как `language-detector` определил JS или TS
- Tools проверены на наличие через `command -v` или `npx <tool> --version`

## Tools

### TypeScript Compiler (tsc)

```bash
# Strict check
npx tsc --noEmit --strict 2>&1 | tee /tmp/tsc-output.txt

# JSON-friendly format
npx tsc --noEmit --pretty false 2>&1 | tee /tmp/tsc-output.txt
```

Парсить tsc output:
- Type errors → HIGH severity
- Missing types на public APIs → MEDIUM
- `any` overuse → LOW

### ESLint

```bash
# JSON output
npx eslint . --format=json --output-file=/tmp/eslint.json 2>/dev/null

# С security plugin (если установлен)
npx eslint . --config=.eslintrc.security.json --format=json --output-file=/tmp/eslint-security.json 2>/dev/null
```

Severity mapping:
- ESLint `error` (severity 2) - HIGH/MEDIUM
- ESLint `warning` (severity 1) - LOW

Plugins worth using:
- `eslint-plugin-security` - SAST patterns
- `eslint-plugin-react-hooks` - React-specific
- `eslint-plugin-no-secrets` - hardcoded secrets

### Knip (dead code)

```bash
npx knip --reporter=json > /tmp/knip.json 2>/dev/null
```

Knip - современный tool для нахождения:
- Unused dependencies в package.json
- Unused exports
- Unused files
- Duplicate exports

Cleaner и более accurate чем `ts-unused-exports`.

### Madge (cycles)

```bash
npx madge --circular --json src/ > /tmp/madge-circular.json 2>/dev/null
npx madge --orphans --json src/ > /tmp/madge-orphans.json 2>/dev/null
```

Cyclic dependencies - HIGH severity.
Orphan files (никем не импортированы) - MEDIUM.

### Coverage (Vitest или Jest)

**Vitest** (modern, быстрый):
```bash
npx vitest run --coverage --coverage.reporter=json-summary --coverage.reporter=html 2>/dev/null
```

Output: `coverage/coverage-summary.json`

**Jest** (legacy но common):
```bash
npx jest --coverage --coverageReporters=json-summary 2>/dev/null
```

Output: `coverage/coverage-summary.json`

Парсить:
- `total.statements.pct` - statement coverage %
- `total.branches.pct` - branch coverage %
- Per-file breakdown в `coverage-summary.json`

### npm audit / pnpm audit / yarn audit

```bash
# npm
npm audit --json > /tmp/npm-audit.json 2>/dev/null

# pnpm
pnpm audit --json > /tmp/pnpm-audit.json 2>/dev/null

# yarn (v3+)
yarn npm audit --json > /tmp/yarn-audit.json 2>/dev/null
```

Severity mapping (audit output already has severity):
- `critical` → CRITICAL
- `high` → HIGH
- `moderate` → MEDIUM
- `low` → LOW

Cross-reference с CISA KEV для known exploits.

### Retire.js (known vulnerabilities)

```bash
npx retire --outputformat=json --outputpath=/tmp/retire.json 2>/dev/null
```

Sometimes finds CVEs which `npm audit` misses (особенно для bundled libs).

### Stryker (mutation testing - DEEP MODE ONLY)

**Внимание**: медленный.

Setup (если нет):
```bash
npm install --save-dev @stryker-mutator/core @stryker-mutator/typescript-checker
npx stryker init  # creates stryker.conf.json
```

Run:
```bash
npx stryker run --reporters json,html
```

Output: `reports/mutation/mutation.json`

Mutation score interpretation:
- > 80% - excellent
- 60-80% - good  
- 40-60% - mediocre
- < 40% - poor

В deep mode:
- Запускать на critical модулях
- Спросить пользователя подтверждение если оценочное время > 1 hour
- Можно настроить `mutate` paths в stryker.conf.json для focused run

### Dependency-cruiser (layering rules)

Если в проекте есть `.dependency-cruiser.cjs`:

```bash
npx depcruise --output-type json src/ > /tmp/depcruise.json 2>/dev/null
```

Layering violations findings - HIGH severity.

### Complexity-report

Cyclomatic complexity для JS/TS:

```bash
npx complexity-report-cli --format=json src/ > /tmp/complexity.json 2>/dev/null
```

Альтернатива: `cr` (cyclomatic-report) или встроенные ESLint rules `complexity` и `max-depth`.

## Package manager detection

Определить какой PM используется:
- `package-lock.json` → npm
- `pnpm-lock.yaml` → pnpm  
- `yarn.lock` → yarn
- Multiple - вероятно проблема (legacy migration), MEDIUM finding

Запускать соответствующие audit commands.

## Output

Сырые outputs в `docs/audit/<TS>/<phase>/tooling-output/js/`.

## Tool unavailability

Если tools не установлены:

```markdown
## Missing tools (JS/TS)

- knip: not installed (`npm i -g knip` или `npm i -D knip`)
- stryker: not installed; mutation testing skipped
```

Многие JS/TS tools работают через `npx` без установки - но требуют network access (РФ может быть блок).

## React-specific checks

Если detect React в проекте:

- `eslint-plugin-react-hooks` rules - critical для hooks correctness
- React component complexity (большой component с множественными hooks)
- Missing `key` props в lists
- Unsafe lifecycle methods

## Build tool detection

- `vite.config.ts` → Vite
- `webpack.config.js` → Webpack
- `next.config.js` → Next.js  
- `nuxt.config.ts` → Nuxt
- `remix.config.js` → Remix

Каждый имеет свои best practices для bundler config audit.
