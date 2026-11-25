---
name: autoresearch
description: Measured software improvement loop for codebases. Use when asked to improve a project through small experiments with measurable metrics, baselines, safe scope, experiment budgets, commits/reverts, logs, and a final report across frontend, backend, mobile, CLI, parser/classifier, AI/ML, library, full-stack, test reliability, performance, build reliability, developer experience, accessibility, documentation, or code simplification work.
---

# Autoresearch

## Purpose

Use this skill to improve a software project through a measured experiment loop. The loop must ask clarifying questions, select a safe scope, establish a baseline, run small experiments, measure results, keep improvements, revert failures, and summarize findings.

Autoresearch is for improving a project. Do not use it to merely explain code, perform a one-shot requested edit, run broad refactors without metrics, or redesign unrelated product areas.

## Required order

1. Inspect the repo structure and identify available package scripts, test commands, benchmark commands, and project conventions.
2. Ask clarifying questions before any baseline, branch creation for experiments, edits, or experiment loop.
3. Refuse to proceed if no measurable metric exists.
4. Establish a clean baseline.
5. Run the experiment loop.

Never run autoresearch on a repo just because this skill file is being created or edited.

## Clarifying questions

Ask concise questions that lock these decisions before proceeding:

- Project type: frontend app, backend API, mobile app, CLI tool, library/package, parser/classifier, AI/ML experiment, full-stack app, or unknown/mixed project.
- Main improvement target: build reliability, TypeScript errors, test pass rate, parser accuracy, bundle size, runtime performance, API latency, memory usage, accessibility, Lighthouse score, code simplification, flaky test reduction, developer experience, documentation quality, or another target.
- Exact metric: define the number or boolean being optimized and whether lower or higher is better.
- Metric command: the command that produces or verifies the metric, such as `npm run build`, `npm run typecheck`, `npm test`, `npm run test:parser`, `npm run lint`, `npm run analyze`, `npm run bench`, `pytest`, `go test ./...`, `cargo test`, or `dotnet test`.
- Approved scope: directories and files safe to modify.
- Forbidden scope: files, directories, systems, or behaviors that must not be touched.
- Experiment budget: number of experiments to run. Default to 10.
- Risk level: conservative, moderate, or aggressive.
- Git behavior: create a branch only, commit kept experiments, push branch to GitHub, or open a PR if tooling is available.
- Final output format: short summary, full experiment log, PR-ready report, or next-step recommendations.

## Defaults for incomplete answers

Use these defaults only after asking:

- Project type: unknown/mixed.
- Experiment budget: 10.
- Stop early after 5 consecutive failed non-improving experiments.
- Risk level: conservative.
- Final output format: PR-ready report.
- Git behavior: create a branch and commit kept experiments locally; do not push or open a PR unless approved.
- Forbidden scope: `.env` files, secrets, auth flows, payment logic, database migrations, lockfiles unless approved, generated files, unrelated UI redesigns, and public API changes unless approved.

Do not infer the exact metric. If the user gives a target without a measurable metric, ask again. If a metric command is missing, inspect likely commands and ask the user to approve one.

## Safety boundaries

- Keep every experiment within approved scope.
- Prefer the smallest useful change.
- Avoid dependency changes unless explicitly approved.
- Do not alter secrets, credentials, environment files, auth, payments, migrations, generated files, or public APIs unless explicitly approved.
- Do not run destructive commands outside the intended repo.
- Do not keep changes that pass the metric but violate scope, introduce obvious regressions, or make the project harder to review.
- Do not hide failures. Log them.

## Baseline procedure

1. Confirm the working tree state with `git status --short --branch`.
2. If unrelated user changes exist, do not overwrite or revert them. Ask how to handle them if they block the baseline.
3. Create a branch named `autoresearch/[metric-or-goal]`, using a lowercase, hyphenated metric or goal.
4. Create local ignored logs in the repo root:
   - `results.tsv`
   - `run.log`
   - `autoresearch-notes.md`
5. Add these log files to `.git/info/exclude`, not `.gitignore`.
6. Run the metric command once without edits.
7. Write command output to `run.log`.
8. Extract the baseline metric.
9. Record the baseline in `results.tsv` with this tab-separated header:

```tsv
experiment	commit	metric	status	description
```

Use this baseline row format:

```tsv
baseline	<commit-or-working-tree>	<metric>	baseline	<metric command>
```

## Experiment loop

For each experiment:

1. State one hypothesis before editing.
2. Make the smallest useful change inside approved scope.
3. Check the changed files before measuring.
4. Commit the experiment before measuring.
5. Run the metric command.
6. Append command output to `run.log`.
7. Extract the metric using the same interpretation as baseline.
8. Run any required safety checks for the project and scope.
9. Keep the commit if it improves the metric and passes safety checks.
10. Revert the commit with `git reset --hard HEAD~1` if it regresses, breaks checks, crashes, changes forbidden scope, or cannot be measured.
11. Append one result row to `results.tsv`.

Result rows must use:

```tsv
<experiment-number>	<commit-sha-or-reverted>	<metric>	<kept|reverted|crashed|blocked>	<hypothesis/result summary>
```

## Revert rules

Revert the current experiment with `git reset --hard HEAD~1` when:

- The metric is worse.
- The metric command crashes after a change.
- Required checks fail.
- Forbidden files or behavior changed.
- The change exceeds approved scope.
- The metric cannot be extracted reliably.

If a command is broken before any experiment, stop and report that the baseline cannot be established. If the metric command becomes broken and cannot be repaired safely within approved scope, stop.

## Stop conditions

Stop when any condition is met:

- Experiment budget is reached.
- 5 consecutive experiments fail to improve the metric.
- The metric command is broken and cannot be repaired safely.
- Required scope exceeds approved boundaries.
- The user asks to stop.

## Git workflow

- Use `git status --short --branch` before branching, before each commit, and before the final report.
- Branch name: `autoresearch/[metric-or-goal]`.
- Commit each experiment before measuring.
- Keep improving commits in history.
- Reverted experiments should not remain in history after `git reset --hard HEAD~1`.
- Push or open a PR only if the user approved that Git behavior.
- Never fake a push or PR. Verify remote and branch state before reporting success.

## Final report format

Include:

- Baseline metric.
- Final metric.
- Percentage improvement if applicable.
- Kept experiments.
- Discarded experiments.
- Crashed experiments.
- Top winning changes.
- Files changed.
- Risks introduced.
- Suggested next human-review tasks.
- Exact commands run.

Keep the final report proportional to the requested output format. For PR-ready reports, include a concise summary, validation, risk notes, and review checklist.

## Example invocations

- "Use autoresearch to reduce TypeScript errors. Ask me questions first. Use `npm run typecheck` as the metric command."
- "Use autoresearch on parser fixtures. Improve fixture pass rate with `npm run test:parser`. Only touch `src/parser` and `fixtures`."
- "Use autoresearch to lower API p95 latency. Use the detected benchmark command. Do not touch auth, payments, or migrations."
- "Use autoresearch to reduce flaky tests. Use `npm test`. Run 10 conservative experiments and give me a PR-ready report."
