---
sap_id: SAP-005
version: 2.0.0
status: draft
last_updated: 2025-11-20
progressive_loading:
  phase_1: "0-5k tokens (quick reference, common commands)"
  phase_2: "5-12k tokens (CI workflows, debugging)"
  phase_3: "12k+ tokens (comprehensive, optimization)"
---

# CI/CD Workflows (SAP-005) - Claude-Specific Awareness

**SAP ID**: SAP-005
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-005?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - 4 CLI commands for checking CI status (ci-status, ci-logs, ci-workflows, ci-trigger) with <5 min feedback
- 📚 **Time Savings** - Automated quality gates catch 95%+ issues before merge, <5 min execution vs manual testing
- 🎯 **10 Workflows** - Complete GitHub Actions inventory (test, lint, smoke, security, release, deployment)
- 🔧 **6 CLI Commands** - ci-status, ci-logs, ci-retry, ci-workflows, ci-workflow-show, ci-trigger for workflow management
- 📊 **Success Metrics** - <5 min feedback, 85%+ coverage enforced, 100% security scans, 80-90% cache hit rate
- 🔗 **Integration** - Works with SAP-004 (Testing), SAP-006 (Quality Gates), SAP-028 (Publishing), SAP-011 (Docker)

This CLAUDE.md provides: Claude Code tool patterns (Edit workflows, Bash gh commands, Read logs) for CI/CD automation.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for GitHub Actions workflows.

### First-Time CI/CD Setup

1. Read [AGENTS.md](AGENTS.md) for generic CI/CD workflows
2. Use this file for Claude Code tool integration (Edit, Bash for gh commands, Read for debugging)
3. Follow 3-step process: Copy workflows → Customize → Test via PR → Enforce as required

### Session Resumption

- Check .github/workflows/ for existing workflows
- Use Bash tool for gh commands (run list, view logs, rerun)
- Use Edit tool to update workflow files (matrix, steps, env vars)
- Use Read tool to debug workflow failures (read logs, identify issues)

---

## Claude Code CI/CD Workflows

### Workflow 1: Setting Up CI/CD with Claude Code

```markdown
User: "Set up GitHub Actions CI/CD for this project"

Claude (Phase 1: Check Existing - 0-5k tokens):
1. Check existing workflows:
   Bash: ls -la .github/workflows/
2. Read project structure:
   Bash: ls -la src/ tests/
3. Read pyproject.toml (identify package name)

Claude (Phase 2: Copy Workflows - 5-15k tokens):
4. Copy workflows from static-template:
   Bash: mkdir -p .github/workflows
   Bash: cp /path/to/static-template/.github/workflows/*.yml .github/workflows/
5. List copied workflows:
   Bash: ls -la .github/workflows/

Claude (Phase 3: Customize Workflows - 15-30k tokens):
6. Read test.yml to identify customization points:
   Read .github/workflows/test.yml
7. Edit test.yml to update package name:
   Edit .github/workflows/test.yml
   # old_string: pytest --cov=src/{{ package_name }}
   # new_string: pytest --cov=src/chora_utils
8. Verify customization:
   Read .github/workflows/test.yml (check coverage path)

Claude (Phase 4: Test Workflows - 30-50k tokens):
9. Create feature branch:
   Bash: git checkout -b feature/add-ci-cd
10. Add workflows:
    Bash: git add .github/workflows/
11. Commit:
    Bash: git commit -m "feat: Add GitHub Actions CI/CD workflows (test, lint, smoke, security)"
12. Push and create PR:
    Bash: git push origin feature/add-ci-cd
    Bash: gh pr create --title "Add CI/CD workflows" --body "Sets up test, lint, smoke, docs, security workflows"
13. Monitor workflow runs:
    Bash: gh run list --limit 5

Claude (Phase 5: Verify Workflows - 50-60k tokens):
14. Check workflow status:
    Bash: gh run watch
15. If all pass, merge PR:
    Bash: gh pr merge --squash

Claude (response to user):
"I've set up GitHub Actions CI/CD for this project:

✅ 8 workflows added:
   - test.yml (matrix: Python 3.11, 3.12, 3.13, coverage ≥85%)
   - lint.yml (ruff + mypy)
   - smoke.yml (quick validation)
   - docs-quality.yml (markdown validation)
   - codeql.yml (security scanning)
   - dependency-review.yml (dependency security)
   - release.yml (PyPI publishing)
   - dependabot-automerge.yml (Dependabot automation)

✅ All workflows passed on PR
✅ Branch protection: Require test, lint, smoke, security workflows to pass

Next: Configure branch protection rules to enforce workflows as required checks."

Result: Project has comprehensive CI/CD automation
```

