---
sap_id: SAP-002
version: 1.0.0
status: active
last_updated: 2025-11-05
type: comprehensive_guide
audience: all_agents
complexity: intermediate
estimated_reading_time: 52
progressive_loading:
  phase_1: "lines 1-200"
  phase_2: "lines 201-500"
  phase_3: "full"
phase_1_token_estimate: 5000
phase_2_token_estimate: 7500
phase_3_token_estimate: 7000
tags:
  - meta
  - chora-base
  - template
  - sap-framework
  - production
---

# Agent Awareness Guide: chora-base Template Repository

**SAP ID**: SAP-002
**Capability**: chora-base (Meta-SAP - Self-Description)
**Version**: 1.0.0
**Audience**: All AI agents (Claude Code, Claude Desktop, custom agents)

---

## Progressive Loading

```yaml
phase_1_quick_reference:
  lines: 1-200
  tokens: ~5k
  use_when: "Quick lookup of chora-base structure and capabilities"

phase_2_implementation:
  lines: 200-500
  tokens: ~12k
  use_when: "Generating projects, installing SAPs, working with chora-base"

phase_3_deep_understanding:
  lines: 500-end
  tokens: ~20k
  use_when: "Understanding architecture, contributing to chora-base, ecosystem integration"
```

---

## 📖 Quick Reference

**New to SAP-002?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 4 commands for meta-information and structure verification
- 🏗️ **Architecture** - Three-layer model (template → generated projects → ecosystem)
- 📂 **SAP Categories** - 32+ SAPs organized by function (foundation, workflow, React, meta)
- 🎓 **Progressive Loading** - Token-optimized context loading strategy (60-70% savings)
- 🔍 **Dogfooding Demo** - How SAP-002 proves SAP framework expressiveness

**This AGENTS.md provides**: Deep agent patterns for navigating the chora-base ecosystem, generating projects, and adopting SAPs.

---

## 1. What is chora-base?

**chora-base** is a comprehensive template repository and SAP framework for AI-agent-first development. It provides:

- **30 Skilled Awareness Packages (SAPs)**: Modular capabilities for development workflows
- **Template System**: Generate production-ready Python/TypeScript/React projects
- **Agent Infrastructure**: Nested awareness pattern (AGENTS.md/CLAUDE.md), progressive context loading
- **Coordination System**: Cross-repo inbox (SAP-001), event memory (SAP-010), task tracking (SAP-015)
- **Quality Gates**: CI/CD workflows (SAP-005), testing (SAP-004), linting, security

**Core Guarantee**: Every capability is packaged as a SAP with 5 standardized artifacts (Charter, Protocol, Awareness, Blueprint, Ledger).

---

## 2. User Signal Pattern Table

### Generic User Intents → Agent Actions

| User Signal | User Intent | Agent Action | Tools/Commands |
|-------------|-------------|--------------|----------------|
| "Use chora-base for my project" | Want to scaffold new project from chora-base template | Read protocol-spec.md (Section 3-4), run setup.py or copy static-template/, install selected SAPs | `python setup.py` or `cp -r static-template/ {target}/` |
| "What capabilities does chora-base have?" | Want inventory of all SAPs | Read INDEX.md or protocol-spec.md Section 3 (14 capabilities) | Read INDEX.md lines 25-62 |
| "How do I adopt SAP-X?" | Want to install specific SAP capability | Navigate to SAP directory, read adoption-blueprint.md, follow installation steps | Read docs/skilled-awareness/{sap-name}/adoption-blueprint.md |
| "Show me chora-base architecture" | Want to understand how chora-base works | Read protocol-spec.md Section 2 (architecture), capability-charter.md Section 2 | Read protocol-spec.md lines 20-200 |
| "How does chora-base relate to meta/governance?" | Want to understand chora-base ecosystem | Read protocol-spec.md Section 7 (ecosystem), capability-charter.md Section 6 | Read protocol-spec.md lines 400-500 |
| "What version of chora-base should I use?" | Want version guidance and upgrade path | Read ledger.md Section 2 (version history), CHANGELOG.md | Read ledger.md lines 23-50 |

### Bidirectional Translation (Agent → User Communication)

