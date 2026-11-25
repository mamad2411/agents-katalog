---
name: mig-execute
description: Executes migration plans created by mig-plan skill with automated task execution, progress tracking, and failure recovery. Use this skill whenever the user wants to execute, run, implement, or carry out a migration plan. Also trigger when users say "execute the plan", "run the migration", "implement the migration", "start the migration", or "let's do the migration". This skill requires mig-plan to have run first and orchestrates sub-agents to implement tasks in parallel while tracking progress and handling failures.
---

# Migration Execution Skill

This skill automates the execution of migration plans created by the mig-plan skill. It orchestrates sub-agents to implement tasks in parallel, tracks progress in real-time, handles failures gracefully, and generates comprehensive execution reports.

## What This Skill Does

When invoked, this skill:

1. **Loads the migration plan** from mig-plan-workspace/ (tasks.md, UserStory.md) and mig-prompt-workspace/ (migration-prompt.md)
2. **Parses user stories and tasks** into an executable workflow
3. **Orchestrates sub-agents** to execute tasks in parallel where dependencies allow
4. **Tracks progress** by updating checkboxes in plan files and maintaining a detailed execution log
5. **Handles failures** by pausing, presenting options, and waiting for user decisions
6. **Generates final report** summarizing successes, failures, and next steps
7. **References code understanding** from rgctl output when needed

## When to Use This Skill

Use this skill when the user:
- Says "execute the migration plan"
- Wants to "run the migration" or "start the migration"
- Asks to "implement the migration tasks"
- Says "let's do this" after reviewing a migration plan
- Wants to "carry out the migration" or "make it happen"

## Prerequisites

**CRITICAL**: This skill requires mig-plan to have run first. Before proceeding:

1. Check if `mig-plan-workspace/` exists with these files:
   - `tasks.md` - Task breakdown
   - `UserStory.md` - User stories

2. Check if `mig-prompt-workspace/` exists with:
   - `migration-prompt.md` - Migration specification and design (from mig-prompt-builder)

3. If missing, tell the user: "I need to run mig-plan first to create the migration plan. Should I do that now?"

