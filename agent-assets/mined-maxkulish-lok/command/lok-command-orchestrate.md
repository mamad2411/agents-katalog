# /task:orchestrate - Complete Task Lifecycle Management

**Purpose**: Orchestrate the complete lifecycle of a Linear task from design through PR merge. Manages workflow state, coordinates phase transitions, and ensures checkpoints for human validation.

**Usage**:
- `/task:orchestrate CLO-XX` - Start or resume a task workflow
- `/task:orchestrate CLO-XX --status` - Show current workflow state only
- `/task:orchestrate CLO-XX --ops` - Start as operational task (skip design/plan)
- `/task:orchestrate CLO-XX --spec` - Start as specification task (use /spec instead of full design doc)
- `/task:orchestrate CLO-XX --skip-discovery` - Skip discovery phase (go straight to design)
- `/task:orchestrate` - Interactive mode

---

## State Machine

```
ENTRY -> DISCOVERY -> DESIGN -> PLAN -> IMPLEMENT -> PR -> COMPLETE  (development)
ENTRY -> SPEC -> IMPLEMENT -> PR -> COMPLETE                         (specification)
ENTRY -> EXECUTE -> DOCUMENT -> PR (conditional) -> COMPLETE         (operational)
                          |
                       BLOCKED (any phase)
```

**State file**: `docs/status/clo-XX-workflow.yaml`
**Phase instructions**: `.claude/commands/task/phases/{phase}.md`

---

## Dispatch Logic

1. **Parse arguments**: Read `phases/init.md` for initialization/resume logic
2. **Read workflow YAML** to determine `current_phase` and `status`
3. **Load the phase file** for the current phase and follow its instructions:

| Phase | File | Entry Condition |
|-------|------|-----------------|
| Initialize | `phases/init.md` | No workflow YAML exists |
| Discovery | `phases/discovery.md` | `current_phase: discovery` (development tasks) |
| Spec | `phases/spec.md` | `current_phase: spec` (specification tasks) |
| Design | `phases/design.md` | `current_phase: design` |
| Plan | `phases/plan.md` | `current_phase: plan` |
| Implement | `phases/implement.md` | `current_phase: implement` |
| PR | `phases/pr.md` | `current_phase: pr` |
| Complete | `phases/complete.md` | `current_phase: complete` |
| Blocked | `phases/blocked.md` | `status: blocked` (any phase) |
| Status | `phases/status.md` | `--status` flag |
| Operational | `phases/operational.md` | `task_type: operational` |

4. **After each phase completes**: the phase file MUST complete its YAML Checkpoint (see bottom of each phase file), THEN update `workflow.current_phase`. The orchestrator MUST validate the checkpoint before loading the next phase (Step 3.5).

---

## Phase Transition Validation (Step 3.5)

**CRITICAL**: Before loading the next phase file, validate the outgoing phase.

After a phase file signals completion by updating `workflow.current_phase`, re-read the YAML and verify the following minimum fields exist and are non-null:

### Required Fields per Phase

| Outgoing Phase | Required Fields (must be non-null/non-empty) |
|---|---|
| discovery | `discovery.status=complete` OR `discovery.status=skipped`, `discovery.approved=true` |
| spec | `spec.status=complete`, `spec.spec_file`, `spec.approved=true`, `spec.review_completed` |
| design | `design.status=complete`, `design.design_doc`, `design.draft_ready=true`, `design.finalized=true`, `design.review_completed` |
| plan | `plan.status=complete`, `plan.plan_file`, `plan.approved=true` |
| implement | `implement.status=complete` |
| pr | `pr.status=complete`, `pr.pr_url`, `pr.pr_number` |

### If Validation Fails

1. **DO NOT** load the next phase file
2. Display: `TRANSITION BLOCKED: Phase [X] is missing required fields: [list]`
3. Fill the missing fields from available context:
   - History entries (timestamps, details)
   - File system (glob for design docs, plans, reviews)
   - Git log (commit SHAs)
   - GitHub CLI (`gh pr list/view` for PR data)
4. Re-validate - only proceed when all required fields are present

---

## State Persistence

**CRITICAL**: Update workflow state file after EVERY action.

```yaml
history:
  - timestamp: [ISO timestamp]
    action: [action name]
    phase: [current phase]
    details: [what happened]
```

### History Action Types

