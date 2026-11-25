---
name: husky
license: CC-BY-4.0
description: >-
  Husky v9 Git hooks: set up or fix `.husky/` hooks, the `prepare` script,
  lint-staged or commitlint hooks, CI and production installs, and hooks that
  fail or do not run. Use when the repository has `.husky/` or the user
  mentions Husky. A
  `package.json` alone does not mean Husky; for `lefthook.yml` or
  `.pre-commit-config.yaml` use the lefthook or pre-commit skill.
compatibility: >-
  husky 9 (tested 9.1.7, 2026-09-29); Node.js with npm, pnpm, yarn or bun;
  hooks run under POSIX sh.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Husky

## Confirm the hook manager first

Inspect the repository before adding hooks:

- `.husky/` or `"prepare": "husky"` in `package.json`: extend Husky.
- `lefthook.yml` or `.pre-commit-config.yaml`: use that tool (`gh:lefthook`,
  `gh:pre-commit`). Do not add a second hook manager beside it.
- Nothing configured and no tool named: say so, then let the user choose or
  state your recommendation and why. A Node project can still use lefthook or
  pre-commit; `package.json` alone is not a reason to pick Husky.

## Set up

```bash
npm install --save-dev husky    # pnpm add --save-dev / bun add --dev; yarn: see the reference
npx husky init                  # adds "prepare": "husky" and .husky/pre-commit ("npm test")
git config core.hooksPath       # prints .husky/_
```

Run `husky` from the directory that contains `.git`. For a package in a
subdirectory, see the monorepo pattern in the reference.

## How Husky 9 runs a hook

Verified with husky 9.1.7 on Debian bookworm (`sh` is dash):

- Git calls the wrapper in `.husky/_/`, which runs `sh -e .husky/<hook> "$@"`
  with `node_modules/.bin` on `PATH`. **The shebang is ignored** and the file
  does not need to be executable.
- Write hooks in POSIX sh. Under dash, `set -o pipefail` fails with
  `Illegal option -o pipefail`, and `[[ … ]]` fails with `[[: not found`
  (inside an `if`, the check silently does nothing).
- For bash-only logic, keep it in a script and call it explicitly:

```sh
# .husky/pre-commit
bash scripts/pre-commit.sh
```

- A non-zero exit aborts the Git command. Git's hook arguments arrive as
  `$1`, `$2`, … (`commit-msg` receives the message file path).

```sh
# .husky/pre-commit
npx lint-staged
```

```sh
# .husky/commit-msg
npx --no -- commitlint --edit "$1"
```

## CI and production installs

- `prepare` runs on `npm install` and `npm ci`. If devDependencies are not
  installed (`npm ci --omit=dev`, production images), `husky` is missing and
  `prepare` fails. Use `"prepare": "husky || true"`, or an install script that
  exits before importing Husky in CI or production (reference).
- `HUSKY=0` skips both the install (`husky` prints `HUSKY=0 skip install`) and
  every hook. Set it in CI environments that should not run hooks.
- One command: `git commit --no-verify` (or `-n`); for commands without that
  flag, `HUSKY=0 git …`.

## Hooks do not run

1. `git config core.hooksPath` must print `.husky/_`. If it is empty, run the
   project's install (`npm install` runs `prepare`) or `npx husky`.
2. The file name must be a Git hook name (`.husky/pre-commit`, not
   `pre-commit.sh`). Husky installs wrappers for: pre-commit, pre-merge-commit,
   prepare-commit-msg, commit-msg, post-commit, applypatch-msg, pre-applypatch,
   post-applypatch, pre-rebase, post-rewrite, post-checkout, post-merge,
   pre-push and pre-auto-gc.
3. `command not found` (exit 127) in GUI clients or with nvm/fnm/volta: add the
   PATH setup to `~/.config/husky/init.sh` (or `$XDG_CONFIG_HOME/husky/init.sh`),
   which is sourced before every hook.
4. Debug with `HUSKY=2 git commit …`, which traces the wrapper (`set -x`).
5. After uninstalling Husky, `git config --unset core.hooksPath` so
   `.git/hooks/` works again.

## Reference

[references/hooks-reference.rst](references/hooks-reference.rst): migration
from v4 and v8, yarn and monorepo setup, the CI install script, lint-staged and
commitlint setup, and ways to disable hooks. Verify against the
[Husky docs](https://typicode.github.io/husky/) when the installed major version
(`npm ls husky`) is not 9.
