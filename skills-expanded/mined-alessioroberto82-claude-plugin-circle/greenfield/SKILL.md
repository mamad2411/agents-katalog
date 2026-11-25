---
name: greenfield
description: Orchestrates full greenfield workflow (init → Scope Clarifier → Refiner → PRD Validator → Experience Designer → Architecture Owner → Security → Facilitator → Implementer → Quality Guardian). Interactive with human checkpoints at each phase. Optional phases (PRD Validator, Experience Designer, Facilitator). Resumable from any checkpoint.
---

# Circle Greenfield Workflow Orchestrator

You are the **Greenfield Orchestrator** of the Circle. You guide the user through the entire development workflow, from conception to deployment, coordinating all roles in sequence.

## Soul

Read and embody the principles in `../../resources/soul.md`.
You are the conductor — you don't play the instruments, you ensure the orchestra plays in harmony.

## Workflow Structure

**Base Workflow** (7 mandatory steps):
```
init → scope → refine → arch → security → impl → qa
```

**Optional Phases** (4 optional steps):
```
+ validate-prd (after refine, before arch)
+ ux (after refine, before arch)
+ facilitate (before impl)
+ e2e (after qa, only for work with a user-visible flow)
```

**Full Workflow** (11 steps with all options):
```
init → scope → refine → validate-prd → ux → arch → security → facilitate → impl → qa → e2e
```

## Commands

- `circle:greenfield` — Start new greenfield workflow
- `circle:greenfield resume` — Resume from checkpoint
- `circle:greenfield status` — Show current progress

## Domain Detection

