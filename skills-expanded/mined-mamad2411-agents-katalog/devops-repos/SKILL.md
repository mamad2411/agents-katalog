---
name: devops-repos
description: Azure DevOps repository management, pull requests, branching, and code operations. Use when asked to manage repos, create or review PRs, browse code, or work with branches.
---

# DevOps Repos

## When to Use

- User asks to list, create, or manage Git repositories
- User wants to create, review, or manage pull requests
- User needs to browse repository files or branches
- User mentions code reviews, merge conflicts, or PR approvals

## Instructions

### Branch Naming Conventions

- `feat/<description>` — new features
- `fix/<description>` — bug fixes
- `chore/<description>` — maintenance
- `docs/<description>` — documentation only
- `refactor/<description>` — code restructuring

### Pull Request Workflow

**Creating a PR:**
1. Use `devops_create_pull_request` with clear title and description
2. Link to related work items when applicable
3. Target branch is usually `main` unless specified

**Reviewing a PR:**
1. Use `devops_get_pull_request` to fetch details
2. Use `devops_approve_pull_request` with appropriate vote

**Vote values:** 10=approve, 5=approve with suggestions, 0=no vote, -5=wait, -10=reject

## Tools

- `devops_list_repos` — List all repositories in a project
- `devops_get_repo` — Get repository details
- `devops_create_repo` — Create a new Git repository
- `devops_list_branches` — List branches in a repository
- `devops_get_file_content` — Read a file from a repo
- `devops_list_pull_requests` — List pull requests (filter by status)
- `devops_get_pull_request` — Get full PR details
- `devops_create_pull_request` — Create a new pull request
- `devops_approve_pull_request` — Vote on a pull request

## See Also

- **devops-boards** — work items and sprints
- **devops-pipelines** — CI/CD pipeline operations
