---
name: all-github-repo
description: List all GitHub repositories of the user and organizations they are a member of
argument-hint: "[username]"
allowed-tools:
  - read
  - exec
  - report
  - suggest-next-action
  - ask_user_question
triggers:
  - user
  - model
related:
  - list-github
  - search
  - report
  - suggest-next-action
---

## Goal

List all GitHub repositories of the personal user and the organizations they are a member of, filtering out forks and archived repos.

## Scope

Use the `gh` CLI to fetch repos from the user and each org, then combine them into a single table sorted by most recent updatedAt.

See also: /list-github-repo, /open-github, /list-github-project, /list-github-star-latest, /search-github-star

## Execute

### 1. Get User And Organizations

> Goal: Know all owners to list

1. If a `username` is passed as an argument, use it as `user_login`
2. Otherwise, run `gh api user --jq .login` to find the authenticated user
3. If `gh` is not logged in, stop and suggest `gh auth login`
4. Run `gh api user/orgs --jq '.[].login'` to find the organizations the user is a member of
5. Combine `user_login` and the org logins into the `owners` list

### 2. List Personal Repositories

> Goal: Fetch the personal user's repos

1. Run `gh repo list <user_login> --source --no-archived --json name,description,primaryLanguage,stargazerCount,forkCount,updatedAt,visibility,url --limit 1000`
2. If the result returns 1000 items, warn that pagination may be needed
3. Save the result as a JSON array, adding an `owner` field set to `<user_login>`

### 3. List Organization Repositories

> Goal: Fetch each org's repos

1. For each `org` in the `owners` list that is not `user_login`:
   - Run `gh repo list <org> --source --no-archived --json name,description,primaryLanguage,stargazerCount,forkCount,updatedAt,visibility,url --limit 1000`
   - Save the result as a JSON array, adding an `owner` field set to `<org>`
2. If an org has more than 1000 repos, warn and continue with pagination
3. If the API returns 403 or 404 for any org, skip that org and record the reason

### 4. Merge And Format

> Goal: Present the results in a readable way

1. Merge all JSON arrays with `jq -s 'add'` or an equivalent script
2. Sort by `updatedAt`, most recent first
3. Convert `updatedAt` to `YYYY-MM-DD`
4. Extract `primaryLanguage.name`; if missing, show `n/a`
5. Produce a `/report` with these columns:
   - No.
   - Owner
   - Name
   - Description
   - Language
   - Stars
   - Forks
   - Updated
   - Visibility
   - URL
6. Summarize the total number of repos and the number of repos per owner

### 5. Suggest Next Steps

> Goal: Suggest the next actions

1. To inspect a repo's metadata, run `/open-github <owner>/<name>`
2. To open the repo page in a browser, run `/open-github`
3. To list only the personal user's repos, run `/list-github-repo`
4. To view that owner's GitHub Projects, run `/list-github-project`
5. To view starred repositories, run `/list-github-star-latest` or search within stars with `/search-github-star`
6. Run `/suggest-next-action` to suggest more

## Rules

### 1. GitHub Authentication

- Must log in with `gh auth login` first
- If `gh api user` returns an error, stop and suggest logging in

### 2. Exclude Forks And Archived

- Use `--source` to filter out forks
- Use `--no-archived` to filter out archived repos
- If the user wants to include archived repos, remove `--no-archived`

### 3. Pagination

- Use `--limit 1000` by default
- If an owner has more than 1000 repos, warn and use `gh api`/`graphql` for pagination

### 4. Output

- Always use `/report`
- The No. column must be the first column, ordered 1, 2, 3, ...
- Do not show secrets, tokens, or sensitive data
- Include a summary of the total repo count and the per-owner counts

## Expected Outcome

- A list of all repos of the user and the organizations they are a member of
- Complete data: owner, name, description, language, stars, forks, updated, visibility, url
- Excludes forks and archived repos
- Includes next actions for the selected repo
