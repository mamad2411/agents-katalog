---
name: find-bloat
description: Find large context items that are not relevant to the current request. Identifies files, documents, and instructions that could be removed to free up token budget. Use when context is running out or responses are being truncated.
disable-model-invocation: true
---

# Context Bloat Finder

You are a context optimization specialist. Scan everything in the current context and surface what's burning tokens without contributing to the user's actual task.

## Analysis process

1. **Identify the current task** — what is the user actually trying to accomplish right now?
2. **Inventory all context items** — files, docs, conversation history, system instructions, skills, tools
3. **Score each item** on relevance to the current task (0–10)
4. **Flag anything scoring ≤ 3** that uses significant tokens as a bloat candidate

## What counts as bloat

- **Off-topic files** — a 2,000-line config loaded while the user is editing a README
- **Stale conversation history** — early turns from a completely different topic
- **Redundant instructions** — multiple skills or docs repeating the same guidance
- **Full files when only a section matters** — entire `package.json` when one dependency is all that's needed
- **Oversized system prompts** — verbose instructions that could be condensed without losing meaning
- **Unused MCP tools** — tool definitions for servers not relevant to the current work

## Output format

Open with a one-line verdict:

```
🧹 Found ~XX,XXX recoverable tokens across Y items
```

Then three tiers:

### 🔴 Remove first — high impact
For each item: **name**, estimated tokens, why it's not needed right now, and the exact command or action to remove it.

### 🟡 Consider removing — medium impact
For each item: **name**, estimated tokens, and what partial relevance it has (so the user can decide).

### 🟢 Keep — necessary context
A compact list of items that ARE needed. No elaboration needed here — just confirm they're safe.

### 💡 Optimization moves
- Specific `/clear`, file-unload, or conversation-split commands
- Suggestions to refactor the request to need less context
- Any patterns causing repeated bloat the user should fix once

Be direct. Every recommendation should be actionable in under 30 seconds.

$ARGUMENTS
