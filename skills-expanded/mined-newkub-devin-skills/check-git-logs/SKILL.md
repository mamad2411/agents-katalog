---

name: check-git-logs
description: Browse a file's git log per commit until a condition matches — supports local and remote repos
argument-hint: "[scope]"
related:
  - deep-debug
  - git-file-history
  - restore-files
  - report
  - suggest-next-action

---

## Goal

Find the change history of a specified file by walking `git log` from newest backwards until the user's condition is met (e.g. file not empty, contains a certain value, modified by a particular person). Supports both local repos and remote GitHub repos

## Scope

- Specify the target file and the condition to search for
- Supports local git repos and remote GitHub repos
- Show the commits matching the condition along with the file content in that commit
- Used as a helper tool in `/deep-debug` and `/restore-files`
- Boundary: finds condition-matching commits only — interactive viewer → `/git-file-history`; evolution analysis → `/diff-file-history`

- See also: /git-file-history, /restore-files-from-my-dotfiles

## Execute

### 1. Identify Target And Condition

> Goal: know what you are looking for

1. Take the file path from the argument or context
2. Take the repo source: a local path or `owner/repo` on GitHub
3. Take the condition from the user, e.g.:
   - "file is not empty" (`mcpServers` has keys)
   - "has a line containing X"
   - "file was deleted"
   - "file was modified by author Y"
4. If there is no condition → show the full history

### 2. Local Repo

> Goal: use git log on a local repo

1. Run `git log --all --pretty=format:"%H %ad %an %s" --date=iso <file>` to see the related commits
2. If the file was renamed → add `--follow`
3. For each commit from newest to oldest:
   - Run `git show <sha>:<file>` to view the content
   - Check the condition
   - If it matches → stop and report
4. If nothing is found → report that no commit matches the condition

### 3. Remote Repo

> Goal: use the GitHub API on a remote repo

1. Use `gh repo view <owner/repo>` to confirm the repo
2. Use `gh api repos/<owner>/<repo>/commits?path=<file>&per_page=100` to fetch commits
3. For each commit from newest to oldest:
   - Use `gh api repos/<owner>/<repo>/contents/<file>?ref=<sha>` to fetch the content (base64)
   - decode base64
   - Check the condition
   - If it matches → stop and report
4. If nothing is found → paginate with the `page` parameter

### 4. Report

> Goal: summarize the results

1. Produce a `/report` showing: No, Commit SHA, Date, Author, Message, Match
2. If the condition is met → show the file's content in that commit (if not sensitive)
3. If nothing is found → state that nothing was found
4. Run `/suggest-next-action`, e.g. restore, bisect, or view the previous commit

## Rules

### 1. Local And Remote

- Local uses `git log` + `git show`
- Remote uses `gh api`
- If no repo is specified → use the current local repo

### 2. Condition Parsing

- Supports content-based conditions: `contains`, `not-empty`, `empty`, `equals`, `size-gt`
- If the condition is a string → use `contains` on the content
- If the condition is a JSON path → verify with `jq` or Python

### 3. Safety

- Never modify files or the repo
- Never expose secrets in the report
- If the content has sensitive data → redact before displaying

### 4. Stop Condition

- Stop immediately at the first commit matching the condition (the most recent match)
- If the user wants the full list → they must state it explicitly

- Use /restore-files-from-git-log if needed

## Expected Outcome

- The condition-matching commit is found
- Reports commit SHA, date, author, message, and content
- Supports both local and remote repos
- Works with `/deep-debug` and `/restore-files`
