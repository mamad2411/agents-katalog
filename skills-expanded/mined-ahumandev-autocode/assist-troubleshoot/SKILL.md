---
name: assist-troubleshoot
description: When task fails, use assist-troubleshoot skill, then follow its Troubleshoot Workflow to resolve OBSTACLES.
---

## Outcome Definitions

- APPROACH = changes needed to fix CAUSE and resolve SYMPTOM (like "upgrade lib to v2")
- OBSTACLE = what temporary issue prevent APPROACH from being implemented (like "recent fix caused syntax error")
- BLOCKER = what permanent issue prevent APPROACH from being implemented (like "no sudo access to upgrade library")

### Relationships

- CAUSE indicates why SYMPTOM is observed
- EVIDENCE could support or refute assumed CAUSE
- EVIDENCE is gathered by REPRODUCTION steps or research
- ERROR is a type of EVIDENCE
- TRACE shows where ERROR was observed, could help to mentally simulate CAUSE
- REPRODUCTION is only possible in ENVIRONMENT context
- APPROACH can only be designed after CAUSE was identified
- BLOCKER is obstacle that prevent APPROACH from being implemented (technical/legal/safety)
- BLOCKER is only applies when no other APPROACH is possible

### Hypothesis

- ALWAYS treat CAUSE as hypothesis until confirmed by EVIDENCE
- Consider that EVIDENCE might be misleading or coincidental
- Working SOLUTION supports CAUSE. Verify expected behavior and regression case.

---

## Troubleshoot Workflow

### STEP 1: Cheap EVIDENCE Discovery

1. Gather cheap read-only EVIDENCE without questioning user:
   - Recall previous SOLUTIONS with \`skill\` tool
   - Read configs, env, input
   - Search logs
   - Check Git diff/history
   - Check system, fs, permissions
   - Inspect stored data
   - Trace source
   - Similar SYMPTOMS reported online (suspicious public dependency)
   - Create and run integration tests (debug component in isolation)
2. Summarize EVIDENCE found in 1 sentence.

### STEP 2: Expensive EVIDENCE Discovery

CAUSE is clear when EVIDENCE explains SYMPTOM and no remaining plausibly refute it.

1. CAUSE is clear? Skip to STEP 6 to propose APPROACHES
2. Otherwise, each hypothesis need 1 or more follow up actions to confirm hypothesis in this preferred order (skip irrelevant/impractical actions):
   1. Add debug logging, redeploy, reproduce (in local/test/sandbox env), view new logs
   2. Experiment: create and run stripped project copy with only suspicious components
   3. Reinstall last known working version separately and systematically reapply recent changes until broken
   4. Manual instructions - if above not autonomously possible (most expensive, last resort)

### STEP 3: Report Hypotheses

Report most likely CAUSE hypotheses:
- Which explain observed symptoms
- Not refuted by EVIDENCE
- Conflicting hypotheses? Clarify with more EVIDENCE (repeat STEP 1 or STEP 2 with more focussed queries)

### STEP 4: Confirm/Refute Hypotheses

1. Gather more hypotheses EVIDENCE as follows:
   * \`task\` subagents with details of chosen hypotheses, to confirm/refute chosen hypotheses, in "preferred order" according STEP 2.
   * If "Manual instructions" are needed: use \`primary-manual\` skill to guide user how to gather EVIDENCE and wait for user feedback.
2. Hypotheses refused? Repeat STEP 3 with report of next most likely CAUSE hypotheses.

### STEP 5: Propose APPROACHES

Report to user 1-4 APPROACH PROPOSALS in PROPOSAL REPORT to solve confirmed hypothesis and give each:
   - Numbered heading name
   - Section include in Concise English:
      * numbered list of planned actions (like "update source code", "redeploy", etc.) to solve ROOT CAUSE
      * technical changes (like components affected, scripts modified, db modifications, etc.)
      * behavioral from user perspective (changes to UX, configs, performance, output)
      * warn about potential unwanted side effects of APPROACH

### STEP 6: Choose Best APPROACH

\`question\` user with options matching "Numbered heading name" of listed APPROACHES (previous STEP):
   - answer = selected APPROACH

### STEP 7: Implement APPROACH

1. \`task\` subagents with GOAL to implement selected APPROACH and \`prompt\` must include needed known facts to avoid duplicate rediscoveries.
2. Compare \`task\` output with APPROACH description:
  - If misunderstood or missing details: \`task\` same subagent again with same \`task_id\` to clarify
  - If subagent failed because lack of tools: \`task\` another subagent to complete task
  - If new CONSTRAINT discovered making APPROACH impractical: Restart Troubleshoot Workflow from STEP 1 with new CONSTRAINT and discoveries.
  - If APPROACH SOLUTION completed successfully, continue next STEP.

### STEP 8: Store Durable Lesson

Store durable lesson with \`learn-memory\` subagent as follows:
- Describe OBSTACLE as SYMPTOM (include exact errors)
- Include EVIDENCE that lead to CAUSE (include paths to source code/configs)
- Explain what APPROACH solved issue (include key code/config changes)

### STEP 9: Report

List facts that proof original OBSTACLE is removed (APPROACH SOLUTION success)

### STEP 10: Resume Assistant Workflow

Resume Assistant Workflow to complete original ASSIGNMENT GOAL.
