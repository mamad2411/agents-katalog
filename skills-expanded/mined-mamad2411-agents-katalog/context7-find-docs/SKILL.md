---
name: context7-find-docs
description: Fetch current library, framework, SDK, CLI, and cloud-service documentation through Context7. Use when the user asks about current API syntax, configuration, migration, setup, or library-specific debugging.
---

# context7-find-docs

## Purpose

Use Context7 for current technical documentation before answering version-sensitive library or framework questions.

## Workflow

1. Identify the exact library, framework, CLI, SDK, or cloud service.
2. Build a focused query from the user's task; exclude private project values.
3. Resolve the library ID through the Context7 CLI.
4. Query docs with the resolved ID and the focused question.
5. Cite the command result in your answer or state why Context7 was unavailable.

## Required Checks

- Do not use training memory for unstable API details when Context7 is available.
- Do not send private project snippets, keys, account data, or customer data to an external docs lookup.
- Use at most three lookup attempts per question before falling back with a clear limitation.
- If Context7 is not installed or unavailable, say so and use official docs or local project sources as fallback.

## Output

Give the resolved library, the relevant current guidance, and any version or limitation that affects the answer.
