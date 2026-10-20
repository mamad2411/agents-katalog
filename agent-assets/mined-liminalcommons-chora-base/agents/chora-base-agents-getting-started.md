# Getting Started: chora-base

**Purpose**: Quick onboarding guide for working with chora-base template repository.

**Navigation**:
- [← Back to root AGENTS.md](../AGENTS.md) - Complete project overview
- [→ SAPs Quick Reference](../saps/AGENTS.md) - SAP catalog
- [→ Workflows](../workflows/AGENTS.md) - Development processes

---

## 🔴 CROSS-PLATFORM REMINDER

**ALL code MUST work on Windows, Mac, and Linux without modification.**

Before writing Python scripts, read: [scripts/AGENTS.md](../scripts/AGENTS.md) for cross-platform patterns.

**Quick Template**: Copy [templates/cross-platform/python-script-template.py](../templates/cross-platform/python-script-template.py)

**Validation**: `python scripts/validate-windows-compat.py --file your-script.py`

---

## ⚠️ CRITICAL: chora-base is a TEMPLATE SOURCE

**DO NOT** try to "set up chora-base" as if it were a project to develop.

**chora-base** is a **template repository** used to **generate other projects**.

### Decision Tree for Agents

**Question 1: Are you trying to CREATE A NEW PROJECT using chora-base?**

✅ **YES** → Use the fast-setup script:

```bash
python scripts/create-capability-server.py \
    --name "Your Project Name" \
    --namespace yournamespace \
    --enable-mcp \
    --output ~/projects/your-project
```

**⚠️ SAP-014 Deprecation**: The old `create-model-mcp-server.py` script and SAP-014 (mcp-server-development) have been **deprecated**. Use SAP-047 (capability-server-template) instead, which provides multi-interface support (CLI, REST, optional MCP).

**SAP Dependencies**: SAP-047 automatically includes:
- **SAP-042** (Interface Design) - Core/interface separation patterns
- **SAP-043** (Multi-Interface) - CLI, REST, and optional MCP interfaces
- **SAP-044** (Registry) - Service discovery (optional)
- **SAP-045** (Bootstrap) - Self-provisioning (optional)
- **SAP-046** (Composition) - Service orchestration (optional)

**Documentation**:
- [README.md](../README.md) - Complete instructions
- [docs/user-docs/quickstart-mcp-server.md](../docs/user-docs/quickstart-mcp-server.md) - MCP server quick start

**Time Estimate**: 5-10 minutes to fully-configured project

**What You Get**:
- Production-ready capability server with multi-interface support (CLI, REST, optional MCP)
- Testing framework (pytest, 85%+ coverage gate)
- CI/CD workflows (GitHub Actions)
- Quality gates (pre-commit hooks: ruff, mypy, black)
- Documentation structure (Diátaxis 4-domain)
- Agent awareness (AGENTS.md, CLAUDE.md)
- Coordination protocol (inbox/)
- Memory system (.chora/memory/)
- Task tracking (.beads/)

---

**Question 2: Are you DEVELOPING chora-base itself** (contributing to the template)?

✅ **YES** → Continue reading this guide

**What You're Working On**:
- Template source code
- SAP definitions (30+ capabilities)
- Scripts (automation, installation, validation)
- Documentation (4-domain structure)

**Key Directories**:
- `static-template/` - Files copied to generated projects
- `docs/skilled-awareness/` - SAP documentation (30+ capabilities)
- `scripts/` - Automation scripts (create-capability-server.py, install-sap.py, etc.)
- `blueprints/` - Blueprint templates for generated projects

---

## Project Overview

**chora-base** is a blueprint-driven Python project template designed for LLM-intelligent development. It generates production-ready Python projects with built-in support for AI coding agents, comprehensive documentation, and quality gates without relying on Copier.

### Key Facts

- **Repository Type**: Template repository (generates other projects)
- **Primary Users**: Human developers and AI agents generating/maintaining Python projects
- **Technology Stack**: Static scaffolding (`static-template/`), Skilled Awareness Packages (SAPs) for capability governance
- **Current Version**: v1.9.3 (see [CHANGELOG.md](../CHANGELOG.md))
- **License**: MIT (see [LICENSE](../LICENSE))

