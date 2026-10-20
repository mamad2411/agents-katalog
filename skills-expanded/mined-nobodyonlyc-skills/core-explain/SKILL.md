---
name: core-explain
description: Explain a specific file, class, function, or block of code in depth, including design patterns and potential gotchas.
---

Code to explain: $ARGUMENTS

> Scope: this skill explains **one known** file/function/block. To understand a **large or unfamiliar codebase** without running out of context, use [core-explore](../core-explore/SKILL.md) (map-first + fan-out summaries) instead.

If $ARGUMENTS is a file path, read it. If it's a function or concept name, search for it:

```bash
[ -f "$ARGUMENTS" ] && cat -n "$ARGUMENTS" || grep -rn "$ARGUMENTS" --include="*.{js,ts,py,go,rs,java}" -l | head -5
```

Explain the code at two levels:

## What it does
Plain-language description of the behavior and purpose. No code jargon — explain as if the reader is new to this part of the codebase.

## How it works
Walk through the key logic step by step:
- Entry point and inputs
- Core algorithm or data flow
- Edge cases handled (and any not handled)
- Output and side effects

## Context
- Why this code exists (if inferrable from names, comments, or surrounding code)
- What calls it / what it calls
- Known gotchas or non-obvious behaviors

Keep it concise. Skip explaining obvious language constructs. Focus on what would take a developer time to figure out by reading alone.
