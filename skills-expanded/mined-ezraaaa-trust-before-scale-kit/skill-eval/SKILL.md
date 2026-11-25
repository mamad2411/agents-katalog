---
name: skill-eval
description: "Run, read or extend the evals proving review skills still catch real faults. Use when a review skill changed, before a release, when the eval check is red, or to add a seeded fault after a review miss."
---

# Skill evals

- **Run a suite:** `node scripts/tbs/skill-eval.mjs <suite>` (suites are in `.agents/trust-before-scale.json` (falling back to `.claude/trust-before-scale.json`)).
  It writes `evals/<suite>/result.json`; commit it. Each review case runs the review headless (the configured suite `reviewer`, default `claude`) and a
  configured judge (default `codex`) on a different model, so a full run costs real tokens: run it when the skill changes and weekly.
- **One case:** `--case <id>` prints the result and never writes the record.
  A missing ID or a value starting with `-` prints usage and exits with status 2.
- **Check:** `--check` fails when a skill changed, a case failed, the record is missing, its `evidenceRule` differs from 4, or its `settingsHash`
  is missing or differs from the effective review prompt/model, judge (including `TBS_JUDGE_MODEL`), repeats,
  base or link directories. `--check --fresh` (lanes, self-merge) also fails a record older than `maxAgeDays`, and,
  for suites with gate cases, one whose gate fingerprint is missing or no longer matches the checkout. Plain `--check`
  (CI) does not compare fingerprints: a PR that changes a gate cannot refresh its record until the change is merged.
- **Add a case** after any miss: `evals/<suite>/cases/<id>/case.json` and `seed.patch`, a real diff against the
  current base that a person could plausibly ship. Neither the added lines, the branch name nor the message may say
  any whole word (case-insensitive) from: eval, seed, test, judge, rubric, score, candidate, benchmark,
  planted, fixture. Unchanged context is excluded; identifiers such as `testCount` are allowed. `expect` is
  `gate` when a command already catches it (name the command), else `review` with `rule`, `file` and `mustName` tokens. The evidence must quote the review
  and state the fault at that file. It must contain the file basename as a case-insensitive substring and at least one literal, case-insensitive whole `mustName` token.
  A gate must pass on the clean base, in its own throwaway checkout, before its failure on the seed can count. Both runs
  share the repository's refs and config and the `linkDirs`: link only read-only dependencies (such as `node_modules`),
  and a gate must leave no state there (tags, branches, config, caches).
  The fingerprint captures the gate command, its entry script and transitive literal relative imports before the
  clean gate runs. List additional inputs in the case's optional `gateInputs` array, for example
  `["scripts/lib/**", "package.json"]`. Use repository-relative Git glob patterns without `..`; only tracked files count, for imports too. Import scanning is pattern-based,
  not a parser: list in `gateInputs` anything a gate loads in an unusual way.
- **A seed that no longer applies** is rewritten against the current code. Never delete a case to make a suite green.
- A failing case is a finding about the skill: fix the skill, rerun, and commit the new record with the skill change.
- **Dry run:** `<suite> --dry-run` prints the effective judge and checks each patch with `git apply --check`
  against the suite base. `STALE <id>` fails the command. Dry runs, real runs and `--check` all fail for an
  empty suite, with a hint to add 3–8 cases from real failures.
- **Judge:** suite `judgeModel` is optional. `TBS_JUDGE_MODEL` takes precedence; with neither set, Codex uses
  its default (no `--model` argument).
- **Repeats:** optional suite `repeats` is a positive integer and defaults to 2. Every repeat must pass.
  Each case in `result.json` records `passes` and `repeats`; `--check` reads an old record without `repeats` as one run and requires
  a new run when the configured repeat count changes.

Blind review cases use a hermetic repository containing only a sanitized base snapshot and the seeded commit; hidden answer keys are absent from both files and git history. Optional suite `hidePaths` adds repo-relative paths to the defaults (`evals`, `.agents/trust-before-scale.json` (falling back to `.claude/trust-before-scale.json`), `docs/trust-before-scale`, `scripts/tbs`); these must not overlap skills or linked directories.

Blindness covers everything reachable from the review clone and its git data. Review `linkDirs` point to isolated copies shared across the run, and kept reviews default to `<project git common dir>/tbs-reviews` (override with `TBS_REVIEW_DIR`). Gate cases retain links to the real checkout. The reviewer still runs with the user's normal filesystem access: a reviewer that already knows the project's absolute path can open it.
