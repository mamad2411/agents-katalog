---
sap_id: SAP-006
version: 1.0.0
status: draft
last_updated: 2025-11-20
progressive_loading:
  phase_1: "0-5k tokens (quick reference)"
  phase_2: "5-15k tokens (implementation)"
  phase_3: "15k+ tokens (comprehensive)"
---

# Quality Gates - Claude-Specific Awareness (SAP-006)

**SAP ID**: SAP-006
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-11-05

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "Claude (first-time orientation)"
  estimated_tokens: 5000
  estimated_time_minutes: 3
  sections:
    - "1. Quick Start for Claude"
    - "2. When to Use Quality Gates"
    - "3. Tool Integration Patterns"

phase_2_implementation:
  target_audience: "Claude implementing quality gates"
  estimated_tokens: 15000
  estimated_time_minutes: 10
  sections:
    - "4. Key Workflows (Claude Code)"
    - "5. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Claude debugging quality issues"
  estimated_tokens: 30000
  estimated_time_minutes: 20
  files_to_read:
    - "protocol-spec.md (complete ruff/mypy configuration)"
    - "capability-charter.md (design rationale)"
    - ".pre-commit-config.yaml (hook configuration)"
    - "pyproject.toml (tool settings)"
```

---

## 📖 Quick Reference

**New to SAP-006?** → Read **[README.md](README.md)** first (9-min read) for pre-commit hooks, CLI commands, and troubleshooting guide.

**This CLAUDE.md provides**: Claude Code tool patterns (Bash, Edit) for quality gate setup, fixing violations, and integration workflows.

---

## 1. Quick Start for Claude

### What is Quality Gates? (Claude perspective)

**Quality Gates (SAP-006)** provides **automated code quality enforcement** using:
- **Ruff**: Modern all-in-one linter + formatter (200x faster than legacy tools)
- **Mypy**: Strict type checking
- **Pre-commit hooks**: Automated checks before git commits

**Claude's Role**:
- Set up quality gates using **Bash tool** (pre-commit install)
- Diagnose violations using **Read tool** (check error logs)
- Fix violations using **Edit tool** (modify code)
- Configure rules using **Edit tool** (modify pyproject.toml)

---

### When Should Claude Use This?

**Use Quality Gates when**:
- User asks "set up linting" or "enforce code quality"
- Project is Python (ruff/mypy are Python-specific)
- User mentions style violations in code reviews
- User wants type checking enabled
- Project already has `.pre-commit-config.yaml` (verify setup)

**Don't use Quality Gates when**:
- Project is non-Python (JavaScript, Go, etc. need different tools)
- User explicitly wants legacy tools (flake8, black)
- Quick prototyping phase (quality gates add friction)
- User disabled pre-commit hooks intentionally

---

### Tool Integration Patterns

**Bash tool** (for commands):
```bash
# Install and run pre-commit
pre-commit install
pre-commit run --all-files

# Run specific hooks
pre-commit run ruff --all-files
pre-commit run mypy --all-files

# Update hook versions
pre-commit autoupdate
```

**Read tool** (for diagnostics):
```bash
# Check hook configuration
Read .pre-commit-config.yaml

# Check ruff/mypy settings
Read pyproject.toml

# Review error output (if pre-commit failed)
Read .git/hooks/pre-commit
```

**Edit tool** (for fixes):
```bash
# Fix code violations
Edit src/module.py
# Apply ruff suggestions, add type annotations

# Customize rules
Edit pyproject.toml
# Add ruff rule ignores, adjust line-length
```

**Write tool** (for new config):
```bash
# Only if .pre-commit-config.yaml missing
Write .pre-commit-config.yaml
# Create hook configuration

# Only if [tool.ruff] section missing
Write pyproject.toml
# Add ruff/mypy configuration
```

---

## 2. When to Use Quality Gates

### User Signal Detection

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Set up code linting" | Install pre-commit, configure ruff | Bash, Read, Edit |
| "Enforce type hints" | Configure mypy strict mode | Edit (pyproject.toml) |
| "Pre-commit hook failing" | Diagnose error, suggest fix | Read (logs), Edit (code) |
| "Linting is slow" | Migrate to ruff from flake8/black | Edit (.pre-commit-config.yaml) |
| "Need to exclude files" | Add exclusions to config | Edit (pyproject.toml, .pre-commit-config.yaml) |

---

## 3. Tool Integration Patterns

### Pattern 1: Check Before Act

**Always read configuration before modifying**:

```markdown
Step 1: Read existing config
Read .pre-commit-config.yaml
Read pyproject.toml

