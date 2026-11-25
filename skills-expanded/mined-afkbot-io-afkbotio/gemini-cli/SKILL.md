---
name: gemini-cli
description: "Google Gemini CLI orchestration through `bash.exec`. Use when the user explicitly wants to run Gemini from shell, install or authenticate the `gemini` CLI, choose a Gemini model, or execute one-shot `gemini -p` workflows against a repo or prompt."
triggers:
  - gemini cli
  - google gemini cli
  - gemini -p
  - через gemini cli
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
  - gemini
execution_mode: executable
---

# gemini-cli

Use this skill when AFKBOT should drive the external Google Gemini CLI through `bash.exec`.

## Default mode

- Prefer one-shot shell usage for AFKBOT:
  - `gemini -p "<prompt>"`
  - `gemini -p "<prompt>" --output-format json`
  - `gemini -p "<prompt>" --output-format stream-json`
- Use interactive `gemini` only if the user explicitly wants a live terminal session or browser sign-in flow.

## What to pass

Build each `bash.exec` command from these inputs:
1. target workspace:
   - `cwd` in the tool call
   - optional `--include-directories <dir1,dir2>` for multi-root work
2. prompt:
   - `-p "<prompt>"`
3. model:
   - `-m <model>`
4. output shape:
   - default plain text for human-readable answers
   - `--output-format json` for structured automation
   - `--output-format stream-json` for long-running streamed events

## Common commands

```bash
gemini --version
gemini -p "Summarize this repository"
gemini -p "Explain the current test failures" --output-format json
gemini -m gemini-2.5-flash -p "Draft a migration plan"
gemini --include-directories ../src,../lib -p "Compare these directories"
```

## Installation

Gemini CLI supports several installation paths:

```bash
npx @google/gemini-cli
npm install -g @google/gemini-cli
brew install gemini-cli
sudo port install gemini-cli
```

- In restricted environments, the official docs also describe installing Node in Conda first and then installing the package with npm.

## Authentication

Gemini CLI supports three main auth paths:

- Google sign-in / Code Assist: run `gemini` and complete the browser login.
- Gemini API key: export `GEMINI_API_KEY`.
- Vertex AI: export `GOOGLE_API_KEY` and `GOOGLE_GENAI_USE_VERTEXAI=true`.

Useful environment examples:

```bash
export GEMINI_API_KEY="..."
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_API_KEY="..."
export GOOGLE_GENAI_USE_VERTEXAI=true
```

If AFKBOT must help collect a secret:
- check `credentials.list` first under global credentials;
- request the missing value with `credentials.request`;
- never print API keys in chat or shell output.

## Models

Pass models with `-m <model>`. Common current choices from Google Gemini docs:

- `gemini-3-pro-preview`
- `gemini-3-flash-preview`
- `gemini-2.5-pro`
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`

Model availability depends on the auth backend, release channel, and CLI version.

## Post-run flow

After Gemini CLI finishes:
- inspect changed or generated files with `file.list`, `file.read`, or `file.search`;
- use `diffs.render` if the user wants a compact change summary;
- report the exact command, model, output mode, and affected files.

## Rules

- Prefer `-p` over interactive REPL mode when AFKBOT is automating the run.
- Use explicit skill invoke forms such as `/gemini-cli` or `$gemini-cli` when the user wants this shell workflow deterministically.
- Use `--output-format json` when downstream parsing matters.
- If the user asks for the latest Gemini model, verify the exact current model name first.
