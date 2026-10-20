# Skilled Awareness (SAP Registry) - Claude-Specific Awareness

**Domain**: Skilled Awareness Packages (SAPs)
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude-specific patterns** for navigating and adopting SAPs (Skilled Awareness Packages).

### First-Time SAP Navigation

1. Read [AGENTS.md](AGENTS.md) for generic SAP discovery patterns
2. Use this file for Claude Code-specific shortcuts
3. When adopting a SAP, read its `AGENTS.md` or `CLAUDE.md` first

### Session Resumption

- Check [INDEX.md](INDEX.md) for complete SAP list
- Navigate directly to relevant SAP directory
- Use progressive context loading (Phase 1/2/3)

---

## Progressive Context Loading for SAPs

### Phase 1: Quick Discovery (0-10k tokens)

**Goal**: Find the right SAP for the task

**Read**:
1. [AGENTS.md](AGENTS.md) - SAP catalog overview
2. Target SAP's `AGENTS.md` - Quick reference

**Example**:
```markdown
User: "I need task tracking across sessions"

Claude (Phase 1):
1. Read docs/skilled-awareness/AGENTS.md
2. Find SAP-015 (task-tracking) in catalog
3. Read docs/skilled-awareness/task-tracking/AGENTS.md
4. Understand: beads CLI, git-backed, persistent memory
```

**Output**: Know which SAP to adopt, high-level understanding

---

### Phase 2: Implementation (10-50k tokens)

**Goal**: Adopt the SAP successfully

**Read**:
1. Target SAP's `adoption-blueprint.md` - Step-by-step installation
2. Target SAP's `protocol-spec.md` - Complete technical spec

**Example**:
```markdown
Claude (Phase 2):
1. Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
2. Follow installation steps:
   - npm install -g @beads/bd
   - bd init
   - Create first tasks
3. Verify with validation commands
4. Update project AGENTS.md
```

**Output**: SAP successfully adopted and verified

---

### Phase 3: Deep Understanding (50-200k tokens)

**Goal**: Understand design rationale and integration

**Read**:
1. Target SAP's `capability-charter.md` - Problem/solution design
2. Target SAP's `ledger.md` - Adoption history, feedback
3. Related SAPs' integration patterns

**Example**:
```markdown
Claude (Phase 3 - if needed):
1. Read docs/skilled-awareness/task-tracking/capability-charter.md
   - Why beads? (session amnesia problem)
   - Why not inbox? (different use case)
2. Read ledger.md for adoption metrics
3. Read integration patterns with SAP-001 and SAP-010
```

**Output**: Complete understanding for complex integrations

---

## Claude Code Integration

### Tool Usage Patterns for SAP Adoption

**When using Read tool**:
```bash
# Phase 1: Quick discovery
Read docs/skilled-awareness/AGENTS.md
Read docs/skilled-awareness/{sap-name}/AGENTS.md

# Phase 2: Implementation
Read docs/skilled-awareness/{sap-name}/adoption-blueprint.md
Read docs/skilled-awareness/{sap-name}/protocol-spec.md

# Phase 3: Deep dive (if needed)
Read docs/skilled-awareness/{sap-name}/capability-charter.md
Read docs/skilled-awareness/{sap-name}/ledger.md
```

---

**When using Bash tool for SAP adoption**:
```bash
# Installation commands from adoption-blueprint.md
npm install -g @beads/bd
bd init
bd version

# Validation commands
bd doctor
bd validate

# Usage commands from protocol-spec.md
bd ready --json
bd create "Task title" --priority 0
bd list --status open --json
```

---

**When using Write/Edit tool for SAP integration**:
```bash
# Update project AGENTS.md with SAP patterns
Edit /path/to/AGENTS.md
# Add SAP-specific section (from SAP's AGENTS.md)

# Update project docs
Edit README.md
# Add SAP to capabilities list
```

---

### Common Claude Code Workflows

#### Workflow 1: Discover and Adopt SAP

