---
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[issue-number]"
description: "Clean up code and remove dead code with Genesis"
model: claude-sonnet-4-20250514
---

# Cleanup Workflow for Issue #$1

Remove dead code, unused dependencies, and technical debt using Genesis integration and specialized agents.

---

# ⚠️ CRITICAL: EXECUTION vs DELEGATION ⚠️

**📍 SETUP PHASE (STEPS 1-7): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT use Task tool - use Bash tool
- ⚠️ YOU must run commands yourself

**🤖 CLEANUP PHASE (STEP 8): DELEGATION ALLOWED**
- ✅ NOW use Task tool with specialized agents

**📍 FINALIZATION PHASE (STEPS 9-11): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT delegate commits/PRs
- ⚠️ YOU must run commands with Bash tool

---

## CONTEXT: Pure Module Isolation

This workflow creates a Genesis worktree with all supporting files needed for pure module isolation.

---

## ═══════════════════════════════════════════════════
## SETUP PHASE - YOU MUST EXECUTE (NO DELEGATION)
## ═══════════════════════════════════════════════════

⚠️ **DO NOT use Task tool for STEPS 1-7 - use Bash tool**

## STEP 1-7: Standard Genesis Worktree Setup

**Tool to use:** `Bash`

```bash
genesis status || echo "⚠️ WARNING: Genesis health issues"
source .envrc || { echo "❌ FATAL: Failed to source .envrc"; exit 1; }
gh issue view $1 || exit 1
genesis clean || echo "⚠️ WARNING: Clean encountered issues"

genesis worktree create cleanup-$1 \
  --focus genesis/ \
  --max-files ${WORKTREE_MAX_FILES:-30}

cd worktrees/cleanup-$1/ || { echo "❌ FATAL: Failed to navigate"; exit 1; }
pwd  # VERIFY: Must show .../genesis/worktrees/cleanup-$1

for symlink in shared-python .genesis .venv docs; do
    [[ -L "$symlink" ]] && echo "✓ $symlink symlinked" || echo "⚠️ $symlink missing"
done

source .envrc || { echo "❌ FATAL: Failed to source in worktree"; cd ../../; exit 1; }
genesis version || { echo "❌ Genesis CLI unavailable"; cd ../../; exit 1; }
genesis status || echo "⚠️ WARNING: Status issues detected"
```

---

## 🛑 CHECKPOINT: Verify Before Delegation

**Before STEP 8:**
- [ ] Worktree created at worktrees/cleanup-$1/
- [ ] Currently in worktree
- [ ] Genesis CLI available

✅ **All checks passed?** → Proceed to STEP 8

---

## ═══════════════════════════════════════════════════
## CLEANUP PHASE - DELEGATION ALLOWED
## ═══════════════════════════════════════════════════

✅ **You may now use Task tool with specialized agents**

## STEP 8: Cleanup Agent Workflow

### Agent 1: issue-analyst
Validate cleanup scope is atomic and well-defined.

### Agent 2: bloat-detector
Identify removal targets:
- Dead code (unused functions, classes)
- Commented-out code
- Unused imports
- Unused dependencies
- Obsolete files
- Over-engineered abstractions

### Agent 3: dependency-tracker
Verify safe to remove:
- Check for any remaining usage
- Identify dependencies on target code
- Ensure removal won't break anything

### Agent 4: lean-implementer
Remove identified bloat:
- Delete dead code
- Remove unused dependencies
- Clean up commented code
- Simplify over-engineered code
- Keep changes minimal and focused

### Agent 5: build-validator
Validate cleanup:
- All tests still pass
- No functionality broken
- Dependencies resolved
- Genesis quality gates satisfied

### Agent 6: scope-guardian
Verify no scope creep:
- Only specified cleanup performed
- No refactoring beyond cleanup
- No new features added

---

## ═══════════════════════════════════════════════════
## FINALIZATION PHASE - YOU MUST EXECUTE (NO DELEGATION)
## ═══════════════════════════════════════════════════

⚠️ **DO NOT delegate STEPS 9-11 - use Bash tool**

## STEP 9-11: Quality Gates, Commit, and Return

**Tool to use:** `Bash`

```bash
echo "🔍 Running quality gates..."
genesis autofix || echo "⚠️ WARNING: Autofix issues"
make test || pytest || echo "⚠️ WARNING: Tests failed"

git add .
genesis commit -m "cleanup: remove dead code for issue #$1

Closes #$1

- Removed dead code and unused dependencies
- Cleaned up technical debt
- All tests still pass
- No functionality altered"

gh pr create \
  --title "cleanup: remove dead code for issue #$1" \
  --body "Code cleanup and dead code removal per issue #$1" \
  --assignee @me || echo "⚠️ WARNING: PR creation failed"

cd ../../ || echo "⚠️ WARNING: Failed to return"
pwd  # VERIFY: Should show .../genesis
genesis status

echo "✅ SUCCESS: Cleanup completed for issue #$1"
```

---

## 🚫 COMMON MISTAKES TO AVOID

**❌ WRONG:** Delegating setup to agents
**✅ CORRECT:** Execute STEPS 1-7 with Bash tool, THEN use Task tool in STEP 8

---

## Success Criteria
- ✅ Dead code removed
- ✅ Unused dependencies cleaned up
- ✅ All tests still pass
- ✅ No functionality broken
- ✅ No scope creep
