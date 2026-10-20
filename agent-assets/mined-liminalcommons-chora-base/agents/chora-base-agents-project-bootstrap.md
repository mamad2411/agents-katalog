---
sap_id: SAP-003
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-130"    # Quick Reference + Generate Project Workflow
  phase_2: "lines 131-280"  # Validation + Customization + Troubleshooting Workflows
  phase_3: "full"           # Complete including best practices, pitfalls, integration
phase_1_token_estimate: 3500
phase_2_token_estimate: 8000
phase_3_token_estimate: 12000
---

# Project Bootstrap (SAP-003) - Agent Awareness

**SAP ID**: SAP-003
**Capability**: project-bootstrap
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-003?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - Single command to generate production-ready project in 1-2 minutes with 100+ files
- 📚 **Time Savings** - 95% reduction (1-2 min vs 30-60 min manual setup), 20-40 second execution for AI agents
- 🎯 **Zero Dependencies** - Blueprint-based templating using Python stdlib (no Copier/Cookiecutter/Jinja2)
- 🔧 **5-Step Generation** - Gather variables → Copy template → Rename packages → Process blueprints → Initialize git
- 📊 **Quality Gates** - 100+ files generated with pytest (85%+ coverage), ruff, mypy, pre-commit hooks, CI/CD workflows
- 🔗 **Integration** - Works with SAP-002 (Chora-Base), SAP-014 (MCP Server), SAP-004 (Testing), SAP-005 (CI/CD), SAP-006 (Quality Gates), SAP-007 (Documentation), SAP-009 (Agent Awareness), SAP-011 (Docker)

This AGENTS.md provides: Agent-executable workflows for generation, validation, customization, and troubleshooting.

### What is Project Bootstrap?

A **comprehensive project generation system** enabling agents to:
1. **Generate** production-ready Python projects from template (30-60 seconds)
2. **Validate** generated project structure and correctness (no placeholders, tests pass)
3. **Customize** generation with optional flags (--no-docker, --no-memory, etc.)
4. **Troubleshoot** generation failures (placeholder detection, missing files)

### When to Use

**Trigger Signals**:

| User Signal | Workflow | Context Needed |
|-------------|----------|----------------|
| "Create new Python project" | Workflow 1 | setup.py + protocol |
| "Generate MCP server" | Workflow 1 | setup.py + protocol |
| "Bootstrap new project from template" | Workflow 1 | setup.py + protocol |
| "Check if project generated correctly" | Workflow 2 | Validation logic |
| "Why did generation fail?" | Workflow 4 | Error handling |
| "Customize project template" | Workflow 3 | Blueprint system |
| "Add chora-base to existing project" | Workflow 5 | Adoption guide |

**Do NOT Use For**:
- Non-Python projects (chora-base is Python-specific)
- Minimal/simple projects (chora-base is comprehensive, production-ready scaffold)
- Manual project creation without generation (use static-template/ directly)

### Core Files

```
setup.py                      # Generation orchestrator (443 lines)
blueprints/                   # Variable substitution templates (12 files)
├── pyproject.toml.blueprint
├── README.md.blueprint
├── src/__init__.py.blueprint
└── ...

static-template/              # Complete project scaffold (100+ files)
├── pyproject.toml            # Python package config
├── README.md                 # Project documentation
├── src/{package_name}/       # Source code directory
├── tests/                    # Test suite
├── .github/workflows/        # CI/CD (if included)
└── ...

docs/skilled-awareness/project-bootstrap/
├── capability-charter.md     # Problem statement, scope
├── protocol-spec.md          # Generation flow, contracts, variables
├── awareness-guide.md        # Detailed agent workflows
├── adoption-blueprint.md     # Installation guide
└── ledger.md                 # Generated project tracking
```

---

## Common Workflows

### Workflow 1: Generate New Project (30-60 seconds)

**User Signal**: "Create new Python project called X"

**Context**: User wants to generate a new project from chora-base template.

**Steps**:

