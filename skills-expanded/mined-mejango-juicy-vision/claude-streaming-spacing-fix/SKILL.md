---
name: claude-streaming-spacing-fix
description: |
  Fix for unwanted spaces appearing inside words when streaming Claude API responses.
  Use when: (1) words appear split like "re deems" instead of "redeems", (2) numbers
  show spaces like "10. 00" instead of "10.00", (3) spacing fix between sentences
  causes mid-word spaces. The issue is adding spaces between ALL streaming chunks
  instead of only between API turns.
author: Claude Code
version: 1.0.0
date: 2026-01-30
---

# Claude Streaming Spacing Fix

## Problem

When streaming Claude API responses, words and numbers appear with unwanted spaces
inside them (e.g., "re deems", "10. 00%", "proport ional"). This breaks readability
and looks like a bug to users.

## Context / Trigger Conditions

- Words split with spaces: "re deems" instead of "redeems"
- Numbers split: "10. 00" instead of "10.00"
- Pattern: spaces appear before the last chunk of split tokens
- Usually appears after implementing a "fix" for missing spaces between sentences
- The original problem was sentences running together ("you.Let me try")

## Root Cause

Claude's streaming API returns individual tokens which can split words arbitrarily.
A naive fix for missing spaces between sentences:

```javascript
// WRONG - Too aggressive
if (!fullContent.match(/[\s\n]$/) && !chunk.match(/^[\s\n]/)) {
  yield ' '; // Adds space between ANY chunks without whitespace
}
```

This inserts spaces between streaming tokens WITHIN the same word, because words
can be split across multiple streaming chunks (e.g., "re" + "deems").

## Solution

Only add spaces between **API turns** (after tool use), not between streaming
tokens within a single response:

```javascript
let isFirstTextChunkThisTurn = true;

for await (const event of streamMessage(...)) {
  if (event.type === 'text') {
    const textChunk = event.data as string;

    // Only check spacing at the START of each API turn
    if (isFirstTextChunkThisTurn && fullResponseContent &&
        !fullResponseContent.match(/[\s\n]$/) && !textChunk.match(/^[\s\n]/)) {
      fullResponseContent += ' ';
      yield { type: 'text', data: ' ' };
    }

    isFirstTextChunkThisTurn = false; // Don't check again this turn
    fullResponseContent += textChunk;
    yield event;
  }
}
// Reset isFirstTextChunkThisTurn = true at start of next turn
```

The key insight: the original "you.Let me try" problem happens between different
Claude API calls in an agentic loop (turn 1 ends at "you.", tool use, turn 2
starts with "Let"). It does NOT happen between streaming tokens within a single
response.

## Verification

1. Test sentences after tool use: "I found it. Let me explain" should have space
2. Test words in normal streaming: "redeems" should NOT become "re deems"
3. Test numbers: "10.00" should NOT become "10. 00"

## Example

Before fix (too aggressive):
```
"10. 00%" - space before "00"
"re deems" - space before "deems"
"proport ional" - space before "ional"
```

After fix (turn-boundary only):
```
"10.00%" - correct
"redeems" - correct
"you. Let me try" - space added between turns (correct)
```

## Notes

- The original problem only occurs in agentic loops with tool use
- Streaming tokens can split ANYWHERE - mid-word, mid-number, mid-punctuation
- Don't try to be "smart" about detecting word boundaries in streaming
- Track turn boundaries explicitly with a flag

## References

- Claude API streaming documentation
- Agentic loop patterns with tool use
