---
name: use-reddit
description: Use the Reddit JoAi app plugin when the task needs Reddit tools or workflows.
---

# Reddit

Connect Reddit to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Reddit tools available in this app.
- Explain what setup or authentication Reddit needs before I run an action.
- Use Reddit to help me with the task I describe next.

## Action Inventory

- `reddit-create-comment` (collect) — Create a comment on a Reddit post or reply to another comment.
- `reddit-create-post` (collect) — Create a new post in a Reddit subreddit. Supports both text posts and link posts.
- `reddit-get-comments` (collect) — Retrieve comments for a specific Reddit post. Supports different sorting options (best, top, new, controversial, old, qa) and depth limits.
- `reddit-get-post-details` (collect) — Retrieve detailed information about a specific Reddit post including its content, score, comments count, and metadata.
- `reddit-get-posts` (collect) — Retrieve posts from a Reddit subreddit. Supports different sorting options (hot, new, top, rising) and pagination.
- `reddit-get-user-info` (collect) — Retrieve information about a Reddit user including their karma, account age, and profile details.
- `reddit-search` (collect) — Search Reddit for posts matching a query. Can search all of Reddit or within a specific subreddit.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