---

### Workflow 2: Debugging Workflow Failures with Claude Code

```markdown
User: "GitHub Actions test workflow failed on my PR"

Claude (Phase 1: Identify Failure - 0-5k tokens):
1. List recent runs:
   Bash: gh run list --workflow=test.yml --limit 5
2. Get run ID of failed workflow
3. View failed run:
   Bash: gh run view <run-id>

Claude (Phase 2: Read Logs - 5-20k tokens):
4. View detailed logs:
   Bash: gh run view <run-id> --log | grep -A 10 "FAILED"
5. Identify failure type:
   - "FAILED tests/..." → Test failure (assertion error)
   - "Coverage: XX% (below 85%)" → Coverage failure
   - "ruff check" → Lint failure
   - "mypy" → Type error

Claude (Phase 3: Diagnose - 20-40k tokens):
# Scenario A: Test failure
6. Read test file:
   Read tests/utils/test_validation.py
7. Read implementation:
   Read src/utils/validation.py
8. Identify issue in implementation or test

# Scenario B: Coverage failure
6. Run coverage locally to see missing lines:
   Bash: pytest --cov=src/chora_utils --cov-report=term-missing
7. Identify uncovered lines

Claude (Phase 4: Fix - 40-60k tokens):
# Fix implementation or add tests
9. Edit implementation:
   Edit src/utils/validation.py
   # Fix bug identified in step 8
10. Or add test:
    Edit tests/utils/test_validation.py
    # Add test for uncovered branch

Claude (Phase 5: Verify Fix - 60-70k tokens):
11. Run tests locally:
    Bash: pytest tests/utils/test_validation.py -v
12. Check coverage:
    Bash: pytest --cov=src/chora_utils --cov-report=term-missing
13. Verify ≥85% coverage

Claude (Phase 6: Push Fix - 70-75k tokens):
14. Commit fix:
    Bash: git add src/utils/validation.py tests/utils/test_validation.py
    Bash: git commit -m "fix: Correct email validation, add branch test (coverage 86%)"
15. Push:
    Bash: git push
16. Monitor re-run:
    Bash: gh run watch

Claude (response to user):
"Fixed test workflow failure:

Issue: test_validate_email assertion error + coverage 83% < 85%
Fix:
  - Corrected email validation logic in src/utils/validation.py:42
  - Added test for edge case in tests/utils/test_validation.py:67
  - Coverage now 86% ✅

Workflow re-running... ✅ All checks passed!"

Result: Test workflow passes after fix
```

---

### Workflow 3: Customizing Workflows with Claude Code

```markdown
User: "Add Python 3.10 support to test matrix"

Claude (Phase 1: Read Current Workflow - 0-5k tokens):
1. Read test.yml:
   Read .github/workflows/test.yml
2. Identify matrix configuration:
   # Current:
   strategy:
     matrix:
       python-version: ["3.11", "3.12", "3.13"]

Claude (Phase 2: Update Matrix - 5-10k tokens):
3. Edit test.yml to add Python 3.10:
   Edit .github/workflows/test.yml
   # old_string: python-version: ["3.11", "3.12", "3.13"]
   # new_string: python-version: ["3.10", "3.11", "3.12", "3.13"]

Claude (Phase 3: Test Change - 10-20k tokens):
4. Create branch:
   Bash: git checkout -b feature/add-python-3.10
5. Commit change:
   Bash: git add .github/workflows/test.yml
   Bash: git commit -m "feat: Add Python 3.10 support to test matrix"
6. Push and create PR:
   Bash: git push origin feature/add-python-3.10
   Bash: gh pr create --title "Add Python 3.10 support" --body "Extends test matrix to Python 3.10-3.13"
7. Monitor workflow:
   Bash: gh run watch

Claude (Phase 4: Verify - 20-25k tokens):
8. Check all matrix jobs pass:
   Bash: gh run view <run-id>
   # Verify: test (3.10) ✅, test (3.11) ✅, test (3.12) ✅, test (3.13) ✅

Claude (response to user):
"Added Python 3.10 support to test matrix:

✅ Updated test.yml matrix: Python 3.10, 3.11, 3.12, 3.13
✅ All matrix jobs passed on PR
✅ Project now validates Python 3.10-3.13 compatibility

Workflow runs on every push/PR, testing 4 Python versions in parallel."

Result: Test matrix expanded to Python 3.10-3.13
```