1. **Determine generation mode**:
   - **Interactive mode** (with user): Run `python setup.py <target-dir>`, follow prompts
   - **Programmatic mode** (headless): Prepare variables dict, pass to generation function

2. **For interactive mode** (typical for Claude Code):
   ```bash
   # Run setup.py with target directory
   python setup.py my-new-project

   # Setup will prompt for:
   # - Project name: "My New Project"
   # - Description: "One-line project description"
   # - Author name: "Your Name"
   # - Author email: "email@example.com"
   # - GitHub username: "yourusername"
   # - Python version: "3.11" (default)
   # - License: "MIT" (default)
   ```

3. **Generation phases** (automatic):
   - **Phase 1**: Copy static-template/ to target directory
   - **Phase 2**: Rename {package_name} directories
   - **Phase 3**: Process blueprints (variable substitution)
   - **Phase 4**: Initialize git repository
   - **Phase 5**: Validate (check placeholders, file existence)

4. **Validate generation** (verify success):
   ```bash
   cd my-new-project

   # Check critical files exist
   test -f pyproject.toml && echo "✅ pyproject.toml"
   test -f README.md && echo "✅ README.md"
   test -d src/my_new_project && echo "✅ source directory"

   # Check no unreplaced placeholders
   grep -r "{{" . | grep -v ".git" | grep -v "node_modules"
   # Should return empty (no matches)

   # Check tests loadable
   pytest --collect-only
   # Should show test collection without errors
   ```

5. **Report to user**:
   ```markdown
   ✅ Project generated successfully!

   **Created**: `my-new-project/`
   **Structure**:
   - pyproject.toml (Python package config)
   - README.md (project documentation)
   - src/my_new_project/ (source code)
   - tests/ (test suite)
   - .github/workflows/ (CI/CD)

   **Next steps**:
   1. cd my-new-project
   2. pip install -e ".[dev]"  # Install in development mode
   3. pytest                    # Run tests (should pass)
   4. git status                # Check git initialized

   **Template version**: 3.3.0
   ```

**Expected Output**: Fully functional Python project with all chora-base patterns integrated.

---

### Workflow 2: Validate Generated Project (10 seconds)

**User Signal**: "Check if project generated correctly" or "Validate project structure"

**Context**: After generation, verify project correctness.

**Steps**:

1. **Run validation checks** (same as setup.py validation logic):
   ```bash
   cd <project-directory>

   # Check 1: Critical files exist
   test -f pyproject.toml || echo "❌ Missing pyproject.toml"
   test -f README.md || echo "❌ Missing README.md"
   test -f .gitignore || echo "❌ Missing .gitignore"
   test -d src || echo "❌ Missing src/ directory"
   test -d tests || echo "❌ Missing tests/ directory"
   ```

2. **Check for unreplaced placeholders**:
   ```bash
   # Find any remaining {{ placeholders }}
   find . -type f -name "*.py" -o -name "*.md" -o -name "*.toml" | \
   xargs grep -l "{{" | \
   grep -v ".git"

   # Should return empty (all placeholders replaced)
   ```

3. **Validate Python package loadable**:
   ```bash
   # Check package can be imported
   python -c "import importlib; importlib.import_module('$(basename $(pwd) | tr '-' '_)')"

   # Should succeed without errors
   ```

4. **Validate tests runnable**:
   ```bash
   # Check tests can be collected
   pytest --collect-only

   # Run tests
   pytest

   # Both should succeed
   ```

5. **Report validation results**:
   ```markdown
   ## Validation Results

   ✅ All critical files present
   ✅ No unreplaced placeholders
   ✅ Package importable
   ✅ Tests passing (3 passed)

   **Project Status**: Valid ✅
   **Template Version**: 3.3.0
   **Generated**: 2025-11-04
   ```

**Expected Output**: Validation summary with pass/fail for each check.

---

### Workflow 3: Customize Generation with Flags (30-60 seconds)

