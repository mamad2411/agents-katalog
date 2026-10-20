# Project Documentation - Claude-Specific Awareness

**Domain**: Project Documentation (project-docs)
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude-specific patterns** for managing project artifacts and plans.

### First-Time Project Navigation

1. Read [AGENTS.md](AGENTS.md) for generic project patterns
2. Use this file for Claude Code integration patterns
3. Navigate sprints, releases, plans, audits effectively

### Session Resumption

- Check [plans/](plans/) for strategic direction
- Read [sprints/](sprints/) for execution context
- Review [audits/](audits/) for quality status

---

## Progressive Context Loading for Project Docs

### Phase 1: Strategic Context (0-10k tokens)

**Goal**: Understand project direction and current phase

**Read**:
1. [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md) - Strategic roadmap
2. [plans/](plans/) - Current execution plan
3. Recent sprint plan from [sprints/](sprints/)

**Example**:
```markdown
User: "What's the current project status?"

Claude (Phase 1):
1. Read docs/project-docs/CHORA-BASE-4.0-VISION.md
   - Understand v4.0 transformation plan
2. ls docs/project-docs/plans/
   - Find latest plan
3. Read latest sprint plan
   - Understand current work

Result: Claude knows project phase and priorities
```

---

### Phase 2: Detailed Planning (10-50k tokens)

**Goal**: Execute or update specific project artifact

**Read**:
1. Relevant plan, sprint, or release document
2. Related artifacts (audits, metrics, inventory)
3. Templates from static-template if creating new artifact

**Example**:
```markdown
User: "Create sprint plan for Phase 2 of SAP-009 adoption"

Claude (Phase 2):
1. Read docs/project-docs/plans/sap-009-full-adoption-plan.md
   - Understand Phase 2 scope
2. Read static-template/project-docs/sprints/sprint-template.md
   - Get sprint plan structure
3. Create new sprint plan
4. Populate from Phase 2 deliverables

Result: Sprint plan created for Phase 2
```

---

### Phase 3: Historical Analysis (50-200k tokens)

**Goal**: Understand project evolution and decisions

**Read**:
1. Multiple sprint retrospectives
2. Release notes and post-mortems
3. Audit reports and inventory
4. Git history for additional context

**Example**:
```markdown
User: "Why did we adopt this architecture?"

Claude (Phase 3):
1. Read docs/project-docs/audits/*.md
   - Find architecture audits
2. Read docs/project-docs/releases/v*.md
   - See evolution over versions
3. Read docs/ARCHITECTURE.md
   - Current architecture rationale
4. git log --grep="architecture"
   - Git history for decisions

Result: Comprehensive historical context
```

---

## Claude Code Tool Usage for Project Docs

### Using Read Tool

**Pattern**: Navigate project artifacts efficiently

```bash
# Strategic planning
Read docs/project-docs/CHORA-BASE-4.0-VISION.md
Read docs/project-docs/plans/sap-009-full-adoption-plan.md

# Sprint management
Read docs/project-docs/sprints/wave-1-sprint-plan.md
ls docs/project-docs/sprints/  # List all sprints

# Release management
Read docs/project-docs/releases/v4.1.0-release-notes.md
Read CHANGELOG.md

# Quality assurance
Read docs/project-docs/audits/wave-2-sap-awareness-integration-audit.md
Read docs/project-docs/inventory/COHERENCE_REPORT.md

# Metrics
Read docs/project-docs/metrics/{metric}.md
```

**Why**: Project docs are living artifacts, read for current state

---

### Using Write Tool

**Pattern**: Create new project artifacts

```bash
# New sprint plan
Write docs/project-docs/sprints/sprint-{number}-plan.md
# Content from template + current goals

# New release plan
Write docs/project-docs/releases/v{version}-release-plan.md
# Content: features, timeline, blockers

# New strategic plan
Write docs/project-docs/plans/PLAN-{date}-{name}.md
# Content: goals, phases, deliverables

# New audit report
Write docs/project-docs/audits/audit-{capability}-{date}.md
# Content: findings, recommendations
```

**Why**: Project docs are generated during execution, not upfront

---

### Using Edit Tool

**Pattern**: Update living documents during execution