```markdown
User: "Add task tracking to this project"

Claude:
1. Read docs/skilled-awareness/AGENTS.md (Phase 1)
2. Find SAP-015 (task-tracking)
3. Read docs/skilled-awareness/task-tracking/AGENTS.md (Phase 1)
4. Read docs/skilled-awareness/task-tracking/adoption-blueprint.md (Phase 2)
5. Execute installation via Bash tool:
   npm install -g @beads/bd
   bd init
6. Verify via Bash tool:
   bd version
   bd doctor
7. Update project AGENTS.md via Edit tool
8. Report success to user
```

**Progressive Loading**: Phase 1 → Phase 2, skip Phase 3 unless integration issues arise

---

#### Workflow 2: Integrate Two SAPs

```markdown
User: "Decompose inbox coordination into beads tasks"

Claude:
1. Read docs/skilled-awareness/inbox/AGENTS.md (Phase 1)
2. Read docs/skilled-awareness/task-tracking/AGENTS.md (Phase 1)
3. Look for "Integration with Other SAPs" sections
4. Read protocol-spec.md for both SAPs (Phase 2)
5. Implement integration pattern:
   - Create epic from coordination request
   - Decompose into subtasks
   - Link dependencies
6. Log in A-MEM if SAP-010 adopted
7. Update both SAPs' usage documentation
```

**Progressive Loading**: Phase 1 → Phase 2 for both SAPs, Phase 3 only if integration unclear

---

#### Workflow 3: Generate New SAP

```markdown
User: "Create SAP-033 for database migrations"

Claude:
1. Read docs/skilled-awareness/sap-generation/AGENTS.md (Phase 1)
2. Read docs/skilled-awareness/sap-generation/adoption-blueprint.md (Phase 2)
3. Read docs/skilled-awareness/sap-framework/protocol-spec.md (Phase 2)
4. Use SAP templates to scaffold 5 artifacts
5. Fill in SAP-033 content (charter, spec, guide, blueprint, ledger)
6. Update INDEX.md and sap-catalog.json
7. Validate with link checker
8. Commit SAP-033
```

**Progressive Loading**: Phase 1 → Phase 2, reference SAP-015 as example (Phase 3)

---

#### Workflow 4: Using Beads for Persistent Memory (SAP-015)

```markdown
User: "Continue working on the feature from yesterday"

Claude:
1. Check if SAP-015 adopted: ls .beads/
2. If yes: bd ready --json to find unblocked work
3. Read task details: bd show {id} --json
4. Update status: bd update {id} --status in_progress --assignee claude
5. Work on task, add progress comments: bd comment {id} "Status update"
6. Close when done: bd close {id} --reason "Completed X"
```

**Progressive Loading**: Phase 1 (read .beads/ dir), execute commands

**Why This Matters**: Beads eliminates session amnesia. Claude can resume exactly where left off with full task context, no user re-explanation needed.

**Key Commands**:
- `bd ready --json`: Find unblocked work (respects dependencies)
- `bd show {id} --json`: Get full task details (description, history, dependencies)
- `bd comment {id} "..."`: Add progress notes (visible to future sessions)
- `bd close {id} --reason "..."`: Complete task with closure reason

---

#### Workflow 5: Coordinating via Inbox (SAP-001)

```markdown
User: "Check if there are any coordination requests for chora-base"

Claude:
1. Check active requests: cat inbox/coordination/active.jsonl
2. Parse coordination details (sender, task, deadline, status)
3. If coordination requires work:
   - Create epic task in beads: bd create "COORD-XXX: Title" --type epic
   - Decompose into subtasks with dependencies
   - Track progress via beads
4. Update coordination status in active.jsonl
5. When complete, archive to inbox/coordination/archived.jsonl
```

**Progressive Loading**: Phase 1 (check active.jsonl), Phase 2 (read protocol-spec.md if complex)

**Why This Matters**: Inbox provides broadcast coordination across repos without tight coupling. One repo broadcasts, others respond asynchronously.

