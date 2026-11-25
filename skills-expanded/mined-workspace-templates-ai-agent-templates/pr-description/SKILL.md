---
name: pr-description
description: Drafts a pull request title and description from the diff between your branch and the base branch, ready to paste into GitHub.
disable-model-invocation: true
---

Write a pull request description for the current branch. Base branch: $ARGUMENTS (use main if empty).

1. Run `git log --oneline <base>..HEAD` and `git diff <base>...HEAD --stat`, then read the diff of the files that carry the logic. Skip lockfiles and generated files.
2. Check for a pull request template in .github/ and follow its headings if one exists.
3. Write a title under 70 characters that names the outcome, not the activity.
4. Write these sections: **Summary** (two or three sentences on what and why), **Changes** (bullets grouped by area, not by commit), **How to test** (exact commands or clicks, with the expected result), **Risk** (migrations, config, behavior changes, rollback).
5. Mark anything you cannot know from the code, such as the ticket or screenshots, as `Fill in:` instead of guessing.

Print the result in one Markdown block. Ask whether to adjust it. Do not run `gh pr create` unless the user then asks for it.
