---
name: context-prune
description: Context window management: context budgeting, priority-based pruning, conversation summarization, reference replacement, token counting, strategic truncation, and context window optimization for Claude/GPT models.
origin: AI Dev Kit
disable-model-invocation: false
---

# Context Prune

Techniques for managing context windows in LLM-assisted development: context budgeting, priority-based pruning, conversation summarization, reference replacement, token counting, strategic truncation, and optimizing context for Claude, GPT, and other models.

## When to Use

- Context window approaching its limit during a long session
- Session contains many irrelevant earlier messages
- Need to continue working on a large codebase in one session
- Transferring context between sessions (handoff)
- Optimizing prompts for cost or latency
- Working with large files that consume significant context budget
- Model starts losing track of earlier instructions

## Core Concepts

### 1. Context Window Budgets

| Model | Context Window | Recommended Budget (70% for work) |
|---|---|---|
| Claude 3.5 Sonnet | 200K tokens | 140K tokens |
| Claude 3 Opus | 200K tokens | 140K tokens |
| GPT-4o | 128K tokens | 90K tokens |
| GPT-4 Turbo | 128K tokens | 90K tokens |
| Claude 3 Haiku | 200K tokens | 140K tokens |

**Token budget allocation:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT BUDGET                           │
│                                                             │
│  System prompt    │  5-10%   │  7K-14K tokens               │
│  Instructions     │  5-10%   │  7K-14K tokens               │
│  Active files     │  40-50%  │  56K-70K tokens              │
│  Conversation     │  20-25%  │  28K-35K tokens              │
│  Reserved (output)│  10%     │  14K tokens (generation)     │
└─────────────────────────────────────────────────────────────┘
```

### 2. Token Estimation

**Quick estimation rules:**
- 1 token ≈ 4 characters (English text)
- 1 token ≈ 0.75 words
- Code is denser: ~3 chars/token (more symbols, less natural language)
- File paths: ~1 token per path segment

```python
def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars ≈ 1 token for English, 3 for code)."""
    if any(c in text for c in "{}();<>=[]"):
        return len(text) // 3  # Code-like content
    return len(text) // 4      # English text


def estimate_file_tokens(filepath: str) -> int:
    """Estimate tokens for a file's contents."""
    try:
        with open(filepath, "r") as f:
            content = f.read()
        return estimate_tokens(content)
    except (OSError, IOError):
        return 0


def context_budget(files: list[str], max_tokens: int = 140_000) -> dict:
    """Calculate context budget and warn if approaching limit."""
    total = 0
    file_costs = {}

    for f in files:
        cost = estimate_file_tokens(f)
        file_costs[f] = cost
        total += cost

    system_overhead = 15_000  # System prompt + instructions
    output_reserve = 14_000   # Reserve for model output
    available = max_tokens - system_overhead - output_reserve

    return {
        "total_file_tokens": total,
        "available_budget": available,
        "remaining": available - total,
        "usage_pct": round(total / available * 100, 1),
        "file_costs": file_costs,
        "at_risk": total > available,
    }
```

### 3. Priority-Based Pruning

Not all context is equally valuable. Prune by priority:

```
Priority 1 (KEEP):     Current task, active file, most recent exchange
Priority 2 (SUMMARIZE): Earlier relevant files, important decisions
Priority 3 (REPLACE):   Full file contents → file paths + brief descriptions
Priority 4 (DISCARD):   Explored-but-irrelevant files, failed attempts, debug output
```

**Pruning algorithm:**

```python
from dataclasses import dataclass, field
from enum import Enum


class ContextPriority(Enum):
    CRITICAL = 1    # Must keep verbatim
    HIGH = 2        # Keep, but can summarize
    MEDIUM = 3      # Replace with reference + summary
    LOW = 4         # Safe to discard


@dataclass
class ContextItem:
    content: str
    priority: ContextPriority
    description: str  # Brief description for replacement
    token_count: int
    age: int = 0       # How many messages ago this was added


def prune_context(
    items: list[ContextItem],
    max_tokens: int = 120_000,
) -> list[ContextItem]:
    """
    Prune context items to stay within token budget.

    Strategy:
    1. Keep all CRITICAL items
    2. Summarize HIGH items if over budget
    3. Replace MEDIUM items with references
    4. Discard LOW items first
    """
    total = sum(item.token_count for item in items)

    if total <= max_tokens:
        return items  # No pruning needed

    # Phase 1: Discard LOW priority items
    pruned = [i for i in items if i.priority != ContextPriority.LOW]
    total = sum(i.token_count for i in pruned)

    if total <= max_tokens:
        return pruned

    # Phase 2: Replace MEDIUM with references
    result = []
    for item in pruned:
        if item.priority == ContextPriority.MEDIUM:
            # Replace full content with path + 1-line description
            replacement = f"[Reference: {item.description}]"
            result.append(ContextItem(
                content=replacement,
                priority=item.priority,
                description=item.description,
                token_count=len(replacement) // 4,
            ))
        else:
            result.append(item)

    total = sum(i.token_count for i in result)

    if total <= max_tokens:
        return result

    # Phase 3: Summarize HIGH priority items
    final = []
    for item in result:
        if item.priority == ContextPriority.HIGH:
            summary = summarize_content(item.content, max_sentences=3)
            final.append(ContextItem(
                content=summary,
                priority=item.priority,
                description=item.description,
                token_count=len(summary) // 4,
            ))
        else:
            final.append(item)

    return final


