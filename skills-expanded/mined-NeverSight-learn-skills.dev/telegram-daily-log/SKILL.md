---
name: telegram-daily-log
description: Summarize today's verified accomplishments as a Telegram daily log and copy it to the clipboard.
disable-model-invocation: true
---

# Telegram Daily Log

Use the computer's local calendar date and include activity up to the current time.

## Reconstruct the day

Inspect all four evidence streams:

- Codex and Claude histories and transcripts.
- GitHub activity through `gh`.
- Local git activity across repositories under `~/ghq`.
- Zsh history and files changed today for leads that the other sources miss.

Treat prompts, commands, commit messages, and PR descriptions as claims. Verify completion
against the resulting files, refs, PR state, releases, or other observable output. Distinguish
finished, published, and still-open work accurately.

Read each stream deeply enough that a whole item cannot hide inside it:

- Anything published outside this machine leaves no trace in git, `gh`, or the shell. Only the
  transcript holds it, usually as the user pasting a URL or saying they posted, sent, replied,
  shipped, or submitted. Search the day's transcripts for those before writing.
- Judge the size of a change by the files it touched, not by its subject lines. Read
  `--name-only` or a diffstat across the day; a run of narrow-sounding subjects routinely spans
  far more surface than any one of them admits.
- Never infer why a shell command ran. Attribute it to the session working in that repository
  at that hour, or leave it out.
- Codex transcripts usually yield no readable prompt. Attribute their work by `cwd` and
  timestamp instead, and say so when that is all the evidence there is.

History can contain credentials. Filter before printing tool output, never emit raw histories,
and omit secrets and unnecessary personal or customer data from the post. Warn separately when
a credential is found, without repeating its value.

## Write the post

Produce plain text in this shape:

```text
Daily Log — Month D, YYYY

1. Short grouped title
One short first-person description.

2. Short grouped title
One short first-person description.

3. Short grouped title
One short first-person description.

Small wins: ...

Today's output: ...
```

- Use exactly three main items, grouped and ordered by effort.
- Keep descriptions concise and natural in the user's voice.
- Add `Small wins` only when several worthwhile minor items remain.
- Add verified output counts when they make the day easier to scan.
- Use Telegram-safe plain text: blank lines, numbered items, and bare URLs only when useful.
  Markdown link syntax and decorative formatting render inconsistently when pasted.

## Copy

Copy only the completed post to the macOS clipboard with `pbcopy`, verify that the clipboard is
non-empty, then report the copied title. Keep coverage gaps and credential warnings outside the
clipboard content.