| Agent Observation | Interpretation | Communication to User |
|-------------------|----------------|----------------------|
| User reading root CLAUDE.md or AGENTS.md | Orienting to chora-base project structure | "You're looking at chora-base, a template for AI-assisted development with 30 SAPs. What would you like to do? (scaffold project / adopt SAP / understand architecture / contribute)" |
| User browsing docs/skilled-awareness/ | Exploring SAP capabilities | "You're in the SAP directory. There are 30 capabilities available. Popular ones: SAP-015 (task-tracking), SAP-005 (ci-cd), SAP-020-025 (React ecosystem). What are you working on?" |
| User asking "how to use chora-base" without specifics | Unclear intent (scaffold? adopt SAP? understand?) | "I can help with: (1) Scaffolding a new project, (2) Adopting a specific SAP capability, (3) Understanding chora-base architecture, (4) Contributing to chora-base. Which interests you?" |
| User has empty directory, asks "setup chora-base" | Wants to scaffold new project | "I'll help scaffold a new project from chora-base. What's your project name? (I'll use setup.py or static-template/)" |

---

## 3. Common Workflows

### Workflow 1: Scaffold New Project from chora-base Template

**Time Estimate**: 15-30 minutes
**Scope**: Implementation
**Prerequisites**: None (chora-base is foundational)

**Steps**:

1. **Choose Generation Method**:
   - **Option A**: Blueprint-based generation (custom setup.py, zero dependencies)
   - **Option B**: Static template copy (simpler, manual substitution)

2. **Option A: Blueprint-Based Generation** (recommended for Python projects):
   ```bash
   # Clone chora-base
   git clone https://github.com/liminalcommons/chora-base.git
   cd chora-base

   # Run generator
   python setup.py
   # Follow prompts:
   #   - Project name (e.g., "my-app")
   #   - Author name
   #   - Include optional features (Inbox SAP-001, Docker, CI/CD)

   # Generated project at ../my-app/
   cd ../my-app
   ```

3. **Option B: Static Template Copy** (recommended for React/TypeScript projects):
   ```bash
   # Copy template
   cp -r chora-base/static-template/ my-app/
   cd my-app

   # Manual substitution (replace placeholders):
   #   - {{project_name}} → my-app
   #   - {{author}} → Your Name
   #   - {{package_name}} → my_app (Python) or myApp (TypeScript)

   # Initialize git
   git init
   git add .
   git commit -m "Initial commit from chora-base template"
   ```

4. **Verify Project Structure**:
   ```
   my-app/
   ├── CLAUDE.md                    # Root awareness file
   ├── AGENTS.md                    # Agent guidance
   ├── README.md                    # Project overview
   ├── pyproject.toml               # Python dependencies (if Python)
   ├── package.json                 # npm dependencies (if TypeScript/React)
   ├── src/                         # Source code
   ├── tests/                       # Test suite
   ├── .github/workflows/           # CI/CD (if SAP-005 adopted)
   ├── docs/                        # Documentation
   └── inbox/                       # Coordination (if SAP-001 adopted)
   ```

5. **Select SAPs to Adopt** (optional but recommended):
   - **Core**: SAP-004 (testing), SAP-005 (ci-cd), SAP-007 (docs)
   - **Development**: SAP-015 (task-tracking), SAP-010 (memory), SAP-008 (automation)
   - **React**: SAP-020-025 (React ecosystem if frontend project)

6. **Install Selected SAPs**:
   - For each SAP, navigate to `docs/skilled-awareness/{sap-name}/adoption-blueprint.md`
   - Follow installation steps (usually: copy files, run commands, update configs)

**Success Criteria**:
- ✅ Project directory created with chora-base structure
- ✅ Git repository initialized
- ✅ Dependencies installable (`pip install -e .` or `npm install`)
- ✅ Tests runnable (`pytest` or `npm test`)
- ✅ AGENTS.md/CLAUDE.md present for agent awareness

---

### Workflow 2: Adopt Specific SAP Capability

**Time Estimate**: 30-60 minutes (varies by SAP complexity)
**Scope**: Implementation
**Prerequisites**: Existing project (chora-base or compatible structure)

**Steps**:

1. **Identify SAP by Need**:
   - Read [INDEX.md](INDEX.md) for full SAP catalog (30 capabilities)
   - Common scenarios:
     - **Task tracking?** → SAP-015 (beads persistent task system)
     - **CI/CD?** → SAP-005 (GitHub Actions workflows)
     - **React project?** → SAP-020 (foundation), SAP-021 (testing), SAP-022 (linting)
     - **Cross-repo coordination?** → SAP-001 (inbox)
     - **Event memory?** → SAP-010 (A-MEM)

