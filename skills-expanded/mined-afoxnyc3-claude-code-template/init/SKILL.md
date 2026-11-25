---
name: init
description: Bootstrap CLAUDE.md by analyzing the current codebase structure
allowed-tools: Bash, Read, Glob, Grep, Write
disable-model-invocation: true
---

# Initialize Project Context

Analyze the current codebase and generate a customized CLAUDE.md file.

## Instructions

### Step 1: Analyze Project Structure

```bash
# Find project type indicators
ls -la
cat package.json 2>/dev/null | head -20
cat pyproject.toml 2>/dev/null | head -20
cat Cargo.toml 2>/dev/null | head -20
cat go.mod 2>/dev/null | head -20

# Find existing documentation
ls README* 2>/dev/null
ls docs/ 2>/dev/null

# Identify directory structure
find . -type d -maxdepth 2 | grep -v node_modules | grep -v .git | grep -v __pycache__ | grep -v .venv | head -30

# Find test directories
find . -type d -name "test*" -o -name "*tests" 2>/dev/null | head -10

# Check for existing Claude config
ls -la .claude/ 2>/dev/null
cat CLAUDE.md 2>/dev/null
```

### Step 2: Detect Tech Stack

Identify:
- **Language**: Python, TypeScript, Go, Rust, etc.
- **Framework**: FastAPI, Express, React, etc.
- **Build tools**: npm, poetry, cargo, etc.
- **Test runner**: pytest, vitest, jest, etc.
- **Linter**: ruff, eslint, golint, etc.

### Step 3: Extract Commands

Find available commands from:
- `package.json` scripts
- `pyproject.toml` scripts
- `Makefile` targets
- `Justfile` recipes
- Existing CI/CD configs

### Step 4: Generate CLAUDE.md

Create a CLAUDE.md with:

```markdown
# CLAUDE.md - Project Context for AI Agents

## Project Overview

**[Project Name]** is [detected description from README or package.json].

## Architecture Summary

- **[Component 1]**: [detected from directory structure]
- **[Component 2]**: [detected from directory structure]

## Quick Reference

### Required Environment
\`\`\`bash
[detected from .env.example or docs]
\`\`\`

### Common Commands
\`\`\`bash
# Lint
[detected lint command]

# Format
[detected format command]

# Test
[detected test command]

# Build
[detected build command]
\`\`\`

## Hierarchical Context

Claude Code auto-loads:
- `.claude/rules/*.md` - Project-wide rules
- `[component]/CLAUDE.md` - Component-specific context
- `knowledge/` - Domain expertise

## Testing Strategy

[detected from test structure]

## Acceptance Criteria

Before marking a task complete:
1. Code compiles/runs without errors
2. Tests pass
3. Linting passes
4. Committed and pushed
```

### Step 5: Offer to Create Supporting Files

Ask if user wants to also create:
- `.claude/rules/01-code-standards.md` (based on detected stack)
- `.claude/settings.json` (with appropriate hooks)
- `knowledge/` directory structure

## Output

After generating CLAUDE.md, display:

```markdown
## Project Initialized

**Detected Stack**: [language] + [framework]
**Test Runner**: [tool]
**Linter**: [tool]

### Files Created
- CLAUDE.md (project context)

### Recommended Next Steps
1. Review and customize CLAUDE.md
2. Add component-specific CLAUDE.md files
3. Create knowledge skills for your domain
4. Run `/prime` to load context
```
