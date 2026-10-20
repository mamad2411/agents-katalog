---
sap_id: SAP-001
version: 1.2.0
status: active
last_updated: 2025-11-11
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-150"   # Quick Start + Core Workflows
  phase_2: "lines 151-280" # Advanced Operations
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 9500
---

# Inbox Protocol (SAP-001) - Claude-Specific Awareness

**SAP ID**: SAP-001
**Version**: 1.2.0
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-11

---

## 📖 Quick Reference

**New to SAP-001?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - 5-minute setup with 4 CLI commands and coordination request examples
- 📚 **Time Savings** - 60% coordination time reduction (2 hours → 45 min per request with formalized SLAs)
- 🎯 **Type 1/2/3 Intake** - Structured coordination request taxonomy with priority-based routing
- 🔧 **7 CLI Tools** - Complete command reference (install, query, respond, generate, status, validate, archive)
- 📊 **SLA Guidelines** - Response time expectations (4h urgent, 48h default, 1-week backlog)
- 🔗 **Integration** - Works with SAP-010 (Memory), SAP-015 (Tasks), SAP-027 (Dogfooding), SAP-013 (Metrics)

This CLAUDE.md provides: Claude Code-specific workflows using Read (status), Bash (commands), Write/Edit (updates).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for using the inbox coordination system.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic inbox patterns
2. Use this file for Claude Code tool integration (Read for status, Edit for updates, Bash for events)
3. Always check `inbox/coordination/ECOSYSTEM_STATUS.yaml` for current state

### Three-Tier Intake System

| Type | Directory | Review Frequency | File Pattern |
|------|-----------|------------------|--------------|
| **Type 1: Proposals** | `inbox/incoming/proposals/` | Strategic sessions | `proposal-NNN.md` |
| **Type 2: Coordination** | `inbox/incoming/coordination/` | Sprint planning (bi-weekly) | `COORD-YYYY-NNN.json` |
| **Type 3: Tasks** | `inbox/active/` | Daily | `task-NNN/` |

---

## Claude Code Inbox Workflows

### Workflow 1: Showing Inbox Status with Read

```markdown
User: "show inbox"

Claude (Phase 1: Read Status - 0-5k tokens):
1. Read ecosystem status:
   Read inbox/coordination/ECOSYSTEM_STATUS.yaml

2. Parse key sections:
   - coordination.active_requests: Pending coordination requests
   - active_work: Current sprint tasks
   - blockers: Cross-repo dependencies

Claude (response to user):
"✅ Inbox Status:

   **Active Coordination Requests**: 3
   - COORD-2025-001: SAP validation framework (priority: high)
   - COORD-2025-002: Gateway timeout fix (priority: medium)
   - COORD-2025-003: Documentation update (priority: low)

   **Active Work**: 5 tasks in progress
   - task-042: Implement metrics tracking
   - task-043: Update awareness files

   **Blockers**: 1
   - Gateway dependency blocking backend refactor

   **Recent Completions**: 2 (last 30 days)"

Result: Inbox status displayed from ECOSYSTEM_STATUS.yaml
```

---

### Workflow 2: Creating Coordination Request with Write and Bash

