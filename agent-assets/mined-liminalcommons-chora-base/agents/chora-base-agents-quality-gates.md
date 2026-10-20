---
sap_id: SAP-006
version: 1.0.0
status: draft
last_updated: 2025-11-20
progressive_loading:
  phase_1: "0-8k tokens (quick reference)"
  phase_2: "8-20k tokens (implementation)"
  phase_3: "20k+ tokens (comprehensive)"
---

# Quality Gates - Agent Awareness (SAP-006)

**SAP ID**: SAP-006
**Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-11-05

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "All agents (first-time orientation)"
  estimated_tokens: 8000
  estimated_time_minutes: 5
  sections:
    - "1. Quick Start for Agents"
    - "2. What You Can Do"
    - "3. When to Use This Capability"
    - "4. Common User Signals"

phase_2_implementation:
  target_audience: "Agents implementing quality gates"
  estimated_tokens: 25000
  estimated_time_minutes: 15
  sections:
    - "5. How It Works"
    - "6. Key Workflows"
    - "7. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Agents debugging or customizing quality gates"
  estimated_tokens: 50000
  estimated_time_minutes: 30
  files_to_read:
    - "protocol-spec.md (complete technical specification)"
    - "capability-charter.md (design rationale)"
    - ".pre-commit-config.yaml (hook configuration)"
    - "pyproject.toml (ruff and mypy settings)"
```

---

## 📖 Quick Reference

**New to SAP-006?** → Read **[README.md](README.md)** first (9-min read)

The README provides:
- 🚀 **Quick Start** - 3 commands to install and run pre-commit hooks
- 📚 **7 Hooks** - Complete pre-commit hook reference (ruff, mypy, file hygiene)
- 🎓 **Hook Execution Order** - Critical ordering (ruff before ruff-format)
- 🔧 **Troubleshooting** - 5 common problems with solutions
- 🔍 **Ruff vs Legacy** - 200x speed improvement comparison

**This AGENTS.md provides**: Agent-executable workflows for quality gate setup, fixing violations, and pre-commit integration.

---

## 1. Quick Start for Agents

### What is Quality Gates? (60-second overview)

**Quality Gates (SAP-006)** provides **pre-commit hooks for code quality** using modern Python tooling:

- **Ruff**: All-in-one linter + formatter (200x faster than flake8+isort+black)
- **Mypy**: Strict type checking (enforces type annotations)
- **Pre-commit hooks**: Automated quality enforcement before commits

**Purpose**: Prevent low-quality code from entering the repository by enforcing style, types, and formatting before commit.

**Key Benefits**:
- **Fast Feedback**: Ruff completes in <1s (vs 10-30s for legacy tools)
- **Consistent Quality**: Automated enforcement prevents style drift
- **Type Safety**: Mypy strict mode catches type errors early
- **Zero Config**: Pre-configured with sensible defaults

---

### When Should You Use This?

**Use Quality Gates when**:
- User asks "how do I enforce code quality?"
- Project needs automated linting/formatting
- User wants type checking for Python
- Pre-commit hooks need configuration
- Code reviews mention style violations

**Don't use Quality Gates when**:
- Working with non-Python projects (different tooling needed)
- User explicitly wants legacy tools (flake8, black, isort)
- Quick prototyping (quality gates add friction)
- Project already has established quality tooling

---

### Quick Command Reference

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run ruff-format --all-files
pre-commit run mypy --all-files

# Update hook versions
pre-commit autoupdate

# Skip hooks for emergency commits (use sparingly)
git commit --no-verify -m "Emergency fix"
```

---

## 2. What You Can Do

### Core Capabilities

1. **Automated Linting** (ruff check)
   - Enforce PEP 8 style guidelines
   - Detect unused imports, undefined names
   - Sort imports automatically
   - Fix violations automatically (`--fix` flag)

2. **Automated Formatting** (ruff format)
   - Format code consistently (replaces black)
   - 88-character line length (black default)
   - Consistent quote style, indentation

3. **Type Checking** (mypy)
   - Enforce type annotations on all functions
   - Detect type mismatches early
   - Warn when returning `Any` type
   - Strict mode (no untyped code)

