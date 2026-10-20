---
sap_id: SAP-003
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-100"    # Quick Start + Generate Project Workflow
  phase_2: "lines 101-220"  # Validation + Troubleshooting Workflows
  phase_3: "full"           # Complete including tips and pitfalls
phase_1_token_estimate: 3000
phase_2_token_estimate: 7000
phase_3_token_estimate: 10000
---

# Project Bootstrap (SAP-003) - Claude-Specific Awareness

**SAP ID**: SAP-003
**Claude Compatibility**: Sonnet 4.5+
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

This CLAUDE.md provides: Claude Code tool patterns (Bash, Read, Write, Edit) for project generation, validation, and error recovery.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for generating Python projects using Claude's tool suite (Bash, Read, Write, Edit).

### First-Time Generation

1. Read [AGENTS.md](AGENTS.md) for generic project generation workflows
2. Use this file for Claude Code tool integration (Bash for setup.py, Read for validation, Write for customization)
3. Generate project → validate → report to user

### Session Resumption

- Use Bash tool to run `python setup.py <target-dir>`
- Use Read tool to check generated files
- Use Glob tool to find unreplaced placeholders
- Use Edit tool to fix generation issues

---

## Claude Code Project Generation Workflows

### Workflow 1: Generating New Project with Claude Code

```markdown
User: "Create a new Python project called 'weather-mcp-server'"

Claude (Phase 1: Run Generation - 0-10k tokens):
1. Determine target directory name:
   - Convert to slug: "weather-mcp-server" ✅ (already slug format)
   - Will create: weather-mcp-server/

2. Run setup.py via Bash:
   Bash: python setup.py weather-mcp-server

3. Setup.py prompts for variables:
   # Claude responds to each prompt:
   # Project name: Weather MCP Server
   # Description: MCP server for weather data retrieval
   # Author: Your Name
   # Email: email@example.com
   # GitHub username: yourusername
   # Python version: 3.11 (accept default)
   # License: MIT (accept default)

Claude (Phase 2: Validate Generation - 10-20k tokens):
4. Change to project directory:
   Bash: cd weather-mcp-server

5. Check critical files exist:
   Bash: ls -la
   # Expected: pyproject.toml, README.md, src/, tests/, .github/

6. Check for unreplaced placeholders:
   Bash: grep -r "{{" . | grep -v ".git" | grep -v "node_modules" | wc -l
   # Expected: 0 (no unreplaced placeholders)

7. Validate package structure:
   Bash: ls -la src/
   # Expected: weather_mcp_server/ directory (underscores, not hyphens)

8. Check tests loadable:
   Bash: pytest --collect-only
   # Expected: Tests collected successfully

Claude (Phase 3: Report to User - 20-25k tokens):
9. Summarize generation results:

"✅ Project generated successfully!

**Project**: weather-mcp-server/
**Package**: weather_mcp_server
**Template Version**: 3.3.0

**Structure**:
- pyproject.toml (Python package config)
- README.md (project documentation)
- src/weather_mcp_server/ (source code)
  - __init__.py
  - server.py (MCP server entry point)
- tests/ (test suite)
  - test_server.py
- .github/workflows/ (CI/CD)
  - test.yml

**Validation**:
✅ All files created
✅ No unreplaced placeholders
✅ Tests loadable

**Next steps**:
1. cd weather-mcp-server
2. pip install -e \".[dev]\"  # Install dependencies
3. pytest                     # Run tests
4. uv run weather-mcp-server  # Start MCP server (if using uv)"

Result: User has fully functional MCP server project ready for development
```

---

### Workflow 2: Validating Generated Project with Claude Code