```markdown
User: "Create coordination request for backend timeout fix"

Claude (Phase 1: Create JSON - 0-10k tokens):
1. Generate coordination request ID:
   Bash: ls inbox/incoming/coordination/ | grep "COORD-2025" | tail -1
   # Last ID: COORD-2025-003 → Next: COORD-2025-004

2. Write coordination request JSON:
   Write inbox/incoming/coordination/COORD-2025-004.json
   {
     "type": "coordination",
     "request_id": "CORD-2025-004",
     "title": "Backend timeout fix",
     "created": "2025-11-04",
     "description": "Gateway returns 504 timeout after 30s, need to increase to 60s",
     "priority": "high",
     "requesting_repo": "chora-base",
     "target_repos": ["backend-gateway"],
     "relationships": {
       "blocks": [],
       "blocked_by": [],
       "related_to": ["COORD-2025-002"]
     },
     "affects_saps": ["SAP-015"],
     "affects_domains": ["gateway"]
   }

Claude (Phase 2: Update Ecosystem Status - 10-20k tokens):
3. Read current status:
   Read inbox/coordination/ECOSYSTEM_STATUS.yaml

4. Edit to add request:
   Edit inbox/coordination/ECOSYSTEM_STATUS.yaml
   # Add COORD-2025-004 to coordination.active_requests

Claude (Phase 3: Log Event - 20-25k tokens):
5. Append event to log:
   Bash: echo '{"timestamp":"2025-11-04T10:30:00Z","event_type":"coordination_request_created","request_id":"COORD-2025-004","priority":"high"}' >> inbox/coordination/events.jsonl

Claude (response to user):
"✅ Created coordination request:
   - ID: COORD-2025-004
   - Title: Backend timeout fix
   - Priority: high
   - Status: pending_triage (will be reviewed in next sprint planning)

   Files created:
   - inbox/incoming/coordination/COORD-2025-004.json
   - Updated: inbox/coordination/ECOSYSTEM_STATUS.yaml
   - Logged: inbox/coordination/events.jsonl"

Result: Coordination request created and tracked
```

---

### Workflow 3: Triaging Coordination Request with Edit

```markdown
User: "Accept COORD-2025-004"

Claude (Phase 1: Read Request - 0-5k tokens):
1. Read coordination request:
   Read inbox/incoming/coordination/COORD-2025-004.json

Claude (Phase 2: Add Decision - 5-15k tokens):
2. Edit JSON to add decision:
   Edit inbox/incoming/coordination/COORD-2025-004.json
   # Add decision field:
   "decision": {
     "status": "accepted",
     "decided_by": "claude-sonnet-4",
     "decided_at": "2025-11-04T10:35:00Z",
     "rationale": "High priority, affects gateway stability"
   }

Claude (Phase 3: Update Status - 15-25k tokens):
3. Read ecosystem status:
   Read inbox/coordination/ECOSYSTEM_STATUS.yaml

4. Edit to reflect decision:
   Edit inbox/coordination/ECOSYSTEM_STATUS.yaml
   # Update COORD-2025-004 status in active_requests

Claude (Phase 4: Log Event - 25-30k tokens):
5. Log acceptance event:
   Bash: echo '{"timestamp":"2025-11-04T10:35:00Z","event_type":"coordination_request_accepted","request_id":"COORD-2025-004"}' >> inbox/coordination/events.jsonl

Claude (response to user):
"✅ Accepted COORD-2025-004:
   - Decision: accepted
   - Rationale: High priority, affects gateway stability
   - Next: Will be assigned to sprint

   Updated:
   - inbox/incoming/coordination/COORD-2025-004.json
   - inbox/coordination/ECOSYSTEM_STATUS.yaml"

Result: Coordination request triaged and accepted
```

---

### Workflow 4: Analyzing COORDs as Intentions for Light+ Planning

