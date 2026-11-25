---
name: conductor-toolkit
description: Consolidated toolkit for conductor. Covers conductor-manage, conductor-implement, conductor-setup, conductor-status, conductor-new-track, conductor-revert, conductor-validator
---
# Conductor Toolkit

## Use this skill when
- Archiving, restoring, renaming, or deleting Conductor tracks
- Listing track status or cleaning orphaned artifacts
- Managing the track lifecycle across active, completed, and archived states
- Needing guidance, best practices, or checklists for check if conductor directory exists
- Needing guidance, best practices, or checklists for conductor setup
- Needing guidance, best practices, or checklists for conductor status
- Needing guidance, best practices, or checklists for implement track
- Needing guidance, best practices, or checklists for new track
- Needing guidance, best practices, or checklists for revert track
- Working on check if conductor directory exists tasks or workflows
- Working on conductor setup tasks or workflows
- Working on conductor status tasks or workflows
- Working on implement track tasks or workflows
- Working on new track tasks or workflows
- Working on revert track tasks or workflows

## Do not use this skill when
- Conductor is not initialized in the repository
- The task is unrelated to Conductor track management
- The task is unrelated to check if conductor directory exists
- The task is unrelated to conductor setup
- The task is unrelated to conductor status
- The task is unrelated to implement track
- The task is unrelated to new track
- The task is unrelated to revert track
- You lack permission to modify track metadata or files
- You need a different domain or tool outside this scope

## Core Capabilities
# Conductor Toolkit

# Track Manager

Manage the complete track lifecycle including archiving, restoring, deleting, renaming, and cleaning up orphaned artifacts.

## Safety

- Backup track data before delete operations.
- Avoid removing archived tracks without explicit approval.

## Resources

- `resources/implementation-playbook.md` for detailed modes, prompts, and workflows.

---

# Implement Track

Execute tasks from a track's implementation plan, following the workflow rules defined in `conductor/workflow.md`.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/product.md` exists
   - Check `conductor/workflow.md` exists
   - Check `conductor/tracks.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Load workflow configuration:
   - Read `conductor/workflow.md`
   - Parse TDD strictness level
   - Parse commit strategy
   - Parse verification checkpoint rules

## Track Selection

### If argument provided:

- Validate track exists: `conductor/tracks/{argument}/plan.md`
- If not found: Search for partial matches, suggest corrections

### If no argument:

1. Read `conductor/tracks.md`
2. Parse for incomplete tracks (status `[ ]` or `[~]`)
3. Display selection menu:

   ```
   Select a track to implement:

   In Progress:
   1. [~] auth_20250115 - User Authentication (Phase 2, Task 3)

   Pending:
   2. [ ] nav-fix_20250114 - Navigation Bug Fix
   3. [ ] dashboard_20250113 - Dashboard Feature

   Enter number or track ID:
   ```

## Context Loading

Load all relevant context for implementation:

1. Track documents:
   - `conductor/tracks/{trackId}/spec.md` - Requirements
   - `conductor/tracks/{trackId}/plan.md` - Task list
   - `conductor/tracks/{trackId}/metadata.json` - Progress state

2. Project context:
   - `conductor/product.md` - Product understanding
   - `conductor/tech-stack.md` - Technical constraints
   - `conductor/workflow.md` - Process rules

3. Code style (if exists):
   - `conductor/code_styleguides/{language}.md`

## Track Status Update

Update track to in-progress:

1. In `conductor/tracks.md`:
   - Change `[ ]` to `[~]` for this track

2. In `conductor/tracks/{trackId}/metadata.json`:
   - Set `status: "in_progress"`
   - Update `updated` timestamp

## Task Execution Loop

For each incomplete task in plan.md (marked with `[ ]`):

### 1. Task Identification

Parse plan.md to find next incomplete task:

- Look for lines matching `- [ ] Task X.Y: {description}`
- Track current phase from structure

### 2. Task Start

Mark task as in-progress:

- Update plan.md: Change `[ ]` to `[~]` for current task
- Announce: "Starting Task X.Y: {description}"

### 3. TDD Workflow (if TDD enabled in workflow.md)

**Red Phase - Write Failing Test:**

```
Following TDD workflow for Task X.Y...

Step 1: Writing failing test
```

- Create test file if needed
- Write test(s) for the task functionality
- Run tests to confirm they fail
- If tests pass unexpectedly: HALT, investigate

**Green Phase - Implement:**

```
Step 2: Implementing minimal code to pass test
```

- Write minimum code to make test pass
- Run tests to confirm they pass
- If tests fail: Debug and fix

**Refactor Phase:**

```
Step 3: Refactoring while keeping tests green
```

- Clean up code
- Run tests to ensure still passing

### 4. Non-TDD Workflow (if TDD not strict)

- Implement the task directly
- Run any existing tests
- Manual verification as needed

### 5. Task Completion

**Commit changes** (following commit strategy from workflow.md):

```bash
git add -A
git commit -m "{commit_prefix}: {task description} ({trackId})"
```

**Update plan.md:**

- Change `[~]` to `[x]` for completed task
- Commit plan update:

```bash
git add conductor/tracks/{trackId}/plan.md
git commit -m "chore: mark task X.Y complete ({trackId})"
```

**Update metadata.json:**

- Increment `tasks.completed`
- Update `updated` timestamp

### 6. Phase Completion Check

After each task, check if phase is complete:

- Parse plan.md for phase structure
- If all tasks in current phase are `[x]`:

**Run phase verification:**

```
Phase {N} complete. Running verification...
```

- Execute verification tasks listed for the phase
- Run full test suite: `npm test` / `pytest` / etc.

**Report and wait for approval:**

```
Phase {N} Verification Results:
- All phase tasks: Complete
- Tests: {passing/failing}
- Verification: {pass/fail}

