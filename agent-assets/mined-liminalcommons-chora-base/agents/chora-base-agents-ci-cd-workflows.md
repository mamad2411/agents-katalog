---
sap_id: SAP-005
version: 2.0.0
status: draft
last_updated: 2025-11-20
progressive_loading:
  phase_1: "0-5k tokens (quick reference, workflows)"
  phase_2: "5-12k tokens (implementation patterns)"
  phase_3: "12k+ tokens (comprehensive, CI optimization)"
---

# CI/CD Workflows (SAP-005) - Agent Awareness

**SAP ID**: SAP-005
**Version**: 2.0.0
**Status**: Draft
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

This AGENTS.md provides: Agent-executable workflows for CI setup, debugging failures, triggering releases, and monitoring builds.

### What is CI/CD Workflows?

**CI/CD Workflows** = Comprehensive GitHub Actions automation for testing, quality, security, and deployment

SAP-005 provides:
- 8 GitHub Actions workflows (test, lint, smoke, docs, security, release, dependabot)
- Matrix testing across Python 3.11, 3.12, 3.13
- Quality gates (≥85% coverage, ruff + mypy, security scans)
- Parallel execution with pip caching for speed
- Integration with SAP-004 (testing), SAP-028 (publishing)

### When to Use CI/CD Workflows

✅ **Use SAP-005 for**:
- Setting up GitHub Actions for Python projects
- Enforcing quality gates on pull requests
- Running security scans (CodeQL, dependency review)
- Automating PyPI publishing on releases
- Understanding workflow failures and fixes

❌ **Don't use for**:
- Non-GitHub CI/CD systems (CircleCI, GitLab CI, etc.)
- Self-hosted runners (SAP-005 uses GitHub-hosted runners)
- Non-Python projects (workflows Python-specific)
- Advanced deployment strategies (blue-green, canary)

---

## Common Workflows

### Workflow 1: Setting Up CI/CD for New Project

**Context**: You have a new Python project and want to add GitHub Actions workflows for testing, linting, and security

**Research First** (Optional but recommended):
```bash
# Research CI/CD best practices before setup
just research "CI/CD best practices: GitHub Actions, trunk-based development, DORA metrics"

# Use research to inform workflow design:
# - DORA metrics → add deployment frequency tracking
# - Decision playbooks → choose between matrix vs separate jobs
# - Anti-patterns → avoid flaky tests, excessive builds
```

**Steps**:
1. Copy workflow files from static-template/.github/workflows/ to project:
   - test.yml (matrix testing, coverage)
   - lint.yml (ruff, mypy)
   - smoke.yml (quick validation)
   - docs-quality.yml (markdown validation)
   - codeql.yml (security scanning)
   - dependency-review.yml (dependency security)
   - release.yml (PyPI publishing)
   - dependabot-automerge.yml (Dependabot automation)

2. Customize workflows for project:
   - Update package_name in test.yml coverage path
   - Configure Dependabot in .github/dependabot.yml
   - Add CODECOV_TOKEN secret if using Codecov

3. Create pull request to test workflows:
   - Push feature branch
   - Open pull request
   - Verify all required workflows pass (test, lint, smoke, codeql, dependency-review)

4. Merge pull request after workflows pass:
   - Required: test.yml ✅, lint.yml ✅, smoke.yml ✅, codeql.yml ✅, dependency-review.yml ✅
   - Recommended: docs-quality.yml ✅

**Result**: Project has comprehensive CI/CD automation with quality gates enforced on every pull request

**Example (chora-utils)**:
```markdown
Context: New chora-utils project needs GitHub Actions

Step 1: Copy workflows
$ cp static-template/.github/workflows/*.yml chora-utils/.github/workflows/
$ cd chora-utils

Step 2: Customize test.yml
# Update coverage path:
pytest --cov=src/chora_utils --cov-report=xml --cov-fail-under=85

Step 3: Test workflows
$ git checkout -b feature/add-ci-cd
$ git add .github/workflows/
$ git commit -m "feat: Add GitHub Actions CI/CD workflows"
$ git push origin feature/add-ci-cd
$ gh pr create --title "Add CI/CD workflows" --body "Sets up test, lint, smoke, security workflows"

# GitHub Actions runs:
- test.yml (Python 3.11, 3.12, 3.13) ✅
- lint.yml (ruff + mypy) ✅
- smoke.yml (quick tests) ✅
- codeql.yml (security) ✅
- dependency-review.yml (deps) ✅
- docs-quality.yml (markdown) ✅

Step 4: Merge after all pass
$ gh pr merge --squash
```