4. **File Hygiene** (pre-commit-hooks)
   - Validate YAML syntax
   - Ensure files end with newlines
   - Remove trailing whitespace
   - Prevent large file commits (>500KB)

5. **Customization**
   - Add/remove ruff rule categories
   - Adjust mypy strictness
   - Exclude files/directories
   - Override hook configuration

---

### Integration Points

**SAP-003 (project-bootstrap)**:
- Quality gates pre-configured in chora-base template
- `.pre-commit-config.yaml` included
- `pyproject.toml` with ruff/mypy settings

**SAP-005 (ci-cd-workflows)**:
- GitHub Actions run same checks as pre-commit
- CI enforces quality gates for PRs
- Prevents merging code with violations

**SAP-012 (development-lifecycle)**:
- Quality gates enforce coding standards
- Integrate with code review process
- Fast feedback loop (seconds vs minutes)

**SAP-015 (task-tracking)**:
- Quality gate violations can be tracked as tasks
- "Fix mypy errors" becomes actionable work item

---

## 3. When to Use This Capability

### User Signal Pattern: Quality Enforcement

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "Code reviews always mention style issues" | Inconsistent formatting | Set up ruff pre-commit hooks |
| "How do I enforce type hints?" | Type safety needed | Configure mypy strict mode |
| "Linting is too slow" | Performance issues | Migrate from flake8/black to ruff |
| "Imports are unsorted" | Import organization | Enable ruff isort rules (I category) |
| "Need to prevent bad commits" | Quality gate missing | Install pre-commit hooks |

---

### User Signal Pattern: Debugging Quality Issues

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "Pre-commit hook failing" | Hook configuration issue | Check `.pre-commit-config.yaml` syntax |
| "Mypy error: untyped function" | Missing type annotations | Add function signatures with types |
| "Ruff error E501: line too long" | Line length violation | Reformat code or increase line-length |
| "Hook order wrong?" | ruff-format before ruff check | Reorder: ruff check MUST come first |
| "Need to skip hooks for emergency" | Urgent commit needed | Use `git commit --no-verify` |

---

## 4. Common User Signals

### Signal 1: "Code quality is inconsistent across PRs"

**Context**: Team has style guidelines but no automated enforcement

**Agent Response**:
1. Verify Python project (check for `pyproject.toml` or `setup.py`)
2. Check if pre-commit hooks already installed (`ls .pre-commit-config.yaml`)
3. If not installed, set up quality gates:
   ```bash
   # Install pre-commit
   pip install pre-commit

   # Install hooks
   pre-commit install

   # Run on all files to establish baseline
   pre-commit run --all-files
   ```
4. Commit hook configuration files
5. Update team documentation with pre-commit workflow

**Expected Outcome**: All commits automatically enforced for quality

---

### Signal 2: "Linting takes forever (10-30 seconds)"

**Context**: Using legacy tools (flake8, isort, black) instead of ruff

**Agent Response**:
1. Check current linting setup:
   ```bash
   grep -E "flake8|black|isort" pyproject.toml
   grep -E "flake8|black|isort" .pre-commit-config.yaml
   ```
2. Migrate to ruff:
   - Update `.pre-commit-config.yaml` to use ruff-pre-commit
   - Convert flake8/isort config to ruff rules in `pyproject.toml`
   - Remove legacy tool dependencies
3. Benchmark performance:
   ```bash
   time pre-commit run --all-files  # Should be <2s total
   ```
4. Document 200x speedup in commit message

**Expected Outcome**: Linting completes in <1 second

---

### Signal 3: "How do I enforce type annotations?"

**Context**: Project needs type safety but mypy not configured

**Agent Response**:
1. Check if mypy already configured:
   ```bash
   grep -A 10 "\[tool.mypy\]" pyproject.toml
   ```
2. If not configured, add strict mypy settings to `pyproject.toml`:
   ```toml
   [tool.mypy]
   python_version = "3.11"
   strict = true
   disallow_untyped_defs = true
   warn_return_any = true
   exclude = ["temp/"]
   ```
3. Add mypy to `.pre-commit-config.yaml`:
   ```yaml
   - repo: https://github.com/pre-commit/mirrors-mypy
     rev: v1.11.0
     hooks:
       - id: mypy
         args: [--config-file=pyproject.toml]
   ```
