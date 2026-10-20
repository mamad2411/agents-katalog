# /plan:implement - Implement Plans Step-by-Step with Progress Tracking

**Purpose**: Execute implementation plans from `docs/plans/` by running tasks phase-by-phase, updating progress dynamically, and syncing status to Linear.

**Usage**:
- `/plan:implement [clo-XX]` - Implement specific task plan
- `/plan:implement` - Interactive mode

---

## Project Context

| Setting | Value |
|---------|-------|
| Linear Workspace | cloud-ai |
| Issue Prefix | CLO (e.g., CLO-123) |
| Branch Format | `{prefix}/clo-<number>-<short-desc>` (prefix: feat, fix, chore) |

---

## Command Execution Instructions

When this command is invoked, follow these steps:

### Step 1: Extract Task Number

1. **If user provided task number** (e.g., `/plan:implement clo-36`):
   - Extract the CLO-XX identifier
   - Normalize to uppercase for Linear (e.g., "clo-36" -> "CLO-36")
   - Keep lowercase for file matching (e.g., "clo-36")
   - Proceed to Step 2

2. **If no task number provided** (e.g., `/plan:implement`):
   - Ask user: "Which Linear task plan do you want to implement? (e.g., CLO-36)"
   - Wait for response
   - Extract and normalize the task number
   - Proceed to Step 2

### Step 2: Locate Required Files

**Plan File (REQUIRED)**:

1. Search for plan file: `docs/plans/clo-XX-*.md`
2. **If NOT found**:
   - Display error: "Plan file not found matching: docs/plans/clo-XX-*.md"
   - Suggest: "Run `/plan:create clo-XX` first to generate the implementation plan"
   - Exit command
3. **If found**: Extract full filename, continue

**Design Document (OPTIONAL)**:

1. Search for design doc: `docs/design-docs/clo-XX-*.md`
2. **If found**: Will use for context during implementation
3. **If NOT found**: Continue with warning
   - Display: "Design document not found. Will implement based on plan file only."

**Architecture Reference (ALWAYS READ IF EXISTS)**:

1. Read `docs/arch` or `docs/architecture.md`
2. Use for architecture context, patterns, and validation

**Status File (AUTO-CREATE & AUTO-UPDATE)**:

1. Check if status file exists: `docs/status/clo-XX-*.md`
2. **If found**: Read to understand current progress and decisions
3. **If NOT found**: **Create immediately before starting execution**

**Status file is updated**:
- At the START of implementation (created if missing)
- After EACH task completion (add completed task entry)
- After EACH phase completion (add phase summary)
- At the END of implementation session (final status)

**Proceed to Step 2.5: Initialize Status File**

### Step 2.5: Initialize Status File

**CRITICAL: Create status file before any implementation work begins.**

**Create directory if needed**:
```bash
mkdir -p docs/status
```

**If status file doesn't exist**, create `docs/status/clo-XX-[description].md`:

```markdown
# CLO-XX: [Task Title]

**Linear Task**: https://linear.app/cloud-ai/issue/CLO-XX
**Plan File**: docs/plans/clo-XX-[description].md
**Design Document**: docs/design-docs/clo-XX-[description].md (or "N/A")
**Started**: [Current Date/Time]
**Last Updated**: [Current Date/Time]

---

## Current Status: In Progress

**Overall Progress**: 0% (0/[total] tasks)
**Current Phase**: Phase 1 - [Name]

---

## Session Log

### Session 1 - [Date]

**Started**: [Time]
**Branch**: feat/clo-XX-[description]

#### Tasks Completed This Session

[Will be populated as tasks complete]

---

## Completed Phases

[Will be populated as phases complete]

---

## Technical Decisions

[Key decisions made during implementation]

---

## Important Findings

[Insights discovered during implementation]

---

## Questions & Blockers

[Open questions or blocking issues]

---

## Next Steps

[What needs to happen next]
```

**If status file already exists**:
- Read current state
- Add new session entry:

```markdown
### Session N - [Date]

**Started**: [Time]
**Resuming from**: [Last completed task]
**Branch**: feat/clo-XX-[description]

#### Tasks Completed This Session

[Will be populated]
```

**Proceed to Step 3**

### Step 3: Parse Plan File and Build Execution Queue

**Read plan file** and extract:

