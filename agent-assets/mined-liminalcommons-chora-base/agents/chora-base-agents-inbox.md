---
sap_id: SAP-001
version: 1.2.0
status: active
last_updated: 2025-11-11
type: quick_reference
audience: all_agents
complexity: intermediate
estimated_reading_time: 13
progressive_loading:
  phase_1: "lines 1-100"
  phase_2: "lines 101-200"
  phase_3: "full"
phase_1_token_estimate: 3000
phase_2_token_estimate: 6000
phase_3_token_estimate: 6000
tags:
  - inbox
  - coordination
  - cross-repo
  - production
---

# AGENTS.md - Inbox Protocol (SAP-001)

**Domain**: Inbox Coordination
**SAP**: SAP-001 (inbox-protocol)
**Version**: 1.2.0
**Last Updated**: 2025-11-11

---

## Overview

This is the domain-specific AGENTS.md file for the inbox protocol (SAP-001). It provides context for agents working with the inbox coordination system, including Type 1/2/3 intake, coordination requests, and ecosystem status management.

**Parent**: See [/AGENTS.md](/AGENTS.md) for project-level context

**Pattern**: "Nearest File Wins" - This file provides inbox-specific context

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

This AGENTS.md provides: Agent-specific patterns for inbox triage, coordination request processing, and session startup routines.

---

## User Signal Patterns

### Inbox Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "show inbox" | run_inbox_status | Read ECOSYSTEM_STATUS.yaml | Display dashboard |
| "what's pending" | list_pending_coordination_requests | Filter by status: pending_triage | Count by priority |
| "what's in the inbox" | run_inbox_status | Same as "show inbox" | Natural variation |
| "inbox status" | run_inbox_status | Dashboard view | Formal term |
| "check inbox" | run_inbox_status | Verification pattern | Common variation |
| "review coord-NNN" | open_coordination_request(id) | Read incoming/coordination/COORD-NNN.json | Load specific request |
| "open coord-005" | open_coordination_request("coord-005") | Navigate to specific file | With parameter |
| "create coordination request" | create_coordination_request() | Use coordination-request.schema.json | Type 2 intake |
| "new coordination request" | create_coordination_request() | Variation | |
| "triage inbox" | run_sprint_planning_triage | Process pending_triage items | Bi-weekly |
| "what's blocking" | list_blockers | Filter ECOSYSTEM_STATUS.yaml by blockers field | Cross-repo dependencies |
| "show blockers" | list_blockers | Same intent | |
| "archive coord-NNN" | archive_completed_request(id) | Move incoming/ → archived/ | After fulfillment complete |

### Coordination Request Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "accept coord-NNN" | accept_coordination_request(id) | Update decision field to "accepted" | Sprint planning decision |
| "reject coord-NNN" | reject_coordination_request(id) | Update decision field to "rejected" | With rationale |
| "defer coord-NNN" | defer_coordination_request(id) | Update decision field to "backlog" | Postpone |
| "complete coord-NNN" | complete_coordination_request(id) | Move to recent_completions | Mark fulfilled |

### Ecosystem Status Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "ecosystem status" | show_ecosystem_status | Read ECOSYSTEM_STATUS.yaml | Full dashboard |
| "what repos are active" | list_active_repos | From ecosystem.repositories | Filter by status: active |
| "show recent completions" | list_recent_completions | From coordination.recent_completions | Last 30 days |

### Common Variations

**Inbox Status Queries**:
- "show inbox" / "check inbox" / "what's in the queue" → run_inbox_status
- "pending items" / "what needs review" / "coordination queue" → list_pending_coordination_requests

**Blocker Queries**:
- "block" / "blocker" / "what's blocked" / "show blockers" → list_blockers

**Coordination Request Management**:
- "review coord-NNN" / "open coord-NNN" / "show coord-NNN" → open_coordination_request(id)
- "accept coord-NNN" / "approve coord-NNN" → accept_coordination_request(id)

---

## Inbox Protocol Quick Reference

### Three-Tier Intake System

**Type 1: Strategic Proposals** (`inbox/incoming/proposals/`)
- Major changes requiring ecosystem-wide coordination
- Reviewed in strategic planning sessions
- File pattern: `proposal-NNN.md`

**Type 2: Coordination Requests** (`inbox/incoming/coordination/`)
- Cross-repo dependencies or blocking work
- Reviewed in sprint planning (every 2 weeks)
- File pattern: `COORD-YYYY-NNN.json`

**Type 3: Implementation Tasks** (`inbox/active/`)
- Implementation work within single repo
- Directly assigned to sprints
- File pattern: `task-NNN/` directories

### Key Files

