---
name: gitea-flow
description: "Call AT THE START of a code task on a repository whose tracker is Gitea. Trigger words (RU+EN): завести issue, ветка, PR, смержить, закрыть issue, gitea, issue-first, трекер, берём задачу NNN / open an issue, branch, PR, merge, close issue, gitea, issue-first, tracker, take task NNN. Runs the flow: labeled issue → branch issue-NNN → commits #NNN → PR Closes #NNN → merge → cleanup. Each step under its own auto/ask/off gate (resolver from flow_* and autonomy_level). The executor of the task-cycle discipline; for a GitLab tracker use `/retainer:gitlab-flow`, launched by the owner."
---

# gitea-flow — the mechanical executor of issue-first

Without a frame the flow "issue → branch → PR → merge" the agent assembles "from memory" and it
breaks out of order: a task was born as issue-**last** (code before tracking) precisely because "the
agent understands on its own". gitea-flow gives ONE and the same sequence every run, while
`[[task-cycle]]` stays the discipline (WHAT and in what order, DoD) — gitea-flow EXECUTES it at the
steps that must touch the tracker or git. Do not duplicate the plan/review/gate here — they are in
task-cycle.

## The gate of EVERY step — one resolver, not "from memory"

Before each step ask the policy:

```
POL="$("${CLAUDE_PLUGIN_ROOT}/bin/retainer-flow-policy.sh" <issue|branch|commit|pr|merge|cleanup>)"
```

- **`auto`** — do the step yourself.
- **`ask`** — show EXACTLY what you will do (title+labels · branch name · PR text), wait for an
  explicit "ok", then do it.
- **`off`** — do not do it yourself (the owner by hand, or the step is skipped).

The default matrix (step×level) and the `flow_<step>` override live in the resolver — do not rewrite
them here and do not compute them in your head (that is the RED). The per-step override is the
essence of "each cycle governed separately".

The flow has six steps. Two more resolver gates do not belong to the flow and belong to
[[task-cycle]] — do not pull them from here: `ask_owner` (the right to stop work with a question
about a fork) and `confirm_intake` (confirming the understanding of the task before work begins).

## The sequence

Precondition: **the task is taken into work** — the owner gave an "ok" on it or the `ask_owner` gate
= `off` (an autonomous run: the task is taken from the tracker queue, no "ok" is awaited). Only after
that:

0. **Already an issue?** If the task is already tracked (the number is known) — skip the `issue`
   step, work by it.
   **Before starting, check readiness:** `${CLAUDE_PLUGIN_ROOT}/bin/retainer-ready-check.sh <owner/repo> <NNN>`.
   A readiness label is no proof by itself: a measurement gave 12 of 12 labeled that could not be
   taken. Codes: `0` — may take · `1` — not ready, what is missing is printed · `2` — could not
   check (the tracker is silent or returned an error); "not checked" is not "not ready" and still
   less "ready".

   **What to do on `1` — grooming, not reconnaissance along the way.** The missing is gathered
   BEFORE code and goes into the task BODY (files · plan · boundaries and the acceptance block under
   the heading `## Acceptance Criteria` — the form is machine-read: the merge lock reads it, or
   the Russian «Критерии приёмки» / «Критерий приёмки», and rejects checkboxes under any other
   heading) and into a comment (landmines with `file:line` addresses, found by reading the code,
   not assumed). This is work the agent does itself: read the
   code, complete the task, re-verify. The difference from "I'll figure it out along the way" is not
   the volume but that the result stays in the tracker and the next session does not repeat it.

   Grooming hit an owner decision (no product option chosen, no data) — the task gets `blocked`, the
   fork goes into the task with an open-question marker, and the next in the queue is taken. **Do not
   stand and wait**: the right to stop is decided by the `ask_owner` gate, not this step. On `2` the
   task is not taken and not labeled: first the tracker access is fixed.

   **Setting `blocked`, name the blocker in one of two forms — otherwise the label asserts nothing.**
   The blocker is a task: a dependency in the tracker (`POST /issues/<N>/dependencies`; the body must
   carry `index` + `owner` + `repo`, a bare `{"index": N}` gives **404**, i.e. "no such endpoint"
   instead of "a wrong body", and the conclusion suggests itself wrongly). The blocker is a person: a
   line `Blocker: owner — <what exactly to do>` in the task body; a dependency expresses only
   task→task and cannot express a person, and on live blockages the blocker was exactly them.
   Checked by `${CLAUDE_PLUGIN_ROOT}/bin/retainer-blocked-check.sh <owner/repo>` — by a command, not
   a gate step: a blockage lives in the tracker, while the gate must work offline.

   **By the same motion — the clock:** `${CLAUDE_PLUGIN_ROOT}/bin/retainer-task-clock.sh <owner/repo> start <NNN>`.
   The measurement comes free, because the step touches the task anyway; as a separate ritual it
   would not stick — there is no point pressing a button mid-work, and over the project's whole
   history nothing was recorded to the tracker. The clock did not start — no reason not to take the
   task: say so and work on.
