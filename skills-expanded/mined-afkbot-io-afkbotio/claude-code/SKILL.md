---
name: claude-code
description: "Anthropic Claude Code orchestration through `bash.exec`. Use when the user explicitly wants to run Claude Code from shell, install or authenticate the `claude` CLI, choose model aliases such as `sonnet` or `opus`, or execute non-interactive `claude -p` workflows."
triggers:
  - claude code
  - anthropic claude code
  - claude -p
  - через claude code
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
  - claude
execution_mode: executable
---

# claude-code

Use this skill when AFKBOT should drive the external Anthropic Claude Code CLI through `bash.exec`.

## Default mode

- Prefer non-interactive mode for AFKBOT automation:
  - `claude -p "<prompt>"`
- Use interactive `claude` only if the user explicitly wants a live coding session, browser login, or in-session commands like `/model`.
- Run from the repo root that Claude should inspect.

## What to pass

Build each `bash.exec` command from these inputs:
1. target workspace:
   - use the correct `cwd`
2. prompt:
   - `-p "<prompt>"`
3. model:
   - `--model <alias|name>`
4. reasoning effort when needed:
   - `--effort low|medium|high|max`

## Common commands

```bash
claude --version
claude doctor
claude --model sonnet -p "Review the staged diff for correctness"
claude --model opus --effort high -p "Design a refactor plan for this service"
```

## Installation

Claude Code currently documents these supported installation paths:

```bash
curl -fsSL https://claude.ai/install.sh | bash
brew install --cask claude-code
winget install Anthropic.ClaudeCode
```

- Anthropic documents native install as the recommended path.
- The docs also note that the old npm installation path is deprecated.

## Authentication

Claude Code supports:

- browser login via `claude` for Pro, Max, Teams, Enterprise, or Console accounts;
- `ANTHROPIC_API_KEY` for direct API access;
- `ANTHROPIC_AUTH_TOKEN` for bearer-token gateway/proxy flows;
- cloud-provider credentials for Bedrock, Vertex AI, or Foundry.

Useful environment variables:

```bash
export ANTHROPIC_API_KEY="..."
export ANTHROPIC_AUTH_TOKEN="..."
export ANTHROPIC_MODEL="sonnet"
```

If AFKBOT must help with secrets:
- inspect existing global credentials first;
- request missing secrets securely with `credentials.request`;
- never print tokens in chat or logs.

## Models

Claude Code supports model aliases and full model names. Current documented aliases include:

- `default`
- `sonnet`
- `opus`
- `haiku`
- `sonnet[1m]`
- `opus[1m]`
- `opusplan`

Current documented behavior:
- `default` resolves by account tier;
- Max and Team Premium default to Opus 4.6;
- Pro and Team Standard default to Sonnet 4.6.

You can switch models with:

```bash
claude --model sonnet
```

or interactively with `/model`.

## Post-run flow

After Claude Code finishes:
- inspect resulting files with `file.list`, `file.read`, or `file.search`;
- render a diff with `diffs.render` if the user asked what changed;
- report the exact command, model alias or name, effort level, and affected files.

## Rules

- Prefer `claude -p` for AFKBOT automation.
- Use explicit skill invoke forms such as `/claude-code` or `$claude-code` when the user wants this shell workflow deterministically.
- Use interactive `claude` only when the user explicitly wants a live session.
- If the user asks which Claude model is current, verify the exact current alias/version before answering.
