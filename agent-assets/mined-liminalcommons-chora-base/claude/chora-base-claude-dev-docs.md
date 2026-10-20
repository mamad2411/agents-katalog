# Developer Documentation - Claude-Specific Awareness

**Domain**: Developer Documentation (dev-docs)
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for contributing to chora-base.

### First-Time Contribution

1. Read [AGENTS.md](AGENTS.md) for generic development workflows
2. Use this file for Claude Code integration patterns
3. Follow TDD/BDD/DDD workflows from static-template

### Session Resumption

- Check [workflows/](workflows/) for development processes
- Read [research/](research/) for technical context
- Use Claude Code tools (Read, Write, Edit, Bash) effectively

---

## Claude Code Development Workflows

### Workflow 1: Contributing Code to Chora-Base

```markdown
User: "I want to add a new feature to chora-base"

Claude (thinking):
- User wants to contribute to chora-base itself (not use it)
- Need development workflows, not user guides
- dev-docs domain is correct

Claude (Phase 1: Orientation):
1. Read docs/dev-docs/AGENTS.md
   - Understand development process structure
2. Read docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md
   - Understand documentation standards
3. Check docs/dev-docs/patterns/
   - Find relevant code patterns

Claude (Phase 2: Implementation):
4. Follow TDD workflow (from static-template):
   - Write failing test via Write tool
   - Implement minimal code via Write tool
   - Refactor via Edit tool
5. Run tests via Bash tool:
   pytest tests/
6. Update documentation via Edit tool

Claude (Phase 3: Documentation):
7. Document learnings in research/ or patterns/
8. Commit via Bash tool
```

**Progressive Loading**: dev-docs AGENTS.md → workflows → patterns → implement

---

### Workflow 2: Understanding Chora-Base Architecture

```markdown
User: "How does chora-base work internally?"

Claude:
1. Read /CLAUDE.md (root overview)
2. Read docs/dev-docs/AGENTS.md
3. Read docs/ARCHITECTURE.md (4-domain model)
4. Read docs/dev-docs/research/CLAUDE_Complete.md (Claude learnings)
5. Explore source code as needed

Result: Comprehensive architectural understanding
```

**Tool Usage**: Read tool for all documentation, minimal source code reading

---

### Workflow 3: Researching Technical Decisions

```markdown
User: "Why does chora-base use Diataxis?"

Claude:
1. Search research/ directory:
   grep -r "Diataxis" docs/dev-docs/research/
2. Read relevant research document
3. If not found, check:
   - docs/DOCUMENTATION_PLAN.md
   - docs/user-docs/explanation/
4. Synthesize answer from multiple sources

Result: Clear rationale for technical decision
```

**Tool Usage**: Bash (grep), Read (documentation), no code changes

---

## Tool Usage Patterns for Development

### Using Read Tool

**Pattern**: Read documentation before writing code

```bash
# Architecture and patterns
Read docs/ARCHITECTURE.md
Read docs/dev-docs/patterns/{pattern}.md

# Development workflows
Read docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md
Read static-template/dev-docs/workflows/TDD.md

# Technical context
Read docs/dev-docs/research/CLAUDE_Complete.md
Read docs/dev-docs/research/adopter-learnings-executable-docs.md
```

**Why**: Understand existing patterns before adding new code

---

### Using Write Tool

**Pattern**: Write new files following TDD

```bash
# 1. Write test first (TDD)
Write tests/test_new_feature.py
# Content: Failing test for new feature

# 2. Implement minimal code
Write src/new_feature.py
# Content: Minimal implementation to pass test

# 3. Document learnings
Write docs/dev-docs/research/new-feature-learnings.md
# Content: Technical investigation and decisions
```

**Why**: TDD ensures quality, documentation captures rationale

---

### Using Edit Tool

**Pattern**: Refactor existing code incrementally

```bash
# 1. Read file first
Read src/existing_feature.py

# 2. Edit incrementally
Edit src/existing_feature.py
# Old: {specific old code}
# New: {specific new code}

# 3. Run tests
Bash: pytest tests/test_existing_feature.py

# 4. Iterate until tests pass
```