```bash
# Update sprint progress
Edit docs/project-docs/sprints/sprint-{number}-plan.md
# old_string: "Status: In Progress"
# new_string: "Status: Complete"

# Update release notes
Edit docs/project-docs/releases/v{version}-release-notes.md
# Add new features as shipped

# Update plan execution status
Edit docs/project-docs/plans/PLAN-{date}-{name}.md
# Update phase completion status
```

**Why**: Living documents evolve as work progresses

---

### Using Bash Tool

**Pattern**: Generate reports, search history, git operations

```bash
# Generate audit reports
bash scripts/audit-{capability}.sh > docs/project-docs/audits/audit-{date}.md

# Search project history
grep -r "{keyword}" docs/project-docs/

# Git operations
git log --oneline --grep="{sprint}"
git log --all --since="2024-10-01"

# Create release
gh release create v4.10.0 --title "..." --notes "$(cat <<'EOF'
...release notes...
EOF
)"
```

**Why**: Bash tool executes commands, generates reports

---

## Claude-Specific Project Management Tips

### Tip 1: Always Read Strategic Plan First

**Pattern**:
```markdown
User: "Start working on X"

Claude:
1. Read docs/project-docs/CHORA-BASE-4.0-VISION.md
2. Read docs/project-docs/plans/{current-plan}.md
3. Understand: Is X aligned with strategic direction?
4. Proceed if aligned
```

**Why**: Avoid working on out-of-scope tasks

---

### Tip 2: Update Plans as You Work

**Pattern**:
```bash
# After completing phase deliverable
Edit docs/project-docs/plans/{plan}.md
# Update: "Phase 1: ⏳ Pending" → "Phase 1: ✅ Complete"
```

**Why**: Plans are living documents, reflect reality

---

### Tip 3: Create Sprint Plans from Strategic Plans

**Pattern**:
```markdown
User: "Plan Sprint 5"

Claude:
1. Read docs/project-docs/plans/sap-009-full-adoption-plan.md
   - Extract Phase 2 deliverables
2. Read static-template/project-docs/sprints/sprint-template.md
3. Create sprint-5-plan.md with Phase 2 scope

Result: Sprint plan aligned with strategic plan
```

**Why**: Sprints execute strategic plans, should align

---

### Tip 4: Document Decisions in Multiple Places

**Pattern**:
```bash
# After making architectural decision
1. Write docs/project-docs/plans/{plan}.md (strategic context)
2. Write docs/dev-docs/research/{decision}.md (technical rationale)
3. Update docs/ARCHITECTURE.md (architecture impact)
```

**Why**: Different audiences need different perspectives

---

### Tip 5: Use Audits to Drive Plans

**Pattern**:
```markdown
User: "What should we work on next?"

Claude:
1. Read docs/project-docs/audits/*.md
   - Find gaps and issues
2. Read docs/project-docs/inventory/COHERENCE_REPORT.md
   - Find structural issues
3. Create plan to address findings
4. Prioritize by impact

Result: Plan driven by quality data
```

**Why**: Audits identify real problems, plans fix them

---

## Common Pitfalls for Claude Managing Projects

### Pitfall 1: Not Updating Plans During Execution

**Problem**: Plan says "Pending" but work is done

**Fix**:
```bash
# After completing deliverable
Edit docs/project-docs/plans/{plan}.md
# Update status: Pending → In Progress → Complete
```

---

### Pitfall 2: Creating Artifacts Without Templates

**Problem**: Sprint plan missing sections or inconsistent format

**Fix**:
```bash
# Always use template
Read static-template/project-docs/sprints/sprint-template.md
# Then create sprint plan with all sections
```

---

### Pitfall 3: Not Linking Related Artifacts

**Problem**: Sprint plan doesn't reference strategic plan

**Fix**:
```markdown
# In sprint plan, add:
**Related Plans**:
- [SAP-009 Full Adoption Plan](plans/sap-009-full-adoption-plan.md)
- [Wave 1 Sprint Plan](sprints/wave-1-sprint-plan.md)
```

---

### Pitfall 4: Not Running Audits Before Planning

**Problem**: Planning without knowing current state

**Fix**:
```bash
# Before planning, audit current state
bash scripts/audit-{capability}.sh
Read docs/project-docs/inventory/COHERENCE_REPORT.md
# Then create plan based on findings
```

---

### Pitfall 5: Not Documenting Sprint Retrospectives

**Problem**: Completing sprint without capturing learnings