**User Signal**: "Generate project without Docker" or "Customize template generation"

**Context**: User wants to generate project with optional components excluded.

**Steps**:

1. **Understand available flags** (from protocol-spec.md):
   - `--no-docker`: Skip Docker files (Dockerfile, docker-compose.yml, .dockerignore)
   - `--no-memory`: Skip memory system (.chora/memory/)
   - `--no-claude`: Skip Claude artifacts (.claude/, .clinerules)
   - `--include-github-actions`: Include CI/CD workflows (default: excluded)

2. **Run generation with flags**:
   ```bash
   # Example: Generate without Docker and memory system
   python setup.py my-project --no-docker --no-memory
   ```

3. **Verify exclusions**:
   ```bash
   cd my-project

   # Check Docker files NOT created
   test ! -f Dockerfile && echo "✅ Docker excluded"
   test ! -f docker-compose.yml && echo "✅ docker-compose excluded"

   # Check memory system NOT created
   test ! -d .chora/memory && echo "✅ Memory system excluded"
   ```

4. **Report customization**:
   ```markdown
   ✅ Project generated with customizations

   **Included**:
   - Core Python package ✅
   - Tests ✅
   - CI/CD ✅
   - Claude artifacts ✅

   **Excluded**:
   - Docker ❌ (--no-docker)
   - Memory system ❌ (--no-memory)

   **Template Version**: 3.3.0
   ```

**Expected Output**: Project generated with specified components excluded.

---

### Workflow 4: Troubleshoot Generation Failure (5-10 minutes)

**User Signal**: "Why did project generation fail?" or "Fix generation error"

**Context**: Generation failed or produced incorrect output.

**Common Failure Scenarios**:

#### Scenario 1: Unreplaced Placeholders

**Symptom**:
```bash
grep -r "{{" my-project/ | grep -v ".git"
# Returns: src/my_project/__init__.py:3: """{{project_description}}"""
```

**Diagnosis**:
- Variable not in variables dict
- Blueprint file not processed
- Typo in variable name

**Fix**:
```bash
# Check which variable is unreplaced
grep -r "{{.*}}" my-project/ | sed 's/.*{{\(.*\)}}.*/\1/' | sort -u

# Check variables dict in setup.py
grep "variables\[" setup.py | grep "project_description"

# If variable exists, check blueprint processing
# Likely blueprint file not in processing list
```

**Resolution**:
- Add missing variable to variables dict
- Add blueprint file to process_blueprints() list
- Fix typo in variable name

---

#### Scenario 2: Package Directory Not Created

**Symptom**:
```bash
ls src/
# Returns empty or {package_name}/ instead of actual package name
```

**Diagnosis**:
- Directory renaming failed
- package_name variable incorrect

**Fix**:
```bash
# Check package_name in variables
grep "package_name" my-project/.chora/metadata.json

# Manually rename if needed
mv src/{package_name} src/my_actual_package
```

**Resolution**:
- Re-run generation with correct package_name
- Or manually rename directories and re-process blueprints

---

#### Scenario 3: Tests Not Loadable

**Symptom**:
```bash
pytest --collect-only
# Returns: ImportError: No module named 'my_project'
```

**Diagnosis**:
- Package not installed
- Package structure incorrect
- pyproject.toml malformed

**Fix**:
```bash
# Install package in editable mode
pip install -e ".[dev]"

# Check package structure
ls -la src/my_project/
# Should have __init__.py

# Check pyproject.toml
grep "name =" pyproject.toml
# Should match package name
```

**Resolution**:
- Install package: `pip install -e ".[dev]"`
- Fix package structure if __init__.py missing
- Regenerate project if pyproject.toml malformed

---

### Workflow 5: Adopt chora-base in Existing Project (2-4 hours)

**User Signal**: "Add chora-base patterns to existing project"

**Context**: Existing Python project wants to adopt chora-base patterns without full regeneration.

**Steps**:

