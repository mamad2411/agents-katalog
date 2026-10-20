# CLAUDE.md

Consumer-facing context (exported functions and their signatures) lives in `AGENTS.md`.

## Commands

```bash
npm run build # Rolldown → ./lib, outputs CJS + ESM
npm test      # from the repo root — no per-package test script
```

## Internal architecture

Four modules exported from `src/index.ts`:

- **`objectMergeRight`** — **deprecated**, removed in the next major. Deep merge using `structuredClone`; walks both objects recursively, right side wins, `undefined` values delete the key from the left side. No consumer left in this monorepo: the `eslint-v9-*` packages compose delta layers into `configs.*` arrays and `StylelintExecutor` prepends the template to `extends` — both let the tool's own config cascade do the merging. Don't reintroduce it anywhere outside this package
- **`executeCommand`** — wraps `child_process.spawn` in a Promise; overloaded to return `EExitCode` or captured stdout string depending on `captureOutput`
- **`packages`** — thin wrappers around `local-pkg` (`isPackageExists`, `getPackageInfoSync`, `loadPackageJSONSync`)
- **`paths`** — three helpers that compose `process.cwd()` with `path.resolve` to produce absolute or relative paths
