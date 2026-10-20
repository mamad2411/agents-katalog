---
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[issue-number]"
description: "Refactor code to improve structure without changing behavior"
model: claude-sonnet-4-20250514
---

# Refactoring Workflow for Issue #$1

Improve code structure and maintainability without changing behavior using Genesis and specialized agents.

---

# ⚠️ CRITICAL: EXECUTION vs DELEGATION ⚠️

This workflow has THREE phases with DIFFERENT execution modes:

**📍 SETUP PHASE (STEPS 1-7): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT use Task tool - use Bash tool
- ⚠️ YOU must run commands yourself
- ⚠️ Verify each step completes

**🤖 REFACTORING PHASE (STEP 8): DELEGATION ALLOWED**
- ✅ NOW use Task tool with specialized agents
- ✅ Agents work in worktree YOU created

**📍 FINALIZATION PHASE (STEPS 9-11): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT delegate commits/PRs
- ⚠️ YOU must run commands with Bash tool
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

⚠️ **DO NOT use Task tool for STEPS 1-7 - use Bash tool**

## STEP 1-7: Standard Genesis Worktree Setup

**Tool to use:** `Bash` (for all commands below)

```bash
# Standard setup with Pure Module Isolation
genesis status || echo "⚠️ WARNING: Genesis health issues"
source .envrc || { echo "❌ FATAL: Failed to source .envrc"; exit 1; }
gh issue view $1 || exit 1
genesis clean || echo "⚠️ WARNING: Clean encountered issues"

# Create worktree with auto-symlinked dependencies
genesis worktree create refactor-$1 \
  --focus genesis/ \
  --max-files ${WORKTREE_MAX_FILES:-30}

cd worktrees/refactor-$1/ || { echo "❌ FATAL: Failed to navigate"; exit 1; }
pwd  # VERIFY: Must show .../genesis/worktrees/refactor-$1

# Verify Pure Module Isolation (symlinks auto-created by script)
for symlink in shared-python .genesis .venv docs; do
    [[ -L "$symlink" ]] && echo "✓ $symlink symlinked" || echo "⚠️ $symlink missing"
done

for file in Makefile pyproject.toml pytest.ini .envrc; do
    [[ -f "$file" ]] && echo "✓ $file present" || echo "⚠️ $file missing"
done

source .envrc || { echo "❌ FATAL: Failed to source in worktree"; cd ../../; exit 1; }
genesis version || { echo "❌ Genesis CLI unavailable"; cd ../../; exit 1; }
genesis status || echo "⚠️ WARNING: Status issues detected"
```

---

## 🛑 CHECKPOINT: Verify Before Delegation

**Before STEP 8, verify YOU completed:**
- [ ] genesis clean executed
- [ ] Worktree created at worktrees/refactor-$1/
- [ ] Currently in worktree (pwd shows worktrees/refactor-$1/)
- [ ] Symlinks verified
- [ ] .envrc sourced in worktree
- [ ] Genesis CLI available

✅ **All checks passed?** → Proceed to STEP 8
❌ **Any failed?** → Fix before delegation

---

## ═══════════════════════════════════════════════════
## REFACTORING PHASE - DELEGATION ALLOWED
## ═══════════════════════════════════════════════════

✅ **You may now use Task tool with specialized agents**

## STEP 8: Refactoring Agent Workflow

**Prerequisites:** STEPS 1-7 completed, worktree exists, checkpoint verified

### Agent 1: issue-analyst
Validate refactoring scope and objectives:
```
Analyze issue #$1 to validate refactoring scope.

Requirements:
- Confirm refactoring objectives clear
- Validate atomic scope
- Identify target code for improvement
- Flag any scope creep

Success Criteria:
- Scope validated and focused
- Target code identified
- Objectives clear
```

### Agent 2: test-designer
Ensure comprehensive test coverage FIRST:
```
Ensure test coverage for code being refactored in issue #$1.

Requirements:
- Write tests for existing behavior if missing
- Ensure tests document current functionality
- Tests must pass before refactoring begins
- Use Genesis testing patterns

Success Criteria:
- Adequate test coverage exists
- All tests pass
- Behavior documented by tests
```

