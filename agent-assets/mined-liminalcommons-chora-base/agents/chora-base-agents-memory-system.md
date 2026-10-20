---
sap_id: SAP-010
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 11
progressive_loading:
  phase_1: "lines 1-220"   # Quick Reference + Core Workflows
  phase_2: "lines 221-450" # Advanced Workflows + Event Tagging
  phase_3: "full"          # Complete including troubleshooting
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 12000
tags:
  - memory
  - a-mem
  - event-sourcing
  - knowledge-graph
  - production
---

# Memory System (A-MEM) (SAP-010) - Agent Awareness

**SAP ID**: SAP-010
**Last Updated**: 2025-11-04
**Audience**: Generic AI Coding Agents

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

This AGENTS.md provides: Generic agent patterns for memory operations, event logging workflows, and knowledge note creation for AI coding assistants.

---

## Quick Reference (Detailed)

### When to Use

**Use memory-system (A-MEM) when**:
- Learning from past failures (query knowledge graph)
- Debugging multi-step workflows (trace events by trace_id)
- Preserving user preferences across sessions (agent profiles)
- Understanding what was previously learned about topic X
- Tracking capability growth over time (successful_operations counter)

**Don't use when**:
- Storing session-specific context (use in-memory variables)
- Storing sensitive data (memory files not encrypted, use secret manager)
- Real-time metrics (use metrics-tracking SAP)
- File system backups (use git for code)

### Memory Architecture

```
.chora/memory/
├── events/                 # Event logs (JSONL format)
│   ├── script-usage.jsonl  # Script execution events
│   ├── errors.jsonl        # Error/failure events
│   └── coordination.jsonl  # Cross-agent coordination
├── knowledge/              # Zettelkasten knowledge graph
│   ├── notes/              # Individual knowledge notes
│   │   ├── 001-backend-timeout.md
│   │   └── 002-sap-evaluation.md
│   └── index.yaml          # Knowledge graph index
└── agent-profiles/         # Agent preferences
    ├── claude-sonnet-4.yaml
    └── cursor-composer.yaml
```

### Memory Types

| Type | When to Use | Persistence | Retention |
|------|-------------|-------------|-----------|
| **Event Log** | Record all operations | Append-only JSONL | 6 months |
| **Knowledge Graph** | Save learned patterns | Markdown notes | Indefinite |
| **Agent Profiles** | Store preferences + capabilities | YAML | Indefinite |

---

## Common Workflows

### Workflow 1: Learn from Past Failures (2-5 minutes)

**User signal**: "Encountered error", "Failed again", "How to fix X?"

**Purpose**: Query knowledge graph for solutions before attempting new fix

**Steps**:
1. When error encountered, search knowledge graph:
   ```bash
   grep -r "error_pattern" .chora/memory/knowledge/notes/
   ```

2. If similar error found:
   - Read knowledge note: `cat .chora/memory/knowledge/notes/NNN-error-name.md`
   - Apply documented solution
   - Update note with additional context if solution worked

3. If no match found, create new knowledge note after resolving:
   ```bash
   # After resolving error, create knowledge note
   cat > .chora/memory/knowledge/notes/$(date +%s)-backend-timeout.md <<'EOF'
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
   EOF
   ```

4. Log event to track learning:
   ```bash
   echo '{"timestamp":"2025-11-04T10:30:00Z","event":"knowledge_created","note_id":"backend-timeout-001","source":"error_resolution"}' >> .chora/memory/events/coordination.jsonl
   ```

**Expected outcome**: Avoid repeating same fix, accumulate solutions

**Common patterns**:
- Error already solved → Apply known solution (30 seconds vs 5 minutes)
- New error → Document solution for future (create knowledge note)

---

### Workflow 2: Trace Multi-Step Workflow (1-2 minutes)

**User signal**: "Debug workflow", "Trace request", "Find what happened"

**Purpose**: Correlate events across multi-step operation using trace_id

**Steps**:
1. Identify trace_id from recent event:
   ```bash
   tail -10 .chora/memory/events/coordination.jsonl | jq -r .trace_id
   ```

2. Query all events with this trace_id:
   ```bash
   cat .chora/memory/events/*.jsonl | grep "trace_id_value" | jq .
   ```

3. Reconstruct workflow timeline:
   - Sort events by timestamp
   - Identify workflow stages (request → processing → completion)
   - Find failure point (last successful event before error)

