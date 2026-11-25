---

name: open-pull-request
description: Take a Gateweave Agents change from a working tree to a reviewable pull request - branch naming, verification, Conventional Commits, the pull request template, CI and the CLA check. Use when committing work or opening/updating a pull request.
---

# Open a pull request

## 1. Branch

`main` is protected, so all work lands through pull requests. Branch from an up-to-date `main`:

```sh
git switch main && git pull
git switch -c feat/short-description   # or fix/, docs/, chore/, refactor/, test/
```

## 2. Verify

```sh
pnpm verify   # check, typecheck, test, build: exactly what CI runs
```

Fix what fails. Don't skip or weaken tests. `pnpm format` fixes most lint and format findings.

## 3. Commit

- One logical change per commit, in [Conventional Commits](https://www.conventionalcommits.org)
  form: `type(scope): summary` in the imperative, at most about 72 characters.
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf`. Scopes are package or
  area names: `web`, `auth`, `registry`, `deps`.
- The body says why the change is needed and anything a reviewer could not tell from the diff.
- Commit the generated files that belong to the change (migrations, `pnpm-lock.yaml`). Never
  commit `.dev.vars`.
- Each commit should pass on its own. In particular, keep `package.json` and `pnpm-lock.yaml` in
  the same commit.

## 4. Push and open the pull request

```sh
git push -u origin HEAD
gh pr create --base main --fill-first
```

Then fill in `.github/pull_request_template.md`: what changed and why, how it was tested
(commands and manual checks), and any follow-ups. Call out migrations that a deploy must apply
and new environment variables.

## 5. Checks

- `check` (CI) must pass before merging. Read the logs of a failure; don't re-run blindly.
- `cla`: first-time contributors sign by commenting with the sentence the bot gives them.
  Maintainers are on the allowlist.
- Merges are squash or rebase. The branch is deleted after merging.
