---
name: create-workflow
description: Design and validate a YAML workflow state machine with state transitions, permission modes, and tool restrictions. Use when the user wants to create a multi-step process with enforced stages like code review flows, deployment pipelines, research processes, or approval chains.
user-invocable: true
---

# Create Workflow — State Machine Designer

Design a YAML workflow that enforces a multi-step process with state transitions, per-state tool restrictions, and permission modes.

## When to Use Workflows vs Skills

| Use a Skill | Use a Workflow |
|-------------|----------------|
| Repeatable task with steps | Process with enforced stages |
| Agent follows instructions voluntarily | System enforces what tools are available per stage |
| No state tracking needed | State tracked across interactions |
| e.g., "Run a DCF valuation" | e.g., "Plan → Implement → Review → Ship" |

**Rule of thumb**: If the agent must NOT skip a stage or use certain tools before completing a prior stage, use a workflow. If it's guidance the agent follows, use a skill.

## Process

### Step 1: Understand the Process

Ask one at a time:

1. **What process does this workflow enforce?**
   - e.g., "Code change: plan → implement → review → verify"
   - e.g., "Research: gather → analyze → validate → present"
   - e.g., "Incident: triage → investigate → remediate → postmortem"

2. **What are the stages (states)?**
   - List each stage and what happens there
   - What marks a stage as complete (transition condition)?

3. **Should tools be restricted per stage?**
   - e.g., Planning stage: read-only tools only
   - e.g., Review stage: no file writes
   - e.g., Implementation: all tools available

4. **What permission mode per stage?**
   - `plan` — read-only, agent proposes but doesn't act
   - `ask` — agent asks before each action
   - `allow` — agent can read/write freely
   - `bypass` — full autonomy including shell execution

### Step 2: Design the State Machine

Map out states and transitions:

```
[initial] → [state-2] → [state-3] → [done]
              ↑                        |
              └────── (rejected) ──────┘
```

For each state, define:
- **name**: Short identifier (snake_case)
- **allowed_tools**: Tool allowlist (null = all)
- **permission_mode**: plan | ask | allow | bypass (optional, derived from tools if omitted)
- **on_entry**: Instructions when entering this state
- **on_exit**: Cleanup when leaving (optional)
- **transitions**: List of possible next states with optional conditions

### Step 3: Write the YAML

Use this format:

```yaml
name: workflow-name
description: What this workflow enforces
initial_state: first-state

states:
  first-state:
    name: first-state
    allowed_tools:
      - file_read
      - grep_search
      - glob
      - web_search
    permission_mode: plan
    on_entry: "Explore the problem space. Read relevant code and docs. Do NOT make changes yet."
    transitions:
      - to: second-state
        condition: "has_plan_summary"
        action: "Summarize your plan before proceeding"

  second-state:
    name: second-state
    allowed_tools: null    # all tools
    permission_mode: allow
    on_entry: "Implement the plan. Make changes as needed."
    transitions:
      - to: review
      - to: first-state    # allow going back

  review:
    name: review
    allowed_tools:
      - file_read
      - grep_search
      - shell          # for running tests
    permission_mode: ask
    on_entry: "Review all changes. Run tests. Verify correctness."
    transitions:
      - to: done
        condition: "tests_pass"
      - to: second-state
        condition: "needs_fixes"

  done:
    name: done
    on_entry: "Work complete. Present summary of changes."
    transitions: []
```

### Step 4: Validate

Run the validation script:

```bash
bash scripts/validate-workflow.sh <workflow-file.yaml>
```

The validator checks:
- Initial state exists in states map
- All transition targets point to existing states
- State names match their keys
- No orphan states (unreachable from initial)
- Required fields present (name, description, initial_state)

**Fix any validation errors before delivering.**

### Step 5: Place the File

- If part of an agent: `agents/<agent-name>/workflows/<name>.yaml`
- If standalone: `workflows/<name>.yaml`
- If adding to existing agent: update AGENT.yaml workflows list

## Common Workflow Patterns

### Linear Pipeline
```
gather → analyze → validate → present
```
Good for: research, analysis, report generation

### Review Gate
```
draft → review → (approve → done | reject → draft)
```
Good for: code changes, content creation, deployments

### Triage Fork
```
intake → triage → (critical → escalate | normal → process → done)
```
Good for: incident response, support tickets

### Iterative Loop
```
attempt → evaluate → (pass → done | fail → attempt)
```
Good for: optimization, testing, quality improvement

## State Design Tips

- **Start restrictive**: Begin with `plan` mode and read-only tools, open up as the process advances
- **Gate important transitions**: Require explicit conditions before moving to destructive stages
- **Allow backwards transitions**: Let the agent go back if it discovers problems
- **Keep states focused**: Each state should have one clear purpose
- **Terminal state**: Always include a `done` state with empty transitions

$ARGUMENTS