4. Example trace correlation:
   ```json
   {"timestamp":"2025-11-04T10:00:00Z","trace_id":"abc123","event":"sap_evaluation_start","sap_id":"SAP-003"}
   {"timestamp":"2025-11-04T10:00:05Z","trace_id":"abc123","event":"artifact_check","status":"pass"}
   {"timestamp":"2025-11-04T10:00:10Z","trace_id":"abc123","event":"sap_evaluation_complete","level":2}
   ```

**Expected outcome**: Identify failure point in multi-step workflow

**Tips**:
- Use consistent trace_id across all operations in workflow
- Include trace_id in all error events
- Query trace_id to reconstruct full workflow history

---

### Workflow 3: Preserve Agent Preferences (30 seconds)

**User signal**: "Remember my preferences", "Use my settings", "Save this config"

**Purpose**: Persist agent preferences across sessions

**Steps**:
1. Read current agent profile:
   ```bash
   cat .chora/memory/agent-profiles/claude-sonnet-4.yaml
   ```

2. Update profile with new preferences:
   ```yaml
   agent_id: claude-sonnet-4
   version: 1.0.0
   last_updated: 2025-11-04T10:30:00Z

   preferences:
     code_style: black
     commit_message_style: conventional_commits
     test_framework: pytest
     documentation_style: google

   capabilities:
     successful_operations:
       sap_evaluation: 25
       code_generation: 150
       debugging: 40
     learned_patterns:
       - backend_timeout_fix
       - docker_permission_error
   ```

3. Save updated profile:
   ```bash
   # Write updated YAML to profile file
   ```

4. Log preference update event:
   ```bash
   echo '{"timestamp":"2025-11-04T10:30:00Z","event":"preference_updated","agent_id":"claude-sonnet-4","preference":"code_style","value":"black"}' >> .chora/memory/events/coordination.jsonl
   ```

**Expected outcome**: Preferences persist across sessions

**Common preferences**:
- Code style (black, ruff format)
- Commit message style (conventional commits)
- Test framework (pytest, behave)
- Documentation style (Google, NumPy, Sphinx)

---

### Workflow 4: Query Knowledge Notes (30 seconds)

**User signal**: "What did we learn about X?", "Any existing solutions?", "Previous research on Y?"

**Purpose**: Search knowledge graph for relevant information

**Steps**:
1. Search knowledge notes by keyword:
   ```bash
   grep -r "keyword" .chora/memory/knowledge/notes/ | head -10
   ```

2. List all knowledge notes:
   ```bash
   ls -la .chora/memory/knowledge/notes/
   ```

3. Read relevant note:
   ```bash
   cat .chora/memory/knowledge/notes/001-backend-timeout.md
   ```

4. Check knowledge graph index for relationships:
   ```bash
   cat .chora/memory/knowledge/index.yaml | grep "backend-timeout"
   ```

**Expected outcome**: Discover existing knowledge, avoid duplicate research

**Query patterns**:
- By tag: `grep -r "tags: .*error" .chora/memory/knowledge/notes/`
- By date: `ls -lt .chora/memory/knowledge/notes/ | head -5`
- By confidence: `grep -r "confidence: 0.9" .chora/memory/knowledge/notes/`

---

### Workflow 5: Log Operation Events (10 seconds)

**User signal**: "Log this operation", "Record event", "Track this action"

**Purpose**: Append event to appropriate event log

**Steps**:
1. Determine event category:
   - Script execution → `script-usage.jsonl`
   - Errors/failures → `errors.jsonl`
   - Coordination → `coordination.jsonl`

2. Create event JSON:
   ```json
   {
     "timestamp": "2025-11-04T10:30:00Z",
     "event": "script_execution",
     "script": "bump-version.sh",
     "status": "success",
     "duration_ms": 1250,
     "trace_id": "abc123"
   }
   ```

3. Append to log file:
   ```bash
   echo '{"timestamp":"..."}' >> .chora/memory/events/script-usage.jsonl
   ```

4. Validate JSON format:
   ```bash
   tail -1 .chora/memory/events/script-usage.jsonl | jq .
   ```

**Expected outcome**: Event logged for future queries

**Event schema fields** (required):
- `timestamp` (ISO 8601)
- `event` (event type string)
- `status` (success/failure/pending)
- `trace_id` (for correlation)