2. **Navigate to SAP Directory**:
   ```bash
   cd docs/skilled-awareness/{sap-name}/
   ls
   # Expected files:
   #   - capability-charter.md    (problem/solution)
   #   - protocol-spec.md         (technical specification)
   #   - awareness-guide.md       (or AGENTS.md - agent patterns)
   #   - adoption-blueprint.md    (installation guide)
   #   - ledger.md                (adoption tracking)
   ```

3. **Read Adoption Blueprint**:
   ```bash
   # Quick scan: Read adoption-blueprint.md
   # Focus on:
   #   - Prerequisites (dependencies, existing SAPs)
   #   - Installation steps (sequential, agent-executable)
   #   - Validation commands (ensure successful installation)
   #   - Post-install verification
   ```

4. **Follow Installation Steps** (example: SAP-015 beads task tracking):
   ```bash
   # Step 1: Install CLI
   npm install -g @beads/bd

   # Step 2: Initialize
   bd init
   # Creates:
   #   - .beads/config.yaml
   #   - .beads/issues.jsonl (git-tracked source of truth)
   #   - .beads/beads.db (gitignored SQLite cache)

   # Step 3: Create first task
   bd create "Setup CI/CD pipeline" --priority high --status open

   # Step 4: Verify
   bd list --status open --json
   ```

5. **Update Project Awareness Files**:
   - Add SAP to project `AGENTS.md`:
     ```markdown
     ## Adopted SAPs

     - **SAP-015** (task-tracking): Persistent task memory with beads
       - CLI: `bd` (create, list, update, close tasks)
       - Storage: `.beads/issues.jsonl` (git-committed)
       - Agent workflow: `bd ready --json` to find unblocked work
     ```

   - Add SAP to project `CLAUDE.md` (if Claude-specific patterns):
     ```markdown
     ### SAP-015 (beads) Usage

     **Finding work**:
     ```bash
     bd ready --json  # Unblocked tasks
     ```

     **Claiming task**:
     ```bash
     bd update {id} --status in_progress --assignee me
     ```
     ```

6. **Record Adoption in Ledger**:
   - Open `docs/skilled-awareness/{sap-name}/ledger.md`
   - Add adoption entry (optional, helps track ROI):
     ```markdown
     ## Adoption Entry

     **Project**: my-app
     **Date**: 2025-11-05
     **Time to Install**: 42 minutes
     **Selected Features**: Core beads + GitHub issue sync
     **Notes**: Smooth installation, immediately useful for multi-session work
     ```

**Success Criteria**:
- ✅ SAP capabilities functional (run validation commands from adoption-blueprint.md)
- ✅ Project AGENTS.md updated with SAP patterns
- ✅ Tests pass (if SAP includes tests)
- ✅ CI/CD passes (if applicable)

---

### Workflow 3: Understand chora-base Architecture

**Time Estimate**: 30-45 minutes
**Scope**: Planning
**Prerequisites**: None

**Steps**:

1. **Read Root Awareness Files**:
   - Start: `CLAUDE.md` (root) for navigation map
   - Then: `AGENTS.md` (root) for quick reference
   - Lines 1-100 of each for orientation

2. **Read Architecture Documentation**:
   - `capability-charter.md` (this SAP-002):
     - Lines 1-80: Problem statement (why chora-base exists)
     - Lines 80-150: Solution design (meta-reflexive SAP framework)
   - `protocol-spec.md` (this SAP-002):
     - Lines 20-60: Repository structure, generation architecture
     - Lines 60-400: All 14 capabilities (SAP-000 through SAP-013 + Wave 2/3/4)

3. **Explore SAP Framework** (foundational):
   - Navigate to `docs/skilled-awareness/sap-framework/`
   - Read `protocol-spec.md`:
     - Section 2: 5-artifact structure (Charter, Protocol, Awareness, Blueprint, Ledger)
     - Section 3: Scope levels (Vision & Strategy, Planning, Implementation)
     - Section 5: Agent execution patterns

4. **Review SAP Catalog**:
   - Read `INDEX.md` for complete inventory (30 SAPs)
   - Group by domain:
     - **Meta**: SAP-000 (framework), SAP-002 (chora-base), SAP-009 (awareness)
     - **Core Infrastructure**: SAP-001 (inbox), SAP-010 (memory), SAP-015 (tasks)
     - **Development**: SAP-004 (testing), SAP-005 (ci-cd), SAP-006 (quality gates)
     - **React**: SAP-020-025 (foundation, testing, linting, state, styling, performance)
     - **Ecosystem**: SAP-027 (dogfooding), SAP-029 (sap-generation)