```markdown
User: "Check if the project I just generated is correct"

Claude (Phase 1: File Existence Checks - 0-5k tokens):
1. Read critical files to verify they exist:
   Read pyproject.toml
   Read README.md
   Read src/weather_mcp_server/__init__.py

2. If any Read fails, report missing file to user

Claude (Phase 2: Placeholder Detection - 5-10k tokens):
3. Search for unreplaced placeholders:
   Bash: find . -type f \\( -name "*.py" -o -name "*.md" -o -name "*.toml" \\) -exec grep -l "{{" {} \\; | grep -v ".git"

4. If placeholders found:
   Read <file-with-placeholder>
   # Identify which variable(s) unreplaced

Claude (Phase 3: Package Structure Validation - 10-15k tokens):
5. Verify package directory structure:
   Bash: ls -la src/
   # Check: Directory name uses underscores, not hyphens

6. Check __init__.py exists:
   Bash: test -f src/weather_mcp_server/__init__.py && echo "✅" || echo "❌"

Claude (Phase 4: Test Validation - 15-20k tokens):
7. Attempt to collect tests:
   Bash: pytest --collect-only

8. If collection fails:
   - Check pytest installed: pip list | grep pytest
   - Check package installed: pip list | grep weather-mcp-server
   - If not installed: Suggest pip install -e ".[dev]"

Claude (Phase 5: Report Results - 20-25k tokens):
9. Summarize validation:

"## Validation Results

✅ File Structure: All critical files present
✅ Placeholders: No unreplaced {{ }} found
✅ Package: src/weather_mcp_server/ correctly named
✅ Tests: 3 tests collected successfully

**Status**: Valid ✅

**Metadata**:
- Template Version: 3.3.0
- Generated: 2025-11-04
- Python: 3.11"

Result: User has confidence project generated correctly
```

---

### Workflow 3: Troubleshooting Generation Errors with Claude Code

```markdown
User: "The project generation failed - can you help?"

Claude (Phase 1: Identify Error Type - 0-5k tokens):
1. Ask user for error message or symptoms:
   "What error did you see? Or what's not working?"

2. Common error patterns:
   - "ImportError" → Package not installed
   - "{{ project_description }}" in files → Unreplaced placeholder
   - "No such file" → Missing directory
   - "Invalid package name" → Name validation failed

Claude (Phase 2: Diagnose Issue - 5-15k tokens):

**If "Unreplaced placeholders"**:
3. Find all unreplaced placeholders:
   Bash: grep -r "{{.*}}" . | grep -v ".git" | sed 's/.*{{\(.*\)}}.*/\1/' | sort -u

4. Read setup.py to check if variable defined:
   Read setup.py
   # Search for variable in variables dict

5. Identify root cause:
   - Variable not in dict → Need to add
   - Blueprint not processed → Need to add to process_blueprints()
   - Typo in variable name → Fix spelling

**If "Package not loadable"**:
6. Check if package installed:
   Bash: pip list | grep weather-mcp-server

7. If not installed:
   Bash: pip install -e ".[dev]"

8. Check package structure:
   Bash: ls -la src/weather_mcp_server/
   # Verify __init__.py exists

Claude (Phase 3: Apply Fix - 15-30k tokens):
9. Based on diagnosis, apply appropriate fix:

**Fix Example: Add missing variable**:
```python
# If project_tagline variable unreplaced:
# 1. Read setup.py
Read setup.py

# 2. Find variables dict (around line 200)
# 3. Edit to add missing variable
Edit setup.py
# old_string:
#   variables = {
#       "project_name": ...,
#       "project_description": ...,
#   }
# new_string:
#   variables = {
#       "project_name": ...,
#       "project_description": ...,
#       "project_tagline": project_description,  # Add missing variable
#   }
```

Claude (Phase 4: Verify Fix - 30-35k tokens):
10. Re-run generation:
    Bash: python setup.py weather-mcp-server-fixed

11. Validate fix worked:
    Bash: grep -r "{{" weather-mcp-server-fixed/ | grep -v ".git" | wc -l
    # Should be 0

Claude (response to user):
"Fixed generation issue!

**Problem**: Variable `project_tagline` was unreplaced
**Root Cause**: Variable not in setup.py variables dict
**Fix**: Added `project_tagline` to variables (derived from description)

**Verification**:
- Re-generated project: weather-mcp-server-fixed/
- Placeholder check: 0 unreplaced (✅)
- Tests loadable: ✅

Project is now valid!"

Result: Generation error identified, fixed, and verified
```

---

## Claude-Specific Tips

### Tip 1: Use Bash Tool for Generation, Not Write

**Pattern**:
```bash
# ALWAYS use Bash to run setup.py
Bash: python setup.py my-project

# DON'T try to generate manually with Write
# ❌ Write pyproject.toml (manual creation)
```

**Why**: setup.py orchestrates entire generation flow (copy, rename, process blueprints, validate) - Bash delegates to it correctly.

---

### Tip 2: Use Read Tool to Verify Generated Files

**Pattern**:
```bash
# After generation, Read critical files to verify content
Read pyproject.toml  # Check package name, dependencies
Read README.md       # Check project description, title
Read src/my_project/__init__.py  # Check package imports
```

**Why**: Read tool provides full file content - enables checking for unreplaced placeholders, correct variable substitution.

---