---

### Workflow 4: Adding Security Scanning with Claude Code

```markdown
User: "Add CodeQL security scanning to this project"

Claude (Phase 1: Check Existing - 0-5k tokens):
1. List workflows:
   Bash: ls .github/workflows/
   # Output: test.yml, lint.yml (missing codeql.yml)

Claude (Phase 2: Copy Security Workflows - 5-10k tokens):
2. Copy CodeQL workflow:
   Bash: cp /path/to/static-template/.github/workflows/codeql.yml .github/workflows/
3. Copy dependency review workflow:
   Bash: cp /path/to/static-template/.github/workflows/dependency-review.yml .github/workflows/

Claude (Phase 3: Verify Configuration - 10-15k tokens):
4. Read codeql.yml:
   Read .github/workflows/codeql.yml
5. Verify language configuration (should be Python):
   # Check: language: python ✅

Claude (Phase 4: Test Security Workflows - 15-30k tokens):
6. Create branch:
   Bash: git checkout -b feature/add-security-scanning
7. Add workflows:
   Bash: git add .github/workflows/codeql.yml .github/workflows/dependency-review.yml
8. Commit:
   Bash: git commit -m "feat: Add CodeQL and dependency review security scanning"
9. Push and create PR:
   Bash: git push origin feature/add-security-scanning
   Bash: gh pr create --title "Add security scanning" --body "Adds CodeQL and dependency review workflows"
10. Monitor workflows (CodeQL may take 3-5 min):
    Bash: gh run watch

Claude (Phase 5: Review Results - 30-40k tokens):
11. Check CodeQL results:
    Bash: gh run view <run-id> --log | grep -i "vulnerabilities\\|found\\|alert"
12. Check dependency review:
    Bash: gh run view <run-id> --log | grep -i "vulnerable"

Claude (response to user):
"Added security scanning workflows:

✅ CodeQL (static analysis):
   - Language: Python
   - Queries: security-extended
   - Status: ✅ No vulnerabilities found

✅ Dependency Review (dependency security):
   - Status: ✅ No vulnerable dependencies

Workflows run on every PR, blocking merge if vulnerabilities detected.

Next: Configure branch protection to require CodeQL and Dependency Review as required checks."

Result: Security scanning active on all PRs
```

---

### Workflow 5: Optimizing Workflow Performance with Claude Code

