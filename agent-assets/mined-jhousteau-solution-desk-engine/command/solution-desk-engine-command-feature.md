---
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[issue-number]"
description: "Implement feature using TDD workflow with Genesis integration"
model: claude-sonnet-4-20250514
---

# Feature Implementation Workflow for Issue #$1

Complete feature implementation using strict Test-Driven Development (TDD) methodology with Genesis integration and specialized agents.

---

# ⚠️ CRITICAL: EXECUTION vs DELEGATION ⚠️

This workflow has THREE phases with DIFFERENT execution modes:

**📍 SETUP PHASE (STEPS 1-7): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT use Task tool for these steps
- ⚠️ YOU must run bash commands yourself using the Bash tool
- ⚠️ Verify each step completes before proceeding

**🤖 IMPLEMENTATION PHASE (STEP 8): DELEGATION ALLOWED**
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
genesis worktree create feature-$1 \
  --focus genesis/ \
  --max-files ${WORKTREE_MAX_FILES:-30}
```

## STEP 4: Navigate to Worktree (CRITICAL)

**Tool to use:** `Bash`

```bash
# MUST navigate to worktree for all subsequent operations
cd worktrees/feature-$1/ || {
    echo "❌ FATAL: Failed to navigate to worktree"
    exit 1
}

pwd  # VERIFY: Must show .../genesis/worktrees/feature-$1
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

**Before proceeding to STEP 8 (Implementation Phase), verify YOU have completed:**

**Environment Setup:**
- [ ] Verified: `pwd` shows `.../genesis` (main repo)
- [ ] Executed: `source .envrc` successfully
- [ ] Executed: `genesis status` completed
- [ ] Executed: `genesis clean` completed

**Worktree Creation:**
- [ ] Executed: `genesis worktree create feature-$1` successfully
- [ ] Executed: `cd worktrees/feature-$1/` successfully
- [ ] Verified: `pwd` shows `.../genesis/worktrees/feature-$1`
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
## IMPLEMENTATION PHASE - DELEGATION ALLOWED
## ═══════════════════════════════════════════════════

✅ **You may now use Task tool with specialized agents**
✅ **Agents will work in the worktree you created above**

## STEP 8: TDD Agent Workflow Implementation

**IMPORTANT PREREQUISITES:**
- You have completed STEPS 1-7 yourself (setup phase)
- Worktree exists at `worktrees/feature-$1/`
- You have verified the checkpoint criteria above
- You are ready to delegate the implementation work

**How to delegate implementation:**

You can either delegate to individual agents for each TDD phase, or use a single agent for the entire workflow. Choose based on complexity.

### Option A: Single Agent for Complete TDD Workflow

Use the lean-implementer agent for the entire RED-GREEN-REFACTOR cycle:

```
Use Task tool with lean-implementer agent:

You are working in a Genesis worktree at: /Users/source_code/genesis/worktrees/feature-$1

Implement feature #$1 using complete TDD methodology (RED-GREEN-REFACTOR):

**Context:**
- Pure module isolation worktree already created
- Environment already configured
- Genesis CLI available

**TDD RED Phase:**
- Write minimal failing acceptance tests
- Tests define expected feature behavior
- Focus on critical path functionality

**TDD GREEN Phase:**
- Implement simplest code to make tests pass
- Use Genesis shared components (shared_core.logger, shared_core.errors, etc.)
- No over-engineering or premature abstractions

**TDD REFACTOR Phase:**
- Improve code quality while maintaining test passage
- Eliminate duplication
- Follow Genesis code quality standards

**Success Criteria:**
- All tests pass
- Code follows Genesis patterns
- No unnecessary complexity
- Feature ready for quality gates

Run tests frequently to verify progress.
```

### Option B: Phased Agents for Detailed TDD Workflow

Or use specialized agents for each phase:

#### Agent 1: Feature Analysis and Decomposition

Use the issue-analyst agent to decompose feature into atomic, testable units:

```
Analyze feature request #$1 and decompose into atomic, testable units following lean principles.

Requirements:
- Break down feature into minimal testable units
- Verify feature has clear acceptance criteria
- Identify core functionality vs nice-to-have
- Ensure atomic implementation approach
- Validate user story format and completeness

Genesis Lean Principles:
- YAGNI (You Aren't Gonna Need It) - implement only what's required
- Minimal Viable Feature - simplest version that delivers value
- No over-engineering or premature optimization
- Focus on core functionality first

Feature Decomposition:
- Identify minimum viable functionality
- Break into atomic user stories if compound
- Define clear acceptance criteria for each part
- Prioritize core vs peripheral functionality
- Flag any scope creep in original request

Success Criteria:
- Feature decomposed into atomic units
- Clear acceptance criteria defined
- Minimal implementation path identified
- Scope validated and focused
```

#### Agent 2: Acceptance Test Creation (RED Phase)

Use the test-designer agent to write failing acceptance tests for feature:

```
Write minimal failing acceptance tests for feature #$1 following TDD RED phase principles.

TDD Phase: RED (write failing tests first)

Requirements:
- Write acceptance tests that define expected feature behavior
- Tests must currently FAIL (no implementation exists yet)
- Focus on critical path functionality only
- Use Genesis testing patterns and shared utilities
- Avoid over-testing and edge case obsession

TDD RED Phase Principles:
- Write just enough tests to define desired behavior
- Tests should be minimal and focused
- Avoid testing implementation details
- Focus on user-observable behavior
- Each test should fail for clear reason

Genesis Testing Integration:
- Use existing test framework configuration
- Import Genesis shared test utilities
- Follow established test naming conventions
- Integrate with current test structure
- Use shared_core.logger for test output

Test Design Criteria:
- Clear test names describing feature behavior
- Minimal setup and teardown
- Focus on happy path scenarios first
- Tests clearly demonstrate expected functionality
- All tests currently fail appropriately

Lean Testing Approach:
- Test ONLY the core feature functionality
- No comprehensive edge case testing (yet)
- No performance testing unless feature requirement
- Minimal test code to define behavior

Success Criteria:
- Acceptance tests written and failing appropriately
- Tests clearly define expected feature behavior
- Critical path functionality covered
- Tests are minimal and maintainable
```

#### Agent 3: Minimal Feature Implementation (GREEN Phase)

Use the lean-implementer agent to implement minimal feature to make tests pass:

```
Implement minimal feature code to make acceptance tests pass for feature #$1.

TDD Phase: GREEN (make tests pass with minimal code)

Requirements:
- Implement simplest possible code to make tests pass
- No abstractions or patterns unless absolutely necessary
- Use Genesis shared components for infrastructure concerns
- Follow existing code patterns and architecture
- Direct, simple solutions over clever implementations

TDD GREEN Phase Principles:
- Write minimal code to make tests pass
- No over-engineering or premature abstractions
- Direct solutions over complex patterns
- YAGNI - implement only what tests require
- Defer refactoring to next phase

Genesis Shared Components Integration:
- Use shared_core.logger for any logging needs
- Use shared_core.errors for error handling
- Use shared_core.config for configuration access
- Use shared_core.health for health checks if needed

Lean Implementation Guidelines:
- Simplest thing that could possibly work
- No design patterns unless clearly needed
- No performance optimizations (yet)
- Hard-code values rather than abstract too early
- Focus on making tests pass, not perfect code

Implementation Constraints:
- ONLY implement what acceptance tests require
- No additional functionality beyond test coverage
- No refactoring of existing code (save for refactor phase)
- No architectural improvements (yet)

Success Criteria:
- All acceptance tests now pass
- Implementation is minimal and direct
- No unnecessary complexity introduced
- Feature functionality works as defined by tests
- Code follows Genesis patterns and uses shared components
```

#### Agent 4: Code Quality Improvement (REFACTOR Phase)

Use the refactoring-specialist agent to refactor feature code while maintaining test passage:

```
Improve feature #$1 code quality through refactoring while keeping all tests passing.

TDD Phase: REFACTOR (improve code without changing behavior)

Requirements:
- Improve code structure and readability
- Eliminate any duplication introduced
- Apply appropriate abstractions if beneficial
- Maintain all test passage throughout
- Follow Genesis code quality standards

Refactoring Principles:
- Improve internal structure without changing external behavior
- All tests must continue passing throughout process
- Apply DRY principle where appropriate
- Extract methods/functions if they improve readability
- Rename variables/functions for clarity

Genesis Quality Standards:
- Use shared components consistently
- Follow established naming conventions
- Maintain consistent error handling patterns
- Ensure proper logging integration
- Follow existing architectural patterns

Refactoring Guidelines:
- Small, incremental changes only
- Run tests after each change
- Focus on readability and maintainability
- Remove any hard-coded values if appropriate
- Simplify complex conditional logic

Improvement Areas:
- Extract reusable functions if duplication exists
- Improve variable and function names
- Simplify complex expressions
- Remove any dead code introduced
- Organize code following project conventions

Success Criteria:
- All tests continue to pass after refactoring
- Code is more readable and maintainable
- Appropriate abstractions applied
- Duplication eliminated
- Code follows Genesis quality standards
```