Approve to continue to Phase {N+1}?
1. Yes, continue
2. No, there are issues to fix
3. Pause implementation
```

**CRITICAL: Wait for explicit user approval before proceeding to next phase.**

## Error Handling During Implementation

### On Tool Failure

```
ERROR: {tool} failed with: {error message}

Options:
1. Retry the operation
2. Skip this task and continue
3. Pause implementation
4. Revert current task changes
```

- HALT and present options
- Do NOT automatically continue

### On Test Failure

```
TESTS FAILING after Task X.Y

Failed tests:
- {test name}: {failure reason}

Options:
1. Attempt to fix
2. Rollback task changes
3. Pause for manual intervention
```

### On Git Failure

```
GIT ERROR: {error message}

This may indicate:
- Uncommitted changes from outside Conductor
- Merge conflicts
- Permission issues

Options:
1. Show git status
2. Attempt to resolve
3. Pause for manual intervention
```

## Track Completion

When all phases and tasks are complete:

### 1. Final Verification

```
All tasks complete. Running final verification...
```

- Run full test suite
- Check all acceptance criteria from spec.md
- Generate verification report

### 2. Update Track Status

In `conductor/tracks.md`:

- Change `[~]` to `[x]` for this track
- Update the "Updated" column

In `conductor/tracks/{trackId}/metadata.json`:

- Set `status: "complete"`
- Set `phases.completed` to total
- Set `tasks.completed` to total
- Update `updated` timestamp

In `conductor/tracks/{trackId}/plan.md`:

- Update header status to `[x] Complete`

### 3. Documentation Sync Offer

```
Track complete! Would you like to sync documentation?

This will update:
- conductor/product.md (if new features added)
- conductor/tech-stack.md (if new dependencies added)
- README.md (if applicable)

1. Yes, sync documentation
2. No, skip
```

### 4. Cleanup Offer

```
Track {trackId} is complete.

Cleanup options:
1. Archive - Move to conductor/tracks/_archive/
2. Delete - Remove track directory
3. Keep - Leave as-is
```

### 5. Completion Summary

```
Track Complete: {track title}

Summary:
- Track ID: {trackId}
- Phases completed: {N}/{N}
- Tasks completed: {M}/{M}
- Commits created: {count}
- Tests: All passing

Next steps:
- Run /conductor:status to see project progress
- Run /conductor:new-track for next feature
```

## Progress Tracking

Maintain progress in `metadata.json` throughout:

```json
{
  "id": "auth_20250115",
  "title": "User Authentication",
  "type": "feature",
  "status": "in_progress",
  "created": "2025-01-15T10:00:00Z",
  "updated": "2025-01-15T14:30:00Z",
  "current_phase": 2,
  "current_task": "2.3",
  "phases": {
    "total": 3,
    "completed": 1
  },
  "tasks": {
    "total": 12,
    "completed": 7
  },
  "commits": [
    "abc1234: feat: add login form (auth_20250115)",
    "def5678: feat: add password validation (auth_20250115)"
  ]
}
```

## Resumption

If implementation is paused and resumed:

1. Load `metadata.json` for current state
2. Find current task from `current_task` field
3. Check if task is `[~]` in plan.md
4. Ask user:

   ```
   Resuming track: {title}

   Last task in progress: Task {X.Y}: {description}

   Options:
   1. Continue from where we left off
   2. Restart current task
   3. Show progress summary first
   ```

## Critical Rules

1. **NEVER skip verification checkpoints** - Always wait for user approval between phases
2. **STOP on any failure** - Do not attempt to continue past errors
3. **Follow workflow.md strictly** - TDD, commit strategy, and verification rules are mandatory
4. **Keep plan.md updated** - Task status must reflect actual progress
5. **Commit frequently** - Each task completion should be committed
6. **Track all commits** - Record commit hashes in metadata.json for potential revert

---

# Conductor Setup

Initialize or resume Conductor project setup. This command creates foundational project documentation through interactive Q&A.

## Pre-flight Checks

1. Check if `conductor/` directory already exists in the project root:
   - If `conductor/product.md` exists: Ask user whether to resume setup or reinitialize
   - If `conductor/setup_state.json` exists with incomplete status: Offer to resume from last step

2. Detect project type by checking for existing indicators:
   - **Greenfield (new project)**: No .git, no package.json, no requirements.txt, no go.mod, no src/ directory
   - **Brownfield (existing project)**: Any of the above exist

3. Load or create `conductor/setup_state.json`:
   ```json
   {
     "status": "in_progress",
     "project_type": "greenfield|brownfield",
     "current_section": "product|guidelines|tech_stack|workflow|styleguides",
     "current_question": 1,
     "completed_sections": [],
     "answers": {},
     "files_created": [],
     "started_at": "ISO_TIMESTAMP",
     "last_updated": "ISO_TIMESTAMP"
   }
   ```

## Interactive Q&A Protocol

**CRITICAL RULES:**

- Ask ONE question per turn
- Wait for user response before proceeding
- Offer 2-3 suggested answers plus "Type your own" option
- Maximum 5 questions per section
- Update `setup_state.json` after each successful step
- Validate file writes succeeded before continuing

### Section 1: Product Definition (max 5 questions)

**Q1: Project Name**

```
What is your project name?

