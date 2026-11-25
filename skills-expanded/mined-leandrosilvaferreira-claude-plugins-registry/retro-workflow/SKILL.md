---
name: retro-workflow
description: >
  Mines the project's Claude Code session transcripts for repeated friction (hook blocks,
  tool errors, corrections, declined or unapplied proposals), shows the ranked findings,
  asks the human to decide each proposed harness fix, applies the approved ones, and
  records every decision in the proposal ledger. Use through /aia-harness:retro, or when
  the user asks to review past sessions and improve the harness.
argument-hint: "[path] [--since=YYYY-MM-DD]"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - AskUserQuestion
  - Skill
---

# Retro workflow

Input: a resolved absolute project path, then an optional `--since=YYYY-MM-DD`.

## Hard rules

- Never open an issue or a PR in the `aia-harness` repository. Never send anything there.
- A fix to a plugin-provided artifact stays in this project. Record it in the ledger with `origin` `plugin`. The next `patch` shows it as a local fix.
- Never write the report to a file in the repository. Only the ledger line goes to disk.
- Never run `git stash`.
- `Current branch` applies the edit and shows the diff. It never commits.
- The human decides every gate with `AskUserQuestion`.

## Steps

1. Run the scan. Use `timeout` 600000.

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/harness.mjs" sessions-scan "<path>" [--since=YYYY-MM-DD] --json
   ```

   Exit codes:
   - 0: report written to stdout.
   - 1 with the stderr message `no Claude Code transcripts found for <path>`: no transcript for this project. Tell the user and stop.
   - 2: wrong usage (bad option or bad `--since`). Show stderr and stop.
   - Any other non-zero exit, or exit 1 with any other stderr message: a crash. Show stderr and stop. Do not retry and do not read a partial report.

   Exit 0: read the `SessionsReport` JSON. If `drift.warning` is not null, show it first. For an applied fix, `before` also counts days before the scan window, so a fix whose friction stopped reads `improved`.
2. **Decision D0.** Run this step only if the ledger has a line with status `open` and `ref` `#n`, and `gh` works. Read the state of each PR or issue with `gh`. Then ask one `AskUserQuestion`: mark the merged ones `applied`? On yes, show the old and new line, then change the line with `Edit`.
3. Show a table of the first 10 `findings`: `kind`, `key`, `sessions`, `per100`, `artifact`, `origin`, `ledger` state.
4. Pick up to 4 candidates in ranking order. Skip:
   - an environment failure (network, expired auth);
   - a `declined` ledger line when the signal count after its date did not grow;
   - an `open` ledger line already in progress.

   For each candidate, read the artifact. Compute `origin` yourself: `plugin` if the artifact belongs to the harness plan (`plan --json`, same file or inside a `copyFrom` directory), else `project`. This overrides the report if they differ.
5. **Decision D1.** Ask one `AskUserQuestion` with one question per candidate (4 at most). Each question:
   - states what failed, with the report numbers;
   - states the workaround that worked and the minimum fix;
   - lists the files and mirrored copies that change;
   - says whether the fix changes policy (a gate, a merge rule, a permission);
   - ends with `(signature: <kebab-case-slug>)`.

   Options:
   - `Own branch and PR (recommended)`
   - `Current branch`
   - `Open issue` (this project's tracker)
   - `Do not apply` (the user gives the reason under Other)
6. For each answer, build one ledger line. Keep it in memory. Do not write it yet: step 8 writes it, after the fix, so `ref` is known. The format is:

   ```text
   - <date> | <signature> | <artifact> | <origin> | <signal> | <decision> | <status> | <ref> | <reason>
   ```

   - `decision`: `pr`, `branch`, `issue` or `declined`. `declined` needs status `not-applied`.
   - `status`: `open` until the PR or issue is merged or closed; `applied` for `Current branch`.
   - `signal` and `ref`: `-` when none. `ref` is `#n`, a commit hash or a URL. Any non-empty value without `|` is accepted. Prefer one of these forms.
   - `date`: the local date.
   - `reason`: one line, 300 characters at most. For `Do not apply` with no reason: `no reason given`.

   If the ledger file does not exist, create it with `Write`: the title `# Harness proposal ledger`, the marker `<!-- aia-harness:proposal-ledger v1 -->` and its two format comments, then the line.
7. **Lens check (optional).** Run this step before step 8, only if an approved D1 answer edits a file that matches `review.lensGlobs` (or the rule that lens reads) and `.claude/evals/cases/` has approved cases. Ask with `AskUserQuestion`: `Check with the lens replay before applying?`. Show the estimated runs and cost from `lens-run --estimate`. On yes: `Read` `skills/lens-check-workflow/SKILL.md` and follow its `run` mode on the edit (the working tree for `Current branch`, or the `harness/<signature>` branch). The user gives the budget. A verdict is advice. Never skip a gate because of it.
8. Apply each approved proposal, then write its ledger line (show it first) with `Edit` to `.claude/harness-proposals.md`, in the user's checkout. Never change the user's checkout branch for a fix.
   - `Own branch and PR`: work in a separate worktree.
     1. Resolve the default branch: `git symbolic-ref refs/remotes/origin/HEAD` (strip `refs/remotes/origin/`). Else the current branch's upstream. Else `main`.
     2. `git worktree add <tmp> -b harness/<signature> <default-branch>`. Use a path under the OS temp directory for `<tmp>`.
     3. Apply the edit in `<tmp>` and show the diff.
     4. Ask with `AskUserQuestion` whether to commit, push and open the PR. Do nothing outward without a yes.
     5. On yes: commit, `git push -u`, `gh pr create` (all from `<tmp>`). Set `ref` to the PR number. On no: `ref` is `-`.
     6. `git worktree remove <tmp>`, also after a failure.
     7. Write the ledger line in the user's checkout, with `ref` filled, in one edit.
   - `Current branch`: apply the edit and show the diff. Do not commit.
   - `Open issue`: if `.claude/commands/pm/ticket-new.md` exists, use `/pm:ticket-new`. Else if the remote is GitHub, use `gh issue create` in the project's own repository. Else put the issue text in the final report.
9. An artifact with `origin` `plugin`: apply the fix in this project and record `origin` `plugin`. Never touch the plugin copy. A local fix is protected by the last ledger line for its signature. An artifact ending in `/` covers every file under that directory.
10. **Decision D2.** Ask with `AskUserQuestion` whether to run another round with the next 4 candidates. Allow 3 rounds at most.
11. Final report, in chat only: one line per decision (ledger line and `ref`), the `lensGaps` count only, and a reminder to commit the ledger file. If `lensGaps` is above 0, add one line that offers `/aia-harness:lens-check add`.