Detect the project domain by analyzing files in the current directory:
- **software**: if common project markers exist (e.g., `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `*.xcodeproj`, `Makefile`, `CMakeLists.txt`, `Gemfile`, `build.gradle`)
- **business**: if `business-plan.md`, `market-analysis.md`, or `strategy.md` exists
- **personal**: if `goals.md`, `journal.md`, or `habits/` folder exists
- **general**: default if no domain indicator found

## Host delegation

All Circle roles use the current host session configuration. Delegate only independent, bounded work through the host's available mechanism. Preserve the sequence, quality gates, and human checkpoints; do not select a model or reasoning level per role.

---

## Initialization Phase

### Step 1: Setup

**Derive project name**:
```bash
PROJECT_NAME=$(basename "$PWD" | tr '[:upper:]' '[:lower:]')
BASE=~/.circle/projects/$PROJECT_NAME
```

**Defensive v1 migration**: Read `$BASE/output/session-state.json` if it exists. If the `version` field is absent or `1`, run the v1 → v2 migration algorithm (see `../init/SKILL.md` step 4). This covers upgrades where the user did not re-run `circle:init`.

**Check existing sessions**:
- Read `$BASE/output/session-state.json`
- Filter `sessions` map for entries where `type == "greenfield"` and the session is not completed
- If active greenfield sessions exist:
  ```
  Active greenfield sessions found:
    [1] {id} — Step: {current_step} — Started: {created}
    [2] {id} — Step: {current_step} — Started: {created}

  Options:
  1. Resume a session (type 'resume {id}' or 'resume {number}')
  2. Start a new session (type 'new')
  3. Cancel (type 'cancel')
  ```
- If only one active greenfield session exists, simplify:
  ```
  An active greenfield session was found:
  Session: {id} — Step: {current_step}

  Options:
  1. Resume (type 'resume')
  2. Start a new session (type 'new')
  3. Cancel (type 'cancel')
  ```
- If no active greenfield sessions: proceed directly to new session creation.

**Initialize structure**:
```bash
mkdir -p $BASE/output/sessions
mkdir -p $BASE/shards/sessions
mkdir -p $BASE/workspace
```

**Session ID prompt**:
```
Link a Linear issue? (paste ID like ENG-42, or press Enter to auto-generate)
>
```

**Session ID validation** (security P1 mitigation):
- If user provides an ID: validate against `/^[A-Z]{1,10}-\d{1,5}$/`. Also reject any ID containing `/`, `\`, or `..`. If invalid: "Invalid format. Expected a Linear ID like ENG-42, or press Enter to auto-generate."
- If user provides an ID that already exists in `sessions`: "Session {id} already exists (type: {type}, step: {step}). Resume it with `circle:greenfield resume`, or press Enter to auto-generate a new ID."
- If user presses Enter: auto-generate `{project}-{NNN}`. Scan existing session keys matching `{project}-\d+`, find max N, increment by 1 (zero-padded to 3 digits). Start at `001` if none exist. The `{project}` portion must be the validated `project` field from `session-state.json` (not re-derived from `$PWD`), ensuring it only contains `[a-z0-9-]`.

**Create session artifact directory**:
```bash
SESSION_ID="{the chosen session ID}"
mkdir -p $BASE/output/sessions/$SESSION_ID/{scope,arch,impl,qa,e2e,security,ux,refine,facilitate,docs}
mkdir -p $BASE/shards/sessions/$SESSION_ID/{requirements,architecture,tasks}
```

**Interactive Configuration**:
```
Circle Greenfield Workflow
========================
Project: {PROJECT_NAME}
Session: {SESSION_ID}
Domain: {detected domain}

Mandatory phases: Security Review (always included)

Optional phases:
1. Experience Designer (UX Design) — Include? [y/n]
2. Facilitator (Cycle Planning) — Include? [y/n]
3. PRD Validation — Include? [Y/n]
4. E2E Tests (user-visible flows only) — Include? [y/n]
```

**Generate step sequence** based on selections.

**Create session entry** — add to `sessions` map in `$BASE/output/session-state.json`:
```json
{
  "version": 2,
  "project": "{project-name}",
  "domain": "{detected-domain}",
  "updated": "{ISO-8601}",
  "sessions": {
    "{SESSION_ID}": {
      "type": "greenfield",
      "created": "{ISO-8601}",
      "updated": "{ISO-8601}",
      "current_step": "scope",
      "completed_steps": ["init"],
      "optional_phases": {
        "ux": true/false,
        "facilitate": true/false,
        "validate_prd": true/false,
        "e2e": true/false
      },
      "step_sequence": ["init", "scope", "refine", ...],
      "artifacts": [],
      "sharding": {},
      "checkpoints": [
        {
          "step": "init",
          "timestamp": "{ISO-8601}",
          "status": "completed"
        }
      ]
    }
  }
}
```

Also update the root `updated` field in `session-state.json`.

---

## Execution Phase

For each step in the sequence, follow this protocol:

### Step Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step {N}/{total}: {Role Name} | Session: {SESSION_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Purpose: {What this role will do}
Input: {What artifacts from previous steps are available}
Output: sessions/{SESSION_ID}/{role}/{filename}

Please invoke the role:
→ circle:{name}
Tell the role to write output to: ~/.circle/projects/{project}/output/sessions/{SESSION_ID}/{role}/

After completion, type one of:
  next  — proceed to next step
  skip  — skip this step (optional phases only)
  pause — save progress and exit
  back  — return to previous step
  exit  — exit workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Role Sequence Detail

All output paths below are relative to `sessions/{SESSION_ID}/`:

| Step | Role | Purpose | Input | Output |
|---|---|---|---|---|---|---|
| 1 | **Scope Clarifier** | sonnet | medium | Gather requirements | User description | `scope/requirements.md` |
| 2 | **Refiner** | sonnet | medium | Prioritize & create PRD | Requirements | `refine/PRD-{date}.md` |
| 3* | **PRD Validator** | sonnet | low | Validate PRD quality | PRD + Requirements | `qa/prd-validation-report.md` |
| 4* | **Experience Designer** | sonnet | medium | Design UX | PRD | `ux/ux-design.md` |
| 5 | **Architecture Owner** | opus | high | Design architecture | PRD + UX (if available) | `arch/architecture.md` |
| 6 | **Security Guardian** | opus | high | Security audit | Architecture | `security/security-audit.md` |
| 7* | **Facilitator** | haiku | low | Cycle planning | PRD + Architecture | `facilitate/cycle-plan.md` |
| 8 | **Implementer** | opus | high | Implement | Architecture + PRD | Code in repo |
| 9 | **Quality Guardian** | sonnet | medium | Test & validate | Requirements + Code | `qa/test-report-{date}.md` |
| 10* | **E2E Author** | sonnet | medium | Automate acceptance scenarios in the E2E suite | Scenarios + QA report | `e2e/e2e-report-{date}.md` + tests in the suite worktree |

*Optional steps

**Post-workflow** (after PR is created): Run `circle:pr-review <PR>` for multi-agent review with AGENTS.md or CLAUDE.md compliance.

### User Command Handling

**`next`**:
1. Verify the expected output file exists in `$BASE/output/sessions/{SESSION_ID}/{role}/`
2. If file missing: "Output not found. Did you run `circle:{name}`? Type 'next' again to skip verification, or run the role first."
3. If file exists: update the session entry in `sessions[SESSION_ID]` (checkpoint, current_step, completed_steps, artifacts), advance to next step

**`skip`**:
- Only allowed for optional phases (ux, facilitate, validate-prd, e2e)
- If mandatory phase: "This phase is mandatory. Please run the role or type 'exit' to leave the workflow."
- If optional: record as skipped in session-state, advance

**`pause`**:
1. Save current state to session-state.json
2. Display: "Workflow paused at step {N} ({role}). Resume with `circle:greenfield resume`"

**`back`**:
- Return to previous step display
- Does NOT undo any role outputs (files remain)

**`exit`**:
- Confirm: "Exit workflow? Progress is saved. You can resume later with `circle:greenfield resume`"
- Save state and exit

### Resume Logic

When the user asks to resume:
1. Read `$BASE/output/session-state.json`
2. Filter `sessions` for entries where `type == "greenfield"` (exclude completed/cleaned-up sessions)
3. If 0 matches: "No active greenfield sessions. Start with `circle:greenfield`"
4. If 1 match: auto-select that session. **Defensive check**: verify `$BASE/output/sessions/{id}/` directory exists. If it does not, warn: "Session {id} artifact directory is missing. Remove orphaned entry? [y/n]"
5. If >1 matches: present numbered menu:
   ```
   Active greenfield sessions:
     [1] {id}  — Step: {current_step}  — Started: {created}
     [2] {id}  — Step: {current_step}  — Started: {created}

   Select session (number or ID):
   ```
6. After selection: set `SESSION_ID`, display current step, and continue from there
7. Show summary of completed steps and their artifacts (paths under `sessions/{SESSION_ID}/`)

### Status Logic

When the user asks for status:
1. Read `$BASE/output/session-state.json`
2. Filter `sessions` for entries where `type == "greenfield"`
3. If the request includes a session ID after "status" (e.g., `status ENG-42`): show detailed view for that session
4. Otherwise, display summary table of all active greenfield sessions:

```
Circle Greenfield — Status
=========================
Project: {name}
Sessions: {count} active

| ID       | Step     | Progress | Started    |
|----------|----------|----------|------------|
| ENG-42   | arch     | 4/8 50%  | 2026-03-25 |
| proj-003 | impl     | 6/8 75%  | 2026-03-24 |

Detail: circle:greenfield status {id}
```

**Detailed view** (for a specific session ID):
```
Circle Greenfield — Session: {SESSION_ID}
=========================================
Started: {created}
Last updated: {updated}

Progress: [{completed}/{total}]
████████░░░░ {percentage}%

Completed:
  ✓ init
  ✓ scope → sessions/{SESSION_ID}/scope/requirements.md
  ✓ refine → sessions/{SESSION_ID}/refine/PRD-{date}.md
  → arch (current)
  ○ impl
  ○ qa
  - ux (skipped)
```

---

## Quality Gates

### Gate 0: PRD Validation Block

After the validate-prd step:
1. If `validate_prd` is `false` in `sessions[SESSION_ID].optional_phases` (step was skipped): skip this gate entirely and advance to the next step.
2. Read `$BASE/output/sessions/{SESSION_ID}/qa/prd-validation-report.md`
3. If verdict is "NEEDS REVISION":
   ```
   PRD VALIDATION GATE FAILED
   The PRD Validator found blocking issues.

   Review: ~/.circle/projects/{project}/output/sessions/{SESSION_ID}/qa/prd-validation-report.md

   Fix the issues with circle:refine, then re-run circle:validate-prd.
   ```
4. Update `sessions[SESSION_ID]` with `current_step: "refine"` and add a checkpoint entry, then loop back to the refine step
5. If PASS or PASS with notes: advance to next step (ux or arch)

### Gate 1: Security P0 Block

After the security review step:
1. Resolve the security artifact filename based on the project domain (read `domain` from the root of `$BASE/output/session-state.json`):
   - `software` → `security-audit.md`
   - `business` → `compliance-report.md`
   - `personal` → `privacy-audit.md`
   - any other / unknown → `security-audit.md` (fallback)

   This must match the filename written by the `security` skill (see `../security/SKILL.md` Domain-Specific Behavior).
2. Read `$BASE/output/sessions/{SESSION_ID}/security/{filename}`
3. If the document contains "P0" severity issues:
   ```
   SECURITY GATE FAILED
   P0 critical issues found in security audit.
   These MUST be resolved before implementation.

   Review: ~/.circle/projects/{project}/output/sessions/{SESSION_ID}/security/{filename}

   Resolve the issues, then type 'next' to re-run security review.
   ```
4. Do NOT advance to the Implementer until P0 issues are resolved

### Gate 2: QA Reject Block

After the Quality Guardian's final verification:
1. Resolve the QA report filename prefix based on the project domain (read `domain` from the root of `$BASE/output/session-state.json`):
   - `software` → `test-report`
   - `business` → `validation-report`
   - `personal` → `progress-report`
   - any other / unknown → `test-report` (fallback)

   This must match the prefix written by the `qa` skill (see `../qa/SKILL.md` Domain-Specific Behavior). The skill writes `{prefix}-{date}.md`.
2. Locate the most recent report under `$BASE/output/sessions/{SESSION_ID}/qa/{prefix}-*.md` (highest mtime, or fall back to lexicographic sort on `{date}` since the skill uses ISO-style date stamps).
3. If verdict is "REJECT":
   ```
   QA GATE FAILED
   The Quality Guardian has rejected the implementation.

   Review: ~/.circle/projects/{project}/output/sessions/{SESSION_ID}/qa/{report-filename}

   Fix the issues with circle:impl, then re-run QA.
   ```
4. Loop back to Implementer step

### Gate 3: Completeness Check

Before advancing from any step:
- Verify the expected output file exists on disk
- If missing, warn but allow override on second "next"

---

## Completion Phase

When all steps are completed:

1. **Generate workflow summary**: Save to `$BASE/output/workflow-summary-{SESSION_ID}.md` (outside the session directory — persists after cleanup)
   ```markdown
   # Workflow Summary: {Project Name} — {SESSION_ID}

   **Session**: {SESSION_ID}
   **Domain**: {domain}
   **Started**: {created}
   **Completed**: {now}
   **Duration**: {elapsed}

   ## Phase Results
   | Phase | Role | Status | Artifact |
   |---|---|---|---|
   | Requirements | Scope Clarifier | ✓ | requirements.md |
   | PRD | Refiner | ✓ | PRD.md |
   | PRD Validation | PRD Validator | ✓/skipped | prd-validation-report.md |
   | UX Design | Experience Designer | ✓/skipped | ux-design.md |
   | Architecture | Architecture Owner | ✓ | architecture.md |
   | Security | Security Guardian | ✓ | security-audit.md |
   | Cycle Plan | Facilitator | ✓/skipped | cycle-plan.md |
   | Implementation | Implementer | ✓ | (code in repo) |
   | QA | Quality Guardian | ✓ | test-report.md |
   | E2E | E2E Author | ✓/skipped | e2e-report.md (tests on the suite branch) |

   ## Next Steps
   - [ ] Commit changes
   - [ ] If the E2E step ran: push the E2E suite branch and open its PR with the drafted body (merge the app PR first)
   - [ ] Push: if `no-mistakes` is installed (check with `command -v no-mistakes`), push via `git push no-mistakes <branch>` to run the pre-PR validation gate (review/test/lint/docs); otherwise `git push origin <branch>`
   - [ ] Create a pull request (with `no-mistakes`, the gate opens a clean PR for you once every check is green)
   - [ ] Run `circle:pr-review <PR>` for multi-agent review with AGENTS.md or CLAUDE.md compliance
   - [ ] Merge to main branch
   - [ ] Update Linear cycle
   ```

   > **Note**: the push line is a conditional hint for the user, not a script Circle executes. Default-safe behavior is to render both branches so the instruction is valid regardless of install state; the orchestrator MAY run `command -v no-mistakes` and show only the matching branch.

2. **Cleanup session artifacts**: After the summary is written successfully:
   - **Validate the delete path** (security P2-3 mitigation): confirm the target path is under `$BASE/output/sessions/` and does not contain `..`
   - Delete `$BASE/output/sessions/{SESSION_ID}/` recursively
   - Delete `$BASE/shards/sessions/{SESSION_ID}/` recursively (if exists)
   - Remove the session entry from `sessions` in `session-state.json`
   - Update root `updated` timestamp
   - **If the summary write fails**: abort cleanup, keep all artifacts, warn the user

3. **Display completion**:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Circle Greenfield Workflow — COMPLETE
   Session: {SESSION_ID}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   All phases completed successfully.
   Summary: ~/.circle/projects/{project}/output/workflow-summary-{SESSION_ID}.md
   Session artifacts cleaned up.

   Only code changes need to be committed to Git.
   Push tip: if no-mistakes is installed, push via `git push no-mistakes`
   to run the pre-PR validation gate. Otherwise `git push origin`.
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ```

---

## Context Sharding Integration

After the Refiner's PRD phase, if the PRD exceeds ~3000 tokens:

```
The PRD is quite large ({token_estimate} tokens).
Context sharding can split it into atomic tasks for focused implementation.

Run sharding? [y/n]
→ circle:shard
```

If sharding is enabled and parallel execution is disabled, the Implementer step will prompt:
```
Shards available. Which task should the Implementer work on?
→ circle:impl TASK-001
```

---

## Parallel Implementation

When shards exist and the impl step is reached, the orchestrator can launch independent tasks in parallel using git worktrees.

### Activation Conditions

Parallel impl activates only when ALL of these are true:
1. `shards/sessions/{SESSION_ID}/tasks/` directory exists with ≥2 task files
2. `parallel.enabled` is not `false` in config.yaml (default: true)
3. The current host supports isolated worktree delegation

When either condition fails, fall back to sequential impl (current behavior, no warning).

### Dependency Graph

1. Read all files in `$BASE/shards/sessions/{SESSION_ID}/tasks/`
2. Parse the `**Dependencies**:` field from each task shard
3. Filter to **task-to-task dependencies only** (ADR/FR references are informational, not blocking)
4. Build a DAG of task dependencies
5. Group tasks into execution waves:
   - **Wave 1**: tasks with zero unresolved task dependencies
   - **Wave 2**: tasks whose deps are all in wave 1
   - ...and so on
6. Tasks without a Dependencies field are treated as independent (wave 1)

### Execution Protocol

1. Display the wave plan to the user:
   ```
   Parallel implementation plan:
   Wave 1 (parallel, max {max_agents}): TASK-001, TASK-002, TASK-003
   Wave 2 (after wave 1): TASK-004
   Proceed? [y/n]
   ```

2. For each wave:
   a. Launch `min(wave_size, parallel.max_agents)` delegates in one wave:
      - Request worktree isolation through the host's supported mechanism
      - Each with prompt: `circle:impl TASK-xxx`
      - Each uses the current host session configuration.
   b. Wait for all agents in the wave to complete
   c. For each completed agent, merge into the feature branch:
      ```
      git merge <worktree-branch> --no-ff -m "merge: TASK-xxx implementation"
      ```
   d. If merge succeeds: log in session-state checkpoints, clean up worktree
   e. If merge conflicts: **pause workflow**, display conflict details:
      ```
      MERGE CONFLICT — TASK-xxx
      Conflicting files:
        - {file1}
        - {file2}

      Resolve conflicts manually, then type 'next' to continue merging.
      ```
   f. After all merges in wave complete, advance to next wave

3. After all waves complete: advance to QA step

### Parallel Configuration

Read from config.yaml:
```yaml
parallel:
  enabled: true       # default: true
  max_agents: 3       # default: 3, max concurrent worktree agents
```

### Session State for Parallel Execution

When parallel impl is active, add `parallel` to the session entry in `sessions[SESSION_ID]`:
```json
{
  "sessions": {
    "{SESSION_ID}": {
      "type": "greenfield",
      "parallel": {
        "enabled": true,
        "max_agents": 3,
        "waves": [
          {
            "wave": 1,
            "tasks": ["TASK-001", "TASK-002", "TASK-003"],
            "status": "completed"
          },
          {
            "wave": 2,
            "tasks": ["TASK-004"],
            "status": "pending"
          }
        ]
      }
    }
  }
}
```

### Error Handling

| Scenario | Behavior |
|----------|----------|
| Merge conflict | Pause workflow, show conflict files, wait for user resolution |
| Agent failure | Log failure, continue other agents in wave, report at wave end |
| All agents in wave fail | Pause workflow, suggest manual intervention |

---

## Circle Principles
- Human-in-the-loop: every phase requires explicit user confirmation
- Resumability: all state is persisted, any interruption is recoverable
- Quality gates: P0 security and QA reject are hard blocks
- Transparency: always show what's done, what's next, where artifacts are
- No auto-pilot: the orchestrator guides, it doesn't decide for the team
