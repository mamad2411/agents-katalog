---
name: create-pr-with-template
description: Create a GitHub Pull Request with gh CLI and prefer repository PR templates automatically. Use this whenever the user asks to open/create a PR, especially when template compliance is needed. If multiple templates exist, ask the user which template to use.
---

# Create PR with Template

Use this skill to create pull requests reliably using the GitHub CLI while respecting repository PR templates.

## Outcomes

- Create a PR with `gh pr create`.
- Use a repository PR template when available.
- Ask the user to choose only when multiple templates exist.
- Return the final PR URL.

## Safety and Scope

- Use `gh` for all GitHub PR operations.
- Do not force push.
- Do not create or edit commits unless the user asked for that separately.
- If the current branch has no remote tracking branch, push with `-u` before creating the PR.

## Workflow

### 1) Inspect branch and diff context

Run:

```bash
git status --short
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name @{u}
git log --oneline --decorate -n 20
```

If upstream is missing, note it and prepare to push current branch with `git push -u origin <branch>`.

Determine base branch:

- Prefer repository default branch from GitHub when available.
- Otherwise use `main`.

### 2) Discover PR templates

Search for templates in common locations:

- `.github/PULL_REQUEST_TEMPLATE.md`
- `PULL_REQUEST_TEMPLATE.md`
- `docs/PULL_REQUEST_TEMPLATE.md`
- `.github/PULL_REQUEST_TEMPLATE/*.md`

Behavior:

- If no template exists: generate a clean body with a short summary.
- If exactly one template exists: use it automatically.
- If more than one template exists: ask the user which template to use and wait for the answer.

### 3) Build title and body

Gather PR content from branch commits and diff since base branch.

Guidelines:

- Keep title concise and outcome-focused.
- Keep body short and clear.
- Preserve template section headers when template is used.
- Fill placeholders with concrete changes from the branch.
- Remove instructional comments from template in final body.

### 4) Ensure remote branch is ready

- If branch is not pushed/upstream missing, push with upstream:

```bash
git push -u origin <branch>
```

- If branch already tracks remote, push normally only if needed:

```bash
git push
```

### 5) Create the PR with gh

Use heredoc body for stable formatting:

```bash
gh pr create --base <base> --head <branch> --title "<title>" --body "$(cat <<'EOF'
<body>
EOF
)"
```

If the repository requires a specific template format, ensure body follows that template.

### 6) Return result

After successful creation, return only the essential outcome:

- PR URL
- Base and head branches
- Template used (or `none`)

## Multiple Template Prompt Contract

When multiple templates are found, ask one clear question listing options by number and file path:

- Option 1: `<path>`
- Option 2: `<path>`

Then continue only after user picks one.

## Failure Handling

- If `gh` is not authenticated, instruct user to run `gh auth login` and retry.
- If PR already exists for head/base, return the existing PR URL.
- If push fails due to permissions, report the exact failure and stop.

## Response Contract

Final response must include the PR URL explicitly, for example:

`PR created: https://github.com/org/repo/pull/123`
