---
name: engineer-pr
description: Commit, open the PR, and triage review-bot comments
---

You're now asked to open a PR. Follow these steps carefully:

1. First, make sure all tests pass for the current branch. Run the appropriate test suite for this project and confirm everything is green. If anything fails, fix it before proceeding.

2. Commit the changes you made. Use a clear, concise commit message that summarizes the change.

3. Move the associated GitHub issue to "in review": `gh issue edit <number> --add-label "status:in-review" --remove-label "status:in-progress"` (adjust label names to match the repo's existing labels).

4. Open a Pull Request with the execution details. Include a `Closes #<number>` line in the description so the issue auto-closes on merge, and comment the PR link back on the issue: `gh issue comment <number> --body "PR opened for review: #<pr-number>"`.

   Important: don't mention any AI- or Codex-related tooling in the PR description.

5. After opening the PR, wait 3 minutes, then check for comments from the automated code review tool. If nothing shows up, wait another 3 minutes and check again.

6. Once you get feedback from the automated review, go through each comment carefully. Decide which ones require a fix and which can be safely dismissed or explained. Present your recommendations to the user and ask for permission before making changes.

7. For comments that require a fix:
   a. Make the necessary code changes.
   b. Commit them with a clear message.
   c. Push the new commit(s) to the same branch.

8. After addressing the comments and pushing updates, tell the user the task is complete and ready for their final review and manual merge.

**Golden rule**: only commit the files you actually changed. Don't use `git add .` — it risks committing files that shouldn't be committed.

Your final output should be a message to the user, formatted as follows:

<task_completion_message>
Task complete:
- Tests passing
- Changes committed
- GitHub issue #[ISSUE NUMBER] moved to "in review"
- PR opened: [PR TITLE]
- Automated review comments addressed and fixes pushed

The PR is now ready for your final review and manual merge.

[PR LINK]
</task_completion_message>
