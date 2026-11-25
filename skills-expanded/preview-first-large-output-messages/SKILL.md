---
name: preview-first-large-output-messages
description: "Annotate persisted tool results with a preview-first header that leads with the saved artifact reference and shows the first slice before truncation."
metadata:
  author: ychampion
---

# SKILL: Preview-First Large Output Messages
**Domain:** messaging  
**Trigger:** Apply whenever a persisted tool result response must include a preview so the model sees the start of the output along with the saved artifact reference.  
**Source Pattern:** Distilled from reviewed large-result persistence and preview UX implementations.

## Core Method
When tool output is too large to show inline, persist the full artifact first and then render a response that leads with the saved-file reference plus a short preview from the beginning of the content. Build the preview from the stored artifact rather than regenerating it from a second formatting path, so what the user sees matches what was actually saved. Include enough metadata to show that the preview is partial and that the full artifact remains available for later reading.

## Key Rules
- Always begin the visible message with the persisted-file reference and the preview block so readers know the full output was preserved.
- Generate the preview from the saved content so the preview equals the displayed portion; don’t replay the original stream twice.
- Include an explicit partial-output marker when the original content exceeded the preview length so downstream renderers know the preview is incomplete.
- Persisted metadata should note whether the content is JSON so future reads interpret the file correctly.

## Example Application
When a tool returns a 200 KB JSON dump, store it as `tool-results/<id>.json`, then emit a message that points to that file and shows the first couple kilobytes as a preview so the user immediately understands what was returned.

## Anti-Patterns (What NOT to do)
- Don’t reinject the entire persisted file into the preview; keep the preview length bound to the configured slice.
- Don’t omit the persisted-file reference; without it, the preview becomes a dead end instead of a usable large-output contract.