4. Run mypy to identify untyped functions:
   ```bash
   pre-commit run mypy --all-files
   ```
5. Fix type errors or add `# type: ignore` comments with justification

**Expected Outcome**: All functions have type annotations

---

### Signal 4: "Pre-commit hook failing with 'hook order' error"

**Context**: ruff-format running before ruff check (incorrect order)

**Agent Response**:
1. Open `.pre-commit-config.yaml`
2. Verify hook order in ruff-pre-commit section:
   ```yaml
   - repo: https://github.com/astral-sh/ruff-pre-commit
     rev: v0.5.5
     hooks:
       - id: ruff          # MUST be first
         args: [--fix, --exit-non-zero-on-fix]
       - id: ruff-format   # MUST be second
   ```
3. Explain rationale:
   - `ruff check --fix` modifies code to fix violations
   - `ruff-format` formats the modified code
   - Reversing order causes inconsistent results
4. Reorder hooks if needed
5. Re-run pre-commit to verify

**Expected Outcome**: Hooks run in correct order, consistent results

---

### Signal 5: "Need to exclude certain files from linting"

**Context**: Some files (generated code, temp files) shouldn't be linted

**Agent Response**:
1. Identify files to exclude (e.g., `temp/`, `generated/`)
2. Add exclusions to `.pre-commit-config.yaml`:
   ```yaml
   - id: ruff
     exclude: ^(temp/|generated/|repo-dump\.py)
   - id: ruff-format
     exclude: ^(temp/|generated/|repo-dump\.py)
   - id: mypy
     exclude: ^(temp/|generated/|repo-dump\.py)
   ```
3. Add exclusions to `pyproject.toml`:
   ```toml
   [tool.ruff]
   exclude = ["temp/", "generated/", "repo-dump.py"]

   [tool.mypy]
   exclude = ["temp/", "generated/"]
   ```
4. Verify exclusions work:
   ```bash
   pre-commit run --all-files  # Should skip excluded files
   ```

**Expected Outcome**: Excluded files bypass quality gates

---

## 5. How It Works

### Architecture Overview

Quality Gates uses **pre-commit hooks** to run quality checks before commits:

```
Developer commits code
         ↓
Pre-commit hooks triggered
         ↓
1. Basic file checks (YAML, whitespace, large files)
         ↓
2. Ruff linting (check violations, auto-fix)
         ↓
3. Ruff formatting (consistent style)
         ↓
4. Mypy type checking (strict mode)
         ↓
All checks pass → Commit succeeds
Any check fails → Commit blocked (fix issues first)
```

---

### Hook Execution Order (CRITICAL)

**Correct order** (enforced in `.pre-commit-config.yaml`):

1. **pre-commit-hooks** (basic file hygiene)
   - check-yaml
   - end-of-file-fixer
   - trailing-whitespace
   - check-added-large-files

2. **ruff** (linting with auto-fix)
   - Check violations (E, F, I, N, W, UP rules)
   - Auto-fix when possible (`--fix` flag)

3. **ruff-format** (formatting)
   - Format code consistently
   - Apply after ruff check fixes code

4. **mypy** (type checking)
   - Check type annotations
   - Strict mode (all functions must be typed)

**Why this order?**:
- Basic checks first (fast, catch simple errors)
- Ruff check before format (fixes logical issues before styling)
- Mypy last (slowest, checks types after code is clean)

---

### Ruff Rule Categories

Quality Gates uses 6 rule categories (configured in `pyproject.toml`):

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

**E (pycodestyle errors)**:
- Indentation, whitespace, line length
- Example: E501 (line too long)

**F (pyflakes)**:
- Unused imports, undefined names
- Example: F401 (imported but unused)

**I (isort)**:
- Import sorting and organization
- Example: I001 (imports unsorted)

**N (pep8-naming)**:
- Naming conventions (PEP 8)
- Example: N802 (function name should be lowercase)

**W (pycodestyle warnings)**:
- Trailing whitespace, blank line issues
- Example: W291 (trailing whitespace)

**UP (pyupgrade)**:
- Modern Python syntax (3.11+ features)
- Example: UP006 (use `list` instead of `List`)