```markdown
User: "Run Phase 1.1 Discovery for Q4 2025"

Claude (Phase 1: Read Active COORDs - 0-10k tokens):
1. Read active coordination requests:
   Bash: cat inbox/coordination/active.jsonl | jq 'select(.status == "active")'

2. Parse each COORD to extract:
   - request_id, title, description
   - priority (P0/P1/P2), urgency (blocks_sprint/next_sprint/backlog)
   - requesting_repo (determines external vs internal)
   - affects_saps, affects_domains (user demand indicators)
   - estimated_effort (effort hours)

Claude (Phase 2: Categorize Evidence Level - 10-20k tokens):
3. For each COORD, apply evidence level rules:

   Evidence Level A (Direct feedback):
   - P0 or P1 priority
   - blocks_sprint or next_sprint urgency
   - External repo (not chora-base)
   Example: COORD-2025-006 from ecosystem-manifest (P1, next_sprint) → Level A

   Evidence Level B (Inferred need):
   - P1 or P2 priority
   - next_sprint urgency
   - Internal team request
   Example: COORD-2025-003 from chora-workspace (P2, next_sprint) → Level B

   Evidence Level C (Hypothetical):
   - P2 or P3 priority
   - backlog urgency
   - Technical debt or refactoring
   Example: COORD-2025-012 internal refactoring (P3, backlog) → Level C

Claude (Phase 3: Calculate User Demand - 20-30k tokens):
4. Calculate user demand score:
   user_demand = (affects_saps.length × 3) + (affects_domains.length × 2)

   Example:
   - COORD affects 2 SAPs + 3 domains → 2×3 + 3×2 = 12 (high demand)
   - COORD affects 0 SAPs + 1 domain → 0×3 + 1×2 = 2 (low demand)

Claude (Phase 4: Create Intention Inventory - 30-40k tokens):
5. Create .chora/planning/intentions/ directory if needed:
   Bash: mkdir -p .chora/planning/intentions

6. For each COORD, create intention entry:
   Bash: echo '{
     "intention_id": "INT-2025-005",
     "source": "COORD-2025-003",
     "description": "Update SAP-019 verification documentation",
     "evidence_level": "A",
     "user_demand": 12,
     "effort_hours": 18
   }' >> .chora/planning/intentions/2025-Q4.jsonl

Claude (Phase 5: Update COORDs with Metadata - 40-50k tokens):
7. Update each COORD with Light+ metadata:
   Read inbox/coordination/COORD-2025-003.json

   Edit inbox/coordination/COORD-2025-003.json
   # Add light_plus_metadata object:
   "light_plus_metadata": {
     "intention_id": "INT-2025-005",
     "evidence_level": "A",
     "user_demand_score": 12,
     "effort_estimate_hours": 18,
     "vision_wave_assignment": null,
     "assigned_to_roadmap": null,
     "status": "discovery"
   }

Claude (Phase 6: Log Discovery Event - 50-55k tokens):
8. Log Phase 1.1 Discovery completion:
   Bash: echo '{
     "timestamp": "2025-11-11T10:00:00Z",
     "event_type": "light_plus_phase_1_1_discovery",
     "quarter": "2025-Q4",
     "coords_analyzed": 8,
     "intentions_created": 8,
     "evidence_breakdown": {"A": 3, "B": 4, "C": 1}
   }' >> inbox/coordination/events.jsonl

Claude (response to user):
"✅ Phase 1.1 Discovery Complete (Q4 2025):

   **COORDs Analyzed**: 8 active coordination requests

   **Intentions Created**: 8
   - Evidence Level A: 3 (direct user feedback)
   - Evidence Level B: 4 (inferred needs)
   - Evidence Level C: 1 (hypothetical)

   **High-Demand Intentions** (≥10 score):
   - INT-2025-005: SAP-019 verification (demand: 12, effort: 18h)
   - INT-2025-007: React state management (demand: 15, effort: 24h)

   **Next Steps**:
   1. Run Phase 1.2 Analysis to apply Wave 1 criteria
   2. Assign intentions to Wave 1 (Q4) or Wave 2 (Q1)
   3. Update COORDs with wave assignments

   **Files Updated**:
   - Created: .chora/planning/intentions/2025-Q4.jsonl (8 intentions)
   - Updated: 8 COORD files with light_plus_metadata
   - Logged: inbox/coordination/events.jsonl"

Result: Coordination requests analyzed as intentions, ready for Wave assignment
```

---

### Workflow 5: Assigning COORDs to Wave 1/Wave 2