**Outcome**: chora-utils has CI/CD automation, all PRs now require workflows to pass before merge

---

### Workflow 2: Debugging Workflow Failures

**Context**: GitHub Actions workflow failed on pull request, need to diagnose and fix

**Steps**:
1. Identify which workflow failed:
   - Check GitHub Actions tab
   - Note workflow name (test.yml, lint.yml, etc.)

2. Read workflow logs:
   - Click failed workflow run
   - Expand failed step
   - Note error message

3. Diagnose failure type:
   - Test failure: pytest output shows failing test
   - Coverage failure: Coverage <85% message
   - Lint failure: ruff or mypy errors
   - Security failure: CodeQL or dependency vulnerabilities

4. Fix issue locally:
   - Reproduce failure: `pytest tests/` or `ruff check src/` or `mypy src/`
   - Fix code based on error
   - Verify fix: Re-run command locally until passing

5. Push fix and re-run workflow:
   - Commit fix
   - Push to same branch
   - GitHub Actions automatically re-runs workflows

**Result**: Workflow passes after fix, pull request can be merged

**Example (test.yml failure)**:
```markdown
Context: Pull request workflow failed with "test.yml - Python 3.12" failure

Step 1: Identify workflow
# GitHub Actions tab shows: "Test / test (3.12)" failed

Step 2: Read logs
# Failed step: "Run tests with coverage"
# Error:
FAILED tests/utils/test_validation.py::test_validate_email - AssertionError: assert False is True
Coverage: 83.2% (below 85% threshold)

Step 3: Diagnose
# Two issues:
1. test_validate_email failing (assertion error)
2. Coverage 83.2% < 85%

Step 4: Fix locally
$ pytest tests/utils/test_validation.py::test_validate_email -v
# Fix implementation in src/utils/validation.py
# Add test for uncovered branch

$ pytest --cov=src/chora_utils --cov-report=term-missing
# Coverage now 86.1% ✅

Step 5: Push fix
$ git add src/utils/validation.py tests/utils/test_validation.py
$ git commit -m "fix: Correct email validation, add branch test (coverage 86.1%)"
$ git push

# GitHub Actions re-runs:
- test.yml (Python 3.11, 3.12, 3.13) ✅ All pass
```

**Outcome**: Test workflow passes after fixing test and coverage issues

---

### Workflow 3: Customizing Workflows for Project-Specific Needs

**Context**: Project needs custom workflow configuration (different Python versions, additional steps, custom secrets)

**Steps**:
1. Read workflow file to understand structure:
   - Identify trigger conditions (on: push, pull_request)
   - Note matrix configuration (Python versions)
   - Understand steps (checkout, setup, install, test)

2. Identify customization point:
   - Change Python versions: Update matrix.python-version
   - Add environment variables: Add env: section
   - Add secrets: Add to repository secrets, reference in workflow
   - Add steps: Insert new step in jobs.<job_id>.steps

3. Test customization locally (if possible):
   - Install act (GitHub Actions local runner): `brew install act`
   - Run workflow locally: `act -j test`
   - Verify customization works

4. Deploy customization via pull request:
   - Edit .github/workflows/<workflow>.yml
   - Create PR with customization
   - Verify workflow runs with new configuration
   - Merge after validation

**Result**: Workflow customized for project needs while preserving quality gates

**Example (add Python 3.10 support)**:
```markdown
Context: Project needs to support Python 3.10 in addition to 3.11-3.13

Step 1: Read test.yml
# Current matrix:
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]

Step 2: Identify customization
# Change: Add "3.10" to matrix

Step 3: Test locally (optional)
$ act -j test
# Verifies workflow syntax valid

Step 4: Deploy via PR
$ edit .github/workflows/test.yml
# Change matrix to:
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12", "3.13"]

$ git add .github/workflows/test.yml
$ git commit -m "feat: Add Python 3.10 support to test matrix"
$ git push
$ gh pr create --title "Add Python 3.10 support" --body "Extends test matrix to Python 3.10-3.13"

# GitHub Actions runs test matrix with Python 3.10, 3.11, 3.12, 3.13
# Verify all pass before merge
```

**Outcome**: Test workflow now validates Python 3.10 compatibility on every PR

---

### Workflow 4: Adding Security Scanning to Existing Project

