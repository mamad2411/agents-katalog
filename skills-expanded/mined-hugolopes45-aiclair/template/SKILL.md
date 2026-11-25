---
name: <hook-name>
description: <What this skill does. Keep under 1024 chars.>
---

# <Hook Name> Skill

## When Invoked

Hook has determined the prompt is vague. Proceed to research and clarification.

## Core Workflow

### Phase 1: Research

Check conversation history first. If sufficient context exists, skip codebase exploration.

If more context needed:
1. [Your research steps here]
2. Document findings

### Phase 2: Generate Questions

Based on research, ask 1-6 targeted questions using `AskUserQuestion`.

### Phase 3: Clarify

Use `AskUserQuestion` tool with:
- `question`: clear, specific, ends with `?`
- `header`: max 12 chars
- `multiSelect`: false unless choices are non-exclusive
- `options`: 2-4 concrete choices from research

### Phase 4: Execute

Proceed with original intent using answers and research.
