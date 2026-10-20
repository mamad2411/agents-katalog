# Phase: Discovery

**Purpose**: Frame the problem, explore the solution space, and validate assumptions before committing to a design. Answers three questions: What are we trying to achieve? What different ways can we achieve this? What is the best way?

**Entry conditions**: `current_phase: discovery`

**Skip conditions**: This phase is automatically skipped for:
- Specification tasks (`--spec`) - spec workflow has its own scoping
- Operational tasks (`--ops`) - no design needed
- User explicitly passes `--skip-discovery`

---

## Status: pending or awaiting_input

1. **Update state**: `phases.discovery.status: in_progress`

2. **Fetch Linear task context**:
   - Read task details via `mcp__linear-server__get_issue` (if not already cached in YAML)
   - Extract: title, description, labels, subtasks, comments, attachments
   - Check labels for `bug` or `hotfix` - if found, offer to skip:
     ```
     DISCOVERY SKIP CHECK

     This task is labeled as a bug/hotfix. Discovery is typically
     skipped for targeted fixes with clear scope.

     Skip discovery and go straight to design? (yes/no)
     ```
     - If **yes**: Set `phases.discovery.status: skipped`, `phases.discovery.skip_reason: "bug/hotfix"`, advance to `design`
     - If **no**: Continue with discovery

3. **Check for existing PRD or requirements document**:
   ```bash
   ls docs/prds/clo-XX-*.md docs/design-docs/clo-XX-*.md 2>/dev/null
   ```
   - If a PRD exists: Set `phases.discovery.prd_exists: true`, `phases.discovery.prd_file: <path>`
   - If no PRD exists: Proceed to Step 4

---

## Step 4: Problem Framing - "What are we trying to achieve?"

This step ensures we understand the problem before exploring solutions.

**4a. Build Problem Statement**

Synthesize from Linear task details a structured problem statement:

```
PROBLEM FRAMING (CLO-XX)
========================

Problem Statement:
  [1-2 sentence summary of what problem this task solves]

Who is affected:
  [User persona or system component]

Current state:
  [How things work today / what's broken / what's missing]

Desired state:
  [What success looks like]

Constraints already known:
  [From Linear description, labels, or project context]
  - Architecture: [e.g., "Rust owns all state", "in-process everything"]
  - Technical: [e.g., "must work on macOS only", "local-first"]
  - Scope: [e.g., "single module change", "cross-cutting"]

Does this accurately capture the problem? (yes / refine)
```

- If **refine**: Ask user for corrections, rebuild statement
- If **yes**: Continue to Step 5

Update state: `phases.discovery.problem_framed: true`
Add history entry: `problem_framed`

---

## Step 5: Solution Space Exploration - "What different ways can we achieve this?"

**5a. Draft a lightweight PRD (if none exists)**

If `phases.discovery.prd_exists: false`:
- Invoke `/prd create` with the problem statement as input
- This produces a draft PRD with: problem, goals, requirements, success metrics
- Set `phases.discovery.prd_file: <path>`
- Set `phases.discovery.prd_created: true`

If a PRD already exists, use it as-is.

**5b. Run PRD Discovery**

Invoke the `prd-discovery` skill with the PRD file:

```
/prd-discovery <prd_file_path>
```

This runs 6 phases internally:
1. **Baseline scoring** - review checklist assessment
2. **Prior-art research** - 3 parallel agents search academic papers, existing solutions, and standards
3. **Multi-persona criticism** - 4 personas (Skeptical Engineer, User Advocate, Business Strategist, Adversarial Reviewer) stress-test the PRD
4. **Assumption mapping** - identify and score all assumptions on importance x certainty
5. **Reverse stress test** - "what would make this fail even if built as specified?"
6. **Synthesis** - compiled discovery report with verdict

Wait for the discovery report to be produced.

Update state:
- `phases.discovery.discovery_report: <path>`
- `phases.discovery.discovery_debt: <killer_assumption_count>`
- `phases.discovery.baseline_score: <percentage>`
Add history entry: `discovery_report_complete`

**5c. Extract alternative approaches**

From the discovery report's prior-art research and persona feedback, synthesize the approaches:

```
SOLUTION SPACE (CLO-XX)
=======================

Approaches Identified:

1. [Approach Name]
   How: [1-2 sentence description]
   Pros: [key advantages]
   Cons: [key disadvantages]
   Prior art: [relevant finding from discovery]
   Risk level: Low / Medium / High

2. [Approach Name]
   ...

3. [Approach Name]
   ...

Discovery Debt: [N] killer assumptions
Verdict: [Ready to Build | Needs Iteration | Major Gaps]
```