1. **Current progress line**: `Overall Progress: X% (Y/Z tasks completed)`
2. **All tasks with status markers**:
   - `[ ]` = To do (queue for execution)
   - `[~]` = In progress (resume from here)
   - `[x]` = Done (skip)
   - `[!]` = Blocked (skip, needs manual intervention)

**Calculate statistics**:

```
Total tasks: Count all checkboxes ([ ], [~], [x], [!])
Completed tasks: Count [x] only
Pending tasks: Count [ ] and [~]
Blocked tasks: Count [!]
Progress percentage: (completed / total) * 100
```

**Build execution queue** (phase-by-phase):

```
Phase 1: [Phase Name]
  - [x] Task 1.1 [SKIP - already done]
  - [ ] Task 1.2 [QUEUE - add to execution list]
  - [ ] Task 1.3 [QUEUE - add to execution list]

Phase 2: [Phase Name]
  - [ ] Task 2.1 [QUEUE - add to execution list]
```

**Intelligent Resume Logic**:

- If task is `[x]`: Skip entirely (already completed)
- If task is `[~]`: Add to queue first (was interrupted)
- If task is `[ ]`: Add to queue in order
- If task is `[!]`: Skip (requires manual intervention)

**Display execution summary to user**:

```
PLAN ANALYSIS: CLO-XX

Total tasks: 20
Completed: 8 (40%)
Pending: 11
Blocked: 1

Next execution queue: 11 tasks across 3 phases

Phases to execute:
- Phase 2: Core Implementation (1 in progress, 2 pending)
- Phase 3: Testing & Validation (4 pending)
- Phase 4: Finalization (4 pending)

Blocked tasks (will skip):
- Phase 2: External API integration (marked [!])

Ready to start implementation? (yes/no)
```

### Step 3.5: Git Branch Management

**Purpose**: Ensure work happens on a feature branch.

**Branch naming convention**:
- Features: `feat/clo-XX-short-description`
- Bug fixes: `fix/clo-XX-short-description`

#### Check Current Branch

```bash
git rev-parse --abbrev-ref HEAD
```

#### Branch Decision Logic

**Case A: On main branch**

```
BRANCH CHECK: Currently on main

Implementation will create commits for CLO-XX.
These commits should be on a feature branch, not main.

Suggested branch name: feat/clo-XX-[short-description]

Options:
1. [create] - Create feature branch and switch to it (recommended)
2. [stay] - Stay on main (NOT recommended)
3. [cancel] - Exit command

Your choice:
```

**Handle user response**:
- **create**: Create and switch to `feat/clo-XX-short-desc`
- **stay**: Warn and continue on main
- **cancel**: Exit command

**Case B: On feature branch matching task**

Example: On `feat/clo-10-websocket` when implementing CLO-10

```
BRANCH CHECK: Currently on feat/clo-10-websocket

This matches task CLO-10. Continuing implementation on this branch.
```

Continue to Step 4.

**Case C: On feature branch NOT matching task**

```
BRANCH CHECK: Currently on feat/clo-15-parser

This branch appears to be for CLO-15, but you're implementing CLO-10.

Options:
1. [switch] - Switch to main and create feat/clo-10 branch
2. [stay] - Continue on this branch
3. [cancel] - Exit

Your choice:
```

### Step 4: Phase-by-Phase Execution Loop

**For each phase** in the execution queue:

#### Phase Start

1. **Display phase overview**:

   ```
   ========================================
   PHASE: Phase 2 - Core Implementation
   ========================================

   Tasks in this phase:
   1. [~] Implement connection handler (IN PROGRESS - resuming)
   2. [ ] Add message parsing
   3. [ ] Implement error handling

   Completed tasks (will skip):
   - [x] Define data structures

   Architecture section: WebSocket module
   Source files: src/websocket/
   ```

2. **Request phase approval**:
   - Ask user: "Ready to execute Phase 2? (yes/no/skip)"
   - **yes**: Proceed with task execution
   - **no**: Stop command completely
   - **skip**: Skip phase, proceed to next

#### Task Execution Loop

**For each task** in the approved phase:

##### Task 1: Mark Task as In Progress

1. Update plan file: Change `[ ]` to `[~]`
2. Update progress percentage
3. Save plan file
4. Display: "Starting: [Task name]"

##### Task 2: Read Context

**If design doc exists**:
1. Search for relevant section
2. Extract technical details, patterns, acceptance criteria

**Always read**:
- Architecture document for patterns
- Existing code in relevant modules for conventions

##### Task 3: Execute Implementation

