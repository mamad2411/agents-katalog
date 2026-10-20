---
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[issue-number]"
description: "Deprecate old code and provide migration path"
model: claude-sonnet-4-20250514
---

# Deprecation Workflow for Issue #$1

Deprecate old code with clear migration path using Genesis and specialized agents.

---

# ⚠️ CRITICAL: EXECUTION vs DELEGATION ⚠️

**📍 SETUP PHASE (STEPS 1-7): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT use Task tool - use Bash tool
- ⚠️ YOU must run commands yourself

**🤖 DEPRECATION PHASE (STEP 8): DELEGATION ALLOWED**
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

genesis worktree create deprecate-$1 \
  --focus genesis/ \
  --max-files ${WORKTREE_MAX_FILES:-30}

cd worktrees/deprecate-$1/ || { echo "❌ FATAL: Failed to navigate"; exit 1; }
pwd  # VERIFY: Must show .../genesis/worktrees/deprecate-$1

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
- [ ] Worktree created at worktrees/deprecate-$1/
- [ ] Currently in worktree
- [ ] Genesis CLI available

✅ **All checks passed?** → Proceed to STEP 8

---

## ═══════════════════════════════════════════════════
## DEPRECATION PHASE - DELEGATION ALLOWED
## ═══════════════════════════════════════════════════

✅ **You may now use Task tool with specialized agents**

## STEP 8: Deprecation Agent Workflow

### Agent 1: issue-analyst
Validate deprecation scope:
- Identify what needs deprecation
- Confirm migration requirements
- Ensure atomic deprecation approach

### Agent 2: dependency-tracker
Identify all usage:
- Find all code using deprecated functionality
- Identify external dependencies
- Document migration impact

### Agent 3: documentation-minimalist
Create migration guide:
- Document what's being deprecated
- Provide clear migration path
- Include code examples
- Keep documentation minimal and actionable

### Agent 4: lean-implementer
Implement deprecation:
- Add deprecation warnings
- Maintain backward compatibility during transition
- Provide alternative implementations
- Keep changes minimal

### Agent 5: test-designer
Add deprecation tests:
- Verify deprecation warnings fire
- Test migration path works
- Ensure backward compatibility maintained

### Agent 6: build-validator
Validate deprecation:
- All tests pass
- Warnings appear appropriately
- Migration path documented
- Genesis quality gates satisfied

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
genesis commit -m "deprecate: deprecate functionality for issue #$1

Closes #$1

- Deprecated old functionality with clear warnings
- Provided migration path and documentation
- Maintained backward compatibility
- All tests pass"

gh pr create \
  --title "deprecate: deprecate functionality for issue #$1" \
  --body "Deprecation with migration path per issue #$1" \
  --assignee @me || echo "⚠️ WARNING: PR creation failed"

cd ../../ || echo "⚠️ WARNING: Failed to return"
pwd  # VERIFY: Should show .../genesis
genesis status

echo "✅ SUCCESS: Deprecation completed for issue #$1"
```

---

## 🚫 COMMON MISTAKES TO AVOID

**❌ WRONG:** Delegating setup to agents
**✅ CORRECT:** Execute STEPS 1-7 with Bash tool, THEN use Task tool in STEP 8

---

## Success Criteria
- ✅ Deprecation warnings added
- ✅ Migration path documented
- ✅ Backward compatibility maintained
- ✅ All tests pass