| Action | Description |
|--------|-------------|
| `workflow_started` | Initial workflow creation |
| `project_sync_start` | Task added to Active Work via `/project:sync --start` |
| `problem_framed` | Problem statement validated by user |
| `discovery_report_complete` | PRD discovery report produced |
| `discovery_pivot` | User changed direction based on discovery findings |
| `discovery_approved` | Discovery phase approved, proceeding to design |
| `task_skipped_after_discovery` | Discovery showed task should not be built |
| `design_started` | Design doc creation began |
| `design_draft_ready` | Design doc draft completed |
| `design_review_started` | AI review of design document began |
| `design_review_complete` | AI review completed with verdict |
| `design_review_timeout` | AI review timed out |
| `design_review_failed` | AI review encountered an error |
| `design_finalized` | Design doc approved and finalized |
| `spec_review_complete` | AI review of specification completed with verdict |
| `spec_review_failed` | AI review of specification failed or timed out |
| `spec_review_applied` | AI review feedback applied to specification |
| `spec_approved` | Specification approved for implementation |
| `plan_created` | Implementation plan generated |
| `plan_approved` | Plan approved for implementation |
| `phase_completed` | Implementation phase finished |
| `implementation_complete` | All plan tasks done |
| `commit_created` | Git commit made |
| `pushed_to_remote` | Branch pushed to origin |
| `pr_created` | Pull request created |
| `review_addressed` | PR review feedback addressed |
| `pr_approved` | PR approved for merge |
| `pr_merged` | PR merged to main |
| `project_sync_complete` | Task moved to Recently Completed via `/project:sync --complete` |
| `workflow_complete` | Full workflow finished |
| `workflow_paused` | User paused workflow |
| `workflow_resumed` | Workflow resumed from pause |
| `workflow_blocked` | Task blocked by another task |
| `workflow_unblocked` | Blocker resolved, task unblocked |

---

## Integration with Existing Skills

### Development Task Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `/project:sync --start` | Entry | Validate WIP limit, add to Active Work |
| `/prd create` | Discovery | Draft lightweight PRD if none exists |
| `/prd-discovery` | Discovery | Multi-model PRD review, prior-art research, assumption mapping |
| `/design-doc:create` | Design | Interactive design creation (receives discovery report) |
| `/design-doc:review` | Design | AI review (Ollama + Claude fallback) |
| `/design-doc:finalize` | Design | Mark design as approved |
| `/plan:create` | Plan | Generate implementation plan |
| `/plan:implement` | Implement | Execute plan phases |
| `/pr:create` | PR | Create pull request |
| `/pr:review` | PR | Handle review feedback |
| `/pr:finalize` | Complete | Post-merge cleanup |
| `/project:sync --complete` | Complete | Move to Recently Completed, unblock dependents |
| `/project:sync --block` | Any (on block) | Update blockers in aggregation files |
| `/project:sync --unblock` | Any (on recovery) | Remove from blockers, mark ready |

### Specification Task Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `/project:sync --start` | Entry | Validate WIP limit, add to Active Work |
| `/spec` | Spec | Write 5-section autonomous specification |
| Ollama review + synthesis | Spec | AI review of specification (same pattern as design review) |
| `/plan:implement` | Implement | Execute spec decomposition |
| `/pr:create` | PR | Create pull request |
| `/pr:review` | PR | Handle review feedback |
| `/pr:finalize` | Complete | Post-merge cleanup |
| `/project:sync --complete` | Complete | Move to Recently Completed |

### Operational Task Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `/project:sync --start` | Entry | Validate WIP limit, add to Active Work |
| *(manual execution)* | Execute | Interactive procedure execution |
| *(status file updates)* | Document | Capture findings and lessons |
| `/pr:create` | PR (conditional) | Only if code changes |
| `/pr:finalize` | Complete | Post-merge cleanup (if PR created) |
| `/project:sync --complete` | Complete | Move to Recently Completed |

---

## Philosophy

**This orchestrator is designed to**:

1. **Provide single entry point**: One command for entire task lifecycle
2. **Enable resume capability**: Pick up where you left off
3. **Ensure human checkpoints**: Validate at critical decision points
4. **Maintain visibility**: Clear status at all times
5. **Coordinate skills**: Chain existing skills intelligently
6. **Track history**: Full audit trail of actions

**This orchestrator does NOT**:

1. **Make architectural decisions**: Uses design docs and plans
2. **Skip validation**: Requires human approval at checkpoints
3. **Force completion**: User can pause anytime
4. **Hide state**: Everything persisted in YAML file
