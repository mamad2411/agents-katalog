# @ladamczyk/qoq-cli — Agent Context

`@ladamczyk/qoq-cli` orchestrates Prettier, ESLint, Knip, JSCPD, Stylelint, Structurelint, Skillslint, and npm-outdated checks behind the commands below, plus an on-demand `scan`. It reads `qoq.config.js` from the consumer project root, generates tool-specific config files at runtime into its own `bin/` directory, and delegates to each tool.

## Commands

```bash
qoq --init              # interactive wizard — writes qoq.config.js, eslint.config.js, .prettierrc (+ stylelint.config.js if Stylelint is enabled)
qoq --check             # full quality check (CI / pre-push)
qoq staged [files]      # check staged files only (pre-commit / lint-staged)
qoq --fix               # auto-fix across all tools
qoq [tools...]          # run only the named tools, e.g. `qoq eslint prettier`
qoq scan [flags]        # on-demand vulnerability scan of package-lock.json; never part of the checks
```

Check commands accept these flags (`scan` takes only `--json`, `--output`, `--timeout`, `--production`, `--graph`, `--silent`; see `docs/CONFIG.md#scan`):

| Flag                                                                         | Effect                                                                |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `--disable-cache`                                                            | Skip caching for all tools                                            |
| `--skip-{prettier,jscpd,knip,eslint,npm,stylelint,structurelint,skillslint}` | Skip individual tools                                                 |
| `--concurrency <off\|auto>`                                                  | Run tools concurrently where possible                                 |
| `--production`                                                               | Run Knip in production mode                                           |
| `--config-hints`                                                             | Enable Knip config hints                                              |
| `--silent`                                                                   | Suppress QoQ output                                                   |
| `--warmup`                                                                   | Pre-generate config files without running tools                       |
| `--json`                                                                     | Write each tool's output to a JSON file in `--output`                 |
| `--output <path>`                                                            | Directory for JSON reports (default: `bin/report`); requires `--json` |

Add `"postinstall": "qoq --warmup"` to the consumer's `package.json` so IDEs get valid ESLint/Stylelint configs immediately after `npm install`.

## Checks

**Default checks** run on every command unless explicitly skipped with the matching `--skip-*` flag:

- **npm packages check** — `@ladamczyk/outdated`'s JS API (table of problems; under `--json` the schema v1 result is written verbatim to `npm-report.json`), advisory — a failure warns and never fails the run, throttled to `npm.checkOutdatedEvery` days (`--skip-npm`)
- **Prettier** (`--skip-prettier`), **JSCPD** (`--skip-jscpd`), **Knip** (`--skip-knip`), **ESLint** (`--skip-eslint`)

**Optional checks** run only when their config block is present in `qoq.config.js`; omit the block to disable them, or skip for a single run with the matching `--skip-*` flag:

- **Stylelint** (`--skip-stylelint`) — backed by the compliant `@ladamczyk/qoq-stylelint-{css,scss}` templates; enabled via a `stylelint` block
- **Structurelint** (`--skip-structurelint`) — validates project file/folder structure; backed by `@ladamczyk/structurelint`; enabled via a `structurelint` block; runs before Skillslint
- **Skillslint** (`--skip-skillslint`) — lints Claude Code skill docs; backed by `@ladamczyk/skillslint`; enabled via a `skillslint` block

## qoq.config.js schema

The config can be authored as `qoq.config.{js,ts,mjs,cjs}`. For a TypeScript
config, import the exported `QoqConfig` type and annotate with `satisfies` to get
autocomplete and type-checking while keeping the literal's inferred type:

```ts
import type { QoqConfig } from '@ladamczyk/qoq-cli';

export default {
  srcPath: './src',
} satisfies QoqConfig;
```

A `qoq.config.ts` is loaded natively by Node's type stripping (cosmiconfig 10) —
no temp file is written. Erasable syntax only: no `enum`, `namespace` or
parameter properties. Without `"type": "module"` in the project's
`package.json`, Node prints a `MODULE_TYPELESS_PACKAGE_JSON` warning.

All fields are optional. Defaults apply when omitted.

