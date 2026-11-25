---
name: empty-trigger-short-circuit-before-app-state
description: "Skip nested memory collection when no triggers exist so render-bound `getAppState()` is never invoked unnecessarily."
metadata:
  author: ychampion
---

# SKILL: Empty Trigger Short-Circuit Before App State
**Domain:** context-management  
**Trigger:** Use when nested memory attachment triggers may be empty and you want to avoid React render-cycle work unless there is actual work to do.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Before calling expensive or render-bound helpers, check the cheap trigger state. If `nestedMemoryAttachmentTriggers` is missing or empty, return immediately so that the expensive `getAppState()` call does not fire on every turn. Only when work exists do you fetch the React-bound state and iterate over the trigger set, ensuring each attachment run still has access to the required context but only when needed.

## Key Rules
- Check `nestedMemoryAttachmentTriggers` for truthiness and non-zero size before doing anything else.
- Keep the early exit path separate from the work path so future readers recognize the guard without parsing the loop logic.
- Only call `getAppState()` or other render-dependent helpers after you confirm there are triggers to process.
- Treat the guard as part of the method contract; stateful or async helpers should not run unless this simple check passed.

## Example Application
In a turn that has no nested memory triggers, return `[]` right away so `getAppState()` is never invoked; when triggers exist, call `getAppState()`, collect each nested attachment, and clear the set afterward as usual.

## Anti-Patterns (What NOT to do)
- Do not fetch the React `appState` before validating that the trigger set requires it.
- Do not assume the triggers will always be non-empty and let React-dependent helpers run every turn.