### Agent 3: complexity-auditor
Baseline complexity measurement:
```
Measure baseline complexity for refactoring target in issue #$1.

Requirements:
- Measure current cyclomatic complexity
- Identify complex methods and classes
- Document baseline metrics

Success Criteria:
- Complexity metrics captured
- Problem areas identified
```

### Agent 4: refactoring-specialist
Improve structure without behavior change:
```
Refactor code for issue #$1 without changing behavior.

Requirements:
- Extract methods for clarity
- Remove duplication
- Simplify complex conditionals
- Apply appropriate patterns
- Maintain test passage throughout

Success Criteria:
- Structure improved
- All tests still pass
- No behavior changes
- Code more maintainable
```

### Agent 5: complexity-auditor
Verify complexity improved:
```
Verify complexity improvements for issue #$1.

Requirements:
- Re-measure complexity metrics
- Confirm reduction in complexity
- Document improvements

Success Criteria:
- Complexity reduced
- Improvements measured
```

### Agent 6: build-validator
Prove behavior unchanged:
```
Validate refactoring for issue #$1 maintained behavior.

Requirements:
- All tests still pass
- No functionality altered
- Performance not degraded
- Genesis quality gates satisfied

Success Criteria:
- All tests pass
- Behavior unchanged
- Quality gates satisfied
```

---

## ═══════════════════════════════════════════════════
## FINALIZATION PHASE - YOU MUST EXECUTE (NO DELEGATION)
## ═══════════════════════════════════════════════════

⚠️ **DO NOT delegate STEPS 9-11 - use Bash tool**

## STEP 9-11: Quality Gates, Commit, and Return

**Tool to use:** `Bash`

```bash
# Quality validation
echo "🔍 Running quality gates..."
genesis autofix || echo "⚠️ WARNING: Autofix issues"
genesis status || echo "⚠️ WARNING: Status issues"

if [[ -f "Makefile" ]] && grep -q "^test:" Makefile; then
    make test || echo "⚠️ WARNING: Tests failed"
elif [[ -f "pytest.ini" ]]; then
    pytest || echo "⚠️ WARNING: Tests failed"
fi

# Commit and PR
echo "📝 Creating commit..."
git add .
genesis commit -m "refactor: improve code structure for issue #$1

Closes #$1

- Improved code structure without changing behavior
- Maintained all test passage
- Reduced complexity
- No functionality altered"

echo "🚀 Creating PR..."
gh pr create \
  --title "refactor: improve code structure for issue #$1" \
  --body "$(cat <<'EOF'
Closes #$1

## Refactoring Completed
- ✅ Test coverage verified before refactoring
- ✅ Structure improved
- ✅ Complexity reduced
- ✅ All tests still pass
- ✅ Behavior unchanged

## Changes Made
- Improved code structure
- Reduced complexity
- Enhanced maintainability
- No behavior changes

## Validation
- ✅ All tests pass
- ✅ Genesis quality gates satisfied
- ✅ No scope creep
EOF
)" \
  --assignee @me || echo "⚠️ WARNING: PR creation failed"

# Return to main
cd ../../ || echo "⚠️ WARNING: Failed to return"
pwd  # VERIFY: Should show .../genesis
genesis status

echo "✅ SUCCESS: Refactoring completed for issue #$1"
echo "📋 Next: Review PR, merge when ready, then run: /close $1"
```

---

## 🚫 COMMON MISTAKES TO AVOID

**❌ WRONG:** `<invoke name="Task"><parameter name="prompt">Run genesis clean...</parameter></invoke>`
**✅ CORRECT:** `<invoke name="Bash"><parameter name="command">genesis clean</parameter></invoke>`

**❌ WRONG:** Using Task tool in STEPS 1-7 or 9-11
**✅ CORRECT:** Use Bash tool for setup and finalization, Task tool only in STEP 8

---

## Success Criteria
- ✅ Test coverage verified before refactoring
- ✅ Structure improved without behavior change
- ✅ Complexity metrics reduced
- ✅ All tests still pass
- ✅ Quality gates satisfied
- ✅ No scope creep