**Based on task type**, use appropriate approach:

**Code Implementation Tasks**:

- Use `Read` to understand existing code patterns
- Use `Edit` or `Write` to implement
- Follow project conventions

**Test Tasks**:

```bash
# Run tests
cargo test

# Check coverage if configured
cargo tarpaulin
```

**Validation Tasks**:

```bash
# Format check
cargo fmt -- --check

# Lint check
cargo clippy
```

##### Task 4: Handle Errors

**If any step fails**:

1. **Mark task as blocked**: Update plan file `[~]` -> `[!]`
2. **Document error**:

   ```markdown
   - [!] Implement connection handler
     - BLOCKED: Compilation error
     - Error: "trait bound not satisfied"
     - Needs: Review trait implementations
   ```

3. **Ask user**:

   ```
   ERROR: Task failed during execution

   Task: Implement connection handler
   Error: Compilation error

   How would you like to proceed?
   1. [retry] - Try again (after fixing)
   2. [skip] - Mark as blocked and continue
   3. [stop] - Stop execution completely

   Your choice:
   ```

##### Task 5: Validate Completion

**Run validation commands**:

```bash
# Build check
cargo build

# Test check
cargo test

# Format check
cargo fmt -- --check
```

**If validation fails**: Ask user to fix or continue

##### Task 6: Mark Task as Complete

1. Update plan file: `[~]` -> `[x]`
2. Recalculate progress
3. Save plan file

##### Task 7: Create Git Commit

**Commit format** (conventional commits):

| Task Type | Commit Type |
|-----------|-------------|
| New feature | `feat(CLO-XX):` |
| Bug fix | `fix(CLO-XX):` |
| Refactoring | `refactor(CLO-XX):` |
| Documentation | `docs(CLO-XX):` |
| Tests | `test(CLO-XX):` |

**Commit message template**:

```
feat(CLO-XX): implement [concise description]

- [Specific change 1]
- [Specific change 2]

Related: docs/plans/clo-XX-[description].md
```

**Execute commit**:

```bash
git add <modified files>
git commit -m "$(cat <<'EOF'
feat(CLO-XX): implement [task]

- [Details...]

Related: docs/plans/clo-XX-[description].md
EOF
)"
```

**Let pre-commit hooks run** (never use `--no-verify` unless user explicitly requests)

##### Task 8: Update Status File (MANDATORY)

**ALWAYS update the status file after each task completion.**

**Add completed task entry to current session**:

```markdown
#### Tasks Completed This Session

- [x] [Task name from plan]
  - **Time**: [HH:MM]
  - **Module**: src/[module]/
  - **Files Modified**: [List of files]
  - **Commit**: [SHA or "pending"]
  - **Notes**: [Brief implementation notes]
```

**Update header section**:

```markdown
**Last Updated**: [Current Date/Time]

## Current Status: In Progress

**Overall Progress**: X% (Y/Z tasks)
**Current Phase**: Phase N - [Name]
```

**Add to Technical Decisions** (if any decisions were made):

```markdown
## Technical Decisions

- **[Decision Topic]**: [What was decided and why]
  - Task: [Task name]
  - Alternatives considered: [If any]
```

##### Task 9: Display Task Completion

```
COMPLETED: [Task name]

Files changed: [count]
Commit: [SHA]
Validation: PASS

Phase 2 progress: 2/3 tasks complete
Overall progress: 45% (9/20 tasks)
```

**Continue to next task**

#### Phase Completion

**After all tasks in phase complete**:

1. **Update Status File with Phase Summary** (MANDATORY):

   **Add to Completed Phases section**:

   ```markdown
   ## Completed Phases

   ### Phase 2: Core Implementation

   **Completed**: [Date/Time]
   **Tasks**: 3/3 completed
   **Duration**: [Estimated time spent]

   **Summary**:
   - Implemented connection handler
   - Added message parsing
   - Implemented error handling

   **Files Modified**:
   - src/websocket/handler.rs
   - src/websocket/parser.rs
   - src/websocket/mod.rs

   **Commits**:
   - abc1234: feat(CLO-XX): add connection handler
   - def5678: feat(CLO-XX): implement message parsing
   - ghi9012: feat(CLO-XX): add error handling
   ```

   **Update Current Phase**:

   ```markdown
   **Current Phase**: Phase 3 - Testing & Validation
   ```

