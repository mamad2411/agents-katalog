---
name: context-summarization
description: Create structured, thorough summaries of conversations and work sessions. Preserves technical details, code changes, errors, and pending tasks for continuity. Use when summarizing a session, creating handoff notes, compacting context, or when asked to recap progress.
user-invocable: true
---

# Context Summarization

CRITICAL: Respond with TEXT ONLY. Do NOT call any tools. You already have all the context you need in the conversation. Tool calls will waste your turn.

## Two-Phase Output

Always produce two blocks:

1. **`<analysis>`** -- Your private scratchpad. Chronologically walk through the conversation, ensuring every point is covered. This block is stripped before the summary reaches anyone.
2. **`<summary>`** -- The structured artifact others will read. Must stand alone without the analysis.

## Analysis Phase

In your `<analysis>` block:
1. Chronologically analyze each message and section. For each, thoroughly identify:
   - The user's explicit requests and intents
   - Your approach to addressing them
   - Key decisions, technical concepts, and code patterns
   - Specific details: file names, full code snippets, function signatures, file edits
   - Errors encountered and how they were fixed
   - Specific user feedback, especially corrections ("do it differently")
2. Double-check for technical accuracy and completeness.

## Summary Schema

Your `<summary>` must include these sections:

### 1. Primary Request and Intent
Capture all of the user's explicit requests and intents in detail.

### 2. Key Technical Concepts
List all important technologies, frameworks, and patterns discussed.

### 3. Files and Code Sections
Enumerate specific files examined, modified, or created. For each:
- Why this file is important
- Summary of changes made (if any)
- Important code snippets (include them -- they survive compaction, your memory doesn't)

### 4. Errors and Fixes
Every error encountered, how it was fixed, and any user feedback on the fix.

### 5. Problem Solving
Problems solved and any ongoing troubleshooting.

### 6. All User Messages
List ALL non-tool-result user messages. These are critical for understanding changing intent.

### 7. Pending Tasks
Tasks explicitly asked for that are not yet complete.

### 8. Current Work
Precisely what was being worked on immediately before this summary. Include file names and code snippets.

### 9. Optional Next Step
The next step directly in line with the user's most recent explicit request. Include **verbatim quotes** from the conversation showing exactly what task was underway and where it left off. This prevents drift in task interpretation.

IMPORTANT: Only list next steps that are directly in line with the most recent work. Do not start tangential requests or revisit old completed requests without confirming with the user first.

## Scope Variants

### Full Conversation
Summarize everything from the start. Use the base schema above.

### Partial (Recent Messages Only)
When earlier context is retained and only recent messages need summarizing:
- Focus on what was discussed, learned, and accomplished in the recent messages only
- Don't re-summarize retained earlier context

### Up-To (Prefix Summary)
When your summary will precede newer messages the reader will see next:
- Replace "Current Work" with "Work Completed"
- Replace "Optional Next Step" with "Context for Continuing Work" -- key decisions, state, or context needed to understand subsequent messages

## Anti-Drift Rules

- Include verbatim quotes for next-step anchoring -- paraphrasing introduces drift
- Include full code snippets for critical changes -- they're the only thing that survives compaction reliably
- For non-critical files, prefer structural outlines (function signatures, type definitions, import/export maps) over full code blocks. Full blocks are warranted only when the exact implementation matters for continuity.
- Don't duplicate what's in CLAUDE.md or project config -- summarize work, not documentation
- No filler. Every line must carry information that would be lost without this summary.

CRITICAL REMINDER: TEXT ONLY. No tool calls. Produce `<analysis>` then `<summary>`. The analysis is your scratchpad; the summary is the artifact.

## Related Skills

- `codebase-exploration` findings should be summarized using this schema for handoff.
- `session-handoff` extends this pattern with title generation and template-based notes.
- `knowledge-management` uses these summaries to classify what should become durable knowledge.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Additional summary sections required by the team
- Focus areas for summarization (e.g., "always include test output verbatim")
- Summary length constraints
- Custom instructions appended to the summarization prompt