def summarize_content(content: str, max_sentences: int = 3) -> str:
    """Extractive summarization: keep first N sentences."""
    sentences = content.split(". ")
    return ". ".join(sentences[:max_sentences]) + "."
```

### 4. Conversation Summarization

When the conversation history grows large, summarize earlier exchanges:

**Before pruning (verbose, ~2000 tokens):**
```
User: Can you help me refactor the auth module? It's getting too complex.
      The main file is src/auth/service.py and it has about 800 lines.
      I think we should split it into separate modules for token management,
      user validation, and session handling.

Assistant: I'll help you refactor the auth module. Let me first read the
           current file to understand the structure...
           [reads 800-line file]
           I can see three clear responsibilities here...
```

**After summarization (~200 tokens):**
```
Context: Refactoring src/auth/service.py (800 lines) into 3 modules:
  - token_management.py
  - user_validation.py
  - session_handler.py
  Assistant analyzed file, identified 3 responsibility boundaries.
```

**Python — Session Summarizer:**

```python
@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str
    token_count: int


def summarize_conversation(
    messages: list[Message],
    max_tokens: int = 20_000,
    keep_last: int = 5,  # Always keep the last N messages verbatim
) -> list[Message]:
    """
    Summarize earlier messages in a conversation to reduce token usage.

    Preserves:
    - The system message (always)
    - The last `keep_last` messages (always)
    - Summarizes everything in between
    """
    if len(messages) <= keep_last + 1:
        return messages  # No summarization needed

    total = sum(m.token_count for m in messages)
    if total <= max_tokens:
        return messages  # Under budget

    # Extract messages to summarize (everything between system and keep_last)
    system_msg = messages[0] if messages[0].role == "system" else None
    recent = messages[-keep_last:]
    to_summarize = messages[1:-keep_last] if system_msg else messages[:-keep_last]

    # Build summary of earlier conversation
    summary_parts = []
    current_topic = None
    topic_actions = []

    for msg in to_summarize:
        # Extract key actions/decisions from each message
        first_line = msg.content.split("\n")[0][:200]
        topic_actions.append(f"{msg.role}: {first_line}")

    summary_content = (
        f"Earlier conversation summary ({len(to_summarize)} messages):\n"
        + "\n".join(topic_actions[:10])  # Cap at 10 summary points
        + (f"\n... and {len(topic_actions) - 10} more exchanges" if len(topic_actions) > 10 else "")
    )

    summary_msg = Message(
        role="summary",
        content=summary_content,
        token_count=len(summary_content) // 4,
    )

    result = []
    if system_msg:
        result.append(system_msg)
    result.append(summary_msg)
    result.extend(recent)

    return result
```

### 5. Reference Replacement Pattern

Replace full file contents with structured references. The model can always ask to read a file if it needs the details.

**Before (full file, ~3000 tokens):**
```
Here's the contents of src/api/users.py:

[800 lines of code...]
```

**After (reference replacement, ~50 tokens):**
```
File: src/api/users.py (342 lines, 8 functions, 2 classes)
  - Class: UserRouter (FastAPI router, 12 endpoints)
  - Class: UserCreate (Pydantic model, 4 fields)
  - Functions: create_user, get_user, list_users, update_user, delete_user, ...
  Key imports: app.db, app.models.user, app.services.auth
```

**Bash — Generate File Reference:**

```bash
#!/usr/bin/env bash
# file-ref.sh — Generate a compact reference for a file
# Usage: file-ref src/api/users.py

file="$1"
if [[ ! -f "$file" ]]; then
  echo "File not found: $file"
  exit 1
fi

lines=$(wc -l < "$file")
chars=$(wc -c < "$file")

echo "File: $file ($lines lines, $chars chars)"

# Python: extract classes and functions
if [[ "$file" == *.py ]]; then
  echo "  Classes: $(grep -c '^class ' "$file")"
  echo "  Functions: $(grep -c '^def \|^async def ' "$file")"
  grep '^class \|^def \|^async def ' "$file" | head -20 | sed 's/^/    - /'

# TypeScript: extract exports, classes, functions
elif [[ "$file" == *.ts || "$file" == *.tsx ]]; then
  echo "  Exports: $(grep -c 'export ' "$file")"
  echo "  Functions: $(grep -c 'function \|const.*=.*(' "$file")"
  grep 'export \|function \|^const.*= ' "$file" | head -20 | sed 's/^/    - /'
fi

