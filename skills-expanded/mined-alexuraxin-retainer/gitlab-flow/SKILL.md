---
name: gitlab-flow
description: "Issue-first flow on a GitLab tracker: labeled issue → branch by the project convention → commits in the project format → merge request (MR) with Closes #NNN → green pipeline → merge → cleanup. Each step under its own auto/ask/off gate. Trigger words (RU+EN): gitlab, merge request, MR, пайплайн, ветка, задача NNN / gitlab, merge request, MR, pipeline, branch, task NNN."
disable-model-invocation: true
---

# gitlab-flow — issue-first where the tracker is not ours

The engine grew around Gitea, and on a GitLab project the agent assembles the sequence "from
memory" — exactly what [[gitea-flow]] was created to cancel. Here the same six-step sequence and the
same gate resolver, but the terms, the API and the **format rules are taken from the project**, not
from the engine.

The main difference from [[gitea-flow]]: there the repository is ours and the rules are ours. Here
the repository is someone else's, the flow is already accepted by the team, and the skill's job is to
execute THEIRS predictably, not to substitute its own.

## The gate of EVERY step — the same resolver

```
POL="$("${CLAUDE_PLUGIN_ROOT}/bin/retainer-flow-policy.sh" <issue|branch|commit|pr|merge|cleanup>)"
```

`auto` — do it yourself · `ask` — show EXACTLY what you will do, wait for an explicit "ok" · `off` —
do not. The default matrix lives in the resolver; do not rewrite it here and do not compute it in
your head. The `pr` step resolves under the name `pr` — a merge request is it; the flow keeps no
second resolver.

## First, distill the project's rules — three questions, three addresses

The format is not guessed and not carried over from the engine. Before the first step answer with a
fact:

| What | Where to look |
|---|---|
| branch name | `git branch -r` — the convention is seen in existing branches, not in our `issue-NNN` |
| commit format | the validator in the project CI: `grep -rn "commit" .gitlab-ci.yml` and its script directory; the format that fails the pipeline is the only real one |
| MR form and reviewers | `.gitlab/merge_request_templates/`, `.gitlab/CODEOWNERS` |
| the default branch | `git symbolic-ref refs/remotes/origin/HEAD`; at the tracker — the project's `default_branch`. Nothing to guess: in old projects `master`, in later ones `main` |
| how to reach the tracker | is `glab` accepted in the project; otherwise REST `/api/v4` — with the PROJECT's token, see "Secrets" |

The answers are recorded in the project's `.retainer/PROJECT.md`, not held in the head: the next
session would start with the same question and answer it differently.

## The sequence

Precondition — the task is taken: the owner gave an "ok" or the `ask_owner` gate = `off`.

1. **issue** — create it in GitLab with the project's markup (its labels, its templates from
   `.gitlab/issue_templates/`). The body is the plan and context, durable. An acceptance block is
   needed just as with us: without it "done" is checked by nothing. The block's form is the
   project's, if the project has one.
2. **branch** — off the project's default branch (the address is in the table above, not from
   memory), named by the convention from the table above. On taking the task, write the
   active-issue marker (step 6) and give the owner the task's link in one line: `retainer-state.sh
   links` prints it in this tracker's `/-/issues/<N>` form, and the next session start shows it too.
3. **commit** — messages in the project's format; edits in small commits. The format is checked by
   CI: a red commit linter stops work for nothing, and it is fixed by rewriting the message, not by
   arguing with the validator.
4. **pr** — a merge request. `Closes #NNN` in the description (GitLab closes the task by this same
   key), the title by the project's template, reviewers by `CODEOWNERS`.
5. **merge** — by the step's gate. The proof of green is the **merge-request pipeline**, not our
   memory and not our status check: checks in GitLab projects are often raised `only:
   merge_requests`, i.e. they do not run on the branch at all and "the branch was green" means
   nothing. The [[receiving-review]] gate and the `merge-checker` agent are mandatory at both gate
   values.
