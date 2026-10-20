---
sap_id: SAP-008
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: agents
complexity: beginner
estimated_reading_time: 10
progressive_loading:
  phase_1: "lines 1-200"   # Quick Reference + Core Workflows
  phase_2: "lines 201-400" # Advanced Workflows + Script Categories
  phase_3: "full"          # Complete including troubleshooting
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 11000
---

# Automation Scripts (SAP-008) - Agent Awareness

**SAP ID**: SAP-008
**Last Updated**: 2025-11-04
**Audience**: Generic AI Coding Agents

---

## Quick Reference

### When to Use

**Use automation-scripts when**:
- Running pre-merge quality gates (`just pre-merge`)
- Releasing new versions to PyPI (`just bump-patch`, `just publish-prod`)
- Running tests and linting locally (`just test`, `just lint`)
- Validating documentation (`just docs-validate`)
- Diagnosing environment issues (`just diagnose`)

**Don't use when**:
- Running one-off bash commands (use bash directly)
- Project doesn't have justfile (SAP-008 specific)
- Learning justfile syntax (use justfile docs)

### Primary Interface

**ALWAYS use justfile** (not direct script invocation):
```bash
just <task>              # ✅ Correct (unified interface)
./scripts/<script>.sh    # ❌ Avoid (direct invocation)
```

### Common Tasks

| User Request | Command | Purpose |
|--------------|---------|---------|
| "Run tests" | `just test` | Run pytest suite |
| "Run all checks" | `just pre-merge` | All quality gates (tests, lint, type check) |
| "Fix lint errors" | `just lint-fix` | Auto-fix ruff errors |
| "Bump version" | `just bump-patch` | Bump patch version (1.0.0 → 1.0.1) |
| "Release to PyPI" | `just publish-prod` | Build + publish to production PyPI |
| "Quick validation" | `just smoke` | 10-second smoke test |
| "Diagnose environment" | `just diagnose` | Check Python, dependencies, versions |

---

## Common Workflows

### Workflow 1: Pre-Merge Quality Gates (1-2 minutes)

**User signal**: "Run all checks before committing", "Validate changes", "Run pre-merge"

**Purpose**: Validate code quality before creating commit/PR

**Steps**:
1. Run all quality gates:
   ```bash
   just pre-merge
   ```

   This runs:
   - `pytest` (tests)
   - `ruff check` (linting)
   - `mypy --strict` (type checking)
   - `behave` (BDD scenarios, if present)

2. Check exit code:
   - Exit 0: All checks pass ✅
   - Non-zero: Fix errors and re-run

3. If all pass, create commit:
   ```bash
   git add .
   git commit -m "feat: Add feature X"
   ```

**Expected outcome**: All quality gates pass, ready to commit

**Common errors**:
- Test failures → Fix tests, re-run `just test`
- Lint errors → Run `just lint-fix` to auto-fix
- Type errors → Fix type hints, re-run `just type-check`

---

### Workflow 2: Release New Version (5-10 minutes)

**User signal**: "Release new version", "Publish to PyPI", "Bump version"

**Purpose**: Release new version following semver

**Steps**:
1. Bump version (choose level):
   ```bash
   just bump-patch   # 1.0.0 → 1.0.1 (bug fixes)
   just bump-minor   # 1.0.0 → 1.1.0 (new features)
   just bump-major   # 1.0.0 → 2.0.0 (breaking changes)
   ```

2. Update CHANGELOG.md with release notes

3. Run release preparation:
   ```bash
   just prepare-release patch
   ```

   This:
   - Validates version consistency
   - Runs all quality gates
   - Checks git status (must be clean)

4. Build distribution packages:
   ```bash
   just build
   ```

   Creates: `dist/<package>-<version>.tar.gz` and `.whl`

5. Publish to production PyPI:
   ```bash
   just publish-prod
   ```

   This:
   - Uploads to PyPI
   - Creates git tag (v1.0.1)
   - Pushes tag to remote

**Expected outcome**: New version published to PyPI, git tag created

**Common errors**:
- Dirty git status → Commit or stash changes first
- Quality gates fail → Fix issues, re-run `just pre-merge`
- PyPI credentials missing → Set `PYPI_API_TOKEN` environment variable

---

### Workflow 3: Development Loop (Continuous)

**User signal**: "Run tests", "Check tests", "Test while developing"

**Purpose**: Fast feedback during feature development

**Steps**:
1. Run tests frequently:
   ```bash
   just test
   ```

2. Check test coverage:
   ```bash
   just test-coverage
   ```

   Opens HTML coverage report in browser

3. Quick validation (10 seconds):
   ```bash
   just smoke
   ```

   Runs subset of critical tests

4. Fix lint errors automatically:
   ```bash
   just lint-fix
   ```

**Expected outcome**: Fast feedback, maintain high test coverage