5. **Understand Nested Awareness Pattern** (SAP-009):
   - Read `docs/skilled-awareness/agent-awareness/protocol-spec.md`
   - Key concepts:
     - **5-level hierarchy**: Root → Domain → Capability → Feature → Component
     - **AGENTS.md/CLAUDE.md**: Generic vs Claude-specific patterns
     - **Progressive loading**: Phase 1 (quick) → Phase 2 (impl) → Phase 3 (deep)
     - **"Nearest file wins"**: Navigate progressively, load context as needed

**Success Criteria**:
- ✅ Understand what chora-base is (template + SAP framework)
- ✅ Know where to find capabilities (docs/skilled-awareness/)
- ✅ Can navigate SAP structure (5 artifacts per SAP)
- ✅ Understand awareness pattern (AGENTS.md/CLAUDE.md hierarchy)

---

### Workflow 4: Contribute to chora-base

**Time Estimate**: 2-4 hours (for new SAP contribution)
**Scope**: Implementation
**Prerequisites**: Understanding of SAP framework (Workflow 3), Git/GitHub

**Steps**:

1. **Identify Contribution Type**:
   - **New SAP**: Propose new capability (e.g., SAP-031 routing-navigation)
   - **SAP Enhancement**: Improve existing SAP (add features, fix bugs)
   - **Documentation**: Update awareness files, fix broken links
   - **Template**: Improve static-template/, blueprints/, setup.py

2. **For New SAP Contribution**:

   a. **Check SAP Catalog** (avoid duplicates):
      ```bash
      grep -r "capability-name" docs/skilled-awareness/INDEX.md
      ```

   b. **Use SAP Generation** (SAP-029):
      ```bash
      # If SAP-029 adopted:
      python scripts/generate-sap.py \
        --id SAP-031 \
        --name routing-navigation \
        --status draft \
        --description "Next.js App Router and navigation patterns"

      # Generates:
      #   docs/skilled-awareness/routing-navigation/
      #   ├── capability-charter.md (template)
      #   ├── protocol-spec.md (template)
      #   ├── awareness-guide.md (template)
      #   ├── adoption-blueprint.md (template)
      #   └── ledger.md (template)
      ```

   c. **Fill Out 5 Artifacts** (see SAP-000 protocol-spec.md for requirements):
      - **Capability Charter**: Problem statement, solution design, success criteria
      - **Protocol Spec**: Complete technical specification, commands, APIs
      - **Awareness Guide**: Agent operating patterns (rename to AGENTS.md)
      - **Adoption Blueprint**: Step-by-step installation guide
      - **Ledger**: Adoption tracking structure (empty initially)

   d. **Create Awareness Files** (SAP-009 Phase 1):
      - `AGENTS.md`: 5 workflows (generic, all agents)
      - `CLAUDE.md`: 3 workflows (Claude-specific tool patterns)
      - Add self-evaluation section to protocol-spec.md

3. **For SAP Enhancement**:

   a. **Navigate to SAP directory**:
      ```bash
      cd docs/skilled-awareness/{sap-name}/
      ```

   b. **Update relevant artifact**:
      - Bug fix → Update protocol-spec.md + adoption-blueprint.md
      - New feature → Update capability-charter.md + protocol-spec.md + awareness-guide.md
      - Improved guidance → Update awareness-guide.md (or AGENTS.md/CLAUDE.md)

   c. **Update version** in all 5 artifacts (MAJOR.MINOR.PATCH):
      - MAJOR: Breaking changes
      - MINOR: New features (backward compatible)
      - PATCH: Bug fixes

   d. **Record in ledger.md** (Section 2: Version History):
      ```markdown
      | 1.1.0 | 2025-11-05 | MINOR | Added GitHub issue sync | N (backward compatible) |
      ```

4. **Validate Changes**:
   ```bash
   # Run link validation
   bash scripts/validate-awareness-links.sh

   # Run SAP evaluator (if SAP-019 adopted)
   python scripts/sap-evaluator.py --sap {sap-name}

   # Ensure no broken links or missing files
   ```

