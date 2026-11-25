---
name: wiff-review
description: Read and annotate a wiff code-review session from the command line. Use when asked to review a diff and leave comments in wiff, or to read and address the comments already left in a wiff review.
---

# Wiff Review

wiff is a terminal-first code-review tool. A review lives in a local session that a
human browses in the wiff TUI while an agent reads and writes the same session
through the `wiff` command line. The TUI belongs to the human: never launch or
drive it. Do all of your work through the `wiff` subcommands below.

If there is no session to act on, ask the user to start one with wiff first.
The exception is when you are the automation that opens reviews (see below).

## Opening or refreshing a review from automation

When your job is to trigger reviews rather than review within a session a human
opened, create-or-refresh the session for the current changes in one idempotent
step:

```bash
wiff new --no-tui --if-needed
```

It creates a session when none exists for these changes, refreshes one in place
when the working copy has moved on, and does nothing when it is already current.
With no changes and no session yet, it exits non-zero with "no changes to
review". By default it reviews the uncommitted working-tree changes; add
`--from-base` to review the whole branch against its trunk instead. Requires
`--no-tui`.

## Selecting the session

Every command acts on the active session for the current project by default, so
run wiff from inside the checkout being reviewed and you can usually omit any
session flag. When the active session is not the one you want, or the project
cannot be derived from the working directory, select it explicitly:

```bash
wiff session list
wiff render --session 2br8zf30h
wiff comment add --agent --session 2br8zf30h --review --body "..."
```

- `wiff session list` prints the sessions for this project and their ids.
- `--session <id>` targets a specific session instead of the active one.
- `--project <name>` forces the project when the working directory cannot name
  it on its own.

## Exploring existing code

Not every review is about a change. To annotate existing code, open an explore
review: an empty session over the current working copy, to which you add the
files you want to comment on.

```bash
wiff new --no-tui --explore
wiff explore add src/lib.rs src/parser.rs
```

- `wiff new --explore` creates the review with no files yet. Add `--no-tui` when
  you are driving it from the command line rather than handing it to a human.
- `wiff explore add <PATH>...` brings files into the review, each captured at its
  current state. Re-adding a file already under review does nothing.
- You do not have to add a file before commenting on it: `wiff comment add --file
  F ...` on an explore review adds `F` first when it is not yet present, so
  `--file` doubles as the way to bring a file in.

Everything else, reading with `wiff render` and leaving or revising comments,
works the same as on a diff review.

## Reading a review

Start here when asked to read a review or to address the comments it holds.

```bash
wiff render
wiff render --format json
wiff comment list
```

- `wiff render` prints the review as markdown: comments grouped by file, each
  led by its number (like `#3`) and showing its author and kind, target
  location, resolved or outdated state, body, and a fenced snippet of the
  surrounding code. This is the one command you need to read the review and to
  pick up the numbers you act on below.
- Each comment has a short review-scoped number, shown as `#N`, and a long ULID.
  Every command that names a comment (`resolve`, `verdict`, `rm`, `--reply-to`)
  accepts either. Prefer the number: pass it as the bare digits `N` (a leading
  `#` starts a comment in the shell, so write `3`, not `#3`, unless you quote it
  as `'#3'`). The ULID stays valid and is the durable identity across sessions.
- When the review has a description (a title and optional body, the same shape
  as a commit message), `wiff render` prints it under a `## Description` heading
  and the JSON includes it in a top-level `description` field. See below to set
  one.
- `wiff render --format json` prints the same folded state as JSON for
  programmatic use. Each comment reports `updated_seq` and `updated_at`. To order
  changes or find the most recent one, use `updated_seq`, which always advances;
  `updated_at` is a display timestamp and, for a comment imported from a forge,
  can predate an earlier change.
- `wiff comment list` is an optional compact form: one comment per line, number
  first, with its status and location, when you want a terse pass without the
  bodies and snippets.

When you finish addressing a comment, resolve it so the human sees it is done.
Pass `--agent` here too, so the resolution is attributed to you rather than the
human:

```bash
wiff comment resolve --agent 7
```

## Leaving review comments

Use these when asked to review a change and record your findings. Always pass
`--agent` on every command that writes to the review, so your comments,
resolutions, and withdrawals are attributed to you rather than the human.

```bash
wiff comment add --agent --file src/lib.rs --line 42 --body "This can overflow."
wiff comment add --agent --file src/lib.rs --line 10-14 --body "Extract this loop."
wiff comment add --agent --file src/lib.rs --line 42 --side before --body "..."
wiff comment add --agent --file src/lib.rs --body "This module needs tests."
wiff comment add --agent --review --body "Overall the change reads well."
wiff comment add --agent --reply-to 3 --body "Agreed, done."
```

- `--file F --line N` comments on a single line; `--line N-M` on an inclusive
  range. Line numbers are 1-based.
- `--reply-to <comment>` replies to an existing comment, named by its number or
  ULID, forming a thread. A reply takes its position from the comment it
  answers, so it needs no file or line. A thread shows as a flat sequence in the
  order the replies were written; a reply to a withdrawn comment is refused.
- `--side after` (the default) refers to the post-change content; `--side
  before` refers to the pre-change content.
- `--file F` with no `--line` comments on the whole file; `--review` comments on
  the change overall.
- `--verdict approve` or `--verdict request_changes` records a verdict along
  with the comment. A comment without one is a neutral remark.
- Provide the body with `--body`, or pipe it on stdin for anything long or
  multi-line:

```bash
printf '%s\n' 'First point.' 'Second point.' | wiff comment add --agent --file src/lib.rs --line 42
```

To revise your own comments:

```bash
wiff comment list
wiff comment resolve --agent 3
wiff comment resolve --agent --reopen 3
wiff comment verdict --agent 3 request_changes
wiff comment edit --agent 3 --body "Revised wording."
wiff comment rm --agent 3
```

- `wiff comment resolve <comment>` marks a comment resolved; `--reopen` undoes
  that. Name the comment by its number or ULID, as everywhere.
- `wiff comment verdict <comment> approve|request_changes|none` sets or clears
  the verdict on your own comment. Only its author may. `wiff render` reports
  each actor's current verdict, reduced from their comments, under a
  `## Verdicts` heading and in a top-level `verdicts` field in the JSON.
- `wiff comment edit <comment>` rewrites a comment's body from `--body` or
  stdin. You may edit only your own comments.
- `wiff comment rm <comment>` withdraws a comment. You may withdraw only your
  own comments.

## Describing the review

A review can carry a description: a one-line title and an optional body, the
same shape as a commit message. It is the review's own summary, distinct from
any comment.

```bash
wiff description show
wiff description set --agent "Tidy the parser"
printf '%s\n\n%s\n' 'Tidy the parser' 'Split the lexer out.' | wiff description set --agent
```

- `wiff description show` prints the current description.
- `wiff description set` sets it from the argument, or from piped stdin when no
  argument is given. The first line is the title; the rest, past a blank line,
  is the body. Setting it again replaces the previous description.
- Pass `--agent` so the description is attributed to you rather than the human.

## Guidelines

- Read the change before commenting. `wiff render` gives you each comment with
  its surrounding code; read the diff itself from the checkout as needed.
- Comment where it matters: intent, correctness, risks, and follow-ups. Do not
  leave a note on every hunk; highlight what the human would not spot alone.
- Anchor each comment on the most specific target you can, a line or a range,
  and fall back to a whole-file or review comment only for points that have no
  single home.
- Quote comment bodies in the shell so punctuation is not mangled, or pipe them
  on stdin.
