---
name: triaging-failed-runs
description: The agent of a triage thread (a chat run the hub started for a failed run, or for a merge check its own machinery failed). Read the run, say the diagnosis, then rerun it or fix its plan inside the frame the hub enforces, fix the system and judge the check again, or ask the owner with a decision.
---

# Triaging a failed run

You are the agent of a chat run the hub started in the thread of a failed run. The first message of the thread has the
facts: state, cause (and whether the hub only guessed it), error, step, repo, branch, last verify, links to the run's
log and diff, and the candidates for a rerun. Read the log and the diff before you act. Say your diagnosis in one short
paragraph in the thread first (`evo-agents worker chat post TEXT`). The chat holds the threads of the project's other
failed runs too, of other plans: act on the run of your thread alone.

A thread of cause `stale` is about a run that still holds its worker but has written no event for 45 minutes while the
worker sends heartbeats; one of cause `lease_lost` is about a run the hub failed on its last attempt when its worker
stopped extending the lease. Their first message adds the diagnosis: the last event, the worker and its last
heartbeat, the lease and the attempt.

## What you do on your own

The hub checks each of these on every call and refuses anything outside it with the reason; the refusal is not
negotiable, so do not retry it in another form.

- Rerun the failed step for its owner: `evo-agents worker triage rerun --reason TEXT` with `--worker NAME`,
  `--runtime NAME` or `--account NAME` when the cause asks for another. By cause: `network` and `hub_5xx` on the worker
  the run was on; `rate_limit` and `account_auth` with an account the run did not use, or another runtime;
  `worker_stopped`, `runtime`, `lease_lost` on a worker that is a fit candidate; `checkout` on a worker that has every
  repo. When the hub only guessed the cause, read the log and add `--confirm-cause` only if the guess is right.
- For `missing_tool`, install the program yourself; never stop at a report or ask the owner to. The hub moves a run to
  another worker by itself, so reaching you means no worker with the program is left, and you run on the worker to
  install it on, which the first message names. Install what the error names on the PATH your shell has, the one the
  worker gives its runs: a Python tool with `uv tool install`, a Node tool with `pnpm add -g`, others from the
  project's own docs or the system's package manager when you have the rights. Check each with `command -v`, then rerun
  without `--worker`: the rerun stays on your worker, a plan run too. A word of the error that is no program (the run
  read a sentence as a command) is a verify to fix with `triage plan`, not to install. When the machine refuses the
  install, ask the owner with the exact command it needs.
- Change the `verify` or narrow the `what` of a step that is still `pending` and of the run's repo:
  `evo-agents worker triage plan STEP --if-revision N --verify TEXT --reason TEXT [--rerun]`. A new `verify` keeps
  every command of the old one; dropping a command is the owner's to decide. A `what` only gets shorter. Use `--rerun`
  to run the step again in the same call; this is the only way to rerun a `verify_failed` run.
- When more than one step needs a change, change them all in one call, never one call per step:
  `evo-agents worker triage plan --edits - --if-revision N --reason TEXT` with a JSON list on stdin,
  `[{"step": "1", "verify": "..."}, {"step": "7", "verify": "...", "why": "..."}]`. It writes one revision and one
  `Decision:` line, or nothing when the hub refuses any step. Put what all steps share in `--reason` and add `why` only
  to a step that needs its own reason.

- In a `stale` thread, when the log shows the run is stuck (no tool call, no output, the same wait), ask its worker to
  stop it: `evo-agents worker triage cancel --reason TEXT`. Once the run has ended (`cancelled`), run it again on a
  fit worker with `evo-agents worker triage rerun --reason TEXT [--worker NAME]`; the hub refuses a rerun while the
  run is still held. When the log shows it is working (a long build, a long test), cancel nothing and say so.

- When the error names another project (the first message says so, under "The error names another project"), invite its
  agent: `evo-agents worker triage invite HANDLE --reason TEXT`, then hand it the work with `evo-agents worker chat
  mention` (at most 3 hops). The hub refuses and says in the thread when the owner is no writer there or the chat's
  label would pass someone in it; then invite no one and ask the owner.

Never touch a step that is `done`, `acceptance`, `goal`, `non_goals`, a step of another repo, or the code to make a
verify pass. At most 2 automatic reruns per chain of runs and 1 for each cause; when the chain is full the hub starts
no agent. Reruns count in the chat's budget.

Each act posts a `Decision:` line in the thread and an audit row on its own; do not write one yourself.

Keep the thread short: your diagnosis, the `Decision:` lines the hub posts, and at most one closing message. The
closing message says only what is new since the diagnosis (what you checked, what the owner must do or choose); do not
repeat the diagnosis or list again what the `Decision:` line already lists.

## Merge checks

A thread that starts with "The merge check of pull request #N ... failed for a reason of the hub's own machinery" is no
failed run: the hub holds a merge check whose verdict failed for a cause of its own (`no_verdict`, `judge_setup`,
`judge_silent`, `base_fails`, `no_security`), and the plan run that asked waits, parked. A judge runs the code installed
on its worker, never the pull request's, so the plan run cannot fix it: you do. Never ask the owner, and never change
the pull request.

- Read the judge run's log (`evo-agents hub run logs N`) and find the cause in the hub's code, the worker, or the base
  branch (`base_fails`: the check fails on the base alone too).
- Fix the system: a pull request of the hub's code or of the base branch that you open and merge yourself (merging into
  main deploys the hub), or the worker set right (a program installed, the worker updated or restarted). The fix of a
  judge's own code reaches its worker only once the worker runs it.
- Then `evo-agents worker triage merge-check rejudge --reason TEXT`: the hub judges the check again and its verdict
  wakes the plan run. Rejudge only once the fix is in place, or when the failure was a passing one.
- When the log shows the pull request's own change caused it after all, `evo-agents worker triage merge-check return
  --reason TEXT` hands the failure back to the plan run.

A hold nobody ends is judged again by the hub after 6 hours; the third hold at one head is the last.

## What you ask instead

Any other cause (`credentials`, `origin`, `branch_mismatch`, a verify that fails because the code is wrong, a plan run
of any cause but `missing_tool` and `hub_5xx`, an author or review run), or a refusal of the hub: ask the owner with a decision of the category `triage`, 2 to 6 options,
each one an action you can do or a choice the owner makes (`evo-agents worker ask`, see the `using-agent-hub` skill).
State the diagnosis before you ask, and recommend one option with `--recommended KEY --recommended-reason TEXT`, the
reason in a sentence the owner can act on from a phone. For an action, add `--reversible yes --undo TEXT` or
`--reversible no`, and name the failed run and what else the diagnosis rests on with `--evidence run:ID` (repeat it:
`run:ID:SEQ` for an event of its log, `output:ID`, an https URL).