### Key Concepts

1. **Template vs Generated Project**
   - **chora-base**: The template (this repository)
   - **Generated projects**: Adopters created via fast-setup script

2. **Blueprint Generation**
   - `.blueprint` files define how adopters bootstrap projects
   - Agent-led or scripted workflows
   - Variable substitution (project name, namespace, etc.)

3. **Static Assets**
   - `static-template/` contains ready-to-copy files
   - Used by blueprints during project generation
   - Includes src/, tests/, scripts/, .github/workflows/, etc.

4. **Skilled Awareness Packages (SAPs)**
   - Major capabilities packaged as complete bundles
   - 5 artifacts per SAP (charter, protocol, awareness, blueprint, ledger)
   - Installable, upgradeable, trackable
   - 30+ SAPs available

5. **Upgrade Path**
   - Adopters follow SAP adoption blueprints
   - Ledger/broadcast updates keep adopters aligned
   - Version-specific upgrade guides in docs/upgrades/

---

## Skilled Awareness Packages (SAPs)

### What Are SAPs?

SAPs are **complete, installable capability bundles** with clear contracts and agent-executable blueprints.

**Why SAPs Matter**:
- ✅ Clear contracts (explicit guarantees, no assumptions)
- ✅ Predictable upgrades (sequential adoption, migration blueprints)
- ✅ Machine-readable (AI agents can parse and execute)
- ✅ Governance (versioning, change management, tracking)

### SAP Structure

Every SAP includes:

**1. Five Core Artifacts**:
- **Capability Charter** (problem, scope, outcomes)
- **Protocol Specification** (technical contract)
- **Awareness Guide** (agent execution patterns)
- **Adoption Blueprint** (installation steps)
- **Traceability Ledger** (adopter tracking)

**2. Infrastructure** (schemas, templates, configs, directories)

**3. Testing Layer** (optional validation)

### Key SAP Documents

