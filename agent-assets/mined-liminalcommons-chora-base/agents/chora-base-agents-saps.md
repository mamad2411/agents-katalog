# SAP Quick Reference - chora-base

**Purpose**: Quick reference guide for all Skilled Awareness Packages (SAPs) in chora-base

**For**: Root awareness file, see [../AGENTS.md](../AGENTS.md)

**Last Updated**: 2025-11-10

---

## What are SAPs?

**Skilled Awareness Packages (SAPs)** are complete, installable capability bundles with clear contracts and agent-executable blueprints.

**Every SAP includes**:
1. Capability Charter (problem, scope, outcomes)
2. Protocol Specification (technical contract)
3. Awareness Guide (agent execution patterns)
4. Adoption Blueprint (installation steps)
5. Traceability Ledger (adopter tracking)

**Why SAPs Matter**:
- Clear contracts (explicit guarantees, no assumptions)
- Predictable upgrades (sequential adoption, migration blueprints)
- Machine-readable (AI agents can parse and execute)
- Governance (versioning, change management, tracking)

---

## SAP Index

**Complete SAP catalog**: [docs/skilled-awareness/INDEX.md](../docs/skilled-awareness/INDEX.md)

**SAP Framework**: [docs/skilled-awareness/sap-framework/](../docs/skilled-awareness/sap-framework/)
- Meta-SAP defining the SAP pattern itself
- Complete reference implementation
- Templates and guidelines

---

## Core SAPs Quick Reference

### SAP-000: SAP Framework

**Purpose**: Defines what SAPs are and how they work

**Key documents**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol
- [docs/skilled-awareness/sap-framework/](../docs/skilled-awareness/sap-framework/) - Framework SAP

**When to use**:
- Creating new SAPs
- Understanding SAP structure
- Installing SAPs in projects

---

### SAP-001: Inbox Coordination Protocol

**Status**: Production (v1.1.0)

**Purpose**: Cross-repo coordination with formalized SLAs

**Quick start**:
```bash
# Read domain-specific guidance (60-70% token savings)
cat docs/skilled-awareness/inbox/AGENTS.md     # 12-min read
cat docs/skilled-awareness/inbox/CLAUDE.md     # 8-min read

# Query inbox status
python scripts/inbox-status.py --json

# Create coordination request
python scripts/inbox-generate.py --interactive
```

**What you get**:
- Type 2 intake (coordination requests) with 48h default SLA
- Event tracking in inbox/coordination/events.jsonl
- 5 CLI tools (install, query, respond, generate, status)
- Cross-repo collaboration patterns

**Integration**:
- **SAP-015**: Decompose coordination requests into beads tasks
- **SAP-010**: Log coordination events to memory system

**Documentation**:
- Protocol: [docs/skilled-awareness/inbox/protocol-spec.md](../docs/skilled-awareness/inbox/protocol-spec.md)
- Blueprint: [docs/skilled-awareness/inbox/adoption-blueprint.md](../docs/skilled-awareness/inbox/adoption-blueprint.md)

**ROI**: 20-30 min saved per coordination vs ad-hoc communication

---

### SAP-009: Agent Awareness

**Status**: Active (v2.1.0)

**Purpose**: Structured guidance files for AI agents using AGENTS.md and CLAUDE.md patterns

**Key pattern**: "Nearest File Wins" - agents read awareness file closest to code they're working on

**Quick start**:
```bash
# Adopt in your project
python scripts/install-sap.py SAP-009 --source /path/to/chora-base

# Validate awareness structure
python scripts/validate-nested-awareness.py
```

**What you get**:
- Root AGENTS.md + CLAUDE.md files
- Nested domain-specific awareness files
- Progressive context loading (200k token management)
- Critical Workflows pattern for discoverability

**File size thresholds**:
- Warning: 1,000 lines (~5.6k tokens)
- Critical: 2,000 lines (~11.2k tokens)
- **Action**: Split files when exceeding thresholds

**Documentation**:
- Protocol: [docs/skilled-awareness/agent-awareness/protocol-spec.md](../docs/skilled-awareness/agent-awareness/protocol-spec.md)
- Awareness: [docs/skilled-awareness/agent-awareness/awareness-guide.md](../docs/skilled-awareness/agent-awareness/awareness-guide.md)
- Blueprint: [docs/skilled-awareness/agent-awareness/adoption-blueprint.md](../docs/skilled-awareness/agent-awareness/adoption-blueprint.md)

**ROI**: 60-70% token reduction via progressive loading, zero missed workflows

---

### SAP-010: Memory System (A-MEM)

