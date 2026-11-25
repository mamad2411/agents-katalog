---
name: publish
description: GBrain-inspired publishing workflow for Codex. Use when a memo, report, or saved artifact should become a clean shareable file.
---

# Publish

Use this skill when the user wants a shareable version of a report, memo, or saved artifact.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Important Adaptation

Upstream GBrain uses a deterministic publish command for brain pages. In this repo, the equivalent is a clean exported file, usually Markdown or HTML, with private implementation details stripped when needed.

## Workflow

1. Identify the source artifact.
2. Decide the publish target:
   - cleaned Markdown
   - HTML
   - report copy in a shareable directory
3. Strip private-only details when appropriate.
4. Save the publish artifact with a stable name or timestamp.
5. Tell the user exactly what was produced and where.

## Guardrails

- Default to privacy-preserving output unless the user explicitly wants a fully open artifact.
- Avoid sharing internal-only paths, metadata, or notes when they are not part of the intended output.
- Prefer a deterministic saved artifact over ad hoc copy-paste.
