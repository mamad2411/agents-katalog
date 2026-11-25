---
name: loopmath-record-run
description: "Record a finished agent run in loopmath with one command, from the session ids noted while the work ran, with test results and scores, then show the receipt: predicted against actual cost, and the outcome. Use when a task planned with loopmath is done, when the user asks to record, log or save a run in loopmath, or when both runs of a loopmath pair are done and need a blind judge."
allowed-tools: Bash(loopmath:*), Bash(open:*), Bash(xdg-open:*)
---

# Record a run with loopmath

One command records the whole run: one attempt per session (a Claude Code session counts its sub-agents), the commits made since the base commit, the verdicts and scores, the cost from the logs, the receipt and a background refit. Ask nothing unless you cannot tell which sessions did the work.

Use exactly the commands below, and read their JSON as printed. Flags and fields are in `reference.md` next to this file. Never run `--help`.

## 1. Gather what the command needs (no question)

- **The run.** The run id from `loopmath run start` earlier in this conversation. If you do not have it, run `loopmath status --json` and read `open_runs[]` (`run`, `type`, `repo`, `started_at`). Take the entry whose type and repo match the task, the latest first. With no open run, record with the second form in step 2.
- **The sessions**, one `--session [PIECE=]ID` each. The ID is a session id the user gives you (as given), the UUID you gave `claude --session-id`, the `thread_id` from `codex exec --json`, or the word `self` only for work you did yourself in this Claude Code session (in Codex, give your own piece with `--cwd PIECE=PATH`). `PIECE=` is optional: a piece of the run (`plan`, `implement`, `review`), never `self`. So a session the user ran is `--session UUID`, or `--session implement=UUID` when you know it implemented. For a piece run by an agent with no session id (interactive Codex, for example), give `--cwd PIECE=PATH`, the folder it worked in. Outside a Claude Code tool shell, `--session self` uses the one Claude Code session in this folder active in the last 10 minutes; otherwise run `loopmath run sessions` and pass the id.
- **The verdicts.** If the task has tests, you can run them, and nobody has run them since the last change, run them now. Your own observations are `--verified` (a test command's exit code, CI status read from its API, a merged PR). What an agent or the user told you is `--reported`: the user saying the tests passed is `--reported tests=pass`. Values: `pass`, `fail`, `accept`, `reject`, `error`.
- **Scores**, when the user's goal names one (`--score runtime_s=182`). A score you could not measure: `--score NAME=`.

Only if you cannot tell which sessions did the work, ask the user once.

## 2. Record

```sh
loopmath run record --run RUN --session UUID --session review=THREAD_ID \
  --verified tests=pass --reported review=accept --json
```

Without a run from `run start`, the same command opens one. In place of `--run RUN`, give `--rec REC --choice KEY` when the task was planned with loopmath (the choice the user made; for a pair, start it with `run start` and record each run with `--run`). Else give the task and the workflow that ran, with source `habit`:

```sh
loopmath run record --type TYPE --repo REPO --title "TITLE" --workflow SHAPE \
  --set PIECE=HARNESS:MODEL:EFFORT --source habit --session self --since TS --verified tests=pass --json
```

`--since TS` (an ISO time, or `2h`) is when the work on this task began. Give it when this session did other work before the task (else the whole session counts), and whenever you use `--cwd` without `--run`. With `--run`, a session that started before the run is counted from the run's start; give `--since TS` (and `--until TS`) when the task's work began or ended at another time. A Codex session counts the usage it logged inside the window: each reading's increase at the reading's time, a reading on either edge included. A sub-agent or a Codex child thread counts in full when it started inside the window, and not at all when it started before it. A Codex reading lower than the one before it (a compaction reset) counts from zero. A Codex session that cannot be cut to the window counts whole, with a note that says why: a reading with no time, or increases inside the window that add up to less than zero.

Read `run`, `attempts[]` (`piece`, `session`, `model`, `how`), `unmatched[]` (`attempt`, `reason`), `commits[]` (`sha`), `signals[]`, `cost.usd`, `outcome`, `receipt.line`, `fit.started`, `notes[]`.

If it exits 2 because a session is not in the logs, check the id against what you noted and retry once with the right id. Never guess an id. If it exits 1, the message names the flag to fix; fix it and retry once. An error writes nothing, so a retry never records twice.

## 3. Show the result

```sh
loopmath runs --run RUN --html
```

It prints the page path. Open it (`open PATH` on macOS, `xdg-open PATH` on Linux); if that fails, give the path. Then end with at most 5 lines:

> Recorded run_01M3...: accepted (tests pass, verified).
> Predicted $1.20 (0.60 to 2.10), actual $0.97: inside the range.
> 3 attempts: plan (self), implement (claude-sonnet-5), review (gpt-6-astra); 2 commits.
> Run page: /Users/me/.loopmath/views/runs-20260924-190211.html

The second line is `receipt.line`. Report every `unmatched` entry and every note as it is. Never fill in a cost or a session yourself.

## 4. Pairs: judge blind, after both runs are recorded

When the run belongs to a slate (a pair from `loopmath-plan-task`) and both runs are recorded:

1. `loopmath config get referee.model --json`: launch a fresh agent of that family (a family other than both runs' implementers when `value` is null).
2. Give it the task and the two diffs in random order as A and B, without run ids, workflow names or models, with this prompt:
   "Two changes attempt the same task. Judge which one better completes the task as stated, considering correctness, tests, scope and code quality. Answer A, B or tie, then give three sentences of reasons."
3. Map A or B back to its run and record:

   ```sh
   loopmath outcome --slate SLT --prefer RUN --judge referee --blinded --json
   ```

   (`--prefer tie` for a tie.) Keep the preferred change. The other worktree is the user's to delete.

## Later

When the user mentions an incident, revert or hotfix tied to a commit made under loopmath:

```sh
loopmath outcome --commit SHA --signal incident=REF --kind event --source user --json
```

## Never

- Do not record another person's sessions.
- Do not mark a verdict `--verified` unless you observed it yourself.
- Do not edit files under `~/.loopmath` or `$LOOPMATH_HOME` by hand.