**Why**: Edit tool requires exact old_string, incremental changes are safer

---

### Using Bash Tool

**Pattern**: Run tests, validation, git operations

```bash
# Testing
pytest tests/
coverage run -m pytest
coverage report

# Linting and type checking
ruff check .
ruff format .
mypy src/

# Git operations
git add .
git commit -m "feat: Add new feature"
git push

# Package operations
pip install -e ".[dev]"
```

**Why**: Bash tool executes commands, Read/Write/Edit tools handle files

---

## Claude-Specific Development Tips

### Tip 1: Follow TDD Workflow Strictly

**Pattern**:
1. Write failing test (Write tool)
2. Implement minimal code (Write tool)
3. Refactor (Edit tool)
4. Run tests (Bash tool)
5. Repeat

**Why**: TDD catches bugs early, refactoring is safer with tests

---

### Tip 2: Document Learnings as You Go

**Pattern**:
```bash
# After investigating technical decision
Write docs/dev-docs/research/{topic}-learnings.md
# Content: What I learned, why it matters, recommendations
```

**Why**: Future Claude sessions (and humans) need context

---

### Tip 3: Check Patterns Before Writing Code

**Pattern**:
```bash
# Before implementing new feature
Read docs/dev-docs/patterns/{relevant-pattern}.md
grep -r "{similar_feature}" src/
```

**Why**: Consistency with existing codebase patterns

---

### Tip 4: Use pre-commit Hooks for Quality

**Pattern**:
```bash
# Install pre-commit hooks (once)
pre-commit install

# Hooks run automatically on commit
git commit -m "feat: New feature"
# (ruff, mypy, coverage checks run automatically)
```

**Why**: Automated quality enforcement, catch issues before push

---

### Tip 5: Read Research Documents for Context

**Pattern**:
```bash
# Before contributing, understand Claude-specific learnings
Read docs/dev-docs/research/CLAUDE_Complete.md
Read docs/dev-docs/research/adopter-learnings-executable-docs.md
```

**Why**: Avoid repeating past mistakes, leverage existing learnings

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Running Tests After Changes

**Problem**: Implementing feature without running tests

**Fix**:
```bash
# Always run tests after code changes
pytest tests/
pytest tests/test_specific.py  # Run specific test
```

---

### Pitfall 2: Skipping Documentation

**Problem**: Implementing feature without documenting rationale

**Fix**:
```bash
# After implementing feature, document:
# - Why this approach? (research/)
# - What pattern? (patterns/)
# - How to use? (workflows/)
```

---

### Pitfall 3: Not Following Code Patterns

**Problem**: Writing code that doesn't match existing patterns

**Fix**:
```bash
# Before writing code:
grep -r "{similar_feature}" src/
Read docs/dev-docs/patterns/{pattern}.md
# Follow existing patterns
```

---

### Pitfall 4: Large Refactors Without Tests

**Problem**: Refactoring without test coverage

**Fix**:
```bash
# 1. Check coverage first
coverage run -m pytest
coverage report
# 2. Add missing tests
# 3. Then refactor
```

---

### Pitfall 5: Not Using Edit Tool Correctly

**Problem**: Using Write tool to overwrite entire file instead of Edit

**Fix**:
```bash
# Don't:
Write src/file.py  # Overwrites entire file

# Do:
Read src/file.py  # Read first
Edit src/file.py  # Edit specific section
# old_string: {exact old code}
# new_string: {new code}
```

**Why**: Edit is safer, preserves unchanged code

---

## Integration with Claude Desktop

### Claude Desktop Strengths (for dev-docs)

**Best for**:
- Architectural discussions
- Design reviews
- Documentation generation
- Research exploration

**Example**:
```markdown
User: "Should we use Pydantic or dataclasses?"

Claude Desktop:
1. Discuss trade-offs
2. Research both approaches
3. Generate comparison document
4. Recommend approach with rationale
5. User approves
6. Switch to Claude Code for implementation
```