**Tips**:
- Use `just smoke` for quick checks (10s vs 60s for full suite)
- Run `just test-coverage` to identify untested code
- Run `just lint-fix` before committing to auto-fix style issues

---

### Workflow 4: Environment Diagnosis (2-5 minutes)

**User signal**: "Environment issues", "Dependencies not working", "Fix setup"

**Purpose**: Diagnose and fix environment problems

**Steps**:
1. Run diagnostics:
   ```bash
   just diagnose
   ```

   Checks:
   - Python version (≥3.11)
   - Virtual environment active
   - Dependencies installed
   - Git configuration

2. If issues found, follow recommendations:
   - Python version wrong → Install correct version
   - Dependencies missing → Run `just install`
   - Virtual environment issues → Run `just venv-clean && just venv-create`

3. Validate environment:
   ```bash
   just check-env
   ```

   Exit 0 = environment OK ✅

**Expected outcome**: Environment validated and working

**Common fixes**:
- Missing dependencies: `just install`
- Corrupt virtual environment: `just venv-clean && just venv-create && just install`
- Python version wrong: Use pyenv or install correct version

---

### Workflow 5: Documentation Validation (30 seconds)

**User signal**: "Validate docs", "Check documentation", "Lint markdown"

**Purpose**: Validate documentation quality and accuracy

**Steps**:
1. Validate all documentation:
   ```bash
   just docs-validate
   ```

   Checks:
   - Markdown syntax (no broken links)
   - Code examples (extract and test)
   - Frontmatter consistency
   - Cross-references

2. Check documentation metrics:
   ```bash
   just docs-metrics
   ```

   Reports:
   - Total files, lines
   - Completeness score
   - Missing sections

3. Generate documentation map:
   ```bash
   just docs-map
   ```

   Creates: `docs/DOCS_MAP.md` with sitemap

**Expected outcome**: Documentation validated, metrics reported

**Common errors**:
- Broken links → Fix URLs in markdown files
- Code examples fail → Update examples to match current API
- Missing frontmatter → Add YAML frontmatter to markdown files

---

### Workflow 6: Troubleshooting Script Failures (5-15 minutes)

**User signal**: "Script failed", "Just command not working", "Debug automation"

**Purpose**: Debug failed automation script

**Steps**:
1. Identify which script failed:
   ```bash
   just <task>   # Note the error message
   ```

2. Check script source:
   - Justfile: `cat justfile | grep -A 5 "<task>"`
   - Script file: `cat scripts/<script>.sh`

3. Run script directly with debugging:
   ```bash
   bash -x ./scripts/<script>.sh <args>
   ```

   `-x` flag shows each command before execution

4. Check common issues:
   - Exit code non-zero → Script failed validation
   - Missing file → Check path, create if needed
   - Permission denied → Run `chmod +x scripts/<script>.sh`
   - Environment variable missing → Set required vars

5. Check script logs (if applicable):
   ```bash
   cat logs/<script>.log
   ```

**Expected outcome**: Script issue identified and fixed

**Common patterns**:
- Idempotency check failed → Script already ran successfully, safe to ignore
- Validation failed → Fix code to pass quality gates
- Missing dependency → Install via `just install`

---

## User Signal Pattern Table

| User Signal | Workflow | Command | Expected Time |
|-------------|----------|---------|---------------|
| "Run all checks" | Pre-Merge Gates | `just pre-merge` | 1-2 min |
| "Release new version" | Release Version | `just bump-patch && just publish-prod` | 5-10 min |
| "Run tests" | Development Loop | `just test` | 30-60s |
| "Fix environment" | Diagnose Environment | `just diagnose` | 2-5 min |
| "Validate docs" | Documentation Validation | `just docs-validate` | 30s |
| "Script failed" | Troubleshoot Failure | `bash -x ./scripts/<script>.sh` | 5-15 min |
| "Quick check" | Development Loop | `just smoke` | 10s |
| "Bump version" | Release Version | `just bump-patch` | 5s |

---

## Best Practices

### Practice 1: Always Use Justfile Interface

**Pattern**:
```bash
# ✅ Correct (unified interface)
just test
just pre-merge
just publish-prod

# ❌ Avoid (direct invocation, bypasses justfile guarantees)
./scripts/pytest.sh
./scripts/pre-merge.sh
./scripts/publish-prod.sh
```

**Why**: Justfile provides consistent interface, handles edge cases, validates preconditions

---

### Practice 2: Run Pre-Merge Before Every Commit

**Pattern**:
```bash
# Before committing:
just pre-merge

# If all pass:
git add .
git commit -m "feat: Add feature X"
```

**Why**: Catches issues locally before CI, prevents failed PR checks

---

### Practice 3: Use Smoke Tests During Development

**Pattern**:
```bash
# During active development (every 5 minutes):
just smoke   # 10 seconds

# Before committing:
just test    # 60 seconds

# Before pushing:
just pre-merge   # 2 minutes
```