**Root Protocol**: [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- Defines what SAPs are and how they work
- Installation pattern (blueprint-based, not scripts)
- Integration with DDD → BDD → TDD
- Scope levels (Vision & Strategy, Planning, Implementation)

**SAP Index**: [docs/skilled-awareness/INDEX.md](../docs/skilled-awareness/INDEX.md)
- Registry of all 30+ capabilities
- Status (production, pilot, draft)
- Dependencies, priorities, effort estimates
- Current coverage: 28/30+ SAPs defined

**Framework SAP**: [docs/skilled-awareness/sap-framework/](../docs/skilled-awareness/sap-framework/)
- Meta-SAP defining the SAP pattern itself (SAP-000)
- Complete reference implementation
- Templates and guidelines

**Reference Implementation**: [docs/skilled-awareness/inbox/](../docs/skilled-awareness/inbox/)
- Pilot SAP for cross-repo coordination (SAP-001)
- Complete example with infrastructure and testing

---

## Creating SAPs

### When to Create a SAP

Create a SAP when:
- Adding new major capability (e.g., testing-framework, docker-operations)
- Capability needs structured governance
- Multiple adopters will use capability
- Clear upgrade path needed

### SAP Creation Process

**6-Step Process**:

```bash
# Step 1: Read SAP documentation
cat docs/skilled-awareness/document-templates.md

# Step 2: Create directory
mkdir -p docs/skilled-awareness/<capability-name>/

# Step 3: Create 5 artifacts using templates
# - capability-charter.md (problem statement, solution design)
# - protocol-spec.md (complete technical specification)
# - awareness-guide.md (operating patterns for agents)
# - adoption-blueprint.md (step-by-step installation)
# - ledger.md (adopter tracking, metrics, version history)

# Step 4: Add infrastructure
# - schemas/ (JSON schemas if needed)
# - templates/ (templates for generated files)
# - configs/ (configuration files)
# - Create capability-specific directories

# Step 5: Update SAP Index
vim docs/skilled-awareness/INDEX.md
# Add new SAP to registry with status, version, dependencies

# Step 6: Follow DDD → BDD → TDD
# - DDD: Create Charter + Protocol (document requirements)
# - BDD: Define acceptance criteria (behaviors)
# - TDD: Implement infrastructure + Awareness + Blueprint (tests first)
```

**Time Estimate**: 8-20 hours per SAP (varies by complexity)

**Example**: Creating SAP-042 (New Capability)
```bash
# 1. Read templates
cat docs/skilled-awareness/document-templates.md

# 2. Create directory
mkdir -p docs/skilled-awareness/new-capability/

# 3. Create artifacts (copy templates)
cp templates/sap-artifacts/capability-charter.md docs/skilled-awareness/new-capability/
cp templates/sap-artifacts/protocol-spec.md docs/skilled-awareness/new-capability/
cp templates/sap-artifacts/awareness-guide.md docs/skilled-awareness/new-capability/
cp templates/sap-artifacts/adoption-blueprint.md docs/skilled-awareness/new-capability/
cp templates/sap-artifacts/ledger.md docs/skilled-awareness/new-capability/

# 4. Fill in artifacts with capability-specific content
vim docs/skilled-awareness/new-capability/capability-charter.md
# ... (fill in problem, solution, scope, stakeholders, lifecycle)

# 5. Update INDEX.md
vim docs/skilled-awareness/INDEX.md
# Add: "SAP-042 | new-capability | draft | 1.0.0 | New capability description"

# 6. Validate structure
just validate-sap-structure docs/skilled-awareness/new-capability
```

---

## Installing SAPs

### Installation Process

**5-Step Process**:

```bash
# Step 1: Find SAP in INDEX.md
cat docs/skilled-awareness/INDEX.md

# Step 2: Navigate to SAP directory
cd docs/skilled-awareness/<sap-name>/

# Step 3: Read adoption-blueprint.md
cat adoption-blueprint.md

# Step 4: Execute installation steps sequentially
# Follow blueprint instructions (agent-executable markdown)
# Example steps might include:
# - Copy files to target directories
# - Update configuration files
# - Install dependencies
# - Run validation commands

# Step 5: Run validation commands
# Verify installation succeeded
# Example: ls inbox/coordination/CAPABILITIES && echo "✅ Installed"

# Step 6: Update ledger.md (add adopter record)
vim ledger.md
# Add adopter entry with project name, version, date, status
```

**Example**: Installing SAP-001 (Inbox Coordination)
```bash
# 1. Find SAP
cat docs/skilled-awareness/INDEX.md | grep "SAP-001"
# Output: SAP-001 | inbox | production | 1.1.0 | Cross-repo coordination protocol

# 2. Navigate to SAP
cd docs/skilled-awareness/inbox/

# 3. Read blueprint
cat adoption-blueprint.md

# 4. Execute steps (example from blueprint)
mkdir -p inbox/coordination
cp schemas/coordination-request.schema.json inbox/coordination/
touch inbox/coordination/active.jsonl
touch inbox/coordination/archived.jsonl
touch inbox/coordination/events.jsonl

# 5. Validate
ls inbox/coordination/CAPABILITIES && echo "✅ Installed"

# 6. Update ledger (add adopter record)
echo "- chora-base | 1.1.0 | active | 2025-11-10" >> ledger.md
```

---

## Validating SAPs

### Automated SAP Structure Validation

**Tool**: [scripts/sap-validate.py](../scripts/sap-validate.py) (SAP-008 L3)

### Quick Commands

```bash
# Validate single SAP
just validate-sap-structure docs/skilled-awareness/testing-framework

# Validate all SAPs
just validate-all-saps

# Or call directly
python scripts/sap-validate.py docs/skilled-awareness/testing-framework
python scripts/sap-validate.py --all
```

### What It Checks

- ✅ 5 required artifacts present (charter, protocol, awareness, blueprint, ledger)
- ✅ Valid frontmatter in each artifact (---...---)
- ✅ SAP ID format (SAP-###)
- ✅ Version follows semver (X.Y.Z)
- ✅ Required frontmatter fields (sap_id, version, status)

### Output Example

```
[OK] docker-operations
  ✅ 5 required artifacts present
  ✅ Valid frontmatter in all artifacts
  ✅ SAP ID format: SAP-011
  ✅ Version: 1.0.0 (semver)
  ✅ Status: production

[FAIL] testing-framework
  ❌ capability-charter.md: Missing frontmatter (---...---)
  ❌ protocol-spec.md: Missing frontmatter (---...---)

Summary: 1/2 SAPs passed validation
```

### Baseline Status (2025-11-09)

- **Compliant SAPs**: 28/30+ SAPs have proper frontmatter
- **Target**: 100% SAP compliance (ongoing)
- **Quality Gate**: SAP validation runs in CI/CD (GitHub Actions)

---

## SAP Roadmap

### Phase 1 (2025-10 → 2025-11): Framework Hardening

**Status**: ✅ Complete

- ✅ SAP-000 (sap-framework) - Meta-SAP defining SAP pattern
- ✅ SAP-001 (inbox-coordination) - Cross-repo coordination (pilot)
- ✅ SAP-002 (chora-base-meta) - chora-base self-documentation

### Phase 2 (2025-11 → 2026-01): Core Capabilities

**Status**: 🔄 In Progress

- ✅ SAP-003 (project-bootstrap) - Fast-setup script
- ✅ SAP-004 (testing-framework) - pytest with coverage gates
- ✅ SAP-005 (ci-cd-workflows) - GitHub Actions automation
- ✅ SAP-006 (quality-gates) - Pre-commit hooks

### Phase 3 (2026-01 → 2026-03): Extended Capabilities

**Status**: 🔄 In Progress

- ✅ SAP-007 (documentation-framework) - Diátaxis 4-domain structure
- ✅ SAP-008 (automation-scripts) - 25 script toolkit
- ✅ SAP-009 (agent-awareness) - Nested AGENTS.md/CLAUDE.md pattern
- ✅ SAP-010 (memory-system / A-MEM) - Event-sourced agent memory
- ✅ SAP-011 (docker-operations) - Production containerization
- ✅ SAP-012 (development-lifecycle) - 8-phase development process

### Phase 4 (2026-03 → 2026-05): Optimization

**Status**: ⏳ Planned

- SAP-013 (metrics-tracking) - Quality/velocity/process/adoption metrics
- SAP-014 (mcp-server-development) - MCP server patterns
- SAP-015 (task-tracking) - Beads persistent task management
- Additional SAPs as needed

**See**: [docs/skilled-awareness/chora-base-sap-roadmap.md](../docs/skilled-awareness/chora-base-sap-roadmap.md)

---

## Quick Start Examples

### Example 1: Create New MCP Server Project

```bash
# Use fast-setup script (1-2 minutes)
python scripts/create-capability-server.py \
    --name "Weather Data MCP" \
    --namespace weatherdata \
    --output ~/projects/weather-mcp

# Verify project generated successfully
cd ~/projects/weather-mcp
pytest --cov=src --cov-fail-under=85  # Should pass 100%
just test                             # Should pass with coverage
just pre-merge                        # Should pass all quality gates

# Implement MCP tools
vim src/weatherdata/server.py
# Add @mcp.tool() decorated functions

# Test and commit
pytest
git add .
git commit -m "feat: Add weather data MCP tools"
```

### Example 2: Adopt New SAP in Existing Project

```bash
# Find SAP in catalog
cat docs/skilled-awareness/INDEX.md | grep "task-tracking"
# Output: SAP-015 | task-tracking | pilot | 1.0.0 | Beads persistent task management

# Read adoption blueprint
cat docs/skilled-awareness/task-tracking/adoption-blueprint.md

# Follow installation steps
# ... (steps from blueprint)

# Validate installation
bd --version && echo "✅ Beads installed"

# Update project AGENTS.md with new patterns
vim AGENTS.md
# Add task-tracking section
```

### Example 3: Contribute to chora-base Template

```bash
# Clone repository
git clone https://github.com/your-org/chora-base.git
cd chora-base

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Create feature branch
git checkout -b feat/new-capability

# Make changes
vim static-template/src/new-feature.py

# Run quality gates
just pre-merge  # Test + lint + format + type-check

# Commit changes
git add .
git commit -m "feat: Add new capability"

# Push and create PR
git push origin feat/new-capability
gh pr create --title "Add new capability" --body "..."
```

---

## Common Tasks

### Task 1: Update Documentation

```bash
# Use Diátaxis decision tree
# 1. Learning-oriented? → docs/user-docs/tutorials/
# 2. Task-oriented? → docs/user-docs/how-to/
# 3. Understanding-oriented? → docs/user-docs/explanation/
# 4. Information-oriented? → docs/user-docs/reference/

# Create new how-to guide
vim docs/user-docs/how-to/new-task.md

# Add frontmatter
---
audience: [developers, agents]
time: 10 minutes
prerequisites: [Python 3.11+]
difficulty: intermediate
---

# Validate
just validate-frontmatter
just extract-doc-tests
```

### Task 2: Add Automation Script

```bash
# Create script in appropriate category
vim scripts/new-automation.sh

# Make executable
chmod +x scripts/new-automation.sh

# Add justfile recipe
vim justfile
# Add: new-automation: bash scripts/new-automation.sh

# Validate
just new-automation

# Test in CI (add to .github/workflows/ if needed)
```

### Task 3: Release New Version

```bash
# Follow release workflow (see workflows/AGENTS.md)
# 1. Pre-release validation
# 2. Create upgrade guide
# 3. Update core files
# 4. Commit and tag
# 5. Create GitHub release
# 6. Update upgrade docs index

# Quick commands
just bump-minor  # 1.9.3 → 1.10.0
just build       # Build distribution packages
just publish-prod  # Publish to PyPI (if applicable)
```

---

## Related Resources

**Navigation**:
- [← Root AGENTS.md](../AGENTS.md) - Complete project overview
- [→ SAPs Quick Reference](../saps/AGENTS.md) - All SAP capabilities
- [→ Workflows](../workflows/AGENTS.md) - Development processes

**Key Documents**:
- [README.md](../README.md) - Project overview and quick start
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [DOCUMENTATION_STANDARD.md](../DOCUMENTATION_STANDARD.md) - Documentation rules
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - SAP protocol

**Documentation Domains**:
- [docs/user-docs/](../docs/user-docs/) - User guides, tutorials, how-tos
- [docs/dev-docs/](../docs/dev-docs/) - Architecture, contributing
- [docs/project-docs/](../docs/project-docs/) - Plans, decisions
- [docs/skilled-awareness/](../docs/skilled-awareness/) - SAP capabilities

**Tools**:
- [scripts/](../scripts/) - Automation scripts directory
- [justfile](../justfile) - Unified automation interface
- [.pre-commit-config.yaml](../.pre-commit-config.yaml) - Quality gates

---

## Need Help?

**For Users** (creating projects from chora-base):
- Start: [README.md](../README.md#-start-here-ai-agent-quick-decision-tree)
- Quick Start: [docs/user-docs/quickstart-mcp-server.md](../docs/user-docs/quickstart-mcp-server.md)
- FAQ: [docs/user-docs/reference/faq.md](../docs/user-docs/reference/faq.md)

**For Contributors** (developing chora-base):
- Contributing: [docs/dev-docs/CONTRIBUTING.md](../docs/dev-docs/CONTRIBUTING.md)
- Architecture: [docs/dev-docs/ARCHITECTURE.md](../docs/dev-docs/ARCHITECTURE.md)
- Workflows: [workflows/AGENTS.md](../workflows/AGENTS.md)

**For SAP Adopters** (installing SAPs):
- SAP Index: [docs/skilled-awareness/INDEX.md](../docs/skilled-awareness/INDEX.md)
- SAP Framework: [docs/skilled-awareness/sap-framework/protocol-spec.md](../docs/skilled-awareness/sap-framework/protocol-spec.md)
- Specific SAP: Navigate to `docs/skilled-awareness/<sap-name>/adoption-blueprint.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-11-10
**Status**: Active (nested awareness pattern v2.1.0)