1. **issue** — look up label ids by name (not an empty `labels`), create the issue with the markup
   **priority · area · type · impact** per the repo schema. Impact names who suffers:
   `impact-user` — whoever uses the product, and the body says what they see while it is not
   fixed; `impact-maker` — whoever makes it, and the body names the price now (minutes, runs,
   repeats). Neither fits — the subject is a mechanism watching a mechanism, and it is not
   filed. The body = the plan/context (durable, not a scratchpad). The acceptance block is called `## Acceptance Criteria`, the items are checkboxes
   right under it: the form is machine-read, the merge lock reads it and the Russian «Критерии
   приёмки». The body skeleton lives in `.gitea/ISSUE_TEMPLATE/task.md`.
   **A readiness label is not set at creation at all** — a just-created task is ungroomed by
   definition. It is set later and only after `retainer-ready-check.sh` exits 0: markup at creation
   is classification (priority·area·type·impact, known at once), while readiness is a claim about state that
   is checked. Taken into work → remove readiness, set `in-progress`.
2. **branch** — `issue-NNN-slug` off `main`. Steps 1-2 plus the label, the marker and the clock are
   done by ONE command `bin/retainer-task-start.sh <owner/repo> <N>` — symmetric to `task-close.sh`.
   It also prints the task body: the precondition is taken from the tracker, not from the agent's
   memory. Its `▶ task #N: <url>` line is for the owner: pass it to them as is, in one line, when
   you take the task — the command's output does not reach their screen by itself.