```markdown
User: "Workflows are slow (~4 min), can you speed them up?"

Claude (Phase 1: Analyze Performance - 0-5k tokens):
1. Check workflow run times:
   Bash: gh run list --workflow=test.yml --limit 5 | awk '{print $1, $NF}'
2. View detailed timing for slowest workflow:
   Bash: gh run view <run-id>
   # Identify slow steps (e.g., "Install dependencies" 3m 30s)

Claude (Phase 2: Identify Optimization - 5-10k tokens):
3. Read test.yml:
   Read .github/workflows/test.yml
4. Check if caching present:
   # If no caching step → Add pip caching
   # If caching present → Check other optimizations

Claude (Phase 3: Add Pip Caching - 10-20k tokens):
5. Edit test.yml to add caching:
   Edit .github/workflows/test.yml
   # old_string: (step after "Set up Python")
   # new_string: (add caching step):
   - name: Cache pip dependencies
     uses: actions/cache@v4
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
       restore-keys: |
         ${{ runner.os }}-pip-

Claude (Phase 4: Add Parallel Test Execution - 20-30k tokens):
6. Read pyproject.toml to check for pytest-xdist:
   Read pyproject.toml
7. If missing, add pytest-xdist:
   Edit pyproject.toml
   # old_string: [project.optional-dependencies] dev = [...]
   # new_string: Add "pytest-xdist>=3.5.0"
8. Edit test.yml to use parallel execution:
   Edit .github/workflows/test.yml
   # old_string: pytest --cov=...
   # new_string: pytest -n auto --cov=...

Claude (Phase 5: Test Optimization - 30-45k tokens):
9. Create branch:
   Bash: git checkout -b perf/optimize-workflows
10. Commit changes:
    Bash: git add .github/workflows/test.yml pyproject.toml
    Bash: git commit -m "perf: Add pip caching and parallel test execution"
11. Push and create PR:
    Bash: git push origin perf/optimize-workflows
    Bash: gh pr create --title "Optimize workflow performance" --body "Adds pip caching and pytest-xdist for faster tests"
12. Monitor first run (cold cache):
    Bash: gh run watch
13. Get timing:
    Bash: gh run view <run-id> | grep "Duration"

Claude (Phase 6: Measure Improvement - 45-50k tokens):
14. Trigger second run to test warm cache:
    Bash: gh pr comment <pr-number> --body "/rerun"
15. Compare timings:
    # Before: 4m 15s
    # After (cold): 3m 45s (15% faster)
    # After (warm): 1m 50s (57% faster) ✅

Claude (response to user):
"Optimized workflow performance:

Changes:
1. ✅ Added pip caching (actions/cache@v4)
   - Key: pyproject.toml hash
   - Cache invalidation: Automatic on dependency changes

2. ✅ Added parallel test execution (pytest-xdist)
   - Pytest -n auto (uses all CPU cores)

Results:
- Before: 4m 15s
- After (cold cache): 3m 45s (15% faster)
- After (warm cache): 1m 50s (57% faster) ✅

Target <2 min: ✅ Achieved (1m 50s)

Future runs benefit from warm cache (most common case)."

Result: Workflow execution time reduced from 4m 15s → 1m 50s (57% faster)
```

---

## Claude-Specific Tips

### Tip 1: Use Bash for gh Commands

**Pattern**:
```bash
# List workflow runs
Bash: gh run list --workflow=test.yml --limit 5

# View workflow run
Bash: gh run view <run-id>

# Watch workflow run in real-time
Bash: gh run watch

# View workflow logs
Bash: gh run view <run-id> --log

# Rerun failed workflow
Bash: gh run rerun <run-id>

# Create PR
Bash: gh pr create --title "Title" --body "Description"

# Merge PR
Bash: gh pr merge --squash
```

**Why**: Bash tool executes gh CLI commands for workflow management

---

### Tip 2: Use Edit for Workflow Customization

**Pattern**:
```bash
# Read workflow first
Read .github/workflows/test.yml

# Edit specific section (not full rewrite)
Edit .github/workflows/test.yml
# old_string: python-version: ["3.11", "3.12", "3.13"]
# new_string: python-version: ["3.10", "3.11", "3.12", "3.13"]
```

**Why**: Edit tool preserves workflow structure, avoids overwriting entire file

---

### Tip 3: Use Read to Debug Workflow Failures

**Pattern**:
```bash
# Read workflow logs
Bash: gh run view <run-id> --log | grep "FAILED"

# Read test file to understand failure
Read tests/utils/test_validation.py

# Read implementation to find bug
Read src/utils/validation.py
```

**Why**: Read tool provides context for diagnosing failures

---

### Tip 4: Monitor Workflows with gh run watch

**Pattern**:
```bash
# Push commit, then watch workflow
Bash: git push
Bash: gh run watch

# Or watch specific workflow
Bash: gh run watch --workflow=test.yml
```

**Why**: Real-time feedback on workflow status

---

### Tip 5: Use grep to Filter Workflow Logs

