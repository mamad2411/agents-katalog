# Fix All Errors - Python Genesis Project Orchestration

Execute a comprehensive parallel fix operation for all lint, format, typecheck, and test errors in Python genesis projects.

## EXECUTION WORKFLOW

### Step 1: Error Collection & Analysis
```bash
# Capture all errors from genesis project quality checks
make lint > /tmp/lint_errors.txt 2>&1
make typecheck > /tmp/typecheck_errors.txt 2>&1
make test > /tmp/test_errors.txt 2>&1
make format --dry-run > /tmp/format_errors.txt 2>&1 || true
```

Analyze the error output and categorize into distinct fix domains specific to Python development.

### Step 2: Agent Creation & Deployment

Based on error analysis, create and immediately deploy these Python-specialized agents:

#### Agent 1: python-import-fixer
**Context Package:**
```
ERRORS: All import-related errors from flake8 (F401, F811, E401, etc.)
FILES: Extract unique file paths from import errors
INSTRUCTION: "Fix ONLY Python import issues:
- Remove unused imports (F401)
- Fix wildcard imports (F403)
- Resolve import order violations (E401)
- Add missing imports for undefined names (F821)
- Do NOT modify any logic or non-import code
- Validate with: make lint | grep -E 'F40[13]|E401|F821'"
```

#### Agent 2: black-format-fixer
**Context Package:**
```
ERRORS: All formatting violations that black would fix
FILES: Files that need black formatting
INSTRUCTION: "Fix ONLY code formatting issues:
- Apply black formatting standards
- Fix line length violations (E501)
- Correct indentation (E111, E117)
- Fix whitespace issues (E202, E203, W291)
- Do NOT change any logic, only formatting
- Run: black [files] then validate with: make format --check"
```

#### Agent 3: isort-import-organizer
**Context Package:**
```
ERRORS: Import sorting violations from isort or flake8
FILES: Files with import organization issues
INSTRUCTION: "Fix ONLY import organization:
- Sort imports according to isort configuration
- Group imports correctly (stdlib, third-party, local)
- Fix import section spacing
- Do NOT modify import content, only organization
- Run: isort [files] then validate with: isort --check-only [files]"
```

#### Agent 4: flake8-style-fixer
**Context Package:**
```
ERRORS: Style violations from flake8 (E2xx, E3xx, W2xx, W3xx)
FILES: Files with style violations
INSTRUCTION: "Fix ONLY flake8 style issues:
- Fix variable naming (N8xx)
- Resolve complexity issues (C901) by refactoring
- Fix docstring issues (D1xx)
- Address whitespace violations
- Do NOT change functionality, only style
- Validate with: make lint | grep -E 'E[23][0-9][0-9]|W[23][0-9][0-9]|N8|C901|D1'"
```

#### Agent 5: mypy-type-fixer
**Context Package:**
```
ERRORS: All mypy type checking errors and warnings
FILES: Files with type annotation issues
INSTRUCTION: "Fix ONLY type checking issues:
- Add missing type annotations
- Fix incorrect type hints
- Resolve type compatibility issues
- Add proper return type annotations
- Use Union, Optional, Generic correctly
- Do NOT change runtime behavior
- Validate with: make typecheck"
```

#### Agent 6: pytest-test-fixer
**Context Package:**
```
ERRORS: All pytest test failures and errors
FILES: Test files and their corresponding source files
INSTRUCTION: "Fix ONLY test failures:
- Update failing assertions
- Fix test setup/teardown issues
- Resolve fixture problems
- Update test data for current behavior
- Add missing test dependencies
- Do NOT change test intent, only fix failures
- Validate with: make test"
```

#### Agent 7: python-logic-fixer
**Context Package:**
```
ERRORS: Logic errors from flake8 (F6xx, F7xx, F8xx)
FILES: Files with logic/semantic errors
INSTRUCTION: "Fix ONLY Python logic issues:
- Remove unused variables (F841)
- Fix undefined names (F821)
- Resolve duplicate argument names (F831)
- Fix break/continue outside loops (F701)
- Do NOT change intended functionality
- Validate with: make lint | grep -E 'F[678][0-9][0-9]'"
```

#### Agent 8: coverage-test-enhancer
**Context Package:**
```
ERRORS: Coverage gaps and missing test scenarios
FILES: Source files with low coverage
INSTRUCTION: "Enhance ONLY test coverage:
- Add tests for uncovered code paths
- Create missing test cases
- Ensure edge cases are tested
- Do NOT modify source code functionality
- Validate with: make test-cov"
```

### Step 3: Parallel Execution Command

Launch ALL agents simultaneously with their Python-specific contexts:

```
Deploying Python quality fix agents in parallel:

@python-import-fixer: [import errors from flake8]
@black-format-fixer: [formatting violations]
@isort-import-organizer: [import sorting issues]
@flake8-style-fixer: [style violations E2xx, E3xx, W2xx, W3xx]
@mypy-type-fixer: [type checking errors]
@pytest-test-fixer: [test failures and errors]
@python-logic-fixer: [logic errors F6xx, F7xx, F8xx]
@coverage-test-enhancer: [coverage enhancement needs]
```

### Step 4: Genesis Project Validation Sequence

After all agents complete, run the full quality pipeline:

