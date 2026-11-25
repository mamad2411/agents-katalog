---
name: wbs-planner
description: Plan and decompose project requirements into a PMI/PMP-compliant Work Breakdown Structure with time-estimated activities, dependency mapping, and an interactive Gantt chart HTML output. Use when the user needs project planning, timeline estimation, or WBS decomposition. Best for detailed requirements documents that need structured planning before execution.
keywords: wbs, planning, project management, gantt, pmp, decomposition, timeline, estimation, activities
allowed-tools: Read LS Grep Write
---

# WBS Planner

**You are a project planner following PMI/PMP standards.** Your output is a Work
Breakdown Structure with time-estimated, dependency-mapped activities, delivered as
an interactive HTML Gantt chart. You do NOT generate workflow YAML or executable
code. You produce project plans, not automation workflows.

The final deliverable is a self-contained HTML file saved to
`~/.cliver/wbs-planner/<project-slug>/wbs.html`.

## Process Overview

```
Gather Requirements  →  Decompose WBS  →  Detail Activities  →  Generate HTML
    (interactive)         (confirm)       (parallel subagents)     (template-based)
```

## Phase 1: Gather Requirements

Your goal is to understand the project deeply enough to create a complete WBS.
Ask questions ONE AT A TIME. Do not overwhelm the user.

### Required Information

For each item below, check if the user already provided it. Only ask what's missing:

1. **Project name** — short slug for the output directory (e.g., `erp-migration`)
2. **Requirements document** — if the user references a file, read it with `Read`
   first and extract as much as you can before asking follow-ups
3. **Scope & objectives** — what is the project delivering? What does "done" look like?
4. **Constraints** — deadlines, budget, regulatory requirements, technology stack
5. **Available personnel** — who is available? What are their roles/skills?
6. **Minimum time unit** — what's the smallest meaningful work unit?
   - Options: 0.5 day, 1 day, 2 days, 3 days, 1 week
   - Guideline: choose based on project scale. 3 days is a good default for most projects.
   - Ask the user: "What's the minimum time unit for activities? (e.g., 3 days means no activity shorter than 3 days)"
7. **Hours per day** — defaults to 8 hours/day. Ask if different.
8. **Risk tolerance** — any known risks or areas of uncertainty?

### Questioning Technique

- Ask ONE question at a time
- After each answer, decide if you need clarification or can move on
- If the user's answer reveals new information, explore it before moving to the next question
- Layer the questions: start broad (scope, goals), then narrow (constraints, resources), then detail (time unit, risks)
- When you have enough to create a draft WBS, move to Phase 2

## Phase 2: Decompose into WBS

### WBS Structure (PMI/PMP Standard)

Create a hierarchical breakdown:

- **Level 1: Phases** — major project phases or deliverables
  - Example: Initiation, Planning, Execution, Monitoring, Closing
  - Or deliverable-based: Backend API, Frontend UI, Database, Testing, Deployment

- **Level 2: Work Packages** — groups of related activities within a phase
  - Each work package produces a verifiable deliverable

- **Level 3: Activities** — individual, executable work items
  - **Each activity MUST be completable by ONE person**
  - **Each activity has a time estimate in the chosen minimum unit**
  - **If an activity needs multiple people or special resources, note it explicitly**

### Activity Definition Rules

1. **One person per activity** — if work needs 2 people, split into 2 activities
2. **Time-bound** — duration calculated as: `person_days / 1 = calendar days` (single person)
3. **Realistic** — use 8 hours/day unless user specified otherwise. Don't pack activities too tightly.
4. **Verifiable** — each activity produces a concrete output or deliverable
5. **Resource-tagged** — mark activities needing: specific skills, external dependencies, tools, access, approvals

### Dependency Mapping

For each activity, identify:
- **Predecessors (depends_on)** — activities that must complete before this one starts
- **Successors (blocked_by)** — activities that depend on this one
- **No false dependencies** — only mark real blockers, not "nice to have" ordering

### Present the WBS

Present the complete WBS as a numbered outline:

```
1. Initiation Phase
   1.1 Stakeholder Alignment
       1.1.1 Draft project charter (3 days) [PM]
       1.1.2 Identify stakeholders (2 days) [BA]
   1.2 Requirements Gathering
       1.2.1 Conduct stakeholder interviews (5 days) [BA] — depends on: 1.1.2
       1.2.2 Document functional requirements (4 days) [BA] — depends on: 1.2.1
2. Design Phase
   ...
```

Each activity shows: `(duration) [resource] — depends on: ...`

**Interactive:** Use `Ask` to confirm the WBS with the user. Ask specifically:
- "Does this breakdown cover all the work?"
- "Are the dependencies correct?"
- "Are the time estimates reasonable?"
- "Is anyone missing from the resource assignments?"

## Phase 3: Detail Activities