Step 2: Identify what needs to change
- Check if ruff already configured
- Check if mypy already configured
- Check hook versions

Step 3: Make targeted edits
Edit .pre-commit-config.yaml
# Only modify sections that need changes
```

**Don't**: Write entire config files from scratch (overwrites customizations)

---

### Pattern 2: Validate After Changes

**Always run quality checks after modifying configuration**:

```markdown
Step 1: Make configuration change
Edit pyproject.toml
# Add new ruff rule

Step 2: Test configuration
Bash: pre-commit run --all-files

Step 3: Verify success
- Check exit code (0 = success)
- Review any new violations
- Fix issues before committing
```

**Don't**: Commit config changes without testing

---

### Pattern 3: Progressive Fixing

**Fix violations incrementally, not all at once**:

```markdown
Step 1: Run checks to identify violations
Bash: pre-commit run --all-files
# Output: 50 violations across 10 files

Step 2: Let auto-fix handle what it can
Bash: ruff check --fix .
# Fixes ~40 violations automatically

Step 3: Fix remaining violations manually
Edit src/module.py
# Address violations ruff can't auto-fix

Step 4: Verify all fixed
Bash: pre-commit run --all-files
# Should pass
```

**Don't**: Try to fix all violations manually (ruff can auto-fix 80%)

---

## 4. Key Workflows (Claude Code)

### Workflow 1: Set Up Quality Gates

**Goal**: Install and configure pre-commit hooks for Python project

**Tools**: Bash (install), Read (verify), Edit (configure)

**Steps**:

1. **Verify Python project**:
   ```bash
   Bash: python --version  # Should be 3.11+
   Bash: ls pyproject.toml  # Should exist
   ```

2. **Check if pre-commit already configured**:
   ```bash
   Read .pre-commit-config.yaml
   # If exists, verify ruff and mypy hooks present
   # If missing, need to create
   ```

3. **Install pre-commit** (if needed):
   ```bash
   Bash: pip install pre-commit
   ```

4. **Verify hook configuration** (read existing):
   ```bash
   Read .pre-commit-config.yaml
   # Check for:
   # - ruff-pre-commit (with ruff and ruff-format hooks)
   # - mirrors-mypy (with mypy hook)
   # - Hook versions (should be recent)
   ```

5. **If config missing or incomplete, create/update**:
   ```bash
   # If file doesn't exist:
   Write .pre-commit-config.yaml
   # Content: Standard chora-base hook configuration

   # If file exists but hooks missing:
   Edit .pre-commit-config.yaml
   # Add missing ruff or mypy hooks
   ```

6. **Verify ruff/mypy settings in pyproject.toml**:
   ```bash
   Read pyproject.toml
   # Check for [tool.ruff] and [tool.mypy] sections
   ```

7. **If settings missing, add them**:
   ```bash
   Edit pyproject.toml
   # Add [tool.ruff] with select rules
   # Add [tool.mypy] with strict mode
   ```

8. **Install git hooks**:
   ```bash
   Bash: pre-commit install
   # Output: pre-commit installed at .git/hooks/pre-commit
   ```

9. **Run on all files to establish baseline**:
   ```bash
   Bash: pre-commit run --all-files
   # May find violations, need to fix before committing
   ```

10. **If violations found, fix them**:
    ```bash
    # Auto-fix with ruff
    Bash: ruff check --fix .

    # Manually fix remaining violations
    Edit src/module.py
    # Add type annotations, fix style issues
    ```

11. **Verify all checks pass**:
    ```bash
    Bash: pre-commit run --all-files
    # Should pass (exit code 0)
    ```

12. **Commit configuration**:
    ```bash
    Bash: git add .pre-commit-config.yaml pyproject.toml
    Bash: git commit -m "chore: Set up quality gates (SAP-006)"
    ```

**Expected Outcome**: Quality gates enforced on all future commits

**Time Estimate**: 10-15 minutes

**Common Issues**:
- **Pre-commit not installed**: Install with `pip install pre-commit`
- **Hook versions outdated**: Run `pre-commit autoupdate`
- **Many violations on first run**: Normal for existing codebase, fix incrementally

---

### Workflow 2: Diagnose and Fix Quality Violations

**Goal**: Identify and resolve violations preventing commits

**Tools**: Read (error logs), Bash (run checks), Edit (fix code)

**Steps**:

1. **User reports pre-commit hook failure**:
   ```
   User: "My commit is being blocked by pre-commit hooks"
   ```

2. **Run pre-commit to see violations**:
   ```bash
   Bash: pre-commit run --all-files
   # Output shows which hooks failed and why
   ```

3. **Read error output to categorize violations**:
   ```bash
   # Example output:
   # ruff.....................................................Failed
   # - src/module.py:10:1: F401 'os' imported but unused
   # - src/module.py:25:88: E501 line too long (95 > 88 characters)
   #
   # mypy.....................................................Failed
   # - src/module.py:15: error: Function is missing a type annotation
   ```

4. **Fix violations by category**:

   **For ruff violations (auto-fixable)**:
   ```bash
   Bash: ruff check --fix .
   # Fixes F401 (removes unused imports)
   # Fixes I001 (sorts imports)
   ```

   **For ruff violations (manual fix required)**:
   ```bash
   Read src/module.py
   # Review line 25 (E501: line too long)

   Edit src/module.py
   # Break long line into multiple lines
   ```

   **For mypy violations (add type annotations)**:
   ```bash
   Read src/module.py
   # Review line 15 (missing type annotation)

   Edit src/module.py
   # Before:
   # def calculate_total(items):
   #     return sum(items)
   #
   # After:
   # def calculate_total(items: list[float]) -> float:
   #     return sum(items)
   ```

5. **Verify fixes**:
   ```bash
   Bash: pre-commit run --all-files
   # Should pass (all violations fixed)
   ```

6. **Commit fixes**:
   ```bash
   Bash: git add .
   Bash: git commit -m "style: Fix quality gate violations"
   ```

**Expected Outcome**: All violations resolved, commit succeeds

**Time Estimate**: 5-30 minutes (depending on violation count)

**Common Violations and Fixes**:

| Violation | Fix Pattern | Tool |
|-----------|-------------|------|
| F401 (unused import) | Run `ruff check --fix` | Bash |
| E501 (line too long) | Break line or increase line-length | Edit |
| I001 (imports unsorted) | Run `ruff check --fix` | Bash |
| Mypy: untyped function | Add type annotations | Edit |
| Mypy: type mismatch | Fix return type or cast | Edit |

---

### Workflow 3: Customize Rules for Project

**Goal**: Adjust ruff/mypy rules to match project needs

**Tools**: Read (current config), Edit (modify config), Bash (test)

**Steps**:

1. **User requests customization**:
   ```
   User: "Increase line length to 100 characters"
   User: "Ignore E501 (line too long)"
   User: "Exclude temp/ directory from linting"
   ```

2. **Read current configuration**:
   ```bash
   Read pyproject.toml
   # Check [tool.ruff] and [tool.mypy] sections
   ```

3. **Make requested changes**:

   **Increase line length**:
   ```bash
   Edit pyproject.toml
   # Find [tool.ruff]
   # Change: line-length = 88
   # To:     line-length = 100
   ```

   **Ignore specific rule**:
   ```bash
   Edit pyproject.toml
   # Find [tool.ruff.lint]
   # Add: ignore = ["E501"]
   ```

   **Exclude directory**:
   ```bash
   Edit pyproject.toml
   # Find [tool.ruff]
   # Add: exclude = ["temp/"]

   Edit .pre-commit-config.yaml
   # Find ruff hooks
   # Add: exclude: ^temp/
   ```

4. **Test customizations**:
   ```bash
   Bash: pre-commit run --all-files
   # Verify changes work as expected
   # Check that excluded files are skipped
   # Check that ignored rules don't trigger
   ```

5. **If tests fail, debug**:
   ```bash
   # Check for syntax errors in pyproject.toml
   Bash: python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"

   # Check for regex errors in .pre-commit-config.yaml
   Bash: pre-commit validate-config
   ```

6. **Document customizations**:
   ```bash
   Edit pyproject.toml
   # Add comments explaining why rules were changed
   # Example:
   # [tool.ruff.lint]
   # # Ignore E501 because formatter handles line length
   # ignore = ["E501"]
   ```

7. **Commit configuration changes**:
   ```bash
   Bash: git add pyproject.toml .pre-commit-config.yaml
   Bash: git commit -m "config: Customize quality gate rules for project"
   ```

**Expected Outcome**: Quality gates tailored to project needs

**Time Estimate**: 10-20 minutes

**Common Customizations**:

| Customization | File | Section | Change |
|---------------|------|---------|--------|
| Line length | pyproject.toml | [tool.ruff] | line-length = 100 |
| Ignore rule | pyproject.toml | [tool.ruff.lint] | ignore = ["E501"] |
| Add rule category | pyproject.toml | [tool.ruff.lint] | select = ["E", "F", "B"] |
| Exclude directory | pyproject.toml + .pre-commit-config.yaml | [tool.ruff], hooks | exclude = ["temp/"] |
| Relax mypy | pyproject.toml | [tool.mypy] | strict = false |

---

## 5. Integration with Other SAPs

### SAP-003 (project-bootstrap)

**Integration**: Quality gates pre-configured in chora-base template

**Claude workflow**:
1. When bootstrapping project, verify quality gates included:
   ```bash
   Read .pre-commit-config.yaml  # Should exist
   Read pyproject.toml  # Should have [tool.ruff] and [tool.mypy]
   ```
2. After project creation, install hooks:
   ```bash
   Bash: pre-commit install
   ```
3. Run baseline check:
   ```bash
   Bash: pre-commit run --all-files
   ```

---

### SAP-005 (ci-cd-workflows)

**Integration**: CI runs same quality checks as pre-commit

**Claude workflow**:
1. Verify CI workflow includes quality checks:
   ```bash
   Read .github/workflows/quality.yml
   # Should have: pre-commit run --all-files
   ```
2. If missing, add quality gate step:
   ```bash
   Edit .github/workflows/quality.yml
   # Add pre-commit job
   ```
3. Ensure CI uses same hook versions:
   ```bash
   Read .pre-commit-config.yaml  # Check versions
   # CI should use same versions
   ```

---

### SAP-015 (task-tracking)

**Integration**: Track quality violations as tasks

**Claude workflow**:
1. Run quality checks to find violations:
   ```bash
   Bash: pre-commit run --all-files
   ```
2. Create tasks for violations:
   ```bash
   Bash: bd create "Fix mypy type errors in src/module.py" --priority 1
   Bash: bd create "Add type annotations to 10 functions" --priority 2
   ```
3. Track progress as violations are fixed
4. Close tasks when violations resolved

---

## 6. Claude-Specific Tips

### Tip 1: Let Ruff Auto-Fix Before Manual Edits

**Pattern**:
```markdown
Step 1: Run ruff auto-fix
Bash: ruff check --fix .

