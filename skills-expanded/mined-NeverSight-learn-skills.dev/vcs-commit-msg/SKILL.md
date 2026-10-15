---
name: vcs-commit-msg
description: >-
  Writes commit messages that match the project's existing style —
  detected from history, asked when the signal isn't strong enough,
  and never mentioning an AI agent or model in any form. Git is
  primary; the same flow applies to other popular VCS (hg, jj, svn)
  by analogy.
when_to_use: >-
  Use whenever a commit message is being written, reworded, or
  amended — explicitly via user request ("закоммить", "сделай
  коммит", "оформи сообщение коммита", "make a commit", "write a
  commit message", "amend the commit message", "reword commit") or
  implicitly when running `git commit` / `git commit --amend` /
  interactive rebase reword, or editing `.git/COMMIT_EDITMSG` or
  any equivalent VCS commit-message buffer.
---

# vcs-commit-msg

Write a commit message that fits the project's existing style.
Detect from history.
Ask the user when the signal isn't strong enough.
Show the result before committing.
Never attribute the change to an AI agent or model.

## Scope

This skill governs the **text of commit messages only.**
It does not cover branch names,
PR titles or descriptions,
tag messages,
or anything outside the commit-message buffer.

## Procedure

### 1. Detect the style

Sample recent history before composing.

For git:

```
git log -n 100 --no-merges \
  --pretty=format:'--- commit ---%nauthor: %an <%ae>%nsubject: %s%nbody:%n%b'
```

Each commit appears as a `--- commit ---` block with explicit
`author:`, `subject:`, and `body:` fields.
An empty `body:` means the commit has no body.

For other VCS (hg, jj, svn),
produce an equivalent sample using each tool's log/template syntax.
The output must contain, per commit:

- a clear commit boundary marker;
- the author's name and email;
- the subject (first line of the message);
- the body (remaining lines, may be empty).

For svn use `svn log --xml`,
since svn has no flexible template language.

Filter obvious bot commits — best-effort,
full coverage is not required:

- author email or display name contains the substring `[bot]`;
- author email is `noreply@github.com`,
  or contains a known bot marker
  (`dependabot`, `renovate`, `github-actions`, `-bot@`);
- subject matches `^Merge pull request #` / `^Merge branch ` /
  `^Revert "`.

Some bot leakage is acceptable —
do not chase 100% filtering.

For each dimension below,
decide the dominant pattern when ≥80% of the filtered sample
agrees;
otherwise the dimension is **inconclusive**.

Dimensions:

- **subject format** —
  Conventional Commits (`feat: ...`, `fix(scope): ...`),
  ticket-first / task-first prefix
  (`PROJ-123: ...`, `[PROJ-123] ...`),
  plain imperative ("Add ..."),
  descriptive ("Added ...", "Adds ..."),
  or other;
- **language** — English, Russian, etc.;
- **capitalisation** —
  capital / lowercase first letter,
  trailing dot present / absent;
- **subject length cap** —
  smallest of 50, 72, 80 where ≥80% of subjects fit;
- **presence of body** —
  body usual when ≥80% have one,
  body absent when ≥80% don't;
- **body wrap column** —
  smallest of 72, 80, 100 where ≥80% of body lines fit;
- **trailers in regular use** —
  `Signed-off-by`, `Closes #`, `Fixes #`, `Refs:`, etc.

### 2. Ask about inconclusive dimensions

If any dimension is inconclusive —
including an empty repository where everything is inconclusive by
definition —
ask the user explicitly before composing.
Group all questions into a single message;
do not ask one at a time.

An explicit user request — for language or any dimension —
always wins over detection.

### 3. Compose

Build the subject (and body, if applicable)
in the detected or chosen style.
For ticket-prefix conventions,
take the ticket from the branch / bookmark name;
ask if it isn't there.
Body content style follows the detected convention —
do not import external best-practices over what history shows.

### 4. No AI attribution

The composed message must not mention any AI agent, model, or
tool (Claude, ChatGPT / GPT, Copilot, Cursor, Gemini, Aider,
Codex, Codeium / Windsurf, Replit AI, JetBrains AI, Tabnine,
Cody, Devin, etc.) in **any form**:

- no `Co-Authored-By:` trailer for AI accounts
  (`noreply@anthropic.com`,
  `noreply@openai.com`,
  similar machine addresses);
- no "Generated with ...",
  "Made by ...",
  "Authored by ..." lines;
- no inline references in subject or body.

Human `Co-Authored-By:` and `Signed-off-by` trailers are fine,
per project practice.

These rules apply from scratch regardless of any existing content
in the commit-message buffer —
the prior message when amending or rewording,
`commit.template` content,
text inserted by another hook or tool,
or an earlier draft.
Drop any AI attribution that was already there;
do not carry it forward.

### 5. Show before applying

Always show the composed message to the user
and ask whether it fits before committing.
Briefly note which dimensions were detected from history
and which the user resolved manually,
so the user sees where the choice came from.
Apply via the VCS's standard commit / amend command
only after the user accepts.
