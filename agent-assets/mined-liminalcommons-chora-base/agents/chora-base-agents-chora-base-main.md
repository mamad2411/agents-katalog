---
nested_structure: true
nested_files:
  - "saps/AGENTS.md"
  - "workflows/AGENTS.md"
  - "getting-started/AGENTS.md"
  - "scripts/AGENTS.md"
version: 2.0.0
last_updated: 2025-11-12
---

# AGENTS.md - chora-base Template Repository

**Purpose**: Machine-readable instructions for AI agents working on the chora-base template repository.

**Last Updated**: 2025-11-10 (Nested awareness pattern v2.1.0)

---

## ⚠️ Critical Workflows (Read This First!)

**These workflows are frequently missed by agents. Read carefully before proceeding.**

### 1. Fast-Setup Script Usage ⚠️ MOST IMPORTANT

**When**: User says "help me with chora-base" or "set up chora-base"

**Common Mistake**: Agents try to `pip install` or "set up" chora-base itself.

**Correct Action**: chora-base is a TEMPLATE SOURCE, not a project to set up.

```bash
# ✅ CORRECT: Generate new project from template
python scripts/create-capability-server.py \
    --name "Your Project Name" \
    --namespace yournamespace \
    --output ~/projects/your-project

# ❌ WRONG: Try to set up chora-base
# pip install -e .          # NO!
# ./scripts/setup.sh        # NO!
# pytest                    # NO! (unless developing chora-base itself)
```

**Quick Reference**:
- User wants new project → Use fast-setup script
- User contributing to template → Continue reading this file