Step 2: Check what remains
Bash: pre-commit run ruff --all-files

Step 3: Only manually fix what ruff couldn't
Edit src/module.py
```

**Why**: Ruff fixes 80%+ of violations automatically, saves time

**Don't**: Manually fix violations like unused imports (ruff handles this)

---

### Tip 2: Read Error Output Carefully

**Pattern**:
```markdown
Step 1: Run pre-commit
Bash: pre-commit run --all-files

Step 2: Parse output to identify issue
# Example: "mypy....Failed"
# - src/module.py:15: error: Function is missing a type annotation

Step 3: Read specific line
Read src/module.py (offset=10, limit=20)
# Focus on lines 10-30 (around line 15)

Step 4: Make targeted fix
Edit src/module.py
# Add type annotation to specific function
```

**Why**: Targeted fixes faster than reading entire files

**Don't**: Read entire file when error points to specific line

---

### Tip 3: Test Configuration Changes Immediately

**Pattern**:
```markdown
Step 1: Make config change
Edit pyproject.toml
# Add ruff rule ignore

Step 2: Test immediately
Bash: pre-commit run --all-files

Step 3: Verify change works
# Check that ignored rule no longer triggers
# Check that other rules still work
```

**Why**: Catch config errors early before committing

**Don't**: Make multiple config changes without testing

---

### Tip 4: Use Read Tool for Diagnostics

**Pattern**:
```markdown
Step 1: User reports issue
User: "Pre-commit hook not working"