---

### Mypy Strict Mode

Quality Gates enforces **strict type checking**:

```toml
[tool.mypy]
python_version = "3.11"
strict = true                    # Enable all strict checks
disallow_untyped_defs = true     # All functions must have types
warn_return_any = true           # Warn if returning Any
```

**What strict mode catches**:
- Functions without type annotations
- Return types that are `Any` (too broad)
- Type mismatches between function signatures
- Missing types for variables, attributes

**Module overrides** (for third-party libraries):
```toml
[[tool.mypy.overrides]]
module = ["fastmcp", "fastmcp.*"]
ignore_missing_imports = true
```

---

## 6. Key Workflows

### Workflow 1: Initial Setup (First-Time Installation)

**Goal**: Install and configure quality gates for a Python project

**Steps**:

1. **Verify prerequisites**:
   ```bash
   python --version  # Should be 3.11+
   pip --version
   ```

2. **Install pre-commit**:
   ```bash
   pip install pre-commit
   ```

3. **Verify `.pre-commit-config.yaml` exists**:
   ```bash
   cat .pre-commit-config.yaml
   # Should contain ruff-pre-commit and mypy hooks
   ```

4. **Install git hooks**:
   ```bash
   pre-commit install
   # Output: pre-commit installed at .git/hooks/pre-commit
   ```

5. **Run on all files** (establish baseline):
   ```bash
   pre-commit run --all-files
   # May find violations, fix them before committing
   ```

6. **Commit hook configuration**:
   ```bash
   git add .pre-commit-config.yaml pyproject.toml
   git commit -m "chore: Set up quality gates (SAP-006)"
   ```

7. **Verify hooks work**:
   - Make a small code change
   - Try to commit (hooks should run automatically)
   - Fix any violations
   - Commit succeeds

**Expected Outcome**: Quality gates enforced on all future commits

**Time Estimate**: 10-15 minutes

---

### Workflow 2: Running Quality Checks Manually

**Goal**: Run quality checks without committing

**Steps**:

1. **Run all hooks**:
   ```bash
   pre-commit run --all-files
   ```

2. **Run specific hook**:
   ```bash
   # Linting only
   pre-commit run ruff --all-files

   # Formatting only
   pre-commit run ruff-format --all-files

   # Type checking only
   pre-commit run mypy --all-files
   ```

3. **Check specific files**:
   ```bash
   pre-commit run --files src/module.py tests/test_module.py
   ```

4. **Debug hook failures**:
   ```bash
   # Show detailed output
   pre-commit run --verbose --all-files

   # Show which files failed
   pre-commit run --show-diff-on-failure --all-files
   ```

5. **Update hook versions**:
   ```bash
   pre-commit autoupdate
   # Updates .pre-commit-config.yaml with latest versions
   ```

**Expected Outcome**: Quality checks run on-demand, violations identified

**Time Estimate**: 1-5 minutes

---

### Workflow 3: Fixing Ruff Violations

**Goal**: Resolve linting errors identified by ruff

**Steps**:

1. **Run ruff to identify violations**:
   ```bash
   pre-commit run ruff --all-files
   # Output shows violations with codes (E501, F401, etc.)
   ```

2. **Let ruff auto-fix** (when possible):
   ```bash
   # Ruff automatically fixes on pre-commit
   # Or manually:
   ruff check --fix .
   ```

3. **Fix remaining violations manually**:
   ```bash
   # Example: E501 (line too long)
   # Break line into multiple lines

   # Example: F401 (unused import)
   # Remove the import

   # Example: I001 (imports unsorted)
   # Let ruff --fix handle this
   ```

4. **Verify fixes**:
   ```bash
   pre-commit run ruff --all-files
   # Should show no violations
   ```

5. **Commit fixes**:
   ```bash
   git add .
   git commit -m "style: Fix ruff violations"
   ```

**Common Violations and Fixes**:

| Code | Violation | Fix |
|------|-----------|-----|
| E501 | Line too long (>88 chars) | Break line or increase line-length in config |
| F401 | Imported but unused | Remove import or add `# noqa: F401` |
| F841 | Variable assigned but never used | Remove variable or rename to `_` |
| I001 | Imports unsorted | Run `ruff check --fix` |
| N802 | Function name not lowercase | Rename function (snake_case) |