**Full Details**: [getting-started/AGENTS.md](getting-started/AGENTS.md#-critical-chora-base-is-a-template-source)

---

### 2. Cross-Platform Compatibility ⚠️ REQUIRED

**When**: Writing Python scripts or shell commands

**Common Mistake**: Using Unix-specific commands (`rm`, `/`, `\n`) that fail on Windows.

**Correct Action**: Follow cross-platform patterns.

```python
# ✅ CORRECT: Cross-platform file operations
from pathlib import Path
import shutil

file_path = Path("docs") / "example.md"  # Works on all platforms
shutil.rmtree(Path("temp"))              # Works on all platforms

# ❌ WRONG: Unix-specific operations
import os
os.system("rm -rf temp")                 # Fails on Windows
file_path = "docs/example.md"            # May fail on Windows
```

**Quick Reference**:
- Use `Path` from `pathlib` for file operations
- Use `shutil` for file/directory operations
- NO `os.system()` with shell commands
- Read [scripts/AGENTS.md](scripts/AGENTS.md) before writing scripts

**Full Details**: [scripts/AGENTS.md](scripts/AGENTS.md#cross-platform-requirements)

---

### 3. Pre-commit Hooks (Quality Gates) ⚠️ BEFORE EVERY COMMIT

**When**: Before `git commit`

**Common Mistake**: Committing without running quality gates, causing CI failures.

**Correct Action**: Run quality gates locally first.

```bash
# ✅ CORRECT: Run quality gates before commit
pre-commit run --all-files        # Or: just pre-commit-all
just pre-merge                    # Runs test + lint + format + type-check

# If hooks fail → Fix issues → Re-run → Then commit
ruff check --fix src/
mypy src/
git add .
git commit -m "feat: Add feature"

# ❌ WRONG: Skip quality gates
git commit -m "feat: Add feature" --no-verify  # Only for emergencies!
```

**Quick Reference**:
- ALWAYS run `just pre-merge` before committing
- Pre-commit hooks catch 95%+ preventable issues locally (saves 5-10 min CI cycle)
- Only use `--no-verify` for true emergencies

**Full Details**: [workflows/AGENTS.md](workflows/AGENTS.md#quality-gates-sap-006)

---

### 4. SAP Installation Process ⚠️ MULTI-STEP

**When**: User asks to "install SAP-XXX" or "adopt capability"

**Common Mistake**: Incomplete installation (missing steps, no validation, no ledger update).

**Correct Action**: Follow complete 5-step process.

```bash
# Step 1: Read adoption blueprint
cat docs/skilled-awareness/<sap-name>/adoption-blueprint.md

# Step 2: Execute installation steps (from blueprint)
# ... follow blueprint instructions sequentially ...

# Step 3: Run validation commands
# ... validation from blueprint ...

# Step 4: Update ledger.md
vim docs/skilled-awareness/<sap-name>/ledger.md
# Add adopter entry

# Step 5: Update project AGENTS.md with new patterns
vim AGENTS.md  # Or relevant nested AGENTS.md
```

**Quick Reference**:
- Installation is NOT just copying files
- ALWAYS validate after installation
- ALWAYS update ledger.md
- ALWAYS update project awareness files

**Full Details**: [saps/AGENTS.md](saps/AGENTS.md#installing-saps) + [getting-started/AGENTS.md](getting-started/AGENTS.md#installing-saps)

---

### 5. Release Version Process ⚠️ 6-STEP WORKFLOW

**When**: User says "release new version" or "publish vX.Y.Z"

**Common Mistake**: Missing upgrade guide, incorrect CHANGELOG, forgetting tags.

**Correct Action**: Follow complete 6-step release process.

```bash
# Step 1: Pre-release validation
cd /tmp/test-release && ./scripts/setup.sh && pytest

# Step 2: Create upgrade guide
cp docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md docs/upgrades/vX.Y-to-vX.Z.md
vim docs/upgrades/vX.Y-to-vX.Z.md

# Step 3: Update core files
vim CHANGELOG.md      # Change [Unreleased] to [X.Y.Z] - 2025-MM-DD
vim README.md         # Add version to Recent Updates

# Step 4: Commit and tag
git add -A
git commit -m "feat(scope): Brief description (vX.Y.Z)"
git tag vX.Y.Z
git push origin main --tags

# Step 5: Create GitHub release
gh release create vX.Y.Z --title "vX.Y.Z - Title" --notes "..."

# Step 6: Update upgrade docs index
vim docs/upgrades/README.md
```

**Quick Reference**:
- Release is NOT just `git tag`
- ALWAYS create upgrade guide first
- ALWAYS update CHANGELOG + README
- ALWAYS create GitHub release

**Full Details**: [workflows/AGENTS.md](workflows/AGENTS.md#releasing-new-version)

---

## 🔴 CROSS-PLATFORM REMINDER

**ALL code MUST work on Windows, Mac, and Linux without modification.**

Before writing Python scripts, read: [scripts/AGENTS.md](scripts/AGENTS.md) for cross-platform patterns.

**Quick Template**: Copy [templates/cross-platform/python-script-template.py](templates/cross-platform/python-script-template.py)

**Validation**: `python scripts/validate-windows-compat.py --file your-script.py`

---

## Project Overview

**chora-base** is a blueprint-driven Python project template designed for LLM-intelligent development. It generates production-ready Python projects with built-in support for AI coding agents, comprehensive documentation, and quality gates.

### Key Facts

- **Repository Type**: Template repository (generates other projects, NOT a project itself)
- **Primary Users**: Human developers and AI agents generating/maintaining Python projects
- **Technology Stack**: Static scaffolding (`static-template/`), Skilled Awareness Packages (SAPs)
- **Current Version**: v5.1.0 (see [CHANGELOG.md](CHANGELOG.md))
- **SAP Count**: 45 capabilities (see [saps/AGENTS.md](saps/AGENTS.md))

### Key Concepts

- **Template vs Generated Project**: chora-base is the template; generated projects are adopters
- **Blueprint Generation**: `.blueprint` files define project scaffolding workflows
- **Static Assets**: `static-template/` contains ready-to-copy files
- **Skilled Awareness Packages (SAPs)**: 30+ modular capabilities with 5 artifacts each
- **Nested Awareness Pattern**: Progressive context loading via domain-specific AGENTS.md files

---

## Nested Awareness Structure

**chora-base uses a nested awareness pattern (SAP-009 v2.1.0) for progressive context loading.**

### Navigation Tree

```
/AGENTS.md (you are here) - Root navigation + critical workflows
│
├─ getting-started/AGENTS.md     - Onboarding guide for new contributors
├─ saps/AGENTS.md                - SAP catalog and quick references (45 SAPs)
├─ workflows/AGENTS.md           - Development processes and automation
├─ scripts/AGENTS.md             - Script patterns and cross-platform requirements
│
└─ docs/                         - Domain-specific documentation
   ├─ skilled-awareness/         - SAP capabilities (45 SAPs)
   │  ├─ AGENTS.md               - SAP catalog and adoption patterns
   │  ├─ CLAUDE.md               - Claude-specific SAP navigation
   │  └─ {sap-name}/             - Individual SAP directories
   │     ├─ AGENTS.md            - SAP-specific patterns
   │     ├─ capability-charter.md
   │     ├─ protocol-spec.md
   │     ├─ adoption-blueprint.md
   │     └─ ledger.md
   │
   ├─ dev-docs/                  - Developer documentation
   │  ├─ AGENTS.md               - Development patterns
   │  ├─ CLAUDE.md               - Claude development workflows
   │  └─ ... (architecture, contributing, etc.)
   │
   ├─ user-docs/                 - User-facing documentation
   │  ├─ AGENTS.md               - User guidance patterns
   │  ├─ CLAUDE.md               - Claude user support
   │  └─ ... (getting started, tutorials, reference)
   │
   └─ project-docs/              - Project management
      ├─ AGENTS.md               - Project coordination patterns
      ├─ CLAUDE.md               - Claude project navigation
      └─ ... (plans, decisions, retrospectives)
```

**Principle**: "Nearest file wins" - navigate from root → domain → capability → feature, progressively loading context as needed.

### When to Use Each File

**Use [getting-started/AGENTS.md](getting-started/AGENTS.md) when**:
- User is new to chora-base
- User wants to create project from template (fast-setup)
- User wants to understand SAP structure
- User asks "how do I start?"

**Use [saps/AGENTS.md](saps/AGENTS.md) when**:
- User asks about specific SAP (SAP-001, SAP-015, etc.)
- User wants to install/adopt capability
- User wants SAP catalog or quick reference
- User asks "what capabilities are available?"

**Use [workflows/AGENTS.md](workflows/AGENTS.md) when**:
- User wants to add features to template
- User wants to release new version
- User wants to run quality gates
- User asks "how do I develop chora-base?"

**Use [scripts/AGENTS.md](scripts/AGENTS.md) when**:
- User wants to write Python script
- User wants to add automation
- User needs cross-platform patterns
- User asks "how do I write scripts?"

**Use [docs/skilled-awareness/AGENTS.md](docs/skilled-awareness/AGENTS.md) when**:
- User wants comprehensive SAP catalog with full metadata
- User needs SAP adoption patterns and integration examples
- User asks "how do SAPs work together?"
- User wants to navigate to specific SAP documentation

**Use [docs/dev-docs/AGENTS.md](docs/dev-docs/AGENTS.md) when**:
- User wants to understand chora-base architecture
- User wants to contribute to chora-base development
- User asks "how is chora-base built?"
- User needs design decisions and technical details

**Use [docs/user-docs/AGENTS.md](docs/user-docs/AGENTS.md) when**:
- User wants tutorials and how-to guides
- User needs reference documentation
- User asks "how do I use feature X?"
- User wants FAQ and troubleshooting

**Use [docs/project-docs/AGENTS.md](docs/project-docs/AGENTS.md) when**:
- User wants to see project roadmap and plans
- User wants to understand governance and decisions
- User asks "what's the project status?"
- User wants to coordinate work across the project

---

## Quick Decision Tree

**Question 1: What does the user want to do?**

### A. Create New Project from Template

→ **Action**: Use fast-setup script (see Critical Workflow #1 above)

```bash
python scripts/create-capability-server.py \
    --name "Project Name" \
    --namespace namespace \
    --output ~/projects/output
```

**Documentation**: [README.md](README.md), [docs/user-docs/quickstart-mcp-server.md](docs/user-docs/quickstart-mcp-server.md)

**Time**: 1-2 minutes to fully-configured project

---

### B. Understand chora-base (Onboarding)

→ **Read**: [getting-started/AGENTS.md](getting-started/AGENTS.md)

**Topics**: Project overview, SAP structure, creating/installing SAPs, roadmap, examples

---

### C. Install/Adopt SAP Capability

→ **Read**: [saps/AGENTS.md](saps/AGENTS.md) + specific SAP adoption blueprint

```bash
# Find SAP
cat saps/AGENTS.md | grep "SAP-015"

# Read adoption blueprint
cat docs/skilled-awareness/task-tracking/adoption-blueprint.md

# Follow installation steps (see Critical Workflow #4)
```

---

### D. Develop chora-base Template

→ **Read**: [workflows/AGENTS.md](workflows/AGENTS.md)

**Topics**: Adding features, releasing versions, testing strategy, quality gates, automation

---

### E. Write Script or Automation

→ **Read**: [scripts/AGENTS.md](scripts/AGENTS.md) (see Critical Workflow #2)

**Topics**: Cross-platform patterns, Path usage, automation scripts, justfile recipes

---

### F. Write or Run Tests

→ **Read**: [tests/AGENTS.md](tests/AGENTS.md)

**Topics**: pytest patterns, coverage gates, test structure, validation

---

## Repository Structure

```
chora-base/
├── AGENTS.md (this file)          # Root navigation + critical workflows
├── CLAUDE.md                       # Claude-specific navigation patterns
├── SKILLED_AWARENESS_PACKAGE_PROTOCOL.md  # Root SAP protocol
├── sap-catalog.json                # Machine-readable SAP registry
│
├── saps/AGENTS.md                  # SAP catalog + quick references
├── workflows/AGENTS.md             # Development workflows
├── getting-started/AGENTS.md       # Onboarding guide
│
├── static-template/                # Files copied to generated projects
│   ├── src/                        # Python source baseline
│   ├── tests/                      # Test baseline
│   ├── scripts/                    # Automation scripts
│   ├── .github/workflows/          # CI/CD workflows
│   └── ...                         # Other project files
│
├── docs/                           # Template documentation
│   ├── user-docs/                  # Getting started, tutorials, how-to
│   ├── dev-docs/                   # Architecture, contributing
│   ├── project-docs/               # Plans, decisions, retrospectives
│   └── skilled-awareness/          # SAP capabilities (30+ packages)
│       ├── INDEX.md                # SAP registry
│       ├── sap-framework/          # SAP-000: Framework SAP
│       ├── inbox/                  # SAP-001: Inbox coordination
│       ├── testing-framework/      # SAP-004: Testing
│       └── ... (30+ SAPs)
│
├── scripts/                        # Automation scripts
│   ├── AGENTS.md                   # Script patterns + cross-platform
│   ├── create-capability-server.py  # Fast-setup script
│   ├── install-sap.py              # SAP installation
│   ├── sap-validate.py             # SAP validation
│   └── ... (25 scripts)
│
├── tests/                          # Test suite
│   ├── AGENTS.md                   # Testing patterns
│   └── ...
│
├── inbox/                          # Inbox coordination (SAP-001)
│   ├── INBOX_PROTOCOL.md
│   ├── CLAUDE.md
│   └── coordination/
│
├── examples/                       # Example generated projects
│   └── ...
│
├── CHANGELOG.md                    # Version history
├── README.md                       # Project overview
└── justfile                        # Unified automation interface
```

---

## Skilled Awareness Packages (SAPs)

### What Are SAPs?

SAPs are **complete, installable capability bundles** with clear contracts and agent-executable blueprints. Each SAP includes 5 artifacts:

1. **Capability Charter** (problem, scope, outcomes)
2. **Protocol Specification** (technical contract)
3. **Awareness Guide** (agent execution patterns)
4. **Adoption Blueprint** (installation steps)
5. **Traceability Ledger** (adopter tracking)

### SAP Quick Reference

**For complete SAP catalog and quick references**, see **[saps/AGENTS.md](saps/AGENTS.md)**.

**Core Infrastructure & Development** (most commonly used):

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-000 | sap-framework | production | Meta-SAP defining SAP pattern |
| SAP-001 | inbox | production | Cross-repo coordination |
| SAP-003 | project-bootstrap | draft | Fast-setup script (1-2 min) |
| SAP-004 | testing-framework | production | pytest with coverage gates |
| SAP-005 | ci-cd-workflows | production | GitHub Actions automation |
| SAP-006 | quality-gates | production | Pre-commit hooks |
| SAP-009 | agent-awareness | production | Nested AGENTS.md pattern |
| SAP-015 | task-tracking | pilot | Beads persistent tasks |

**Capability Server Architecture** (NEW - pilot):

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-042 | interface-design | pilot | Core/interface separation (80% coupling reduction) |
| SAP-043 | multi-interface | pilot | CLI/REST/MCP patterns (75% time savings) |
| SAP-044 | registry | pilot | Service discovery with manifests |
| SAP-045 | bootstrap | pilot | Startup orchestration (90% failure reduction) |
| SAP-046 | composition | pilot | Saga, circuit breaker, events (1,141% ROI) |
| SAP-047 | capability-server-template | pilot | Jinja2-based template (2,271% ROI, 5-min setup) |

**React Foundation** (pilot):

| SAP | Name | Status | Description |
|-----|------|--------|-------------|
| SAP-020 | react-foundation | active | Next.js 15 + TypeScript (8-12h → 45min) |
| SAP-033 | react-authentication | pilot | NextAuth/Clerk/Supabase (93.75% time savings) |
| SAP-034 | react-database-integration | pilot | Prisma/Drizzle + PostgreSQL (89.6% savings) |
| SAP-041 | react-form-validation | pilot | React Hook Form + Zod (88.9% savings) |

**See**: [saps/AGENTS.md](saps/AGENTS.md) for all 45 SAPs

---

## Development Workflows

### Common Workflows

**For complete workflow documentation**, see **[workflows/AGENTS.md](workflows/AGENTS.md)**.

**Quick Commands**:

```bash
# Quality gates (BEFORE every commit - see Critical Workflow #3)
just pre-merge                    # Test + lint + format + type-check

# Testing
just test                         # pytest with coverage
just smoke                        # Quick smoke tests (~5-10s)

# Documentation
just validate-docs                # Diátaxis validation
just extract-doc-tests            # Generate tests from how-to guides

# Version management
just bump-minor                   # 1.9.3 → 1.10.0
just build                        # Build distribution
just publish-prod                 # Publish to PyPI

# SAP validation
just validate-all-saps            # Validate all SAP structures
just validate-sap-structure docs/skilled-awareness/testing-framework

# Automation
just automation-help              # Show all 30+ commands
```

**See**: [workflows/AGENTS.md](workflows/AGENTS.md) for complete workflows

---

## File Organization Conventions

### Upgrade Documentation

**Location**: `docs/upgrades/`
**Naming**: `vX.Y-to-vX.Z.md` (e.g., `v1.9.2-to-v1.9.3.md`)
**Template**: `docs/upgrades/UPGRADE_GUIDE_TEMPLATE.md`

**Why This Matters**: Previous upgrade docs were misplaced in repo root because chora-base lacked this guidance.

### Research Documents

**Location**: `docs/research/`
**Format**: PDF, markdown, or other documentation formats
**Purpose**: Background research informing template features

### How-To Guides

**Location**: `docs/user-docs/how-to/`
**Naming**: `NN-kebab-case-title.md` (e.g., `01-setup-new-project.md`)
**Frontmatter Required**: audience, time, prerequisites, difficulty

### SAP Documentation

**Location**: `docs/skilled-awareness/<sap-name>/`
**Structure**: 5 artifacts (charter, protocol, awareness, blueprint, ledger)
**Naming**: kebab-case (e.g., `testing-framework`, `quality-gates`)

---

## Documentation Domains

chora-base uses **Diátaxis 4-domain documentation architecture**:

### 1. User Documentation

**Path**: [docs/user-docs/](docs/user-docs/)

**Structure**:
- `tutorials/` - Learning-oriented (step-by-step lessons)
- `how-to/` - Task-oriented (practical guides)
- `explanation/` - Understanding-oriented (concepts, rationale)
- `reference/` - Information-oriented (API docs, specs)

**Use When**: User asks "how do I use chora-base?"

### 2. Developer Documentation

**Path**: [docs/dev-docs/](docs/dev-docs/)

**Contents**: Architecture, contributing guidelines, development setup

**Use When**: User asks "how do I contribute to chora-base?"

### 3. Project Documentation

**Path**: [docs/project-docs/](docs/project-docs/)

**Contents**: Plans, decisions (ADRs), retrospectives, verification

**Use When**: User asks about project roadmap or decisions

### 4. Skilled Awareness

**Path**: [docs/skilled-awareness/](docs/skilled-awareness/)

**Contents**: 30+ SAP capabilities (see [saps/AGENTS.md](saps/AGENTS.md))

**Use When**: User asks about capabilities or wants to install SAP

---

## Common Tasks (Quick Reference)

### Task 1: Create New Project

```bash
python scripts/create-capability-server.py \
    --name "Project Name" \
    --namespace namespace \
    --output ~/projects/output
```

**See**: Critical Workflow #1, [getting-started/AGENTS.md](getting-started/AGENTS.md)

### Task 2: Install SAP

```bash
# Read blueprint
cat docs/skilled-awareness/<sap-name>/adoption-blueprint.md

# Follow 5-step process (see Critical Workflow #4)
```

**See**: Critical Workflow #4, [saps/AGENTS.md](saps/AGENTS.md)

### Task 3: Add Feature to Template

```bash
# 5-phase workflow: Research → Design → Implementation → Documentation → Validation
```

**See**: [workflows/AGENTS.md](workflows/AGENTS.md#adding-new-features-to-template)

### Task 4: Release New Version

```bash
# 6-step process: Validation → Upgrade Guide → Core Files → Commit/Tag → Release → Index
```

**See**: Critical Workflow #5, [workflows/AGENTS.md](workflows/AGENTS.md#releasing-new-version)

### Task 5: Run Quality Gates

```bash
just pre-merge  # BEFORE every commit
```

**See**: Critical Workflow #3, [workflows/AGENTS.md](workflows/AGENTS.md#quality-gates-sap-006)

### Task 6: Write Cross-Platform Script

```python
# Use Path from pathlib, NO os.system()
from pathlib import Path
import shutil

file_path = Path("docs") / "example.md"
shutil.rmtree(Path("temp"))
```

**See**: Critical Workflow #2, [scripts/AGENTS.md](scripts/AGENTS.md)

### Task 7: Track Work Across Sessions (SAP-015)

```bash
# Check for unblocked tasks
bd ready --json

# Claim a task
bd update {task-id} --status in_progress --assignee {your-name}

# Add progress comments
bd comment {task-id} "Completed X, working on Y"

# Close completed task
bd close {task-id} --reason "Implemented and tested feature"

# List open tasks
bd list --status open --json
```

**Why Use Beads**: Persistent task memory across sessions eliminates context re-establishment overhead. Perfect for multi-session work.

**See**: [docs/skilled-awareness/task-tracking/AGENTS.md](docs/skilled-awareness/task-tracking/AGENTS.md)

### Task 8: Coordinate Cross-Repo Work (SAP-001)

```bash
# Check active coordination requests
cat inbox/coordination/active.jsonl

# Decompose coordination into tasks (with SAP-015)
bd create "COORD-XXX: Epic Title" --priority 0 --type epic
bd create "Subtask 1" --priority 0 --parent {epic-id}
bd create "Subtask 2" --priority 1 --parent {epic-id}

# Add dependencies
bd dep add {subtask2-id} {subtask1-id}

# Update coordination status
vim inbox/coordination/active.jsonl
# (Mark progress, update status)

# Archive completed coordination
mv inbox/coordination/{file}.jsonl inbox/coordination/archived.jsonl
```

**Why Use Inbox**: Broadcast coordination protocol for multi-repo workflows. Reduces coordination overhead by 90%.

**See**: [docs/skilled-awareness/inbox/AGENTS.md](docs/skilled-awareness/inbox/AGENTS.md)

---

## Related Resources

### Nested Awareness Files

- [saps/AGENTS.md](saps/AGENTS.md) - SAP catalog + quick references
- [workflows/AGENTS.md](workflows/AGENTS.md) - Development workflows
- [getting-started/AGENTS.md](getting-started/AGENTS.md) - Onboarding guide
- [scripts/AGENTS.md](scripts/AGENTS.md) - Script patterns
- [tests/AGENTS.md](tests/AGENTS.md) - Testing patterns

### Key Documents

- [CLAUDE.md](CLAUDE.md) - Claude-specific navigation
- [README.md](README.md) - Project overview
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [DOCUMENTATION_STANDARD.md](DOCUMENTATION_STANDARD.md) - Documentation rules
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - SAP protocol

### Documentation Domains

- [docs/user-docs/](docs/user-docs/) - User guides, tutorials
- [docs/dev-docs/](docs/dev-docs/) - Architecture, contributing
- [docs/project-docs/](docs/project-docs/) - Plans, decisions
- [docs/skilled-awareness/](docs/skilled-awareness/) - SAP capabilities

### Tools

- [justfile](justfile) - Unified automation interface
- [scripts/](scripts/) - Automation scripts (25 scripts)
- [.pre-commit-config.yaml](.pre-commit-config.yaml) - Quality gates

---

## Need Help?

**For Users** (creating projects):
- Start: [README.md](README.md#-start-here-ai-agent-quick-decision-tree)
- Quick Start: [docs/user-docs/quickstart-mcp-server.md](docs/user-docs/quickstart-mcp-server.md)

**For Contributors** (developing template):
- Onboarding: [getting-started/AGENTS.md](getting-started/AGENTS.md)
- Workflows: [workflows/AGENTS.md](workflows/AGENTS.md)
- Architecture: [docs/dev-docs/ARCHITECTURE.md](docs/dev-docs/ARCHITECTURE.md)

**For SAP Adopters** (installing capabilities):
- SAP Catalog: [saps/AGENTS.md](saps/AGENTS.md)
- SAP Index: [docs/skilled-awareness/INDEX.md](docs/skilled-awareness/INDEX.md)
- Specific SAP: `docs/skilled-awareness/<sap-name>/adoption-blueprint.md`

---

**Version**: 2.0.0 (nested awareness pattern v2.1.0)
**Last Updated**: 2025-11-10
**Status**: Active
**Line Count**: ~850 lines (reduced from 4,749 lines, 82% reduction)