3. **commit** — messages `#NNN — …`; edits in small commits, each meaningful.
4. **pr** — a PR with `Closes #NNN` in the body; the title `#NNN — …`.
5. **merge** — by the step's gate. Outside an autonomous run it is `off`: stop the flow at "PR
   opened" and hand the merge to the owner, not bypassing it with other tools. In an autonomous run —
   `auto`: the agent does the merge, this is the owner's decision (the old note "the agent is cut by
   the harness classifier" was lifted by them). But `auto` is the right to merge, not the right to
   merge anything: before the merge request
   `${CLAUDE_PLUGIN_ROOT}/bin/retainer-merge-ready.sh <owner/repo> <NNN>`. Not `exit 0` — do not
   merge, the reason is printed. The script is fail-closed: the tracker's silence is also "may not".
   The check is made not by your memory that "the gate was green" — that rule is what killed the note
   "CI must be green".

   **This is not a request: the verdict is issued as a status check.** `retainer-merge-lock.sh` hangs
   on the PR head the status `retainer/merge-lock`; where the context is entered into the branch
   protection's `status_check_contexts`, a merge without it is closed. Pass the head to the merge via
   `head_commit_id` with the SHA the lock named: a new commit does not inherit the status. Recompute
   the lock after the review record and the report appear:
   `POST /api/v1/repos/<owner>/<repo>/actions/workflows/merge-lock.yml/dispatches` with the body
   `{"ref":"main","inputs":{"pr":"<PR number>"}}` — or wait for a comment to recompute it.

   **Name the ceiling honestly.** The status is written by the same token you use for the tracker —
   so "cannot be bypassed" is wrong. Correct: the merge is closed while there is no status, and
   writing one past the lock is a separate deliberate action, visible in the commit's status log.

   Closing the task by a mechanism is NOT guarded: `PATCH state=closed` passes. So the acceptance
   criteria and the result report are checked by `retainer-task-close.sh`, and the merge lock refuses
   if they are absent — for close-on-merge this is the only seam.

   **The content gate is the `merge-checker` agent, and it is mandatory at BOTH gate values.**
   `merge-ready.sh` checks the mechanics and the identity of the reviewed commit; the gate checks
   that the DECLARED was done: acceptance criteria with addresses in the diff, declared files against
   changed, a test for each edit that carries a use case, task boundaries. Call the agent AFTER a
   green `merge-ready` and pass it the PR number, the task number and the SHA range — **without your session history**:
   it holds exactly the rationalizations the gate protects against. The verdict `MERGE-CLEAN` is
   recorded by the label `merge-clean` on the PR. Blocking findings — do not merge, fix, repeat the
   gate.

   Why a separate agent and not another pass of yours: independence gives not a second reading but a
   cold start. You remember why you wrote it that way, and that memory works as a ready
   justification. At `merge = off` the gate is the same — otherwise a manual merge has fewer checks
   than an automatic one.

   **The owner-allowed path: the gated merge script `bin/retainer-merge-gated.sh`, installed by the
   owner as a root-owned file at its `INSTALL_DIR` constant, with its tracker and gate constants
   set for that machine, and allowed as exactly that one command.** Where it is
   installed, send the merge through it and through nothing else. It merges only while the merge
   setting is on (`flow_merge = auto`, or unset under marathon) and the latest `retainer/merge-lock`
   and `gate / gate (pull_request)` rows on the head are green and written by an Actions run;
   otherwise it refuses with the reason. `--check` runs the same checks and sends nothing. A refusal
   on the lock or the gate is yours to fix; a refusal on the switch is the owner's, and the agent
   never changes `flow_merge`. Do not run `retainer-merge-lock.sh` yourself before a gated merge: its
   row carries your token, and the script refuses it as "not written by CI" until the lock is raised
   in CI again — by a comment, or by the dispatch above. The filter stops a hand-posted status, not a
   PR written to mint one with the run token — the ceiling above still stands.

   **A refused merge in an autonomous run goes to the owner as one line in the same turn, not as a
   wait.** Where that path is absent, or the classifier refuses it too: `merge = auto` is the
   owner's standing permission, but the harness classifier judges the conversation, not the
   regulator. On a refusal, in the same turn: one line naming the PR, its head,
   the green lock and the independent review record, asking the owner to confirm the merge. When the
   owner confirms in the chat, send the merge. Do not reshape the request, do not switch transports;
   while waiting, move on down the list rather than defer the rest of the work until the merge.
   Outside an autonomous run (`merge = off`) the merge is the owner's.
6. **cleanup** — part of the merge step, not a separate intent. Right after the merge request:
   `${CLAUDE_PLUGIN_ROOT}/bin/retainer-task-close.sh <owner/repo> --pr <PR number>`. The command
   reads the PR body, cleans ALL tasks named in it (`Closes`/`Fixes`/`Resolves`) and verifies the
   result on the same run: an open task or a working label left — `exit 1`, and **the merge step is
   not closed** until the command gives `exit 0`. The single form `… <owner/repo> <NNN>` remains for
   tasks closed without a PR and for cleaning a historical tail.

   Why tied to the merge: `Closes #N` closes the task by the TRACKER's own force, and the state change
   does not touch the labels. The merge is the only point of the cycle where a task closes without
   the participation of whoever must call the command, and cleanup there stayed a promise.

   Then: close the PR (`PATCH state=closed` — the close API the classifier passes; this is also how a
   "stuck" PR is closed when the merge commit is already in main but Gitea keeps it open),
   `git fetch` + `--ff-only` main, delete the branch, clear the active-issue marker (`retainer-task-close.sh` does it).

   **The boundary is honest:** the machine check INSIDE the call — forgetting one task of ten or
   leaving a partial result is no longer possible. You must still call the command; one not called at
   all is caught by `retainer-preflight.sh` (`closed-labels`, hard on manual/assisted).

