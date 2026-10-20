Address the review of the open pull request for the current branch. Work on this branch only.

1. Find the pull request: `gh pr view --json number,url,headRefName`. Read every review comment:
   `gh pr view --comments`, `gh api repos/{owner}/{repo}/pulls/N/comments` (inline comments, with
   file and line) and the `ai-review` job's tracking comment on the pull request. Also read
   `gh pr checks` for failed jobs.
2. List the findings before touching anything: file:line, what the reviewer asks, and whether you
   will fix it or propose to dismiss it with a reason. A finding that contradicts an approved spec or
   the plan of record is dismissed with that reference, never fixed around.
3. Address each finding in its own commit (conventional commit, scope = module, agent trailer),
   following CLAUDE.md conventions. Run `make verify` before every commit. A finding that needs a
   new dependency goes into the PR body with license and reason.
4. Reply to the thread of each finding with what changed (commit hash) or why it was dismissed, via
   `gh api` on the review comment, and update the PR body's "Reviewer notes".
5. Stop before `git push`: list the commits and ask the Owner to push. Never push, never merge,
   never close the pull request.