**Integration with Beads**: Inbox + Beads pattern is standard:
- Inbox: Cross-repo coordination requests
- Beads: Decompose coordination into tasks, track execution

---

#### Workflow 6: Generating Capability Servers (SAP-047)

```markdown
User: "Generate a new capability server for data analysis"

Claude:
1. Read docs/skilled-awareness/capability-server-template/AGENTS.md (Phase 1)
2. Confirm parameters with user:
   - Name: "Analyzer"
   - Namespace: "chora"
   - Enable MCP? Yes/No
   - Enable Saga? Yes/No
   - Enable circuit breaker? Yes/No
3. Execute generation script via Bash tool:
   python scripts/create-capability-server.py \
       --name "Analyzer" \
       --namespace chora \
       --description "AI code analysis service" \
       --enable-mcp \
       --enable-saga \
       --output ~/projects/analyzer
4. Verify generated structure
5. Report success to user with next steps
```

**Progressive Loading**: Phase 1 (AGENTS.md quick ref), Phase 2 (adoption-blueprint.md if issues)

**Why This Matters**: SAP-047 reduces capability server setup from 40-60 hours to 5 minutes. Template includes multi-interface support (CLI, REST, MCP), startup orchestration, composition patterns.

**Key Pattern**: Uses Jinja2-based generation (not Cookiecutter), matches chora-base's create-model-mcp-server.py pattern.

---

## Claude-Specific Tips

### Tip 1: Use JSON Output for Structured Data

Many SAP CLIs provide `--json` flags for Claude Code parsing:

```bash
# Task tracking (SAP-015)
bd ready --json
bd show {id} --json
bd list --status open --json

# Parse JSON in Claude Code for structured workflows
```

**Why**: JSON output is easier to parse programmatically than human-readable text

---

### Tip 2: Read AGENTS.md Before adoption-blueprint.md

**Pattern**:
1. Read `AGENTS.md` for quick overview (2-5 min)
2. Read `adoption-blueprint.md` for installation (10-20 min)

**Don't**:
- Jump straight to adoption-blueprint.md without context

**Why**: AGENTS.md provides "what" and "why", adoption-blueprint.md provides "how"

---

### Tip 3: Check SAP Status Before Recommending

Always verify SAP status in [sap-catalog.json](../../sap-catalog.json) before adoption:

```bash
# Check status
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep status

# Status meanings:
# - production: Recommend freely
# - pilot: Dogfooding phase, use with caution
# - draft: Experimental, only if user explicitly requests
# - deprecated: Don't recommend, suggest alternative
```

---

### Tip 4: Use Progressive Loading Aggressively

**Don't over-read**:
- User asks "what is SAP-015?" → Read `AGENTS.md` only (5 min)
- User asks "install SAP-015" → Read `AGENTS.md` + `adoption-blueprint.md` (15 min)
- User asks "why beads?" → Then read `capability-charter.md` (10 min)

**Why**: Optimize token usage, minimize read time

---

### Tip 5: Update Project AGENTS.md After Adoption

After adopting a SAP, always update project `AGENTS.md`:

```bash
# Read SAP's AGENTS.md for patterns to include
Read docs/skilled-awareness/{sap-name}/AGENTS.md

# Edit project AGENTS.md
Edit /path/to/project/AGENTS.md

# Add section like:
## Task Tracking (SAP-015)
### Quick Reference
{Copy from SAP's AGENTS.md}
```

**Why**: Agents in future sessions need to discover the SAP was adopted

---

## Common Pitfalls for Claude

### Pitfall 1: Reading All 5 Artifacts Upfront

**Problem**: Reading charter, spec, guide, blueprint, ledger for every SAP (30+ min)

**Fix**: Progressive loading
- Phase 1: `AGENTS.md` only
- Phase 2: `adoption-blueprint.md` + `protocol-spec.md`
- Phase 3 (if needed): `capability-charter.md` + `ledger.md`

---

### Pitfall 2: Not Checking SAP Dependencies