Suggested:
1. [Infer from directory name]
2. [Infer from package.json/go.mod if brownfield]
3. Type your own
```

**Q2: Project Description**

```
Describe your project in one sentence.

Suggested:
1. A web application that [does X]
2. A CLI tool for [doing Y]
3. Type your own
```

**Q3: Problem Statement**

```
What problem does this project solve?

Suggested:
1. Users struggle to [pain point]
2. There's no good way to [need]
3. Type your own
```

**Q4: Target Users**

```
Who are the primary users?

Suggested:
1. Developers building [X]
2. End users who need [Y]
3. Internal teams managing [Z]
4. Type your own
```

**Q5: Key Goals (optional)**

```
What are 2-3 key goals for this project? (Press enter to skip)
```

### Section 2: Product Guidelines (max 3 questions)

**Q1: Voice and Tone**

```
What voice/tone should documentation and UI text use?

Suggested:
1. Professional and technical
2. Friendly and approachable
3. Concise and direct
4. Type your own
```

**Q2: Design Principles**

```
What design principles guide this project?

Suggested:
1. Simplicity over features
2. Performance first
3. Developer experience focused
4. User safety and reliability
5. Type your own (comma-separated)
```

### Section 3: Tech Stack (max 5 questions)

For **brownfield projects**, first analyze existing code:

- Run `Glob` to find package.json, requirements.txt, go.mod, Cargo.toml, etc.
- Parse detected files to pre-populate tech stack
- Present findings and ask for confirmation/additions

**Q1: Primary Language(s)**

```
What primary language(s) does this project use?

[For brownfield: "I detected: Python 3.11, JavaScript. Is this correct?"]

Suggested:
1. TypeScript
2. Python
3. Go
4. Rust
5. Type your own (comma-separated)
```

**Q2: Frontend Framework (if applicable)**

```
What frontend framework (if any)?

Suggested:
1. React
2. Vue
3. Next.js
4. None / CLI only
5. Type your own
```

**Q3: Backend Framework (if applicable)**

```
What backend framework (if any)?

Suggested:
1. Express / Fastify
2. Django / FastAPI
3. Go standard library
4. None / Frontend only
5. Type your own
```

**Q4: Database (if applicable)**

```
What database (if any)?

Suggested:
1. PostgreSQL
2. MongoDB
3. SQLite
4. None / Stateless
5. Type your own
```

**Q5: Infrastructure**

```
Where will this be deployed?

Suggested:
1. AWS (Lambda, ECS, etc.)
2. Vercel / Netlify
3. Self-hosted / Docker
4. Not decided yet
5. Type your own
```

### Section 4: Workflow Preferences (max 4 questions)

**Q1: TDD Strictness**

```
How strictly should TDD be enforced?

Suggested:
1. Strict - tests required before implementation
2. Moderate - tests encouraged, not blocked
3. Flexible - tests recommended for complex logic
```

**Q2: Commit Strategy**

```
What commit strategy should be followed?

Suggested:
1. Conventional Commits (feat:, fix:, etc.)
2. Descriptive messages, no format required
3. Squash commits per task
```

**Q3: Code Review Requirements**

```
What code review policy?

Suggested:
1. Required for all changes
2. Required for non-trivial changes
3. Optional / self-review OK
```

**Q4: Verification Checkpoints**

```
When should manual verification be required?

Suggested:
1. After each phase completion
2. After each task completion
3. Only at track completion
```

### Section 5: Code Style Guides (max 2 questions)

**Q1: Languages to Include**

```
Which language style guides should be generated?

[Based on detected languages, pre-select]

Options:
1. TypeScript/JavaScript
2. Python
3. Go
4. Rust
5. All detected languages
6. Skip style guides
```

**Q2: Existing Conventions**

```
Do you have existing linting/formatting configs to incorporate?

[For brownfield: "I found .eslintrc, .prettierrc. Should I incorporate these?"]

Suggested:
1. Yes, use existing configs
2. No, generate fresh guides
3. Skip this step
```

## Artifact Generation

After completing Q&A, generate the following files:

### 1. conductor/index.md

```markdown
# Conductor - [Project Name]

Navigation hub for project context.

## Quick Links

- [Product Definition](./product.md)
- [Product Guidelines](./product-guidelines.md)
- [Tech Stack](./tech-stack.md)
- [Workflow](./workflow.md)
- [Tracks](./tracks.md)

## Active Tracks

<!-- Auto-populated by /conductor:new-track -->

## Getting Started

