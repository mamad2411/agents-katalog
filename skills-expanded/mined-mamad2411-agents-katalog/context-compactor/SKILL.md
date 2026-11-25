---
name: context-compactor
description: 9-section context compression with analysis scratchpad. Adapted from Claude Code's /compact system (2026-03-31).
argument-hint: "run | status"
allowed-tools:
  - Read
  - Bash
  - Write
auto-invoke: false
model: default
context_trigger: "context window, running low, compress, compact, too long, token limit, summarize context, /compact"
---

# Semantic Context Compactor v2.0

Protects the session from Token Bloat and "Lost in the Middle" syndrome.

> **Source**: Claude Code `/compact` prompt architecture (2026-03-31).
> **Key Innovation**: Uses an `<analysis>` scratchpad block (chain-of-thought) that gets **stripped before the summary reaches context**. The analysis improves summary quality but consumes no tokens in the final context window.

## Triggers

"compact", "token limit", "clean memory", "summarize session", "context full"

## Execution Protocol

### Step 1: Analysis Phase (Private Scratchpad)

Wrap your analysis in `<analysis>` tags. This is a drafting scratchpad that will be stripped from the final output. In your analysis:

1. Chronologically analyze each message and section of the conversation. For each section thoroughly identify:
   - The user's explicit requests and intents
   - Your approach to addressing the user's requests
   - Key decisions, technical concepts and frameworks discussed
   - Specific details like: file names, full code snippets, function signatures, file edits
   - Errors you ran into and how you fixed them
   - **Specific user feedback** — especially if the user told you to do something differently
2. Double-check for technical accuracy and completeness

### Step 2: 9-Section Summary (Structured Output)

After analysis, produce a summary in `<summary>` tags with exactly these sections:

```
1. Primary Request and Intent
   — Capture ALL explicit user requests and intents in detail

2. Key Technical Concepts
   — List all important technical concepts, technologies, and frameworks discussed

3. Files and Code Sections
   — Enumerate specific files examined, modified, or created
   — Include full code snippets where applicable
   — Include WHY each file read or edit is important

4. Errors and Fixes
   — List ALL errors encountered + how fixed + user feedback on each

5. Problem Solving
   — Document problems solved and ongoing troubleshooting

6. All User Messages (Non-Tool-Result)
   — Verbatim list of ALL user messages
   — CRITICAL for detecting intent drift across the session

7. Pending Tasks
   — Outline any pending tasks explicitly asked to work on

8. Current Work
   — Describe in detail precisely what was being worked on IMMEDIATELY before this summary
   — Include file names and code snippets

9. Optional Next Step
   — Only if directly in line with user's most recent explicit request
   — Include DIRECT QUOTES from the most recent conversation
   — Do NOT start on tangential or old completed requests
```

### Step 3: Post-Processing

1. Strip the `<analysis>` block — it was for reasoning quality only
2. Format the `<summary>` content with section headers
3. Write the formatted summary to `activeContext.md` under a new `## Compacted Session` heading
4. If activeContext.md exceeds 15K tokens, archive older compacted sessions to `sessionArchive.md`

## Anti-Patterns

- ❌ Summarizing tool results verbatim (summarize the OUTCOME, not the output)
- ❌ Losing user feedback/corrections (these are the MOST IMPORTANT signals)
- ❌ Starting tangential work after compaction without user confirmation
- ❌ Acknowledging the summary or recapping — just resume as if the break never happened

## Auto-Continue Rule (Post-Compact)

> "Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with 'I'll continue' or similar. Pick up the last task as if the break never happened."

## Reference Paths

- `.context/memory_bank/activeContext.md`
- `.context/memory_bank/sessionArchive.md`