2. **Display phase summary**:

   ```
   ========================================
   PHASE 2 COMPLETE: Core Implementation
   ========================================

   Completed: 3/3 tasks
   Blocked: 0 tasks
   Commits created: 3

   Overall progress: 55% (11/20 tasks)

   Status file updated: docs/status/clo-XX-[description].md

   Next phase: Phase 3 - Testing & Validation (4 tasks)
   ```

3. **Post progress update to Linear**:

```markdown
## Phase 2 Complete: Core Implementation

**Status**: All tasks completed successfully

**Completed Tasks**:
- Implement connection handler
- Add message parsing
- Implement error handling

**Modules Modified**:
- src/websocket/

**Overall Progress**: 55% (11/20 tasks)

**Commits**:
- abc1234: feat(CLO-XX): add connection handler
- def5678: feat(CLO-XX): implement message parsing
- ghi9012: feat(CLO-XX): add error handling

**Next Phase**: Phase 3 - Testing & Validation
```

### Step 5: Handle Completion or Interruption

**ALWAYS update status file before ending any session.**

#### Case 1: All Tasks Complete (100%)

**Update status file with final state**:

```markdown
**Last Updated**: [Current Date/Time]

## Current Status: Complete

**Overall Progress**: 100% (20/20 tasks)
**Completed**: [Date/Time]
**Total Duration**: [Estimated total time]

---

## Final Summary

**Implementation**: Successfully completed all 20 tasks across 4 phases.

**Modules Created/Modified**:
- src/websocket/ - WebSocket handler
- src/parser/ - Message parsing

**Total Commits**: 20

**Branch**: feat/clo-XX-[description]
**Ready for PR**: Yes
```

**Display to user**:

```
========================================
IMPLEMENTATION COMPLETE: CLO-XX
========================================

Total tasks: 20
Completed: 20 (100%)
Phases completed: 4/4

Files updated:
- Plan: docs/plans/clo-XX-[description].md (100%)
- Status: docs/status/clo-XX-[description].md (Final)

Modules created/modified:
- src/websocket/
- src/parser/

Commits created: 20

Next steps:
1. Run final tests: cargo test
2. Push branch: git push origin feat/clo-XX-short-desc
3. Create PR: gh pr create --title "feat(CLO-XX): [description]"
4. Update Linear task status to "In Review"

-------------------------------------------
ACTION REQUIRED: Update Aggregation Files
-------------------------------------------

Update the following files to reflect task completion:

1. docs/PROJECT.md
   - Move CLO-XX from "Active Work" to "Recently Completed"
   - Move next priority task to "Active Work"

2. docs/ROADMAP.md
   - Update CLO-XX status to "Done"
   - Update phase completion percentage

3. docs/DEPENDENCIES.md
   - Remove CLO-XX from "Current Blockers" (if listed)
   - Move newly unblocked tasks to "Unblocked & Ready"
   - Update dependency graph if needed
```

#### Case 2: User Stopped Mid-Execution

**Update status file before pausing**:

```markdown
**Last Updated**: [Current Date/Time]

## Current Status: Paused

**Overall Progress**: 55% (11/20 tasks)
**Paused at**: Phase 3 - Testing & Validation
**Last Completed Task**: Add message parsing
**Reason**: User requested stop

---

## Session Log

### Session 1 - [Date]

**Started**: [Time]
**Ended**: [Time]
**Reason for pause**: User requested stop

#### Tasks Completed This Session

- [x] Task 1...
- [x] Task 2...

---

## Next Steps

- Resume with: `/plan:implement clo-XX`
- Next task: [First pending task in queue]
```

**Display to user**:

```
========================================
IMPLEMENTATION PAUSED: CLO-XX
========================================

Reason: User requested stop

Progress: 55% (11/20 tasks)
Last completed: "Add message parsing"
Current phase: Phase 3 (0/4 tasks)

Status file updated: docs/status/clo-XX-[description].md

To resume: Run `/plan:implement clo-XX`
```

#### Case 3: Blocked by Errors

**Update status file with blocker details**:

```markdown
**Last Updated**: [Current Date/Time]

## Current Status: Blocked

**Overall Progress**: 55% (11/20 tasks)
**Blocked Tasks**: 2

---

## Questions & Blockers

### Blocker 1: Connection Handler

- **Task**: Implement connection handler
- **Error**: Trait bound not satisfied
- **Error Message**: `the trait 'Send' is not implemented for 'Rc<RefCell<Connection>>'`
- **Resolution Required**: Use Arc<Mutex<>> instead of Rc<RefCell<>>
- **Blocked Since**: [Date/Time]

---

## Next Steps

1. Resolve blockers listed above
2. Update plan file: Change `[!]` to `[ ]` for resolved tasks
3. Re-run: `/plan:implement clo-XX`
```

