---
sap_id: SAP-010
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-180"   # Quick Start + Core Workflows
  phase_2: "lines 181-350" # Advanced Operations
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 11000
---

# Memory System (A-MEM) (SAP-010) - Claude-Specific Awareness

**SAP ID**: SAP-010
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-010?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - 2-minute setup (log events, query logs, create knowledge notes)
- 📚 **Time Savings** - Eliminates 10-15 min context restoration per session, enables cross-session continuity (hours, days, weeks)
- 🎯 **Event-Sourced Memory** - JSONL logs for development, coordination, testing, errors with append-only history
- 🔧 **Knowledge Graph** - Zettelkasten-style notes with wikilinks for long-term knowledge capture
- 📊 **Trace Correlation** - Link events across SAPs via trace_id (e.g., COORD-2025-011, BATCH-8)
- 🔗 **Integration** - Works with SAP-001 (Inbox), SAP-015 (Beads), SAP-013 (Metrics), all SAPs (event logging)

This CLAUDE.md provides: Claude Code tool integration for memory operations (Read, Bash), event logging patterns, and knowledge note workflows.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for using A-MEM cross-session memory.

### First-Time Setup

1. Read [AGENTS.md](AGENTS.md) for generic A-MEM workflows
2. Use this file for Claude Code tool integration (Read for queries, Bash for event logging)
3. Always query memory before acting (avoid repeating work)

### Session Resumption

- Use Read tool to query knowledge notes
- Use Bash tool to append events to JSONL logs
- Use Grep tool to search event logs by pattern
- Check `.chora/memory/` for existing knowledge

---

## Claude Code Memory Workflows

### Workflow 1: Learning from Past Failures with Read

```markdown
User: "Backend timeout error again"

Claude (Phase 1: Query Knowledge - 0-5k tokens):
1. Search knowledge graph for existing solution:
   Grep: pattern="backend timeout", path=".chora/memory/knowledge/notes/"

   If match found:
     Read .chora/memory/knowledge/notes/001-backend-timeout.md

2. Check knowledge note content:
   ---
   id: backend-timeout-001
   created: 2025-11-04T10:30:00Z
   tags: [error, backend, timeout]
   confidence: 0.8
   ---

   # Backend Timeout Error

   ## Problem
   Gateway returning 504 timeout after 30s

   ## Solution
   Increase timeout in gateway config to 60s:
   `uvicorn.run(..., timeout_keep_alive=60)`

   ## Related
   - gateway-config-001

Claude (Phase 2: Apply Solution - 5-15k tokens):
3. If solution found, apply it:
   Read config/gateway.py
   Edit config/gateway.py
   # Update timeout_keep_alive=60

4. Verify fix:
   Bash: python -m pytest tests/test_gateway.py::test_timeout

Claude (Phase 3: Update Knowledge if New - 15-30k tokens):
5. If NO solution found, resolve and document:
   # After fixing issue:
   Write .chora/memory/knowledge/notes/$(date +%s)-backend-timeout.md
   # Document problem, solution, related notes

6. Log knowledge creation event:
   Bash: echo '{"timestamp":"2025-11-04T10:30:00Z","event":"knowledge_created","note_id":"backend-timeout-001"}' >> .chora/memory/events/coordination.jsonl

Claude (response to user):
"✅ Backend timeout resolved:
   - Found solution in knowledge graph (001-backend-timeout.md)
   - Applied fix: Updated timeout_keep_alive to 60s
   - Verified: Tests passing

   Saved 5 minutes by querying memory first!"

Result: Error resolved quickly using existing knowledge
```

---

### Workflow 2: Tracing Multi-Step Workflows with Bash and Grep

```markdown
User: "Debug the SAP evaluation workflow"

Claude (Phase 1: Find Trace ID - 0-5k tokens):
1. Check recent events for trace_id:
   Bash: tail -10 .chora/memory/events/coordination.jsonl | grep -o '"trace_id":"[^"]*"' | head -1

   Output: "trace_id":"abc123"

Claude (Phase 2: Query All Events for Trace - 5-15k tokens):
2. Find all events with this trace_id:
   Bash: cat .chora/memory/events/*.jsonl | grep '"trace_id":"abc123"' | jq '.'

   Output:
   {"timestamp":"2025-11-04T10:00:00Z","trace_id":"abc123","event":"sap_evaluation_start","sap_id":"SAP-003"}
   {"timestamp":"2025-11-04T10:00:05Z","trace_id":"abc123","event":"artifact_check","status":"pass"}
   {"timestamp":"2025-11-04T10:00:10Z","trace_id":"abc123","event":"sap_evaluation_complete","level":2}

Claude (Phase 3: Analyze Timeline - 15-25k tokens):
3. Reconstruct workflow timeline:
   - 10:00:00 - Evaluation started for SAP-003
   - 10:00:05 - Artifact check passed
   - 10:00:10 - Evaluation completed (Level 2)

4. Identify failure point (if any):
   # Check for last successful event before error
   Bash: cat .chora/memory/events/*.jsonl | grep '"trace_id":"abc123"' | grep -E '(success|failure)' | tail -3

Claude (response to user):
"✅ SAP-003 evaluation workflow traced:
   - Timeline: 10 seconds total
   - Stages: start → artifact check → complete
   - Status: All stages successful
   - Result: Level 2 adoption

   No failures detected in this workflow."

Result: Workflow successfully traced and analyzed
```