Step 2: Read configuration
Read .pre-commit-config.yaml
# Check hook configuration

Step 3: Read settings
Read pyproject.toml
# Check ruff/mypy settings

Step 4: Diagnose issue
# Example: Hook version outdated, wrong hook order, etc.
```

**Why**: Read tool gives complete view of configuration

**Don't**: Guess at configuration issues, always read first

---

### Tip 5: Document Why Rules Were Changed

**Pattern**:
```markdown
Step 1: Make customization
Edit pyproject.toml

Step 2: Add comment explaining why
# [tool.ruff.lint]
# # Ignore E501 because our formatter handles line length
# # and we prefer 100-char lines for readability
# ignore = ["E501"]
# line-length = 100
```

**Why**: Future Claude (or developers) understand rationale

**Don't**: Customize without explanation (confusing later)

---

## 7. Common Pitfalls

### Pitfall 1: Creating Config Files from Scratch

**Problem**: Using Write tool for existing config files (overwrites customizations)

**Symptom**:
- User complains "my custom rules disappeared"
- Previous exclusions no longer work

**Fix**:
```markdown
# Always Read first
Read .pre-commit-config.yaml

# Use Edit to modify, not Write
Edit .pre-commit-config.yaml
# Make targeted changes only
```

**Prevention**: Read before Write, Edit for modifications

---

### Pitfall 2: Not Running Auto-Fix First

**Problem**: Manually fixing violations that ruff can auto-fix

**Symptom**:
- Spending 10+ minutes manually removing unused imports
- Manually sorting imports
- Manually fixing whitespace

**Fix**:
```markdown
# Always run auto-fix first
Bash: ruff check --fix .

