---
sap_id: SAP-008
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: beginner
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-150"   # Quick Start + Pre-Merge Workflow
  phase_2: "lines 151-300" # Release + Development Workflows
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3000
phase_2_token_estimate: 6500
phase_3_token_estimate: 9500
---

# Automation Scripts (SAP-008) - Claude-Specific Awareness

**SAP ID**: SAP-008
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for using automation scripts via justfile.

### First-Time Setup

1. Read [AGENTS.md](AGENTS.md) for generic automation workflows
2. Use this file for Claude Code tool integration (Bash for `just` commands)
3. Always use `just <task>` (not direct script invocation)

### Session Resumption

- Use Bash tool for all `just` commands
- Check exit codes (0 = success, non-zero = failure)
- Run `just --list` to see available tasks

---

## Claude Code Automation Workflows

### Workflow 1: Running Pre-Merge Checks with Bash

```markdown
User: "Run all checks before committing"

Claude (Phase 1: Run Pre-Merge - 0-5k tokens):
1. Run all quality gates via Bash:
   Bash: just pre-merge

   This runs:
   - pytest (tests)
   - ruff check (linting)
   - mypy --strict (type checking)
   - behave (BDD scenarios, if present)

2. Check exit code:
   - Exit 0: All checks pass ✅
   - Non-zero: Continue to Phase 2 (Fix Issues)

Claude (Phase 2: Fix Issues if Failed - 5-20k tokens):
3. If pre-merge failed, identify which check failed:
   - Test failures:
     Bash: just test
     # Fix failing tests

   - Lint errors:
     Bash: just lint-fix   # Auto-fix
     Bash: just lint       # Verify

   - Type errors:
     Bash: just type-check
     # Fix type hints

4. Re-run pre-merge after fixes:
   Bash: just pre-merge
   # Repeat until exit 0

Claude (Phase 3: Commit if All Pass - 20-30k tokens):
5. If pre-merge passes (exit 0), create commit:
   Bash: git add . && git commit -m "feat: Add feature X

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

Claude (response to user):
"✅ All pre-merge checks passed:
   - Tests: PASS
   - Lint: PASS
   - Type check: PASS

   Created commit: feat: Add feature X"

Result: Code validated and committed
```

---

### Workflow 2: Releasing New Version with Bash

```markdown
User: "Release a new patch version"

Claude (Phase 1: Bump Version - 0-5k tokens):
1. Bump version via Bash:
   Bash: just bump-patch

   This updates:
   - pyproject.toml version
   - __version__ in code
   - Git commit with version bump

2. Check current version:
   Bash: grep -E "^version = " pyproject.toml

Claude (Phase 2: Update Changelog - 5-15k tokens):
3. Read current CHANGELOG.md:
   Read CHANGELOG.md

4. Edit CHANGELOG.md to add release notes:
   Edit CHANGELOG.md
   # Add: Version, date, changes

Claude (Phase 3: Prepare Release - 15-25k tokens):
5. Run release preparation:
   Bash: just prepare-release patch

   This validates:
   - Version consistency
   - All quality gates pass
   - Git status clean

6. If prepare-release fails:
   - Check git status: Bash: git status
   - Commit uncommitted changes
   - Re-run: Bash: just prepare-release patch

Claude (Phase 4: Build and Publish - 25-35k tokens):
7. Build distribution packages:
   Bash: just build

   Creates: dist/<package>-<version>.tar.gz and .whl

8. Publish to production PyPI:
   Bash: just publish-prod

   This:
   - Uploads to PyPI
   - Creates git tag (v1.0.1)
   - Pushes tag to remote

9. Verify release:
   Bash: git tag --list | tail -5
   # Check latest tag

Claude (response to user):
"✅ Released version 1.0.1:
   - Version bumped: pyproject.toml updated
   - CHANGELOG.md: Release notes added
   - Quality gates: All passed
   - PyPI: Package uploaded
   - Git tag: v1.0.1 created and pushed

   Next: Wait 5-10 minutes for PyPI indexing"

Result: New version published to PyPI
```

---

### Workflow 3: Development Loop with Bash

```markdown
User: "Run tests while I develop"

Claude (Phase 1: Quick Tests - 0-5k tokens):
1. Run smoke tests for fast feedback:
   Bash: just smoke

   Expected: 10 seconds, critical tests only

2. Check exit code:
   - Exit 0: Continue development
   - Non-zero: Fix failing tests

Claude (Phase 2: Full Test Suite - 5-15k tokens):
3. Run full test suite:
   Bash: just test

   Expected: 30-60 seconds, all tests

4. Check coverage:
   Bash: just test-coverage

   Opens HTML coverage report

Claude (Phase 3: Fix Lint Issues - 15-25k tokens):
5. Auto-fix lint errors:
   Bash: just lint-fix

   Automatically fixes:
   - Import sorting
   - Code formatting
   - Simple style issues

6. Verify lint fixed:
   Bash: just lint

   Expected: Exit 0 (no errors)

Claude (response to user):
"✅ Development checks complete:
   - Smoke tests: PASS (10s)
   - Full tests: PASS (45s)
   - Coverage: 87% (target: ≥85%)
   - Lint: PASS (auto-fixed 3 issues)

   Ready to continue development"

Result: Fast feedback loop, high confidence
```

---

## Claude-Specific Tips

### Tip 1: Always Check Exit Codes for Bash Commands

