---
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[issue-number]"
description: "Debug and resolve bugs using systematic workflow with Genesis integration"
model: claude-sonnet-4-20250514
---

# Bug Resolution Workflow for Issue #$1

Complete bug resolution implementation using TDD methodology, Genesis integration, and specialized agents.

---

# ⚠️ CRITICAL: EXECUTION vs DELEGATION ⚠️

This workflow has THREE phases with DIFFERENT execution modes:

**📍 SETUP PHASE (STEPS 1-7): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT use Task tool for these steps
- ⚠️ YOU must run bash commands yourself using the Bash tool
- ⚠️ Verify each step completes before proceeding

**🤖 DEBUG PHASE (STEP 8): DELEGATION ALLOWED**
- ✅ NOW you can use Task tool with specialized agents
- ✅ Agents work in the worktree YOU created above

**📍 FINALIZATION PHASE (STEPS 9-11): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT delegate commits/PRs to agents
- ⚠️ YOU must run bash commands yourself using the Bash tool
- ⚠️ Return to main repo yourself

---

## CONTEXT: Pure Module Isolation

This workflow creates a Genesis worktree with all supporting files needed for pure module isolation.
A functional module requires not just its own code, but the Genesis infrastructure (.genesis/),
shared utilities (shared-python/), and Python environment files (pyproject.toml, poetry.lock, .venv).

## Debug Methodology
This workflow follows the systematic debug approach: reproduce → isolate → test → fix → validate.

---

## ═══════════════════════════════════════════════════
## SETUP PHASE - YOU MUST EXECUTE (NO DELEGATION)
## ═══════════════════════════════════════════════════

⚠️ **DO NOT use Task tool for STEPS 1-7**
⚠️ **YOU must run these bash commands directly using the Bash tool**

## STEP 1: Environment and Health Validation

**Tool to use:** `Bash`

```bash
# Verify project health and environment
genesis status || echo "⚠️ WARNING: Genesis project health issues detected"
source .envrc || {
    echo "❌ FATAL: Failed to source .envrc"
    exit 1
}

# Verify issue exists and is accessible
if ! gh issue view $1 2>/dev/null; then
    echo "❌ ERROR: Issue #$1 not found or not accessible"
    exit 1
fi
```

## STEP 2: Clean Workspace (MANDATORY)

**Tool to use:** `Bash`

```bash
# Remove old worktrees and build artifacts
genesis clean || echo "⚠️ WARNING: Genesis clean encountered issues"
```

## STEP 3: Create Genesis Worktree with Pure Module Isolation

**Tool to use:** `Bash`

```bash
# Create AI-safe worktree with Pure Module Isolation
# Script auto-symlinks: shared-python/, .genesis/, .venv/
# Script auto-includes: Makefile, pyproject.toml, pytest.ini, .envrc (from manifest)
# Note: Adjust --focus based on bug location
genesis worktree create fix-$1 \
  --focus genesis/ \
  --max-files ${WORKTREE_MAX_FILES:-30}
```

## STEP 4: Navigate to Worktree (CRITICAL)

**Tool to use:** `Bash`

```bash
# MUST navigate to worktree for all subsequent operations
cd worktrees/fix-$1/ || {
    echo "❌ FATAL: Failed to navigate to worktree"
    exit 1
}

pwd  # VERIFY: Must show .../genesis/worktrees/fix-$1
```

## STEP 5: Verify Pure Module Isolation Setup

**Tool to use:** `Bash`

```bash
# Verify symlinks created automatically by worktree script
echo "Verifying Pure Module Isolation setup..."

# Check symlinks exist (auto-created by script)
for symlink in shared-python .genesis .venv docs; do
    if [[ ! -L "$symlink" ]]; then
        echo "⚠️ WARNING: Symlink missing: $symlink (should be auto-created)"
    else
        echo "✓ Symlink present: $symlink -> $(readlink $symlink)"
    fi
done

# Check shared files from manifest
for file in Makefile pyproject.toml pytest.ini .envrc; do
    if [[ ! -f "$file" ]]; then
        echo "⚠️ WARNING: Shared file missing: $file (should be from manifest)"
    else
        echo "✓ Shared file present: $file"
    fi
done

# Count visible files (should be <30 for Pure Module Isolation)
file_count=$(find . -type f -not -path "./.git/*" -not -path "./.*" | wc -l | xargs)
echo "✓ File count: $file_count (target: <30 for AI safety)"
```

## STEP 6: Source Genesis Environment (REQUIRED)

