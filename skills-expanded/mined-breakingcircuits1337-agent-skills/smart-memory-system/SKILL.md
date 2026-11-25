---
name: smart-memory-system
description: Use when implementing or improving LISA's memory system with priority-based retrieval
---

# Smart Memory System

Implements a priority-based memory system that goes beyond static markdown files.

## The Problem

Static markdown memories (SOUL.md, USER.md, etc.) are just system prompts. They don't learn or adapt.

## The Solution

Priority-based memory with:
1. **Access tracking** - How often is each memory used?
2. **Recency scoring** - When was it last accessed?
3. **Importance weighting** - Manual + auto importance
4. **Smart retrieval** - Load high-priority, query medium, skip low

## Priority Calculation

```python
priority = (access_score * 0.3) + (recency_score * 0.4) + (importance * 0.3)
```

| Priority | Action |
|----------|--------|
| > 0.7 | Always load |
| 0.3-0.7 | Query when relevant |
| < 0.3 | Skip |

## Files

- `bin/smart-memory.py` - Main memory manager
- `.memory_meta.json` - Access tracking data

## Usage

```bash
# Run smart memory
python3 bin/smart-memory.py

# Or use memory.py (legacy)
python3 bin/memory.py
```

## Memory Layers

| Layer | Purpose | Default Priority |
|-------|---------|-----------------|
| LONG_TERM | Core identity | 0.8 |
| SOUL | Values | 0.7 |
| USER | User info | 0.6 |
| TOOLS | Available tools | 0.5 |
| AGENTS | Instructions | 0.5 |
| MEDIUM_TERM | Cross-session | 0.4 |
| SHORT_TERM | Current session | 0.6 |

## Future Enhancements

1. **ChromaDB integration** - Semantic vector search
2. **Continuous Learning v2** - Instinct-based observation hooks
3. **Learned priorities** - AI adjusts importance based on usage
