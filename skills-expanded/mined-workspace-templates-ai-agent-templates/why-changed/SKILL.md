---
name: why-changed
description: Explains why a file or function looks the way it does by tracing its commits, blame and linked issues, with evidence.
disable-model-invocation: true
---

Explain why this code looks the way it does: $ARGUMENTS

1. Resolve the target to a file and line range. If a function name is given, find its definition first.
2. Use `git blame -w -C -L <range> <file>` to list the commits behind those lines, ignoring whitespace and moved code.
3. For each distinct commit, run `git show <hash>` and read the message, body and diff. Then follow renames with `git log --follow -p -- <file>` when the trail ends at a move.
4. Collect references: issue or PR numbers (#123, JIRA-45) in messages. If the gh CLI is available and authenticated, read them with `gh pr view` or `gh issue view`. Never guess at links you cannot open.
5. Look at nearby tests and comments added in the same commits; they often state the intent.

Answer in this shape: **Short answer** (two sentences), **Timeline** (date, commit, author, what changed and why), **Evidence** (quotes from messages or tickets), **Confidence** (high, medium, low) and **Safe to change?** with the conditions. Make no edits.
