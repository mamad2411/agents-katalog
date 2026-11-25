---
name: docs-change
description: Use for README, Markdown, and human-facing documentation edits so docs stay concise, audience-appropriate, and scoped to the request.
---

# Docs Change

## Core rule

Preserve the document's purpose, audience, tone, and level of detail.

A README is the project's front door:
- explain what the project is
- help a reader understand what it does
- provide only the setup information needed to get started
- link or defer to deeper technical material when needed

Do not turn concise human-facing docs into architecture manuals, changelogs, or exhaustive implementation references unless explicitly requested.

## Editing rules

- Make only the requested documentation change.
- Keep nearby wording consistent, but do not broaden scope.
- Prefer concise useful wording over exhaustive technical detail.
- Do not add new sections, large rewrites, or speculative content unless the issue explicitly asks for them.
- Verify factual claims against the relevant source file when needed.

## Verification

For docs-only work, prefer lightweight verification:
- inspect the diff for only the intended files
- confirm no unrelated files changed
- run heavier checks only if the issue or changed files justify them
