---
name: compact-boundary-session-distillation
description: "Distill the compact boundary delta into the session memory summary and the freshest user cues needed for skill capture prompts."
metadata:
  author: ychampion
---

# SKILL: Compact Boundary Session Distillation
**Domain:** context-management  
**Trigger:** When skillify captures a repeating process, use the latest session memory and the user messages after the most recent compact boundary so the prompt only contains the current instructions.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
- Call `getSessionMemoryContent()` to fill the `<session_memory>` block; the helper already returns `null` when no file exists so the prompt displays `No session memory available.` instead of throwing.
- Slice the transcript with `getMessagesAfterCompactBoundary(context.messages)` from `runtime/utils/messages.ts`, which locates the last compact boundary and optionally projects out snipped history via `projectSnippedView` when `HISTORY_SNIP` is on.
- Feed that clip into `extractUserMessages`, which keeps only `type === 'user'` entries, flattens mixed content blocks into strings, trims blank text, and yields the freshest user steering cues.
- Replace `{{sessionMemory}}`, `{{userMessages}}`, and the optional `{{userDescriptionBlock}}` inside `SKILLIFY_PROMPT` so the kernel prompt knows which context to expose to the skill authoring assistant.

## Key Rules
- Do not let user text from before the compact boundary slip into the distilled user stanza; the `getMessagesAfterCompactBoundary` call enforces that slice.
- Always wrap the memory summary in `<session_memory>` and the user messages in `<user_messages>` so downstream tooling can parse them reproducibly.
- Respect the description the user optionally supplied, because it seeds the suggested skill name, goals, and trigger phrases in the AskUserQuestion rounds that follow.

## Example Application
When the user redirects the conversation toward automation mid-session, this pattern yields a short prompt that highlights the current process and memory highlights without dragging the whole transcript along.

## Anti-Patterns (What NOT to do)
- Do not include assistant or system messages—even if they appear in the slice—since only the user's intent should feed into the new skill definition.
- Do not drop the session memory block; even if it resolves to `null`, the placeholder text keeps the prompt structure stable for downstream parsers.
