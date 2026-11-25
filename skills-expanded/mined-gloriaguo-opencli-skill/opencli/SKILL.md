---
name: opencli
description: Use when an AI agent needs to install, inspect, troubleshoot, or operate a local OpenCLI setup, or when a task involves websites, Electron desktop apps, browser-login reuse, downloads, plugins, external CLI passthrough, or adapter generation through OpenCLI.
---

# OpenCLI

OpenCLI turns websites, Electron apps, and existing local CLIs into structured terminal commands. Prefer it when deterministic CLI output is more useful than ad-hoc browser automation.

## Trigger Cues

Load this skill when the task sounds like any of these:

- "use opencli"
- "pull data from Bilibili/Zhihu/Xiaohongshu/Weixin/Boss"
- "reuse my Chrome login"
- "control Cursor/Codex/Notion/ChatGPT from the terminal"
- "download article/video/media through OpenCLI"
- "inspect what OpenCLI supports on this machine"
- "create or troubleshoot an OpenCLI adapter"

## Reference Files

| Reference | Use for |
| --- | --- |
| [references/agent-playbook.md](references/agent-playbook.md) | Agent-first trigger patterns, action order, and safe defaults |
| [references/commands.md](references/commands.md) | Common commands, category selection, and example invocations |
| [references/china-workflows.md](references/china-workflows.md) | China-focused site templates and desktop-agent workflows |
| [references/practical-scenarios.md](references/practical-scenarios.md) | Detailed field manual for choosing OpenCLI and executing end-to-end workflows |
| [references/troubleshooting.md](references/troubleshooting.md) | Failure signatures, browser bridge issues, auth problems, and fixes |

## Core Workflow

1. Confirm the binary exists. If `opencli` is missing, install it with `npm install -g @jackwener/opencli`.
2. Discover before guessing. Run `opencli list -f yaml` to inspect available adapters and commands.
3. Choose the command class:
   - Public commands: run directly. No browser login is required.
   - Browser commands: ensure Chrome is open and already logged in to the target site, then run `opencli doctor` if this is the first browser-backed task or if anything looks broken.
   - Desktop adapters: make sure the target app is running, inspect the registered commands first, then start with `read`, `history`, `model`, `send`, `ask`, or adapter-specific commands.
   - External CLI passthrough: use `opencli <tool> ...` and keep the original arguments intact.
   - New site development: use `explore`, `synthesize`, `generate`, and `cascade`.
4. Prefer `-f json` for agent-readable output. Use `-f yaml` for human inspection, `-f table` for terminal browsing, and `-v` only when debugging.
5. If a browser-backed command returns empty data or authorization errors, verify the Chrome login state before changing commands or code.
6. Before any write-like action such as `post`, `reply`, `send`, `publish`, `greet`, or `follow`, do at least one read-only command first unless the user explicitly asks to skip that safety step.

## Decision Guide

### Public data

Use this path for sources such as `hackernews`, `wikipedia`, `google`, `arxiv`, or similar read-only commands. These are the cheapest and most reliable because they do not depend on Chrome state.

### Browser-backed sites

Use this path for adapters such as `bilibili`, `zhihu`, `xiaohongshu`, `twitter`, `reddit`, `pixiv`, `weixin`, `boss`, or other commands that reuse Chrome login. Keep Chrome running, keep the account logged in, and use `opencli doctor` before deeper debugging.

### Desktop adapters

Use this path for apps such as `cursor`, `codex`, `chatgpt`, `notion`, `discord-app`, or `doubao-app`. Do not assume a command exists just because another adapter or README example has it; inspect the registry first with `opencli list -f yaml` or adapter help.

### External CLI hub

Use this path when the user really wants the underlying CLI but wants discovery, installation help, or a unified entrypoint. Examples include `opencli gh ...`, `opencli docker ...`, `opencli obsidian ...`, and `opencli gws ...`.

### Adapter generation

Use `opencli explore <url> --site <name>` to inspect a site, `opencli synthesize <site>` to build an adapter, `opencli generate <url> --goal "<goal>"` for the fast path, and `opencli cascade <url>` to probe authentication strategy.

## Operating Rules

- Use explicit limits like `--limit 5` for exploratory reads.
- Prefer structured output over prose whenever another tool or agent will consume the result.
- For media downloads, install `yt-dlp` when the adapter requires it.
- When a command is likely browser-backed, assume login state matters until proven otherwise.
- For desktop adapters, check `--help` before assuming command parity across apps or versions.
- Treat `opencli list -f yaml` as the source of truth when the README and installed commands disagree.
- Read [references/troubleshooting.md](references/troubleshooting.md) before concluding that an adapter is broken.