**Display to user**:

```
========================================
IMPLEMENTATION BLOCKED: CLO-XX
========================================

Progress: 55% (11/20 tasks)
Blocked: 2 tasks

Blocked tasks:
1. [!] Implement connection handler
   - Error: Trait bound not satisfied
   - Needs: Use Arc<Mutex<>> pattern

Status file updated: docs/status/clo-XX-[description].md
(See status file for full error details)

Next steps:
1. Resolve blockers (see docs/status/clo-XX-[description].md)
2. Update plan: Change [!] to [ ]
3. Re-run: /plan:implement clo-XX
```

### Step 6: Post Final Update to Linear

**Post comprehensive update for any completion state**:

```markdown
## Implementation Update: CLO-XX

**Status**: [Complete / Paused / Blocked]
**Overall Progress**: X% (Y/Z tasks)

**Completed Phases**:
- Phase 1: [Name] (X/X tasks)
- Phase 2: [Name] (X/X tasks)

**Modules**:
- src/[module]/: [status]

**Commits**: [count]

**Files**:
- Plan: docs/plans/clo-XX-[description].md
- Status: docs/status/clo-XX-[description].md

**Next Steps**: [Context-specific guidance]
```

### Step 7: Final Display to User

```
========================================
IMPLEMENTATION SESSION SUMMARY
========================================

Task: CLO-XX
Branch: feat/clo-XX-short-desc
Status: [Complete / Paused / Blocked]

Progress: X% (Y/Z tasks)
Phases: A/B completed
Commits: C

Files updated:
- Plan: docs/plans/clo-XX-[description].md
- Status: docs/status/clo-XX-[description].md

Linear: Updated

Next:
1. Review: git log feat/clo-XX-short-desc
2. Push: git push origin feat/clo-XX-short-desc
3. PR: gh pr create --title "feat(CLO-XX): [description]"
```

---

## Special Cases

### Case 1: Plan File Doesn't Exist

```
ERROR: Plan file not found

Expected: docs/plans/clo-XX-*.md

Run: /plan:create clo-XX
```

Exit command.

### Case 2: All Tasks Already Complete

```
PLAN STATUS: Fully implemented (100%)

All 20 tasks are marked [x].

Options:
1. Review completed work
2. Re-execute all tasks (reset to 0%)
3. Exit

Your choice:
```

### Case 3: Git Working Directory Not Clean

```
WARNING: Uncommitted changes detected

Uncommitted files:
[list]

Please commit or stash changes first, then re-run.
```

Exit command.

### Case 4: Design Document Missing

```
WARNING: Design document not found

Will implement based on plan file and architecture doc only.

Continue? (yes/no)
```

### Case 5: Pre-commit Hook Failure

```
COMMIT FAILED: Pre-commit hook rejected

Error: [hook output]

Options:
1. [fix] - I've fixed it, retry
2. [skip-hooks] - Skip hooks (not recommended)
3. [abort] - Stop execution

Your choice:
```

---

## Command Philosophy

**This command is designed to**:

1. **Automate implementation**: Follow patterns from architecture doc
2. **Maintain quality**: Validate after each task
3. **Track progress**: Update plan file and status in real-time
4. **Be resumable**: Continue where you left off
5. **Document thoroughly**: Create comprehensive status files
6. **Follow conventions**: Conventional commits, no emojis

**This command does NOT**:

1. **Make architecture decisions**: Follows plan and design docs
2. **Skip validation**: Always runs tests
3. **Hide errors**: Surfaces failures immediately
4. **Bypass hooks**: Always runs pre-commit (from CLAUDE.md)

---

## Aggregation Files

When a task reaches 100% completion, remind the user to update these project-level files:

| File | Purpose | What to Update |
|------|---------|----------------|
| `docs/PROJECT.md` | Dashboard | Move task to "Recently Completed", update "Active Work" |
| `docs/ROADMAP.md` | Big picture | Update task status, phase completion % |
| `docs/DEPENDENCIES.md` | Blockers | Update blockers, mark unblocked tasks as ready |

These files provide high-level project visibility and should be kept in sync with task completion.