6. **cleanup** — the task closed, the branch deleted, the local default branch synced. The
   active-issue marker is kept here BY HAND (Write `<NNN>` to the path `retainer-state.sh path
   active-issue` prints on taking; on closing run `retainer-state.sh clear <NNN>`, which removes the
   task from every session's slot, so the settings page stops showing it as taken): it is written by
   `retainer-task-start.sh`, and that one goes to the Gitea API and does not survive to the write on
   this tracker.

## What the engine does NOT use here

The cycle commands (`retainer-task-start.sh`, `task-close.sh`, `ready-check.sh`, `merge-ready.sh`,
`merge-lock.sh`) go to the Gitea API and do not work on a GitLab project. Name this directly, do not
pass their silence off as a green light:

- **task readiness** is checked by the same blocks (files · a step plan · boundaries · acceptance
  criteria), but by eye — there is no machine check on this tracker;
- **the merge lock** does not carry over: it hangs a status in Gitea. Its role here is played by the
  mandatory green pipeline and the `merge-checker` gate;
- **the engine labels** (`in-progress`, `gate-passed`, `ready`) are not created in a foreign project
  — the team has its own scheme, and a second one on top makes both useless;
- **the task skeleton** is taken from `.gitlab/issue_templates/`; our `.gitea/ISSUE_TEMPLATE/task.md`
  is not placed into a foreign tree;
- **the token resolver** (`retainer_token`) does not carry over: it knows one chain, all of it about
  Gitea. Taking it here means sending OUR tracker's secret to a foreign host — and getting a refusal,
  because the foreign API's header is different.

What works here too: the project's quality gate, [[task-cycle]] in full, review, the mutation check,
the edit guard.

## Armor against rationalizations

| You'll tell yourself | The answer |
|---|---|
| "the project is foreign, the discipline is not ours" | foreign are the FORMAT rules; the order "issue → branch → MR → green pipeline" you execute the same |
| "our commit format is better, I'll set it" | the format fails the project's pipeline; the best one is the one that passes their validator |
| "I'll use the usual `issue-NNN`" | the branch name is dictated by the project; your own breaks their automation and search |
| "the pipeline is long, I'll merge on a green branch" | the checks are raised on the MR: on the branch they did not run at all |
| "I'll set our labels, it's clearer to me" | the labels are read by their team, not you; your scheme over theirs devalues both |
| "`ready-check` was silent — so the form is fine" | it goes to Gitea; on this tracker it checked nothing |
| "the MR template is a formality, I'll write my own words" | the template carries what the reviewer looks for by eye; your own text lengthens the review, not shortens it |
| "CODEOWNERS will assign the wrong person" | the assignment is their rule; argue it in the MR, do not bypass it |

Bypass red flags: "it's all wrong on their side anyway", "formally there is an issue", "I'll bring it
to their format later". The rule's spirit: in a foreign project predictability matters more than our
habits — otherwise the engine's tooling looks like an imposition and is removed along with its use.

## Secrets

The GitLab token is **its own**, from the project environment or a file with `chmod 600` named in
its `.retainer/PROJECT.md`. Our `retainer_token` does not fit here: its chain is all about Gitea, and
substituting it means handing our tracker's secret to a foreign host.

When the project names no token of its own, the file `~/.config/retainer/gitlab_token` (the settings
page writes it there) is taken, and only if the host of the project's remote is the host of
`gitlab_url`. A GitLab on any other host gets no token from there.

The header is its own too: the foreign API accepts `PRIVATE-TOKEN: <token>` (or
`Authorization: Bearer`), not our tracker's form — a request in the usual form will return a refusal,
easy to read as "no rights" and start fixing the wrong thing.

The value is never echoed: not `git remote -v`, not curl output. On such projects the token is often
baked into the remote URL — mask it with `sed 's#://[^@]*@#://***@#'`.

## Done (checkable)

The task closed · the MR merged · its pipeline was green · the branch deleted · the default branch
synced · the active-issue marker cleared. Each item confirmed by fact, not by memory.

## When NOT to apply

- **The tracker is Gitea**: there [[gitea-flow]], with its own commands, labels and merge lock.
- **A repository with no tracker** — the flow around tasks turns into ceremony around a commit.
- **Not a substitute for task discipline**: the plan, the plan check, the review and the acceptance
  criteria live in [[task-cycle]]; a green MR does not replace them.

Related: [[task-cycle]] (the discipline this skill executes), [[gitea-flow]] (the same flow on our
tracker), [[receiving-review]] (receiving review findings at the MR step), [[guardrails]] (the guard
keeps a foreign gate from being weakened).