---

### Workflow 3: Preserving Preferences with Read and Edit

```markdown
User: "Remember to use black for code formatting"

Claude (Phase 1: Read Current Profile - 0-5k tokens):
1. Read agent profile:
   Read .chora/memory/agent-profiles/claude-sonnet-4.yaml

Claude (Phase 2: Update Preference - 5-15k tokens):
2. Edit profile to add preference:
   Edit .chora/memory/agent-profiles/claude-sonnet-4.yaml
   # old_string:
   preferences:
     commit_message_style: conventional_commits

   # new_string:
   preferences:
     commit_message_style: conventional_commits
     code_style: black

Claude (Phase 3: Log Update - 15-20k tokens):
3. Log preference update:
   Bash: echo '{"timestamp":"2025-11-04T10:30:00Z","event":"preference_updated","agent_id":"claude-sonnet-4","preference":"code_style","value":"black"}' >> .chora/memory/events/coordination.jsonl

Claude (response to user):
"✅ Preference saved:
   - Agent: claude-sonnet-4
   - Preference: code_style = black
   - Persisted in: .chora/memory/agent-profiles/claude-sonnet-4.yaml

   I'll use black for all future code formatting in this project."

Result: Preference persisted across sessions
```

---

### Workflow 4: Querying Knowledge with Grep and Read

```markdown
User: "What did we learn about Docker permission errors?"

Claude (Phase 1: Search Knowledge - 0-5k tokens):
1. Search for relevant knowledge notes:
   Grep: pattern="docker.*permission", path=".chora/memory/knowledge/notes/", output_mode="files_with_matches"

   Result:
   .chora/memory/knowledge/notes/003-docker-permission.md

Claude (Phase 2: Read Knowledge Note - 5-15k tokens):
2. Read matched note:
   Read .chora/memory/knowledge/notes/003-docker-permission.md

   Content:
   ---
   id: docker-permission-003
   tags: [docker, permission, error]
   confidence: 0.9
   ---

   # Docker Permission Error

   ## Problem
   "permission denied while trying to connect to Docker daemon socket"

   ## Solution
   Add user to docker group:
   `sudo usermod -aG docker $USER`
   Then logout and login

   ## Related
   - docker-setup-001

Claude (response to user):
"✅ Found knowledge about Docker permission errors:

   **Problem**: Permission denied accessing Docker daemon socket

   **Solution**:
   1. Add user to docker group: `sudo usermod -aG docker $USER`
   2. Logout and login for changes to take effect

   **Confidence**: 0.9 (highly reliable)

   **Related Knowledge**: docker-setup-001

   Saved in: .chora/memory/knowledge/notes/003-docker-permission.md"

Result: Knowledge retrieved and presented to user
```

---

## Claude-Specific Tips

### Tip 1: Use Grep to Search Knowledge Notes Before Read

**Pattern**:
```markdown
# ALWAYS search first to find relevant notes
Grep: pattern="error_keyword", path=".chora/memory/knowledge/notes/", output_mode="files_with_matches"

# Then read matched files
Read .chora/memory/knowledge/notes/NNN-error-name.md
```

**Why**: Grep quickly identifies relevant notes, Read retrieves content

---

### Tip 2: Use Bash for Event Logging, Not Edit

**Pattern**:
```markdown
# ✅ GOOD: Append with Bash
Bash: echo '{"timestamp":"...", "event":"..."}' >> .chora/memory/events/coordination.jsonl

# ❌ BAD: Read entire log, Edit to append
Read .chora/memory/events/coordination.jsonl  # Loads thousands of events
Edit .chora/memory/events/coordination.jsonl  # Inefficient
```

**Why**: Event logs can be thousands of lines, Bash append is efficient

---

### Tip 3: Check Knowledge Graph Before Long Operations

**Pattern**:
```markdown
# User: "Fix backend timeout"

# BEFORE starting work:
Grep: pattern="backend timeout", path=".chora/memory/knowledge/notes/"

# If match found:
Read .chora/memory/knowledge/notes/NNN-backend-timeout.md
# Apply existing solution

# If no match:
# Resolve issue, THEN create knowledge note
```

**Why**: Avoid repeating work, save 5-15 minutes per error

---

### Tip 4: Use jq for Filtering JSONL Event Logs