**Expected Outcome**: All ruff violations resolved

**Time Estimate**: 5-30 minutes (depending on violation count)

---

### Workflow 4: Fixing Mypy Type Errors

**Goal**: Resolve type checking errors identified by mypy

**Steps**:

1. **Run mypy to identify type errors**:
   ```bash
   pre-commit run mypy --all-files
   # Output shows type errors with line numbers
   ```

2. **Common mypy errors and fixes**:

   **Error: Function is missing a type annotation**
   ```python
   # Before (error)
   def calculate_total(items):
       return sum(items)

   # After (fixed)
   def calculate_total(items: list[float]) -> float:
       return sum(items)
   ```

   **Error: Returning Any**
   ```python
   # Before (warning)
   def get_data() -> Any:
       return fetch_from_api()

   # After (fixed)
   def get_data() -> dict[str, str]:
       return fetch_from_api()
   ```

   **Error: Type mismatch**
   ```python
   # Before (error)
   def process(value: int) -> str:
       return value  # Error: returning int, expected str

   # After (fixed)
   def process(value: int) -> str:
       return str(value)
   ```

3. **Add type ignore for third-party libraries**:
   ```python
   from untyped_library import module  # type: ignore[import-untyped]
   ```

4. **Configure module overrides** (if many imports from library):
   ```toml
   # pyproject.toml
   [[tool.mypy.overrides]]
   module = ["untyped_library", "untyped_library.*"]
   ignore_missing_imports = true
   ```

5. **Verify type errors resolved**:
   ```bash
   pre-commit run mypy --all-files
   # Should show no errors
   ```

6. **Commit type fixes**:
   ```bash
   git add .
   git commit -m "types: Add type annotations for mypy strict mode"
   ```

**Expected Outcome**: All mypy errors resolved, full type coverage

**Time Estimate**: 15-60 minutes (depending on codebase size)

---

### Workflow 5: Customizing Quality Gate Rules

**Goal**: Adjust ruff/mypy rules for project-specific needs

**Steps**:

1. **Review current rules**:
   ```bash
   grep -A 10 "\[tool.ruff" pyproject.toml
   grep -A 10 "\[tool.mypy\]" pyproject.toml
   ```

2. **Add new ruff rule categories**:
   ```toml
   # pyproject.toml
   [tool.ruff.lint]
   select = [
     "E",   # pycodestyle errors
     "F",   # pyflakes
     "I",   # isort
     "N",   # pep8-naming
     "W",   # pycodestyle warnings
     "UP",  # pyupgrade
     "B",   # flake8-bugbear (new)
     "C90", # mccabe complexity (new)
   ]
   ```

3. **Ignore specific rules**:
   ```toml
   [tool.ruff.lint]
   ignore = [
     "E501",  # Line too long (handled by formatter)
     "N806",  # Variable naming (project uses different convention)
   ]
   ```

4. **Adjust line length**:
   ```toml
   [tool.ruff]
   line-length = 100  # Default is 88
   ```

5. **Relax mypy strictness** (if needed):
   ```toml
   [tool.mypy]
   strict = false  # Disable strict mode
   disallow_untyped_defs = false  # Allow untyped functions
   ```

6. **Test customizations**:
   ```bash
   pre-commit run --all-files
   # Verify new rules work as expected
   ```

7. **Document customizations**:
   ```toml
   # pyproject.toml
   [tool.ruff.lint]
   # Ignore E501 because formatter handles line length
   ignore = ["E501"]
   ```

8. **Commit configuration changes**:
   ```bash
   git add pyproject.toml
   git commit -m "config: Customize quality gate rules for project"
   ```

**Expected Outcome**: Quality gates tailored to project needs

**Time Estimate**: 10-20 minutes

---

## 7. Integration with Other SAPs

### SAP-003 (project-bootstrap)

**Integration**: Quality gates pre-configured in chora-base template

**Files included**:
- `.pre-commit-config.yaml` - Hook configuration
- `pyproject.toml` - Ruff and mypy settings

