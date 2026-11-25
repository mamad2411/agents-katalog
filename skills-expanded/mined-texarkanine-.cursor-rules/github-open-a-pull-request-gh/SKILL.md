---
name: "github-open-a-pull-request-gh"
description: "The one and only correct way to open a GitHub Pull Request with the `gh` command-line tool"
---


# Opening a Pull Request

This rule guides you through the process of opening a pull request.

**IMPORTANT:** when running `git` commands in this process, **always** use `git --no-pager`! The terminal will get STUCK if you do not use `git --no-pager`!

## Pre-flight Checks

1. Ensure you are on a non-default branch (not `main` or `master`).
	- **HARD ERROR:** If on a default branch, STOP. Do NOT create a branch yourself. Output an error and instruct the USER to switch to a feature branch.

## Information Gathering

1. Extract the GitHub Owner and Repository name from output of `git remote -v`
2. Extract ticket or issue ID if present:
	- Parse current branch name for ticket/issue patterns (e.g., `feature/ABC-123`, `fix/issue-456`).
	- If the branch is ahead of default, check the new commits' messages for ticket/issue references: `git --no-pager log --oneline main..HEAD`
3. Resolve the pull request template. Read **only** the template you will use — do not load the others into context:
	1. Look in this repository first (`.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE.md`; capitalization may vary). If found, use it.
	2. If none, fetch the repository **owner's** community-health default from their `.github` repository at the same paths (e.g. `gh api "repos/<owner>/.github/contents/.github/pull_request_template.md" --jq .content`, base64-decode; try common capitalizations on 404). If found, use it.
	3. If that is also missing, read `references/pull_request_template.md` next to this skill and use that.

## Preparation

1. Commit all uncommitted changes if needed:
	- Use a [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0) message.
		- Prefer `feat` or `fix` types.
		- If a ticket/issue ID exists, include it in square brackets at the end of the message (e.g., `feat(scope): description... [ABC-123]`).
		- Use existing scopes from commit history if possible; otherwise, omit scope.
2. Push the changes up to the feature branch.
	- **HARD ERROR:** If this push fails, STOP. Output an error and instruct the USER to investigate. DO NOT continue with the rest of the process.
3. Complete the PR template:
	- Fill all sections with appropriate info.
	- For checklists, check off only items you have completed. Leave others unchecked.
	- Do NOT remove template sections unless explicitly instructed by the template.
	- When writing about files in the project, hyperlink the filename to the file on the feature branch. Example:
		- pattern:
			```markdown
			* Added [README.md](https://github.com/<owner>/<repo>/blob/<branch>/docs/README.md) to doc site
			```
		- example for repo `texarkanine/onair` on feature branch `fix-ip`:
			```markdown
			* Added [README.md](https://github.com/texarkanine/onair/blob/fix-ip/docs/README.md) to doc site
			```

## Opening the Pull Request

1. You **MUST** write the PR body to a temporary file as follows:
	1. Use `mktemp` to create a temp file
	2. You **MUST** write each line using chained `echo` commands with `&&`, single quotes, and proper escaping for single quotes (`'\''`).
		Example:
		```bash
		TEMPFILE=$(mktemp) && echo '# Feature: New User Authentication' > "${TEMPFILE}" && echo '' >> "${TEMPFILE}" && echo 'Implements new user authentication as specified in ABC-123.' >> "${TEMPFILE}" && echo '' >> "${TEMPFILE}" && echo '## Changes' >> "${TEMPFILE}" && echo '- Added OAuth2 integration' >> "${TEMPFILE}" && echo '- Created user session management' >> "${TEMPFILE}" && echo 'This doesn'\''t affect existing users.' >> "${TEMPFILE}"
		```
2. Open a draft pull request using the `gh` CLI:
	- Use `--body-file "${TEMPFILE}"` for the body.
	- For the title:
		- If only one commit exists and it is a conventional commit, use its message as the title.
		- Otherwise, generate a conventional commit-style title.
	- Use the `--draft` flag.
		Example:
		```bash
		gh pr create --draft --title "feat(auth): implement OAuth2 authentication" --body-file $TEMPFILE
		```
3. Report the result to the user with ONLY and EXACTLY the following message (filling in the `<information>` appropriately):
	Example:
	```markdown
	PR Opened: [feat(auth): implement OAuth2 authentication](https://github.com/<owner>/<repo>/pull/<pr_number>)
	```

