# Ollama Local API Skill

Use this skill when an agent or user needs to call Ollama Local API through Provider API CLI Suite.

## When to use

- local/offline model calls
- privacy-sensitive testing
- no cloud API key local workflows

## Required CLI

```bash
ollama-api doctor --json
```

## Basic dry run

```bash
ollama-api chat "hello" --dry-run --json
```

## Agent-safe rules

- Prefer `--json` for automation.
- Use `--dry-run` before live calls.
- Parse stdout only. Treat stderr as diagnostics.
- Do not expose API keys in prompts, logs, or screenshots.
- Do not execute tool calls inside the CLI; pass tool execution to the Harness or caller.

## Protocol

`ollama_chat`