### Tip 3: Use Glob Tool for Placeholder Detection

**Pattern**:
```bash
# Find all Python/Markdown/TOML files
Glob **/*.py
Glob **/*.md
Glob **/*.toml

# For each file, check for {{ placeholders }}
Read <file>
# Search for "{{" in content
```

**Why**: Glob finds all relevant files efficiently - systematic placeholder detection.

---

### Tip 4: Use Edit Tool for Post-Generation Fixes

**Pattern**:
```bash
# If placeholder found after generation:
Read pyproject.toml

# Fix specific placeholder
Edit pyproject.toml
# old_string: description = "{{project_description}}"
# new_string: description = "Weather data MCP server"
```

**Why**: Edit tool allows surgical fixes - no need to regenerate entire project.

---

### Tip 5: Always Install Before Testing

**Pattern**:
```bash
# After generation:
Bash: cd my-project
Bash: pip install -e ".[dev]"  # Install first
Bash: pytest                    # Then test
```

**Why**: Package must be installed (even editable mode) for Python imports to work.

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Using Bash for Generation

**Problem**: Trying to create project manually with Write tool instead of running setup.py.

**Fix**: ALWAYS use Bash to run setup.py:
```bash
Bash: python setup.py my-project
```

**Why**: setup.py handles entire workflow (443 lines of logic) - manual creation misses critical steps (blueprint processing, validation, git init).

---

### Pitfall 2: Not Reading Generated Files to Verify

**Problem**: Assuming generation succeeded without checking file contents.

**Fix**: ALWAYS read critical files after generation:
```bash
Read pyproject.toml
Read README.md
Read src/my_project/__init__.py
```

**Why**: Read reveals unreplaced placeholders, incorrect variable substitution.

---

### Pitfall 3: Not Installing Package Before Running Tests

**Problem**: Running pytest immediately after generation without pip install.

**Fix**: Install first:
```bash
Bash: cd my-project
Bash: pip install -e ".[dev]"
Bash: pytest
```

**Why**: Python import system requires package installed (even in editable mode).

---

### Pitfall 4: Using Write Instead of Edit for Fixes

**Problem**: Using Write to overwrite entire file when fixing single placeholder.

**Fix**: Use Edit for surgical changes:
```bash
# BAD
Write pyproject.toml  # Overwrites entire file ❌

# GOOD
Edit pyproject.toml   # Changes specific line ✅
```

**Why**: Edit preserves file structure, only modifies target content.

---

### Pitfall 5: Not Validating Placeholder Replacement

**Problem**: Not checking for unreplaced {{ placeholders }} after generation.

**Fix**: ALWAYS check:
```bash
Bash: grep -r "{{" . | grep -v ".git" | wc -l
# Should be 0
```

**Why**: Unreplaced placeholders break functionality - early detection prevents debugging later.

---

## Support & Resources

**SAP-003 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic project generation workflows (5 workflows, user signals)
- [Capability Charter](capability-charter.md) - Problem statement, scope
- [Protocol Spec](protocol-spec.md) - Generation flow, 15+ variables, contracts
- [Adoption Blueprint](adoption-blueprint.md) - Installation, customization
- [Ledger](ledger.md) - Generated project tracking

**Generation System**:
- [setup.py](../../../setup.py) - Generation orchestrator (443 lines)
- [blueprints/](../../../blueprints/) - Variable templates (12 files)
- [static-template/](../../../static-template/) - Project scaffold (100+ files)

**Related SAPs**:
- [SAP-008 (automation-scripts)](../automation-scripts/) - justfile in generated projects
- [SAP-010 (memory-system)](../memory-system/) - .chora/memory/ structure
- [SAP-011 (docker-operations)](../docker-operations/) - Docker files option
- [SAP-029 (sap-generation)](../sap-generation/) - SAP generation using SAP-003

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-003
  - 3 Claude Code workflows (Generate, Validate, Troubleshoot)
  - Tool usage patterns (Bash for setup.py, Read for verification, Edit for fixes, Glob for placeholders)
  - 5 Claude-specific tips (Bash for generation, Read to verify, Glob for placeholders, Edit for fixes, install before test)
  - 5 common pitfalls (manual generation, skip Read, skip install, Write instead of Edit, skip placeholder check)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for comprehensive project generation workflows
2. Review [protocol-spec.md](protocol-spec.md) for generation contracts and variables
3. Try Workflow 1: Generate a test project using Bash tool
4. Try Workflow 2: Validate generated project structure
