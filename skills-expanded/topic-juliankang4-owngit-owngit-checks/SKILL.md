---
name: owngit-checks
description: Run and report OwnGit project checks from an active coding session. Use when the user asks to run, record, or verify OwnGit checks, or to reserve a correction round for a task.
---

# OwnGit checks

Use this skill inside an already active coding session that the user has
permitted to run project commands. It does not start, resume, or change a
session, model, or team, and it does not install anything. Follow the user's
existing project and team instructions; this skill does not replace them.

## Prerequisites

Inspect the supplied and project-known facts first: the installed `owngit`
binary, the server origin, the repository identifier, and the helper credential
file. Ask the user only for missing choices that belong to them. Do not ask the
user to re-enter a fact that is already available.

The credential file is owner-readable and contains an OwnGit-scoped helper
token, not a provider subscription token. Never pass the token as a command
argument, write it into a document, or print it in a log.

Inside a clone whose `origin` remote is the OwnGit clone address
(`http(s)://HOST[:PORT]/git/ID.git`), you may omit `--server` and
`--repository`. The helper reads them from `origin` and names them on standard
error. It sends the credential to that server only when the credential file's
first line names it (`owngit-server: ORIGIN`); otherwise it stops with
`credential_origin_required` or `credential_origin_mismatch`. Do not add or
change that line yourself. Report the error and ask the user.

Do not add `--accept-insecure-http` on your own. Plain HTTP is unencrypted, and
the user must accept that risk for the private connection.

## Workflow

1. Create one stable task for the unit of work. Reuse its identifier across
   revisions instead of creating a new task for every commit.

   ```sh
   owngit check task new \
     --server SERVER --repository REPOSITORY \
     --credential-file CREDENTIAL_FILE \
     --title "TITLE"
   ```

2. Run the checks. Prefer the project's committed configuration by omitting
   `--check`: the helper then runs only the checks in the `.owngit/checks.json`
   committed in the revision being tested. Pass explicit `--check name=command`
   values only when the user asks for a specific command or the revision has no
   committed configuration (`checks_not_configured`).

   ```sh
   owngit check run \
     --server SERVER --repository REPOSITORY \
     --credential-file CREDENTIAL_FILE \
     --task TASK_ID
   ```

3. Read the JSON result and the process exit code. Report the attempt status,
   the tested revision, the worktree state, the per-check results, and the
   remaining correction cycles. Report remaining cycles only from `task` in an
   uploaded run or from `check status`.

4. If a check failed and the user asks for a correction, reserve one round
   before asking for the correction, then pass the `cycle.id` from the reserve
   response as `--cycle` to the verifying run. A correction already authorized
   in the active task may continue within the budget without asking again. Do
   not start an unrequested fix.

   ```sh
   owngit check cycle reserve \
     --server SERVER --repository REPOSITORY \
     --credential-file CREDENTIAL_FILE --task TASK_ID

   owngit check run \
     --server SERVER --repository REPOSITORY \
     --credential-file CREDENTIAL_FILE \
     --task TASK_ID --cycle CYCLE_ID
   ```

5. Read durable state with `check status --task TASK_ID`,
   `check log --attempt ATTEMPT_ID`, and `check cycle list --task TASK_ID`.
   `check config show` shows the configuration recorded most recently from any
   branch; it is not what `check run` uses.

## Reading the result

`check run` prints one JSON object and exits with a code:

- `0`: every check passed. Read `registered` and `uploaded` to see whether the
  attempt was recorded; a local `--no-upload` run also exits 0.
- `1`: at least one check did not pass.
- `2`: this client could not confirm that the attempt was recorded.
- `128` plus the signal number: a signal stopped the run (`130` for Ctrl-C,
  `129` for a closed terminal, `143` for `SIGTERM`). Once registration has
  started, the attempt is still recorded, and this status holds even when the
  checks had already passed. It is `2` instead when the record is unconfirmed,
  and `1` when the checks had finished without passing before the signal or a
  check ended in `error`.

An error object (`{"ok":false,"error":{...}}`) with exit code `1` instead of a
result means nothing ran and nothing was recorded: an argument was invalid, the
committed configuration is missing or invalid, or the server refused the
registration, for example an unreserved `--cycle`. Report the error code; do
not read it as a failed check.

Fields to report:

- `ok`, `registered`, `uploaded`, `attempt_id`, `cycle_id`.
- `task.correction_cycles_used`, `task.correction_cycles_remaining`. Read the
  budget from the `task` object only. The top-level
  `correction_cycles_remaining` is filled in from a server response, so when no
  response set it, it prints `0` because the field has no "unknown" value.
  A result with no `task` object, such as any `--no-upload` run or a failed
  registration, has an unmeasured budget. Run `check status --task TASK_ID`
  instead, and never read that `0` as an exhausted budget. `--no-upload` left
  the server task unchanged. A failed registration may or may not have been
  accepted already, so its outcome is unconfirmed: do not call the task known
  to be unchanged, and do not call it known to have changed.
- `attempt.status`, `attempt.revision_oid`, `attempt.worktree_state`,
  `attempt.cleanup_failed`, and `worktree_note` when it is present.
- `results[].name`, `results[].status`, `results[].exit_code`,
  `results[].cleanup_error`.
- `upload_error` when this client could not confirm the registration or
  completion. The server may still have accepted it, so inspect `check status`
  before repeating a reservation or a run.

Per-check statuses are `passed`, `failed`, `error`, `cancelled`, `incomplete`,
and `unavailable`. A cleanup error makes the result `error` even when the
command exit code is visible. Output beyond the check's output limit makes the
result `incomplete`; a shortened excerpt or log is marked as truncated and does
not change the status. An empty configured set is `unavailable`, never `passed`.

## Limits

- Checks are advisory. They do not block a merge, and a passing check is not
  proof that the code is correct.
- The helper runs checks with the user's permissions and file access. It is
  not a sandbox. Checks get only a fixed list of environment variables (such
  as `PATH`, `HOME` and locale settings), `CI=true`, and a private temporary
  folder in `TMPDIR`, `TEMP` and `TMP`. Proxy settings, tool settings and
  credentials are not passed. If a check needs one, set it in the check
  command. When a check command fails or cannot start, its log begins with
  the names of the variables it did not get. A temporary-folder error is
  reported as its own error, without that note.
- A dirty or unknown worktree is not a tested commit. Report the recorded
  worktree state instead of calling the revision tested. When the state is
  `unknown`, report `worktree_note`, which says why. Each Git reading of the
  worktree, before and after the checks, has 30 seconds; a reading that fails,
  runs out of time, or is stopped by a signal records `unknown`. A run stopped
  during its checks therefore records `unknown` unless a change was already
  seen.
- A signal during preparation, before registration starts, stops the run
  with nothing run, recorded, or printed. Once registration has started, the
  first signal stops the checks but lets registration and completion finish.
  A second signal ends that wait at once; the server may still have recorded
  the attempt, so inspect `check status --task TASK_ID` to see what it kept. A run started
  with `SIGHUP` ignored, as `nohup` starts one, is not stopped by a closed
  terminal.
- `--no-upload` runs locally and is not recorded on the server. Do not describe
  it as server-recorded evidence, and do not read its top-level
  `correction_cycles_remaining` of `0` as a budget. The server task keeps its
  own remaining rounds, attempt count, and sequence.
- A failed registration is unconfirmed, not absent. The attempt may already be
  recorded with the sequence advanced, or may never have arrived. Keep the
  stable task identifier, report the printed `attempt_id` as diagnostic
  evidence, and inspect `check status --task TASK_ID`. Do not rerun the check
  or reserve a round to find out. `check run` generates a new attempt
  identifier on every invocation and has no flag to resubmit an existing one,
  so a rerun cannot continue the unconfirmed attempt. If `check status` does
  not resolve that exact attempt, leave it unconfirmed and report it.
- An upload failure means this client could not confirm registration or
  completion. The server may still have accepted it. Inspect `check status`
  before repeating the operation; this is not a recorded failed check.
- The task budget is three correction rounds. Reserve a round before asking for
  a correction. The initial check and a manual rerun consume no round, and an
  unavailable or cancelled run does not create one by itself. Confirm
  exhaustion from `check status` or from a reserve call that returns
  `correction_budget_exhausted`, never from an unmeasured `0`. When the budget
  is exhausted, stop automatic continuation and report the unresolved task; a
  manual check can still be recorded.
- Do not retry a failed check blindly, and do not weaken or replace the
  committed check configuration to make a check pass.
- Do not launch or resume a coding session, change a model, grant tools to a
  read-only reviewer, reload a team, or inspect authentication files or
  transcripts.
- Skill loading is not a guaranteed callback. If the skill is not loaded, the
  user can invoke it explicitly or run the commands manually.
