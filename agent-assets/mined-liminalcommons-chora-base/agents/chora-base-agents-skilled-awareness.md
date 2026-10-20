# Skilled Awareness (SAP Registry) - Agent Awareness

**Domain**: Skilled Awareness Packages (SAPs)
**Total SAPs**: 45 capabilities
**Last Updated**: 2025-11-12

---

## Quick Reference

### What Are SAPs?

**SAPs (Skilled Awareness Packages)** are modular capabilities for AI-assisted development, each packaged with 5 standardized artifacts:

1. **Capability Charter**: Problem statement, solution design, success criteria
2. **Protocol Spec**: Complete technical specification, commands, workflows
3. **Awareness Guide** (AGENTS.md): Operating patterns for agents
4. **Adoption Blueprint**: Step-by-step installation guide
5. **Ledger**: Adoption tracking, metrics, feedback, version history

### Finding SAPs

**By Name**:
```bash
# Search SAP catalog
grep -i "task-tracking" sap-catalog.json

# List all SAPs
cat docs/skilled-awareness/INDEX.md
```

**By Category**:
- **Core Infrastructure**: SAP-003, SAP-004, SAP-005, SAP-006 (bootstrap, testing, CI/CD, quality)
- **Development Workflow**: SAP-012 (lifecycle), SAP-008 (automation), SAP-015 (task-tracking)
- **Agent Capabilities**: SAP-009 (awareness), SAP-010 (A-MEM memory), SAP-001 (inbox)
- **Framework**: SAP-000 (SAP framework), SAP-002 (chora-base meta)
- **React Ecosystem**: SAP-020 through SAP-026, SAP-030 through SAP-032 (React capabilities)

---

## Common Workflows

### Workflow 1: Discover Available SAPs

**Steps**:
1. Read [INDEX.md](INDEX.md) for complete SAP list
2. Check SAP status (draft, pilot, production)
3. Review dependencies in SAP catalog
4. Navigate to SAP directory for details

**Example**:
```bash
# View SAP index
cat docs/skilled-awareness/INDEX.md

# Check specific SAP
ls docs/skilled-awareness/task-tracking/

# Expected files:
# - capability-charter.md
# - protocol-spec.md
# - awareness-guide.md (or AGENTS.md)
# - adoption-blueprint.md
# - ledger.md
```

---

### Workflow 2: Adopt a SAP

**Steps**:
1. Navigate to SAP directory (e.g., `docs/skilled-awareness/task-tracking/`)
2. Read `AGENTS.md` (or `awareness-guide.md`) for quick overview
3. Read `adoption-blueprint.md` for installation steps
4. Execute installation steps
5. Update project `AGENTS.md` with SAP patterns
6. Verify adoption with validation commands

**Example (SAP-015: Task Tracking)**:
```bash
# Step 1: Navigate
cd docs/skilled-awareness/task-tracking/

# Step 2: Read overview
cat AGENTS.md

# Step 3: Read installation guide
cat adoption-blueprint.md

# Step 4: Execute installation
npm install -g @beads/bd
bd init

# Step 5: Update project AGENTS.md
# (Add beads patterns to root AGENTS.md)

# Step 6: Verify
bd version
bd doctor
```

---

### Workflow 3: Understand SAP Integration

**Steps**:
1. Read target SAP's `AGENTS.md` for integration section
2. Check `protocol-spec.md` for technical integration details
3. Review related SAP's `AGENTS.md` for cross-references
4. Implement integration patterns

**Example (SAP-015 + SAP-001: Beads + Inbox)**:
```bash
# Read SAP-015 awareness guide
cat docs/skilled-awareness/task-tracking/AGENTS.md
# Look for "Integration with Other SAPs" section

# Read SAP-001 awareness guide
cat docs/skilled-awareness/inbox/AGENTS.md
# Look for "Integration with Other SAPs" section

# Read protocol spec for technical details
cat docs/skilled-awareness/task-tracking/protocol-spec.md
# Look for "Integration Patterns" section
```