4. Optionally use **mig-rgctl** during execution for impact analysis ([workflow](../mig-rgctl/references/workflow.md#mig-execute--during-implementation))

## Workflow

### Phase 1: Load and Parse Migration Plan

Read all plan files:

```bash
# Read the migration prompt (contains spec and design)
cat mig-prompt-workspace/migration-prompt.md

# Read the plan files
cat mig-plan-workspace/tasks.md
cat mig-plan-workspace/UserStory.md
```

**Parse the structure**:

1. **Extract user stories** from UserStory.md:
   - Story title
   - Tasks referenced (links to task groups)
   - Acceptance criteria
   - Dependencies

2. **Extract tasks** from tasks.md:
   - Task groups (e.g., "## 1. Migrate Authentication Service")
   - Subtasks with checkboxes (e.g., `- [ ] 1.1 Create new Spring Security configuration`)
   - Integration hooks (test-gen, containerization, deployment)

3. **Build dependency graph**:
   - Parse user story dependencies
   - Identify which tasks can run in parallel
   - Determine execution order based on dependencies

### Phase 2: Initialize Execution Environment

Set up the execution workspace:

```bash
# Create execution workspace
mkdir -p mig-execute-workspace
cd mig-execute-workspace

# Initialize execution log
touch execution-log.md
```

Create the execution log header:

```markdown
# Migration Execution Log

**Started**: [timestamp]
**Migration**: [source → target from migration-prompt.md]
**Plan Version**: [timestamp or version]

---

## Execution Timeline

[Tasks will be logged here with timestamps, status, and outputs]

---

## Summary

- **Total User Stories**: [count]
- **Total Tasks**: [count]
- **Total Subtasks**: [count]
- **Completed**: 0
- **Failed**: 0
- **In Progress**: 0

---
```

### Phase 3: Execute User Stories in Order

For each user story (in dependency order):

1. **Announce the story**:
   ```
   Starting User Story: [title]
   As a: [role]
   I want: [action]
   So that: [benefit]
   ```

2. **Check preconditions**:
   - Verify all dependency user stories are completed
   - Check preconditions listed in the story
   - If not met, log warning and skip (or ask user)

3. **Execute tasks for this story**:
   - Get list of task groups from the story
   - Execute them (see Phase 4)

4. **Validate acceptance criteria**:
   - Check each acceptance criterion
   - Mark as met or not met
   - If not met, this is a failure (go to Phase 6)

5. **Mark story complete**:
   - Update UserStory.md with completion status
   - Log to execution-log.md

### Phase 4: Execute Task Groups (with Parallelization)

For each task group referenced in the current user story:

**Step 1: Analyze subtasks for parallelization**

Group subtasks into:
- **Sequential subtasks** - depend on previous subtasks in the same group
- **Parallel subtasks** - independent, can run concurrently
- **Integration subtasks** - test-gen, containerization, deployment (usually run after code changes)

**Step 2: Execute subtasks**

For each subtask:

**Sequential execution** (must complete before next):
```
1. Spawn a sub-agent with detailed instructions
2. Monitor progress
3. On completion: update checkbox, log result
4. On failure: go to Phase 6 (failure handling)
5. Proceed to next subtask
```

**Parallel execution** (independent subtasks):
```
1. Identify all independent subtasks
2. Spawn sub-agents for each in parallel (in the same turn)
3. Monitor all agents
4. As each completes: update checkbox, log result
5. If any fail: collect all failures, go to Phase 6
6. Wait for all to complete before proceeding
```

**Sub-agent prompt template**:

```
You are executing a migration task. Here's the context:

**Migration Context**:
- Source: [from migration-prompt.md]
- Target: [from migration-prompt.md]
- Overall Goal: [from migration-prompt.md]

**Current Task**: [task group title]

**Subtask to Execute**: [subtask description]

**Code Understanding**: 
[If needed, include relevant info from rgctl metrics / blast-radius queries]
[Include relevant context from migration-prompt.md]

**Dependencies**: [list any outputs from previous subtasks]

**Your Job**:
1. Implement the subtask
2. Run any tests to validate
3. Save outputs to: mig-execute-workspace/outputs/task-[ID]/
4. Report completion with:
   - What you did
   - What files changed
   - Any issues encountered
   - Validation results

**Integration Skills Available**:
- If this involves testing: you can invoke mig-test-gen
- If this involves containerization: you can invoke mig-containerize
- If this involves deployment: you can invoke mig-deploy

Proceed with the implementation.
```

**Step 3: Handle integration subtasks**

When encountering integration subtasks (test-gen, containerization, deployment):

```markdown
- [ ] 1.4 **Test Generation**: Use mig-test-gen to create test cases
```

**For test generation**:
1. Identify what needs testing (from subtask context)
2. Invoke mig-test-gen skill with specific context:
   ```
   /skill mig-test-gen
   Context: Testing [component] after migrating [feature]
   Input: [component files from previous subtasks]
   Expected: [test coverage requirements]
   ```
3. Validate tests run successfully
4. Mark subtask complete

**For containerization**:
1. Identify component to containerize
2. Invoke mig-containerize with configuration:
   ```
   /skill mig-containerize
   Component: [name]
   Config: [env vars, secrets, ConfigMaps from migration-prompt.md]
   ```
3. Validate Dockerfile and config
4. Mark subtask complete

**For deployment**:
1. Identify deployment requirements
2. Invoke mig-deploy with dependencies:
   ```
   /skill mig-deploy
   Component: [name]
   Dependencies: [services, databases]
   Network: [ports, connections]
   ```
3. Validate manifests
4. Mark subtask complete

**Step 4: Update progress**

After each subtask completes:

1. **Update tasks.md** - change `- [ ]` to `- [x]` for the completed subtask
2. **Append to execution-log.md**:
   ```markdown
   ### [timestamp] Task 1.1: [subtask description]
   
   **Status**: ✅ Completed | ❌ Failed | ⏸️ Paused
   **Duration**: [time]
   **Agent**: [sub-agent ID if applicable]
   
   **What was done**:
   [Summary from sub-agent]
   
   **Files changed**:
   - [file 1]
   - [file 2]
   
   **Outputs**:
   - Saved to: mig-execute-workspace/outputs/task-1.1/
   
   **Issues**: [if any]
   
   ---
   ```

3. **Update summary section** in execution-log.md with new counts

### Phase 5: Progress Reporting

Throughout execution, provide periodic updates to the user:

**After each user story completes**:
```
✅ Completed User Story [N]: [title]
   - [X] tasks completed
   - [Y] subtasks completed
   - Duration: [time]

Progress: [N] of [Total] user stories complete ([percentage]%)
```

**After each task group completes**:
```
✅ Completed Task Group [N]: [title]
   - [X] subtasks completed
   - Duration: [time]
```

**Real-time updates** (don't spam, but keep user informed):
- When starting a new user story
- When starting parallel execution of tasks
- When waiting for sub-agents to complete
- When major milestones are hit

### Phase 6: Failure Handling

When a subtask fails:

**Step 1: Pause execution**

Stop all remaining tasks. Let currently running parallel sub-agents complete, but don't start new ones.

**Step 2: Capture failure context**

```markdown
## Failure Report

**Failed Task**: [task group and subtask]
**Error**: [error message from sub-agent]
**Context**: [what was being attempted]
**Files affected**: [list]
**Dependencies**: [what other tasks depend on this]
```

**Step 3: Analyze failure**

Read relevant context:
- The subtask description
- The code being modified (use rgctl if needed)
- Error messages and logs
- Previous subtask outputs

**Step 4: Generate remedy options**

Present 2-4 options to the user:

```
⚠️ Migration task failed. Here's what happened:

**Task**: [description]
**Error**: [error message]

I've identified [N] possible remedies:

1. **[Option 1 - Recommended]**: [description]
   - What I'll do: [explanation]
   - Risk: [Low/Medium/High]
   - Time: [estimate]
   
2. **[Option 2]**: [description]
   - What I'll do: [explanation]
   - Risk: [Low/Medium/High]
   - Time: [estimate]

3. **[Option 3]**: Skip this task for now
   - Continue with independent tasks
   - Come back to this later
   - Risk: Tasks that depend on this will also be skipped

4. **[Option 4]**: Abort migration execution
   - Stop all remaining tasks
   - Generate final report with current progress
   - You can resume later from checkpoint

Which option would you like me to take?
```

**Step 5: Execute user's choice**

Based on user selection:
- **Retry with fix**: Implement the fix, retry the subtask
- **Skip**: Mark task as skipped, continue with independent tasks
- **Abort**: Go to Phase 7 (final report)

**Step 6: Log failure and resolution**

Update execution-log.md:

```markdown
### [timestamp] Task [N]: [subtask] - FAILED

**Error**: [error message]

**Remedy Attempted**: [option chosen]
**Outcome**: [success/failure]

---
```

### Phase 7: Final Report Generation

After all user stories are processed (or execution aborted):

**Step 1: Generate execution summary**

Create `mig-execute-workspace/EXECUTION_REPORT.md`:

```markdown
# Migration Execution Report

**Migration**: [source → target]
**Started**: [timestamp]
**Completed**: [timestamp]
**Duration**: [total time]

---

## Executive Summary

[2-3 sentence overview of what was accomplished]

**Status**: ✅ Completed Successfully | ⚠️ Completed with Issues | ❌ Failed

---

## Statistics

- **Total User Stories**: [count]
  - ✅ Completed: [count]
  - ❌ Failed: [count]
  - ⏸️ Skipped: [count]

- **Total Task Groups**: [count]
  - ✅ Completed: [count]
  - ❌ Failed: [count]
  - ⏸️ Skipped: [count]

- **Total Subtasks**: [count]
  - ✅ Completed: [count]
  - ❌ Failed: [count]
  - ⏸️ Skipped: [count]

---

## User Story Results

### ✅ User Story 1: [title]
- **Status**: Completed
- **Tasks**: [X] of [Y] completed
- **Duration**: [time]
- **Acceptance Criteria**: [X] of [Y] met

### ❌ User Story 2: [title]
- **Status**: Failed
- **Tasks**: [X] of [Y] completed
- **Duration**: [time]
- **Failure Reason**: [description]
- **Remedy Attempted**: [what was tried]

[Repeat for each user story]

---

## Failed Tasks Detail

[If any tasks failed]

### Task [N]: [description]
- **Error**: [error message]
- **Files affected**: [list]
- **Attempted remedies**: [what was tried]
- **Recommendation**: [how to fix]

---

## Files Changed

[List all files modified during execution]

- [file 1] - [what changed]
- [file 2] - [what changed]

---

## Outputs Generated

[List all outputs in mig-execute-workspace/outputs/]

- Task [N] outputs: [description]
- Test reports: [location]
- Container images: [location]
- Deployment manifests: [location]

---

## Next Steps

[Based on completion status]

### If Completed Successfully:
1. Review acceptance criteria validation
2. Run integration tests
3. Deploy to staging environment
4. Monitor for issues

### If Completed with Issues:
1. Review failed tasks in execution log
2. Address failures:
   - [Task X]: [specific remedy]
   - [Task Y]: [specific remedy]
3. Re-run mig-execute to complete remaining tasks
4. Validate fixes

### If Failed:
1. Review failure details above
2. Fix blocking issues:
   - [Issue 1]: [how to fix]
   - [Issue 2]: [how to fix]
3. Consider revising migration plan if needed
4. Re-run mig-execute when ready

---

## Validation

### Acceptance Criteria Met: [X] of [Y]

[For each user story, list acceptance criteria and whether met]

### Tests Passed: [X] of [Y]

[Summary of test results from mig-test-gen]

---

## Detailed Logs

Full execution log available at: `mig-execute-workspace/execution-log.md`

---
```

**Step 2: Present report to user**

Display the executive summary and key statistics:

```
🎉 Migration execution complete!

**Status**: [status]
**User Stories Completed**: [X] of [Y]
**Tasks Completed**: [X] of [Y]
**Duration**: [time]

[If failures]
⚠️ [N] tasks failed. See details in the report.

Full report: mig-execute-workspace/EXECUTION_REPORT.md
Execution log: mig-execute-workspace/execution-log.md

[If successful]
Next steps:
1. Review acceptance criteria
2. Run integration tests
3. Deploy to staging

[If failures]
Next steps:
1. Review failed tasks above
2. Fix issues
3. Re-run mig-execute to continue
```

**Step 3: Offer to continue**

If there are failures or skipped tasks:

```
Would you like me to:
1. Help fix the failed tasks now
2. Re-run execution to complete remaining tasks
3. Revise the migration plan based on learnings
4. Generate a summary for your team
```

## Using Knowledge Graph

Throughout execution, use **mig-rgctl** to understand code ([workflow](../mig-rgctl/references/workflow.md#mig-execute--during-implementation)):

**When to reference rgctl**:
- Before modifying code (understand dependencies)
- When a task fails (analyze what went wrong)
- When determining impact of changes (blast-radius)
- When planning parallel execution (are these truly independent?)

**How to use it**:
```bash
# Hotspots (critical dependencies)
rgctl -f json metrics --pagerank

# Impact of changing a symbol
rgctl -f json blast-radius path/to/Symbol --depth 2

# Communities (helps identify independent work)
rgctl -f json communities list

# One-off slice / flows — lazy CFG OK (see mig-rgctl workflow)
# rgctl -f json slice FILE --line N --variable V
```

### After each completed wave / file-changing phase (required)

Whenever a wave (or user story that edits app sources) finishes — and before starting the next wave, invoking another MigIQ skill that queries the graph, or marking the phase done — refresh the index:

```bash
rgctl update   # required after every set of source-file changes

# Example: javax.* → jakarta.* namespace migration
rgctl -f json find "import javax*" --type import   # expect total == 0

# Optional call-path deltas (install upstream rgctl-review skill)
rgctl -f json review paths --synthetic-head worktree --max-symbols 25
```

If `rgctl -f json status` shows `index_current: false` mid-wave, run `rgctl update` once — do not full rediscover for ordinary edits. Workspace-only markdown under `*-workspace/` does not require `update`.

## Sub-Agent Orchestration Best Practices

**Maximize parallelization**:
- Analyze task dependencies before executing
- Group independent subtasks and spawn all sub-agents in a single turn
- Only run sequentially when there are actual dependencies

**Provide rich context**:
- Include relevant migration-prompt.md excerpts
- Add code examples from the current codebase
- Reference rgctl insights about structure
- Pass outputs from previous subtasks

**Monitor resource usage**:
- Don't spawn more than 10 parallel agents at once
- If execution is slow, reduce parallelism
- Consider user's system resources

**Handle timeouts**:
- Sub-agents might timeout on complex tasks
- If timeout, retry with more time or break into smaller subtasks
- Log timeout and present as failure

## Output Structure

```
mig-execute-workspace/
├── EXECUTION_REPORT.md      # Final summary report
├── execution-log.md          # Detailed timeline log
└── outputs/
    ├── task-1.1/            # Outputs from subtask 1.1
    ├── task-1.2/            # Outputs from subtask 1.2
    ├── tests/               # Test outputs from mig-test-gen
    ├── containers/          # Container configs from mig-containerize
    └── deployments/         # Deployment manifests from mig-deploy
```

Additionally, these files are modified in place:
- `mig-plan-workspace/tasks.md` - checkboxes updated to [x]
- `mig-plan-workspace/UserStory.md` - completion status added

## Important Notes

**Dependency on mig-plan**: This skill cannot run without a migration plan. Always check for plan files first.

**Integration with other skills**: This skill actively invokes mig-test-gen, mig-containerize, and mig-deploy as specified in the plan. Ensure these skills are available.

**Graceful degradation**: If integration skills are not available, log a warning but continue with core migration tasks.

**Resumable execution**: If execution is interrupted, the user can resume by re-running mig-execute. The skill should detect completed tasks (checked checkboxes) and skip them.

**Parallel execution safety**: Ensure parallel subtasks truly don't depend on each other. When in doubt, run sequentially.

**Progress visibility**: Keep the user informed. Don't run silently for long periods.

## Example Invocation

User: "Execute the migration plan"

Skill flow:
1. Check for mig-plan-workspace/ files (if missing, run mig-plan first)
2. Load and parse plan files
3. Initialize execution workspace and log
4. For each user story in order:
   - Check dependencies and preconditions
   - Execute task groups (parallelizing where possible)
   - Invoke integration skills (test-gen, containerize, deploy)
   - Update progress in markdown and log
   - Validate acceptance criteria
5. Handle any failures with user-guided remedies
6. Generate final execution report
7. Present results and next steps to user

## Tips for Success

**Plan before executing**: Read the entire plan before starting. Understand the dependency graph.

**Parallelize wisely**: Independent tasks can run in parallel, but be conservative. It's better to run sequentially than to create race conditions.

**Use rgctl**: When executing code changes, reference the knowledge graph to understand impact and dependencies. After every wave that changes app sources, run `rgctl update` before the next queries or phase.

**Track everything**: Log every action, every file change, every decision. The log is invaluable for debugging.

**Communicate failures clearly**: When things fail, give the user context and actionable options.

**Validate as you go**: Don't wait until the end to check acceptance criteria. Validate after each user story.

**Learn from failures**: If a task fails multiple times, consider whether the plan needs revision.

**Checkpoint progress**: Regular updates to markdown files mean execution is resumable if interrupted.