**Status**: Production (v1.0.0)

**Purpose**: Event-sourced agent memory for context restoration across sessions

**Quick start**:
```bash
# Work in memory system domain
cd .chora/

# Read domain-specific guidance (60-70% token savings vs root files)
cat AGENTS.md        # Generic memory patterns (13-min read)
cat CLAUDE.md        # Claude-specific workflows (8-min read)

# Log an event
echo '{"event_type":"learning_captured","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","data":{"pattern":"test-pattern"}}' >> memory/events/development.jsonl

# Create knowledge note
cp memory/knowledge/templates/default.md memory/knowledge/notes/my-pattern.md

# Query event logs
tail -n 20 memory/events/*.jsonl

# Check system health
python ../scripts/memory-health-check.py
```

**What you get**:
- **Event logging**: JSONL-format logs with trace correlation (CHORA_TRACE_ID)
- **Knowledge notes**: Markdown with YAML frontmatter, Zettelkasten wikilinks
- **Agent profiles**: YAML files capturing learned patterns
- **Query templates**: Reusable queries for common analysis patterns
- **Nested awareness**: Domain-specific .chora/AGENTS.md and .chora/CLAUDE.md

**Example workflow**:
```bash
# 1. Complete task (SAP-015 beads)
bd close task-123 --reason "Implemented async error handling pattern"

# 2. Extract pattern → knowledge note
cp .chora/memory/knowledge/templates/default.md \
   .chora/memory/knowledge/notes/async-error-handling.md

# 3. Log learning event
echo '{"event_type":"learning_captured","task_id":"task-123","confidence":0.9}' >> \
  .chora/memory/events/development.jsonl

# 4. Later: Query for context restoration (new session)
grep "async-error" .chora/memory/events/development.jsonl
```

**Integration**:
- **SAP-001**: Coordination request received → Log event in events/inbox.jsonl
- **SAP-015**: Task completed → Create knowledge note with learnings
- **SAP-012**: Sprint retrospective → Distill insights to knowledge graph

**Documentation**:
- Protocol: [docs/skilled-awareness/memory-system/protocol-spec.md](../docs/skilled-awareness/memory-system/protocol-spec.md)
- Blueprint: [docs/skilled-awareness/memory-system/adoption-blueprint.md](../docs/skilled-awareness/memory-system/adoption-blueprint.md)

**ROI**: 5-15 minutes saved per session via context restoration, 40-48 hours saved annually

**Note**: chora-base template does not use memory system. Memory is included in generated projects when `include_memory_system=true`.

---

### SAP-015: Task Tracking (Beads)

**Status**: Pilot (v1.0.0) | **Adoption Level**: L0 (Available for installation)

**Purpose**: Persistent task tracking using `.beads/issues.jsonl` for cross-session context restoration

**Quick start**:
```bash
# Read domain-specific awareness files (if SAP-015 adopted)
cd .beads/
cat AGENTS.md  # 10-min read: Beads workflow patterns
cat CLAUDE.md  # 7-min read: Claude-specific beads usage

# Alternative: Read full protocol specification
cat docs/skilled-awareness/task-tracking/protocol-spec.md  # 25-min read
```

**When to use**:
- **Session startup**: Restore context from previous session (<2 min vs 5-10 min manual)
- **Multi-session work**: Track progress across multiple Claude Code sessions
- **Backlog management**: Prioritize tasks with dependencies and blockers
- **Audit trails**: Document completion reasons and link artifacts

**Core CLI commands**:
```bash
# Session startup: Find unblocked work
bd ready --json                              # Programmatic (Claude Code)
bd ready                                     # Human-readable

# Claim task
bd update task-123 --status in_progress --assignee "claude-code"

# Add notes during work
bd update task-123 --notes "Implemented async error handling, tests passing"

# Complete task
bd close task-123 --reason "Feature implemented, tested, and documented"

# Query by status
bd list --status open --json                 # Open backlog
bd list --status in_progress --json          # Active work
bd list --status blocked --json              # Blocked tasks
bd list --status closed --json --limit 10   # Recent completions

# Query by assignee
bd list --assignee "claude-code" --json      # All Claude Code tasks
```

**Task data structure**:
```json
{
  "id": "task-456",
  "title": "Implement user authentication",
  "status": "closed",
  "priority": "high",
  "assignee": "claude-code",
  "tags": ["feature", "auth", "security"],
  "created": "2025-11-09T10:30:00Z",
  "updated": "2025-11-09T16:45:00Z",
  "closed": "2025-11-09T16:45:00Z",
  "blockers": [],
  "dependencies": [],
  "completion_reason": "Auth implemented, tested with production API, docs updated",
  "artifacts": ["src/auth.py", "tests/test_auth.py", "docs/authentication.md"]
}
```