**Integration Pattern**:
- SAP-001 (inbox) provides cross-repo coordination requests
- SAP-015 (beads) decomposes coordination into tasks
- Pattern: Coordination request → Epic task → Subtasks

---

### Workflow 4: Generate New SAP

**Steps**:
1. Read SAP-029 (sap-generation) adoption blueprint
2. Use SAP templates to scaffold capability
3. Fill in 5 artifacts (charter, spec, guide, blueprint, ledger)
4. Update [INDEX.md](INDEX.md) and `sap-catalog.json`
5. Validate with SAP-016 (link-validation)

**Example**:
```bash
# Navigate to SAP generation
cd docs/skilled-awareness/sap-generation/

# Read adoption blueprint
cat adoption-blueprint.md

# Use templates (follow blueprint instructions)
# ...

# Update registry
vim docs/skilled-awareness/INDEX.md
vim sap-catalog.json

# Validate links
bash scripts/validate-links.sh
```

---

## SAP Catalog Overview

### Core Infrastructure (6 SAPs)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| **SAP-000** | sap-framework | production | Foundation for all SAPs, 5-artifact pattern |
| **SAP-001** | inbox | pilot | Cross-repo coordination, broadcast workflow |
| **SAP-003** | project-bootstrap | draft | Scaffold new projects from templates |
| **SAP-004** | testing-framework | draft | pytest, coverage, fixtures |
| **SAP-005** | ci-cd-workflows | production | GitHub Actions automation |
| **SAP-006** | quality-gates | draft | pre-commit hooks, linting, type checking |

---

### Development Workflow (4 SAPs)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| **SAP-008** | automation-scripts | draft | 25 scripts, justfile tasks |
| **SAP-012** | development-lifecycle | draft | DDD→BDD→TDD workflow, 8-phase lifecycle |
| **SAP-015** | task-tracking | pilot | Persistent task memory with beads |
| **SAP-028** | publishing-automation | draft | Automated PyPI publishing |

---

### Agent Capabilities (3 SAPs)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| **SAP-009** | agent-awareness | production | This nested AGENTS.md/CLAUDE.md pattern |
| **SAP-010** | memory-system | draft | A-MEM event-sourced memory |
| **SAP-013** | metrics-tracking | draft | Process metrics, ROI calculation |

---

### Documentation & Quality (3 SAPs)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| **SAP-007** | documentation-framework | draft | Diataxis structure, frontmatter schema |
| **SAP-016** | link-validation | draft | Automated link validation |
| **SAP-027** | dogfooding-patterns | production | Validate SAP adoption |

---

### Capability Server Architecture (6 SAPs)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| **SAP-042** | interface-design | pilot | Core/interface separation, 80% coupling reduction |
| **SAP-043** | multi-interface | pilot | CLI/REST/MCP patterns, 75% time savings |
| **SAP-044** | registry | pilot | Service mesh with capability discovery |
| **SAP-045** | bootstrap | pilot | Dependency-ordered startup, 90% failure reduction |
| **SAP-046** | composition | pilot | Saga orchestration, circuit breakers, event bus |
| **SAP-047** | capability-server-template | pilot | Jinja2-based template, 5-min setup (2,271% ROI) |

---

### Technology-Specific (3 SAPs)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| **SAP-011** | docker-operations | production | Multi-stage builds, compose |
| **SAP-014** | mcp-server-development | deprecated | MCP server scaffolding (use SAP-047) |
| **SAP-029** | sap-generation | pilot | Template-based SAP generation |

---

### React Ecosystem (8 SAPs)

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| **SAP-020** | react-foundation | draft | Next.js 15, Vite 7, TypeScript |
| **SAP-021** | react-testing | draft | Vitest, Testing Library, E2E |
| **SAP-022** | react-linting | draft | ESLint 9, Prettier 3 |
| **SAP-023** | react-state-management | draft | Zustand, TanStack Query |
| **SAP-024** | react-styling | draft | Tailwind v4, CSS-in-JS |
| **SAP-025** | react-performance | draft | Core Web Vitals optimization |
| **SAP-026** | react-accessibility | planned | WCAG 2.2 AA compliance |
| **SAP-030-032** | data-fetching, routing, performance | draft | React utilities |