# Top imports
echo "  Imports:"
if [[ "$file" == *.py ]]; then
  grep '^import \|^from ' "$file" | head -10 | sed 's/^/    - /'
elif [[ "$file" == *.ts || "$file" == *.tsx ]]; then
  grep '^import ' "$file" | head -10 | sed 's/^/    - /'
fi
```

### 6. Strategic Truncation

When context is critically over budget, truncate systematically:

```python
def truncate_for_context(
    files: list[str],
    max_tokens: int,
    priority_files: list[str] | None = None,
) -> dict[str, str]:
    """
    Truncate file contents to fit within token budget.

    Strategy:
    1. Always include priority_files in full
    2. For other files, include only the first N lines + function signatures
    3. Truncate large files to their public API (class defs, function signatures)
    """
    priority_files = priority_files or []
    result = {}
    budget_remaining = max_tokens

    # Phase 1: Include priority files in full
    for filepath in priority_files:
        try:
            with open(filepath) as f:
                content = f.read()
            tokens = estimate_tokens(content)
            if tokens <= budget_remaining:
                result[filepath] = content
                budget_remaining -= tokens
        except (OSError, IOError):
            pass

    # Phase 2: Include truncated versions of other files
    for filepath in files:
        if filepath in result or filepath in priority_files:
            continue

        try:
            with open(filepath) as f:
                lines = f.readlines()
        except (OSError, IOError):
            continue

        # Keep first 30 lines (imports, module docstring) + last 10 lines
        # This preserves the "shape" of the file
        if len(lines) > 50:
            truncated = "".join(lines[:30]) + "\n... [truncated] ...\n" + "".join(lines[-10:])
        else:
            truncated = "".join(lines)

        tokens = estimate_tokens(truncated)
        if tokens <= budget_remaining:
            result[filepath] = truncated
            budget_remaining -= tokens

    return result
```

### 7. Context Handoff Between Sessions

When switching sessions or handing off to another developer:

```markdown
# Session Handoff Template

## Current Task
Refactor `src/auth/service.py` into 3 modules.

## What's Done
- [x] Analyzed original file (800 lines, 15 functions)
- [x] Identified 3 responsibility boundaries
- [x] Created `token_management.py` (200 lines)
- [x] Created `user_validation.py` (150 lines)

## What's In Progress
- [ ] Create `session_handler.py` (estimated 180 lines)
- [ ] Update imports in `src/auth/__init__.py`
- [ ] Run full test suite

## Key Context
- Original file: src/auth/service.py (kept for reference, not modifying)
- New modules go in: src/auth/token_management.py, src/auth/user_validation.py, src/auth/session_handler.py
- Tests are in: tests/auth/test_service.py (needs splitting too)
- Framework: FastAPI + SQLAlchemy + Pydantic
- All new modules must pass: ruff check, mypy, pytest

## Decisions Made
- Split by responsibility (not by size)
- Keep UserCreate schema in user_validation.py (it's validation logic)
- Token refresh stays in token_management.py (not session_handler)

## Files to Read Next
1. src/auth/service.py (original, for session_handler extraction)
2. tests/auth/test_service.py (for test splitting)
```

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| No pruning | Context window fills, model loses track | Prune by priority every 50K tokens |
| Truncating active files | Model can't see the code it's editing | Never truncate files currently being modified |
| Summarizing too aggressively | Model loses critical details | Summarize only MEDIUM/LOW priority items |
| Keeping all debug output | Wastes 10K+ tokens on stack traces | Discard debug output after issue resolved |
| No handoff document | Next session starts from zero | Always write a session handoff |
| File paths without content | Model can't reference the code | Include first 30 lines + signatures as minimum |

## Pruning Decision Flowchart

```
Is this item part of the current task?
  │
  ├── No ──▶ DISCARD
  │
  Yes
  │
  Is it a file the model is actively editing?
  │
  ├── Yes ──▶ KEEP VERBATIM (Priority 1)
  │
  No
  │
  Is it a file referenced in the current task?
  │
  ├── Yes ──▶ Keep full if under 200 lines, else replace with reference (Priority 2/3)
  │
  No
  │
  Is it an earlier conversation exchange?
  │
  ├── Yes ──▶ Summarize to 3-5 key points (Priority 3)
  │
  No
  │
  Is it system/instruction context?
  │
  ├── Yes ──▶ KEEP (but trim verbose examples)
  │
  No
  │
  DISCARD
```

## Success Checklist

- [ ] Context token budget calculated and tracked
- [ ] Priority levels defined (CRITICAL, HIGH, MEDIUM, LOW)
- [ ] Low-priority items discarded when over budget
- [ ] Medium-priority items replaced with references
- [ ] High-priority items summarized when necessary
- [ ] Critical items (active files) kept verbatim
- [ ] Conversation summarized before session handoff
- [ ] File reference script available (`file-ref.sh`)
- [ ] Session handoff template documented
- [ ] Output tokens reserved (10% of budget)
