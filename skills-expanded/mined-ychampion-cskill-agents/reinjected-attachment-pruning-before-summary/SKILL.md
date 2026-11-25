---
name: reinjected-attachment-pruning-before-summary
description: "Drop attachment classes that will be regenerated after compaction so the summarizer spends tokens on lasting context instead of disposable payloads."
metadata:
  author: ychampion
---

# SKILL: Reinjected Attachment Pruning Before Summary
**Domain:** context-management
**Trigger:** Use when some attachment types are guaranteed to be regenerated after compaction and should not consume summary budget.
**Source Pattern:** Distilled from reviewed reinjected-attachment pruning strategies.

## Core Method
Remove only the attachment classes that the system already knows it will regenerate after compaction. This keeps the summary focused on durable conversational state and avoids paying twice for transient discovery or guidance payloads. Prune before normalization and summary generation so the saved budget reduces the compaction request itself.

## Key Rules
- Prune only attachment classes with a known reinjection path.
- Apply pruning before summary generation, not after.
- Keep the pruning contract explicit so future attachment types are not stripped accidentally.

## Example Application
If skill discovery attachments are recreated on the next turn after compaction, strip them before summary generation so the compactor focuses on the real debugging conversation.

## Anti-Patterns (What NOT to do)
- Do not strip attachments that lack a reinjection path.
- Do not summarize large disposable attachments that will be reattached immediately afterward.
- Do not use pruning as a blanket excuse to hide important durable state.
