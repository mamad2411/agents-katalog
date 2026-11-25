---
name: use-github
description: Use the GitHub JoAi app plugin when the task needs GitHub tools or workflows.
---

# GitHub

Connect GitHub to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the GitHub tools available in this app.
- Explain what setup or authentication GitHub needs before I run an action.
- Use GitHub to help me with the task I describe next.

## Action Inventory

- `github-add-comment` (collect) — Add a comment to a GitHub issue or pull request. Supports Markdown formatting.
- `github-create-issue` (collect) — Create a new issue in a GitHub repository. Supports title, body, labels, and assignees.
- `github-create-pull-request` (collect) — Create a new pull request in a GitHub repository. Merge changes from one branch into another.
- `github-get-issue` (collect) — Retrieve detailed information about a specific GitHub issue including comments, labels, and assignees.
- `github-get-repository` (collect) — Retrieve information about a GitHub repository including description, stars, forks, and language.
- `github-list-issues` (collect) — List issues in a GitHub repository. Supports filtering by state (open, closed, all), labels, and assignee.
- `github-search-repositories` (collect) — Search for GitHub repositories using GitHub's search API. Supports filtering by language, stars, forks, and more.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
