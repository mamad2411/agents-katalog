---
name: hermes-lcm-context-management
description: Lossless Context Management plugin for Hermes Agent with DAG-based compression and drill-down tools
triggers:
  - install hermes lcm plugin
  - configure lossless context management
  - use hermes lcm tools
  - tune lcm compaction settings
  - debug hermes context compression
  - expand lcm summary nodes
  - manage hermes conversation history
  - configure lcm for long context models
---

# Hermes LCM Context Management

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

Hermes-LCM is a lossless context management plugin for [Hermes Agent](https://github.com/NousResearch/hermes-agent) that prevents message loss during context compression. Instead of replacing old messages with flat summaries, it:

- Stores all messages in SQLite before compaction
- Compacts old context into a hierarchical summary DAG
- Provides agent tools to drill back into compacted material
- Maintains source lineage for filtered retrieval
- Externalizes large payloads to prevent bloat

**Key difference from built-in compression**: LCM makes recall part of the active context engine with drill-down tools (`lcm_grep`, `lcm_expand`, `lcm_expand_query`) rather than relying on auxiliary cross-session search.

## Installation

### Standard Installation

Clone into Hermes plugins directory:

```bash
# General user plugin (all profiles)
git clone https://github.com/stephenschoettler/hermes-lcm \
  ~/.hermes/plugins/hermes-lcm

# Profile-specific install
git clone https://github.com/stephenschoettler/hermes-lcm \
  ~/.hermes/profiles/myprofile/plugins/hermes-lcm
```

### Symlink Installation

From an existing checkout:

```bash
cd hermes-lcm
./scripts/install.sh

# Profile-specific
HERMES_PROFILE=myprofile ./scripts/install.sh
```

### Configuration

Enable in Hermes config (YAML):

```yaml
plugins:
  enabled:
    - hermes-lcm

context:
  engine: lcm

# Keep compression enabled - LCM needs this gate
compression:
  enabled: true
```

Restart Hermes after configuration changes.

### Verification

```bash
hermes plugins
```

Expected output includes:
- Plugin list shows `hermes-lcm`
- Context engine shows `lcm`
- Tools include: `lcm_grep`, `lcm_describe`, `lcm_expand`, `lcm_expand_query`, `lcm_status`, `lcm_doctor`, `lcm_load_session`

## Core Concepts

### Message Storage

LCM stores messages in SQLite before compaction happens:

```
~/.hermes/profiles/<profile>/lcm.db  # Default path
```

### Summary DAG

Old messages are compacted into hierarchical summary nodes:

```
Raw messages → Leaf summaries → Branch summaries → Root
```

Each node tracks:
- Descendant message count
- Source lineage (for filtering)
- Depth in DAG
- Token counts

### Bounded Recovery

Agent can page back into compacted material without flooding active context:

- `lcm_grep`: Search raw messages and summaries
- `lcm_describe`: Get summary metadata
- `lcm_expand`: Retrieve child summaries or raw messages
- `lcm_expand_query`: Synthesize answer from DAG material

## Environment Configuration

### Core Settings

```bash
# Compaction trigger (fraction of context window)
export LCM_CONTEXT_THRESHOLD=0.75

# Recent messages protected from compaction
export LCM_FRESH_TAIL_COUNT=64

# Raw backlog floor before leaf compaction
export LCM_LEAF_CHUNK_TOKENS=20000

# Enable dynamic chunk-sized leaf compaction
export LCM_DYNAMIC_LEAF_CHUNK_ENABLED=false
export LCM_DYNAMIC_LEAF_CHUNK_MAX=40000
```

### Session Management

```bash
# DAG depth retained after /new (-1 all, 0 none)
export LCM_NEW_SESSION_RETAIN_DEPTH=2

# Exclude sessions from LCM storage (glob patterns)
export LCM_IGNORE_SESSION_PATTERNS="test-*,debug-*"

# Keep sessions read-only (glob patterns)
export LCM_STATELESS_SESSION_PATTERNS="readonly-*"

# Exclude messages by content regex (comma-separated)
export LCM_IGNORE_MESSAGE_PATTERNS="^SYSTEM:,^\[INTERNAL\]"
```

### Large Payload Handling

```bash
# Store oversized payloads externally
export LCM_LARGE_OUTPUT_EXTERNALIZATION_ENABLED=true
export LCM_LARGE_OUTPUT_EXTERNALIZATION_THRESHOLD_CHARS=12000

# Compact already-externalized tool results
export LCM_LARGE_OUTPUT_TRANSCRIPT_GC_ENABLED=false
```

### Model Overrides

```bash
# Override summarization model
export LCM_SUMMARY_MODEL=claude-3-5-sonnet-20241022

# Override expansion synthesis model
export LCM_EXPANSION_MODEL=gpt-4-turbo
export LCM_EXPANSION_CONTEXT_TOKENS=32000

# Timeouts
export LCM_SUMMARY_TIMEOUT_MS=60000
export LCM_EXPANSION_TIMEOUT_MS=120000
```

### Advanced

```bash
# Custom database path
export LCM_DATABASE_PATH=/custom/path/lcm.db

# Enable slash commands
export LCM_ENABLE_SLASH_COMMAND=true

# Allow destructive doctor clean operations
export LCM_DOCTOR_CLEAN_APPLY_ENABLED=false

# Critical pressure bypass (0.0 = disabled)
export LCM_CRITICAL_BUDGET_PRESSURE_RATIO=0.0
```

## Tuning for Long Context Models

For large context windows, tune threshold to avoid excessive prompt costs:

**Calculation**:
```
compaction_trigger = effective_context_window * LCM_CONTEXT_THRESHOLD
```

**Examples**:

| Context Window | Desired Trigger | Threshold | Use Case |
|----------------|-----------------|-----------|----------|
| 128K | 96K | 0.75 | Standard |
| 200K | 140K | 0.70 | Balanced |
| 400K | 240K | 0.60 | Long context |
| 1M | 250K | 0.25 | Cost-optimized |
| 1M | 400K | 0.40 | Balanced large |
| 1M | 600K | 0.60 | Max raw context |

**Example configuration for 1M token model**:

```bash
# Cost-optimized: trigger at 300K tokens
export LCM_CONTEXT_THRESHOLD=0.30

# Balanced: trigger at 400K tokens
export LCM_CONTEXT_THRESHOLD=0.40

# Max context: trigger at 600K tokens
export LCM_CONTEXT_THRESHOLD=0.60
```

## Agent Tools Usage

### lcm_status

Get current LCM state:

```python
# Agent calls this to check compression state
{
  "tool": "lcm_status",
  "params": {}
}
```

Returns:
- Session ID
- Threshold tokens
- Current prompt tokens
- Raw message count
- Summary DAG structure
- Storage path
- Git commit (if source checkout)

### lcm_grep

Search messages and summaries:

```python
# Search for keyword in raw messages
{
  "tool": "lcm_grep",
  "params": {
    "pattern": "database schema",
    "search_raw": true,
    "search_summaries": false,
    "max_results": 10
  }
}

# Search summaries only
{
  "tool": "lcm_grep",
  "params": {
    "pattern": "migration",
    "search_raw": false,
    "search_summaries": true,
    "max_results": 5
  }
}

# Filter by source (files/tools mentioned)
{
  "tool": "lcm_grep",
  "params": {
    "pattern": "error",
    "source_filter": "src/database.py",
    "search_raw": true
  }
}
```

### lcm_describe

Get summary node metadata:

```python
# Describe a specific summary node
{
  "tool": "lcm_describe",
  "params": {
    "summary_id": "s_abc123"
  }
}
```

Returns:
- Summary text
- Descendant count
- Token counts
- Depth in DAG
- Source lineage

### lcm_expand

Retrieve child summaries or raw messages:

```python
# Expand a summary to see its children
{
  "tool": "lcm_expand",
  "params": {
    "summary_id": "s_abc123",
    "max_children": 5,
    "max_raw": 10
  }
}

# Get raw messages with source filter
{
  "tool": "lcm_expand",
  "params": {
    "summary_id": "s_abc123",
    "source_filter": "config.py",
    "max_raw": 20
  }
}
```

### lcm_expand_query

Synthesize answer from DAG material using auxiliary LLM:

```python
# Ask a question about compacted history
{
  "tool": "lcm_expand_query",
  "params": {
    "query": "What database migrations were discussed earlier?",
    "summary_id": "s_abc123",  # optional: scope to subtree
    "max_raw": 50
  }
}
```

This tool:
1. Retrieves relevant raw messages and summaries
2. Calls auxiliary LLM with query + material
3. Returns synthesized answer
4. Uses `LCM_EXPANSION_MODEL` and `LCM_EXPANSION_CONTEXT_TOKENS`

### lcm_load_session

Load historical session into current context:

```python
# Load previous session
{
  "tool": "lcm_load_session",
  "params": {
    "session_id": "previous-session-abc123"
  }
}
```

### lcm_doctor

Diagnose and repair LCM state:

```python
# Check for issues
{
  "tool": "lcm_doctor",
  "params": {
    "action": "check"
  }
}

# Preview cleanup (dry run)
{
  "tool": "lcm_doctor",
  "params": {
    "action": "clean_preview"
  }
}

# Apply cleanup (requires LCM_DOCTOR_CLEAN_APPLY_ENABLED=true)
{
  "tool": "lcm_doctor",
  "params": {
    "action": "clean_apply"
  }
}
```

## Slash Commands (Optional)

Enable with `LCM_ENABLE_SLASH_COMMAND=true`:

```bash
# Check status
/lcm status

# Search
/lcm grep pattern search_raw=true

# Describe summary
/lcm describe summary_id=s_abc123

# Expand
/lcm expand summary_id=s_abc123 max_raw=20

# Query
/lcm query What was discussed about the API?

# Doctor
/lcm doctor check
/lcm doctor clean_preview
```

## Common Patterns

### Initial Setup After Installation

```bash
# 1. Verify installation
hermes plugins

# 2. Send a test message to initialize session
hermes chat "Hello"

# 3. Check LCM status
hermes chat "Can you run lcm_status?"

# 4. Verify tools are available
# Agent should have access to lcm_grep, lcm_expand, etc.
```

### Recovering Lost Context

```python
# Scenario: Agent forgot details about earlier discussion

# 1. Search for topic
{
  "tool": "lcm_grep",
  "params": {
    "pattern": "API authentication",
    "search_raw": true,
    "search_summaries": true,
    "max_results": 10
  }
}

# 2. Expand relevant summary
{
  "tool": "lcm_expand",
  "params": {
    "summary_id": "s_found_in_grep",
    "max_raw": 20
  }
}

# 3. Synthesize answer
{
  "tool": "lcm_expand_query",
  "params": {
    "query": "What authentication method did we decide to use?",
    "summary_id": "s_found_in_grep"
  }
}
```

### Debugging Compaction Issues

```bash
# Check current state
export LCM_ENABLE_SLASH_COMMAND=true
hermes chat "/lcm status"

# Run diagnostics
hermes chat "/lcm doctor check"

# Preview cleanup
hermes chat "/lcm doctor clean_preview"

# Check for orphaned summaries or raw messages
# Doctor will report:
# - Orphaned summaries (no parent)
# - Dangling raw messages (session mismatch)
# - Missing required tables
```

### Session Isolation

```bash
# Exclude test sessions from LCM
export LCM_IGNORE_SESSION_PATTERNS="test-*,temp-*,debug-*"

# Keep readonly sessions from being stored
export LCM_STATELESS_SESSION_PATTERNS="readonly-*,audit-*"

# Restart Hermes
hermes restart
```

### Large Payload Management

```bash
# Enable external storage for large outputs
export LCM_LARGE_OUTPUT_EXTERNALIZATION_ENABLED=true
export LCM_LARGE_OUTPUT_EXTERNALIZATION_THRESHOLD_CHARS=12000

# Enable transcript GC for already-externalized content
export LCM_LARGE_OUTPUT_TRANSCRIPT_GC_ENABLED=true

# Restart Hermes
hermes restart
```

External payloads stored in:
```
~/.hermes/profiles/<profile>/lcm_externalized/
```

## Troubleshooting

### Plugin Shows as Not Found

**Symptom**: `hermes plugins` shows `lcm (not found)` but tools exist

**Solution**: If tools are available, LCM is loaded. This is a host discovery mismatch, not a plugin failure.

```bash
# Verify tools exist
hermes chat "Run lcm_status"

# If tools work, plugin is functional
```

### Status Shows Unbound After Restart

**Symptom**: `/lcm status` shows `session_id: (unbound)` or `threshold_tokens: (uninitialized)`

**Solution**: Send one normal message first:

```bash
hermes chat "Hello"
hermes chat "/lcm status"  # Now shows live session data
```

### Compaction Not Triggering

**Check threshold calculation**:

```bash
# Get current context window
hermes chat "What's your context window?"

# Calculate expected trigger
# trigger = context_window * LCM_CONTEXT_THRESHOLD

# Example: 128K window, 0.75 threshold = 96K trigger
export LCM_CONTEXT_THRESHOLD=0.75
```

**Verify compression is enabled**:

```yaml
# In Hermes config
compression:
  enabled: true  # Must be true
```

### Missing Regex Message Filtering

**Symptom**: Warning about disabled message-level regex filtering

**Solution**: Install `regex` package:

```bash
pip install regex
```

LCM uses `regex` with timeouts to prevent unbounded pattern matching. Without it, `LCM_IGNORE_MESSAGE_PATTERNS` is disabled.

### High Token Costs

**Tune threshold for your model**:

```bash
# For 1M token model, don't wait until 750K
# Trigger earlier to reduce costs

# Trigger at 250K (25% of 1M)
export LCM_CONTEXT_THRESHOLD=0.25

# Trigger at 400K (40% of 1M)
export LCM_CONTEXT_THRESHOLD=0.40
```

### Database Corruption

```bash
# Run doctor check
export LCM_ENABLE_SLASH_COMMAND=true
hermes chat "/lcm doctor check"

# Preview cleanup
hermes chat "/lcm doctor clean_preview"

# Apply cleanup (if safe)
export LCM_DOCTOR_CLEAN_APPLY_ENABLED=true
hermes chat "/lcm doctor clean_apply"
```

### Update Plugin

```bash
# From plugin directory
cd ~/.hermes/plugins/hermes-lcm
git pull --ff-only

# Or for symlinked install
cd /path/to/hermes-lcm
./scripts/update.sh

# Restart Hermes
hermes restart
```

## Integration Examples

### Python Code Using LCM Tools

```python
# Example: Agent helper to search and expand context

async def recover_context(topic: str, max_depth: int = 2):
    """Search LCM and expand results to recover context."""
    
    # Search for topic
    grep_result = await hermes.call_tool("lcm_grep", {
        "pattern": topic,
        "search_raw": True,
        "search_summaries": True,
        "max_results": 5
    })
    
    if not grep_result.get("matches"):
        return f"No context found for: {topic}"
    
    # Expand first match
    first_match = grep_result["matches"][0]
    if "summary_id" in first_match:
        expand_result = await hermes.call_tool("lcm_expand", {
            "summary_id": first_match["summary_id"],
            "max_raw": 10
        })
        return expand_result
    
    return first_match


async def query_history(question: str, scope_summary_id: str = None):
    """Ask a question about compacted history."""
    
    params = {"query": question, "max_raw": 50}
    if scope_summary_id:
        params["summary_id"] = scope_summary_id
    
    result = await hermes.call_tool("lcm_expand_query", params)
    return result.get("answer", "No answer generated")
```

### Custom Configuration Template

```bash
#!/bin/bash
# lcm-config.sh - LCM configuration template

# Core compaction settings
export LCM_CONTEXT_THRESHOLD=0.75
export LCM_FRESH_TAIL_COUNT=64
export LCM_LEAF_CHUNK_TOKENS=20000

# Dynamic chunking (optional)
export LCM_DYNAMIC_LEAF_CHUNK_ENABLED=true
export LCM_DYNAMIC_LEAF_CHUNK_MAX=40000

# Session management
export LCM_NEW_SESSION_RETAIN_DEPTH=2
export LCM_IGNORE_SESSION_PATTERNS="test-*,temp-*"
export LCM_STATELESS_SESSION_PATTERNS="readonly-*"

# Large payload handling
export LCM_LARGE_OUTPUT_EXTERNALIZATION_ENABLED=true
export LCM_LARGE_OUTPUT_EXTERNALIZATION_THRESHOLD_CHARS=12000
export LCM_LARGE_OUTPUT_TRANSCRIPT_GC_ENABLED=false

# Model overrides (use env vars for API keys)
# export LCM_SUMMARY_MODEL=claude-3-5-sonnet-20241022
# export LCM_EXPANSION_MODEL=gpt-4-turbo

# Advanced
export LCM_ENABLE_SLASH_COMMAND=true
export LCM_DOCTOR_CLEAN_APPLY_ENABLED=false

# Start Hermes
hermes start
```

## Best Practices

1. **Start with defaults**: Only tune after observing actual compaction behavior
2. **Monitor token usage**: Use `lcm_status` to track prompt size and compaction triggers
3. **Tune threshold for your model**: Don't use 0.75 blindly on 1M token models
4. **Enable slash commands for debugging**: Set `LCM_ENABLE_SLASH_COMMAND=true` during setup
5. **Use source filters**: When expanding, filter by relevant files/tools to reduce noise
6. **External payloads for large outputs**: Enable externalization if tool results include large JSON/media
7. **Regular doctor checks**: Run `/lcm doctor check` periodically to catch issues early
8. **Session patterns for isolation**: Use ignore/stateless patterns to exclude test/debug sessions

## Resources

- [GitHub Repository](https://github.com/stephenschoettler/hermes-lcm)
- [LCM Paper](https://papers.voltropy.com/LCM) by Ehrlich & Blackman
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Lossless CLAW](https://github.com/martian-engineering/lossless-claw) (inspiration)