1. **Assess current project**:
   ```bash
   # Check existing structure
   ls -la  # Look for pyproject.toml, src/, tests/

   # Check dependencies
   cat requirements.txt  # or pyproject.toml
   ```

2. **Identify gaps** (compare to static-template):
   - Missing: tests/, .github/workflows/, .pre-commit-config.yaml?
   - Incomplete: pyproject.toml (missing tool.pytest, tool.ruff)?

3. **Selective adoption** (copy specific files from static-template):
   ```bash
   # Copy test infrastructure
   cp -r /path/to/chora-base/static-template/tests .

   # Copy CI/CD
   cp -r /path/to/chora-base/static-template/.github .

   # Copy quality configs
   cp /path/to/chora-base/static-template/.pre-commit-config.yaml .
   cp /path/to/chora-base/static-template/ruff.toml .
   ```

4. **Process blueprints manually**:
   - Read blueprint file (e.g., pyproject.toml.blueprint)
   - Substitute variables manually
   - Merge with existing pyproject.toml (don't overwrite)

5. **Validate integration**:
   ```bash
   # Run new tests
   pytest

   # Run quality checks
   pre-commit run --all-files
   ruff check .
   ```

**Expected Output**: Existing project enhanced with chora-base patterns (tests, CI/CD, quality gates).

---

## Best Practices

### Practice 1: Always Validate After Generation

**Pattern**: Run validation immediately after generation.

```bash
# Generation
python setup.py my-project

# Immediate validation
cd my-project
pytest --collect-only  # Tests loadable?
grep -r "{{" .         # No placeholders?
```

**Why**: Catches generation errors before committing or starting development.

---

### Practice 2: Use Descriptive Project Names

**Pattern**: Use descriptive, specific project names.

**Good**:
- "Weather MCP Server"
- "E-commerce API"
- "Data Processing Pipeline"

**Bad**:
- "Project" (too generic)
- "Test" (ambiguous)
- "myproject" (not descriptive)

**Why**: Project name appears in README, package metadata, documentation - specificity helps discoverability.

---

### Practice 3: Version Template Usage

**Pattern**: Track which template version generated each project.

```bash
# After generation, record template version
cat my-project/.chora/metadata.json
# Should show: "template_version": "3.3.0"

# Update ledger
# docs/skilled-awareness/project-bootstrap/ledger.md
# Add entry: my-project | 3.3.0 | 2025-11-04
```

**Why**: Enables structured upgrades when template evolves.

---

### Practice 4: Test Generated Project Before Committing

**Pattern**: Run full test suite before first commit.

```bash
# After generation
cd my-project

# Install dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run quality checks
pre-commit run --all-files

# THEN commit
git add .
git commit -m "Initial commit from chora-base template"
```

**Why**: Ensures template-generated code is production-ready from day one.

---

### Practice 5: Customize via Flags, Not Manual Edits

**Pattern**: Use generation flags instead of deleting files after generation.

**Good**:
```bash
python setup.py my-project --no-docker --no-memory
```

**Bad**:
```bash
python setup.py my-project
cd my-project
rm -rf Dockerfile docker-compose.yml .dockerignore  # Manual deletion
rm -rf .chora/memory
```

**Why**: Flags prevent file creation, cleaner history, no accidental deletions.

---

## Common Pitfalls

### Pitfall 1: Not Installing Dependencies Before Testing

**Problem**: Running `pytest` immediately after generation without installing package.

**Symptom**:
```bash
pytest
# ImportError: No module named 'my_project'
```

**Fix**: ALWAYS install package first:
```bash
pip install -e ".[dev]"  # Install in editable mode with dev dependencies
pytest                    # Now tests work
```

**Why**: Package must be installed (even in editable mode) for Python to find it.

---

### Pitfall 2: Using Invalid Package Names

**Problem**: Using package names with hyphens or starting with numbers.

**Bad**:
- `my-package` (hyphens not allowed in Python package names)
- `123-project` (can't start with number)

**Good**:
- `my_package` (underscores allowed)
- `project_123` (can end with number)

**Fix**: setup.py validates package names, will show error if invalid. Use underscores, not hyphens.

**Why**: Python import system requires valid identifiers (no hyphens).

---

### Pitfall 3: Skipping Validation After Generation

**Problem**: Assuming generation succeeded without checking.

**Fix**: ALWAYS run validation:
```bash
# After generation:
cd my-project

# Validation checks (30 seconds)
test -f pyproject.toml && echo "✅ pyproject.toml"
grep -r "{{" . | grep -v ".git" | wc -l  # Should be 0
pytest --collect-only                     # Should succeed
```

**Why**: Generation can fail silently (unreplaced placeholders, missing files) - validation catches issues early.

---

### Pitfall 4: Manually Editing Generated Files Before First Commit

**Problem**: Editing pyproject.toml, README.md before testing template-generated versions.

**Better Workflow**:
1. Generate project
2. Test template-generated files (pytest, pre-commit)
3. Commit template-generated state (baseline)
4. THEN customize

**Why**: First commit should be pure template output - enables clean template upgrades later.

---

### Pitfall 5: Not Tracking Template Version

**Problem**: Generating multiple projects without tracking which template version was used.

**Fix**: After every generation:
```bash
cat my-project/.chora/metadata.json | grep template_version
# Record in project notes or ledger
```

**Why**: When template upgrades (3.3.0 → 3.4.0 → 4.0.0), knowing which version generated each project enables targeted upgrade paths.

---

## Integration with Other SAPs

**SAP-008** (automation-scripts):
- Generated projects include `justfile` (if SAP-008 adopted)
- `just` commands bootstrap development workflow

**SAP-011** (docker-operations):
- Generated projects include Docker files (unless --no-docker)
- Dockerfile, docker-compose.yml, .dockerignore created

**SAP-010** (memory-system):
- Generated projects include .chora/memory/ (unless --no-memory)
- Memory system pre-configured

**SAP-009** (agent-awareness):
- Generated projects include AGENTS.md, CLAUDE.md templates
- Awareness files pre-populated with project-specific workflows

**SAP-029** (sap-generation):
- SAP-029 uses SAP-003 to generate new SAPs
- SAP generation = project generation + SAP-specific structure

---

## Support & Resources

**SAP-003 Documentation**:
- [Capability Charter](capability-charter.md) - Problem statement, scope, outcomes
- [Protocol Spec](protocol-spec.md) - Generation flow, contracts, variables (15+ vars)
- [Awareness Guide](awareness-guide.md) - Detailed agent workflows, troubleshooting
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide, customization
- [Ledger](ledger.md) - Generated project tracking, template versions

**Generation System Files**:
- [setup.py](../../../setup.py) - Generation orchestrator (443 lines)
- [blueprints/](../../../blueprints/) - Variable templates (12 files)
- [static-template/](../../../static-template/) - Complete project scaffold (100+ files)

**Related SAPs**:
- [SAP-008 (automation-scripts)](../automation-scripts/) - justfile for generated projects
- [SAP-010 (memory-system)](../memory-system/) - .chora/memory/ structure
- [SAP-011 (docker-operations)](../docker-operations/) - Docker files in generated projects
- [SAP-029 (sap-generation)](../sap-generation/) - SAP generation using SAP-003

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-003
  - 5 core workflows (Generate, Validate, Customize, Troubleshoot, Adopt)
  - User signal pattern table (7 signals → workflows)
  - 5 best practices (validate, descriptive names, version tracking, test first, flags not edits)
  - 5 common pitfalls (skip install, invalid names, skip validation, edit before commit, no version tracking)
  - Integration with SAP-008, SAP-010, SAP-011, SAP-009, SAP-029

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific tool usage patterns
2. Review [protocol-spec.md](protocol-spec.md) for generation flow and contracts
3. Try Workflow 1: Generate a test project to understand the system
4. Try Workflow 2: Validate generated project structure
