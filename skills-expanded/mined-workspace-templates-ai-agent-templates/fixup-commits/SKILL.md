---
name: fixup-commits
description: Matches staged review fixes to the commits they belong to, creates fixup commits and autosquashes once you approve.
disable-model-invocation: true
---

Turn the staged changes into fixup commits for the branch. Base branch: $ARGUMENTS (use main if empty).

1. Run `git status --short` and `git diff --staged`. If nothing is staged, stop. Never stage files yourself.
2. List the branch commits with `git log --oneline <base>..HEAD`. Stop if HEAD is on the base branch itself.
3. For each staged hunk, run `git blame -L <range> <base>..HEAD -- <file>` on the original lines and note which branch commit last touched them. A hunk touching only new lines of one commit maps to that commit.
4. Show a table: hunk, file, target commit hash and subject, confidence. Mark hunks with no clear owner as "unmatched" and leave them staged.
5. Ask: "Create these fixups?" After a yes, split the index per target and run `git commit --fixup <hash>` for each.
6. Check whether the branch was pushed with `git status -sb`. If it was, warn that autosquash rewrites history and ask again.

Then show `git log --oneline` and ask before running `git rebase -i --autosquash <base>` with GIT_SEQUENCE_EDITOR=true. Never force push.
