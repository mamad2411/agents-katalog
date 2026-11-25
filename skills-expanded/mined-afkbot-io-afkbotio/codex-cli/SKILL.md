---
name: codex-cli
description: "OpenAI Codex CLI orchestration through `bash.exec`. Use when the user explicitly wants to run Codex from shell, install or authenticate Codex CLI, choose a Codex/OpenAI model, or execute one-shot `codex exec` or `codex review` workflows against a repo."
triggers:
  - codex cli
  - openai codex cli
  - codex exec
  - codex review
  - через codex cli
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
  - codex
execution_mode: executable
---

# codex-cli

Use this skill when AFKBOT should drive the external OpenAI Codex CLI through `bash.exec`.

## Default mode

- Prefer non-interactive commands:
  - `codex exec` for one-shot task execution
  - `codex review` for review-only flows
- Use plain `codex` only if the user explicitly wants an interactive TUI or login flow.
- Launch from the target repo root, or pass `-C <dir>` explicitly.

## What to pass

Build each `bash.exec` command from these inputs:
1. target workspace:
   - `cwd` in the tool call
   - optional `-C <dir>` if Codex should operate from a different root
2. task prompt:
   - one quoted prompt argument for short tasks
   - stdin piping for long prompts
3. model:
   - `-m <model>` when the user requested one
4. execution controls:
   - `-s read-only|workspace-write|danger-full-access`
   - `--full-auto` for sandboxed low-friction execution
   - `--json` when AFKBOT needs structured events
   - `-o <file>` or `--output-schema <file>` for machine-readable final output

## Common commands

```bash
codex --version
codex login status
codex exec -C . -m gpt-5.3-codex --json "Fix the failing tests and explain the root cause"
codex review -C .
printf '%s\n' "Summarize the architecture of this repo" | codex exec -
```

## Installation

Codex CLI can be installed in several supported ways:

```bash
npm install -g @openai/codex
brew install --cask codex
```

- GitHub Releases also publish standalone binaries for macOS and Linux.

## Authentication

- Preferred for human use: `codex` or `codex login`, then sign in with ChatGPT.
- For automation: `printenv OPENAI_API_KEY | codex login --with-api-key`
- Use `codex login status` before assuming credentials are valid.

If an API key must be provided inside AFKBOT:
- check `credentials.list` first under global credentials;
- request the secret with `credentials.request` if missing;
- never print the key in chat or command output.

## Models

Pass models with `-m <model>`. Common current choices from OpenAI model docs:

- `gpt-5.3-codex`
- `gpt-5.2-codex`
- `gpt-5-codex`
- `gpt-5.1-codex`
- `gpt-5.1-codex-max`
- `gpt-5.1-codex-mini`
- `codex-mini-latest`
- `gpt-5.4` for general complex reasoning and coding

Exact availability depends on the account, provider, and local Codex configuration.

## Post-run flow

After a successful Codex run:
- inspect changed files with `file.list`, `file.read`, or `file.search`;
- render a diff with `diffs.render` if the user asked what changed;
- report the exact repo path, command, model, and affected files.

## Rules

- Prefer `codex exec` or `codex review` over interactive TUI mode.
- Use explicit skill invoke forms such as `/codex-cli` or `$codex-cli` when the user wants this shell workflow deterministically.
- Do not use `--dangerously-bypass-approvals-and-sandbox` unless the user explicitly asked for unsafe execution.
- Do not assume a model name from memory if the user asked for a specific latest model; verify it first.
