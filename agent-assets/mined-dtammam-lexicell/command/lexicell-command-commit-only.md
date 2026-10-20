# Safely stage and commit without pushing. All quality gates enforced.

## Required input
- Commit message provided as $ARGUMENTS.
- Reject generic messages (update, fix, wip). The message describes the decision, not the diff.
- If no message provided, ask for one.

## Workflow
1. Confirm the branch with `git branch --show-current`. Never commit directly to main.
2. Run `git status --porcelain` and `git diff` to understand what will be staged.
3. Stage changes by EXPLICIT path. Never `git add -A`, `git add .`, or `git commit -a` (a hook blocks them).
4. Commit using HEREDOC format with the Co-Authored-By and Claude-Session trailers.
5. Verify the commit landed with `git log -1`. The pre-commit hook refuses red; a refused commit swallowed by a piped command is the known phantom-commit failure.

## Failure handling
If the commit fails: stop. Do not retry blindly. Do not amend.
Read the error. Fix the root cause. Re-run from step 1.
Never use --no-verify.

If the same failure repeats, add it to docs/exec-plans/tech-debt-tracker.md.
