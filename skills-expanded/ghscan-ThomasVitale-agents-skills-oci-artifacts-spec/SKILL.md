---
name: manage-pull-requests
description:  
  A skill for managing pull requests in Forgejo repositories using the forgejo-cli.
  Supports creating, listing, viewing, merging, closing, and commenting on PRs.
license: Apache-2.0
compatibility: |
  Requires forgejo-cli (https://codeberg.org/forgejo-contrib/forgejo-cli/wiki/PRs).
  Agent must have network access to the Forgejo API.
metadata:
  category: development-tools
  tags: [git, forgejo, pull-requests, automation]
---

# Manage Pull Requests

## Overview
This skill enables agents to automate pull request (PR) management in Forgejo repositories using the `forgejo-cli` tool. It supports common PR operations, making it ideal for CI/CD pipelines, code reviews, and team collaboration workflows.

---

## Instructions

### Prerequisites
- `forgejo-cli` must be installed and configured with Forgejo API credentials.
- The agent must have access to the target repository.

### Supported Actions
- **List PRs:** Fetch all open PRs for a repository.
- **View PR:** Retrieve details of a specific PR.
- **Create PR:** Open a new PR from a branch or fork.
- **Merge PR:** Merge an approved PR into the target branch.
- **Close PR:** Close a PR without merging.
- **Comment on PR:** Add or update comments on a PR.

---

## Parameters

### Input Format
All actions require a JSON object with the following structure:

```json
{
  "action": "<action>",
  "repo": "<owner/repo>",
  [ "pr_id": "<pr-id>", ]
  [ "branch": "<source-branch>", ]
  [ "target_branch": "<target-branch>", ]
  [ "title": "<pr-title>", ]
  [ "description": "<pr-description>", ]
  [ "comment": "<comment-text>", ]
  [ "force": <boolean> ]
}
```

### Action-Specific Parameters

| Action    | Required Parameters                          | Optional Parameters                     |
|-----------|----------------------------------------------|-----------------------------------------|
| `list`    | `repo`                                       | —                                       |
| `view`    | `repo`, `pr_id`                              | —                                       |
| `create`  | `repo`, `branch`, `title`                    | `target_branch`, `description`          |
| `merge`   | `repo`, `pr_id`                              | `force`                                 |
| `close`   | `repo`, `pr_id`                              | —                                       |
| `comment` | `repo`, `pr_id`, `comment`                   | —                                       |

---

## Examples

### 1. List all open PRs
**Input:**
```json
{
  "action": "list",
  "repo": "owner/repo"
}
```
**Output:**
List of open PRs with their IDs, titles, and authors.

---

### 2. Create a new PR
**Input:**
```json
{
  "action": "create",
  "repo": "owner/repo",
  "branch": "feature/new-feature",
  "target_branch": "main",
  "title": "Add new feature",
  "description": "This PR introduces a new feature."
}
```
**Output:**
Confirmation of PR creation with PR ID.

---

### 3. Merge a PR
**Input:**
```json
{
  "action": "merge",
  "repo": "owner/repo",
  "pr_id": "123",
  "force": false
}
```
**Output:**
Confirmation of merge or error if PR cannot be merged.

---

### 4. Add a comment to a PR
**Input:**
```json
{
  "action": "comment",
  "repo": "owner/repo",
  "pr_id": "123",
  "comment": "Please review the changes."
}
```
**Output:**
Confirmation of comment added.

---

## Error Handling
- If `forgejo-cli` is not found:
  > `"Error: forgejo-cli is required but not installed. Install it from [forgejo-cli wiki](https://codeberg.org/forgejo-contrib/forgejo-cli/wiki/PRs)."`
- If the repository or PR ID is invalid:
  > `"Error: Invalid repository or PR ID."`
- For CLI errors:
  > Return the raw error message from `forgejo-cli`.

---
## References
- [Forgejo CLI PRs Wiki](https://codeberg.org/forgejo-contrib/forgejo-cli/wiki/PRs)
- [Agent Skills Specification](https://agentskills.io/specification)
