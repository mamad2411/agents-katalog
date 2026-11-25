---
name: docs-claude
description: >-
  Use when the user says "Claude Code docs", "hooks docs", "what's new", or asks
  how to configure Claude Code features (hooks, settings, MCP, slash
  commands).
---

# Claude Code Docs Helper

## Overview

Use the local helper script to read the Claude Code docs mirror and return official doc links and summaries.

## Workflow

1. Determine intent: index, topic lookup, freshness check (`-t`), or "what's new".
2. Build the argument string from the user request and run:
   `~/.claude-code-docs/claude-docs-helper.sh "<args>"`
3. Return:
   - Private mirror URL (GitHub)
   - Official docs URL
   - Relevant summary or extracted content
   - Official page link for the topic
4. If "what's new", include recent updates and a changelog link.

## Fallbacks

- If the helper script is missing or fails, explain how to install `~/.claude-code-docs` and ask how to proceed.