**Full Catalog**: See [INDEX.md](INDEX.md) or [../../sap-catalog.json](../../sap-catalog.json)

---

## SAP Status Definitions

| Status | Meaning | Recommendation |
|--------|---------|----------------|
| **production** | Battle-tested, recommended for all adopters | Adopt freely |
| **pilot** | Dogfooding phase, feedback collection | Use with caution, provide feedback |
| **draft** | Artifacts complete, limited testing | Experimental, only if needed |
| **planned** | Not yet implemented | Do not use |
| **deprecated** | Superseded by replacement | Migrate away |

---

## SAP Dependency Graph

```
SAP-000 (sap-framework) [FOUNDATIONAL]
   ↓
   ├─→ SAP-001 (inbox)
   ├─→ SAP-002 (chora-base-meta)
   ├─→ SAP-003 (project-bootstrap)
   │      ↓
   │      └─→ SAP-004 (testing-framework)
   │             ↓
   │             ├─→ SAP-005 (ci-cd-workflows)
   │             └─→ SAP-006 (quality-gates)
   ├─→ SAP-007 (documentation-framework)
   ├─→ SAP-008 (automation-scripts)
   ├─→ SAP-009 (agent-awareness)
   ├─→ SAP-010 (memory-system / A-MEM)
   ├─→ SAP-011 (docker-operations)
   ├─→ SAP-012 (development-lifecycle)
   ├─→ SAP-013 (metrics-tracking)
   ├─→ SAP-015 (task-tracking)
   ├─→ SAP-027 (dogfooding-patterns)
   ├─→ SAP-042 (interface-design)
   │      ↓
   │      ├─→ SAP-043 (multi-interface)
   │      ├─→ SAP-044 (registry)
   │      │      ↓
   │      │      └─→ SAP-045 (bootstrap)
   │      └─→ SAP-046 (composition) [depends on SAP-042, SAP-044]
   │             ↓
   │             └─→ SAP-047 (capability-server-template)
   │                    [depends on SAP-042 through SAP-046]
   └─→ SAP-029 (sap-generation)
```

**Key Dependencies**:
- **SAP-000** is foundational; all SAPs depend on it
- **SAP-003 → SAP-004**: Testing depends on project structure
- **SAP-004 → SAP-005, SAP-006**: CI/CD and quality depend on testing
- **SAP-042 → SAP-043, SAP-044, SAP-046**: Interface design is foundation for capability servers
- **SAP-047**: Capability server template integrates SAP-042 through SAP-046

---

## Integration Patterns

### Pattern 1: Inbox + Beads (Coordination → Tasks)

**SAPs**: SAP-001 (inbox) + SAP-015 (beads)

**Use Case**: Decompose coordination requests into actionable tasks

**Workflow**:
1. Receive coordination request in inbox (SAP-001)
2. Create epic task in beads (SAP-015)
3. Decompose epic into subtasks with dependencies
4. Track progress with `bd ready`, `bd close`
5. Update coordination status in inbox

**Example**:
```bash
# 1. Check inbox
cat inbox/coordination/active.jsonl | grep "coord-003"

# 2. Create epic
bd create "COORD-003: Implement feature X" --priority 0 --type epic

# 3. Create subtasks
bd create "Design API schema" --priority 0
bd create "Implement endpoints" --priority 1
bd create "Add tests" --priority 1

# 4. Add dependencies
bd dep add {implement_id} {design_id}
bd dep add {tests_id} {implement_id}

# 5. Track progress
bd ready --json
```

**See Also**:
- [inbox/AGENTS.md](inbox/AGENTS.md) for coordination patterns
- [task-tracking/AGENTS.md](task-tracking/AGENTS.md) for beads patterns

---

### Pattern 2: A-MEM + Beads (Events → Tasks)

**SAPs**: SAP-010 (A-MEM) + SAP-015 (beads)

**Use Case**: Correlate tasks with event traces for debugging

**Workflow**:
1. Include trace ID in task description
2. Log task events in A-MEM event log
3. Query A-MEM for task history
4. Cross-reference with beads task details