Update state: `phases.discovery.approaches_identified: <count>`

---

## Step 6: Approach Selection - "What is the best way?"

Present the evaluation to the user:

```
APPROACH EVALUATION (CLO-XX)
============================

Discovery Debt: [N] killer assumptions
PRD Baseline Score: [X]%
Verdict: [Ready to Build | Needs Iteration | Major Gaps]

Top Killer Assumptions:
1. [assumption] (importance: X, certainty: Y) - [suggested validation]
2. [assumption] (importance: X, certainty: Y) - [suggested validation]

Stress Test Failures:
1. [scenario] - missing requirement: [what to add]

Recommended Approach: [N] - [name]
Reason: [why this approach best fits constraints and findings]

---

Options:
1. [proceed]    - Accept recommended approach, continue to design
2. [choose N]   - Select a different approach (specify number)
3. [iterate]    - PRD needs revision (address killer assumptions first)
4. [pivot]      - Change direction based on findings (describe new direction)
5. [skip-task]  - Discovery shows this task should not be built
6. [pause]      - Save state, continue later

Your choice:
```

**Handle each choice:**

- **proceed / choose N**:
  - Set `phases.discovery.approach_chosen: <description>`
  - Set `phases.discovery.status: checkpoint`
  - Continue to checkpoint

- **iterate**:
  - Ask user which killer assumptions to address
  - Update PRD with findings
  - Re-run relevant parts of discovery
  - Return to this step

- **pivot**:
  - Ask user for new direction
  - Update Linear task description
  - Set `phases.discovery.status: awaiting_input`
  - Add history entry: `discovery_pivot`
  - Return to Step 4 with new context

- **skip-task**:
  - Confirm with user
  - Update Linear task status
  - Set `workflow.status: complete`, `phases.discovery.status: complete`
  - Add history entry: `task_skipped_after_discovery`
  - Exit workflow

- **pause**:
  - Save all state
  - Add history entry: `workflow_paused`
  - Exit with resume instructions

---

## Status: checkpoint

```
DISCOVERY CHECKPOINT (CLO-XX)
=============================

Problem: [1-line problem statement]
Chosen Approach: [approach name and summary]
Discovery Debt: [N] killer assumptions ([rating])
PRD Score: [X]%

Documents:
- PRD: [path] (created: [yes/no])
- Discovery Report: [path]

Unresolved Risks:
- [any killer assumptions not yet validated]

Ready to proceed to Design phase?

Options:
1. [approve]         - Discovery complete, proceed to design
2. [view-report]     - View full discovery report
3. [view-prd]        - View PRD
4. [refine]          - Make changes before proceeding
5. [pause]           - Save state, continue later

Your choice:
```

- **If approve**:
  - Set `phases.discovery.approved: true`
  - Set `phases.discovery.status: complete`
  - Set `workflow.current_phase: design`
  - Set `workflow.status: in_progress`
  - Add history entry: `discovery_approved`
  - **Continue to DESIGN phase**

- **If view-report**: Display discovery report, return to options
- **If view-prd**: Display PRD, return to options
- **If refine**: Ask for changes, update documents, return to checkpoint
- **If pause**: Save state, exit

---

## YAML Checkpoint (MANDATORY before advancing to design phase)

Before setting `workflow.current_phase: design`, write ALL of the following fields to the workflow YAML in a single update:

```yaml
# --- Discovery phase exit fields ---
phases.discovery.status: complete             # or "skipped"
phases.discovery.skip_reason: <reason|null>   # only if skipped
phases.discovery.problem_framed: <true|false>
phases.discovery.prd_exists: <true|false>
phases.discovery.prd_file: <path|null>
phases.discovery.prd_created: <true|false>    # true if /prd create was run
phases.discovery.discovery_report: <path|null>
phases.discovery.discovery_debt: <number|null>
phases.discovery.baseline_score: <number|null>
phases.discovery.approaches_identified: <number|null>
phases.discovery.approach_chosen: <string|null>
phases.discovery.approved: true
workflow.current_phase: design
workflow.status: in_progress
```

If any field cannot be determined (e.g., discovery was skipped), set it to `null` with a YAML comment explaining why.
Do NOT advance to the design phase until every field above is written.
