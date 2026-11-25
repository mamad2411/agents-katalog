---
name: lefthook
license: CC-BY-4.0
description: >-
  Lefthook Git hooks: write or fix `lefthook.yml` jobs (globs, staged files,
  parallel or piped runs, re-staging fixes), install hooks locally and in CI,
  and migrate from Husky. Use when the repository has `lefthook.yml` or the user
  asks for lefthook or which hook manager to choose. For an existing `.husky/`
  or `.pre-commit-config.yaml`, use the husky or pre-commit skill.
compatibility: >-
  lefthook >= 1.10.0 for `jobs:`; examples validated with lefthook 2.1.12
  (docs v2.1.14, 2026-09-29).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Lefthook

## Confirm the hook manager first

Inspect the repository before adding hooks. Extend `lefthook.yml` (or
`.lefthook.yml`, `lefthook.toml`, `lefthook.json`) when it exists. If the repo
already uses `.husky/` or `.pre-commit-config.yaml`, use that tool unless the
user asks to switch; then follow the migration in the reference. When nothing
is configured and no tool is named, say so and let the user choose; the
[decision guide](references/husky-vs-lefthook.rst) lists trade-offs.

## Install

```bash
npm install --save-dev lefthook   # postinstall runs `lefthook install`
uv add --dev lefthook             # or: pipx install lefthook
go install github.com/evilmartians/lefthook/v2@v2.1.14   # needs Go >= 1.26
brew install lefthook
lefthook install                  # after cloning, unless the npm package did it
```

- Hooks read `lefthook.yml` on every run; edit it without reinstalling.
- `lefthook install` stops when `core.hooksPath` is set (for example by
  Husky). Run `lefthook install --reset-hooks-path` once, deliberately.
- npm package in CI: `CI=true` skips the postinstall hook install;
  `LEFTHOOK=1` forces it. pnpm needs `lefthook` in `onlyBuiltDependencies` or
  the postinstall never runs.
- Disable at run time with `LEFTHOOK=0 git commit …` (or `LEFTHOOK=0` in the CI
  environment).

## Configuration

Validated with `lefthook validate` and exercised with `lefthook run`:

```yaml
min_version: 1.10.0          # `jobs:` needs >= 1.10.0

pre-commit:
  parallel: true             # opt-in; the default is sequential
  jobs:
    - name: gofmt
      glob: "*.go"
      run: gofmt -w {staged_files}
      stage_fixed: true      # re-stage what the formatter changed
    - name: buf lint
      glob: "*.proto"
      run: buf lint
    - name: eslint
      root: "web/"           # run in web/; paths are relative to it
      glob: "*.{js,ts}"
      exclude: ["*.gen.ts"]
      run: npx eslint {staged_files}

commit-msg:
  jobs:
    - name: commitlint
      run: npx --no -- commitlint --edit {1}

pre-push:
  jobs:
    - name: test
      run: go test ./...
      env:
        CGO_ENABLED: "0"     # env values must be strings
```

Traps:

- **Filter by extension with `glob`.** `file_types` takes content kinds
  (`text`, `binary`, `executable`, `symlink`, `not symlink`) and MIME types
  (`text/x-python`); `file_types: [".proto"]` filters nothing and every staged
  file reaches the command.
- **Jobs run in list order.** `priority` is not a job option and fails
  `lefthook validate`; order jobs in the list, or use `piped: true` to stop at
  the first failure (`piped` and `parallel` are exclusive).
- **`{staged_files}`** (pre-commit) and **`{push_files}`** (pre-push) expand to
  the filtered files; a job with a glob but no matching files is skipped.
  `{all_files}` and `{files}` (with `files:`) also exist.
- **`skip`/`only`** accept `merge`, `rebase` and `ref: <glob>` entries at hook
  or job level.
- **Local overrides** go in `lefthook-local.yml` (keep it out of Git), for
  example `pre-commit: {exclude_tags: [frontend]}` with jobs tagged `tags:`.
- Run `lefthook validate` after editing and `lefthook run pre-commit` to test
  without committing. `lefthook dump` prints the merged configuration.

Check option names against the
[configuration docs](https://lefthook.dev/configuration/) when the installed
`lefthook version` differs from the tested one; report options it rejects.