# Then manually fix what remains
Edit src/module.py
```

**Prevention**: Check if ruff can fix before manual editing

---

### Pitfall 3: Wrong Hook Order in Config

**Problem**: Adding ruff-format before ruff check in .pre-commit-config.yaml

**Symptom**:
- Pre-commit takes 2-3 runs to stabilize
- Code gets formatted, then changed again

**Fix**:
```markdown
Edit .pre-commit-config.yaml

# Ensure correct order:
- id: ruff          # MUST be first
  args: [--fix, --exit-non-zero-on-fix]
- id: ruff-format   # MUST be second
```

**Prevention**: Always verify hook order when editing config

---

### Pitfall 4: Not Testing Config Changes

**Problem**: Committing config changes without running pre-commit

**Symptom**:
- Config has syntax errors
- New rules cause unexpected failures
- CI fails after config change

**Fix**:
```markdown
# Always test before committing
Edit pyproject.toml
Bash: pre-commit run --all-files  # Test
Bash: git commit  # Only commit if tests pass
```

**Prevention**: Make testing part of config change workflow

---

### Pitfall 5: Not Excluding Generated Files

**Problem**: Quality checks run on generated code (API clients, protobuf, etc.)

**Symptom**:
- Pre-commit fails on files developer can't modify
- Developer manually fixes generated code (gets overwritten)

**Fix**:
```markdown
# Add exclusions to both files
Edit pyproject.toml
# [tool.ruff]
# exclude = ["generated/", "pb2.py"]

Edit .pre-commit-config.yaml
# - id: ruff
#   exclude: ^(generated/|.*pb2\.py)
```

**Prevention**: Ask user about generated files during setup

---

## 8. Quick Reference

### Common Bash Commands

```bash
# Install and setup
pre-commit install
pre-commit run --all-files

# Run specific hooks
pre-commit run ruff --all-files
pre-commit run ruff-format --all-files
pre-commit run mypy --all-files

# Auto-fix violations
ruff check --fix .

# Update hook versions
pre-commit autoupdate

# Skip hooks (emergency only)
git commit --no-verify -m "Emergency fix"
```

---

### Common Read Patterns

```bash
# Check configuration
Read .pre-commit-config.yaml
Read pyproject.toml

# Check specific line with error
Read src/module.py (offset=10, limit=20)

# Check error logs (if needed)
Read .git/hooks/pre-commit
```

---

### Common Edit Patterns

```bash
# Fix code violations
Edit src/module.py
# Add type annotations, fix style

# Customize rules
Edit pyproject.toml
# Add ignores, adjust line-length

# Update hook config
Edit .pre-commit-config.yaml
# Add exclusions, update versions
```

---

## 9. Version History

**1.0.0** (2025-11-05):
- Initial CLAUDE.md for SAP-006 (quality-gates)
- 3 workflows: setup, diagnose/fix, customize
- Integration with SAP-003, SAP-005, SAP-015
- 5 Claude-specific tips, 5 common pitfalls
- Tool usage patterns (Bash, Read, Edit, Write)

---

## Quick Links

- **AGENTS.md**: [AGENTS.md](AGENTS.md) - Generic agent patterns (5 workflows)
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete technical reference
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Design rationale
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- **Configuration Files**: `.pre-commit-config.yaml`, `pyproject.toml` (project root)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for comprehensive workflow details
2. Read [protocol-spec.md](protocol-spec.md) for complete ruff/mypy reference
3. Read [adoption-blueprint.md](adoption-blueprint.md) for step-by-step installation
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
