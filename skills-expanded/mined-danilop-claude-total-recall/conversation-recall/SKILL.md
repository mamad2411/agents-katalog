---
name: conversation-recall
description: |
  Searches past Claude Code conversations using semantic search. Activates when recovering context after compaction, finding discussions from previous sessions, discovering cross-project preferences, or when user says "recall", "remember", "how did we". Delegates to subagent for background context gathering.
---

# Conversation Recall Skill

Search past Claude Code conversation history using semantic search.

## When to Trigger

### 1. After Compaction

When context is compacted, earlier details are summarized. Search to recover originals:

- You see a `compact_boundary` marker
- User references something discussed earlier but details are missing
- User says "like we discussed", "as I mentioned", "continue with..."

```
User: "Continue implementing the auth system like we discussed"
→ search_project_history(query="auth system implementation")
```

### 2. Cross-Session

Find discussions from previous sessions (not just the current one):

- "How did we fix that bug yesterday?"
- "What approach did we decide on last week?"
- "Remember when we refactored the database?"

```
User: "How did we fix that auth bug last week?"
→ search_project_history(query="auth bug fix")
```

### 3. Cross-Project

Find user preferences and patterns across all projects:

- "How do I usually handle errors?"
- "What's my preferred testing approach?"
- "What package manager do I use for Python?"

```
User: "How do I usually structure React components?"
→ search_global_history(query="React component structure")
```

## Which Tool to Use

| Scope | Tool | Examples |
|-------|------|----------|
| **Current project** | `search_project_history` | Bugs, decisions, implementations in *this* codebase |
| **All projects** | `search_global_history` | User preferences, patterns, conventions |

## Parameters

Both tools accept:

- `query` (required): Keywords or sentence to search
- `after` (optional): Filter to messages on/after this date (inclusive). ISO 8601 format.
- `before` (optional): Filter to messages before this date (exclusive). ISO 8601 format.
- `context_before_after` (default: 3): Messages before/after each match
- `threshold` (default: 0.2): Minimum similarity (0-1)
- `max_results` (default: 10): Results to return
- `offset` (default: 0): Skip results for pagination
- `include_subagents` (default: true): Include agent conversations

## Date Filtering

### Date Parameter Semantics

- `after`: inclusive (>=) - messages ON or AFTER this date
- `before`: exclusive (<) - messages BEFORE this date
- Format: ISO 8601 - `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DDTHH:MM:SSZ`

### Examples

**Single day:**
```
User: "What did we discuss about auth yesterday?"
Today is 2025-02-01

-> search_project_history(
    query="auth authentication login",
    after="2025-01-31",
    before="2025-02-01"
  )
```

**Date range:**
```
User: "Find database discussions from last week"
Today is 2025-02-01

-> search_project_history(
    query="database schema migration",
    after="2025-01-25",
    before="2025-02-01"
  )
```

**Open-ended (recent):**
```
User: "What have we been working on lately?"
Today is 2025-02-01

-> search_project_history(
    query="implementation work progress",
    after="2025-01-25"
  )
```

### Tips

- Combine semantic query with date filters for best results
- When date is ambiguous, use broader range and refine based on result timestamps
- Results include timestamps - you can interpret and summarize temporal patterns

## Subagent Pattern for Context Retrieval

To keep the main conversation context clean, delegate history searches to a subagent. The subagent processes full search results and returns only distilled facts.

### When to Use Subagent Pattern

- **After compaction**: Recovering detailed context that was summarized
- **Complex queries**: When you need multiple searches or cross-referencing
- **Large result sets**: When searches may return many matches to synthesize
- **Proactive context gathering**: Before starting implementation work

### How to Invoke

Use the Task tool:
```
Task(
  subagent_type="general-purpose",
  description="Retrieve context about: [TOPIC]",
  prompt="Search history for [TOPIC]. User wants [GOAL].
         Use search_project_history or search_global_history.
         Return bullet points: decisions, approaches, preferences, specifics."
)
```

### Example

User asks: "Continue the auth implementation we discussed last week"

Instead of calling search_project_history directly (which puts full results in main context), spawn a subagent:

```
Task(
  subagent_type="general-purpose",
  description="Retrieve auth implementation context",
  prompt="""
  Search conversation history for context about: authentication implementation

  The user wants to continue auth work discussed last week.
  Today is 2025-02-01.

  Use search_project_history with:
  - query="authentication implementation login JWT"
  - after="2025-01-25"

  Return key facts: what was decided, what's implemented, what's remaining.
  """
)
```

Subagent returns (to main context):
```
Key facts from auth discussions (Jan 25-31):
• Decided on JWT tokens with refresh token rotation (not sessions)
• Implemented: /login endpoint, token generation, middleware
• Remaining: /refresh endpoint, token revocation, logout
• User preference: httpOnly cookies for token storage
• File: src/auth/jwt.ts contains token logic
```

Main agent now has just the essential facts without the full search results consuming context.

### When to Search Directly vs. Use Subagent

| Scenario | Approach |
|----------|----------|
| Quick lookup, single specific fact | Direct search |
| User explicitly asks to "recall" or "search" | Direct search (show results) |
| Background context gathering | Subagent |
| Multiple related searches needed | Subagent |
| After compaction, recovering details | Subagent |
| Before starting complex implementation | Subagent |

## Tips

- Results include **context** (surrounding messages)
- Use `offset` to paginate when `has_more` is true
- Higher scores (closer to 1.0) = better matches
