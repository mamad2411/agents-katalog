---
name: cc-config
description: Use when working with Claude Code CLI, plugins, hooks, MCP servers, skills, configuration, or any Claude Code feature - routes to the official documentation instead of guessing, and can cache it locally for offline use
---

# Working with Claude Code

## Overview

Claude Code's own documentation is the authority on configuration paths, manifest
schemas, hook events and CLI flags. This skill's job is to send you there rather
than let you guess — and, when you want it offline, to fetch it.

**It ships no documentation of its own.** The upstream version of this skill
committed a 42-file mirror of `docs.claude.com/en/docs/claude-code/*`. That copy
was dropped on import: it was nine months stale, it omitted eight plugin manifest
keys that this monorepo's own `packages/mint/schemas/claude-code-plugin-manifest.json`
already validates, and a skill whose pitch is "authoritative, stop guessing" that
is behind the repo's own schema launders a wrong answer as an official one.

## When to Use

- Creating or configuring Claude Code plugins
- Setting up MCP servers
- Working with hooks (SessionStart, Stop, PostToolUse, …)
- Writing or testing skills
- Configuring Claude Code settings
- Troubleshooting Claude Code issues
- Understanding CLI commands
- Setting up integrations (VS Code, JetBrains, …)
- Configuring networking, security, or enterprise features

## How to Get an Answer

**Default: fetch the one page you need.** Every topic is a single markdown file
under one predictable URL:

```
https://docs.claude.com/en/docs/claude-code/<topic>.md
```

Use {web-fetch} on that URL. One page, current, no cache to go stale.

| Question | Topic |
|---|---|
| Create a plugin | `plugins`, then `plugins-reference` |
| Plugin marketplaces | `plugin-marketplaces` |
| Set up an MCP server | `mcp` |
| Configure hooks | `hooks`, then `hooks-guide` |
| Write a skill | `skills` |
| Slash commands | `slash-commands` |
| Subagents | `sub-agents` |
| CLI flags | `cli-reference` |
| Headless / scripting | `headless` |
| Settings reference | `settings` |
| Memory and context | `memory` |
| Costs and usage | `costs`, `monitoring-usage` |
| Troubleshoot | `troubleshooting` |
| Install and set up | `setup`, `quickstart` |

`https://docs.claude.com/llms.txt` lists every page if the topic you want is not
in the table.

## Working Offline

When you have no network, or you want to search across the whole corpus with
{search}, populate a local cache first:

Resolve {resource:skills/cc-config/scripts/update_docs.mjs}
relative to this loaded document, then invoke it with `node`.

It reads `llms.txt`, extracts every `claude-code/*.md` URL, and writes each page
into the sibling `references/` directory beside the resolved script's parent
directory. Then use {read} or {search} on that directory as usual.

Two things to know about the cache:

- **It is not committed.** A fresh checkout has no `references/` directory at
  all, and this skill's answers do not depend on one existing.
- **It goes stale silently.** Nothing dates it and nothing warns you. If a cached
  page disagrees with a fetched one, the fetched one wins — re-run the script
  rather than reasoning from the cache.

## What This Skill Does NOT Do

- It provides **documentation access**, not procedural guidance. For how to
  *build* a plugin — the workflow, the manifest, the release path in this
  repo — use the `cc-plugins` skill.
- It is a **reference router**, not a tutorial.

## Red Flags

If you find yourself:

- Guessing where a config file lives → fetch `settings`
- Speculating about a manifest key → fetch `plugins-reference`
- Unsure which hook event fires when → fetch `hooks`
- Assuming a feature exists → check the docs first

**Consult the documentation before guessing. Do not answer from a stale cache
when the network is available.**
