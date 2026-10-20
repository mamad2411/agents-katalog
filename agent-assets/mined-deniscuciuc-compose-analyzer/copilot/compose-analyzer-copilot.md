# GitHub Copilot Instructions — Compose Analyzer

You are operating inside the **Compose Analyzer** repository. This file is your authoritative guide: follow it before searching the codebase.

## What this tool does

A CLI that analyzes Docker Compose files and emits **JSON to stdout** (with `-j`) or **Markdown reports** to `./reports/`. Use it to inspect image pinning, secret exposure, privileged containers, restart policy gaps, missing resource limits, and weak network isolation.

## Prerequisites checklist

Before running any command, verify:

1. `node_modules/` exists. If missing, run `pnpm install`.
2. A Compose file exists at the path you plan to analyze.
3. If `--with-docker` is used, the Docker daemon must be reachable.

## Standard workflow

Always start with the health check, then drill down only if the score is below 90.

```bash
# 1. Health check
pnpm analyze:health -- --file docker-compose.yml

# 2. If healthScore < 90, drill into specifics
pnpm analyze:images -- --file docker-compose.yml
pnpm analyze:security -- --file docker-compose.yml
pnpm analyze:reliability -- --file docker-compose.yml
pnpm analyze:resources -- --file docker-compose.yml
pnpm analyze:networks -- --file docker-compose.yml
```

## Operational rules for the agent

- **Always reply in English.**
- **Use `-j` for parsing.** Markdown output is for humans only.
- **Do not invent compose content.** Read the actual file being analyzed.
- `--with-docker` is optional enrichment and must not become a hard dependency for core analysis.

## File layout

```text
index.ts                              # CLI entry, bootstrap only
src/cli/{options,runner}.ts           # CLI parsing and command execution
src/config/loader.ts                  # Config loading for non-connection settings
src/constants.ts                      # Commands, defaults, issue severity rules
src/collectors/*.ts                   # Compose file and optional Docker runtime collection
src/analyzers/*.ts                    # Image, security, reliability, resource, network analysis
src/reporters/*.ts                    # Markdown, HTML, and diff output
src/interactive/{index,display,menus}.ts
```