**Pattern**:
```bash
# Find test failures
Bash: gh run view <run-id> --log | grep -A 10 "FAILED"

# Find coverage issues
Bash: gh run view <run-id> --log | grep -i "coverage"

# Find security issues
Bash: gh run view <run-id> --log | grep -i "vulnerabilities\\|alert"
```

**Why**: Large logs, grep filters to relevant sections

---

## Common Pitfalls for Claude Code

### Pitfall 1: Overwriting Workflow Files Instead of Editing

**Problem**: Using Write tool to replace test.yml, losing matrix/caching configuration

**Fix**: Use Edit tool for incremental changes

```bash
# BAD
Write .github/workflows/test.yml  # Overwrites entire file

# GOOD
Read .github/workflows/test.yml  # Check current content
Edit .github/workflows/test.yml  # Modify specific section
```

---

### Pitfall 2: Not Checking Workflow Status Before Declaring Success

**Problem**: Pushing changes but not verifying workflows pass

**Fix**: Always monitor workflow runs

```bash
# After push, ALWAYS:
Bash: gh run watch

# Or check status:
Bash: gh run list --limit 1
```

---

### Pitfall 3: Not Reading Logs for Failure Diagnosis

**Problem**: Workflow fails, but not reading logs to understand why

**Fix**: Read logs with grep for relevant errors

```bash
# ALWAYS read logs for failed workflows:
Bash: gh run view <run-id> --log | grep -A 10 "FAILED\\|ERROR"
```

---

### Pitfall 4: Not Testing Workflow Changes Locally

**Problem**: Edit workflow, push, GitHub Actions fails with syntax error

**Fix**: Validate workflow syntax or use act for local testing

```bash
# Option 1: Validate syntax (actionlint)
Bash: actionlint .github/workflows/test.yml

# Option 2: Test locally (act)
Bash: act -j test
```

---

### Pitfall 5: Not Customizing Package Name in Coverage Path

**Problem**: Copied test.yml from template, coverage path still shows {{ package_name }}

**Fix**: Edit coverage path to actual package name

```bash
# Read workflow
Read .github/workflows/test.yml

# Edit coverage path
Edit .github/workflows/test.yml
# old_string: pytest --cov=src/{{ package_name }}
# new_string: pytest --cov=src/chora_utils
```

---

## Support & Resources

**SAP-005 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic CI/CD workflows
- [Capability Charter](capability-charter.md) - Design principles, guarantees
- [Protocol Spec](protocol-spec.md) - Workflow specifications, best practices
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide (10 min setup)
- [Ledger](ledger.md) - Workflow usage, success rates, performance tracking

**External Resources**:
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Official docs
- [gh CLI](https://cli.github.com/) - GitHub CLI for workflow management
- [act](https://github.com/nektos/act) - Local GitHub Actions testing
- [actionlint](https://github.com/rhysd/actionlint) - Workflow syntax validator

**Related SAPs**:
- [SAP-004 (testing-framework)](../testing-framework/) - pytest configuration enforced by workflows
- [SAP-028 (publishing-automation)](../publishing-automation/) - PyPI publishing via release.yml
- [SAP-006 (quality-gates)](../quality-gates/) - Quality standards enforced by workflows

**Templates**:
- `.github/workflows/test.yml` - Matrix testing workflow
- `.github/workflows/lint.yml` - Code quality workflow
- `.github/workflows/codeql.yml` - Security scanning workflow

---

## Version History

- **2.0.0** (2025-11-04): Initial CLAUDE.md for SAP-005
  - Claude Code workflows (setup, debug, customize, security, optimize)
  - Tool usage patterns (Edit for workflows, Bash for gh commands, Read for debugging)
  - Claude-specific tips (gh CLI, Edit incremental, Read logs, gh run watch, grep filtering)
  - Common pitfalls (overwrite vs edit, check status, read logs, test locally, customize coverage)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic CI/CD workflows
2. Review [protocol-spec.md](protocol-spec.md) for workflow specifications
3. Check [capability-charter.md](capability-charter.md) for design principles
4. Set up workflows: Copy from static-template → Customize → Test via PR → Enforce as required
