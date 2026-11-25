---
name: main-thread-only-cache-editing
description: "Gate cached microcompact cache edits to the main thread so background forks cannot alter the shared cache state."
metadata:
  author: ychampion
---

# SKILL: Main Thread Only Cache Editing
**Domain:** context-management  
**Trigger:** Use when cached microcompact runs and you must prevent subagents or forks from writing cache edits that the main thread shares.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Only perform cache-editing microcompactions when the executing query source is the main thread (`repl_main_thread` or unspecified). This avoids contaminating shared `cachedMCState` with tool results that belong to background runs like session-memory compact, prompt suggestion, or other forks. The guard also ensures the cached MC path is never triggered in non-ANT builds that disable the feature altogether.

## Key Rules
- Wrap the cached microcompact logic with `isMainThreadSource(querySource)` so only canonical queries can edit the global cache.
- Gate the entire block behind `feature('CACHED_MICROCOMPACT')` to keep the functionality out of builds that do not support it.
- The guard must look at `querySource.startsWith('repl_main_thread')` rather than strict equality so styled prompt contexts still match.
- Reread the guard whenever adding new query sources to ensure no rogue forks affect cache edits.
- Keep the cached state initializations and edits strictly within this guarded branch so other modules cannot mutate `cachedMCState` unexpectedly.

## Example Application
When a main-thread REPL session hits the cached microcompact trigger, the guard passes, allowing `registerToolResult` and `createCacheEditsBlock` to run. Forked agents such as session memory or prompt suggestion skip this block entirely, leaving the global cache untouched.

## Anti-Patterns (What NOT to do)
- Do not let background slices access or mutate `cachedMCState`; they should always defer to the main thread’s editing path.
- Do not drop the guard when adding new caching features; the main-thread-only contract must remain explicit.
