---
name: gh-dependabot-batch-pr
description: >
  Use when the user says "batch the dependabot PRs", "consolidate the dependency
  bumps", "merge the dependabot updates into one PR", or hands over a pile of
  Dependabot bump PRs, lines, or a screenshot. NOT for single-PR creation —
  that is gh-pr-create.
---

# Dependabot Batch Pr

GitHub Dependabot only. There is no Origin twin. If the session workshop is
Origin, wait until GitHub `main` has the fast-forward before batching
Dependabot PRs.

## Execution Backend

1. Verify `git` with `git --version` and `gh` with `gh auth status`.
2. Run the bundled scripts and plain `git`/`gh` workflow below.
3. If either verification fails, STOP and report the failed check. For a `gh`
   failure, report verbatim: "`gh` is missing or unauthenticated. Install it if
   needed, run `gh auth login`, then retry."

> **GH CLI:** Scripts call plain `gh`. Ensure `gh auth status` is green before running.

## Overview

Batch pending Dependabot updates into one branch and open one PR after validation. Prefer live GitHub PR data when available, but support text or screenshot-derived bump lines.

## Stale injected skill paths

If the injected skill path points at an old plugin-cache version and reading `.../skills/gh-dependabot-batch-pr/SKILL.md` fails with `No such file or directory`, treat that as a recoverable routing problem. Re-resolve the live skill path immediately instead of stopping on the dead versioned path:

1. Prefer the current workspace copy when already inside the `this-skills-repo` repo.
2. Otherwise locate the installed skill with a targeted search such as `rg --files ~/.codex/plugins/cache ~/.claude/plugins/cache | rg '/gh-dependabot-batch-pr/SKILL\.md$'` and pick the newest matching version.
3. Recompute `<skills-dir>` from the recovered live directory before running any bundled `scripts/`, then continue the workflow.

Do the same for sibling skills named in the prompt, especially `$gh-pr-create` and `$slack-fallback`, because these automations often pin a cache version that has already been evicted.

Treat the skill name as canonical. A dead versioned cache path is a routing problem, not a GitHub or Dependabot failure.

## Workflow

1. Capture the update set.
   - Preferred: query open Dependabot PRs from current repo.
     ```bash
     python <skills-dir>/gh-dependabot-batch-pr/scripts/collect_dependabot_updates.py --from-gh --write-json tmp/dependabot-updates.json
     ```
   - Text fallback:
     ```bash
     python <skills-dir>/gh-dependabot-batch-pr/scripts/collect_dependabot_updates.py --input-file <path-to-lines.txt> --write-json tmp/dependabot-updates.json
     ```
   - Screenshot fallback: extract PR title lines from the image context first, then parse those lines with `--input-file` or stdin.

2. Create a dedicated branch.
   - Use a deterministic branch name such as `chore/dependabot-batch-YYYYMMDD`.
   - Ensure base branch is current before applying updates.

3. Generate batched install commands and apply updates.
   - For npm repos:
     ```bash
     python <skills-dir>/gh-dependabot-batch-pr/scripts/collect_dependabot_updates.py --from-gh --npm-install
     ```
   - Run the emitted commands (grouped by prod/dev dependencies) to update `package.json` and lockfiles.
   - If bump extraction contains unknown scopes, review and assign `--save` vs `--save-dev` explicitly.

4. Run full quality gates.
   - Execute the standard quality runner:
     ```bash
     python <skills-dir>/gh-dependabot-batch-pr/scripts/run_repo_checks.py --require-scripts
     ```
   - Then run any additional repo-specific commands not represented in `package.json` scripts.
   - Do not proceed to PR if checks fail.

5. Perform a thorough review before PR.
   - Inspect diff and lockfile churn:
     - `git diff --stat`
     - `git diff`
   - Run the repository-aware `code-review` guard once on the complete batch,
     with `--uncommitted` (or `--base main` if already committed). First inspect
     the effective `.coderabbit.yaml` filters and prove they exclude the
     repository's actual lockfile paths. If they do not, omit lockfile paths
     with an exact directory scope or defer the CLI pass as filtered coverage
     unavailable; never assume lockfile-only churn is excluded. The pass targets
     config and manifest changes. Before `--uncommitted`, use an isolated worktree or
     verify every tracked edit belongs to this dependency batch and contains no
     credential. See `CONVENTIONS.md` "Code review before push and merge".
   - Focus review on:
     - major-version bumps
     - breaking config changes (lint/test/build tools)
     - transitive lockfile anomalies
   - If risk is high, split only the problematic bump(s), keep the rest batched.