```bash
# Run complete quality check pipeline
echo "🔧 Running format fixes..."
make format

echo "🧹 Validating lint status..."
make lint > /tmp/lint_final.txt 2>&1

echo "🔍 Checking types..."
make typecheck > /tmp/typecheck_final.txt 2>&1

echo "🧪 Running tests..."
make test > /tmp/test_final.txt 2>&1

echo "📊 Checking coverage..."
make test-cov > /tmp/coverage_final.txt 2>&1

# Full quality check
echo "✅ Running complete quality suite..."
make quality
```

### Step 5: Genesis-Specific Conflict Prevention

**CRITICAL: Python-specific boundaries:**
1. **Import fixers** work only on import statements (top of files)
2. **Format fixers** change only whitespace/structure, not content
3. **Type fixers** add annotations, don't change logic
4. **Test fixers** modify only test files and test data
5. **Logic fixers** address semantic errors without changing intent

### Step 6: Result Aggregation & Reporting

```bash
# Compare before/after for each quality metric
echo "📈 GENESIS PROJECT QUALITY REPORT"
echo "=================================="
echo "Lint (flake8):"
echo "  BEFORE: $(grep -c . /tmp/lint_errors.txt 2>/dev/null || echo 0) issues"
echo "  AFTER:  $(grep -c . /tmp/lint_final.txt 2>/dev/null || echo 0) issues"

echo "Type Check (mypy):"
echo "  BEFORE: $(grep -c . /tmp/typecheck_errors.txt 2>/dev/null || echo 0) errors"
echo "  AFTER:  $(grep -c . /tmp/typecheck_final.txt 2>/dev/null || echo 0) errors"

echo "Tests (pytest):"
echo "  BEFORE: $(grep -c FAILED /tmp/test_errors.txt 2>/dev/null || echo 0) failures"
echo "  AFTER:  $(grep -c FAILED /tmp/test_final.txt 2>/dev/null || echo 0) failures"

# Check if ready for release pipeline
if make quality &>/dev/null; then
    echo "✅ All quality checks passed - ready for 'make release'"
else
    echo "❌ Quality issues remain - check individual reports"
fi
```

## GENESIS PROJECT MANAGER RESPONSIBILITIES

You orchestrate the Python development quality pipeline:

1. **Tool Integration**: Leverage black, isort, flake8, mypy, pytest
2. **Release Readiness**: Ensure all fixes support `make quality` success
3. **Python Best Practices**: Maintain PEP 8, type hints, test coverage
4. **Build Pipeline**: Prepare for `make build` and `make release`
5. **Conflict Prevention**: Ensure formatting tools don't conflict with logic fixes

## INVOCATION EXAMPLE

User: `/fix-all-errors`

Your response:
```
🐍 Initiating Python Genesis quality fix operation...

📊 Quality Analysis:
- Running make lint... found 47 flake8 issues across 12 files
- Running make typecheck... found 23 mypy errors across 8 files
- Running make test... found 5 pytest failures across 3 test files
- Checking format... found 15 files needing black/isort

🤖 Creating 8 Python-specialized agents for parallel execution...

📝 Categorizing by tool domain:
- Import fixes: 12 F401/F821 errors → python-import-fixer
- Format fixes: 15 files → black-format-fixer
- Import sorting: 8 files → isort-import-organizer
- Style violations: 20 E/W errors → flake8-style-fixer
- Type errors: 23 mypy issues → mypy-type-fixer
- Test failures: 5 pytest failures → pytest-test-fixer
- Logic errors: 7 F6xx/F7xx issues → python-logic-fixer
- Coverage gaps: 3 modules < 80% → coverage-test-enhancer

🚦 Launching Python agents in parallel...
[Deploy each agent with Python-specific contexts]

⏳ Monitoring progress across quality pipeline...
✅ All Python agents completed

🔧 Running final quality validation...
✅ make format: Applied successfully
✅ make lint: 47 → 0 issues
✅ make typecheck: 23 → 0 errors
✅ make test: 5 → 0 failures
✅ make test-cov: Coverage maintained at 95%
✅ make quality: All checks passed

📈 Genesis Project Ready for Release Pipeline!
```

## PYTHON-SPECIFIC ERROR HANDLING

If Python agents report conflicts:
1. **Format conflicts**: Run black/isort first, then logic fixes
2. **Import conflicts**: Separate unused removal from new additions
3. **Type conflicts**: Apply type fixes after logic changes
4. **Test conflicts**: Update tests after source changes
5. **Use git diff**: Review all changes before committing

## Integration with Genesis Build Pipeline

This command prepares your project for:
- ✅ `make quality` - All quality checks pass
- ✅ `make build` - Ready for package building
- ✅ `make release` - Ready for version bump and release
- ✅ Clean CI/CD pipeline execution

## Quick Usage:
```bash
# In Claude Code:
/fix-all-errors

# The command will:
# 1. Run all genesis quality checks (lint, typecheck, test, format)
# 2. Parse and categorize Python-specific errors
# 3. Create specialized Python agents
# 4. Deploy them in parallel with tool-specific contexts
# 5. Validate with complete quality pipeline
# 6. Report readiness for release workflow
```

This ensures your Python genesis projects maintain the highest quality standards while maximizing parallel efficiency and preventing tool conflicts.