---

### Workflow 6: Query Events by Tag (NEW - 30 seconds)

**User signal**: "Find all SAP evaluation events", "Count script failures", "Show coordination events"

**Purpose**: Filter events using structured event tag taxonomy

**Steps**:
1. Query events by single tag:
   ```bash
   python scripts/query-events-by-tag.py --tags sap:evaluation
   ```

2. Query events by multiple tags (AND logic):
   ```bash
   python scripts/query-events-by-tag.py --tags automation:script errors:failure
   ```

3. Export results to JSON:
   ```bash
   python scripts/query-events-by-tag.py --tags sap:evaluation --output results.json
   ```

4. Count events by tag:
   ```bash
   python scripts/query-events-by-tag.py --tags automation:script | jq length
   ```

**Expected outcome**: Filtered event list matching tag criteria

**Available tag domains**:
- `development` - Code generation, testing, documentation
- `sap` - SAP lifecycle (evaluation, generation, updates)
- `automation` - Script execution, CI/CD pipelines
- `coordination` - Cross-repo/agent coordination
- `memory` - A-MEM operations
- `infrastructure` - Gateway, backends, performance
- `errors` - Error handling, recovery, debugging

**See**: [Event Tag Taxonomy](../../../schemas/event-tag-taxonomy.yaml) for complete tag reference

---

## User Signal Pattern Table

| User Signal | Workflow | Expected Time | Memory Type |
|-------------|----------|---------------|-------------|
| "Encountered error X" | Learn from Past Failures | 2-5 min | Knowledge Graph |
| "Debug workflow" | Trace Multi-Step Workflow | 1-2 min | Event Log |
| "Remember my preferences" | Preserve Preferences | 30s | Agent Profile |
| "What did we learn about X?" | Query Knowledge Notes | 30s | Knowledge Graph |
| "Log this operation" | Log Operation Event | 10s | Event Log |
| "Find events with tag Y" | Query Events by Tag | 30s | Event Log |

---

## Best Practices

### Practice 1: Query Memory Before Acting

**Pattern**:
```bash
# ALWAYS check memory first
grep -r "error_pattern" .chora/memory/knowledge/notes/

# If found: Apply solution
cat .chora/memory/knowledge/notes/NNN-error-name.md

# If not found: Resolve, then document
# (Create knowledge note after resolution)
```

**Why**: Avoid repeating work, learn from past sessions

---

### Practice 2: Use Consistent Trace IDs

**Pattern**:
```bash
# Generate trace_id at workflow start
trace_id=$(uuidgen)

# Include in ALL events for this workflow
echo "{\"trace_id\":\"$trace_id\", ...}" >> .chora/memory/events/coordination.jsonl
```

**Why**: Enables correlation across multi-step workflows

---

### Practice 3: Tag All Events

**Pattern**:
```json
{
  "timestamp": "2025-11-04T10:30:00Z",
  "event": "sap_evaluation",
  "tags": ["sap:evaluation", "development:testing"],
  "status": "success"
}
```

**Why**: Enables filtering, counting, trend analysis via `query-events-by-tag.py`

---

### Practice 4: Update Agent Profile After Major Operations

**Pattern**:
```yaml
# After successful SAP evaluation:
capabilities:
  successful_operations:
    sap_evaluation: 26  # Increment counter
  learned_patterns:
    - sap_evaluation_workflow  # Add new pattern
```

**Why**: Track capability growth, enable more intelligent decisions over time

---

### Practice 5: Link Knowledge Notes with Related IDs

**Pattern**:
```markdown
---
id: backend-timeout-001
related: [gateway-config-001, performance-tuning-002]
---

# Backend Timeout Error

## Related Knowledge
- See: gateway-config-001 for timeout configuration
- See: performance-tuning-002 for optimization strategies
```

**Why**: Build knowledge graph, enable traversal across related concepts

---

## Common Pitfalls

### Pitfall 1: Not Querying Memory Before Acting

**Problem**: Encounter error, immediately start debugging without checking knowledge graph

**Fix**: ALWAYS query memory first

```bash
# ❌ BAD: Start debugging immediately
# (Waste 5 minutes on already-solved problem)

# ✅ GOOD: Query memory first
grep -r "backend timeout" .chora/memory/knowledge/notes/
# Found solution in 001-backend-timeout.md → Apply immediately
```