Run `/conductor:new-track` to create your first feature track.
```

### 2. conductor/product.md

Template populated with Q&A answers for:

- Project name and description
- Problem statement
- Target users
- Key goals

### 3. conductor/product-guidelines.md

Template populated with:

- Voice and tone
- Design principles
- Any additional standards

### 4. conductor/tech-stack.md

Template populated with:

- Languages (with versions if detected)
- Frameworks (frontend, backend)
- Database
- Infrastructure
- Key dependencies (for brownfield, from package files)

### 5. conductor/workflow.md

Template populated with:

- TDD policy and strictness level
- Commit strategy and conventions
- Code review requirements
- Verification checkpoint rules
- Task lifecycle definition

### 6. conductor/tracks.md

```markdown
# Tracks Registry

| Status | Track ID | Title | Created | Updated |
| ------ | -------- | ----- | ------- | ------- |

<!-- Tracks registered by /conductor:new-track -->
```

### 7. conductor/code_styleguides/

Generate selected style guides from `$CLAUDE_PLUGIN_ROOT/templates/code_styleguides/`

## State Management

After each successful file creation:

1. Update `setup_state.json`:
   - Add filename to `files_created` array
   - Update `last_updated` timestamp
   - If section complete, add to `completed_sections`
2. Verify file exists with `Read` tool

## Completion

When all files are created:

1. Set `setup_state.json` status to "complete"
2. Display summary:

   ```
   Conductor setup complete!

   Created artifacts:
   - conductor/index.md
   - conductor/product.md
   - conductor/product-guidelines.md
   - conductor/tech-stack.md
   - conductor/workflow.md
   - conductor/tracks.md
   - conductor/code_styleguides/[languages]

   Next steps:
   1. Review generated files and customize as needed
   2. Run /conductor:new-track to create your first track
   ```

## Resume Handling

If `--resume` argument or resuming from state:

1. Load `setup_state.json`
2. Skip completed sections
3. Resume from `current_section` and `current_question`
4. Verify previously created files still exist
5. If files missing, offer to regenerate

## Error Handling

- If file write fails: Halt and report error, do not update state
- If user cancels: Save current state for future resume
- If state file corrupted: Offer to start fresh or attempt recovery

---

# Conductor Status

Display the current status of the Conductor project, including overall progress, active tracks, and next actions.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/product.md` exists
   - Check `conductor/tracks.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Check for any tracks:
   - Read `conductor/tracks.md`
   - If no tracks registered: Display setup complete message with suggestion to create first track

## Data Collection

### 1. Project Information

Read `conductor/product.md` and extract:

- Project name
- Project description

### 2. Tracks Overview

Read `conductor/tracks.md` and parse:

- Total tracks count
- Completed tracks (marked `[x]`)
- In-progress tracks (marked `[~]`)
- Pending tracks (marked `[ ]`)

### 3. Detailed Track Analysis

For each track in `conductor/tracks/`:

Read `conductor/tracks/{trackId}/plan.md`:

- Count total tasks (lines matching `- [x]`, `- [~]`, `- [ ]` with Task prefix)
- Count completed tasks (`[x]`)
- Count in-progress tasks (`[~]`)
- Count pending tasks (`[ ]`)
- Identify current phase (first phase with incomplete tasks)
- Identify next pending task

Read `conductor/tracks/{trackId}/metadata.json`:

- Track type (feature, bug, chore, refactor)
- Created date
- Last updated date
- Status

Read `conductor/tracks/{trackId}/spec.md`:

- Check for any noted blockers or dependencies

### 4. Blocker Detection

Scan for potential blockers:

- Tasks marked with `BLOCKED:` prefix
- Dependencies on incomplete tracks
- Failed verification tasks

## Output Format

### Full Project Status (no argument)

```
================================================================================
                        PROJECT STATUS: {Project Name}
================================================================================
Last Updated: {current timestamp}

--------------------------------------------------------------------------------
                              OVERALL PROGRESS
--------------------------------------------------------------------------------

Tracks:     {completed}/{total} completed ({percentage}%)
Tasks:      {completed}/{total} completed ({percentage}%)

