---
name: code-review
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git blame:*), Bash(git show:*), Bash(git rev-parse:*), Bash(git ls-files:*)
description: Code review the uncommitted changes in the working tree
disable-model-invocation: false
---

Provide a code review for the uncommitted changes (staged and unstaged) in the working tree.

To do this, follow these steps precisely:

1. Use a Haiku agent to run `git status` and `git diff HEAD` and decide whether a review is warranted. Skip if any of these is true: (a) there are no changes, (b) the change is purely cosmetic (whitespace, formatting), (c) it's an automated change (lockfile bump only, generated file), or (d) it's trivial (a one-line typo fix). If skipping, tell the user why and stop.
2. Use a Haiku agent to give you a list of file paths to (but not the contents of) any relevant CLAUDE.md files: the root CLAUDE.md (if one exists) and any CLAUDE.md files in the directories whose files were modified.
3. Use a Haiku agent to read the diff and return a concise summary of the change.
4. Launch 5 parallel Sonnet agents to independently review the change. Each agent returns a list of issues and the reason each issue was flagged (CLAUDE.md adherence, bug, historical context, etc.):
   a. Agent #1: Audit the changes for compliance with the relevant CLAUDE.md files. Note that CLAUDE.md is guidance for Claude as it writes code, so not all instructions will be applicable during review.
   b. Agent #2: Read the file changes and shallow-scan for obvious bugs. Stay inside the changes; focus on large bugs and avoid small issues and nitpicks. Ignore likely false positives.
   c. Agent #3: Read `git blame` and `git log -p` on the modified lines to identify bugs in light of historical context — e.g., the change silently reverts a prior fix.
   d. Agent #4: Read recent commits that touched these files (`git log --oneline -n 30 -- <files>`) and any in-tree notes (TODO, FIXME, NOTE) near the modified lines. Check whether prior guidance applies to the current change.
   e. Agent #5: Read code comments in the modified files and ensure the change complies with any guidance in the comments.
5. For each issue found in step 4, launch a parallel Haiku agent that takes the diff, the issue description, and the list of CLAUDE.md files (from step 2), and returns a confidence score from 0-100. For issues flagged due to CLAUDE.md, the agent must double-check that the CLAUDE.md actually calls out that issue specifically. The scale (give this rubric to the agent verbatim):
   a. 0: Not confident at all. False positive that doesn't stand up to light scrutiny, or a pre-existing issue.
   b. 25: Somewhat confident. Might be real, may also be a false positive. The agent couldn't verify it. If stylistic, it wasn't explicitly called out in the relevant CLAUDE.md.
   c. 50: Moderately confident. Verified as a real issue, but possibly a nitpick or rare in practice. Relative to the rest of the change, not very important.
   d. 75: Highly confident. Double-checked and very likely a real issue that will be hit in practice. The existing approach is insufficient. The issue is important and will directly impact functionality, or it is directly mentioned in the relevant CLAUDE.md.
   e. 100: Absolutely certain. Confirmed real and will happen frequently in practice. Evidence directly confirms it.
6. Filter out any issues with a score less than 80. If no issues remain, report "No issues found" and stop.
7. Print the review to the user as markdown using the format below. Be brief. Cite each issue with a local path:line reference. No emojis.

Examples of false positives (for steps 4 and 5):

- Pre-existing issues unrelated to the change.
- Something that looks like a bug but isn't.
- Pedantic nitpicks a senior engineer wouldn't call out.
- Issues a linter, typechecker, or compiler would catch (missing imports, type errors, formatting). Assume CI covers these.
- General code-quality complaints (test coverage, security posture, doc completeness) unless explicitly required in CLAUDE.md.
- Issues called out in CLAUDE.md but explicitly silenced in the code (lint ignore comments, eslint-disable, etc.).
- Functional changes that are likely intentional or directly related to the broader change.
- Real issues that sit on lines the change did not modify.

Notes:

- Do not run build, test, or typecheck commands. Assume CI covers them.
- Read file contents via the Read tool. Use the Bash tool only for the read-only git commands listed in `allowed-tools`.
- Make a todo list first.
- Cite every bug with a path:line reference. Use the local-path format (e.g., `src/foo/bar.ts:L12-L18`) — no remote URLs needed.
- Provide at least one line of context before and after the cited line when choosing the range.

Final output format

If issues were found (example assumes 3):

---

### Code review

Found 3 issues:

1. <brief description of bug> (CLAUDE.md says "<...>")

`path/to/file.ts:L12-L18`

2. <brief description of bug> (some/nested/CLAUDE.md says "<...>")

`path/to/other.ts:L40-L46`

3. <brief description of bug> (bug due to `<file and code snippet>`)

`path/to/third.ts:L88-L92`

---

If no issues passed the filter:

---

### Code review

No issues found. Checked for bugs and CLAUDE.md compliance.

---