**Pattern**:
```markdown
# Filter events by field
Bash: cat .chora/memory/events/coordination.jsonl | jq 'select(.event=="sap_evaluation")'

# Extract specific field
Bash: cat .chora/memory/events/coordination.jsonl | jq -r '.trace_id' | sort -u

# Count events by type
Bash: cat .chora/memory/events/coordination.jsonl | jq -r '.event' | sort | uniq -c
```

**Why**: jq efficiently parses JSONL, enables complex queries

---

### Tip 5: Update Agent Profile After Significant Learning

**Pattern**:
```markdown
# After solving complex problem:
Read .chora/memory/agent-profiles/claude-sonnet-4.yaml
Edit .chora/memory/agent-profiles/claude-sonnet-4.yaml
# Add learned_pattern to capabilities section
```

**Why**: Profile tracks capability growth, improves future decision-making

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Querying Knowledge Before Acting

**Problem**: User reports error, Claude immediately starts debugging without checking knowledge graph

**Fix**: ALWAYS search knowledge first

```markdown
# ❌ BAD: Start debugging immediately
User: "Backend timeout error"
Claude: Reads config files, starts debugging...

# ✅ GOOD: Query knowledge first
User: "Backend timeout error"
Claude: Grep: pattern="backend timeout", path=".chora/memory/knowledge/notes/"
# Found solution → Apply immediately
```

**Why**: Knowledge graph may already contain solution, saves 5+ minutes

---

### Pitfall 2: Using Edit Instead of Bash for Event Logging

**Problem**: Use Edit tool to append to event log, loads thousands of lines

**Fix**: Use Bash echo append

```markdown
# ❌ BAD: Edit entire log file
Read .chora/memory/events/coordination.jsonl  # Loads 1000+ events
Edit .chora/memory/events/coordination.jsonl  # Inefficient

# ✅ GOOD: Bash append
Bash: echo '{"timestamp":"...", "event":"..."}' >> .chora/memory/events/coordination.jsonl
```

**Why**: Event logs grow large, Bash append is O(1) vs Edit is O(n)

---

### Pitfall 3: Forgetting to Include Trace ID in Events

**Problem**: Log events without trace_id, can't correlate multi-step workflows

**Fix**: Include trace_id in all events for a workflow

```markdown
# At workflow start:
trace_id=$(uuidgen)

# In EVERY event for this workflow:
Bash: echo '{"trace_id":"'$trace_id'", "event":"..."}' >> .chora/memory/events/coordination.jsonl
```

**Why**: Trace IDs enable workflow reconstruction, critical for debugging

---

### Pitfall 4: Not Creating Knowledge Notes After Solving New Errors

**Problem**: Solve error successfully but don't document solution

**Fix**: ALWAYS create knowledge note after solving new error

```markdown
# After resolving error:
Write .chora/memory/knowledge/notes/$(date +%s)-error-name.md
# Document problem, solution, tags, confidence

# Log knowledge creation:
Bash: echo '{"event":"knowledge_created", "note_id":"error-name-001"}' >> .chora/memory/events/coordination.jsonl
```

**Why**: Future sessions benefit from documented solutions, avoid repeating work

---

### Pitfall 5: Not Using Tags in Knowledge Notes

**Problem**: Create knowledge note without tags in frontmatter

**Fix**: ALWAYS include tags

```markdown
---
id: backend-timeout-001
tags: [error, backend, timeout, gateway]  # ✅ Tags included
confidence: 0.8
---
```

**Why**: Tags enable discovery via Grep, improve knowledge graph navigation

---

## Support & Resources

**SAP-010 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic A-MEM workflows
- [Capability Charter](capability-charter.md) - A-MEM architecture, design principles
- [Protocol Spec](protocol-spec.md) - Event schema, knowledge note format
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Memory adoption tracking

**Event Tag Taxonomy**:
- [schemas/event-tag-taxonomy.yaml](../../../schemas/event-tag-taxonomy.yaml) - Tag reference
- Query tool: `python scripts/query-events-by-tag.py --tags <domain:tag>`

**Related SAPs**:
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - Memory initialization
- [SAP-008 (automation-scripts)](../automation-scripts/) - Script event logging
- [SAP-009 (agent-awareness)](../agent-awareness/) - Memory query patterns
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - Workflow tracing
- [SAP-019 (sap-self-evaluation)](../sap-self-evaluation/) - Evaluation events

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-010
  - 4 workflows: Learn with Read, Trace with Bash/Grep, Preserve with Edit, Query with Grep
  - Tool patterns: Grep for search, Read for retrieval, Bash for logging, Edit for profiles
  - 5 Claude-specific tips, 5 common pitfalls
  - Event logging efficiency (Bash append vs Edit)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic A-MEM workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [schemas/event-tag-taxonomy.yaml](../../../schemas/event-tag-taxonomy.yaml) for tags
4. Query knowledge: `Grep: pattern="keyword", path=".chora/memory/knowledge/notes/"`