**Why**: Knowledge graph may already contain solution, saves 5+ minutes

---

### Pitfall 2: Forgetting to Log Events

**Problem**: Complete operation successfully but don't log event

**Fix**: Log ALL significant operations

```bash
# After completing operation:
echo '{"timestamp":"...", "event":"sap_evaluation", "status":"success"}' >> .chora/memory/events/coordination.jsonl
```

**Why**: Missing events break trace correlation, prevent learning from past operations

---

### Pitfall 3: Not Using Trace IDs for Multi-Step Workflows

**Problem**: Multi-step workflow fails, no way to correlate events

**Fix**: Generate trace_id at start, include in all events

```bash
# At workflow start:
trace_id=$(uuidgen)

# In every event for this workflow:
echo "{\"trace_id\":\"$trace_id\", ...}" >> .chora/memory/events/coordination.jsonl
```

**Why**: Trace IDs enable reconstruction of workflow timeline, identify failure points

---

### Pitfall 4: Creating Knowledge Notes Without Tags

**Problem**: Knowledge note created but no tags, hard to discover later

**Fix**: ALWAYS include tags in frontmatter

```markdown
---
id: backend-timeout-001
tags: [error, backend, timeout, gateway]
confidence: 0.8
---
```

**Why**: Tags enable discovery via grep, improve knowledge graph navigation

---

### Pitfall 5: Not Updating Agent Profile After Learning

**Problem**: Agent learns new pattern but doesn't update profile

**Fix**: Update profile after significant learning

```yaml
# After solving complex problem:
capabilities:
  learned_patterns:
    - backend_timeout_fix  # Add new pattern
```

**Why**: Profile tracks capability growth, enables more informed decisions in future

---

## Integration with Other SAPs

### SAP-003 (project-bootstrap)
- Generated projects include `.chora/memory/` structure
- Setup.py creates initial event logs and agent profiles
- Integration: Memory system initialized during project generation

### SAP-008 (automation-scripts)
- Scripts log execution events to `script-usage.jsonl`
- `just` commands include trace_id for correlation
- Integration: `echo '{"event":"script_execution"}' >> .chora/memory/events/script-usage.jsonl`

### SAP-009 (agent-awareness)
- Awareness files reference memory patterns
- Agents learn optimal workflows via knowledge graph
- Integration: AGENTS.md → Query memory before acting

### SAP-012 (development-lifecycle)
- Multi-phase workflows use trace_id for correlation
- Sprint progress tracked in events
- Integration: Lifecycle phases log events to coordination.jsonl

### SAP-019 (sap-self-evaluation)
- SAP evaluator logs evaluation events
- Evaluation results stored in knowledge graph
- Integration: `python scripts/sap-evaluator.py` logs to coordination.jsonl

---

## Support & Resources

**SAP-010 Documentation**:
- [Capability Charter](capability-charter.md) - A-MEM architecture, design principles
- [Protocol Spec](protocol-spec.md) - Event schema, knowledge note format, retention policies
- [Awareness Guide](awareness-guide.md) - Detailed workflows, memory operations
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Memory adoption tracking

**Event Tag Taxonomy**:
- [schemas/event-tag-taxonomy.yaml](../../../schemas/event-tag-taxonomy.yaml) - Complete tag reference
- [scripts/query-events-by-tag.py](../../../scripts/query-events-by-tag.py) - Query tool

**Related SAPs**:
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - Memory initialization
- [SAP-008 (automation-scripts)](../automation-scripts/) - Script event logging
- [SAP-009 (agent-awareness)](../agent-awareness/) - Memory query patterns
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - Workflow tracing
- [SAP-019 (sap-self-evaluation)](../sap-self-evaluation/) - Evaluation events

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-010
  - 6 workflows: Learn from Failures, Trace Workflow, Preserve Preferences, Query Knowledge, Log Events, Query by Tag
  - 6 user signal patterns
  - 5 best practices, 5 common pitfalls
  - Event tag taxonomy integration
  - Integration with SAP-003, SAP-008, SAP-009, SAP-012, SAP-019

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [schemas/event-tag-taxonomy.yaml](../../../schemas/event-tag-taxonomy.yaml) for tag reference
4. Query events: `python scripts/query-events-by-tag.py --tags <domain:tag>`