**Example**:
```bash
# 1. Create task with trace ID
bd create "Fix bug X" --description "Bug details\n\nTrace: trace-abc123"

# 2. Log task start event
echo '{
  "event": "task_started",
  "beads_id": "chora-base-xyz",
  "trace_id": "trace-abc123",
  "timestamp": "2025-11-04T10:00:00Z"
}' >> .chora/memory/events/development.jsonl

# 3. Work on task...

# 4. Log task complete event
echo '{
  "event": "task_completed",
  "beads_id": "chora-base-xyz",
  "trace_id": "trace-abc123",
  "timestamp": "2025-11-04T11:00:00Z"
}' >> .chora/memory/events/development.jsonl

# 5. Close task
bd close chora-base-xyz --reason "Fixed, trace: trace-abc123"
```

**See Also**:
- [memory-system/AGENTS.md](memory-system/AGENTS.md) for A-MEM patterns
- [task-tracking/AGENTS.md](task-tracking/AGENTS.md) for beads patterns

---

### Pattern 3: Agent Awareness + All SAPs (Nested Discovery)

**SAPs**: SAP-009 (agent-awareness) + all SAPs

**Use Case**: Progressive context loading for efficient navigation

**Principle**: "Nearest file wins" - agents navigate from root → domain → SAP

**Hierarchy**:
```
/CLAUDE.md                                    ← Root awareness
│
└─ docs/skilled-awareness/                    ← Domain awareness
   ├─ AGENTS.md                               ← You are reading this
   ├─ CLAUDE.md                               ← Claude-specific patterns
   │
   └─ {sap-name}/                             ← SAP-level awareness
      ├─ AGENTS.md                            ← SAP-specific patterns
      ├─ CLAUDE.md                            ← Claude-specific (optional)
      └─ ... (5 artifacts)
```

**Progressive Loading**:
- **Phase 1 (0-10k tokens)**: Read root CLAUDE.md + domain AGENTS.md
- **Phase 2 (10-50k tokens)**: Read SAP AGENTS.md + protocol-spec.md
- **Phase 3 (50-200k tokens)**: Read capability-charter.md + ledger.md

**See Also**:
- [agent-awareness/AGENTS.md](agent-awareness/AGENTS.md) for awareness patterns
- [/CLAUDE.md](../../CLAUDE.md) for root navigation

---

## Navigation Map

### By Use Case

**"I want to bootstrap a new project"**
→ [project-bootstrap/AGENTS.md](project-bootstrap/AGENTS.md)

**"I need task tracking across sessions"**
→ [task-tracking/AGENTS.md](task-tracking/AGENTS.md)

**"I want cross-repo coordination"**
→ [inbox/AGENTS.md](inbox/AGENTS.md)

**"I need event-sourced memory"**
→ [memory-system/AGENTS.md](memory-system/AGENTS.md)

**"I want to generate a new SAP"**
→ [sap-generation/AGENTS.md](sap-generation/AGENTS.md)

**"I want to validate SAP adoption"**
→ [dogfooding-patterns/AGENTS.md](dogfooding-patterns/AGENTS.md)

**"I want CI/CD automation"**
→ [ci-cd-workflows/AGENTS.md](ci-cd-workflows/AGENTS.md)

**"I want Docker containerization"**
→ [docker-operations/AGENTS.md](docker-operations/AGENTS.md)

**"I want React development patterns"**
→ [react-foundation/AGENTS.md](react-foundation/AGENTS.md)

---

### By SAP Status

**Production SAPs** (Recommend freely):
- [sap-framework/](sap-framework/)
- [agent-awareness/](agent-awareness/)
- [ci-cd-workflows/](ci-cd-workflows/)
- [docker-operations/](docker-operations/)
- [dogfooding-patterns/](dogfooding-patterns/)

**Pilot SAPs** (Use with caution):
- [inbox/](inbox/)
- [task-tracking/](task-tracking/)
- [sap-generation/](sap-generation/)

