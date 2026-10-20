---
name: setup-lint-format-precommit
description: Stands up a lint, format, and pre-commit toolchain (Biome or ESLint flat config + Prettier, or ruff + ruff format) with .editorconfig, fast staged-only git hooks (husky+lint-staged or the pre-commit framework), and a check-only CI gate (lint --max-warnings=0 + format --check, no auto-fix), plus a one-shot reformat of a dirty repo hidden behind .git-blame-ignore-revs.
when_to_use: A repo has no/inconsistent linting or formatting, style churn floods diffs, or commits bypass checks and you're adding enforced gates. Distinct from type-safety-strict (type-checker strictness, not style), code-review (human correctness review), refactor-cleanup (behavior-preserving cleanups, not gates), and pin-toolchain-versions (pinning the binaries the gate runs).
---

## When to Use

- "Set up ESLint/Biome/ruff + a formatter for this repo"
- "Add a pre-commit hook so unformatted/lint-failing code can't get committed"
- "Whitespace/quote/import-order churn is polluting every diff — kill it"
- "CI should fail on lint warnings and unformatted files"
- "We have config but it's slow, inconsistent across machines, or people `--no-verify` past it"

NOT this skill:
- Making the **type checker** strict (`strict: true`, removing `any`, `mypy --strict`) → type-safety-strict
- Judging whether the code is **correct** (logic bugs, edge cases) → code-review
- Behavior-preserving **cleanups/renames/dedup** of working code → refactor-cleanup
- Pinning Node/Python/tool **versions** so everyone runs the same binaries → pin-toolchain-versions
- A **monorepo's** cross-package task wiring/caching/affected-only runs → setup-monorepo-tooling

## Steps

1. **Pick the toolchain by ecosystem — never run a linter *and* a formatter that fight over the same rules.** The linter checks logic/correctness rules; the formatter owns whitespace/quotes/commas. Never leave ESLint stylistic/formatting rules on alongside Prettier.

   | Stack | Default | Why |
   |---|---|---|
   | JS/TS, want speed + one tool | **Biome** (`biome lint` + `biome format`) | One Rust binary, no plugin graph, ~10–100x faster, lint+format+import-sort in one config |
   | JS/TS, need plugin ecosystem (React, a11y, import, custom) | **ESLint flat config (`eslint.config.js`) + Prettier** | Plugin coverage Biome lacks; Prettier owns formatting so disable ESLint stylistic rules |
   | Python | **ruff** (`ruff check`) **+ `ruff format`** | Replaces flake8+isort+black+pyupgrade in one tool; `ruff format` is black-compatible |

   Default to **Biome** for greenfield JS/TS; switch to **ESLint flat + Prettier** only when a required plugin (e.g. `eslint-plugin-jsx-a11y`, `eslint-plugin-import`) has no Biome equivalent; **ruff + ruff format** for Python. Don't reach for ESLint legacy `.eslintrc` — flat config is the only supported format on ESLint v9+.

2. **Write minimal config that extends a shared base — don't hand-roll a 200-rule file.** Turn on the recommended preset, override only the handful you actually disagree with.

   Biome (`biome.json`):
   ```json
   {
     "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
     "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
     "linter": { "enabled": true, "rules": { "recommended": true } },
     "formatter": { "enabled": true, "indentStyle": "space", "indentWidth": 2 },
     "organizeImports": { "enabled": true }
   }
   ```
   ESLint flat (`eslint.config.js`) — keep Prettier as the formatter, use `eslint-config-prettier` to switch off every conflicting ESLint rule:
   ```js
   import js from "@eslint/js";
   import prettier from "eslint-config-prettier";
   export default [
     js.configs.recommended,
     prettier, // MUST be last — disables all stylistic rules so Prettier wins
     { ignores: ["dist/", "build/", "coverage/", "node_modules/"] },
   ];
   ```
   ruff (`pyproject.toml`):
   ```toml
   [tool.ruff]
   line-length = 100
   [tool.ruff.lint]
   select = ["E", "F", "I", "UP", "B"]  # pycodestyle, pyflakes, isort, pyupgrade, bugbear
   ```

3. **Add `.editorconfig` + format-on-save so the editor stops introducing churn at the source.** One `.editorconfig` at the repo root makes every editor agree on charset/EOL/indent before a linter ever runs:
   ```ini
   root = true
   [*]
   charset = utf-8
   end_of_line = lf
   insert_final_newline = true
   trim_trailing_whitespace = true
   indent_style = space
   indent_size = 2
   ```
   Commit `.vscode/settings.json` with `"editor.formatOnSave": true` and `"editor.defaultFormatter"` set to the chosen tool (`biomejs.biome`, `esbenp.prettier-vscode`, or `charliermarsh.ruff`) so the gate rarely fires in the first place.