---

### Claude Code Strengths (for dev-docs)

**Best for**:
- Implementing features (TDD workflow)
- Running tests and validation
- Git operations
- File editing and refactoring

**Example**:
```markdown
User: "Implement the feature we discussed"

Claude Code:
1. Read docs/dev-docs/research/{decision}.md (context)
2. Write failing test
3. Implement feature
4. Run tests
5. Refactor
6. Commit
```

---

## Example Claude Code Session (Contributing to Chora-Base)

```markdown
User: "Add support for custom SAP templates"

Claude (thinking):
- Contributing to chora-base itself (dev-docs domain)
- Need to understand existing template system
- Follow TDD workflow

Claude (Phase 1: Research - 0-10k tokens):
1. Read docs/dev-docs/AGENTS.md
2. Read docs/skilled-awareness/sap-generation/protocol-spec.md
   - Understand current template system
3. grep -r "template" src/
   - Find existing template code

Claude (Phase 2: Design - 10-50k tokens):
4. Draft design in docs/dev-docs/research/custom-sap-templates.md
   - Problem statement
   - Solution design
   - Trade-offs

Claude (Phase 3: Implementation - 50-200k tokens):
5. Write failing test:
   Write tests/test_custom_templates.py
6. Implement feature (TDD):
   Write src/sap_templates/custom.py
7. Run tests:
   Bash: pytest tests/test_custom_templates.py
8. Refactor:
   Edit src/sap_templates/custom.py
9. Run full test suite:
   Bash: pytest tests/
10. Update documentation:
    Edit docs/skilled-awareness/sap-generation/protocol-spec.md
11. Commit:
    Bash: git add . && git commit -m "feat: Add custom SAP template support"

Claude (response to user):
"I've implemented custom SAP template support:

- Added src/sap_templates/custom.py
- Added tests (100% coverage)
- Updated SAP-029 protocol-spec.md
- Committed with tests passing

You can now use --template-dir flag with sap-generate command."

Result: Feature implemented following TDD, documented, committed
Time: 1-2 hours (comprehensive implementation)
```

---

## Support & Resources

**Development Workflows**:
- [workflows/](workflows/) - Chora-base specific processes
- [static-template/dev-docs/workflows/](../../static-template/dev-docs/workflows/) - TDD, BDD, DDD

**Technical Context**:
- [research/](research/) - Investigations and learnings
  - [CLAUDE_Complete.md](research/CLAUDE_Complete.md) - Claude learnings
  - [adopter-learnings-executable-docs.md](research/adopter-learnings-executable-docs.md) - Executable docs
- [patterns/](patterns/) - Reusable code patterns

**Architecture**:
- [../../ARCHITECTURE.md](../../ARCHITECTURE.md) - 4-domain model
- [../../README.md](../../README.md) - Project overview

**Quality Tools**:
- pre-commit hooks (ruff, mypy, coverage)
- pytest, coverage, ruff, mypy
- GitHub Actions (SAP-005)

**Related Domains**:
- [../user-docs/](../user-docs/) - End-user documentation
- [../project-docs/](../project-docs/) - Project management
- [../skilled-awareness/](../skilled-awareness/) - SAP capabilities

**Root Navigation**:
- [/CLAUDE.md](../../CLAUDE.md) - Root navigation
- [AGENTS.md](AGENTS.md) - Generic development patterns

---

## Version History

- **1.0.0** (2025-11-04): Initial domain CLAUDE.md for dev-docs
  - Claude Code development workflows
  - Tool usage patterns (Read, Write, Edit, Bash)
  - TDD/BDD/DDD integration with Claude Code
  - Common pitfalls and tips
  - Claude Desktop vs Claude Code for development

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic development workflows
2. Check [workflows/](workflows/) for specific processes
3. Read [research/](research/) for technical context (especially CLAUDE_Complete.md)
4. Follow TDD workflow: test → implement → refactor → repeat
5. Document learnings in research/ or patterns/ as you go
