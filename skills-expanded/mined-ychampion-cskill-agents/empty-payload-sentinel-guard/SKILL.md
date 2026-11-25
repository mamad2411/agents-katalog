---
name: empty-payload-sentinel-guard
description: "Guard requests from closing instantly when a tool returns nothing by injecting the sentinel message and logging the event."
metadata:
  author: ychampion
---

# SKILL: Empty Payload Sentinel Guard
**Domain:** tool-orchestration  
**Trigger:** Apply this when a tool_result block might legitimately be empty (shell commands with no stdout, MCP commands returning `content: []`, statements that finish silently) so the assistant still sees something to react to.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
Run the same emptiness check used inside `isToolResultContentEmpty`: undefined/null, whitespace strings, empty arrays, or arrays whose text blocks are themselves empty count as empty. When the check fires, log `tengu_tool_empty_result` with the sanitized tool name and short-circuit the persistence path by returning the original block with `content: "({toolName} completed with no output)"`, guaranteeing the model always sees at least one token even when the tool produced nothing.

## Key Rules
- Copy the normalized emptiness logic from `isToolResultContentEmpty` so structured arrays and whitespace-only strings are treated identically.
- Call `sanitizeToolNameForAnalytics` before logging so GrowthBook metrics stay consistent.
- Only swap the `content`; leave `tool_use_id`, `tool_version`, and other metadata untouched.
- Keep the sentinel text stable—downstream budgeting, logging, and tests rely on the literal `({toolName} completed with no output)` message.

## Example Application
Invoke this guard inside `maybePersistLargeToolResult` before any size checks; if the guard fires, it returns the sentinel immediately and prevents the empty `</function_results>` tail from tricking Claude into ending the turn.

## Anti-Patterns (What NOT to do)
- Don’t reinject a sentinel into non-empty results or structured content; the guard is exclusively for truly empty outputs.
- Don’t skip the analytics event—without it you lose signals that a tool ran but returned nothing.
- Don’t persist an empty file just to explain emptiness; the guard rewrites the content in memory without writing disk files.
