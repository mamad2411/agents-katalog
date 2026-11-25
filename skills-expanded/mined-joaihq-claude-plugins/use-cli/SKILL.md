---
name: use-cli
description: Use the CLI JoAi app plugin when the task needs CLI tools or workflows.
---

# CLI

Connect CLI to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the CLI tools available in this app.
- Explain what setup or authentication CLI needs before I run an action.
- Use CLI to help me with the task I describe next.

## Action Inventory

- `cli-clipboard-copy` (prompt) — Copy text content to the system clipboard.
- `cli-clipboard-read` (prompt) — Read and display the current contents of the system clipboard.
- `cli-compress` (prompt) — Compress files or directories into a ZIP archive.
- `cli-copy-file` (prompt) — Copy a file or directory to a new location.
- `cli-create-folder` (prompt) — Create a new folder, including any parent directories.
- `cli-current-directory` (prompt) — Show the current working directory.
- `cli-decompress` (prompt) — Extract files from a ZIP archive.
- `cli-delete-file` (prompt) — Delete a file or directory permanently.
- `cli-disk-usage` (prompt) — Show available and used disk space on the system.
- `cli-download-file` (prompt) — Download a file from a URL and save it locally.
- `cli-execute` (prompt) — Run a command on the desktop.
- `cli-find-files` (prompt) — Search for files matching a name pattern in a directory.
- ...and 13 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