```markdown
User: "Apply Wave 1 criteria and assign intentions"

Claude (Phase 1: Read Intention Inventory - 0-10k tokens):
1. Read intention inventory:
   Bash: cat .chora/planning/intentions/2025-Q4.jsonl | jq -s '.'

2. Calculate Wave 1 criteria compliance:
   - Count Evidence A+B intentions
   - Check if Evidence A+B ≥ 70% of total
   - Filter intentions with user_demand ≥ 10
   - Filter intentions with effort < 50h

Claude (Phase 2: Apply Wave 1 Criteria - 10-20k tokens):
3. For each intention, check criteria:

   Wave 1 Criteria (ALL must be true):
   - Evidence Level A or B
   - User demand score ≥ 10
   - Effort estimate < 50 hours
   - Aligns with strategic themes

   Example:
   INT-2025-005: Evidence A, demand 12, effort 18h → Wave 1 ✅
   INT-2025-012: Evidence C, demand 3, effort 60h → Wave 2 ❌

Claude (Phase 3: Update COORDs - 20-40k tokens):
4. For each COORD source, update wave assignment:

   Wave 1 assignments:
   Read inbox/coordination/COORD-2025-003.json
   Edit inbox/coordination/COORD-2025-003.json
   # Update light_plus_metadata:
   "vision_wave_assignment": 1,
   "assigned_to_roadmap": "2025-Q4",
   "status": "in_wave_1"

   Wave 2 deferrals:
   Read inbox/coordination/COORD-2025-012.json
   Edit inbox/coordination/COORD-2025-012.json
   # Update light_plus_metadata:
   "vision_wave_assignment": 2,
   "assigned_to_roadmap": "2026-Q1",
   "status": "wave_2_candidate"

Claude (Phase 4: Log Wave Assignments - 40-45k tokens):
5. Log Wave 1/2 assignments:
   Bash: echo '{
     "timestamp": "2025-11-11T11:00:00Z",
     "event_type": "light_plus_wave_assignment",
     "quarter": "2025-Q4",
     "wave_1_count": 5,
     "wave_2_count": 3,
     "evidence_a_b_percent": 75
   }' >> inbox/coordination/events.jsonl

Claude (response to user):
"✅ Wave Assignment Complete (Q4 2025):

   **Wave 1 (Q4 2025)**: 5 intentions
   - INT-2025-005: SAP-019 verification (18h)
   - INT-2025-007: React state management (24h)
   - INT-2025-010: Fast-setup integration (32h)
   - INT-2025-014: Inbox SLA tracking (16h)
   - INT-2025-018: Documentation templates (12h)
   Total effort: 102 hours

   **Wave 2 (Q1 2026)**: 3 intentions (deferred)
   - INT-2025-012: Performance refactoring (60h, epic-sized)
   - INT-2025-015: ML-based analytics (85h, requires pilot)
   - INT-2025-019: Cross-org security (40h, low demand: 4)

   **Criteria Met**:
   - Evidence A+B: 75% (≥70% ✅)
   - Wave 1 capacity: 102h (< 120h target ✅)
   - Strategic alignment: All Wave 1 support ecosystem maturity theme ✅

   **Next Steps**:
   1. Communicate wave assignments to requesting repos (SLA: 48h)
   2. Run Phase 1.4 Backlog Cascade to create beads epics
   3. Update ROADMAP.md with Wave 1 themes

   **Files Updated**:
   - Updated: 8 COORD files with wave assignments
   - Logged: inbox/coordination/events.jsonl"

Result: COORDs assigned to Wave 1 (Q4) or Wave 2 (Q1) based on evidence criteria
```

---

### Workflow 6: Tracing COORD Lead Time