**Problem**: Adopting SAP-004 (testing) before SAP-003 (bootstrap)

**Fix**: Check dependencies in sap-catalog.json:
```bash
grep -A 10 '"id": "SAP-004"' sap-catalog.json | grep dependencies
# Output: "dependencies": ["SAP-000", "SAP-003"]
```

---

### Pitfall 3: Ignoring Integration Sections

**Problem**: Adopting SAP-015 without reading "Integration with SAP-001" section

**Fix**: Always read "Integration with Other SAPs" sections in:
- AGENTS.md
- protocol-spec.md
- awareness-guide.md

---

### Pitfall 4: Not Validating After Adoption

**Problem**: Assuming SAP adopted successfully without verification

**Fix**: Always run validation commands from adoption-blueprint.md:
```bash
bd doctor
bd validate
bd version
```

---

### Pitfall 5: Not Updating Project Documentation

**Problem**: Adopting SAP-015 but not updating project AGENTS.md

**Fix**: After adoption, update:
- Project AGENTS.md (add SAP patterns)
- README.md (add SAP to capabilities)
- .gitignore (if SAP requires it)

---

## SAP Navigation Shortcuts

### By Frequency (High → Low)

**Daily Use**:
- SAP-015 (task-tracking) - If adopted, use `bd ready` daily
- SAP-001 (inbox) - Check `inbox/coordination/active.jsonl` regularly
- SAP-009 (agent-awareness) - This pattern, use for all SAP navigation

**Weekly Use**:
- SAP-005 (ci-cd-workflows) - GitHub Actions, check on push
- SAP-027 (dogfooding-patterns) - Validate SAP adoption weekly
- SAP-010 (A-MEM) - Query event logs for debugging

**Monthly Use**:
- SAP-013 (metrics-tracking) - Monthly metrics review
- SAP-029 (sap-generation) - Generate new SAPs as needed

**One-Time Use**:
- SAP-003 (project-bootstrap) - Scaffold new project
- SAP-011 (docker-operations) - Set up Docker once
- SAP-014 (mcp-server-development) - Create MCP server once

---

### By Status (Recommend First)

**Production SAPs** (Recommend freely):
```bash
# List production SAPs
grep '"status": "production"' sap-catalog.json -B 5 | grep '"id"'
```

**Pilot SAPs** (Use with caution, collect feedback):
```bash
# List pilot SAPs
grep '"status": "pilot"' sap-catalog.json -B 5 | grep '"id"'
```

**Draft SAPs** (Experimental, only if user requests):
```bash
# List draft SAPs
grep '"status": "draft"' sap-catalog.json -B 5 | grep '"id"'
```

---

### By Category (Group Related SAPs)

**Core Infrastructure** (Adopt first):
- SAP-000 (sap-framework)
- SAP-001 (inbox)
- SAP-003 (project-bootstrap)
- SAP-004 (testing-framework)
- SAP-005 (ci-cd-workflows)

**Agent Capabilities** (Adopt for agent workflows):
- SAP-009 (agent-awareness)
- SAP-010 (memory-system)
- SAP-015 (task-tracking)

**Development Tools** (Adopt as needed):
- SAP-008 (automation-scripts)
- SAP-011 (docker-operations)
- SAP-012 (development-lifecycle)

**SAP Ecosystem** (Adopt for SAP management):
- SAP-027 (dogfooding-patterns)
- SAP-029 (sap-generation)
- SAP-028 (publishing-automation)

---

## Example Claude Code Session