5. **Create Pull Request**:
   ```bash
   git checkout -b feat/sap-031-routing-navigation
   git add docs/skilled-awareness/routing-navigation/
   git commit -m "feat(sap-031): Add routing-navigation SAP for Next.js App Router"
   git push -u origin feat/sap-031-routing-navigation

   # Create PR on GitHub
   gh pr create --title "feat(sap-031): Add routing-navigation SAP" \
     --body "$(cat <<'EOF'
   ## Summary
   - New SAP-031 (routing-navigation) for Next.js App Router patterns
   - All 5 artifacts complete (Charter, Protocol, Awareness, Blueprint, Ledger)
   - Phase 1 awareness files (AGENTS.md, CLAUDE.md)

   ## Validation
   - ✅ Link validation passed
   - ✅ SAP evaluator passed (equivalent support)
   - ✅ Self-evaluation criteria documented

   Generated with Claude Code
   EOF
   )"
   ```

6. **Respond to Review Feedback**:
   - Address reviewer comments
   - Update artifacts as needed
   - Re-run validation scripts

**Success Criteria**:
- ✅ All 5 SAP artifacts present (if new SAP)
- ✅ Awareness files created (AGENTS.md, CLAUDE.md for Phase 1)
- ✅ Link validation passes
- ✅ SAP evaluator passes (if applicable)
- ✅ PR approved and merged

---

### Workflow 5: Navigate chora-base Ecosystem

**Time Estimate**: 20-30 minutes
**Scope**: Planning
**Prerequisites**: Basic understanding of chora-base (Workflow 3)

**Steps**:

1. **Understand Ecosystem Structure**:
   - **chora-base** (this repo): Template + 30 SAPs + coordination infrastructure
   - **Related Repositories** (if applicable):
     - `chora-meta`: Meta-level governance, cross-repo coordination
     - `chora-governance`: Decision records, RFCs, architectural decisions
     - `ecosystem-manifest`: Multi-repo status dashboard

2. **Check Ecosystem Status**:
   ```bash
   # If SAP-001 (inbox) adopted:
   cat inbox/ECOSYSTEM_STATUS.yaml
   # Shows:
   #   - Active repos
   #   - Broadcast subscriptions
   #   - Capability status
   ```

3. **Cross-Repo Coordination** (if working across multiple repos):

   a. **Create Coordination Request** (SAP-001):
      ```bash
      # Example: Requesting "Add dark mode support" across 3 repos
      cat > inbox/incoming/coordination/COORD-2025-XXX.json <<EOF
      {
        "id": "COORD-2025-XXX",
        "title": "Add Dark Mode Support",
        "description": "Implement dark mode across chora-base, chora-meta, documentation",
        "requester": "my-app",
        "targets": ["chora-base", "chora-meta", "docs"],
        "deadline": "2025-12-01",
        "priority": "medium"
      }
      EOF
      ```

   b. **Broadcast to Ecosystem** (if coordinator):
      ```bash
      # Notify all subscribed repos
      python scripts/broadcast-coordination.py --id COORD-2025-XXX
      ```

4. **Track Multi-Repo Work** (SAP-015 + SAP-001):
   ```bash
   # Create tasks across repos
   bd create "chora-base: Add dark mode toggle to AGENTS.md" --repo chora-base
   bd create "chora-meta: Update governance docs for dark mode" --repo chora-meta
   bd create "docs: Add dark mode examples" --repo docs

   # Link to coordination request
   bd update {id} --metadata '{"coord_id": "COORD-2025-XXX"}'
   ```

5. **Sync Status**:
   ```bash
   # Update ECOSYSTEM_STATUS.yaml (manual or automated)
   # Show completion:
   #   chora-base: ✅ Dark mode added
   #   chora-meta: 🟡 In progress
   #   docs: ⏳ Not started
   ```

**Success Criteria**:
- ✅ Understand chora-base's role in larger ecosystem
- ✅ Can create coordination requests (if SAP-001 adopted)
- ✅ Can track multi-repo work (if SAP-015 adopted)

---

## 4. Best Practices

### 1. **Always Start with Root CLAUDE.md**

When navigating chora-base for the first time, read `/CLAUDE.md` (root) for the complete navigation tree. It explains:
- What chora-base is
- Where to find documentation (4 domains: user, dev, project, SAPs)
- Progressive loading strategy (Phase 1 → 2 → 3)
- Domain-level CLAUDE.md files for specialized guidance