**Tool to use:** `Bash`

```bash
# Load environment in worktree context
source .envrc || {
    echo "❌ FATAL: Failed to source .envrc in worktree"
    cd ../../
    exit 1
}

# Verify Genesis CLI is available
genesis version || {
    echo "❌ CRITICAL ERROR: Genesis CLI not available in worktree"
    cd ../../
    exit 1
}
```

## STEP 7: Genesis Project Health Check

**Tool to use:** `Bash`

```bash
# Verify project health in worktree
genesis status || echo "⚠️ WARNING: Genesis project health issues detected"
```

---

## 🛑 CHECKPOINT: Verify Before Delegation

**Before proceeding to STEP 8 (Debug Phase), verify YOU have completed:**

**Environment Setup:**
- [ ] Verified: `pwd` shows `.../genesis` (main repo)
- [ ] Executed: `source .envrc` successfully
- [ ] Executed: `genesis status` completed
- [ ] Executed: `genesis clean` completed

**Worktree Creation:**
- [ ] Executed: `genesis worktree create fix-$1` successfully
- [ ] Executed: `cd worktrees/fix-$1/` successfully
- [ ] Verified: `pwd` shows `.../genesis/worktrees/fix-$1`
- [ ] Verified: Pure Module Isolation setup complete
- [ ] Executed: `source .envrc` in worktree successfully

**Current State:**
- [ ] You are currently in the worktree directory (not main repo)
- [ ] Genesis CLI is available in worktree
- [ ] Virtual environment is activated

✅ **All checks passed?** → Proceed to STEP 8 and use Task tool
❌ **Any checks failed?** → Fix the issue before delegation

---

## ═══════════════════════════════════════════════════
## DEBUG PHASE - DELEGATION ALLOWED
## ═══════════════════════════════════════════════════

✅ **You may now use Task tool with specialized agents**
✅ **Agents will work in the worktree you created above**

## STEP 8: Agent Workflow Implementation

**IMPORTANT PREREQUISITES:**
- You have completed STEPS 1-7 yourself (setup phase)
- Worktree exists at `worktrees/fix-$1/`
- You have verified the checkpoint criteria above
- You are ready to delegate the debug work

**How to delegate debugging:**

You can either use a single agent for the complete debug workflow, or use specialized agents for each phase.

### Option A: Single Agent for Complete Debug Workflow

Use the lean-implementer agent for the entire debug workflow:

```
Use Task tool with lean-implementer agent:

You are working in a Genesis worktree at: /Users/source_code/genesis/worktrees/fix-$1

Debug and fix bug #$1 using systematic approach:

**Context:**
- Pure module isolation worktree already created
- Environment already configured
- Genesis CLI available

**Debug Workflow:**
1. Analyze bug report and identify root cause
2. Create minimal regression test that demonstrates bug
3. Implement simplest fix to make test pass
4. Validate no scope creep or unrelated changes

**Genesis Integration:**
- Use shared_core.logger for logging
- Use shared_core.errors for error handling
- Follow existing code patterns

**Success Criteria:**
- Regression test created and passing
- Minimal bug fix applied
- All tests pass
- No scope creep

Run tests frequently to verify progress.
```

### Option B: Phased Agents for Detailed Debug Workflow

Or use specialized agents for each phase:

#### Agent 1: Issue Analysis and Validation

Use the issue-analyst agent to validate bug report scope and atomicity:

```
Analyze GitHub issue #$1 to ensure it represents an atomic, reproducible bug.

Requirements:
- Verify issue describes single, atomic bug (not multiple issues)
- Confirm bug has clear reproduction steps
- Isolate the root cause and validate scope boundaries
- Validate acceptance criteria are well-defined
- Extract root cause if evident from description
- Flag any scope creep or compound issues

Genesis Environment:
- Working in worktree with shared components available
- Must use shared_core.logger for all output
- Must use shared_core.errors for error handling
- Must validate environment with shared_core.config

Success Criteria:
- Issue confirmed as atomic bug report
- Reproduction approach identified
- Root cause hypothesis formed (if possible)
- Scope validated as minimal and focused

Constraints:
- Focus ONLY on the reported bug
- No scope expansion or additional improvements
- Maintain lean development principles
```

#### Agent 2: Regression Test Creation (RED Phase)

Use the test-designer agent to create minimal regression test for bug:

