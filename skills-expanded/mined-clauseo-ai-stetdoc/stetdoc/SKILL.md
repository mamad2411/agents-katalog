---
name: stetdoc
description: Read, redline, comment on and compare Word documents (.docx) with real tracked changes. Use whenever a task involves reading or editing a .docx file.
metadata:
  stetdoc-version: "0.9.4"
---

# stetdoc

In Claude Code, use the `stetdoc` command; with MCP tools, call `skills_get` first.

```
stetdoc view a.docx --find 'net 30' --find 'thirty'
stetdoc replace a.docx 'net 30' 'net 45' 'thirty' 'sixty'
stetdoc comment a.edited.docx 'Liability Cap' 'Mutual?' --in-place
```

An edit writes a.edited.docx beside a.docx and leaves a.docx unchanged. Edit that file next, with `--in-place` (never on the
user's file unless asked). Each OLD must occur once (else use a longer OLD, `--clause 11.1` or `--all`); an empty NEW deletes.

Changes are tracked unless the user asks for manual markup or no Track Changes. A document or note they point you to may
ask for it too, such as a client email: read those first. Then add `--manual` (old text struck through, new underlined) and
say the file is manual markup. Tell the user about others' tracked changes: who made them, and what. Anything else:
`stetdoc skills get core`.

On a long document, never `view --all`: follow each `-- more:` line, or narrow with `--find` or `--range`.

If `stetdoc` is not found, say it is not installed, and stop. Never read or edit a .docx another way, and do not offer to.