**Agent workflow**:
1. When bootstrapping new project, verify quality gates included
2. Run `pre-commit install` after project creation
3. Run `pre-commit run --all-files` to verify setup

---

### SAP-005 (ci-cd-workflows)

**Integration**: GitHub Actions run same quality checks as pre-commit

**CI workflow** (`.github/workflows/quality.yml`):
```yaml
name: Quality Gates
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pre-commit
      - run: pre-commit run --all-files
```

**Agent workflow**:
1. Set up CI to run pre-commit checks
2. Ensure CI uses same hook versions as local
3. Block PRs if quality checks fail

---

### SAP-012 (development-lifecycle)

**Integration**: Quality gates enforce coding standards throughout development

**Development workflow**:
1. Developer writes code
2. Pre-commit hooks run on commit (fast feedback)
3. CI runs same checks on push (gatekeeper)
4. Code review focuses on logic (not style)

**Agent workflow**:
1. Recommend quality gates during project setup
2. Document quality standards in development guide
3. Update style guide based on ruff rules

---

### SAP-015 (task-tracking)

**Integration**: Quality gate violations can be tracked as tasks

**Example tasks**:
- "Fix mypy type errors in src/module.py"
- "Reduce complexity of function (C901 violation)"
- "Add type annotations to 10 untyped functions"

**Agent workflow**:
1. Run quality checks to identify violations
2. Create tasks for each category of violations
3. Track progress using beads
4. Close tasks as violations are fixed

---

## 8. Best Practices

### Best Practice 1: Run Quality Checks Locally Before Pushing

**Why**: Catch violations early (seconds) vs CI feedback (minutes)

**How**:
```bash
# Before pushing
pre-commit run --all-files

# Or set up as git pre-push hook
pre-commit install --hook-type pre-push
```

**Benefit**: Prevents CI failures, cleaner git history

---

### Best Practice 2: Use Ruff's Auto-Fix Feature

**Why**: Ruff can fix 80%+ of violations automatically

**How**:
```bash
# Ruff auto-fixes on pre-commit by default
# Or manually:
ruff check --fix .
```

**Don't**: Manually fix violations that ruff can auto-fix (waste of time)

**Benefit**: Faster violation resolution, consistent style

---

### Best Practice 3: Add Type Annotations Incrementally

**Why**: Strict mypy on large codebase is overwhelming

**How**:
1. Start with new code (all new functions typed)
2. Add types to modified functions (incremental improvement)
3. Set aside time for "type annotation sprints" (bulk improvement)

**Don't**: Try to type entire codebase at once (too slow)

**Benefit**: Gradual improvement, manageable workload

---

### Best Practice 4: Document Rule Customizations

**Why**: Future developers need to understand why rules were changed

**How**:
```toml
# pyproject.toml
[tool.ruff.lint]
# Ignore E501 because our formatter handles line length
# and we use 100-char lines for better readability
ignore = ["E501"]
line-length = 100
```

**Don't**: Customize rules without explanation (confusing)

**Benefit**: Clear rationale, easier to review/modify later

---

### Best Practice 5: Keep Hook Versions Updated

**Why**: New hook versions include bug fixes and new features

**How**:
```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Review changes
git diff .pre-commit-config.yaml

# Test updates
pre-commit run --all-files

# Commit if tests pass
git commit -m "chore: Update pre-commit hook versions"
```

**Frequency**: Monthly or quarterly

**Benefit**: Better performance, new features, bug fixes

---

## 9. Common Pitfalls

### Pitfall 1: Wrong Hook Order (ruff-format before ruff)

**Problem**: Formatter runs before linter, causing inconsistent results

**Symptom**:
- Code gets formatted, then linter changes it again
- Pre-commit hooks take 2-3 runs to stabilize

**Fix**:
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  hooks:
    - id: ruff          # MUST be first
      args: [--fix, --exit-non-zero-on-fix]
    - id: ruff-format   # MUST be second