**Integration**:
- **SAP-001**: Coordination request → Decompose into beads tasks
- **SAP-010**: Task completed → Extract learnings to knowledge notes
- **SAP-005**: CI failure → Create bead to track fix

**Documentation**:
- Protocol: [docs/skilled-awareness/task-tracking/protocol-spec.md](../docs/skilled-awareness/task-tracking/protocol-spec.md)
- Blueprint: [docs/skilled-awareness/task-tracking/adoption-blueprint.md](../docs/skilled-awareness/task-tracking/adoption-blueprint.md)

**ROI**: 5-10 minutes saved per session via context restoration, 40-80 hours saved annually

**Note**: chora-base template does not use beads. Beads is included in generated projects when adopted.

---

### SAP-019: SAP Self-Evaluation

**Purpose**: Assess SAP adoption depth, identify gaps, and generate improvement roadmaps

**When to evaluate**:
- After installing new SAP (validate installation)
- Sprint planning (generate roadmap for next sprint)
- User asks "How's our SAP adoption?"
- User asks "How can we improve SAP-X?"
- Quarterly reviews (track progress over time)

**Evaluation modes**:

**Quick Check** (30 seconds):
```bash
# Check all installed SAPs
python scripts/sap-evaluator.py --quick

# Check specific SAP
python scripts/sap-evaluator.py --quick SAP-004
```

**Deep Dive** (5 minutes):
```bash
# Analyze specific SAP, save report
python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
```

**Strategic Analysis** (30 minutes):
```bash
# Generate quarterly roadmap
python scripts/sap-evaluator.py --strategic --output docs/adoption-reports/sap-roadmap.yaml
```

**Common workflow: "How can we improve SAP-X?"**

1. Run deep dive:
   ```bash
   python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
   ```

2. Read report and extract top 3 gaps

3. Present to user:
   ```markdown
   ## SAP-004 Improvement Opportunities

   **Current Level**: 1 (Basic)
   **Next Milestone**: Level 2

   ### Priority Gaps
   1. **[Gap 1 Title]** (P0, 3 hours)
      - Impact: [description]
      - Actions: [concrete steps]
   ```

4. Offer to execute implementation

**Report structure**:
- Current State: Adoption level, completion %, next milestone
- Validation Results: Automated checks (✅/❌)
- Gap Analysis: Prioritized gaps (P0/P1/P2) with concrete actions
- Sprint Plan: This sprint focus, next sprint goals

