---
name: use-laravel-cloud
description: Use the Laravel Cloud JoAi app plugin when the task needs Laravel Cloud tools or workflows.
---

# Laravel Cloud

Connect Laravel Cloud to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Laravel Cloud tools available in this app.
- Explain what setup or authentication Laravel Cloud needs before I run an action.
- Use Laravel Cloud to help me with the task I describe next.

## Action Inventory

- `laravel-cloud-get-command` (collect) — Retrieve the status and details of a specific CLI command.
- `laravel-cloud-initiate-deployment` (collect) — Start a new deployment for a specific environment from a branch or commit.
- `laravel-cloud-list-applications` (collect) — List all applications in your Laravel Cloud account. Applications are the top-level containers for your code and resources.
- `laravel-cloud-list-deployments` (collect) — List all deployments for a specific environment. Deployments represent the process of shipping code.
- `laravel-cloud-list-environment-logs` (collect) — Retrieve the latest logs for a specific environment. Useful for debugging and monitoring commands.
- `laravel-cloud-list-environments` (collect) — List all environments (e.g., production, staging) for a specific application.
- `laravel-cloud-run-command` (collect) — Execute a CLI command (e.g., Artisan) on a specific environment.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