```
Create minimal regression test for bug #$1 that fails before fix, passes after fix.

Requirements:
- Write single, focused test that demonstrates the bug
- Test must currently FAIL due to bug behavior
- Test will PASS once bug is fixed
- Use Genesis testing patterns and shared utilities
- Follow pytest conventions in pytest.ini
- Use shared_core.logger for test logging

Genesis Testing Integration:
- Use existing test directory structure
- Import and use Genesis shared test utilities
- Follow established naming conventions
- Integrate with current test suite

Test Criteria:
- Minimal test case (no over-testing)
- Clear test name describing bug scenario
- Proper setup/teardown if needed
- Fails for right reason (demonstrates bug)
- Will pass when bug fixed

Lean Principles:
- Test ONLY the specific bug behavior
- No comprehensive test coverage expansion
- No testing of related but unaffected functionality
- Minimal test code to prove bug exists
```

#### Agent 3: Minimal Bug Fix Implementation (GREEN Phase)

Use the lean-implementer agent to implement absolute minimal fix for bug:

```
Fix bug #$1 with the smallest possible code change using lean principles.

Requirements:
- Implement ONLY the minimal change to fix the bug
- Make the regression test pass
- Use Genesis shared components (logging, error handling, config)
- Follow existing code patterns and architecture
- No refactoring or improvements 'while we're here'

Genesis Shared Components Integration:
- Use shared_core.logger for any new logging
- Use shared_core.errors for any error handling
- Use shared_core.config for any configuration access
- Follow existing import patterns

Lean Implementation Principles:
- Absolute minimal code change required
- No architectural modifications
- No refactoring of surrounding code
- No additional features or improvements
- No optimization unless required for fix

Constraints:
- ONLY fix the specific bug reported in issue #$1
- No scope creep beyond exact bug fix
- No code style improvements unless required
- No performance improvements unless bug-related
- Maintain existing API contracts

Success Criteria:
- Regression test now passes
- Bug is resolved as described in issue
- No unrelated functionality affected
- Minimal surface area of change
- All existing tests continue to pass
```

#### Agent 4: Quality Validation and Gates

Use the build-validator agent to validate bug fix quality and run Genesis quality gates:

```
Run complete quality validation for bug fix #$1 using Genesis quality pipeline.

Genesis Quality Gates (MANDATORY):
1. Run 'genesis autofix' - format and lint automatically
2. Run 'genesis status' - verify project health
3. Run full test suite (make test, pytest, or npm test)
4. Verify no regressions in existing functionality
5. Confirm regression test passes
6. Check Genesis health indicators

Quality Validation Requirements:
- All tests pass including new regression test
- No linting violations after genesis autofix
- No type checking errors (if applicable)
- Genesis status shows healthy state
- No performance regressions (if measurable)

Genesis Integration Validation:
- Verify shared components used correctly
- Check logging follows shared_core.logger patterns
- Confirm error handling uses shared_core.errors
- Validate configuration access uses shared_core.config

Test Suite Validation:
- Full test suite passes (not just new test)
- No existing tests broken by change
- New regression test passes consistently
- Test coverage maintained or improved

Success Criteria:
- Complete test suite passes
- All Genesis quality gates satisfied
- No regressions detected in any area
- System remains stable and healthy
- Code meets Genesis quality standards
```

#### Agent 5: Scope Protection and Final Validation

Use the scope-guardian agent to verify no scope creep and validate minimal change:

```
Review bug fix #$1 to ensure changes exactly match issue requirements with zero scope creep.

Scope Validation Requirements:
- Compare all changes against original issue description
- Verify ONLY the reported bug was fixed
- Confirm no additional improvements included
- Flag any unrelated code changes
- Validate minimal change principle followed

Scope Boundaries (STRICT):
- ONLY the specific bug described in issue #$1
- No refactoring or code style improvements
- No additional features or enhancements
- No architectural or design pattern changes
- No performance optimizations unless bug-related
- No documentation updates unless bug-related

Change Analysis:
- Review exact code changes made
- Verify each change serves bug fix purpose
- Flag any changes that go beyond minimal fix
- Confirm no 'while we're here' improvements
- Validate adherence to lean principles

Genesis Principles Validation:
- Confirm minimal code approach used
- Verify no over-engineering introduced
- Check that YAGNI principle followed
- Validate no abstractions added unnecessarily
- Ensure simplest solution was chosen

Success Criteria:
- All changes directly related to bug fix
- No scope creep detected
- Minimal change principle maintained
- Bug fix is focused and targeted
- Lean development principles followed
```

---

## ═══════════════════════════════════════════════════
## FINALIZATION PHASE - YOU MUST EXECUTE (NO DELEGATION)
## ═══════════════════════════════════════════════════

