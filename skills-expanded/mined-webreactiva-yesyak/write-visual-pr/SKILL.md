---
name: write-visual-pr
description: Creates a pull request whose description opens with a plain-language paragraph and then explains the change with ASCII trees and diagrams and validated Mermaid charts. It covers the overview, request flow, data, configuration, how it was built and checked, and follow-ups. Use it whenever the user asks to create, open or write a pull request or merge request, write a PR description, or explain a branch to reviewers, especially when they want it understandable for non-technical readers or with diagrams.
---

# Write visual PR

## 1. Check the ground

```bash
git status --short                       # clean tree?
git remote -v && gh auth status          # remote and auth
git fetch -q origin && git status -sb    # branch pushed and in sync?
gh pr list --state all --json number,headRefName --jq '.[] | select(.headRefName == "<branch>")'   # PR already exists? (old gh has no --head)
git log --oneline <base>..HEAD | wc -l   # commit count
git diff --shortstat <base>...HEAD       # size
```

- If the remote is on GitLab, use `glab` for the same checks: `glab auth status`, `glab mr list --source-branch <branch>`.
- If neither tool is installed or signed in (common in cloud sessions), use the tools that the environment gives (for example an MCP server) for the same checks and for the creation. Do not stop only because `gh` or `glab` is missing.
- If the branch is not on the remote, ask before you push.
- If there is no remote, or the user wants no hosted PR, stop at the body. Report its path and go on with the next step.
- If a PR already exists, update it instead of creating another one.
- Collect real numbers for the description: tests on the base branch and on the branch, commits, files, decisions. Verify each number; do not estimate.

## 2. Write the body

Save it to `.scratchpad/<slug>/pr-body.md`. Write it in the document language of `simplified-technical-language`, with `plain-visual-docs`.

```markdown
## In plain words          one paragraph, no jargon
## New and changed files   ASCII tree with + and ~
## How it works            the diagrams of the spec, updated to what was built (say what
                           changed); a sequence diagram only when a second actor matters
## Data and configuration  only if they change: erDiagram, data behavior, variables,
                           and a short "try it" block
## How it was checked      tests before and after, criteria met, reviews done
## Known follow-ups        what is intentionally left out
<attribution line required by the environment>
```

For a bug fix (`bug-intake`), use a short body instead: In plain words, Reproduction, Root cause, Fix, Contract (source or assumed), Tests.

Rules:

- Aim for a body that a reviewer reads in five minutes, about 120 lines.
- Do not link to files that are not in the repository (for example, `.scratchpad/` reports). Summarize them instead.
- If the run was unattended (`unattended-run`), add "Decisions taken without the user" before "Known follow-ups". If the run left skill feedback, add a short table of the proposed skill changes.

## 3. Validate

- Render every Mermaid block (`plain-visual-docs`). Fix any failure before you publish.
- Re-read every number and claim against the repository.

## 4. Create

Push and create the PR only when the user asked for it:

```bash
gh pr create --base <base> --head <branch> \
  --title "<title in the commit format of git-commit-organizer>" \
  --body-file .scratchpad/<slug>/pr-body.md

# GitLab
glab mr create --target-branch <base> --source-branch <branch> \
  --title "<title>" --description "$(cat .scratchpad/<slug>/pr-body.md)"
```

To change the body later, use `gh pr edit <n> --body-file …`. If it fails with a GraphQL error about Projects (classic), use `gh api repos/<owner>/<repo>/pulls/<n> -X PATCH -F body=@.scratchpad/<slug>/pr-body.md`. On GitLab, use `glab mr update <n> --description "$(cat .scratchpad/<slug>/pr-body.md)"`.

Report the URL. Offer `pr-reviewer-guide` as a follow-up comment.