**Pattern**:
```markdown
# Run just command
Bash: just pre-merge

# Check exit code in response
# Exit 0: Success ✅
# Exit 1: Failure ❌

# Handle failure
If exit code non-zero:
  - Read error output
  - Fix issue
  - Re-run command
```

**Why**: Exit codes indicate success/failure, must handle failures appropriately

---

### Tip 2: Use `just --list` to Discover Available Tasks

**Pattern**:
```markdown
# When user asks "What commands are available?"
Bash: just --list

# Parse output to show user available tasks
```

**Why**: Projects may have custom justfile tasks beyond standard SAP-008 tasks

---

### Tip 3: Auto-Fix Lint Before Manual Fixes

**Pattern**:
```markdown
# ALWAYS try auto-fix first
Bash: just lint-fix

# Then check if manual fixes needed
Bash: just lint

# Only if lint still fails, read files and manually fix
```

**Why**: `just lint-fix` auto-fixes 90% of lint issues, saves time

---

### Tip 4: Run Smoke Tests During Active Development

**Pattern**:
```markdown
# During development (every 5-10 minutes):
Bash: just smoke   # 10 seconds

# Before committing:
Bash: just test    # 60 seconds

# Before creating PR:
Bash: just pre-merge   # 2 minutes
```

**Why**: Smoke tests provide fast feedback, full tests before commit ensure quality

---

### Tip 5: Use Read to Understand Justfile Custom Tasks

**Pattern**:
```markdown
# If user asks about custom task:
Bash: just --list | grep "<task-name>"

# Read justfile to understand implementation:
Read justfile
# Search for task definition
```

**Why**: Projects may extend justfile with custom tasks, Read helps understand them

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Checking Exit Codes After `just` Commands

**Problem**: Run `just pre-merge`, ignore exit code, proceed to commit

**Fix**: ALWAYS check exit code, handle failures

```markdown
# ❌ BAD: Ignore exit code
Bash: just pre-merge
# Proceed to commit (may fail if pre-merge failed)

# ✅ GOOD: Check exit code
Bash: just pre-merge
# Check exit code in response
# If non-zero, fix issues before committing
```

**Why**: Non-zero exit code indicates failure, must fix before proceeding

---

### Pitfall 2: Running Scripts Directly Instead of via Justfile

**Problem**: Use Bash to run `./scripts/<script>.sh` instead of `just <task>`

**Fix**: ALWAYS use justfile interface

```markdown
# ❌ BAD: Direct script invocation
Bash: ./scripts/pre-merge.sh

# ✅ GOOD: Via justfile
Bash: just pre-merge
```

**Why**: Justfile handles preconditions, validates environment, consistent interface

---

### Pitfall 3: Not Running `just lint-fix` Before Manual Fixes

**Problem**: Lint fails, immediately read files to manually fix

**Fix**: Try auto-fix first, then manual fix if needed

```markdown
# ❌ BAD: Manual fix first
Bash: just lint   # Fails
Read src/module.py
Edit src/module.py   # Manual fix

# ✅ GOOD: Auto-fix first
Bash: just lint-fix   # Auto-fixes 90% of issues
Bash: just lint       # Check if still fails
# Only if still fails, read and manually fix
```

**Why**: Auto-fix handles most issues, saves time and tokens

---

### Pitfall 4: Not Validating Release Preparation

**Problem**: Run `just publish-prod` without `just prepare-release`

**Fix**: ALWAYS run prepare-release before publishing

```markdown
# ❌ BAD: Skip prepare-release
Bash: just bump-patch
Bash: just publish-prod   # May publish inconsistent state

# ✅ GOOD: Run prepare-release
Bash: just bump-patch
Bash: just prepare-release patch
Bash: just build
Bash: just publish-prod
```

**Why**: Prepare-release validates version consistency, runs quality gates

---

### Pitfall 5: Not Reading Justfile for Custom Tasks

**Problem**: User asks about custom task, Claude doesn't check justfile

**Fix**: Read justfile to understand custom tasks

```markdown
# User: "Run my custom deployment task"

# ❌ BAD: Assume task doesn't exist
Claude: "I don't see a deployment task in SAP-008"

# ✅ GOOD: Check justfile
Bash: just --list | grep deploy
Read justfile
# Find custom task, run it
Bash: just deploy
```

**Why**: Projects extend justfile with custom tasks, must check before assuming

---

## Support & Resources

**SAP-008 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic automation workflows
- [Capability Charter](capability-charter.md) - Problem statement, script categories
- [Protocol Spec](protocol-spec.md) - Contracts, idempotency guarantees
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Script adoption tracking

**Justfile Resources**:
- [Justfile Manual](https://just.systems/man/en/) - Official documentation
- List tasks: `just --list`

**Related SAPs**:
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - Project generation with scripts
- [SAP-005 (ci-cd-workflows)](../ci-cd-workflows/) - CI automation
- [SAP-006 (quality-gates)](../quality-gates/) - Quality standards
- [SAP-012 (development-lifecycle)](../development-lifecycle/) - 8-phase lifecycle

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-008
  - 3 workflows: Pre-Merge with Bash, Release with Bash, Development Loop
  - Tool patterns: Bash for all `just` commands, Read for justfile
  - 5 Claude-specific tips, 5 common pitfalls
  - Exit code handling patterns, auto-fix before manual fix

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic automation workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Run `just --list` to see available tasks
4. Use `just pre-merge` before every commit
