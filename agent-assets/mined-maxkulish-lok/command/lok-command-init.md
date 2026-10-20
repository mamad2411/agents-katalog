# Phase: Initialize / Resume Workflow

**Purpose**: Parse arguments, initialize new workflows or resume existing ones, classify task type, and sync project aggregation files.

**Called by**: `/task:orchestrate` dispatcher

---

## Step 1: Parse Arguments

1. **Extract task number** from arguments (e.g., `CLO-9` or `clo-9`)
2. **Check for flags**:
   - `--status`: Display current state and exit (load `phases/status.md`)
   - `--ops`: Force operational task type (skip design/plan phases)
   - `--spec`: Force specification task type (use /spec instead of full design doc)
   - `--skip-discovery`: Skip discovery phase for development tasks (go straight to design)
3. **If no task provided**: Ask user interactively

---

## Step 2: Initialize or Resume Workflow

### Check for Existing Workflow State

```bash
# Look for workflow state file
ls docs/status/clo-XX-workflow.yaml 2>/dev/null
```

**If workflow state exists**:
1. Read `docs/status/clo-XX-workflow.yaml`
2. Display current state summary
3. Ask: "Resume from [current phase]? (yes/restart/cancel)"
   - **yes**: Continue from current phase
   - **restart**: Reset workflow to beginning
   - **cancel**: Exit

**If workflow state does NOT exist**:
1. Create new workflow state file
2. Fetch Linear task details using `mcp__linear-server__get_issue`
3. **Classify task type**: Proceed to Step 2.3
4. Initialize phases based on task type
5. Set initial phase and status
6. **Sync project files**: Proceed to Step 2.5

---

## Step 2.3: Classify Task Type (New Workflow Only)

1. **If `--ops` flag provided**: Set `task_type: operational`
2. **If `--spec` flag provided**: Set `task_type: specification`

3. **Otherwise, analyze task**:
   - Check Linear labels for: `ops`, `maintenance`, `admin`, `devops`
   - Check title for keywords: "restore", "backup", "migrate", "configure", "setup", "fix", "investigate", "cleanup"
   - Check description length and complexity (short + clear scope -> specification)
   - Check description for procedural content (step-by-step instructions -> operational)

4. **Auto-classify if clear indicators**:
   - 2+ ops keywords -> likely operational
   - Short, well-scoped description with no architecture decisions needed -> likely specification
   - Complex feature requiring architecture decisions -> development

5. **Ask user if ambiguous**:
   ```
   TASK TYPE CLASSIFICATION

   Task: CLO-XX - [title]
   Labels: [labels]
   Indicators found: [list]

   Which workflow should we use?

   1. [development] - Full workflow (design doc Q&A -> plan -> implement -> PR)
      Use for: New features with architecture decisions, complex cross-module changes (L scope)

   2. [specification] - Lean workflow (write spec -> implement -> PR)
      Use for: Well-scoped features, clear requirements, single-module changes (S/M scope)

   3. [operational] - Streamlined workflow (execute -> document -> PR if needed)
      Use for: Troubleshooting, configuration, admin tasks, investigations

   Your choice:
   ```

6. **Initialize based on classification**:

   **For Development tasks**:
   ```yaml
   task_type: development
   workflow:
     current_phase: discovery    # or "design" if --skip-discovery
     status: awaiting_input
   phases:
     discovery: { status: pending }   # or { status: skipped, skip_reason: "--skip-discovery flag" }
     design: { status: pending }
     plan: { status: pending }
     implement: { status: pending }
     pr: { status: pending }
     complete: { status: pending }
   ```

   If `--skip-discovery` flag is set:
   - Set `workflow.current_phase: design`
   - Set `phases.discovery.status: skipped`
   - Set `phases.discovery.skip_reason: "--skip-discovery flag"`
   - Set `phases.discovery.approved: true`

   **For Specification tasks**:
   ```yaml
   task_type: specification
   workflow:
     current_phase: spec
     status: awaiting_input
   phases:
     discovery: { status: skipped, skip_reason: "Specification task", approved: true }
     design: { status: skipped, reason: "Specification task - using /spec instead" }
     spec: { status: pending, spec_file: null, approved: false }
     implement: { status: pending }
     pr: { status: pending }
     complete: { status: pending }
   ```

   **For Operational tasks**:
   ```yaml
   task_type: operational
   workflow:
     current_phase: execute
     status: in_progress
   phases:
     discovery: { status: skipped, skip_reason: "Operational task", approved: true }
     design: { status: skipped, reason: "Operational task" }
     plan: { status: skipped, reason: "Operational task" }
     execute: { status: pending }
     document: { status: pending }
     pr: { status: pending, required: false }
     complete: { status: pending }
   ```

---

## Step 2.5: Sync Project Aggregation Files (New Workflow Only)

**IMPORTANT**: This step only runs when starting a NEW workflow (not resuming).

1. **Invoke**: `/project:sync CLO-XX --start`

2. **This validates**:
   - WIP limit (max 3 active tasks in PROJECT.md)
   - Task is not blocked (check DEPENDENCIES.md)

3. **If validation fails**:
   - `/project:sync` will display the issue and options
   - User must resolve before proceeding
   - Workflow enters `blocked` state until resolved

4. **If validation passes**:
   - PROJECT.md: Task added to "Active Work"
   - ROADMAP.md: Task status changed to "In Progress"
   - DEPENDENCIES.md: Task removed from "Unblocked & Ready"
   - Add history entry: `project_sync_start`

---

## Return to Dispatcher

After initialization/resume completes, return control to the dispatcher with `current_phase` set. The dispatcher will load the appropriate phase file.