4. **Wire the pre-commit hook to run on *changed files only* — keep it under a few seconds or people will `--no-verify`.** For JS/TS use **husky + lint-staged** (lints/formats only staged files); for Python or polyglot repos use the **pre-commit framework**.

   husky + lint-staged:
   ```bash
   npm i -D husky lint-staged && npx husky init
   printf 'npx lint-staged\n' > .husky/pre-commit
   ```
   `package.json` — lint-staged runs on the staged paths and re-stages what it fixes:
   ```json
   "lint-staged": {
     "*.{js,ts,jsx,tsx}": ["biome check --write --no-errors-on-unmatched"],
     "*.{json,css,md}": ["biome format --write --no-errors-on-unmatched"]
   }
   ```
   pre-commit framework (`.pre-commit-config.yaml`) — pin hook revs, then `pre-commit install`:
   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.6.9
       hooks:
         - id: ruff       # lint
           args: [--fix]
         - id: ruff-format
   ```
   The hook may auto-fix locally; CI must not (step 5). Never run a full-repo lint in the hook — staged-only is what keeps it fast.

5. **Make CI the real gate: check, never fix.** The hook is bypassable (`--no-verify`, unconfigured machines, IDE off); CI is the wall. Run lint with **zero-tolerance** and format in **check** mode so CI fails on drift instead of silently rewriting it:
   - Biome: `biome ci .` (lint + format check + import-order in one CI-tuned command)
   - ESLint + Prettier: `eslint . --max-warnings=0` **and** `prettier --check .`
   - ruff: `ruff check --output-format=github .` **and** `ruff format --check .`

   `--max-warnings=0` makes warnings fail the build (otherwise they rot into hundreds). `--check`/`ci` exits non-zero on any unformatted file and prints the diff — **never** `--write`/`--fix` in CI, which would push autofixes nobody reviewed. Run on the same tool versions the hook uses (a lockfile + pinned hook revs), or CI and local disagree — coordinate with pin-toolchain-versions if the binaries float.

6. **Migrate a dirty repo in one isolated reformat commit, then hide it from blame.** Don't fold the format sweep into a feature PR — it buries the real change. Run the formatter across the whole tree once, commit alone, then add that commit to `.git-blame-ignore-revs` so `git blame` skips it:
   ```bash
   biome format --write . || (prettier --write . ; ruff format .)
   git commit -am "style: format entire repo (no behavior change)"
   git rev-parse HEAD >> .git-blame-ignore-revs
   git config blame.ignoreRevsFile .git-blame-ignore-revs   # local; GitHub/GitLab honor the committed file
   ```
   Sanity-check the sweep changed only formatting: `git show --stat` should be whitespace/quotes only. After this commit the CI `--check` gate passes on a clean tree, so every later PR is gated against an already-formatted baseline.

## Common Errors

- **Linter and formatter fighting.** ESLint stylistic rules (or `airbnb` quote/semi rules) vs Prettier produce an infinite "fixed by one, broken by the other" loop. Add `eslint-config-prettier` **last** in the flat config to disable every conflicting rule; let the formatter own formatting.
- **Hook lints the whole repo.** A pre-commit that runs `eslint .` takes 30s+ and gets `--no-verify`'d into uselessness. Use lint-staged / pre-commit's built-in file filtering so it only touches staged paths.
- **CI auto-fixes instead of checking.** `eslint --fix` / `prettier --write` / `ruff --fix` in CI either commits unreviewed changes or, on a read-only checkout, masks failures. CI must use `--check`/`ci`/`--max-warnings=0` and fail, not mutate.
- **Warnings allowed in CI.** Without `--max-warnings=0`, warnings accumulate into noise nobody reads. Treat warnings as errors in CI; downgrade a rule to `off` deliberately if you truly don't want it.
- **Format sweep mixed into a feature PR.** Reviewers can't see the real diff and `git blame` points everything at you. Reformat in its own commit and register it in `.git-blame-ignore-revs`.
- **No `.editorconfig` / format-on-save.** Editors keep reintroducing CRLF/tabs/trailing whitespace, so the hook fires on every commit. Fix it at the editor with a committed `.editorconfig` + `formatOnSave`.
- **Legacy `.eslintrc` with new ESLint.** ESLint v9 defaults to flat config; a leftover `.eslintrc.json` is silently ignored or errors. Migrate to `eslint.config.js`.
- **Unpinned hook/tool versions.** `pre-commit autoupdate` or a floating `biome`/`eslint` makes CI and local disagree and breaks reproducibly-later. Pin hook `rev`s and lock tool versions (a lockfile, or coordinate with pin-toolchain-versions).
- **Ignoring generated/vendored dirs not configured.** Linting `dist/`, `build/`, `coverage/`, `.next/`, migrations, or snapshots floods output and slows everything. Set ignores in config (and `useIgnoreFile`/`.eslintignore`-equivalent) so they're skipped everywhere — hook and CI alike.

## Verify

1. **Bad file is caught by the formatter check:** create a deliberately mangled file (wrong indent, double→single quotes, no final newline). `biome ci .` / `prettier --check .` / `ruff format --check .` exits non-zero and names that file.
2. **Bad file is caught by the linter:** add an unused import / `==` where a rule forbids it. `eslint . --max-warnings=0` / `biome lint .` / `ruff check .` exits non-zero.
3. **Hook blocks the commit:** `git add` the bad file and `git commit` — the commit is rejected (or the file is auto-fixed and you must re-stage), proving the hook runs on staged files.
4. **Hook is fast:** time a commit touching one file — pre-commit completes in a few seconds, not tens (proves it's staged-only, not whole-repo).
5. **CI gate fails on drift:** push the bad file (or run the CI command locally) → the lint/format job is red; fix it → green. Confirm CI uses `--check`/`--max-warnings=0`, never `--write`/`--fix`.
6. **Clean baseline:** on a freshly formatted tree, the full CI command exits 0 with no changes — the reformat commit landed and is in `.git-blame-ignore-revs` (`git blame` skips it).

Done = a deliberately bad file is rejected by **both** the local pre-commit hook (in seconds, staged-only) and the CI gate (lint `--max-warnings=0` + format `--check`, no auto-fix), the formatter and linter don't fight, and the existing tree is already clean behind a single blame-ignored reformat commit.
