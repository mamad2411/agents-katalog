---
name: commit
description: Write a succinct commit -- Conventional Commits with a scope, an imperative subject under about 70 characters, and a body of one to three lines saying why; long forensics go to the pull request body, NEWS.md or the project's CLAUDE.md instead. Stages named paths only, checks submodule pointers against the remote, and appends the Co-Authored-By trailer. Also covers pull request descriptions.
argument-hint: "[optional: what changed, or paths to stage]"
disable-model-invocation: true
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*), Bash(git submodule status:*), Bash(git -C:*), Bash(git ls-files:*), Read, Grep
---

# Commit messages

Run this only when the user asks for a commit. Never commit unprompted.

A commit message is writing, so the writing rules apply: plain words, no stock
phrasing, nothing a reader has to decode. `r-reporting:report-writing` holds the
full list; the short version is that if a sentence reads as generated, it is.

## 1. Look before staging

```sh
git status --porcelain
git diff --stat
git diff                      # actually read it
```

Stage **named paths**, never `-a` and never `.`:

```sh
git add R/targets_fire.R params/fire/severity.csv
```

`git commit -a` sweeps in unrelated churn -- `renv.lock`, `_targets` metadata,
`.Rproj.user`, regenerated `man/*.Rd`. A `PreToolUse` hook in this plugin flags it.

## 2. If a submodule pointer is staged, verify it exists on the remote

This incident broke every worker node on a shared cluster:

> The superproject recorded the submodule at a SHA that was **another session's
> commit**, and had not been pushed. It landed in the submodule working tree
> between my install and my `git add packages/<pkg>`, and `add` stages
> whatever HEAD is at that moment. Every node then failed to sync:
> `fatal: remote error: upload-pack: not our ref c7be5647`.
>
> **LESSON: verifying the renv.lock diff before staging is not enough. A
> submodule pointer must be checked at STAGE time against what is actually on the
> remote, because `git add <submodule>` reads a moving target in a shared worktree.**

For each staged gitlink:

```sh
sha=$(git ls-files -s <submodule> | awk '{print $2}')
git -C <submodule> fetch --quiet origin
git -C <submodule> branch -r --contains "$sha"      # must print something
```

If it prints nothing, stop: the SHA is local-only. Push the submodule first, or
unstage the pointer.

Also confirm the pointer agrees with the version recorded in `renv.lock` -- these
have silently disagreed before.

## 3. Write the subject

Conventional Commits with a scope: `type(scope): subject`.

Types actually used, in frequency order: `feat`, `fix`, `chore`, `docs`,
`refactor`, `perf`, `revert`, `build`, `style`. Scopes name the pipeline area (`deps`, `calibration`, `fire`, `growth`) or the
sub-project (`prep-fit:`, `predict:`). Package repos also use a `[vX.Y.Z]` subject
prefix on the commit that bumps `Version:`.

**The subject states the decision, not the area touched.** Lowercase, no trailing
period, and **under about 70 characters**:

```
fix(ic): landis_datatype() takes the max map code
fix(growth): treat the comparator sets as priors
revert(ic): keep overrideBiomassInFires ON
```

A contrast ("X, not Y") earns its place only when the contrast *is* the decision and
the wrong option was actually taken. As a reflex it is filler -- and the same
constructed contrast is banned in report prose.

ASCII only: `--` for a dash, `->` for an arrow.

## 4. Keep the body to one to three lines

> "Commit with a succinct message (imperative subject + 1-3 body lines; long
> forensics belong in NEWS / the PR body, not the commit)."

That is the project rule, and it is the one to follow. Say **why**, in a line or two;
the diff already shows what changed. Wrap at ~90 characters.

```
chore(landisutils): bump to 0.0.152 for the FPSM log-check fix

Only a benign missing-substitution-factor message no longer fails a run.
```

**Do not infer the style from `git log`.** Most recent commits in these repos are
machine-written and much longer than this rule, because correcting each one was more
tedious than letting it stand. The log is not the standard; this is.

Where the long version belongs instead:

| Material | Goes in |
| --- | --- |
| measurements, falsified hypotheses, dead ends | the pull request body, or a `_tmp_<slug>.md` for review |
| user-visible behaviour change | `NEWS.md` (packages) |
| a change to numbers a report states | one line in the commit saying results change, with the accounting in the README's corrections section |
| a process lesson | the project's `CLAUDE.md`, where it will actually be read again |

## 4a. If the change goes through a pull request

Keep it to roughly 150-250 words, in this order: why the change was needed, what it
does, how it was verified (exact numbers), and **what was not done or not checked**.
That last part is the most useful section in the record and the easiest to omit.

Use the repository's PR template where one exists, and answer its checklist honestly
-- annotate a box that does not apply with the reason rather than ticking it.

## 5. Trailer

```
Co-Authored-By: Claude <model> <noreply@anthropic.com>
```

Use the actual model name, as the corpus does: `Claude Opus 5 (1M context)`,
`Claude Opus 4.8`. Trailer discipline is currently inconsistent (some
agent-authored commits carry none) -- always add it.

Do **not** add a `Generated with Claude Code` footer; there are zero in the corpus.

## 6. Repo-specific extras

- **R packages**: add a `NEWS.md` entry and bump the version. Run `devtools::document()` first if
  roxygen changed.
- **Pipeline / analysis projects**: `NEWS.md` is typically **not** maintained --
  check before adding an entry.
- `[skip-ci]` in the subject skips CI where CI exists.
- These repos commit directly to a long-lived branch; there is no PR or squash
  workflow. Do not open a PR unless asked.

## 7. Do not push

Push only when the user asks. If you do push, never bare `--force` -- use
`--force-with-lease` (a hook enforces this).