**Draft SAPs** (Experimental):
- All other SAPs (see [INDEX.md](INDEX.md))

---

### By Domain

All SAPs are located in `docs/skilled-awareness/{sap-name}/`:
- [sap-framework/](sap-framework/)
- [inbox/](inbox/)
- [chora-base/](chora-base/)
- [project-bootstrap/](project-bootstrap/)
- [testing-framework/](testing-framework/)
- [ci-cd-workflows/](ci-cd-workflows/)
- [quality-gates/](quality-gates/)
- [documentation-framework/](documentation-framework/)
- [automation-scripts/](automation-scripts/)
- [agent-awareness/](agent-awareness/)
- [memory-system/](memory-system/)
- [docker-operations/](docker-operations/)
- [development-lifecycle/](development-lifecycle/)
- [metrics-tracking/](metrics-tracking/)
- [mcp-server-development/](mcp-server-development/)
- [task-tracking/](task-tracking/)
- [link-validation-reference-management/](link-validation-reference-management/)
- [dogfooding-patterns/](dogfooding-patterns/)
- [sap-generation/](sap-generation/)
- [publishing-automation/](publishing-automation/)
- [react-foundation/](react-foundation/)
- _(and 12+ more React/utility SAPs)_

**Full Directory**: `ls docs/skilled-awareness/` to see all SAPs

---

## Troubleshooting

### Issue: Can't find a SAP

**Solution**:
```bash
# Search SAP catalog by keyword
grep -i "docker" sap-catalog.json

# List all SAP directories
ls docs/skilled-awareness/

# Check SAP index
cat docs/skilled-awareness/INDEX.md
```

---

### Issue: SAP adoption fails

**Solution**:
1. Check SAP status (draft/pilot/production)
2. Verify dependencies installed (check SAP's `adoption-blueprint.md`)
3. Run validation commands from blueprint
4. Check SAP's `ledger.md` for known issues

---

### Issue: SAP integration unclear

**Solution**:
1. Read both SAPs' `AGENTS.md` files for integration sections
2. Check `protocol-spec.md` for technical integration details
3. Search for "Integration with {SAP}" in awareness guides
4. Review integration examples in ledgers

---

## Key Commands

```bash
# Discover SAPs
cat docs/skilled-awareness/INDEX.md
grep -i "{keyword}" sap-catalog.json

# Navigate to SAP
cd docs/skilled-awareness/{sap-name}/
ls  # See 5 artifacts

# Read SAP overview
cat AGENTS.md  # or awareness-guide.md

# Read installation guide
cat adoption-blueprint.md

# Check adoption metrics
cat ledger.md
```

---

## Support & Resources

**Framework Documentation**:
- [SAP Framework (SAP-000)](sap-framework/) - Foundation for all SAPs
- [INDEX.md](INDEX.md) - Complete SAP registry
- [../../sap-catalog.json](../../sap-catalog.json) - Machine-readable catalog

**Agent Patterns**:
- [Agent Awareness (SAP-009)](agent-awareness/) - Nested awareness pattern
- [/CLAUDE.md](../../CLAUDE.md) - Root navigation for Claude

**Key SAPs**:
- [Task Tracking (SAP-015)](task-tracking/) - Persistent task memory
- [Inbox (SAP-001)](inbox/) - Cross-repo coordination
- [A-MEM (SAP-010)](memory-system/) - Event-sourced memory

---

## Version History

- **1.0.0** (2025-11-04): Initial domain AGENTS.md for skilled-awareness
  - Complete SAP catalog overview (30+ SAPs)
  - Common workflows for discovery, adoption, integration
  - Integration patterns (inbox+beads, A-MEM+beads, nested awareness)
  - Navigation map by use case, status, domain
  - Troubleshooting guide

---

**Next Steps**:
1. Browse [INDEX.md](INDEX.md) for complete SAP list
2. Navigate to specific SAP directory for details
3. Read SAP's `AGENTS.md` (or `awareness-guide.md`) for quick overview
4. Follow `adoption-blueprint.md` for installation
5. Check [CLAUDE.md](CLAUDE.md) for Claude-specific patterns