```markdown
User: "Calculate lead time for COORD-2025-003"

Claude (Phase 1: Read COORD Created Date - 0-5k tokens):
1. Read COORD to get created timestamp:
   Read inbox/coordination/COORD-2025-003.json
   Extract: "created": "2025-10-15T14:30:00Z"

Claude (Phase 2: Find Shipped Date - 5-10k tokens):
2. Search git history for COORD completion:
   Bash: git log --all --grep="COORD-2025-003" --date=short --format="%ad %s" | head -10

3. Identify shipped commit (look for "ship", "merge", "release"):
   Example output:
   2025-10-29 feat: ship SAP-019 verification [COORD-2025-003]
   2025-10-25 test: add verification tests [COORD-2025-003]
   2025-10-20 docs: update SAP-019 docs [COORD-2025-003]

4. Extract shipped date: 2025-10-29

Claude (Phase 3: Calculate Lead Time - 10-15k tokens):
5. Calculate days between created and shipped:
   created: 2025-10-15
   shipped: 2025-10-29
   lead_time: 14 days

6. Trace through Light+ phases:
   - Created: 2025-10-15 (COORD-2025-003)
   - Discovery: 2025-10-16 (INT-2025-005)
   - Wave 1 Assignment: 2025-10-17
   - Backlog Cascade: 2025-10-18 (beads epic created)
   - Implementation: 2025-10-20 to 2025-10-28
   - Shipped: 2025-10-29

Claude (response to user):
"✅ COORD-2025-003 Lead Time Analysis:

   **Overall Lead Time**: 14 days (2025-10-15 → 2025-10-29)

   **Phase Breakdown**:
   - Coordination → Intention: 1 day (Phase 1.1 Discovery)
   - Intention → Wave 1: 1 day (Phase 1.2 Analysis)
   - Wave 1 → Backlog: 1 day (Phase 1.4 Cascade)
   - Backlog → Implementation: 2 days (sprint planning)
   - Implementation → Shipped: 9 days (actual work)

   **Comparison to Target**:
   - Target lead time: 21 days
   - Actual: 14 days
   - Performance: 33% faster ✅

   **Traceability Chain**:
   - COORD-2025-003 (SAP-019 verification)
   - → INT-2025-005 (Evidence Level A, demand 12)
   - → Wave 1 assignment (met all criteria)
   - → beads-epic-042 (18h estimated)
   - → 4 tasks completed (beads-task-101 to 104)
   - → Shipped in v4.12.0

   **Bottleneck Analysis**:
   - Planning overhead: 4 days (29% of lead time)
   - Implementation: 9 days (64% of lead time)
   - No blockers encountered ✅"

Result: Complete lead time analysis with phase breakdown and traceability
```

---

## Claude-Specific Tips

### Tip 1: Use Read for ECOSYSTEM_STATUS.yaml First

**Pattern**:
```markdown
# ALWAYS read status before operations
Read inbox/coordination/ECOSYSTEM_STATUS.yaml

# Then perform operation
# (Create, update, triage)
```

**Why**: ECOSYSTEM_STATUS.yaml is central dashboard, must understand current state

---

### Tip 2: Use Bash for Event Logging, Not Edit

**Pattern**:
```markdown
# ✅ GOOD: Append with Bash
Bash: echo '{"event_type":"..."}' >> inbox/coordination/events.jsonl

# ❌ BAD: Read entire log, Edit to append
Read inbox/coordination/events.jsonl  # Loads entire log
Edit inbox/coordination/events.jsonl  # Inefficient
```

**Why**: Event log grows large, Bash append is efficient

---

### Tip 3: Generate IDs from Directory Listing

**Pattern**:
```markdown
# Find last coordination request ID:
Bash: ls inbox/incoming/coordination/ | grep "COORD-2025" | sort | tail -1

# Extract number, increment:
# COORD-2025-003 → COORD-2025-004
```

**Why**: Ensures unique IDs, avoids conflicts

---

### Tip 4: Use Edit for Small JSON Updates

**Pattern**:
```markdown
# Read JSON first:
Read inbox/incoming/coordination/COORD-2025-004.json

# Edit specific field:
Edit inbox/incoming/coordination/COORD-2025-004.json
# old_string: "status": "pending_triage"
# new_string: "status": "accepted"
```

**Why**: Edit preserves JSON structure, safer than rewriting

---

