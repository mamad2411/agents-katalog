# Phase: Plan

**Purpose**: Generate an implementation plan from the design document and get user approval.

**Entry conditions**: `current_phase: plan`

---

## Status: pending or in_progress

1. **Check if plan exists**: `docs/plans/clo-XX-*.md`

2. **If plan does NOT exist**:
   - Display: "Creating implementation plan from design document."
   - Update state: `phases.plan.status: in_progress`
   - **Invoke**: `/plan:create CLO-XX`
   - After completion, update state:
     - `phases.plan.plan_file: [path]`
     - `phases.plan.status: checkpoint`
     - `workflow.status: checkpoint`
   - Add history entry: `plan_created`

3. **If plan exists**:
   - Display: "Implementation plan already exists."
   - Update state: `phases.plan.status: checkpoint`

---

## Status: checkpoint

1. Display plan file location and summary
2. Ask user:
   ```
   PLAN CHECKPOINT

   Implementation plan: docs/plans/clo-XX-[description].md
   Total tasks: [X]
   Phases: [Y]

   Please review the implementation plan.

   Options:
   1. [approve] - Plan is approved, start implementation
   2. [regenerate] - Regenerate plan with different approach
   3. [pause] - Pause workflow, continue later

   Your choice:
   ```

3. **If approve**:
   - Update state:
     - `phases.plan.approved: true`
     - `phases.plan.status: complete`
     - `workflow.current_phase: implement`
     - `workflow.status: in_progress`
   - Add history entry: `plan_approved`
   - **Continue to IMPLEMENT phase**

4. **If regenerate**:
   - Ask for guidance on different approach
   - Delete existing plan file
   - Re-invoke `/plan:create CLO-XX` with updated guidance
   - Return to checkpoint

5. **If pause**:
   - Save state
   - Exit with resume instructions

---

## YAML Checkpoint (Required before transition)

Before signaling completion to the dispatcher, verify:
- `phases.plan.plan_file` is set (non-null)
- `phases.plan.approved: true`
- `phases.plan.status: complete`
- History contains `plan_created` and `plan_approved`
