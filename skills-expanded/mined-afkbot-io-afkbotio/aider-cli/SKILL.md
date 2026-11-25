---
name: aider-cli
description: "Aider CLI orchestration through `bash.exec`. Use when the user explicitly wants to run aider from shell, install aider, choose provider-specific models, or execute one-shot `aider --message` edits against selected files or a repo."
triggers:
  - aider cli
  - aider --message
  - через aider cli
tool_names:
  - credentials.list
  - credentials.request
  - bash.exec
  - file.list
  - file.read
  - file.search
  - diffs.render
preferred_tool_order:
  - credentials.list
  - credentials.request
  - bash.exec
  - file.list
  - file.read
  - file.search
  - diffs.render
requires_bins:
  - aider
execution_mode: executable
---

# aider-cli

Use this skill when AFKBOT should drive the external `aider` CLI through `bash.exec`.

## Default mode

- Prefer one-shot automation:
  - `aider --message "<prompt>" <files...>`
  - `aider --message-file <file> <files...>`
- Run aider from the target git repository.
- Default to `--no-auto-commits` unless the user explicitly asked aider to commit.
- Use `--dry-run` when the user asked only for a preview or planning run.

## What to pass

Build each `bash.exec` command from these inputs:
1. model:
   - `--model <provider/model-or-alias>`
2. authentication:
   - provider env vars or `--api-key provider=value`
3. task:
   - `--message "<prompt>"` or `--message-file <path>`
4. scope:
   - explicit file paths at the end of the command
5. safety controls:
   - `--no-auto-commits`
   - `--dry-run`
   - `--yes` only when the user clearly approved unattended execution

## Common commands

```bash
aider --version
aider --model o3-mini --api-key openai="$OPENAI_API_KEY" --no-auto-commits --message "Refactor this parser" src/parser.py
aider --model sonnet --api-key anthropic="$ANTHROPIC_API_KEY" --dry-run --message "Review this module and propose fixes" src/service.py
aider --model openrouter/anthropic/claude-3.7-sonnet --api-key openrouter="$OPENROUTER_API_KEY" --message-file prompt.txt src/
```

## Installation

Official aider docs describe several supported installation paths:

```bash
curl -LsSf https://aider.chat/install.sh | sh
uv tool install --force --python python3.12 --with pip aider-chat@latest
pipx install aider-chat
```

- For AFKBOT-managed environments, use the uv-based installer path.

## Authentication

Aider is provider-agnostic. It can use:

- provider environment variables;
- `--api-key provider=value`;
- OpenRouter if no direct provider key is configured.

Examples from official docs:

```bash
aider --model deepseek --api-key deepseek=...
aider --model sonnet --api-key anthropic=...
aider --model o3-mini --api-key openai=...
aider --model openrouter/deepseek/deepseek-chat --api-key openrouter=...
```

If AFKBOT needs to collect a secret:
- check global credentials first;
- request the missing value securely with `credentials.request`;
- never echo keys in the shell transcript.

## Models

Aider model names are provider-dependent. Common documented examples include:

- `deepseek`
- `sonnet`
- `o3-mini`
- `openrouter/anthropic/claude-3.7-sonnet`
- `openrouter/deepseek/deepseek-chat`

If no model is specified, aider tries to select one from the keys you already configured.

## Post-run flow

After aider completes:
- inspect edited files with `file.list`, `file.read`, or `file.search`;
- render a diff with `diffs.render` if the user wants a concise change summary;
- explicitly mention whether `--dry-run` or `--no-auto-commits` was used.

## Rules

- Do not let aider auto-commit unless the user explicitly asked for commits.
- Use explicit skill invoke forms such as `/aider-cli` or `$aider-cli` when the user wants this shell workflow deterministically.
- Prefer targeted file lists over pointing aider at the whole repo when the request is narrow.
- If the user asks for a provider/model combination that may have changed recently, verify the exact model name first.