**Status Dashboard**: `inbox/coordination/ECOSYSTEM_STATUS.yaml`
- Active work tracking
- Blocker management
- Recent completions

**Event Log**: `inbox/coordination/events.jsonl`
- Event traceability
- CHORA_TRACE_ID correlation
- Append-only log

**Schemas**: `inbox/schemas/`
- `coordination-request.schema.json` (Type 2)
- `strategic-proposal.schema.json` (Type 1)
- `implementation-task.schema.json` (Type 3)

### Common Tasks

**Create Coordination Request**:
```bash
# 1. Create JSON file following schema
cat > inbox/incoming/coordination/COORD-2025-NNN.json << 'EOF'
{
  "type": "coordination",
  "request_id": "COORD-2025-NNN",
  "title": "Brief title",
  "created": "YYYY-MM-DD",
  "description": "Detailed description",
  "priority": "high",
  "requesting_repo": "chora-base",
  "target_repos": ["other-repo"],

  # NEW: Relationship metadata (optional, for graph-based curation)
  "relationships": {
    "blocks": ["COORD-2025-001"],           # This request blocks others
    "blocked_by": ["COORD-2025-002"],       # Blocked by other requests
    "related_to": ["COORD-2025-003"],       # Related work
    "spawns_tasks": ["task-123"]            # Spawned implementation tasks
  },

  # NEW: SAP correlation (optional, track which SAPs are affected)
  "affects_saps": ["SAP-001", "SAP-015"],

  # NEW: Domain impact (optional, track domain scope)
  "affects_domains": ["skilled-awareness", "dev-docs"]
}
EOF

# 2. Emit event
echo '{"event_type": "coordination_request_created", ...}' >> inbox/coordination/events.jsonl

# 3. Update ECOSYSTEM_STATUS.yaml
# Add to coordination.active_requests
```

