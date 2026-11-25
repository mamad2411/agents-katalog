---
name: creating-pull-requests
description: Create useful pull requests or merge requests with clear reviewer-focused descriptions. Use when opening a PR or MR, especially when the description should explain the problem, summarise the changes, and record testing in a standard structure.
metadata:
  author: gerph@gerph.org
license: MIT
---
# Creating Pull Requests

Use this skill when opening a pull request or merge request and the
description needs to be structured for reviewers.

## Workflow

1. Confirm the branch, base branch, and repository.
2. Gather the commit summary and the actual testing that was performed.
3. Decide whether the PR should be a draft.
4. Write the PR title and description.
5. Create the PR or MR non-interactively where possible.
6. Re-read the created PR to confirm the title, body, draft state, and target.

## Description structure

Use these sections in the PR or MR body:

```markdown
# Summary

What problem is being solved, why the change is being made, and a short
summary of what changed.

# Changes

What was actually done. Use this when there is more than one change, when
changes are related, or when the relationship between commits would not be
obvious from the summary alone.

# Testing

What tests were performed.
```

## Content rules

* Write for reviewers, not for commit archaeology.
* `# Summary` should explain the motivation first, then the high-level result.
* `# Changes` should describe the concrete work without turning into a
  file-by-file changelog unless that detail is genuinely useful.
* `# Testing` should list the checks that were actually run.
* If local validation was possible, say that it was run.
* If CI workflows were part of the change, say that they ran and whether they
  passed.
* If a test could not be run, say why.
* Do not claim tests that were not performed.

## Draft PR rules

Create the PR or MR as a draft when:

* the change is incomplete,
* more work is expected before review is useful,
* testing is blocked or known to be insufficient,
* known issues remain that would waste reviewer time.

If the work is complete enough for review and the relevant checks have passed
or are reasonably explained, create a normal PR.

## Practical guidance

* Prefer a short, descriptive PR title that matches the reviewer-facing change,
  not necessarily the exact commit subject.
* When the body is more than a couple of lines, prepare it in a file or
  heredoc rather than trying to squeeze it into a single command argument.
* Reuse exact test outcomes where they matter, such as a passed CI run URL or
  an explanation that a local compiler or dependency was unavailable.
* If there are uncommitted local changes unrelated to the branch being opened,
  be aware that some tools may warn even though the PR can still be created.

## Minimum useful PR

If the change is simple, the sections can still be brief:

```markdown
# Summary

Add the missing CI workflow for the portable build and generated
documentation.

# Testing

- Ran the workflow on the branch and confirmed it passed.
```