#### Agent 5: Build and Quality Validation

Use the build-validator agent to validate feature meets all Genesis quality standards:

```
Run comprehensive quality validation for feature #$1 using Genesis quality pipeline.

Genesis Quality Gates (MANDATORY):
1. Run 'genesis autofix' for formatting and linting
2. Run 'genesis status' for project health check
3. Execute full test suite to ensure no regressions
4. Validate feature acceptance tests pass
5. Check code complexity and maintainability
6. Verify Genesis shared component usage

TDD Validation:
- All acceptance tests pass consistently
- No existing tests broken by feature addition
- Test coverage appropriate for feature scope
- Tests clearly document feature behavior

Quality Standards Validation:
- Code follows Genesis formatting standards
- No linting violations after autofix
- Type checking passes (if applicable)
- Code complexity within acceptable limits
- Error handling follows shared patterns

Genesis Integration Validation:
- Shared components used appropriately
- Logging follows shared_core.logger patterns
- Error handling uses shared_core.errors
- Configuration access uses shared_core.config
- Health monitoring integrated if applicable

Success Criteria:
- Complete test suite passes including new feature tests
- All Genesis quality gates satisfied
- No regressions in existing functionality
- Code meets Genesis quality and style standards
- Feature ready for production use
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
    echo "ℹ️ No test command found, verify manually"
fi
```

## STEP 10: Genesis Commit and PR Creation

**Tool to use:** `Bash`

```bash
echo "📝 Creating Genesis commit..."

# Stage changes and commit with Genesis
git add .
genesis commit -m "feat: implement feature from issue #$1

Closes #$1

- Implemented using strict TDD methodology (RED-GREEN-REFACTOR)
- Created comprehensive acceptance tests
- Applied minimal implementation to pass tests
- Refactored for code quality while maintaining test passage
- Validated with Genesis quality gates
- No scope creep or unrelated changes"

echo "🔗 Creating PR..."
gh pr create \
  --title "feat: implement feature from issue #$1" \
  --body "$(cat <<'EOF'
Closes #$1

## Genesis TDD Workflow Completed
- ✅ Genesis worktree isolation used
- ✅ RED: Acceptance tests written first (failing)
- ✅ GREEN: Minimal implementation to pass tests
- ✅ REFACTOR: Code quality improved
- ✅ Genesis quality gates passed
- ✅ Lean development principles followed

## Changes Made
- Created acceptance tests defining feature behavior
- Implemented minimal code to satisfy tests
- Refactored for maintainability
- All existing tests continue to pass
- No unrelated changes or scope creep

## Testing
- ✅ Acceptance tests created and passing
- ✅ Full test suite passes
- ✅ Genesis health checks pass
- ✅ No scope creep detected

## TDD Agent Validation
- ✅ issue-analyst: Feature decomposed into atomic units
- ✅ test-designer: Created minimal acceptance tests (RED)
- ✅ lean-implementer: Applied minimal implementation (GREEN)
- ✅ refactoring-specialist: Improved code quality (REFACTOR)
- ✅ build-validator: Quality gates passed
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
    echo "⚠️ WARNING: Failed to return to main directory"
    echo "Current directory: $(pwd)"
}
pwd  # VERIFY: Must show .../genesis (main repo root)

# Final health check
genesis status

echo "✅ SUCCESS: Feature implementation completed for issue #$1"
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
  <parameter name="command">genesis worktree create feature-$1</parameter>
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
- ✅ RED: Acceptance tests written and failing
- ✅ GREEN: Minimal implementation makes tests pass
- ✅ REFACTOR: Code quality improved
- ✅ All Genesis quality gates pass
- ✅ PR created and ready for review
- ✅ No scope creep or unrelated changes
