---
name: gist-management
description: Create, read, update, and manage GitHub Gists via MCP. Use when asked to save, share, or manage code snippets as gists.
---

# GitHub Gist Management via MCP

Use this skill when you need to create, read, update, or manage GitHub Gists. Fills the gap the official GitHub MCP server leaves for Gists.

## Available Tools

| Tool           | What it does                              |
| -------------- | ----------------------------------------- |
| `gist_list`    | List your gists (paginated)               |
| `gist_get`     | Get a gist by ID (includes file contents) |
| `gist_create`  | Create a new gist (public or secret)      |
| `gist_update`  | Update description or file contents       |
| `gist_delete`  | Delete a gist                             |
| `gist_starred` | List your starred gists                   |
| `gist_star`    | Star a gist                               |
| `gist_unstar`  | Unstar a gist                             |

## Workflow

1. `gist_create` to save code snippets — specify `public: false` for secret gists (default)
2. `gist_list` to browse existing gists
3. `gist_get` with a gist ID to read file contents
4. `gist_update` to modify description or files

## Key Patterns

- Gists are secret by default — pass `public: true` for publicly discoverable gists
- `gist_create` accepts multiple files — useful for multi-file snippets
- `gist_get` returns full file contents — use it to read existing gist code
- Requires `GITHUB_TOKEN` with the `gist` scope

## Safety

- Confirm before `gist_delete` — deletions are permanent
- Secret gists are accessible by URL but not searchable — they're not truly private
