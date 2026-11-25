---
name: improve-comments
description: Remove redundant comments and correct verified stale wording in a diff, file, or directory.
license: MIT
disable-model-invocation: true
---

# Improve comments

Apply verified comment edits as you find them. Preserve information that people or tools depend on.

## 1. Set the scope

Use the requested file, directory, diff, or explicit whole-repository scope. With no target, use the current staged and unstaged diff. If that diff is empty, ask for a target.

In a diff, edit only added or modified comment lines. Locate each candidate by path and line in the version shown on the added side of the diff. Map staged lines from the index through the unstaged hunks to the working file. For a supplied diff, establish the version on its added side before tracing its lines to the working file. Skip and report lines that were removed, replaced, or cannot be mapped to a single location. Confirm the text at the mapped location and read the full comment in context. Preserve the Git index.

In a directory or repository, focus on project-owned source and skip generated, vendored, and third-party files.

## 2. Inspect and edit

Use the language's parser or tokenizer when available. Otherwise inspect each candidate in context. Edit only text you can identify as a comment. Comment markers inside strings, fixtures, and embedded data need particular care.

Apply these checks in order:

1. **Required text.** Preserve API documentation, docstrings, legal notices, and language or tool directives, including their placement. Examples include JSDoc and YARD tags, build constraints, and linter suppressions. If you suspect a problem in required text, report it.
2. **Useful information.** Keep non-obvious behavior and local rationale, such as invariants, ordering, compatibility constraints, and why a workaround exists. Retain active TODOs and references that help maintainers act. For broader decisions, use existing project documentation as context. Keep any warning the maintainer needs at the edit site.
3. **Redundant or obsolete text.** Delete confirmed restatements and obsolete notes. Trim mixed comments while preserving their useful parts. If a comment conflicts with the code, use tests, contracts, or history to establish the intended behavior. Correct stale wording only when that evidence settles the conflict. If the comment might describe a bug in the code, keep it and report the discrepancy.

For example, `# Enqueue the job.` above `enqueue(job)` is redundant. Keep `# Enqueue before commit because v1 clients cannot retry a missing job.` while that constraint applies.

Limit edits to comments and whitespace needed to remove them. Preserve token boundaries, significant newlines, and unrelated changes. Treat linter changes, ratchets, issue filing, and new documentation workflows as separate tasks.

## 3. Verify and report

Run relevant syntax, lint, or test checks in read-only mode. Report checks you could not run without modifying files. Then compare the final files with their pre-run state to confirm that only scoped comment text and necessary whitespace changed. If an edit's safety is uncertain, undo that edit and report the reason. Repeat the comparison after any undo.

Summarize the scope, edits, unresolved findings, and checks run. When asked for counts, report actual comment-only lines removed and count inline removals separately.
