---
name: conductor-resume
description: "Resume a conductor dispatch — loads fleet state and handovers from Obsidian, presents what completed/failed, and offers verify/redispatch/merge options. Use when: starting a new session after a conductor dispatch, checking on worker results, picking up where a fleet left off. Triggers on: 'resume dispatch', 'what happened with the workers', 'conductor status', 'check on workers', 'pick up where we left off', 'what's the fleet status', 'any workers done', 'resume fleet', or any question about prior conductor dispatch results."
---

# Conductor Resume — Pick Up Where Workers Left Off

You are resuming a prior conductor dispatch. Workers ran as `claude -p` sessions with full governance. Now you need to see what happened and decide next steps.

---

## STEP 1: LOAD FLEET STATE

Run the resume script to load the latest (or specified) dispatch state:

```bash
# Latest dispatch
bash ~/claude-harness/conductor/resume.sh

# Specific dispatch
bash ~/claude-harness/conductor/resume.sh --dispatch-id <id>

# JSON for programmatic use
bash ~/claude-harness/conductor/resume.sh --json
```

Present the output to the user.

**If resume.sh fails:**
- "No conductor evidence found" → No dispatches have been run yet. Tell the user.
- "No fleet state files found" → Dispatches ran but persist.sh didn't write fleet state. Check `_evidence/conductor/` for individual result JSONs and reconstruct manually.
- "dispatch ID not found" → Wrong ID. List available fleet states: `ls {VAULT}/_evidence/conductor/*fleet-state.json`

---

## STEP 2: REVIEW HANDOVERS

For each completed worker, read its handover document:
- Check acceptance criteria: all met?
- Check for decisions the worker made that need validation
- Check for blockers or issues flagged

For each failed worker:
- Read its handover to understand how far it got
- Check if partial work is usable or needs to be scrapped

---

## STEP 3: PRESENT OPTIONS

For **completed workers** (pending verify + merge):

1. **Verify** — Run `/enterprise-verify` on the worker's branch
   ```bash
   git checkout <branch>
   # Run /enterprise-verify
   ```

2. **Review** — Run `/enterprise-review` on the worker's branch
   ```bash
   git diff dev..<branch>
   # Run /enterprise-review
   ```

3. **Merge** — After verify + review pass
   ```bash
   git checkout dev
   git merge <branch> --no-ff -m "feat: merge <name> from conductor dispatch"
   ```

For **failed workers** (needs redispatch):

1. **Resume session** — Continue where the worker left off
   ```bash
   claude --resume "<session_id>" --max-budget-usd <higher_budget>
   ```

2. **Redispatch** — Fresh start with more budget or a better model
   ```bash
   bash ~/claude-harness/conductor/dispatch.sh \
     --task-file <original_task_file> \
     --model <upgraded_model> \
     --budget <higher_budget> \
     --worktree <name>
   ```

3. **Abandon** — Mark as won't-fix and move on

---

## STEP 4: EXECUTE

After user chooses, execute the selected actions. Process one worker at a time:

1. Verify/review completed branches
2. Redispatch or resume failed workers
3. Merge verified branches in dependency order
4. Run full test suite after each merge
5. Clean up merged worktrees

---

## CONSTRAINTS

- Verify before merge — NEVER merge an unverified branch
- One merge at a time — test between each merge
- Failed workers get ONE retry — if they fail twice, escalate to human
- Keep the user informed at each step — this is collaborative, not autonomous