Progress:   [##########..........] {percentage}%

--------------------------------------------------------------------------------
                              TRACK SUMMARY
--------------------------------------------------------------------------------

| Status | Track ID          | Type    | Tasks      | Last Updated |
|--------|-------------------|---------|------------|--------------|
| [x]    | auth_20250110     | feature | 12/12 (100%)| 2025-01-12  |
| [~]    | dashboard_20250112| feature | 7/15 (47%) | 2025-01-15  |
| [ ]    | nav-fix_20250114  | bug     | 0/4 (0%)   | 2025-01-14  |

--------------------------------------------------------------------------------
                              CURRENT FOCUS
--------------------------------------------------------------------------------

Active Track:  dashboard_20250112 - Dashboard Feature
Current Phase: Phase 2: Core Components
Current Task:  [~] Task 2.3: Implement chart rendering

Progress in Phase:
  - [x] Task 2.1: Create dashboard layout
  - [x] Task 2.2: Add data fetching hooks
  - [~] Task 2.3: Implement chart rendering
  - [ ] Task 2.4: Add filter controls

--------------------------------------------------------------------------------
                              NEXT ACTIONS
--------------------------------------------------------------------------------

1. Complete: Task 2.3 - Implement chart rendering (dashboard_20250112)
2. Then: Task 2.4 - Add filter controls (dashboard_20250112)
3. After Phase 2: Phase verification checkpoint

--------------------------------------------------------------------------------
                               BLOCKERS
--------------------------------------------------------------------------------

{If blockers found:}
! BLOCKED: Task 3.1 in dashboard_20250112 depends on api_20250111 (incomplete)

{If no blockers:}
No blockers identified.

================================================================================
Commands: /conductor:implement {trackId} | /conductor:new-track | /conductor:revert
================================================================================
```

### Single Track Status (with track-id argument)

```
================================================================================
                    TRACK STATUS: {Track Title}
================================================================================
Track ID:    {trackId}
Type:        {feature|bug|chore|refactor}
Status:      {Pending|In Progress|Complete}
Created:     {date}
Updated:     {date}

--------------------------------------------------------------------------------
                              SPECIFICATION
--------------------------------------------------------------------------------

Summary: {brief summary from spec.md}

Acceptance Criteria:
  - [x] {Criterion 1}
  - [ ] {Criterion 2}
  - [ ] {Criterion 3}

--------------------------------------------------------------------------------
                              IMPLEMENTATION
--------------------------------------------------------------------------------

Overall:    {completed}/{total} tasks ({percentage}%)
Progress:   [##########..........] {percentage}%

## Phase 1: {Phase Name} [COMPLETE]
  - [x] Task 1.1: {description}
  - [x] Task 1.2: {description}
  - [x] Verification: {description}

## Phase 2: {Phase Name} [IN PROGRESS]
  - [x] Task 2.1: {description}
  - [~] Task 2.2: {description}  <-- CURRENT
  - [ ] Task 2.3: {description}
  - [ ] Verification: {description}

## Phase 3: {Phase Name} [PENDING]
  - [ ] Task 3.1: {description}
  - [ ] Task 3.2: {description}
  - [ ] Verification: {description}

--------------------------------------------------------------------------------
                              GIT HISTORY
--------------------------------------------------------------------------------

Related Commits:
  abc1234 - feat: add login form ({trackId})
  def5678 - feat: add password validation ({trackId})
  ghi9012 - chore: mark task 1.2 complete ({trackId})

--------------------------------------------------------------------------------
                              NEXT STEPS
--------------------------------------------------------------------------------

1. Current: Task 2.2 - {description}
2. Next: Task 2.3 - {description}
3. Phase 2 verification pending

================================================================================
Commands: /conductor:implement {trackId} | /conductor:revert {trackId}
================================================================================
```

## Status Markers Legend

Display at bottom if helpful:

```
Legend:
  [x] = Complete
  [~] = In Progress
  [ ] = Pending
  [!] = Blocked
```

## Error States

### No Tracks Found

```
================================================================================
                        PROJECT STATUS: {Project Name}
================================================================================

Conductor is set up but no tracks have been created yet.

To get started:
  /conductor:new-track "your feature description"

================================================================================
```

### Conductor Not Initialized

```
ERROR: Conductor not initialized

Could not find conductor/product.md

Run /conductor:setup to initialize Conductor for this project.
```

### Track Not Found (with argument)

```
ERROR: Track not found: {argument}

Available tracks:
  - auth_20250115
  - dashboard_20250112
  - nav-fix_20250114

Usage: /conductor:status [track-id]
```

## Calculation Logic

### Task Counting

```
For each plan.md:
  - Complete: count lines matching /^- \[x\] Task/
  - In Progress: count lines matching /^- \[~\] Task/
  - Pending: count lines matching /^- \[ \] Task/
  - Total: Complete + In Progress + Pending
```

### Phase Detection

```
Current phase = first phase header followed by any incomplete task ([ ] or [~])
```

### Progress Bar

```
filled = floor((completed / total) * 20)
empty = 20 - filled
bar = "[" + "#".repeat(filled) + ".".repeat(empty) + "]"
```

## Quick Mode

If invoked with `--quick` or `-q`:

```
{Project Name}: {completed}/{total} tasks ({percentage}%)
Active: {trackId} - Task {X.Y}
```

## JSON Output

If invoked with `--json`:

```json
{
  "project": "{name}",
  "timestamp": "ISO_TIMESTAMP",
  "tracks": {
    "total": N,
    "completed": X,
    "in_progress": Y,
    "pending": Z
  },
  "tasks": {
    "total": M,
    "completed": A,
    "in_progress": B,
    "pending": C
  },
  "current": {
    "track": "{trackId}",
    "phase": N,
    "task": "{X.Y}"
  },
  "blockers": []
}
```

---

# New Track

Create a new track (feature, bug fix, chore, or refactor) with a detailed specification and phased implementation plan.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/product.md` exists
   - Check `conductor/tech-stack.md` exists
   - Check `conductor/workflow.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Load context files:
   - Read `conductor/product.md` for product context
   - Read `conductor/tech-stack.md` for technical context
   - Read `conductor/workflow.md` for TDD/commit preferences

## Track Classification

Determine track type based on description or ask user:

```
What type of track is this?

1. Feature - New functionality
2. Bug - Fix for existing issue
3. Chore - Maintenance, dependencies, config
4. Refactor - Code improvement without behavior change
```

## Interactive Specification Gathering

**CRITICAL RULES:**

- Ask ONE question per turn
- Wait for user response before proceeding
- Tailor questions based on track type
- Maximum 6 questions total

### For Feature Tracks

**Q1: Feature Summary**

```
Describe the feature in 1-2 sentences.
[If argument provided, confirm: "You want to: {argument}. Is this correct?"]
```

**Q2: User Story**

```
Who benefits and how?

Format: As a [user type], I want to [action] so that [benefit].
```

**Q3: Acceptance Criteria**

```
What must be true for this feature to be complete?

List 3-5 acceptance criteria (one per line):
```

**Q4: Dependencies**

```
Does this depend on any existing code, APIs, or other tracks?

1. No dependencies
2. Depends on existing code (specify)
3. Depends on incomplete track (specify)
```

**Q5: Scope Boundaries**

```
What is explicitly OUT of scope for this track?
(Helps prevent scope creep)
```

**Q6: Technical Considerations (optional)**

```
Any specific technical approach or constraints?
(Press enter to skip)
```

### For Bug Tracks

**Q1: Bug Summary**

```
What is broken?
[If argument provided, confirm]
```

**Q2: Steps to Reproduce**

```
How can this bug be reproduced?
List steps:
```

**Q3: Expected vs Actual Behavior**

```
What should happen vs what actually happens?
```

**Q4: Affected Areas**

```
What parts of the system are affected?
```

**Q5: Root Cause Hypothesis (optional)**

```
Any hypothesis about the cause?
(Press enter to skip)
```

### For Chore/Refactor Tracks

**Q1: Task Summary**

```
What needs to be done?
[If argument provided, confirm]
```

**Q2: Motivation**

```
Why is this work needed?
```

**Q3: Success Criteria**

```
How will we know this is complete?
```

**Q4: Risk Assessment**

```
What could go wrong? Any risky changes?
```

## Track ID Generation

Generate track ID in format: `{shortname}_{YYYYMMDD}`

- Extract shortname from feature/bug summary (2-3 words, lowercase, hyphenated)
- Use current date
- Example: `user-auth_20250115`, `nav-bug_20250115`

Validate uniqueness:

- Check `conductor/tracks.md` for existing IDs
- If collision, append counter: `user-auth_20250115_2`

## Specification Generation

Create `conductor/tracks/{trackId}/spec.md`:

```markdown
# Specification: {Track Title}

**Track ID:** {trackId}
**Type:** {Feature|Bug|Chore|Refactor}
**Created:** {YYYY-MM-DD}
**Status:** Draft

## Summary

{1-2 sentence summary}

## Context

{Product context from product.md relevant to this track}

## User Story (for features)

As a {user}, I want to {action} so that {benefit}.

## Problem Description (for bugs)

{Bug description, steps to reproduce}

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Dependencies

{List dependencies or "None"}

## Out of Scope

{Explicit exclusions}

## Technical Notes

{Technical considerations or "None specified"}

---

_Generated by Conductor. Review and edit as needed._
```

## User Review of Spec

Display the generated spec and ask:

```
Here is the specification I've generated:

{spec content}

Is this specification correct?
1. Yes, proceed to plan generation
2. No, let me edit (opens for inline edits)
3. Start over with different inputs
```

## Plan Generation

After spec approval, generate `conductor/tracks/{trackId}/plan.md`:

### Plan Structure

```markdown
# Implementation Plan: {Track Title}

**Track ID:** {trackId}
**Spec:** [spec.md](./spec.md)
**Created:** {YYYY-MM-DD}
**Status:** [ ] Not Started

## Overview

{Brief summary of implementation approach}

## Phase 1: {Phase Name}

{Phase description}

### Tasks

- [ ] Task 1.1: {Description}
- [ ] Task 1.2: {Description}
- [ ] Task 1.3: {Description}

### Verification

- [ ] {Verification step for phase 1}

## Phase 2: {Phase Name}

{Phase description}

### Tasks

- [ ] Task 2.1: {Description}
- [ ] Task 2.2: {Description}

### Verification

- [ ] {Verification step for phase 2}

## Phase 3: {Phase Name} (if needed)

...

## Final Verification

- [ ] All acceptance criteria met
- [ ] Tests passing
- [ ] Documentation updated (if applicable)
- [ ] Ready for review

---

_Generated by Conductor. Tasks will be marked [~] in progress and [x] complete._
```

### Phase Guidelines

- Group related tasks into logical phases
- Each phase should be independently verifiable
- Include verification task after each phase
- TDD tracks: Include test writing tasks before implementation tasks
- Typical structure:
  1. **Setup/Foundation** - Initial scaffolding, interfaces
  2. **Core Implementation** - Main functionality
  3. **Integration** - Connect with existing system
  4. **Polish** - Error handling, edge cases, docs

## User Review of Plan

Display the generated plan and ask:

```
Here is the implementation plan:

{plan content}

Is this plan correct?
1. Yes, create the track
2. No, let me edit (opens for inline edits)
3. Add more phases/tasks
4. Start over
```

## Track Creation

After plan approval:

1. Create directory structure:

   ```
   conductor/tracks/{trackId}/
   ├── spec.md
   ├── plan.md
   ├── metadata.json
   └── index.md
   ```

2. Create `metadata.json`:

   ```json
   {
     "id": "{trackId}",
     "title": "{Track Title}",
     "type": "feature|bug|chore|refactor",
     "status": "pending",
     "created": "ISO_TIMESTAMP",
     "updated": "ISO_TIMESTAMP",
     "phases": {
       "total": N,
       "completed": 0
     },
     "tasks": {
       "total": M,
       "completed": 0
     }
   }
   ```

3. Create `index.md`:

   ```markdown
   # Track: {Track Title}

   **ID:** {trackId}
   **Status:** Pending

   ## Documents

   - [Specification](./spec.md)
   - [Implementation Plan](./plan.md)

   ## Progress

   - Phases: 0/{N} complete
   - Tasks: 0/{M} complete

   ## Quick Links

   - [Back to Tracks](../../tracks.md)
   - [Product Context](../../product.md)
   ```

4. Register in `conductor/tracks.md`:
   - Add row to tracks table
   - Format: `| [ ] | {trackId} | {title} | {created} | {created} |`

5. Update `conductor/index.md`:
   - Add track to "Active Tracks" section

## Completion Message

```
Track created successfully!

Track ID: {trackId}
Location: conductor/tracks/{trackId}/

Files created:
- spec.md - Requirements specification
- plan.md - Phased implementation plan
- metadata.json - Track metadata
- index.md - Track navigation

Next steps:
1. Review spec.md and plan.md, make any edits
2. Run /conductor:implement {trackId} to start implementation
3. Run /conductor:status to see project progress
```

## Error Handling

- If directory creation fails: Halt and report, do not register in tracks.md
- If any file write fails: Clean up partial track, report error
- If tracks.md update fails: Warn user to manually register track

---

# Revert Track

Revert changes by logical work unit with full git awareness. Supports reverting entire tracks, specific phases, or individual tasks.

## Pre-flight Checks

1. Verify Conductor is initialized:
   - Check `conductor/tracks.md` exists
   - If missing: Display error and suggest running `/conductor:setup` first

2. Verify git repository:
   - Run `git status` to confirm git repo
   - Check for uncommitted changes
   - If uncommitted changes exist:

     ```
     WARNING: Uncommitted changes detected

     Files with changes:
     {list of files}

     Options:
     1. Stash changes and continue
     2. Commit changes first
     3. Cancel revert
     ```

3. Verify git is clean enough to revert:
   - No merge in progress
   - No rebase in progress
   - If issues found: Halt and explain resolution steps

## Target Selection

### If argument provided:

Parse the argument format:

**Full track:** `{trackId}`

- Example: `auth_20250115`
- Reverts all commits for the entire track

**Specific phase:** `{trackId}:phase{N}`

- Example: `auth_20250115:phase2`
- Reverts commits for phase N and all subsequent phases

**Specific task:** `{trackId}:task{X.Y}`

- Example: `auth_20250115:task2.3`
- Reverts commits for task X.Y only

### If no argument:

Display guided selection menu:

```
What would you like to revert?

Currently In Progress:
1. [~] Task 2.3 in dashboard_20250112 (most recent)

Recently Completed:
2. [x] Task 2.2 in dashboard_20250112 (1 hour ago)
3. [x] Phase 1 in dashboard_20250112 (3 hours ago)
4. [x] Full track: auth_20250115 (yesterday)

Options:
5. Enter specific reference (track:phase or track:task)
6. Cancel

Select option:
```

## Commit Discovery

### For Task Revert

1. Search git log for task-specific commits:

   ```bash
   git log --oneline --grep="{trackId}" --grep="Task {X.Y}" --all-match
   ```

2. Also find the plan.md update commit:

   ```bash
   git log --oneline --grep="mark task {X.Y} complete" --grep="{trackId}" --all-match
   ```

3. Collect all matching commit SHAs

### For Phase Revert

1. Determine task range for the phase by reading plan.md
2. Search for all task commits in that phase:

   ```bash
   git log --oneline --grep="{trackId}" | grep -E "Task {N}\.[0-9]"
   ```

3. Find phase verification commit if exists
4. Find all plan.md update commits for phase tasks
5. Collect all matching commit SHAs in chronological order

### For Full Track Revert

1. Find ALL commits mentioning the track:

   ```bash
   git log --oneline --grep="{trackId}"
   ```

2. Find track creation commits:

   ```bash
   git log --oneline -- "conductor/tracks/{trackId}/"
   ```

3. Collect all matching commit SHAs in chronological order

## Execution Plan Display

Before any revert operations, display full plan:

```
================================================================================
                           REVERT EXECUTION PLAN
================================================================================

Target: {description of what's being reverted}

Commits to revert (in reverse chronological order):
  1. abc1234 - feat: add chart rendering (dashboard_20250112)
  2. def5678 - chore: mark task 2.3 complete (dashboard_20250112)
  3. ghi9012 - feat: add data hooks (dashboard_20250112)
  4. jkl3456 - chore: mark task 2.2 complete (dashboard_20250112)

Files that will be affected:
  - src/components/Dashboard.tsx (modified)
  - src/hooks/useData.ts (will be deleted - was created in these commits)
  - conductor/tracks/dashboard_20250112/plan.md (modified)

Plan updates:
  - Task 2.2: [x] -> [ ]
  - Task 2.3: [~] -> [ ]

================================================================================
                              !! WARNING !!
================================================================================

This operation will:
- Create {N} revert commits
- Modify {M} files
- Reset {P} tasks to pending status

This CANNOT be easily undone without manual intervention.

================================================================================

Type 'YES' to proceed, or anything else to cancel:
```

**CRITICAL: Require explicit 'YES' confirmation. Do not proceed on 'y', 'yes', or enter.**

## Revert Execution

Execute reverts in reverse chronological order (newest first):

```
Executing revert plan...

[1/4] Reverting abc1234...
      git revert --no-edit abc1234
      ✓ Success

[2/4] Reverting def5678...
      git revert --no-edit def5678
      ✓ Success

[3/4] Reverting ghi9012...
      git revert --no-edit ghi9012
      ✓ Success

[4/4] Reverting jkl3456...
      git revert --no-edit jkl3456
      ✓ Success
```

### On Merge Conflict

If any revert produces a merge conflict:

```
================================================================================
                           MERGE CONFLICT DETECTED
================================================================================

Conflict occurred while reverting: {sha} - {message}

Conflicted files:
  - src/components/Dashboard.tsx

Options:
1. Show conflict details
2. Abort revert sequence (keeps completed reverts)
3. Open manual resolution guide

IMPORTANT: Reverts 1-{N} have been completed. You may need to manually
resolve this conflict before continuing or fully undo the revert sequence.

Select option:
```

**HALT immediately on any conflict. Do not attempt automatic resolution.**

## Plan.md Updates

After successful git reverts, update plan.md:

1. Read current plan.md
2. For each reverted task, change marker:
   - `[x]` -> `[ ]`
   - `[~]` -> `[ ]`
3. Write updated plan.md
4. Update metadata.json:
   - Decrement `tasks.completed`
   - Update `status` if needed
   - Update `updated` timestamp

**Do NOT commit plan.md changes** - they are part of the revert operation

## Track Status Updates

### If reverting entire track:

- In tracks.md: Change `[x]` or `[~]` to `[ ]`
- Consider offering to delete the track directory entirely

### If reverting to incomplete state:

- In tracks.md: Ensure marked as `[~]` if partially complete, `[ ]` if fully reverted

## Verification

After revert completion:

```
================================================================================
                           REVERT COMPLETE
================================================================================

Summary:
  - Reverted {N} commits
  - Reset {P} tasks to pending
  - {M} files affected

Git log now shows:
  {recent commit history}

Plan.md status:
  - Task 2.2: [ ] Pending
  - Task 2.3: [ ] Pending

================================================================================

Verify the revert was successful:
  1. Run tests: {test command}
  2. Check application: {relevant check}

If issues are found, you may need to:
  - Fix conflicts manually
  - Re-implement the reverted tasks
  - Use 'git revert HEAD~{N}..HEAD' to undo the reverts

================================================================================
```

## Safety Rules

1. **NEVER use `git reset --hard`** - Only use `git revert`
2. **NEVER use `git push --force`** - Only safe push operations
3. **NEVER auto-resolve conflicts** - Always halt for human intervention
4. **ALWAYS show full plan** - User must see exactly what will happen
5. **REQUIRE explicit 'YES'** - Not 'y', not enter, only 'YES'
6. **HALT on ANY error** - Do not attempt to continue past failures
7. **PRESERVE history** - Revert commits are preferred over history rewriting

## Edge Cases

### Track Never Committed

```
No commits found for track: {trackId}

The track exists but has no associated commits. This may mean:
- Implementation never started
- Commits used different format

Options:
1. Delete track directory only
2. Cancel
```

### Commits Already Reverted

```
Some commits appear to already be reverted:
  - abc1234 was reverted by xyz9876

Options:
1. Skip already-reverted commits
2. Cancel and investigate
```

### Remote Already Pushed

```
WARNING: Some commits have been pushed to remote

Commits on remote:
  - abc1234 (origin/main)
  - def5678 (origin/main)

Reverting will create new revert commits that you'll need to push.
This is the safe approach (no force push required).

Continue with revert? (YES/no):
```

## Undo the Revert

If user needs to undo the revert itself:

```
To undo this revert operation:

  git revert HEAD~{N}..HEAD

This will create new commits that restore the reverted changes.

Alternatively, if not yet pushed:
  git reset --soft HEAD~{N}
  git checkout -- .

(Use with caution - this discards the revert commits)
```

---

# Check if conductor directory exists
ls -la conductor/

# Find all track directories
ls -la conductor/tracks/

# Check for required files
ls conductor/index.md conductor/product.md conductor/tech-stack.md conductor/workflow.md conductor/tracks.md
```

## Pattern Matching

**Status markers in tracks.md:**

```
- [ ] Track Name  # Not started
- [~] Track Name  # In progress
- [x] Track Name  # Complete
```

**Task markers in plan.md:**

```
- [ ] Task description  # Pending
- [~] Task description  # In progress
- [x] Task description  # Complete
```

**Track ID pattern:**

```
<type>_<name>_<YYYYMMDD>
Example: feature_user_auth_20250115
```

---