```

**Prevention**: Always check hook order when configuring pre-commit

---

### Pitfall 2: Skipping Hooks Too Often

**Problem**: Using `git commit --no-verify` to bypass quality gates

**Symptom**:
- Quality violations accumulate
- CI starts failing
- Code reviews focus on style issues

**Fix**:
- Only use `--no-verify` for emergencies
- Fix violations instead of skipping
- If hooks too slow, investigate why (usually misconfiguration)

**Prevention**: Make quality checks fast (<5s total) so developers don't skip

---

### Pitfall 3: Not Excluding Generated Files

**Problem**: Linting/formatting generated code (API clients, protobuf, etc.)

**Symptom**:
- Pre-commit hooks fail on generated files
- Developers manually fix generated code (waste of time)
- Regeneration breaks fixes

**Fix**:
```yaml
# .pre-commit-config.yaml
- id: ruff
  exclude: ^(generated/|pb2\.py$|temp/)
- id: mypy
  exclude: ^(generated/|pb2\.py$|temp/)
```

**Prevention**: Identify generated files early, add exclusions immediately

---

### Pitfall 4: Mixing Legacy Tools with Ruff

**Problem**: Using flake8/black/isort alongside ruff (conflicts, slow)

**Symptom**:
- Pre-commit takes 10-30 seconds (should be <2s)
- Conflicting style rules between tools
- Duplicate configuration in multiple files

**Fix**:
1. Remove legacy tools from `.pre-commit-config.yaml`
2. Migrate config to `pyproject.toml` under `[tool.ruff]`
3. Remove flake8/black/isort from dependencies

**Prevention**: When adopting ruff, fully migrate (don't keep old tools)

---

### Pitfall 5: Overly Strict Mypy on Legacy Codebase

**Problem**: Enabling strict mypy on untyped codebase (100+ errors)

**Symptom**:
- Developers overwhelmed by type errors
- Type annotations added incorrectly (just to pass checks)
- Development velocity drops

**Fix**:
1. Start with lenient mypy (strict = false)
2. Gradually increase strictness (enable one check at a time)
3. Add types incrementally (new code first, then modified code)
4. Use `# type: ignore` sparingly with justification

**Prevention**: Match mypy strictness to codebase maturity

---

## 10. Self-Evaluation

### Workflow Coverage Analysis

**Protocol Spec Workflows**: 5 (specified in protocol-spec.md)
1. Initial setup (install pre-commit, configure hooks)
2. Running checks manually (pre-commit run)
3. Fixing violations (ruff auto-fix, manual fixes)
4. Customizing rules (pyproject.toml configuration)
5. Updating hooks (pre-commit autoupdate)

**AGENTS.md Workflows**: 5 (implemented above)
1. Initial Setup (First-Time Installation)
2. Running Quality Checks Manually
3. Fixing Ruff Violations
4. Fixing Mypy Type Errors
5. Customizing Quality Gate Rules

**CLAUDE.md Workflows**: 3 (to be implemented in CLAUDE.md)
1. Set Up Quality Gates (Bash + Read + Write tools)
2. Diagnose and Fix Quality Violations (Read + Edit tools)
3. Customize Rules for Project (Read + Edit tools)

**Coverage**: 5/5 = 100% (all protocol-spec workflows covered)

**Variance**: 40% (5 generic workflows vs 3 Claude-specific workflows)

**Rationale**: CLAUDE.md focuses on tool-specific patterns (Bash/Read/Write/Edit), while AGENTS.md provides comprehensive step-by-step guidance applicable to all agents. Both provide equivalent support for SAP-006 adoption.

**Conclusion**: ✅ Equivalent support across agent types

---

## 11. Version History

**1.0.0** (2025-11-05):
- Initial AGENTS.md for SAP-006 (quality-gates)
- 5 workflows: setup, manual checks, ruff fixes, mypy fixes, customization
- Integration with SAP-003, SAP-005, SAP-012, SAP-015
- 5 best practices, 5 common pitfalls
- Progressive context loading frontmatter

---

## Quick Links

- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete technical reference
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Design rationale
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- **Configuration**: `.pre-commit-config.yaml`, `pyproject.toml` (project root)
- **SAP Framework**: [../sap-framework/](../sap-framework/) - SAP artifact standards

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code tool patterns
2. Read [protocol-spec.md](protocol-spec.md) for complete specification
3. Read [adoption-blueprint.md](adoption-blueprint.md) for installation steps
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
