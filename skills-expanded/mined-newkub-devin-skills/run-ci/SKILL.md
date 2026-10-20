---
name: follow-tool-moonrepo-run-ci
description: Use moon ci on CI providers — affected targets, runInCI, sharding, reports
argument-hint: "[provider]"
related:
  - follow-monorepo
  - follow-tool-github-actions
  - run-verify
  - follow-tool-mise
---

## Goal

Configure `moon ci` so the CI pipeline correctly runs only affected tasks — covering `runInCI`, base/head detection, job sharding, reports, and remote caching

## Scope

Use when the monorepo already uses moonrepo and needs CI integration (GitHub Actions, Buildkite, CircleCI, TravisCI) — it doesn't cover `.moon/` setup (see `workflows/setup-moonrepo/SKILL.md`) or task definitions (see `workflows/config-pipeline/SKILL.md`)

- If there is no `.moon/workspace.yml` yet → do `workflows/setup-moonrepo/SKILL.md` first

## Execute

### 1. Understand moon ci Behavior

> Goal: understand how `moon ci` differs from `moon run`

1. `moon ci` = `moon exec` with prefilled flags: `--affected`, `--ci`, `--on-failure=continue`, `--summary=detailed`, `--upstream=deep`, `--downstream=direct`
2. Runs only tasks affected by changed files and having `options.runInCI: true` (default true)
3. Tasks named `dev`, `start`, `serve` default to `runInCI: false` — long-running processes must always opt out
4. Base/head revisions are detected automatically from the CI provider — falling back to `vcs.defaultBranch` and `HEAD`
5. The report is written to `.moon/cache/ciReport.json` — copy it out if it must persist (upload as a CI artifact)

### 2. Configure runInCI Per Task

> Goal: only suitable tasks run on CI

1. Disable long-running/interactive tasks:
   ```yaml
   tasks:
     dev:
       options:
         runInCI: false
   ```
2. Disable tasks that need secrets or external side-effects that shouldn't run on PRs (e.g. deploy previews)
3. Verify `build`, `lint`, `typecheck`, `test`, `check` are still `runInCI: true` (default)

### 3. Choose Targets Explicitly (Optional)

> Goal: control the task set that runs on CI

1. By default `moon ci` runs every affected task — to split jobs, specify targets:
   - `moon ci :build` — one job, build only
   - `moon ci :test :lint` — another job, test + lint
2. Explicit targets are still filtered by `runInCI` and affected detection as before

### 4. Configure Revision Detection

> Goal: correct affected detection on CI

1. moon needs full commit history — never shallow clone (`fetch-depth: 1`)
2. GitHub Actions: use `actions/checkout` with `fetch-depth: 0` and `filter: 'blob:none'` (blobless clone — fast but complete history)
3. Override with `--base`/`--head` or the `MOON_BASE`/`MOON_HEAD` env when the provider detects wrong revisions
   ```sh
   moon ci --base <BRANCH> --head <SHA>
   ```

### 5. Integrate With Provider

> Goal: correct pipeline file per provider

1. GitHub Actions (recommended — use the official action):
   ```yaml
   steps:
     - uses: 'actions/checkout@v4'
       with:
         fetch-depth: 0
         filter: 'blob:none'
     - uses: 'moonrepo/setup-toolchain@v0'
     - run: 'moon ci'
   ```
2. Other providers: install moon via the package manager (`bun add -D @moonrepo/cli`) then run `bunx moon ci`
3. PR report comment: use `moonrepo/run-report-action@v1` after `moon ci` with `if: success() || failure()`
4. See the full provider matrix in [references/ci.md](../../references/ci.md)

### 6. Shard Across Jobs (Optional)

> Goal: parallelize affected tasks across CI jobs

1. Use `--job` (0-based index) + `--job-total`:
   ```sh
   moon ci --job ${{ matrix.index }} --job-total 2
   ```
2. GitHub: emulate parallelism with `strategy.matrix.index`; Buildkite/CircleCI use native parallelism keys — examples in [references/ci.md](../../references/ci.md)

### 7. Cache Artifacts

> Goal: artifacts/cache ready across CI runs

1. Prefer remote caching per `workflows/optimize-cache/SKILL.md`
2. Manual persistence: persist only `.moon/cache/{hashes,outputs}` — never persist other files in `.moon/cache` (not portable)
3. Don't cache without invalidation — hashes changing every run create garbage cache (the reason remote caching services exist)

### 8. Verify

> Goal: a real CI run meets the bar

1. Run `moon ci` on a test branch — verify affected detection is correct
2. Check `ciReport.json` contains the expected actions
3. If affected detection comes back empty → check fetch-depth and `vcs.defaultBranch`

## Rules

### 1. Never Shallow Clone

- `moon ci` needs the merge base — a shallow clone breaks affected detection
- Use `filter: 'blob:none'` instead of `fetch-depth: 1` when speed is a concern

### 2. runInCI Discipline

- Tasks that spawn servers or watch processes must always be `runInCI: false`
- `dev`/`start`/`serve` tasks are off by default — don't re-enable them

### 3. Report Artifacts

- `.moon/cache/ciReport.json` does not persist between runs — copy/upload it immediately when needed
- Use `run-report-action` for PR visibility on GitHub

- Use /follow-tool-github-actions if needed
- Use /follow-monorepo if needed

## References

- [CI provider configs, sharding, remote cache](../../references/ci.md)

## Expected Outcome

- `moon ci` runs only affected tasks on the CI provider
- `runInCI` set correctly — no server tasks hanging in CI
- Full git history available — affected detection is accurate
- `ciReport.json` + PR report (GitHub) ready to use
