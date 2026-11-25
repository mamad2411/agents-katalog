---
name: review-changes
description: Review a diff, branch or pull request for correctness, tests and clarity, and report findings in order of severity. Use when asked to review a change.
---

# Review changes

1. Read the change's description, then the full diff, then the code around it.
2. Ask of each hunk: what does it do, what could it break, and which test would notice?
3. Look hard at error paths, boundaries, ordering and concurrency, and at anything that
   changes a public interface or stored data.
4. Check that tests cover the new behavior, and that a bug fix has a test that fails without it.
5. Check that names and comments make the code understandable to someone new.

Report a one-line verdict first, then findings from most to least serious, each with file,
line and a suggested fix. Keep taste separate from real problems, and list what you did not
check.