**Why**: Fast feedback loop improves productivity, smoke tests cover critical paths

---

### Practice 4: Validate Environment After Setup

**Pattern**:
```bash
# After cloning repository:
just install
just check-env

# If check-env fails:
just diagnose   # Identify issue
# Fix issue
just check-env  # Verify fixed
```

**Why**: Catches environment issues early before they cause mysterious failures

---

### Practice 5: Document Custom Scripts in Justfile

**Pattern**:
```justfile
# Custom task for project-specific workflow
my-custom-task:
    @echo "Running custom workflow..."
    ./scripts/my-custom-script.sh
    just test
    just lint
```

**Why**: Keeps all automation discoverable via `just --list`, maintains single interface

---

## Common Pitfalls

### Pitfall 1: Running Scripts Directly Instead of via Justfile

**Problem**: Invoking `./scripts/<script>.sh` directly instead of `just <task>`

**Fix**: Always use justfile interface

```bash
# ❌ BAD: Direct invocation
./scripts/pre-merge.sh

# ✅ GOOD: Via justfile
just pre-merge
```

**Why**: Justfile handles preconditions, validates environment, provides consistent interface

---

### Pitfall 2: Not Running Pre-Merge Before Committing

**Problem**: Commit without running quality gates, CI fails

**Fix**: Run `just pre-merge` before every commit

```bash
# ALWAYS run before committing:
just pre-merge

# If all pass, then commit:
git add .
git commit -m "feat: Add feature X"
```

**Why**: Catches issues locally (fast feedback) instead of waiting for CI (slow feedback)

---

### Pitfall 3: Ignoring Script Exit Codes

**Problem**: Script fails (non-zero exit), but agent continues anyway

**Fix**: Check exit code, handle failure

```bash
# Run script
just pre-merge

# Check exit code
if [ $? -ne 0 ]; then
    echo "Pre-merge checks failed, fix issues before committing"
    exit 1
fi
```

**Why**: Non-zero exit code indicates failure, must be addressed before proceeding

---

### Pitfall 4: Publishing Without Running Prepare-Release

**Problem**: Run `just publish-prod` without `just prepare-release`, inconsistent state

**Fix**: Always run prepare-release first

```bash
# ✅ Correct sequence:
just bump-patch
just prepare-release patch
just build
just publish-prod

# ❌ Skip prepare-release:
just bump-patch
just publish-prod   # May publish inconsistent state
```

**Why**: Prepare-release validates version consistency, runs quality gates, ensures clean git status

---

### Pitfall 5: Not Validating Environment After Changes

**Problem**: Install new dependency, forget to validate environment

**Fix**: Run `just check-env` after environment changes

```bash
# After installing new dependency:
pip install <package>

# Validate environment still works:
just check-env

# If fails, diagnose:
just diagnose
```

**Why**: New dependencies may conflict with existing setup, check-env catches issues early

---

## Integration with Other SAPs

### SAP-003 (project-bootstrap)
- Generated projects include justfile with 30+ tasks
- Scripts directory structure matches SAP-008 categories
- Integration: `python setup.py <project>` generates project with SAP-008 scripts

### SAP-005 (ci-cd-workflows)
- GitHub Actions call scripts directly (not via justfile)
- CI workflows use same scripts as local development
- Integration: `.github/workflows/test.yml` runs `./scripts/pytest.sh`

### SAP-006 (quality-gates)
- Quality gates enforced via `just pre-merge`
- Coverage ≥85%, lint 0 errors, type check 0 errors
- Integration: `just pre-merge` runs SAP-006 quality gates

### SAP-012 (development-lifecycle)
- Scripts support 8-phase lifecycle (Vision → Release)
- Release scripts automate Phase 7 (Release Management)
- Integration: `just publish-prod` executes SAP-012 Phase 7

---

## Support & Resources

**SAP-008 Documentation**:
- [Capability Charter](capability-charter.md) - Problem statement, script categories
- [Protocol Spec](protocol-spec.md) - Contracts, idempotency guarantees, justfile interface
- [Awareness Guide](awareness-guide.md) - Detailed workflows, script categories
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Script adoption tracking, metrics

**Justfile Resources**:
- [Justfile Manual](https://just.systems/man/en/) - Official documentation
- [Justfile Recipes](https://github.com/casey/just/blob/master/examples/README.md) - Example recipes

**Related SAPs**:
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - Project generation with scripts
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - CI automation
- [SAP-006 (quality-gates)](../quality-gates/) - Quality standards
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - 8-phase lifecycle

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-008
  - 6 workflows: Pre-Merge, Release, Development Loop, Diagnose, Docs, Troubleshoot
  - 8 user signal patterns
  - 5 best practices, 5 common pitfalls
  - Integration with SAP-003, SAP-005, SAP-006, SAP-012

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [capability-charter.md](capability-charter.md) for design rationale
4. Use `just --list` to see all available tasks
