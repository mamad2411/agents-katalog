---
name: media-block-compaction-prep
description: "Sanitize user messages by replacing images, documents, and other heavy media blocks with lightweight placeholders before compaction."
metadata:
  author: ychampion
---

# SKILL: Media-Block Compaction Prep
**Domain:** context-management
**Trigger:** Use when compaction must summarize a session that contains embedded media or document-heavy user messages.
**Source Pattern:** Distilled from reviewed compaction-time media stripping strategies.

## Core Method
Walk user messages before compaction and replace heavy media blocks with lightweight placeholders that preserve the fact that the media existed. Keep non-media text and message order intact so the summarizer still sees the conversational structure without paying the full token cost of embedded media. Track whether media was stripped so the summary can note that omitted content existed if needed.

## Key Rules
- Replace heavy media with explicit placeholders instead of silently dropping it.
- Preserve message order and all non-media text so downstream heuristics still see the same conversation structure.
- Apply the sanitization before the compaction request so the token savings affect the summary call itself.

## Example Application
If a user uploads screenshots and a PDF before a long debugging exchange, replace those media blocks with markers such as `[image]` or `[document]` before sending the transcript to the compactor.

## Anti-Patterns (What NOT to do)
- Do not delete media with no placeholder.
- Do not rewrite assistant message structure during this prep step.
- Do not leave nested media blocks inside heavy tool results unsanitized.