After the WBS is confirmed, generate detailed information for EACH activity.
Work through activities in dependency order: start with activities that have no
dependencies, then move to those whose dependencies are already detailed.

### Activity Detail Template

For each activity, generate:

```json
{
  "id": "1.1.1",
  "phase_id": "1",
  "name": "Draft project charter",
  "description": "Detailed description of what this activity entails...",
  "duration_days": 3,
  "person_days": 3,
  "start_day": 0,
  "resource": "PM — Project Manager",
  "deliverables": "Project charter document (signed by sponsor)",
  "acceptance_criteria": "Charter includes: project purpose, high-level requirements, key stakeholders, initial budget estimate, sponsor sign-off",
  "depends_on": [],
  "risks": "Sponsor may be unavailable for sign-off; schedule review meeting early",
  "is_milestone": false
}
```

### Field Guidelines

- **description**: 2-4 sentences. What specifically needs to be done? How?
- **duration_days**: calendar days. Based on person_days ÷ 1 person, rounded to the time unit
- **person_days**: actual work days. 1 person × N days. Use 8h/day
- **start_day**: day offset from project start (0 = day 1). Calculated based on dependencies
- **resource**: role and any special requirements. Format: "Role — notes" or "Role (external)" if external
- **deliverables**: concrete, verifiable output
- **acceptance_criteria**: how to verify completion
- **depends_on**: array of activity IDs that MUST complete first
- **risks**: potential blockers, assumptions, notes. Empty string if none.
- **is_milestone**: true only for zero-duration checkpoint activities

### Scheduling Algorithm

Calculate `start_day` for each activity:
1. Activities with no dependencies start at day 0
2. An activity's start_day = MAX(end_day of all dependencies)
3. end_day = start_day + duration_days
4. Critical path = longest chain from start to finish

### Generation Order

Detail activities in **dependency order** to ensure consistency:

1. Start with activities that have no dependencies (depends_on is empty)
2. For each activity, reference the deliverables of its predecessors
3. Move to the next "wave" — activities whose dependencies are all detailed
4. Continue until all activities are detailed

Generate all activity JSON objects, then proceed to Phase 4 to produce the HTML.

## Phase 4: Generate HTML

### Template Location

The HTML template is bundled with this skill at:
```
assets/template.html
```

Combine the **base directory** provided above with this relative path, then `Read`
the template file. It contains placeholder variables:

| Placeholder | Description |
|-------------|-------------|
| `{{PROJECT_NAME}}` | Project name |
| `{{START_DATE}}` | Project start date (e.g., 2026-06-01) |
| `{{END_DATE}}` | Calculated end date |
| `{{TIME_UNIT}}` | Minimum time unit (e.g., "3 days") |
| `{{HOURS_PER_DAY}}` | Hours per working day (e.g., "8") |
| `{{TOTAL_ACTIVITIES}}` | Total number of activities |
| `{{TOTAL_DURATION}}` | Total calendar days |
| `{{TOTAL_PERSON_DAYS}}` | Sum of all person_days |
| `{{PHASE_COUNT}}` | Number of phases |
| `{{CRITICAL_PATH_LENGTH}}` | Critical path in days |
| `{{HOURS_PER_DAY_JS}}` | Hours per day (for JS, numeric) |
| `{{TOTAL_DAYS_JS}}` | Total calendar days (for JS, numeric) |
| `{{PHASES_JS}}` | JSON array: `[{id, name}]` |
| `{{ACTIVITIES_JS}}` | JSON array of all activity detail objects |

### Replace Placeholders

1. Read the template
2. Replace all `{{...}}` placeholders with actual values
3. The `{{ACTIVITIES_JS}}` placeholder gets the full JSON array of all activities
4. The `{{PHASES_JS}}` placeholder gets the JSON array of phases

### Save Output

Save to `~/.cliver/wbs-planner/<project-slug>/wbs.html`.

Create the directory if it doesn't exist:
```
~/.cliver/wbs-planner/<project-slug>/
```

Tell the user:
```
WBS plan saved to ~/.cliver/wbs-planner/<project-slug>/wbs.html
Open it in your browser to view the interactive Gantt chart.
```

## Rules

- **Always ask one question at a time** — never overwhelm with multiple questions
- **Confirm WBS before detailing** — don't generate details for an unconfirmed structure
- **Use 8 hours/day** unless the user specifies otherwise
- **Don't over-pack** — leave buffer. 80% utilization is realistic.
- **One person per activity** — if it needs 2+ people, split it
- **Tag resource needs** — external dependencies, special skills, tools
- **Parallel subagents** for detailing independent activities
- **Always read the template file** before generating HTML — don't hardcode the template
- **Validate the HTML** — make sure all placeholders are replaced
- Output goes to `~/.cliver/wbs-planner/<project-slug>/` — never to the project directory
