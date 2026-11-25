---
name: good-first-issues
description: Keep a small stock of `good first issue` issues open on GitHub, drawn from the backlog for outside contributors; nothing posted without the user's yes. Use when the user asks for good first issues or to attract contributors, or when /repo:contribution has just merged a PR that closed one.
argument-hint: "[target number | off]"
---

A good first issue does not bring contributors by itself; it is the open door for someone who
already wants to help. A few that are clear and alive beat many that rot: the target is small
(3 by default, never more than 5), and an issue nobody took in three months is better closed
than left as a sign of a project nobody follows.

## The setting

It lives in the "How to use" section of `docs/backlog/backlog.md`, one line:

    - **Good first issues**: keep 3 open on GitHub, reserved for outside contributors (skill
      `/repo:good-first-issues`); their tickets have **Owner**: `contributor — #NN`.

- No line: the repo does not do this. Say so and offer to start (`$ARGUMENTS` a number, or the
  user's yes to 3); the line goes in on the work branch with the first issues.
- `$ARGUMENTS` a number: change the target in the line. `off`: remove the line; the open issues
  stay, their tickets go back to `**Owner**: —` only if the user says so.
- A repo without `docs/backlog/backlog.md`: skill `/repo:backlog` first.

## 1. Count what is open

    gh issue list --label "good first issue" --state open --json number,title,assignees,createdAt,updatedAt,comments

Match each issue to its ticket in the backlog (`**Owner**: contributor — #NN`) and fix any drift:
- an issue closed or merged whose ticket is still open: close the ticket (`/repo:backlog done`),
  crediting the contributor (`… — fixed by @login in #PR`);
- an open issue with no ticket (opened by hand): fine, it counts;
- an issue with no activity for three months and no one on it: propose closing it with a
  kind word and giving the ticket back (`**Owner**: —`).

An issue someone asked for or is assigned to still counts: it is taken, not done.

## 2. Pick the tickets that fill the gap

Missing = target − open. Pick that many tickets from `docs/backlog/backlog.md`, all sections,
that a stranger can do without knowing the project:
- effort `XS` or `S`, one subject, a clear notion of done;
- the files to touch are few and can be named; no design decision left open;
- no secret, server, account or access only the user has; nothing urgent (🔴 critical stays
  ours: a contributor may take weeks);
- not `blocked`, not `in progress`, not already reserved.

Prefer variety (a bug, a doc fix, a small improvement) and what a newcomer learns the project
from. Check in the code that each ticket is still to do. If fewer tickets fit than missing, say
so: a smaller stock is better than a vague issue. A large ticket can be split in the backlog
first (a new `<repo>#T-NN` for the small part) when the split is obvious.

## 3. Write the issues

In English, for someone who has never seen the repo. Title: what to achieve, not the ticket's
internal wording. Body:

    <why it matters, two or three sentences>

    ## What to do
    - [ ] …

    ## Where to look
    - `path/to/file.py` — <what is there>

    ## Done when
    <the visible result, and the test that shows it>

    New to the project? Read [CONTRIBUTING.md](https://github.com/<owner>/<repo>/blob/<default branch>/CONTRIBUTING.md);
    ask anything here, there is no wrong question.

No internal jargon (ticket IDs, French names of the repo's skills, decisions made in chat),
no `@` of anyone, nothing about Claude. Labels: `good first issue`, plus `bug`, `enhancement`
or `documentation` as fits (`gh label list`).

## 4. Post, after the yes

Show the user each title and body, say they will be public under their account, and post only
after an explicit yes:

    gh issue create --title "…" --body-file <file> --label "good first issue" --label "…"

Then, on the work branch (a worktree, skill `/repo:worktree`), set each ticket's **Owner** to
`contributor — #NN`, add the setting line if it was missing, commit
(`docs(backlog): good first issues #NN, #NN`), and merge (`/repo:merge`).

## Reserved tickets

A ticket whose **Owner** is `contributor — #NN` is left for outside contributors: never
proposed as next (`/repo:backlog`), never fixed by us, even in ten minutes, even in passing.
The exceptions are the user's decision: they need it now, or it turned out not to fit (then
close the issue with an explanation and give the ticket back).