**Tips for AI agents**:
- Start with quick check (don't deep dive unless user asks)
- Focus on top 3 gaps (don't overwhelm with full list)
- Prioritize P0 gaps (these block other SAPs)
- Be specific (reference exact commands, files, line numbers)
- Track progress (re-run evaluation after implementing improvements)

---

## Bidirectional Translation Layer (Mutual Ergonomics)

**Purpose**: Enable natural conversational interaction while executing procedurally within the ecosystem ontology

**Core Principle**: Meet users where they are. You adapt to their communication style; they don't need to memorize exact commands.

### Tools Available

#### 1. Intent Router (`scripts/intent-router.py`)

Translates natural language to formal actions with confidence scoring.

**Usage**:
```python
from intent_router import IntentRouter

router = IntentRouter("docs/dev-docs/patterns/INTENT_PATTERNS.yaml")
matches = router.route(user_input)

if matches and matches[0].confidence >= 0.7:
    # High confidence: execute
    execute_action(matches[0].action, matches[0].parameters)
elif matches and matches[0].confidence >= 0.5:
    # Medium confidence: ask for clarification
    clarify_with_user(matches[0])
else:
    # Low confidence: show alternatives
    show_alternatives(matches[:3])
```

**Common patterns**:
- "show inbox" → `run_inbox_status`
- "how are saps" → `run_sap_evaluator_quick`
- "i want to suggest a big change" → `create_strategic_proposal`
- "review coordination requests" → `review_coordination_requests`

#### 2. Glossary Search (`scripts/chora-search.py`)

Enables terminology discovery and reverse lookup.

**Usage**:
```bash
# Forward lookup: term → definition
python scripts/chora-search.py "coordination request"

# Reverse lookup: description → term
python scripts/chora-search.py --reverse "I want to suggest a big change"
# Returns: Strategic Proposal (95% confidence)

# Fuzzy matching: handles typos
python scripts/chora-search.py --fuzzy "coordenation"
```

**When to use**:
- User asks "What is X?"
- User uses unfamiliar terminology
- User describes concept without using correct term
- User makes typos

#### 3. User Preferences (`.chora/user-preferences.yaml`)

Adapt behavior based on user working style.

**Key preferences**:
- `verbosity`: concise | standard | verbose
- `formality`: casual | standard | formal
- `output_format`: terminal | markdown | json
- `require_confirmation`: always | destructive | never
- `progressive_disclosure`: true | false

#### 4. Suggestion Engine (`scripts/suggest-next.py`)

Context-aware next action recommendations.

**Usage**:
```bash
# When user asks "what next?" or "what should I do?"
python scripts/suggest-next.py

# Proactive mode (high-priority suggestions only)
python scripts/suggest-next.py --mode proactive
```

**Context signals**:
- Recent events (last 24 hours)
- Active work items (inbox/active/)
- Current phase (DDD/BDD/TDD detection)
- Quality metrics (coverage, tests, lint)
- Inbox backlog

### Communication Patterns

**Pattern 1: Natural Input → Execution → Result**

Don't explain what you'll do, show what you did:

```
✅ Good:
User: "Create coordination request for traceability"
Agent: ✅ Created coord-007-traceability-pilot.json
       ✅ Logged event: coordination_request_created
       Next: Submit for sprint planning (2025-11-15)?
```

**Pattern 2: Progressive Formalization**

Move from casual → formal as needed:
```
"I want to add health monitoring" (casual)
  → Strategic Proposal (semi-formal artifact)
  → RFC (formal discussion)
  → ADR (formal decision)
  → Coordination Request (fully formal)
  → Implementation (procedural)
```

---

## SAP Validation

**Automated SAP structure validation** using [scripts/sap-validate.py](../scripts/sap-validate.py):

**Quick commands**:
```bash
# Validate single SAP
just validate-sap-structure docs/skilled-awareness/testing-framework

# Validate all SAPs
just validate-all-saps

# Or call directly
python scripts/sap-validate.py docs/skilled-awareness/testing-framework
python scripts/sap-validate.py --all
```

**What it checks**:
- ✅ 5 required artifacts present (charter, protocol, awareness, blueprint, ledger)
- ✅ Valid frontmatter in each artifact
- ✅ SAP ID format (SAP-###)
- ✅ Version follows semver (X.Y.Z)
- ✅ Required frontmatter fields (sap_id, version, status)

---

## Creating SAPs

**When to create SAP**:
- New major capability (e.g., testing-framework, docker-operations)
- Capability needs structured governance
- Multiple adopters will use capability
- Clear upgrade path needed

**Process**:
1. Read: [docs/skilled-awareness/document-templates.md](../docs/skilled-awareness/document-templates.md)
2. Create directory: `docs/skilled-awareness/<capability-name>/`
3. Create 5 artifacts using templates
4. Add infrastructure (schemas, templates, etc.)
5. Update SAP Index: [docs/skilled-awareness/INDEX.md](../docs/skilled-awareness/INDEX.md)
6. Follow DDD → BDD → TDD:
   - DDD: Create Charter + Protocol
   - BDD: Define acceptance criteria
   - TDD: Implement infrastructure + Awareness + Blueprint

**Time estimate**: 8-20 hours per SAP (varies by complexity)

---

## Installing SAPs

**Process**:
1. Find SAP in INDEX.md
2. Navigate to SAP directory (e.g., `docs/skilled-awareness/inbox/`)
3. Read `adoption-blueprint.md`
4. Execute installation steps sequentially
5. Run validation commands
6. Update `ledger.md` (add adopter record)

**Example**:
```bash
# Find SAP
cat docs/skilled-awareness/INDEX.md

# Read blueprint
cat docs/skilled-awareness/inbox/adoption-blueprint.md

# Execute steps (agent-executable markdown instructions)
# ... follow blueprint step-by-step ...

# Validate
ls inbox/coordination/CAPABILITIES && echo "✅ Installed"
```

---

## Related Resources

**Back to root**: [../AGENTS.md](../AGENTS.md)

**Workflow guidance**: [../workflows/AGENTS.md](../workflows/AGENTS.md)

**Getting started**: [../getting-started/AGENTS.md](../getting-started/AGENTS.md)

**SAP Index**: [docs/skilled-awareness/INDEX.md](../docs/skilled-awareness/INDEX.md)

**SAP Framework**: [docs/skilled-awareness/sap-framework/](../docs/skilled-awareness/sap-framework/)