### Tip 5: Validate JSON with jq After Edits

**Pattern**:
```markdown
# After editing JSON:
Bash: jq . inbox/incoming/coordination/COORD-2025-004.json > /dev/null

# Check exit code:
# 0 = valid JSON ✅
# Non-zero = invalid JSON ❌
```

**Why**: Catches JSON syntax errors immediately

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Reading ECOSYSTEM_STATUS.yaml Before Operations

**Problem**: Create coordination request without checking current status

**Fix**: ALWAYS read status first

```markdown
# ❌ BAD: Create request blindly
Write inbox/incoming/coordination/COORD-2025-004.json

# ✅ GOOD: Read status first
Read inbox/coordination/ECOSYSTEM_STATUS.yaml
# Check: What's the last ID? Any blockers?
# Then: Create request
```

**Why**: Avoids duplicate IDs, understands current priorities

---

### Pitfall 2: Using Edit for Event Log Appends

**Problem**: Read entire events.jsonl, Edit to append

**Fix**: Use Bash echo append

```markdown
# ❌ BAD: Edit event log
Read inbox/coordination/events.jsonl  # 1000+ events
Edit inbox/coordination/events.jsonl  # Inefficient

# ✅ GOOD: Bash append
Bash: echo '{"event_type":"..."}' >> inbox/coordination/events.jsonl
```

**Why**: Event logs grow large, Edit loads entire file

---

### Pitfall 3: Not Validating JSON After Edits

**Problem**: Edit JSON file, don't validate, breaks parsing

**Fix**: ALWAYS validate with jq

```markdown
# After editing:
Bash: jq . inbox/incoming/coordination/COORD-2025-004.json

# If error, fix syntax
```

**Why**: Invalid JSON breaks coordination system

---

### Pitfall 4: Forgetting to Update ECOSYSTEM_STATUS.yaml

**Problem**: Create coordination request but don't update status dashboard

**Fix**: ALWAYS update both

```markdown
# Create request:
Write inbox/incoming/coordination/COORD-2025-004.json

# Update status dashboard:
Edit inbox/coordination/ECOSYSTEM_STATUS.yaml
# Add to coordination.active_requests
```

**Why**: ECOSYSTEM_STATUS.yaml is single source of truth for status

---

### Pitfall 5: Not Logging Events

**Problem**: Complete operation but don't log event

**Fix**: ALWAYS log events

```markdown
# After operation:
Bash: echo '{"timestamp":"...", "event_type":"coordination_request_created"}' >> inbox/coordination/events.jsonl
```

**Why**: Events enable traceability, required for audit trail

---

## Support & Resources

**SAP-001 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic inbox patterns
- [Capability Charter](capability-charter.md) - Three-tier intake system
- [Protocol Spec](protocol-spec.md) - Coordination request schema
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Inbox adoption tracking

**Schemas**:
- `inbox/schemas/coordination-request.schema.json` - Type 2 schema
- `inbox/schemas/strategic-proposal.schema.json` - Type 1 schema
- `inbox/schemas/implementation-task.schema.json` - Type 3 schema

**Related SAPs**:
- [SAP-000 (sap-framework)](../sap-framework/) - SAP governance
- [SAP-009 (agent-awareness)](../agent-awareness/) - AGENTS.md pattern
- [SAP-010 (memory-system)](../memory-system/) - Event logging
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - DDD→BDD→TDD

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-001
  - 3 workflows: Show Status with Read, Create Request with Write/Bash, Triage with Edit
  - Tool patterns: Read for status, Write for requests, Edit for updates, Bash for events
  - 5 Claude-specific tips, 5 common pitfalls
  - JSON validation patterns

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic inbox patterns
2. Review [protocol-spec.md](protocol-spec.md) for schemas
3. Check [capability-charter.md](capability-charter.md) for three-tier intake system
4. Read status: `Read inbox/coordination/ECOSYSTEM_STATUS.yaml`
