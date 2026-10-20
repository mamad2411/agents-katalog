---
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[issue-number]"
description: "Optimize performance based on measured bottlenecks"
model: claude-sonnet-4-20250514
---

# Optimization Workflow for Issue #$1

Improve performance based on measured bottlenecks using Genesis and specialized agents.

---

# ⚠️ CRITICAL: EXECUTION vs DELEGATION ⚠️

**📍 SETUP PHASE (STEPS 1-7): YOU EXECUTE DIRECTLY**
- ⚠️ DO NOT use Task tool - use Bash tool
- ⚠️ YOU must run commands yourself

**🤖 OPTIMIZATION PHASE (STEP 8): DELEGATION ALLOWED**
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

genesis worktree create optimize-$1 \
  --focus genesis/ \
  --max-files ${WORKTREE_MAX_FILES:-30}

cd worktrees/optimize-$1/ || { echo "❌ FATAL: Failed to navigate"; exit 1; }
pwd  # VERIFY: Must show .../genesis/worktrees/optimize-$1

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
- [ ] Worktree created at worktrees/optimize-$1/
- [ ] Currently in worktree
- [ ] Symlinks verified
- [ ] Genesis CLI available

✅ **All checks passed?** → Proceed to STEP 8

---

## ═══════════════════════════════════════════════════
## OPTIMIZATION PHASE - DELEGATION ALLOWED
## ═══════════════════════════════════════════════════

✅ **You may now use Task tool with specialized agents**

## STEP 8: Optimization Agent Workflow

### Agent 1: issue-analyst
Validate optimization scope and specific performance targets.

### Agent 2: performance-monitor
Establish baseline metrics:
- Measure current performance
- Profile execution time
- Identify bottlenecks
- Document baseline numbers

### Agent 3: complexity-auditor
Baseline complexity measurement:
- Ensure optimization won't increase complexity
- Document current complexity metrics

### Agent 4: lean-implementer
Implement optimizations:
- Target only measured bottlenecks
- Apply minimal changes for maximum impact
- Avoid premature optimization
- Keep changes focused and minimal

### Agent 5: performance-monitor
Verify performance improved:
- Re-measure performance metrics
- Confirm improvement achieved
- Document performance gains

### Agent 6: complexity-auditor
Ensure complexity not increased:
- Re-measure complexity
- Verify no over-engineering introduced

### Agent 7: build-validator
Validate improvements and no regressions:
- All tests pass
- Performance targets met
- No functionality broken
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
genesis commit -m "perf: optimize performance for issue #$1

Closes #$1

- Optimized based on measured bottlenecks
- Performance targets met
- No functionality altered
- All tests pass"

gh pr create \
  --title "perf: optimize performance for issue #$1" \
  --body "Performance optimization based on measured bottlenecks per issue #$1" \
  --assignee @me || echo "⚠️ WARNING: PR creation failed"

cd ../../ || echo "⚠️ WARNING: Failed to return"
pwd  # VERIFY: Should show .../genesis
genesis status

echo "✅ SUCCESS: Optimization completed for issue #$1"
```

---

## 🚫 COMMON MISTAKES TO AVOID

**❌ WRONG:** Delegating setup to agents
**✅ CORRECT:** Execute STEPS 1-7 with Bash tool, THEN use Task tool in STEP 8

---

## Success Criteria
- ✅ Performance measured before and after
- ✅ Optimization targets met
- ✅ All tests still pass
- ✅ No unnecessary complexity added