**Fix**:
```bash
# At sprint end
Write docs/project-docs/sprints/sprint-{number}-retrospective.md
# Content: What went well, what didn't, improvements
```

---

## Example Claude Code Session (Project Management)

```markdown
User: "Plan Phase 2 execution for SAP-009 adoption"

Claude (thinking):
- User wants sprint planning (project-docs domain)
- Need strategic plan context
- Need sprint template

Claude (Phase 1: Strategic Context - 0-10k tokens):
1. Read docs/project-docs/plans/sap-009-full-adoption-plan.md
   - Understand Phase 2 scope (8-11 hours, P0 SAP enhancements)
2. Read docs/project-docs/CHORA-BASE-4.0-VISION.md
   - Confirm alignment with v4.0 strategy

Claude (Phase 2: Create Sprint Plan - 10-50k tokens):
3. Read static-template/project-docs/sprints/sprint-template.md
4. Create sprint plan:
   Write docs/project-docs/sprints/sprint-6-sap-009-phase-2.md
   # Content:
   # - Sprint Goals: Complete P0 SAP enhancements
   # - Scope: SAP-027, SAP-029, SAP-028
   # - Success Criteria: 3 SAPs enhanced, 8-11 hours
   # - Timeline: 1 week
5. Link to strategic plan
6. Add success metrics

Claude (response):
"I've created Sprint 6 plan for SAP-009 Phase 2:

**Sprint Goals**:
- Enhance 3 P0 SAPs (SAP-027, SAP-029, SAP-028)
- Add AGENTS.md + CLAUDE.md + ledger TODOs

**Scope**:
- SAP-027 (dogfooding-patterns): 3-4h ⭐ HIGHEST PRIORITY
- SAP-029 (sap-generation): 3-4h
- SAP-028 (publishing-automation): 2-3h

**Total Effort**: 8-11 hours
**Timeline**: 1 week
**Success Criteria**: All 3 SAPs enhanced, validated with link checker

Ready to begin execution?"

User: "Yes, start with SAP-027"

Claude:
1. Read docs/skilled-awareness/dogfooding-patterns/protocol-spec.md
2. Create docs/skilled-awareness/dogfooding-patterns/AGENTS.md
3. Create docs/skilled-awareness/dogfooding-patterns/CLAUDE.md
4. Update ledger TODOs
5. Validate with link checker
6. Update sprint plan: SAP-027 ✅ Complete

Result: Sprint planned, execution started, tracked
Time: 30 min planning + execution time
```

---

## Support & Resources

**Strategic Planning**:
- [CHORA-BASE-4.0-VISION.md](CHORA-BASE-4.0-VISION.md) - Roadmap
- [plans/](plans/) - Strategic plans (e.g., SAP-009 adoption)
- [DOCUMENTATION_PLAN.md](DOCUMENTATION_PLAN.md) - Doc strategy

**Execution Tracking**:
- [sprints/](sprints/) - Sprint artifacts (7 plans)
- [metrics/](metrics/) - Quality & process metrics
- [releases/](releases/) - Release management (10 artifacts)

**Quality Assurance**:
- [audits/](audits/) - Comprehensive audits (17 reports)
- [inventory/](inventory/) - Structure audits (11 docs)
- [dogfooding-pilot/](dogfooding-pilot/) - SAP pilots (11 experiments)

**Templates**:
- [../../static-template/project-docs/sprints/](../../static-template/project-docs/sprints/) - Sprint templates
- [../../static-template/project-docs/metrics/](../../static-template/project-docs/metrics/) - Metrics templates

**Related Domains**:
- [../dev-docs/](../dev-docs/) - Development processes
- [../user-docs/](../user-docs/) - End-user documentation
- [../skilled-awareness/](../skilled-awareness/) - SAP capabilities

**Navigation**:
- [AGENTS.md](AGENTS.md) - Generic project patterns
- [/CLAUDE.md](../../CLAUDE.md) - Root navigation

---

## Version History

- **1.0.0** (2025-11-04): Initial domain CLAUDE.md for project-docs
  - Progressive context loading for project management
  - Tool usage patterns (Read, Write, Edit, Bash)
  - Sprint, release, planning workflows
  - Common pitfalls and tips
  - Example project management session

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic project patterns
2. Check [plans/](plans/) for strategic direction
3. Use [sprints/](sprints/) for execution tracking
4. Run audits before planning
5. Update plans as you work (living documents)
