---
name: super-review
description: Explicit Super Review of Go, TypeScript, Rust or Java PRs and local source for readability and maintainability.
disable-model-invocation: true
---

Run Super Review in this Cursor Agent chat, preserving the user's selected model
and the original request, including any ordinary-language subagent model choice.
Follow the [core skill](../../resources/super-review/SKILL.md) using only the
[Cursor adapter](../../resources/super-review/references/harnesses/cursor.md).
Resolve these links relative to this installed SKILL.md, not the working directory;
pass resolved resource paths to specialists. Do not start a separate orchestrator.
Help only explains usage. For a review, resolve the specialist selection before
native delegation; model routing is not accomplished by text in a child prompt.
