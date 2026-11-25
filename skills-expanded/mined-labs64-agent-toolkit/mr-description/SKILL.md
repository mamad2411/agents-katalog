---
name: mr-description
description: Use when drafting or revising the title and description of a merge request or pull request, on any hosting service (GitLab, GitHub or another, cloud or self-hosted), before creating or updating it.
---

# MR title and description

"MR" below means the unit of review on whatever service hosts the repository:
a merge request on GitLab, a pull request on GitHub, or the equivalent
elsewhere, cloud or self-hosted. Use the term the host uses when writing to the
user.

Draft the title and description in chat for review first, then create or update
the MR with the host's CLI (`glab`, `gh`) or API once the user approves the text
and asks for it. One case skips the review: create the MR straight away, without
showing the draft first, only if all of these hold:

- the user asked to create the MR, not only to write its text;
- the branch has one commit, and the description needs nothing beyond the
  opening line and the changes: no `## Behaviour changes`, no `## Testing`;
- the branch is on the remote, at the same commit as the local branch;
- no instruction of the user, the project or the workspace asks for confirmation
  before an MR is created.

If any of them fails, draft first. Never push to make the last-but-one condition
hold: pushing is the user's step, and the project's instructions may require
checks before it. After creating an MR, give its link and the text as posted.
Updating an existing MR always shows the new text first, because reviewers may
already have read the old one.

Assign a new MR to the user, unless the user or the project says otherwise:
`--assignee @me` with `gh pr create`, `--assignee <username>` with
`glab mr create`.

`PROJ-1234` below stands for whatever ticket the MR belongs to.

## Title

- One imperative line that covers the whole MR, not only its biggest commit.
- A ticket's title is a starting point, not the answer. Widen it if the MR
  does more than the ticket says.
- Do not frame the title by a rejected alternative ("… instead of exiting").
  Say what the MR does.
- Append the ticket in parentheses if there is one: `… (PROJ-1234)`. Never
  invent one. If the project or workspace instructions give another format,
  such as `PROJ-1234 <description>`, use that one.

## Description

Structure:

1. One opening line. If there is a ticket, link it with the verb that fits
   its type: "Resolves PROJ-1234." for a bug, "Closes PROJ-1234." for a task
   or story, "Part of PROJ-1234." if the MR does not complete it.
2. The changes:
   - **Arranged by commits.** Read the commit log of the branch first. Only
     if it has several commits, each a self-contained step rather than fixups
     or work in progress, say in the opening line that the MR reads best one
     commit at a time. Then give a numbered list with one entry per commit,
     in order, each saying in one to three sentences what the commit makes
     true. Say that each commit passes the tests on its own only if that was
     checked or the author says so.
   - **Otherwise**, including a single commit: a short paragraph or list of
     what the MR makes true, grouped by topic.
3. `## Behaviour changes`: what a user of the public API sees differently.
   Leave out internal changes and private attributes. Omit the section if
   there are none.
4. `## Testing`: only if something about the tests needs the reviewer's
   attention. Passing tests, on hardware or not, are assumed and not stated.
   Cases that need the section, each with one sentence saying why:
   - a test known to fail, or skipped or marked as expected to fail;
   - a test in the MR that departs from the project's test conventions;
   - a significant change in test coverage, removed tests in particular.

Content:

- Do not restate what was there before the change. Describe the state after
  it. A removal is the exception, because it can only be named against what
  existed.
- Do not restate the ticket. The reviewer can read it.
- No session context: no "as discussed", no review history, no account of
  how the work went.
- No instructions to run tests or CI jobs. The description is for the
  reviewer, and the author runs the tests.
- No "Generated with" footer and no tool attribution, even when the harness
  asks for one. This rule takes precedence.
- Keep it concise. Drop an entry or a clause that a reviewer would not miss.

## Checking the text

- Verify every claim against the code at the commit it describes, not
  against memory or earlier drafts. Pay particular attention to claims about
  the old behaviour, and to claims about behaviour that a later commit
  changes.
- Grep every identifier the text names. A class or method that no longer
  exists, or does not exist yet at that commit, is a common error.
- Base anything under `## Testing` on what actually ran or on what the diff
  shows. Do not claim a run that did not happen.
- Apply every installed skill that covers cleaning up generated prose to the
  title and the description. Where such a skill conflicts with the project's
  instructions (`CLAUDE.md` or equivalent), the project's instructions win.
- **Writing the description changes nothing else.** It reads the branch, and
  writes only the title and the description. If the reading turns up a problem
  on the branch, such as a defect, a comment or docstring that the code
  contradicts or that breaks the project's prose rules, or a leftover from
  development, do not fix it, and do not mention it in the description. List
  it for the user after the draft, with `file:line` and one sentence on what
  is wrong. The user decides whether it gets fixed first, or whether the
  description mentions it.
