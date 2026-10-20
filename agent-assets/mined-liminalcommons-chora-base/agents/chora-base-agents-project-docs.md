# Project Documentation - Agent Awareness

**Domain**: Project Documentation (project-docs)
**Audience**: Project managers, stakeholders, future maintainers, leadership
**Last Updated**: 2025-11-04

---

## Quick Reference

### What's in project-docs?

This domain contains **living project management artifacts** generated/updated during project lifecycle:

- **sprints/**: Sprint plans, retrospectives, velocity tracking
- **releases/**: Release notes, plans, post-mortems, upgrade guides
- **plans/**: Strategic plans and roadmaps
- **metrics/**: Quality metrics, process metrics, ROI calculations
- **integration/**: Integration plans, coordination documents
- **inventory/**: Repository audits, coherence reports, gap analyses
- **audits/**: Comprehensive audits and assessments
- **dogfooding-pilot/**: SAP dogfooding experiments and results
- **archives/**: Historical project artifacts

### When to Use This Domain

**Use project-docs when**:
- Planning sprints or releases
- Tracking project progress
- Documenting decisions and rationale
- Coordinating work across teams
- Auditing project structure

**Don't use project-docs for**:
- Development processes → See [../dev-docs/](../dev-docs/)
- End-user guides → See [../user-docs/](../user-docs/)
- SAP documentation → See [../skilled-awareness/](../skilled-awareness/)

---

## Common Workflows

### Workflow 1: Starting a New Sprint

**Steps**:
1. Navigate to [sprints/](sprints/) directory
2. Review previous sprint retrospectives for context
3. Create new sprint plan (see templates in static-template/project-docs/sprints/)
4. Define sprint goals, committed work, success criteria
5. Track progress during sprint execution

**Example**:
```bash
# 1. Navigate to sprints
cd docs/project-docs/sprints/

# 2. Review previous sprint
cat wave-1-sprint-plan.md

# 3. Create new sprint plan
vim sprint-{number}-plan.md

# 4. Use template from static-template
cat ../../static-template/project-docs/sprints/sprint-template.md

# 5. Track progress
vim sprint-{number}-progress.md
```

---

### Workflow 2: Planning a Release

**Steps**:
1. Navigate to [releases/](releases/) directory
2. Review previous release notes for format
3. Create release plan document
4. Track release blockers and progress
5. Write release notes when shipping

**Example**:
```bash
# 1. Navigate to releases
cd docs/project-docs/releases/

# 2. Review previous releases
ls v*.md
cat v4.1.0-release-notes.md

# 3. Create release plan
vim v4.10.0-release-plan.md

# 4. Track blockers
vim v4.10.0-blockers.md

# 5. Write release notes
vim v4.10.0-release-notes.md
```

---

### Workflow 3: Creating Strategic Plans

**Steps**:
1. Navigate to [plans/](plans/) directory
2. Review existing strategic plans for context
3. Create new plan document (e.g., PLAN-YYYY-MM-DD-{name}.md)
4. Define goals, phases, deliverables, timeline
5. Track plan execution progress

**Example (SAP-009 Full Adoption Plan)**:
```bash
# 1. Navigate to plans
cd docs/project-docs/plans/

# 2. Review existing plans
ls PLAN-*.md

# 3. Create new plan
vim PLAN-2025-11-04-SAP-009-FULL.md

# 4. Define structure
# - Executive Summary
# - Phases 1-N
# - Execution Strategy
# - Success Metrics
# - Risk Mitigation

# 5. Track execution
# Update plan with progress notes
```

---

### Workflow 4: Sprint Planning with Beads (SAP-015)

**Steps**:
1. Review backlog: `bd list --status open --priority 0,1 --json`
2. Create sprint epic: `bd create "Sprint N: Goals" --type epic --priority 0`
3. Decompose into tasks with estimated effort
4. Add task dependencies: `bd dep add {dependent_id} {prerequisite_id}`
5. Track sprint progress: `bd ready --json` (shows unblocked work)
6. Sprint retrospective: Review closed tasks, update velocity

**Example**:
```bash
# 1. Review backlog
bd list --status open --priority 0,1 --json
# Output: 15 high-priority tasks

# 2. Create sprint epic
bd create "Sprint 5: SAP-042 Capability Server Architecture" \
    --type epic \
    --priority 0 \
    --description "Implement core/interface separation patterns"

# 3. Decompose into tasks
bd create "Design interface contracts" --priority 0 --parent {epic_id}
bd create "Implement core logic" --priority 0 --parent {epic_id}
bd create "Create integration tests" --priority 1 --parent {epic_id}
bd create "Update documentation" --priority 1 --parent {epic_id}

# 4. Add dependencies
bd dep add {implement_id} {design_id}       # Core depends on design
bd dep add {tests_id} {implement_id}        # Tests depend on implementation
bd dep add {docs_id} {tests_id}             # Docs depend on tests passing

# 5. Track sprint progress daily
bd ready --json
# Shows only unblocked tasks (respects dependencies)

# 6. Sprint retrospective
bd list --status closed --updated-after "2025-11-05" --json
# Review: 12/15 tasks completed, 3 rolled to next sprint
```

**Why Use Beads for Sprints**:
- Dependency management: Ensures tasks are done in correct order
- Progress visibility: `bd ready` shows what's unblocked now
- Historical tracking: Velocity calculated from closed tasks
- Cross-session memory: Sprint context preserved between planning sessions

**Integration with Sprint Documents**:
```bash
# Link sprint plan to beads epic
vim docs/project-docs/sprints/sprint-5-plan.md
# Add: "Epic ID: chora-base-xyz"

# Reference beads tasks in sprint retrospective
bd list --status closed --parent {epic_id} --json > sprint-5-completed.json
```

---

### Workflow 5: Coordinate Cross-Repo Work with Inbox (SAP-001)

**Steps**:
1. Check active coordination requests: `cat inbox/coordination/active.jsonl`
2. Triage coordination: Assign priority, estimate effort
3. Decompose into beads tasks (SAP-015 integration)
4. Track progress via beads: `bd ready --json`
5. Update coordination status in active.jsonl
6. Archive completed coordination: Move to `archived.jsonl`

**Example**:
```bash
# 1. Check active requests
cat inbox/coordination/active.jsonl
# Output: COORD-2025-003: v1.9.0 docs update (overdue)

# 2. Triage coordination
# Priority: P1 (overdue)
# Effort: 2-3 hours
# Assignee: Documentation team

# 3. Decompose into beads tasks
bd create "COORD-2025-003: v1.9.0 Docs Update" \
    --type epic \
    --priority 1 \
    --description "Update chora-compose documentation for v1.9.0 release"

bd create "Review v1.9.0 changelog" --priority 1 --parent {epic_id}
bd create "Update API docs" --priority 1 --parent {epic_id}
bd create "Update migration guide" --priority 1 --parent {epic_id}
bd create "Review and merge PR" --priority 1 --parent {epic_id}

# 4. Track progress
bd ready --json  # Shows unblocked COORD-2025-003 tasks

# 5. Update coordination status
vim inbox/coordination/active.jsonl
# Change: "status": "in_progress"
# Add: "beads_epic": "chora-base-xyz"

# 6. Archive when complete
# (Move entry from active.jsonl to archived.jsonl)
```

**Why Integrate Inbox + Beads**:
- **Inbox**: Broadcast coordination requests across repos (decoupled)
- **Beads**: Decompose coordination into actionable tasks with dependencies
- **Pattern**: Coordination epic → Task breakdown → Dependency tracking → Progress updates

**Coordination Protocol (SAP-001)**:
- Sender broadcasts coordination request to `inbox/coordination/active.jsonl`
- Receiver creates beads epic from coordination
- Receiver tracks progress via beads, updates coordination status
- When complete, receiver archives coordination request

---

### Workflow 6: Auditing Project Structure

**Steps**:
1. Navigate to [audits/](audits/) or [inventory/](inventory/) directory
2. Review existing audit reports for format
3. Conduct audit (e.g., SAP coverage, link validation, coherence)
4. Document findings and recommendations
5. Track remediation actions

**Example**:
```bash
# 1. Navigate to audits
cd docs/project-docs/audits/

# 2. Review existing audits
ls *.md

# 3. Conduct new audit
bash scripts/audit-{capability}.sh > audit-{capability}-{date}.md

# 4. Document findings
vim audit-{capability}-{date}.md

# 5. Track remediation
vim audits/remediation-tracker.md
```

---

## Directory Structure

```
docs/project-docs/
├── AGENTS.md                                  ← You are here
├── CLAUDE.md                                  ← Claude-specific patterns
├── README.md                                  ← Domain overview
│
├── sprints/                                   ← Sprint artifacts
│   ├── wave-1-sprint-plan.md                  ← Wave 1 plan
│   └── ... (7 sprint plans)
│
├── releases/                                  ← Release management
│   ├── v4.1.0-release-notes.md                ← Release notes
│   └── ... (10 release artifacts)
│
├── plans/                                     ← Strategic plans
│   ├── sap-009-full-adoption-plan.md          ← SAP-009 adoption (Phase 1-6)
│   └── ... (strategic planning docs)
│
├── metrics/                                   ← Quality & process metrics
│   └── ... (metrics dashboards)
│
├── integration/                               ← Integration coordination
│   └── ... (integration plans)
│
├── inventory/                                 ← Repository audits
│   ├── COHERENCE_REPORT.md                    ← 100% coherence achievement
│   └── ... (11 inventory docs)
│
├── audits/                                    ← Comprehensive audits
│   ├── wave-2-sap-awareness-integration-audit.md
│   └── ... (17 audit reports)
│
├── dogfooding-pilot/                          ← SAP dogfooding
│   └── ... (11 pilot experiments)
│
├── archives/                                  ← Historical artifacts
│   └── ... (deprecated coordination, archived plans)
│
└── Root files:
    ├── CHORA-BASE-4.0-VISION.md               ← v4.0 transformation roadmap
    ├── DOCUMENTATION_PLAN.md                  ← Documentation strategy
    ├── v4-cleanup-manifest.md                 ← Cleanup tracking
    ├── gap-003-*-summary.md                   ← Gap analysis summaries
    ├── phase-1-execution-summary.md           ← Phase execution summary
    ├── wave-*-summary.md                      ← Wave execution summaries
    └── ... (27 project artifacts)
```

---

## Key Files

### Strategic Planning

**[CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md)**
- v4.0 transformation roadmap
- 4-wave execution plan
- Strategic goals and success criteria

**[plans/sap-009-full-adoption-plan.md](plans/sap-009-full-adoption-plan.md)**
- SAP-009 full adoption plan (Phase 1-6)
- 40-56 hours core work + 19-27 hours optional
- Comprehensive awareness file creation + SAP enhancements

**[DOCUMENTATION_PLAN.md](DOCUMENTATION_PLAN.md)**
- Documentation strategy
- 4-domain model (user-docs, dev-docs, project-docs, skilled-awareness)
- Diataxis framework application

---

### Sprint Management

**[sprints/wave-1-sprint-plan.md](sprints/wave-1-sprint-plan.md)**
- Wave 1 execution plan
- Sprint goals and committed work
- Success criteria

**Template**: See [../../static-template/project-docs/sprints/sprint-template.md](../../static-template/project-docs/sprints/sprint-template.md)

---

### Release Management

**[releases/](releases/)**
- Release notes (v2.x, v3.x, v4.x)
- Release plans
- Post-mortems
- Upgrade guides

**Recent Releases**:
- v4.1.0: MIT License addition
- v3.3.0: MCP server development capability
- v3.2.0: Link validation & reference management

---

### Audits & Inventory

**[inventory/COHERENCE_REPORT.md](inventory/COHERENCE_REPORT.md)**
- 100% coherence achievement
- Repository structure validation
- SAP coverage analysis

**[audits/](audits/)**
- Comprehensive audits (17 reports)
- SAP awareness integration audits
- Link validation audits
- Gap analyses

---

### Metrics & Tracking

**[metrics/](metrics/)**
- Quality metrics (coverage, linting, type checking)
- Process metrics (sprint velocity, adherence)
- ROI calculations (ClaudeROICalculator)

**Template**: See [../../static-template/project-docs/metrics/](../../static-template/project-docs/metrics/)

---

### Integration & Coordination

**[integration/](integration/)**
- Integration plans (v3.2.0, v3.3.0)
- Cross-team coordination documents
- Dependency tracking

---

## Characteristics

### Living Documents
- **Updated continuously**: Sprint plans, metrics, tracking docs
- **Evolve with project**: Release notes, integration plans
- **Reflect current state**: Audits, inventory reports

### Historical Record
- **Permanent**: Sprint retrospectives, release notes, audits
- **Context for future**: Integration plans, decision rationale
- **Learning repository**: Retrospectives, post-mortems

### Stakeholder-Facing
- **Communicates value**: Release notes, metrics dashboards
- **Coordinates work**: Integration plans, sprint plans
- **Demonstrates ROI**: Quality metrics, process adherence

### Generated Artifacts
- **Created during execution**: Not written upfront
- **Reflect actual work**: Sprint retrospectives capture real learnings
- **Timestamp decisions**: Audits and plans dated for context

---

## Navigation Map

### By Task

**"I'm starting a sprint"**
→ Read [sprints/](sprints/) for previous sprint context
→ Create new sprint plan using template

**"I'm planning a release"**
→ Read [releases/](releases/) for previous release format
→ Create release plan and track blockers

**"I need strategic direction"**
→ Read [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md)
→ Check [plans/](plans/) for execution plans

**"I want to audit the project"**
→ Check [audits/](audits/) for existing audits
→ Review [inventory/](inventory/) for structure reports

**"I need project metrics"**
→ Check [metrics/](metrics/) for dashboards
→ Review sprint retrospectives for velocity

**"I want historical context"**
→ Browse [releases/](releases/) for version history
→ Check [archives/](archives/) for deprecated artifacts
→ Read [../../CHANGELOG.md](../../CHANGELOG.md) for changes

---

### By Phase

**Vision & Strategy**:
- [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md)
- [plans/](plans/)

**Sprint Execution**:
- [sprints/](sprints/)
- [metrics/](metrics/)

**Release Management**:
- [releases/](releases/)
- [../../CHANGELOG.md](../../CHANGELOG.md)

**Quality Assurance**:
- [audits/](audits/)
- [inventory/](inventory/)

**Coordination**:
- [integration/](integration/)
- [dogfooding-pilot/](dogfooding-pilot/)

**Historical**:
- [archives/](archives/)

---

## Integration with Other Domains

### With user-docs/

**Relationship**: project-docs tracks project execution, user-docs provides product capabilities

**Example**:
- user-docs: "How to bootstrap a project" (capability)
- project-docs: "Sprint 3: Implement bootstrap feature" (execution)

---

### With dev-docs/

**Relationship**: project-docs uses processes from dev-docs

**Example**:
- dev-docs: "TDD workflow process" (how to develop)
- project-docs: "Sprint 3: Used TDD for SAP-015" (what we did)

---

### With skilled-awareness/

**Relationship**: project-docs tracks SAP adoption and evolution

**Example**:
- skilled-awareness: "SAP-015 ledger" (capability adoption tracking)
- project-docs: "Sprint 3: Adopted SAP-015" (project execution tracking)

---

## Troubleshooting

### Issue: Can't find project artifact

**Solution**:
```bash
# Search by keyword
grep -r "{keyword}" docs/project-docs/

# List recent files
ls -lt docs/project-docs/ | head -20

# Check archives
ls docs/project-docs/archives/
```

---

### Issue: Need sprint context

**Solution**:
```bash
# List all sprints
ls docs/project-docs/sprints/

# Read recent sprint plan
cat docs/project-docs/sprints/wave-1-sprint-plan.md

# Check sprint retrospectives
grep -r "retrospective" docs/project-docs/sprints/
```

---

### Issue: Release information unclear

**Solution**:
```bash
# List releases
ls docs/project-docs/releases/

# Check CHANGELOG
cat CHANGELOG.md

# Find specific release
grep -r "v4.1" docs/project-docs/releases/
```

---

## Key Commands

```bash
# Sprint management
ls docs/project-docs/sprints/
cat docs/project-docs/sprints/wave-1-sprint-plan.md

# Release management
ls docs/project-docs/releases/
cat CHANGELOG.md

# Strategic planning
cat docs/project-docs/CHORA-BASE-4.0-VISION.md
ls docs/project-docs/plans/

# Audits & inventory
ls docs/project-docs/audits/
cat docs/project-docs/inventory/COHERENCE_REPORT.md

# Metrics
ls docs/project-docs/metrics/

# Search artifacts
grep -r "{keyword}" docs/project-docs/
```

---

## Support & Resources

**Strategic Planning**:
- [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md) - Roadmap
- [plans/](plans/) - Strategic plans
- [DOCUMENTATION_PLAN.md](DOCUMENTATION_PLAN.md) - Doc strategy

**Execution Tracking**:
- [sprints/](sprints/) - Sprint artifacts (7 plans)
- [metrics/](metrics/) - Quality & process metrics
- [releases/](releases/) - Release management (10 artifacts)

**Quality Assurance**:
- [audits/](audits/) - Comprehensive audits (17 reports)
- [inventory/](inventory/) - Structure audits (11 docs)
- [dogfooding-pilot/](dogfooding-pilot/) - SAP pilots (11 experiments)

**Coordination**:
- [integration/](integration/) - Integration plans
- [../../CHANGELOG.md](../../CHANGELOG.md) - Version history
- [../../ROADMAP.md](../../ROADMAP.md) - Product roadmap

**Templates**:
- [../../static-template/project-docs/sprints/](../../static-template/project-docs/sprints/) - Sprint templates
- [../../static-template/project-docs/metrics/](../../static-template/project-docs/metrics/) - Metrics templates

**Related Domains**:
- [../dev-docs/](../dev-docs/) - Development processes
- [../user-docs/](../user-docs/) - End-user documentation
- [../skilled-awareness/](../skilled-awareness/) - SAP capabilities

**Claude-Specific**:
- [CLAUDE.md](CLAUDE.md) - Claude patterns for project docs
- [/CLAUDE.md](../../CLAUDE.md) - Root navigation

---

## Meta-Demonstration

Chora-base **dogfoods** its own project-docs/ structure:

- **Wave 1**: [sprints/wave-1-sprint-plan.md](sprints/wave-1-sprint-plan.md)
- **Vision**: [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md)
- **Cleanup**: [v4-cleanup-manifest.md](v4-cleanup-manifest.md)
- **Audits**: [audits/](audits/) (17 comprehensive audits)
- **SAP-009 Plan**: [plans/sap-009-full-adoption-plan.md](plans/sap-009-full-adoption-plan.md)

This demonstrates chora-base using its own patterns for project management.

---

## Version History

- **1.0.0** (2025-11-04): Initial domain AGENTS.md for project-docs
  - Project artifact navigation
  - Sprint, release, planning workflows
  - Integration with other domains
  - Meta-demonstration of dogfooding

---

**Next Steps**:
1. Check [plans/](plans/) for strategic direction (e.g., SAP-009 full adoption)
2. Read [sprints/](sprints/) for execution context
3. Browse [releases/](releases/) for version history
4. Review [audits/](audits/) for quality assurance
5. Read [CLAUDE.md](CLAUDE.md) for Claude-specific project doc patterns
