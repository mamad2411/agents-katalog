---
name: package-change-workflow
description: "The end-to-end workflow for changing a co-developed R package that a project depends on: confirm branch and freshness (main vs development, submodule up to date), implement on development, test locally, push, monitor CI, merge to main only when CI is clean, then install into the project from remote main and record it. Use whenever a change to an R package is needed, including packages carried as git submodules under packages/, even when the request is framed as a project fix."
when_to_use: "Fixing or adding a feature in an R package the user maintains; a project bug whose root cause is in one of its packages; editing files under packages/<pkg>/; asked to bump, release, merge or install a package into a project; about to run renv::install on a package the user develops."
argument-hint: "[package name or path]"
paths:
  - "**/packages/*/R/**"
  - "**/packages/*/DESCRIPTION"
  - "**/packages/*/tests/**"
allowed-tools: Bash(git -C:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(git fetch:*), Bash(git branch:*), Bash(git submodule status:*), Bash(gh run list:*), Bash(gh run view:*), Bash(gh run watch:*), Read, Grep, Glob
---

# Changing a package the project depends on

Follow these stages in order. The two that publish (push, merge) and the one that
changes the project environment (install) each stop for approval. Group those
approvals into a single prompt at each checkpoint rather than asking in passing --
a question buried in a progress update gets missed.

For the package-development mechanics themselves -- `load_all`, `document`, `test`,
`check`, roxygen, NEWS -- use `r-lib:r-package-development`. This skill is the
branch, CI and install discipline around it.

## Stage 1 -- Establish where you are, before editing anything

The package may be a standalone clone or a git submodule under `packages/<pkg>`.
Work in whichever the user is using; the checks are the same.

```sh
P=packages/<pkg>                                  # or the standalone clone path
git -C "$P" fetch --prune origin
git -C "$P" status --short --branch               # branch, ahead/behind, dirty?
git -C "$P" branch --show-current                 # empty => detached HEAD
git -C "$P" rev-parse --short HEAD origin/development origin/main
```

Then answer each of these:

1. **Is a `development` branch present?** Most packages here have `development`
   and `main`; some have only `main`. If there is no `development` branch, stop and
   ask whether to create one from `main` or to work on `main` directly. Do not
   decide this silently.
2. **Which branch is checked out?** A submodule is usually on a *detached HEAD*
   after `git submodule update`. That is not the same as being on `development`.
   Before switching, check the detached HEAD carries no commits of its own:
   ```sh
   git -C "$P" log --oneline origin/development..HEAD   # must be empty
   ```
3. **Is the working tree clean?** Uncommitted changes in a package directory may
   belong to another session or to the user. Do not switch branches over them,
   stash them, or discard them -- ask.
4. **Is local `development` behind `origin/development`?** Collaborators push to
   these packages. Fast-forward only:
   ```sh
   git -C "$P" switch development
   git -C "$P" merge --ff-only origin/development
   ```
   If it will not fast-forward, local and remote have diverged -- stop and report.
5. **Is local `development` ahead of the remote with commits you did not make?**
   Unpushed commits in a shared worktree may be another session's. Ask.
6. **For a submodule: where does the project's pointer sit?** Compare it with
   `origin/main` and with the `RemoteSha` recorded for the package in the project's
   `renv.lock`:
   ```sh
   git submodule status "$P"
   jq -r '.Packages["<pkg>"] | "\(.Version) \(.RemoteRef) \(.RemoteSha)"' renv.lock
   ```
   These disagreeing is itself a finding worth reporting before you start.

Only once all of that is known: make changes on `development`.

## Stage 2 -- Implement and test locally

Work on `development`. Commit named paths, never `git add -A`.

**Check where you are before running anything.** Package tests, `R CMD check` and
source builds each spike to GB scale and spawn subprocesses. On a shared control
node that has repeatedly caused OOM kills that took the user's IDE and every session
in it down. Run them on a compute node (its own clone, brought up to date), or, if
they genuinely must run here, inside a memory-capped scope:

```sh
hostname -s; free -g
systemd-run --user --scope -p MemoryMax=4G -p MemorySwapMax=0 <command>
```

If you are not sure which node to use, that is a decision for the user -- batch it
with the Checkpoint A prompt rather than guessing.

Run the package checks in a **vanilla session from the package directory**, so
development tooling never lands in the project's renv library:

```sh
cd "$P" && Rscript-4.6.1 --vanilla -e 'devtools::document(); devtools::test()'
cd "$P" && Rscript-4.6.1 --vanilla -e 'devtools::check()'
```

Use the project's pinned R binary. If the package's development dependencies are
missing, install them into the user library from that vanilla session with
`pak::local_install_dev_deps()` -- never into the project library, and never with
`devtools::install()`.

Honour package-specific settings (some suites need `TESTTHAT_PARALLEL=false`; some
packages forbid `air format .`). See `package-conventions`.

Before leaving this stage: version bumped, a `NEWS.md` bullet added for any
user-visible change, and `devtools::document()` run, with the regenerated `man/` and
`NAMESPACE` in the same commit as the code that changed them. Only churn from a
roxygen2 version change gets a commit of its own -- see `package-conventions`.

The bullet goes under the existing `# <pkg> (development version)` heading, in the
matching subsection -- never under a new heading for the bumped version, which
release retitling would leave stranded above the release. See `package-conventions`.

**Checkpoint A -- ask to push.** Show the commits (`git -C "$P" log --oneline
origin/development..development`), the local test and check results, and the
version. Ask for approval to push `development`.

## Stage 3 -- Push and monitor CI

```sh
git -C "$P" push origin development
sha=$(git -C "$P" rev-parse HEAD)
gh run list --repo <owner>/<pkg> --commit "$sha" \
  --json databaseId,workflowName,status,conclusion
```

Wait for **every** workflow triggered by that commit, not just the first one that
reports. Use `gh run watch <id> --exit-status` as a background command and wait for
it to finish. Do not poll in a sleep loop.

- **Any failure:** read the log (`gh run view <id> --log-failed`), fix on
  `development`, test locally again, and return to Checkpoint A. Never merge a red
  or partially-finished run.
- **No workflows ran:** CI cannot be called clean. Say so and ask how to proceed.
- **A job was skipped** (e.g. `[skip-ci]`): that is not a pass. Report it.

## Stage 4 -- Merge to main (only on clean CI)

**Checkpoint B -- ask to merge and install.** Report the CI result per workflow
with run links. Ask for approval to merge `development` into `main`, push `main`,
and install into the project. One prompt, grouped.

```sh
git -C "$P" switch main
git -C "$P" merge --ff-only origin/main            # main current first
git -C "$P" merge --ff-only development \
  || git -C "$P" merge --no-ff development -m "Merge branch 'development' into main for vX.Y.Z"
git -C "$P" push origin main
```

Prefer a fast-forward. Where `main` carries commits `development` lacks, a merge
commit is the house convention -- no pull request unless the repo uses them.

Then bring `development` level with `main`, so the next change starts from the
released state and the two branches do not drift:

```sh
git -C "$P" switch development
git -C "$P" merge --ff-only origin/main && git -C "$P" push origin development
```

If `main` has a CI workflow of its own, confirm it passes on the merge commit
before installing.

**Releases and DOIs.** If the package is archived on Zenodo, a DOI is minted only when
a GitHub *release* is published -- a merge or a tag does not. Creating one
(`gh release create vX.Y.Z --notes-file <NEWS excerpt>`) publishes: include it in
Checkpoint B only when the user wants this version archived, and never write the DOI
anywhere until Zenodo has minted it. `r-reporting:provenance-receipts` covers which DOI
to cite.

## Stage 5 -- Install into the project from remote main

**Install from the remote, never from the local path.** Installing from
`packages/<pkg>` records a local source in the lockfile that no other machine or
clone can restore. The lockfile must say `Source: GitHub`, `RemoteRef: main`, and a
`RemoteSha` that exists on the remote.

First confirm no long run is live in this project -- replacing a package under
live workers breaks them hours in. The `SessionStart` report lists what was running;
check again now:

```sh
pgrep -af "<the project's long-run patterns>"
```

Then, from the project root, in the project session:

```r
renv::install("<owner>/<pkg>@main", lock = TRUE, prompt = FALSE)
```

Never a bare `renv::snapshot()`.

Verify the result instead of assuming it:

```sh
jq -r '.Packages["<pkg>"] | "\(.Version) \(.Source) \(.RemoteRef) \(.RemoteSha)"' renv.lock
git -C "$P" rev-parse origin/main
```

The `RemoteSha` must equal `origin/main`. Then move the submodule pointer to that
same commit, so the pointer and the lockfile agree:

```sh
git -C "$P" switch --detach origin/main          # or stay on development if it equals main
git add "$P" renv.lock
```

Check `git status` for `renv/activate.R`: a restore or install has been seen to
rewrite it with an unsubstituted template placeholder, which stops R starting in
the project at all. If it shows as modified and you did not intend that, restore
the committed copy.

## Stage 6 -- Record it, and deal with the consequences

Commit the lockfile and the submodule pointer **together, in one commit**:

```
deps: <pkg> <version> (<why>)
```

Two follow-ups the install does not do for you:

- **Cached results do not see package changes.** A pipeline store or a simulation
  cache built with the old version still counts as current, because neither hashes
  the bodies of installed package functions by default. Identify the cached results
  that exercise the changed code and rebuild them, or ask the user which to rebuild.
  The framework's own skill says how to invalidate them.
- **Multi-machine projects:** the new version reaches another host only through
  push, pull and restore on that host. Node-sync scripts restore from the
  **committed and pushed** lockfile, so the order is: commit the lockfile and
  pointer, push, then sync. Syncing first silently restores the old version. Do not
  sync nodes while a run is live.

Push the project commit only when the user asks -- and include that push in the
Checkpoint B prompt when a node sync is expected to follow.

## When to stop and ask

Consolidated, so they can be batched into one prompt at the next checkpoint:

- no `development` branch;
- a dirty working tree, or unpushed commits you did not make;
- `development` has diverged from `origin/development`;
- the submodule pointer, `origin/main`, and the lockfile `RemoteSha` disagree
  before you start;
- CI failed, did not run, or was skipped;
- a pipeline is running when it is time to install.