6. Open one PR using `$gh-pr-create`.
   - Invoke `$gh-pr-create` after checks pass and changes are staged/committed.
   - PR shape follows `gh-pr-create` standards: never a draft unless the user asked (drafts get no bot review); title in the repo's convention (read recent merged PR titles first); body opens with the plain-language problem ("N Dependabot PRs open against <repo>; batching them cuts CI churn and review noise"), not a bump inventory; the bump list, validation commands, and any excluded updates follow. No AI markers or attribution lines anywhere — PR body or commits.

7. Close superseded Dependabot PRs after batch PR creation.
   - Resolve the newly opened batch PR URL:
     ```bash
     BATCH_PR_URL="$(gh pr view --json url -q .url)"
     ```
   - Run a dry run first:
     ```bash
     python <skills-dir>/gh-dependabot-batch-pr/scripts/close_superseded_dependabot_prs.py --updates-json tmp/dependabot-updates.json --batch-pr-url "$BATCH_PR_URL" --dry-run
     ```
   - Apply closure:
     ```bash
     python <skills-dir>/gh-dependabot-batch-pr/scripts/close_superseded_dependabot_prs.py --updates-json tmp/dependabot-updates.json --batch-pr-url "$BATCH_PR_URL"
     ```
   - If `tmp/dependabot-updates.json` lacks `pr_number` fields (text/screenshot-only flow), recollect via `--from-gh` before closing.
   - Any closure/backlink comment you compose yourself (outside the script's fixed backlink) states the superseding batch PR and the reason in one line.


## Gotchas

1. **Major-version bumps can be silent breaking changes** -- lockfile diffs for a major bump often look small but break runtime behaviour (new default options, removed APIs). Always inspect major bumps individually and run tests before including them in the batch.
2. **Stale injected skill paths fail noisily** -- if automation injects an old
   absolute path to this skill and that path is gone, re-resolve the live skill
   directory and continue. Do not treat stale path failure as a missing-skill
   condition.
3. **Closing Dependabot PRs before the batch PR merges can lose context** -- use `--dry-run` first; confirm the batch PR URL is valid and the PR is open (not draft) before closing superseded PRs. The batch PR itself must not merge until the CodeRabbit App review (where installed) has posted and its threads are handled — green Actions alone are not the merge gate (`CONVENTIONS.md` "Code review before push and merge").
4. **`tmp/dependabot-updates.json` from text/screenshot flow lacks `pr_number`** -- closing superseded PRs requires re-collecting with `--from-gh` to populate `pr_number`; the text-only path cannot close PRs without it.
5. **Quality gates must pass before PR creation** -- if `run_repo_checks.py` fails, do not open the PR and ask for workaround. A broken batch PR is harder to revert than individual Dependabot PRs.

## Addressing PR review comments after merge

If the batch PR receives review comments, **do not inline-implement comment addressing**.
Load `gh-address-comment` explicitly before making any code changes:

```
Skill: <skills-dir>/gh-address-comment/SKILL.md
```

Ops workers / Savart: load `gh-address-comment` explicitly before starting code changes. Do NOT re-implement git checkout + edit + commit logic inline.

## Review Expectations

- Treat this as a production-risk change, not routine formatting.
- Ensure final PR notes include exact test/build commands that were run.
- If no meaningful tests exist, state that explicitly and include manual verification steps.

## Bundled Resources

- `scripts/collect_dependabot_updates.py`
  - Parse Dependabot bumps from live PRs or raw text and emit normalized update sets / npm commands.
- `scripts/run_repo_checks.py`
  - Run repo quality gates based on discovered `package.json` scripts.
- `scripts/close_superseded_dependabot_prs.py`
  - Close superseded Dependabot PRs and leave a backlink comment to the aggregate PR.
- `references/workflow-cheatsheet.md`
  - Quick command reference and failure-handling policy.