⚠️ **DO NOT delegate STEPS 9-11 to agents**
⚠️ **YOU must run these commands directly using the Bash tool**

## STEP 9: Genesis Quality Gates (MANDATORY BEFORE COMMIT)

**Tool to use:** `Bash`

```bash
echo "🔍 Running Genesis quality gates..."

# Run autofix - handle failure gracefully
genesis autofix || {
    echo "⚠️ WARNING: Genesis autofix encountered issues"
    echo "Attempting to continue..."
}

# Final health check
genesis status || echo "⚠️ WARNING: Genesis status shows issues"

# Run appropriate test command
if [[ -f "Makefile" ]] && grep -q "^test:" Makefile; then
    make test || echo "⚠️ WARNING: Some tests failed"
elif [[ -f "pytest.ini" ]]; then
    pytest || echo "⚠️ WARNING: Some tests failed"
elif [[ -f "package.json" ]]; then
    npm test || echo "⚠️ WARNING: Some tests failed"
else
    echo "⚠️ No test command found, verify manually"
fi
```

## STEP 10: Genesis Commit and PR Creation

**Tool to use:** `Bash`

```bash
echo "📝 Creating Genesis commit..."

# Stage changes and commit with Genesis
git add .
genesis commit -m "fix: resolve issue #$1

Fixes #$1

- Implemented minimal bug fix following TDD methodology
- Created regression test that demonstrates the bug
- Applied simplest solution that makes test pass
- Validated with Genesis quality gates
- No scope creep or unrelated changes"

echo "🚀 Creating PR..."
gh pr create \
  --title "fix: resolve issue #$1" \
  --body "$(cat <<'EOF'
Fixes #$1

## Genesis Workflow Completed
- ✅ Genesis worktree isolation used
- ✅ Genesis quality gates passed
- ✅ Genesis shared components integrated
- ✅ Specialized agents validated approach
- ✅ Lean development principles followed

## Changes Made
- Created regression test demonstrating the bug
- Implemented minimal fix to resolve the issue
- All existing tests continue to pass
- No unrelated changes or scope creep

## Testing
- ✅ Regression test created and passing
- ✅ Full test suite passes
- ✅ Genesis health checks pass
- ✅ No scope creep detected

## Agent Validation
- ✅ issue-analyst: Confirmed atomic bug scope
- ✅ test-designer: Created minimal regression test
- ✅ lean-implementer: Applied minimal fix
- ✅ build-validator: Quality gates passed
- ✅ scope-guardian: No scope creep detected
EOF
)" \
  --assignee @me || {
    echo "⚠️ WARNING: PR creation failed - you may need to create manually"
}
```

## STEP 11: Return to Main Repository (CRITICAL!)

**Tool to use:** `Bash`

```bash
# Navigate back to main repository
cd ../../ || {
    echo "❌ WARNING: Failed to return to main directory"
    echo "Current directory: $(pwd)"
}
pwd  # VERIFY: Must show .../genesis (main repo root)

# Final health check
genesis status

echo "✅ SUCCESS: Bug fix workflow completed for issue #$1"
echo "📋 Next: Review PR, merge when ready, then run: /close $1"
```

---

## 🚫 COMMON MISTAKES TO AVOID

**❌ WRONG - Delegating setup to agents:**
```
# This will NOT work - agents cannot create worktrees for you
<invoke name="Task">
  <parameter name="prompt">Run genesis clean and create worktree...</parameter>
</invoke>
```

**✅ CORRECT - Executing setup yourself:**
```
# YOU run the setup commands with Bash tool
<invoke name="Bash">
  <parameter name="command">genesis clean</parameter>
</invoke>
<invoke name="Bash">
  <parameter name="command">genesis worktree create fix-$1</parameter>
</invoke>
```

**❌ WRONG - Using Task tool before worktree exists:**
- Skipping STEPS 1-7 and jumping to STEP 8
- Expecting agents to navigate to worktrees
- Delegating environment setup

**✅ CORRECT - Proper workflow:**
1. Complete STEPS 1-7 yourself with Bash tool
2. Verify checkpoint criteria
3. THEN use Task tool in STEP 8
4. Complete STEPS 9-11 yourself with Bash tool

---

## Success Criteria
- ✅ Bug reproduced with failing test
- ✅ Test passes with minimal fix
- ✅ All Genesis quality gates pass
- ✅ PR created and ready for review
- ✅ No scope creep or unrelated changes
