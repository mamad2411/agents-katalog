---
name: review-changes
description: Reviews your own uncommitted changes before you commit and lists problems by severity, so you catch them before a reviewer does.
disable-model-invocation: true
---

Review my uncommitted changes. Focus from the user: $ARGUMENTS

1. Run `git status --short`, `git diff` and `git diff --staged`. Read untracked files that are new code too.
2. For each changed function, open the surrounding file so you judge it in context, and search for its callers.
3. Check, in order: bugs and unhandled cases (null, empty, off-by-one, async errors); security (user input, secrets, injection); behavior changes not mentioned by the user; missing or weak tests for new logic; leftover `console.log`, `print`, `debugger`, TODOs and commented-out code; unrelated edits that belong in another commit; files that should be ignored.
4. Run the project's lint and fast tests and include failures.
5. Do not edit anything.

Report findings as **Critical**, **Should fix** and **Nit**, each with `file:line`, the problem and a one-line fix. If nothing is wrong, say what you checked. End with a suggestion for how to split the work into commits if it covers more than one concern, then ask which findings to fix.
