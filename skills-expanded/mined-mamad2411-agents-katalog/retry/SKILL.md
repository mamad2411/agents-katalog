---
name: retry
description: "Resets a blocked task and runs it again from scratch."
---

# /sulis:retry

This skill **archives prior failure evidence** and **spawns a fresh
executor agent** for a WP that was previously blocked.

## How to invoke (MUST — archive, then spawn the agent)

The skill has two load-bearing actions:

1. Archive the existing BLOCKER + journal + leftover worktree to
   `.archive/` (preserves the audit trail).
2. Spawn the executor agent fresh via the Agent tool.

Do not run the executor's work inline.

### The two-step dispatch

Given `/sulis:retry WP-NNN`:

**Step 1 — archive prior evidence:**

```bash
# Confirm the WP is blocked (else suggest /run-wp instead).
STATUS=$(awk -v wp="WP-NNN" '...parse INDEX status for WP...' \
         .architecture/{project}/work-packages/INDEX.md)
if [ "$STATUS" != "blocked" ]; then
  echo "WP-NNN is not blocked (status=$STATUS). Use /sulis:run-wp instead."
  exit 1
fi

# Archive BLOCKER + journal + leftover worktree.
TS=$(date -u +%Y%m%dT%H%M%SZ)
ARCHIVE=.architecture/{project}/work-packages/.archive
mkdir -p "$ARCHIVE"

mv .architecture/{project}/work-packages/BLOCKER-WP-NNN.md \
   "$ARCHIVE/BLOCKER-WP-NNN-$TS.md"

mv .architecture/{project}/work-packages/.executor-WP-NNN.md \
   "$ARCHIVE/.executor-WP-NNN-$TS.md" 2>/dev/null

# Remove the leftover worktree if present.
WORKTREE=../wp-NNN-worktree
if [ -d "$WORKTREE" ]; then
  git worktree remove --force "$WORKTREE"
fi

# Reset INDEX status from blocked → pending.
# (sed/awk to update the WP-NNN row's Status column.)
```

**Step 2 — spawn the executor:**

```
Agent({
  subagent_type: "sulis:executor",
  description: "Retry WP-NNN after external blocker resolved",
  prompt: """
You are dispatched to retry WP-NNN. The prior BLOCKER and journal
have been archived to .archive/ (preserving the audit trail). The
INDEX has been reset to status: pending.

Start fresh from step 1 of the 10-step lifecycle. Do not attempt
to "resume" the prior run — the archive exists for human
investigation; the retry is a clean start.

WP file: .architecture/{project}/work-packages/WP-NNN-<title>.md
Continuation Discipline applies. See agents/executor.md for the
full contract.

Return ONLY on step-10 success or new BLOCKER written.
""",
})
```

### What you do NOT do in this skill's session

- **Do not edit the BLOCKER record's content.** Archive is move,
  not rewrite. The historical record is preserved as-is.
- **Do not skip the archive step.** A retry without archiving the
  prior BLOCKER loses the diagnostic trail.
- **Do not retry a non-blocked WP.** If the WP is `done`, retry is
  a no-op. If `pending` or `in_progress`, use `/run-wp`.

### What you DO

1. Verify the WP exists and is in `blocked` status.
2. Run the archive step (Bash).
3. Reset the INDEX entry status from `blocked` → `pending`.
4. Spawn the executor agent (Agent tool).
5. Surface the executor's terminal status when it returns.

## When to use

- **External blocker resolved.** Common cases:
  - Platform team freed staging capacity (BLOCKER said *"503 — no
    healthy upstream; cluster at quota"*).
  - CI infra fix landed (BLOCKER said *"CI runner missing
    dependency X"*).
  - Dependency WP completed (BLOCKER said *"WP-9 depends on WP-7
    which wasn't done"*).
- **Configuration changed.** BLOCKER said *"linter/formatter rule
  conflict at project root"*; someone updated `pyproject.toml`;
  retry can now succeed.

## When NOT to use

- **In-scope budget-exhaustion BLOCKERs.** If the verdict was
  `in-scope (budget exhausted)`, the retry would hit the same wall.
  Re-decompose the WP first; do not retry blindly.
- **`permanently_blocked` WPs.** The orchestrator marks a WP
  permanently blocked after multiple retry-then-block cycles. Use
  `/sulis:plan-work` to re-classify.
- **`done` WPs.** No-op.

## See also

- `agents/executor.md` — the agent this skill spawns.
- The `executor-loop-standard.md` BLOCKER record format (EL-08).
- `/sulis:run-wp WP-NNN` — equivalent for non-blocked WPs.