**Context**: Project has test/lint workflows but missing security scans (CodeQL, dependency review)

**Steps**:
1. Check existing workflows:
   - List .github/workflows/ files
   - Note missing workflows (codeql.yml, dependency-review.yml)

2. Copy security workflows from static-template:
   - Copy codeql.yml (static security analysis)
   - Copy dependency-review.yml (dependency vulnerabilities)

3. Configure CodeQL for project language:
   - Update language: python in codeql.yml
   - Verify queries: uses: security-extended (comprehensive scan)

4. Test security workflows:
   - Create pull request with security workflows
   - Verify CodeQL scan completes (may take 3-5 minutes)
   - Verify dependency-review runs (30-60 seconds)
   - Review any vulnerabilities found

5. Enforce security workflows as required:
   - Repository Settings → Branches → Branch protection rules
   - Check "Require status checks to pass"
   - Select: CodeQL, Dependency Review

**Result**: Security vulnerabilities automatically detected on every pull request

**Example (add CodeQL)**:
```markdown
Context: Project has test.yml and lint.yml but no security scanning

Step 1: Check existing workflows
$ ls .github/workflows/
test.yml  lint.yml  # Missing codeql.yml, dependency-review.yml

Step 2: Copy security workflows
$ cp static-template/.github/workflows/codeql.yml .github/workflows/
$ cp static-template/.github/workflows/dependency-review.yml .github/workflows/

Step 3: Configure CodeQL
# codeql.yml already configured for Python, no changes needed

Step 4: Test security workflows
$ git checkout -b feature/add-security-scanning
$ git add .github/workflows/codeql.yml .github/workflows/dependency-review.yml
$ git commit -m "feat: Add CodeQL and dependency review security scanning"
$ git push origin feature/add-security-scanning
$ gh pr create --title "Add security scanning" --body "Adds CodeQL and dependency review workflows"

# GitHub Actions runs:
- codeql.yml ✅ (no vulnerabilities found)
- dependency-review.yml ✅ (no vulnerable dependencies)

Step 5: Enforce as required (GitHub web UI)
# Repository Settings → Branches → main → Edit branch protection
# ✅ Require status checks: CodeQL, Dependency Review
```

**Outcome**: All future PRs blocked until security scans pass (zero vulnerabilities)

---

### Workflow 5: Optimizing Workflow Performance

**Context**: Workflows slow (>5 minutes), want to reduce execution time with caching and parallelization

**Steps**:
1. Identify slow workflows:
   - Check GitHub Actions workflow run times
   - Note workflows >2 minutes

2. Add pip caching (if not present):
   - Add actions/cache@v4 step before pip install
   - Key cache by pyproject.toml hash
   - Restore keys for partial cache hits