```markdown
User: "Help me set up persistent task tracking for agents"

Claude (thinking):
- Task = persistent task tracking
- "agents" suggests cross-session memory
- Likely SAP-015 (task-tracking)

Claude (Phase 1: Discovery - 0-10k tokens):
1. Read docs/skilled-awareness/AGENTS.md
   - Scan "SAP Catalog Overview" section
   - Find SAP-015 (task-tracking)
2. Read docs/skilled-awareness/task-tracking/AGENTS.md
   - Understand: beads CLI, git-backed, persistent memory
   - Check "When to Use" section
3. Confirm SAP-015 matches user need

Claude (Phase 2: Implementation - 10-50k tokens):
4. Read docs/skilled-awareness/task-tracking/adoption-blueprint.md
5. Execute installation steps via Bash tool:
   npm install -g @beads/bd
   bd init
6. Create first tasks:
   bd create "Set up task tracking" --priority 0
7. Verify installation:
   bd version
   bd doctor
8. Update project AGENTS.md via Edit tool

Claude (response to user):
"I've set up SAP-015 (task-tracking) using beads v0.21.6.
You now have persistent task memory across sessions:

- bd ready --json: Find unblocked work
- bd create \"Task\": Add new task
- bd close {id}: Mark task complete

Created first task: 'Set up task tracking' (chora-base-abc123)"

Result: SAP-015 adopted, user has working task tracking
Time: 15-20 minutes (Phase 1 + Phase 2 only)
```

**Key Points**:
- Phase 1: Discovered SAP-015 in ~5 min
- Phase 2: Adopted SAP-015 in ~10-15 min
- Skipped Phase 3: Not needed for basic adoption
- Updated project docs: AGENTS.md reflects adoption

---

## Integration with Claude Desktop vs Claude Code

### Claude Code (Recommended for SAP Adoption)

**Strengths**:
- Direct file system access (Read, Write, Edit tools)
- Shell command execution (Bash tool)
- Git integration (commit SAP adoption)
- Multi-file editing (update docs, config)

**Best SAPs for Claude Code**:
- SAP-003 (project-bootstrap) - Scaffold projects
- SAP-015 (task-tracking) - Persistent memory
- SAP-005 (ci-cd-workflows) - GitHub Actions
- SAP-011 (docker-operations) - Container management

---

### Claude Desktop (Best for Exploration)

**Strengths**:
- Interactive guidance
- Exploratory conversations
- Documentation generation
- Planning and architecture

**Best SAPs for Claude Desktop**:
- SAP-009 (agent-awareness) - Navigate docs
- SAP-027 (dogfooding-patterns) - Validate adoption
- SAP-029 (sap-generation) - Generate new SAPs
- SAP-001 (inbox) - Coordinate across contexts

---

## Support & Resources

**SAP Discovery**:
- [AGENTS.md](AGENTS.md) - Complete SAP catalog
- [INDEX.md](INDEX.md) - SAP registry index
- [../../sap-catalog.json](../../sap-catalog.json) - Machine-readable catalog

**SAP Framework**:
- [sap-framework/](sap-framework/) - Foundation for all SAPs
- [sap-framework/protocol-spec.md](sap-framework/protocol-spec.md) - 5-artifact pattern

**Claude Navigation**:
- [/CLAUDE.md](../../CLAUDE.md) - Root navigation
- [agent-awareness/](agent-awareness/) - Nested awareness pattern

**Key SAPs**:
- [task-tracking/](task-tracking/) - Persistent task memory (SAP-015)
- [inbox/](inbox/) - Cross-repo coordination (SAP-001)
- [memory-system/](memory-system/) - A-MEM event history (SAP-010)
- [sap-generation/](sap-generation/) - Generate new SAPs (SAP-029)

---

## Version History

- **1.0.0** (2025-11-04): Initial domain CLAUDE.md for skilled-awareness
  - Progressive context loading strategy (Phase 1/2/3)
  - Claude Code integration patterns
  - Tool usage workflows (Read, Bash, Write/Edit)
  - Common pitfalls and shortcuts
  - Claude Desktop vs Claude Code guidance

---

**Next Steps**:
1. Use progressive loading for SAP discovery (Phase 1: AGENTS.md only)
2. Read adoption-blueprint.md when implementing (Phase 2)
3. Always check SAP status before recommending
4. Update project AGENTS.md after adoption
5. See [AGENTS.md](AGENTS.md) for generic SAP patterns
