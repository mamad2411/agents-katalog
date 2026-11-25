---
name: m-feedback
description: Use when, while working with Power Query M in any project, m-reference proves wrong or incomplete - a card or note contradicts what the engine returned, a trap is missing, a real name is reported as nonexistent - or the user asks to report a gap to powerquery-m-for-agents. Drafts a sanitized issue for its public repo and files it only after the user approves the text. Triggers on "report this to powerquery-m-for-agents", "m-reference is wrong", "add this trap to the M reference", "reporta esto a powerquery-m".
---

# Report a gap in m-reference

The reference is fixed in its own repository, never in the installed copy and never from the
project you are working in. Keep working with your own workaround; the gap goes back as an
issue on **CSalcedoDataBI/powerquery-m-for-agents**, which is **public**.

## 1. Reduce it to a case anyone can run

- One `m` block that shows the problem using literals only (`#table`, `{...}`, `[...]`),
  no data source. If the case needs a source, describe its shape ("a CSV read with
  `Csv.Document`, every column text") instead of pasting it.
- What you expected, and what the engine returned. Name the host and build that ran it
  (Power BI Desktop, PQTest, Excel), or say it was not run.
- The card, note or concept page that is wrong or missing, by function name.

## 2. Sanitize - the issue is public

Remove client and company names, people, file paths, server and database names, workspace or
dataset IDs, GUIDs, URLs of private systems, real column names that reveal a business, and
every real value. Rename to neutral ones (`Key`, `Amount`, `T`). Nothing from a private
repository: no code, no file names, no issue numbers. If the case cannot be told without
private detail, stop and tell the user.

## 3. Check it is not already there

```bash
gh issue list -R CSalcedoDataBI/powerquery-m-for-agents --state all --search "<function name>"
```

If an issue covers it, offer to add a comment there instead.

## 4. Show the draft, then file it only on approval

Show the user the title, the label and the whole body. File it only after they approve that
text, with their own `gh` login:

```bash
gh issue create -R CSalcedoDataBI/powerquery-m-for-agents --title "<function>: <what is wrong>" --label documentation --body-file issue.md
```

Labels: `documentation` for a wrong or missing note, `bug` for a wrong card or a broken
script, `enhancement` for something new. Without `gh`, give the user the text and
`https://github.com/CSalcedoDataBI/powerquery-m-for-agents/issues/new` to file it themselves.

Then tell the user the issue link and the workaround the project keeps meanwhile.