```js
export default {
  srcPath: './src', // fallback path used by all tools

  // Overrides the CJS/ESM format otherwise auto-detected from package.json's
  // "type" field. Not offered by `qoq --init`; add it by hand if needed.
  configType: 'ESM', // or 'CJS'

  // Anonymous usage stats consent. Asked once — as the last question of
  // `qoq --init`, or on the first interactive run of a project that has a config
  // without this key — and written back here. When true, each run POSTs
  // `{ tool: 'qoq', options: [...] }` to https://stats.adamczyk.ovh — or, where
  // an outbound POST never leaves the network, fetches
  // https://adamczyk.ovh/img/stats/pixel.png with those same two values in its
  // query string. `options` holds only the value-less flags typed on that run (`--check`,
  // `--fix`, …). Never sent: code, file names, paths, config contents, findings,
  // project names, or anything identifying the user or machine.
  stats: false,

  configPaths: {
    // override locations of generated IDE config files
    eslint: '/eslint.config.js',
    prettier: '/.prettierrc',
    stylelint: '/stylelint.config.js',
  },

  npm: {
    checkOutdatedEvery: 1, // days between dependency checks; 0 = every run
  },

  prettier: {
    sources: ['./src'], // paths passed to Prettier
  },

  jscpd: {
    threshold: 2, // max duplication % before failure
    format: [], // language formats (see jscpd docs)
    ignore: [],
  },

  knip: {
    entry: [], // defaults to src/{index,cli,main,root}.{ts,js,...}
    project: [], // defaults to src/**/*.{ts,js,...}
    ignore: [],
    ignoreDependencies: [], // '@ladamczyk/qoq-*' is always ignored by default
    ignoreBinaries: [],
    ignoreFiles: [],
    ignoreMembers: [],
    ignoreUnresolved: [],
  },

  eslint: [
    {
      template: 'qoq-eslint-v9-ts', // extends configs.base from this template
      files: ['src/**/*.ts'],
      ignores: ['**/*.spec.ts'],
      rules: {}, // additional ESLint rules
    },
    {
      template: 'qoq-eslint-v9-ts-vitest',
      files: ['src/**/*.spec.ts'],
    },
  ],

  stylelint: {
    // omit entirely to disable
    template: 'qoq-stylelint-css', // or 'qoq-stylelint-scss'
    strict: false, // true = fail on warnings
  },

  structurelint: {
    // omit entirely to disable; validates project file/folder structure.
    // Mirrors structurelint's own config shape directly (no separate
    // `structure.config.*` file is read): `structure` is required to get
    // any validation; `structureRoot`, `rules`, `ignorePatterns` are optional.
    structureRoot: '.',
    structure: [{ name: 'src', children: [] }],
  },

  skillslint: {
    // omit entirely to disable; lints Claude Code skill docs
    path: './skills',
  },
};
```

Available ESLint `template` values:
`@ladamczyk/qoq-eslint-v9-{js,ts,js-react,ts-react,js-jest,ts-jest,js-jest-rtl,ts-jest-rtl,js-vitest,ts-vitest,js-vitest-rtl,ts-vitest-rtl}`

## Generated files

QoQ writes tool configs into its own `bin/` at runtime — the consumer project only needs the three root files below. Format (CJS vs ESM) is auto-detected from package.json's `type` field, unless overridden by `configType` in `qoq.config.js`.

**Consumer project root files** (created by `qoq --init`, thin re-exports for IDE support):

- `eslint.config.js` — re-exports `@ladamczyk/qoq-cli/bin/eslint.config.{m,c}js`
- `stylelint.config.js` — re-exports `@ladamczyk/qoq-cli/bin/stylelint.config.{m,c}js`
- `.prettierrc` — points to a `@ladamczyk/qoq-prettier*` template

**Runtime-generated inside `node_modules/@ladamczyk/qoq-cli/bin/`** (do not edit):

| File                               | Notes                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `eslint.config.{m,c}js`            | One `defineConfig({ extends: [configs.base, …], …block })` per `eslint` entry: each template's `configs.base` is extended and scoped to that entry's `files`/`ignores`, with the entry's own keys applied last so they win; includes `.gitignore` patterns. Templates use `eslint-config-prettier` (not `eslint-plugin-prettier`), so Prettier never runs through ESLint's rule pipeline — it only runs as its own standalone check |
| `knip.config.{m,c}js`              | Monorepo-aware: maps `workspaces` into Knip's workspace config                                                                                                                                                                                                                                                                                                                                                                      |
| `stylelint.config.{m,c}js`         | Plain JSON config: the `stylelint` block verbatim, with the template package prepended to `extends` so stylelint's own cascade merges it (consumer rules win; plugins/overrides concatenate)                                                                                                                                                                                                                                        |
| `.npm-outdated-lock`               | Timestamp file that throttles npm checks to `checkOutdatedEvery` days                                                                                                                                                                                                                                                                                                                                                               |
| `.<tool>cache`                     | Per-tool cache directories (cleared on `--warmup`)                                                                                                                                                                                                                                                                                                                                                                                  |
| `report/eslint-report.json`        | ESLint findings (written when `--json` is passed)                                                                                                                                                                                                                                                                                                                                                                                   |
| `report/knip-report.json`          | Knip findings (written when `--json` is passed)                                                                                                                                                                                                                                                                                                                                                                                     |
| `report/jscpd-report.json`         | JSCPD JSON output directory (written when `--json` is passed)                                                                                                                                                                                                                                                                                                                                                                       |
| `report/prettier-report.json`      | List of files with formatting issues (written when `--json` is passed)                                                                                                                                                                                                                                                                                                                                                              |
| `report/stylelint-report.json`     | Stylelint findings (written when `--json` is passed)                                                                                                                                                                                                                                                                                                                                                                                |
| `report/structurelint-report.json` | Structurelint violations (written when `--json` is passed)                                                                                                                                                                                                                                                                                                                                                                          |
| `report/skillslint-report.json`    | Skillslint textlint problems + skill scores (written when `--json` is passed)                                                                                                                                                                                                                                                                                                                                                       |