**Why**: Saves 10-20k tokens by avoiding over-reading. CLAUDE.md is optimized for quick orientation.

---

### 2. **Use Progressive Loading**

Don't read entire SAP protocol-spec.md (often 500-1000 lines) unless implementing. Instead:
- **Quick question?** Read AGENTS.md only (~200-300 lines)
- **Implementation?** Read protocol-spec.md Section 4-6 (commands, workflows)
- **Design rationale?** Read capability-charter.md Section 2 (solution design)

**Why**: Reduces token usage 3-5x, faster response times.

---

### 3. **Check SAP Status Before Recommending**

Always verify SAP status in INDEX.md before recommending to users:
- **production**: Battle-tested, recommend freely
- **pilot**: Dogfooding phase, use with caution, mention experimental status
- **draft**: Early stage, only recommend if user explicitly requests bleeding edge
- **deprecated**: Don't recommend, suggest alternatives

**Example**:
```bash
# Check SAP-015 status
grep "SAP-015" docs/skilled-awareness/INDEX.md
# | SAP-015 | task-tracking | 1.0.0 | Pilot | ...
# → Status: Pilot (mention this to user)
```

**Why**: Sets correct expectations, avoids recommending unstable capabilities.

---

### 4. **Update Awareness Files When Adopting SAPs**

After installing a SAP, ALWAYS update your project's `AGENTS.md` with:
- SAP ID and name
- Key commands/workflows
- Agent-specific patterns
- Integration points with other SAPs

**Example**:
```markdown
## Adopted SAPs

### SAP-015 (task-tracking)
**CLI**: `bd` (beads task tracker)
**Storage**: `.beads/issues.jsonl` (git-committed)

**Agent Workflow**:
1. Find work: `bd ready --json`
2. Claim task: `bd update {id} --status in_progress --assignee me`
3. Complete: `bd close {id} --reason "Done"`
```

**Why**: Enables agents to use SAP capabilities without re-reading adoption docs.

---

### 5. **Validate Links After Editing Awareness Files**

After creating or updating AGENTS.md/CLAUDE.md, always run link validation:

```bash
bash scripts/validate-awareness-links.sh
```

**Why**: Broken links degrade agent experience. Validation catches issues before commit.

---

## 5. Common Pitfalls

### 1. **Reading All 5 SAP Artifacts for Simple Questions**

**Problem**: User asks "What is SAP-015?", agent reads all 5 files (2000+ lines, 50k+ tokens).

**Fix**: Read AGENTS.md only (~300 lines, 7k tokens) for quick questions. Only read protocol-spec.md when implementing.

**Example**:
```
User: "What is SAP-015?"
❌ Bad: Read capability-charter.md + protocol-spec.md + awareness-guide.md + adoption-blueprint.md + ledger.md
✅ Good: Read AGENTS.md (lines 1-50 for summary)
```

---

### 2. **Recommending Draft SAPs as Production-Ready**

**Problem**: Agent recommends SAP-031 (status: draft) without mentioning it's experimental.

**Fix**: Always check `status` field in INDEX.md. Mention status to user:
- "SAP-031 is in draft status, meaning it's experimental. I can help you adopt it, but expect changes."

**Why**: Users need to know stability level before investing time.

---

### 3. **Not Using Beads for Multi-Session Work**

**Problem**: Agent loses context between sessions, user has to re-explain task.

**Fix**: If SAP-015 adopted, ALWAYS use beads for tasks spanning multiple sessions:

```bash
# Session 1: Create task
bd create "Implement dark mode toggle" --status open --priority high

# Session 2 (next day): Find work
bd ready --json  # Shows "Implement dark mode toggle"
bd show {id}     # Full context from task description
```

**Why**: Persistent task memory eliminates context re-establishment overhead (saves 5-10 minutes per session).

---

### 4. **Breaking Awareness File Link Networks**

**Problem**: Creating AGENTS.md with broken links to non-existent files.

**Fix**: After creating awareness files, run validation:

```bash
bash scripts/validate-awareness-links.sh
# Fix any BROKEN links before committing
```

**Why**: Broken links degrade agent navigation. Validation ensures link network integrity.

---

### 5. **Ignoring SAP Dependencies**

**Problem**: Installing SAP-021 (react-testing) without SAP-020 (react-foundation) causes missing dependencies.

**Fix**: Always check `Dependencies` column in INDEX.md before installing:

```markdown
| SAP-021 | react-testing | ... | SAP-000, SAP-004, SAP-020 |
```

Install dependencies first: SAP-000 → SAP-020 → SAP-021.

**Why**: SAPs may depend on files, configs, or patterns from other SAPs.

---

## 6. Integration with Other SAPs

### SAP-000 (sap-framework)

**Relationship**: SAP-002 dogfoods SAP-000 by describing chora-base using SAP framework.

**Integration**:
- All chora-base capabilities packaged as SAPs
- Follows 5-artifact structure (Charter, Protocol, Awareness, Blueprint, Ledger)
- Uses scope levels (Vision & Strategy, Planning, Implementation)

**Agent Pattern**:
- When explaining chora-base structure, reference SAP-000 protocol-spec.md Section 2 (5 artifacts)
- When creating new SAPs, use SAP-000 templates

---

### SAP-001 (inbox-coordination)

**Relationship**: chora-base includes inbox/ infrastructure for cross-repo coordination.

**Integration**:
- `inbox/` directory structure in static-template/
- JSON schemas in schemas/ (coordination-request.json, broadcast.json)
- ECOSYSTEM_STATUS.yaml for multi-repo dashboards

**Agent Pattern**:
- If project has `inbox/`, assume SAP-001 adopted
- Use coordination requests for multi-repo work
- Check `inbox/coordination/active.jsonl` for active coordination

---

### SAP-009 (agent-awareness)

**Relationship**: chora-base uses nested awareness pattern throughout.

**Integration**:
- Root CLAUDE.md/AGENTS.md for project-level navigation
- Domain CLAUDE.md/AGENTS.md (docs/skilled-awareness/, docs/dev-docs/, etc.)
- SAP-level AGENTS.md/CLAUDE.md for capability-specific patterns

**Agent Pattern**:
- Follow "nearest file wins" rule: Root → Domain → Capability → Feature → Component
- Use progressive loading: Phase 1 (quick) → Phase 2 (impl) → Phase 3 (deep)
- Read domain CLAUDE.md after navigating to new domain

---

### SAP-010 (memory-system)

**Relationship**: chora-base includes event memory infrastructure (A-MEM).

**Integration**:
- `.chora/memory/events/*.jsonl` for event-sourced history
- Event schemas for development, inbox, testing

**Agent Pattern**:
- If `.chora/memory/` exists, assume SAP-010 adopted
- Log significant events (SAP adoption, feature completion, bugs)
- Use event correlation for debugging

---

### SAP-015 (task-tracking)

**Relationship**: chora-base can adopt beads for persistent task memory.

**Integration**:
- `.beads/` directory with config.yaml, issues.jsonl, beads.db
- `bd` CLI for task management
- Integration with SAP-001 (coordination requests → beads tasks)

**Agent Pattern**:
- If `.beads/` exists, assume SAP-015 adopted
- Use `bd ready --json` to find work at session start
- Create beads tasks for multi-step work
- Link tasks to coordination requests (metadata: coord_id)

---

### SAP-020 through SAP-025 (React Ecosystem)

**Relationship**: chora-base includes comprehensive React SAPs for frontend projects.

**Integration**:
- SAP-020 (foundation): Next.js 15, Vite 7 templates
- SAP-021 (testing): Vitest, RTL, MSW setup
- SAP-022 (linting): ESLint 9, Prettier 3
- SAP-023 (state): TanStack Query, Zustand, React Hook Form
- SAP-024 (styling): Tailwind v4, shadcn/ui
- SAP-025 (performance): Core Web Vitals, Lighthouse CI

**Agent Pattern**:
- For React projects, recommend adopting SAP-020 first (foundation)
- Then layer on SAP-021-025 based on needs
- All React SAPs depend on SAP-020

---

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-05 | Initial AGENTS.md for SAP-002 (chora-base meta-SAP) - 5 workflows: scaffold project, adopt SAP, understand architecture, contribute, navigate ecosystem |

---

**Next Steps**:
1. **New to chora-base?** Start with Workflow 1 (Scaffold Project)
2. **Need specific capability?** Start with Workflow 2 (Adopt SAP)
3. **Want to understand how it works?** Start with Workflow 3 (Architecture)
4. **Want to contribute?** Start with Workflow 4 (Contribute)

**Questions?** Check root CLAUDE.md for navigation guidance, or read SAP protocol-spec.md for complete technical details.
