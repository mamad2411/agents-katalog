---
name: sending-pull-request
description: Prepare a conventional branch, write or review a pull/merge request title and body, then push and create or update the GitHub PR. Use when work is ready for review or PR/MR copy needs drafting or review.
---

# Send a pull request

When asked only to write or review a PR/MR title or body, inspect the supplied context, read [BODY.md](BODY.md), and return the copy without changing the repository or forge. Read [MEDIA.md](MEDIA.md) when the body needs screenshots or video.

To send work for review:

1. Fetch `origin`, resolve the current and default branches, and inspect commits and working-tree changes against `origin/<default>`. Stop if there is no work to send.

2. Put the work on a conventional `<type>/<short-kebab-description>` branch without stashing or changing it:

   - Keep a conventional non-default branch.
   - On the default branch, choose the name from the work using its Conventional Commit type, then preserve every commit and working-tree change before resetting the local default branch:

     ```bash
     git switch --no-track -c <new-branch>
     git branch -f <default> origin/<default>
     ```

   - Rename a clearly auto-generated placeholder branch with `git branch -m <new-branch>`.
   - Stop on another non-conventional branch unless the user asked to rename it.

3. Verify that the branch and work are unchanged. Stop if any intended change is uncommitted.

4. Inspect the commits and diff against the default branch. Write a Conventional Commit title under 70 characters, read [BODY.md](BODY.md), and write the body from what the diff cannot explain.

5. Check for an open PR from the current branch. Push with tracking; use `--force-with-lease` only after an intentional history rewrite.

6. Create the PR with `--assignee @me`, or update its title and body, using a temporary `--body-file` and deleting it afterward. A direct user invocation creates a ready PR; an autonomous invocation creates a draft unless the user requested otherwise.

7. Return the PR URL.