**Note**: The `relationships`, `affects_saps`, and `affects_domains` fields are **optional** but enable graph-based curation and cross-SAP analysis. See [protocol-spec.md Section 7](protocol-spec.md#7-coordination-request-schema-enhancements) for details.

**Triage Coordination Request**:
```bash
# 1. Review request in sprint planning
# 2. Add decision field to JSON
# 3. Update ECOSYSTEM_STATUS.yaml
# 4. Emit coordination_request_accepted event
```

**Complete Coordination Request**:
```bash
# 1. Add fulfillment field to JSON
# 2. Move from active_work to recent_completions in ECOSYSTEM_STATUS.yaml
# 3. Emit coordination_request_completed event
# 4. Archive if needed: mv inbox/incoming/coordination/COORD-NNN.json inbox/archived/
```

---

## Integration with Bidirectional Translation Layer

This domain AGENTS.md file integrates with the bidirectional translation layer (SAP-009 v1.1.0):

**Discovery Flow**:
1. User says "show inbox" (casual, conversational)
2. Intent router loads root AGENTS.md (discovers intent-router.py exists)
3. Intent router loads THIS FILE (domain-specific patterns)
4. Matches "show inbox" → `run_inbox_status` with high confidence
5. Agent reads `inbox/coordination/ECOSYSTEM_STATUS.yaml`
6. Agent formats output according to user verbosity preference

**Progressive Formalization**:
- Week 1: "show me the inbox" → Agent translates
- Week 2-4: "what are coordination requests?" → Agent teaches term
- Month 2+: "run_inbox_status" → Agent executes directly
- Month 3+: User provides JSON → Agent validates schema

**See**: [/AGENTS.md lines 732-944](/AGENTS.md) for bidirectional translation layer overview

---

## Integration with SAP-012 (Light+ Framework)

SAP-001 coordination requests serve as a primary input source for SAP-012 Light+ strategic planning, specifically feeding into **Phase 1.1 Discovery** to populate the intention inventory.

### Light+ Integration Overview

**What is Light+?**
- 4-level planning construct hierarchy (Strategy → Releases → Features → Tasks)
- Quarterly vision synthesis process
- Evidence-based Wave 1/Wave 2 assignment criteria
- Connects coordination requests to strategic roadmap

**How Inbox Feeds Light+:**
1. **Coordination requests** created in `inbox/coordination/` (SAP-001)
2. **Phase 1.1 Discovery** reads active COORDs quarterly (SAP-012)
3. **Intention analysis** extracts user need, evidence level, effort (SAP-012)
4. **Wave assignment** determines Q4 (Wave 1) vs Q1 (Wave 2) (SAP-012)
5. **Backlog cascade** creates beads epics from intentions (SAP-015)

### User Signal Patterns for Light+ Integration

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "run Phase 1.1 Discovery" | analyze_coords_as_intentions | Read active.jsonl + extract intentions | Quarterly workflow |
| "analyze COORD as intention" | categorize_intention_evidence_level | Assess priority/urgency/source → A/B/C | Manual analysis |
| "assign COORD to Wave 1" | update_coord_wave_assignment | jq '.light_plus_metadata.vision_wave_assignment = 1' | After wave criteria applied |
| "find Wave 1 COORDs" | query_coords_by_wave | jq 'select(.light_plus_metadata.vision_wave_assignment == 1)' | Retrospective query |
| "calculate COORD lead time" | measure_coord_to_shipped_time | Track created → shipped dates | Performance metric |
| "what COORDs became roadmap items" | trace_coord_to_roadmap | Query intention_id linkage | Impact analysis |

### Evidence Level Assessment Patterns

**Pattern: Categorize COORD as Intention Evidence Level**

```bash
# Agent workflow for evidence level assessment

# 1. Read COORD metadata
priority=$(jq -r '.priority' inbox/coordination/COORD-2025-NNN.json)
urgency=$(jq -r '.urgency' inbox/coordination/COORD-2025-NNN.json)
requesting_repo=$(jq -r '.requesting_repo' inbox/coordination/COORD-2025-NNN.json)

# 2. Apply evidence level rules
if [[ "$priority" == "P0" || "$priority" == "P1" ]] && \
   [[ "$urgency" == "blocks_sprint" || "$urgency" == "next_sprint" ]] && \
   [[ "$requesting_repo" != *"chora-base"* ]]; then
    evidence_level="A"  # Direct user feedback (external partner)
elif [[ "$priority" == "P1" || "$priority" == "P2" ]] && \
     [[ "$urgency" == "next_sprint" ]]; then
    evidence_level="B"  # Inferred need (team request)
else
    evidence_level="C"  # Hypothetical (internal improvement)
fi

# 3. Update COORD with evidence level
jq ".light_plus_metadata.evidence_level = \"$evidence_level\"" \
    inbox/coordination/COORD-2025-NNN.json > tmp.json && \
    mv tmp.json inbox/coordination/COORD-2025-NNN.json
```

### Quarterly Vision Synthesis Workflow

**Pattern: Run Phase 1.1 Discovery for Quarterly Planning**

```bash
# Agent workflow at start of quarter (e.g., 2025-Q4)

# 1. Read all active COORDs
cat inbox/coordination/active.jsonl | jq 'select(.status == "active")' > /tmp/active_coords.jsonl

# 2. For each COORD, create intention entry
while read -r coord; do
    coord_id=$(echo "$coord" | jq -r '.request_id')
    title=$(echo "$coord" | jq -r '.title')
    priority=$(echo "$coord" | jq -r '.priority')
    urgency=$(echo "$coord" | jq -r '.urgency')
    effort=$(echo "$coord" | jq -r '.estimated_effort // "unknown"')

    # Derive evidence level (use pattern above)
    evidence_level="B"  # Simplified; use full logic

    # Calculate user demand score
    affected_saps_count=$(echo "$coord" | jq -r '.affects_saps | length')
    affected_domains_count=$(echo "$coord" | jq -r '.affects_domains | length')
    user_demand=$((affected_saps_count * 3 + affected_domains_count * 2))

    # Create intention inventory entry
    echo "{
        \"intention_id\": \"INT-2025-$(date +%s)\",
        \"source\": \"$coord_id\",
        \"description\": \"$title\",
        \"evidence_level\": \"$evidence_level\",
        \"user_demand\": $user_demand,
        \"effort_hours\": \"$effort\"
    }" >> .chora/planning/intentions/2025-Q4.jsonl
done < /tmp/active_coords.jsonl

# 3. Apply Wave 1 criteria (see SAP-012 protocol-spec.md for full criteria)
# Evidence A+B ≥ 70%, user_demand ≥ 10, effort < 50h

# 4. Update COORDs with wave assignments
jq '.light_plus_metadata.vision_wave_assignment = 1' \
    inbox/coordination/COORD-2025-NNN.json > tmp.json && \
    mv tmp.json inbox/coordination/COORD-2025-NNN.json
```

### Wave Assignment Decision Tree

**Agent Decision Pattern:**

```
Is COORD priority P0 or P1?
├─ YES: Is urgency "blocks_sprint" or "next_sprint"?
│   ├─ YES: Is requesting_repo external (not chora-base)?
│   │   ├─ YES: Evidence Level A → Wave 1 candidate
│   │   └─ NO: Evidence Level B → Wave 1 or 2 (check criteria)
│   └─ NO: Evidence Level B → Wave 1 or 2 (check criteria)
└─ NO: Is priority P2 and urgency "next_sprint"?
    ├─ YES: Evidence Level B → Wave 1 or 2 (check criteria)
    └─ NO: Evidence Level C → Wave 2 candidate (or deferred)

Apply Wave 1 Criteria:
- Evidence A+B ≥ 70% of total intentions?
- User demand score ≥ 10?
- Effort estimate < 50 hours?
- Aligns with strategic themes?
    ├─ ALL YES → Assign to Wave 1
    └─ ANY NO → Defer to Wave 2
```

### Traceability Queries

**Pattern: Track COORD through Light+ Pipeline**

```bash
# 1. Find intention created from COORD
intention_id=$(jq -r '.light_plus_metadata.intention_id' inbox/coordination/COORD-2025-003.json)

# 2. Find beads epic created from intention
beads_epic=$(grep -r "$intention_id" .beads/issues.jsonl | jq -r '.id')

# 3. Find all tasks spawned from epic
beads_tasks=$(jq "select(.epic_id == \"$beads_epic\")" .beads/issues.jsonl)

# 4. Calculate lead time
created_date=$(jq -r '.created' inbox/coordination/COORD-2025-003.json)
shipped_date=$(git log --grep="COORD-2025-003" --date=short --format="%ad" | head -1)
lead_time_days=$(( ($(date -d "$shipped_date" +%s) - $(date -d "$created_date" +%s)) / 86400 ))

echo "COORD-2025-003 → $intention_id → $beads_epic → $beads_tasks (lead time: $lead_time_days days)"
```

### Common Workflows

**Workflow 1: Quarterly Phase 1.1 Discovery**
1. User: "Run Phase 1.1 Discovery for Q4 2025"
2. Agent reads active COORDs from `inbox/coordination/active.jsonl`
3. Agent extracts intentions (description, evidence level, user demand, effort)
4. Agent creates intention inventory in `.chora/planning/intentions/2025-Q4.jsonl`
5. Agent updates COORDs with `light_plus_metadata.intention_id`

**Workflow 2: COORD Wave Assignment**
1. User: "Assign COORD-2025-003 to Wave 1"
2. Agent applies Wave 1 criteria (evidence level, user demand, effort, alignment)
3. Agent updates COORD: `jq '.light_plus_metadata.vision_wave_assignment = 1'`
4. Agent emits `coordination_request_updated` event to `events.jsonl`
5. Agent responds to requesting repo with wave assignment decision

**Workflow 3: COORD Lead Time Analysis**
1. User: "Calculate lead time for COORD-2025-003"
2. Agent reads `created` field from COORD JSON
3. Agent finds shipped date via `git log --grep="COORD-2025-003"`
4. Agent calculates days: `(shipped - created) / 86400`
5. Agent reports: "COORD-2025-003 lead time: 14 days"

### Integration Benefits

**For Strategic Planning:**
- Coordination requests drive evidence-based roadmap decisions
- Transparent Wave 1 vs Wave 2 assignment criteria
- Traceability from ecosystem need → shipped feature

**For Ecosystem Partners:**
- Visibility into how COORDs become roadmap items
- Predictable SLA for wave assignment decisions (quarterly review)
- Accountability via lead time metrics

**For Retrospectives:**
- Measure % of shipped features sourced from ecosystem coordination
- Identify bottlenecks (COORDs stuck in discovery > 14 days)
- Evidence-based process improvements

### Light+ Metadata Schema

**Optional COORD fields (v1.2.0+):**

```json
{
  "light_plus_metadata": {
    "intention_id": "INT-2025-005",
    "evidence_level": "A",
    "user_demand_score": 12,
    "effort_estimate_hours": 24,
    "vision_wave_assignment": 1,
    "assigned_to_roadmap": "2025-Q4",
    "status": "in_wave_1"
  }
}
```

**See**: [protocol-spec.md Section 15](protocol-spec.md#15-light-planning-framework-integration) for complete Light+ integration specification

---

## Related SAPs

- **SAP-000** (sap-framework): Defines SAP structure and governance
- **SAP-001** (inbox-protocol): THIS SAP - Coordination system
- **SAP-009** (agent-awareness): AGENTS.md pattern and bidirectional translation
- **SAP-012** (development-lifecycle): DDD→BDD→TDD workflows referenced in coordination

---

**Version History**:
- **1.2.0** (2025-11-11): Added Light+ Framework Integration section (SAP-012), user signal patterns, workflows, decision trees
- **1.1.0** (2025-10-31): Added User Signal Patterns section for bidirectional translation layer integration
- **1.0.0** (2025-10-31): Initial domain AGENTS.md for inbox protocol
