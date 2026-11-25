---
name: session-handoff
description: Create structured session notes for continuity across conversations. Produces fixed-template notes with immutable section headers, session titles, and token-budgeted content. Use when saving session state, creating handoff notes, preparing for context compaction, or when asked to summarize work for continuity.
user-invocable: true
---

# Session Handoff

CRITICAL: Preserve the template structure exactly. Never modify, delete, or add section headers. Never modify the italic section descriptions. Only update the content below each section's description line.

## Session Title Rules

Generate a concise, sentence-case title (3-7 words) that captures the main topic or goal.

**Good titles:**
- "Fix login button on mobile"
- "Add OAuth authentication"
- "Debug failing CI tests"
- "Refactor API client error handling"

**Bad titles:**
- "Code changes" — too vague, doesn't identify the session
- "Investigate and fix the issue where the login button does not respond on mobile devices" — too long
- "Fix Login Button On Mobile" — wrong case (use sentence case, not Title Case)

## Session Notes Template

The notes file uses a fixed template. Each section has two parts that must be preserved exactly:
1. The section header (line starting with `#`)
2. The italic description line (the `_italicized text_` immediately after the header)

You ONLY update the content that comes AFTER these two preserved lines.

### Required Sections

| Section | What to Write |
|---|---|
| **Session Title** | 5-10 word descriptive title, info-dense, no filler |
| **Current State** | What's being worked on RIGHT NOW. Pending tasks. Immediate next steps. This is the most critical section for continuity. |
| **Task specification** | What the user asked to build. Design decisions and explanatory context. |
| **Files and Functions** | Important files, what they contain, why they're relevant. |
| **Workflow** | Bash commands usually run and in what order. How to interpret output if not obvious. |
| **Errors & Corrections** | Errors encountered, how fixed. What the user corrected. What approaches failed. |
| **Codebase and System Documentation** | Important system components. How they work/fit together. |
| **Learnings** | What worked, what didn't, what to avoid. Don't duplicate items from other sections. |
| **Key results** | If the user asked for specific output (answer, table, document), repeat the exact result. |
| **Worklog** | Step-by-step, what was attempted and done. Very terse summary per step. |

## Content Rules

- Write DETAILED, INFO-DENSE content. Include specifics: file paths, function names, error messages, exact commands, technical details.
- For "Files and Functions," prefer structural outlines (file purpose, key exports, function signatures) over copying large code blocks. This maximizes context recovery per token within the 2000-token budget.
- For "Key results," include the complete, exact output the user requested.
- Don't include information already in CLAUDE.md files — session notes capture session-specific knowledge, not project documentation.
- Skip sections with no substantial new insights. Don't add filler content like "No info yet" — leave blank sections unedited.
- Always update "Current State" to reflect the most recent work — this is critical for continuity after compaction.

## Token Budget

- Keep each section under ~2000 tokens. If a section approaches this limit, condense by cycling out less important details while preserving the most critical information.
- Total session notes should stay under ~12000 tokens.
- When condensing, prioritize keeping "Current State" and "Errors & Corrections" accurate and detailed.
- Use terse, information-dense writing. Every line should carry information that would be lost without these notes.

## Update Process

When updating session notes:
1. Review what's new since the last update.
2. Update every section that has new information — make all edits in parallel.
3. Preserve all headers and italic descriptions exactly as they are.
4. Focus on actionable, specific information that helps someone continue the work.
5. Don't reference the note-taking process itself in the notes content.

CRITICAL REMINDER: Never modify section headers or italic descriptions. Always update "Current State." Stay under 2000 tokens per section. Info-dense, no filler.

## Related Skills

- `context-summarization` provides the structured analysis that feeds into session notes.
- `knowledge-management` classifies what should become durable memory vs. session-specific notes.
- Session notes draw on `codebase-exploration` findings for the Files and Functions section.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Custom session note template with additional sections
- Modified token budgets per section
- Team-specific handoff requirements
- Custom title format or naming conventions