## Re-publishing a rebased branch

A rebase before the merge is mandatory — the merge lock requires it. After it an ordinary `push` is
rejected, and before this there was **no safe way at all** to publish the rebased.

**This way — no.** "Delete the branch and push again" CLOSES its pull request, and it cannot be
brought back: the head becomes `refs/pull/N/head`, `mergeable: false`. The discussion, the review
verdict and the edit history are lost. Two PRs were lost this way in one session.

**The regular way — a lease, with the branch EXPLICITLY named:**

```bash
git push --force-with-lease origin issue-<N>-<slug>
```

`--force-with-lease` is not destructive in meaning: it **refuses** if the remote branch moved ahead —
i.e. it does not overwrite someone's work but reports it. The guard passes it in exactly this form.

What is closed and why:

| form | why not |
|---|---|
| `--force` / `-f` | overwrites others' without asking — destructive everywhere, task branches included |
| `--force-with-lease` **without a branch name** | the target is set by the upstream, invisible in the command: the force goes to whatever branch you happen to stand on |
| `--force-with-lease` on `main` | under no conditions |

## Secrets

Take the token by the engine's shared resolver — `retainer_token` from `bin/retainer-config.sh`: the
list of places lives there, and your own copy of the chain diverges from it silently. The file is
`chmod 600`. **Never echo the value** — not in `git remote -v`, not in curl output; mask it with
`sed` (`s#://[^@]*@#://***@#`). This is a global rule, not an option.

## Armor against rationalizations

The flow is bypassed quietly. An answer to each gap:

| You'll tell yourself | The answer |
|---|---|
| "a small edit, I'll file the issue later" | the issue is filed BEFORE code — a task was born exactly on this |
| "it's clear from the commit anyway" | a commit ≠ triage; the issue carries priority·area·type·impact and a durable plan |
| "in `auto` I can do it all myself, merge included" | `auto` ≠ merge: the resolver keeps merge=`off` in auto. Merge yourself — only where the resolver said `auto` |
| "I'll merge it myself, why wait for the owner" | ask the resolver, not yourself: `off` — hand to the owner, `auto` — merge, but green |
| "the run is autonomous, the gate and review can wait" | autonomy removes QUESTIONS, not checks: a red gate stops it there too |
| "I'll put the labels on later" | markup AT creation, not an empty `labels` (a global rule) |
| "it has a readiness label — so it can be taken" | the label is set by the same agent by intuition. Readiness is asked of `retainer-ready-check.sh`, not of the label |
| "no blocks, but the task is clear — I'll figure it out along the way" | "figure it out along the way" is the reconnaissance inside a task that the check was created to cancel |
| "`ask`, but the answer is obvious" | `ask` = wait for an EXPLICIT "ok"; obviousness does not cancel the tracker record |

Bypass red flags: "this time it's fine", "formally there is an issue", "I'll file it later". The
rule's spirit: the record in the tracker and git goes BY the step's gate, not by mood — predictability
over speed on a single step.

## Done (checkable)

All six: the issue closed · the branch in `main` · the PR closed · `in-progress` removed · `main`
synced · the active-issue marker cleared. There is no "done" until each item is confirmed by fact
(not "from memory").

## When NOT to apply

- **The repository is not on a tracker.** The skill executes the flow around tasks and PRs: without
  a tracker it turns into ceremony around an ordinary commit.
- **The edit does not create work others need to know about** — a draft, a one-off script in the
  scratchpad, an experiment that will be torn down.
- **Not a substitute for task discipline.** Branches and PRs are form; the plan, the plan check, the
  review and the acceptance criteria live in [[task-cycle]], and a green flow does not replace them.
- **Not for a foreign repository** with a different flow: an imposed issue-first breaks others' rules
  for the sake of one's own.

Related: [[task-cycle]] (the cycle discipline — this skill is its executor),
[[guardrails]] (the guard keeps the gates from being weakened), [[receiving-review]] (receiving
review findings at the PR step).