3. Enable parallel execution:
   - Ensure workflows are independent (don't depend on each other)
   - GitHub Actions runs independent workflows in parallel automatically
   - For dependent workflows, use needs: keyword

4. Optimize test execution:
   - Use pytest-xdist for parallel test execution: `pytest -n auto`
   - Run fast tests first: `pytest -x` (stop on first failure)
   - Skip slow tests on PR, run on merge: Use workflow conditionals

5. Monitor performance improvement:
   - Compare workflow run times before/after optimization
   - Target: <2 min for test, <1 min for lint, <5 min total

**Result**: Workflows execute faster, improving developer feedback loop

**Example (add caching to test.yml)**:
```markdown
Context: test.yml takes 4 minutes, want to reduce to <2 minutes with caching

Step 1: Check current time
# GitHub Actions shows: test.yml duration = 4m 15s
# Most time in "Install dependencies" step (3m 30s)

Step 2: Add pip caching
$ edit .github/workflows/test.yml
# Add after "Set up Python" step:
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-

Step 3: Parallel execution (already enabled)
# Matrix testing (Python 3.11, 3.12, 3.13) runs in parallel

Step 4: Optimize tests (add pytest-xdist)
# pyproject.toml:
[project.optional-dependencies]
dev = [
    "pytest-xdist>=3.5.0",
]

# test.yml:
- name: Run tests with coverage
  run: pytest -n auto --cov=src/chora_utils --cov-report=xml --cov-fail-under=85

Step 5: Monitor improvement
# After optimization:
- First run (cold cache): 3m 45s (15% faster)
- Subsequent runs (warm cache): 1m 50s (57% faster) ✅

# Deploy optimization:
$ git commit -m "perf: Add pip caching and parallel test execution"
$ git push
```

**Outcome**: test.yml execution time reduced from 4m 15s → 1m 50s (57% faster)

---

## Workflow Patterns Reference

### Matrix Testing Pattern

**Purpose**: Test across multiple Python versions to ensure compatibility

**Pattern**:
```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]

steps:
  - name: Set up Python ${{ matrix.python-version }}
    uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

**When to use**: For library projects that support multiple Python versions

**When not to use**: For application projects that deploy to single Python version

---

### Pip Caching Pattern

**Purpose**: Cache pip dependencies to reduce workflow execution time

**Pattern**:
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Cache invalidation**: Key changes when pyproject.toml changes (dependencies updated)

**Performance impact**: 50-70% faster on cache hit

---

### Quality Gate Pattern

**Purpose**: Enforce quality standards before allowing merge

**Pattern**:
```yaml
- name: Run tests with coverage
  run: pytest --cov=src/package --cov-fail-under=85

- name: Run ruff linting
  run: ruff check src/ tests/

- name: Run mypy type checking
  run: mypy src/
```

**Enforcement**: Set workflows as required in branch protection rules

**Thresholds**:
- Coverage: ≥85% (SAP-004 standard)
- Ruff: 0 errors (strict mode)
- Mypy: 0 type errors

---

### Security Scanning Pattern

**Purpose**: Detect vulnerabilities in code and dependencies

**Pattern**:
```yaml
# CodeQL (static analysis)
- name: Initialize CodeQL
  uses: github/codeql-action/init@v3
  with:
    languages: python
    queries: security-extended

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v3

# Dependency Review (dependency vulnerabilities)
- name: Dependency Review
  uses: actions/dependency-review-action@v4
```

**Triggers**:
- CodeQL: push, pull_request, schedule (weekly)
- Dependency Review: pull_request only

**Action on vulnerabilities**: Workflow fails, blocks merge until fixed

---

### Dependabot Auto-Merge Pattern

**Purpose**: Automatically merge minor/patch Dependabot PRs after tests pass

**Pattern**:
```yaml
name: Dependabot Auto-Merge

on:
  pull_request:
  workflow_run:
    workflows: ["Test"]
    types: [completed]

jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Auto-merge Dependabot PRs
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Safety**: Only merges after test.yml passes, only for minor/patch updates

---

## Integration with Other SAPs

### Integration with SAP-004 (Testing Framework)

**Pattern**: SAP-005 workflows execute SAP-004 tests via test.yml

**Workflow**:
1. SAP-004: Defines pytest configuration (coverage ≥85%, pytest.ini)
2. SAP-005: test.yml runs pytest with coverage enforcement
3. Quality gate: test.yml fails if SAP-004 coverage threshold not met

**Outcome**: Testing standards (SAP-004) enforced automatically via CI/CD (SAP-005)

---

### Integration with SAP-028 (Publishing Automation)

**Pattern**: SAP-005 release.yml triggers SAP-028 PyPI publishing

**Workflow**:
1. Developer: Create GitHub release (git tag v1.0.0, gh release create)
2. SAP-005: release.yml triggered by tag push
3. release.yml: Runs tests, builds wheel
4. SAP-028: Publishes to PyPI via OIDC trusted publishing
5. GitHub Actions: Uploads wheel as release artifact

**Outcome**: Automated publishing integrated with CI/CD pipeline

---

### Integration with SAP-006 (Quality Gates)

**Pattern**: SAP-005 workflows enforce SAP-006 quality standards

**Workflow**:
1. SAP-006: Defines quality standards (coverage ≥85%, 0 lint errors, 0 type errors)
2. SAP-005: Workflows enforce standards (test.yml, lint.yml)
3. Branch protection: Prevents merge if SAP-005 workflows fail

**Outcome**: Quality gates enforced automatically, no manual review needed

---

## Common Pitfalls

### Pitfall 1: Not Caching Pip Dependencies

**Problem**: Workflow slow because pip installs all dependencies on every run

**Fix**:
```yaml
# Add caching step before pip install
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Impact**: 50-70% faster workflow execution on cache hit

---

### Pitfall 2: Running Workflows Serially Instead of Parallel

**Problem**: Workflows run sequentially (test → lint → smoke), slowing feedback

**Fix**: Ensure workflows are independent (don't use needs: keyword unless required)

```yaml
# BAD (serial execution)
jobs:
  test:
    runs-on: ubuntu-latest
  lint:
    needs: test  # Waits for test to complete
    runs-on: ubuntu-latest

# GOOD (parallel execution)
jobs:
  test:
    runs-on: ubuntu-latest
  lint:
    runs-on: ubuntu-latest  # Runs in parallel with test
```

**Impact**: Parallel execution reduces total time by 50-70%

---

### Pitfall 3: Not Enforcing Security Workflows as Required

**Problem**: Security workflows (CodeQL, dependency-review) optional, vulnerabilities slip through

**Fix**: Repository Settings → Branches → Branch protection rules → Require status checks

```markdown
# Required status checks:
✅ Test (test.yml)
✅ Lint (lint.yml)
✅ CodeQL (codeql.yml)
✅ Dependency Review (dependency-review.yml)
```

**Impact**: Zero vulnerabilities merged (security-first)

---

### Pitfall 4: Uploading Coverage Multiple Times

**Problem**: test.yml uploads coverage for every Python version (3.11, 3.12, 3.13), causing duplicates

**Fix**: Upload coverage only once (Python 3.11)

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  if: matrix.python-version == '3.11'  # Upload once
  with:
    file: ./coverage.xml
```

**Impact**: Cleaner coverage reports, no duplicate uploads

---

### Pitfall 5: Not Testing Workflow Changes Locally

**Problem**: Edit workflow, push, GitHub Actions fails with syntax error

**Fix**: Test workflows locally with act before pushing

```bash
# Install act (GitHub Actions local runner)
brew install act

# Test workflow locally
act -j test

# Test specific workflow
act push -W .github/workflows/test.yml
```

**Impact**: Catch syntax errors before pushing, faster iteration

---

## Key Commands

```bash
# List workflows
ls .github/workflows/

# Check workflow status (gh CLI)
gh run list --workflow=test.yml
gh run view <run-id>
gh run watch  # Watch latest run

# Re-run failed workflow
gh run rerun <run-id>

# Test workflow locally (act)
brew install act
act -j test
act push -W .github/workflows/test.yml

# Check required status checks (branch protection)
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks

# Add workflow as required check (web UI)
# Repository Settings → Branches → main → Edit → Require status checks
```

---

## Support & Resources

**SAP-005 Documentation**:
- [Capability Charter](capability-charter.md) - Problem, solution, scope, outcomes
- [Protocol Spec](protocol-spec.md) - All 8 workflows, specifications, best practices
- [CLAUDE.md](CLAUDE.md) - Claude Code-specific automation patterns
- [Adoption Blueprint](adoption-blueprint.md) - Installation, customization, troubleshooting
- [Ledger](ledger.md) - Workflow usage, success rates, performance tracking

**External Resources**:
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - Official GitHub Actions docs
- [actions/cache](https://github.com/actions/cache) - Caching action for pip dependencies
- [actions/setup-python](https://github.com/actions/setup-python) - Python setup action
- [github/codeql-action](https://github.com/github/codeql-action) - CodeQL security scanning
- [actions/dependency-review-action](https://github.com/actions/dependency-review-action) - Dependency security

**Related SAPs**:
- [SAP-004 (testing-framework)](../testing-framework/) - pytest configuration, coverage standards
- [SAP-028 (publishing-automation)](../publishing-automation/) - PyPI publishing via release.yml
- [SAP-006 (quality-gates)](../quality-gates/) - Quality standards enforced by workflows

**Templates**:
- `.github/workflows/test.yml` - Matrix testing workflow
- `.github/workflows/lint.yml` - Code quality workflow
- `.github/workflows/codeql.yml` - Security scanning workflow

---

## Version History

- **2.0.0** (2025-11-04): Phase 2 format migration - Generic workflows for SAP-005
  - 5 common workflows (setup, debug, customize, security, optimize)
  - Workflow patterns reference (matrix testing, caching, quality gates, security)
  - Integration with SAP-004 (testing), SAP-028 (publishing), SAP-006 (quality gates)
  - 5 common pitfalls (no caching, serial execution, security not required, duplicate coverage uploads, no local testing)
  - Key commands (gh CLI, act local runner)

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific CI/CD automation patterns
2. Review [protocol-spec.md](protocol-spec.md) for detailed workflow specifications
3. Check [capability-charter.md](capability-charter.md) for CI/CD design principles and guarantees
4. Set up workflows: Copy from static-template → Customize → Test via PR → Enforce as required
