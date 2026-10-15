---
name: developer-summary
description: Generates a concise developer summary from planning artifacts. Auto-discovers business requirements, technical requirements, milestones, and timeline from the docs/ folder structure. Outputs a focused summary with project overview, deliverables, and milestone roadmap.
---

# Developer Summary

Generates a developer-focused summary document from Sherpy planning artifacts. Provides developers with a quick-start view of what's being built, key deliverables, and the milestone roadmap.

## Usage

```
/developer-summary [base-directory]
```

If no directory is provided, auto-detect by looking for `requirements/business-requirements.yaml` in the current directory.

If not found, prompt the user: "Where are your planning artifacts located?"

Wait for the user to provide a path before proceeding.

## Required Artifacts

The skill auto-discovers these files from the standard Sherpy folder structure:

| File | Location | Purpose |
|------|----------|---------|
| `business-requirements.yaml` | `requirements/` | Project overview and deliverables |
| `technical-requirements.yaml` | `requirements/` | Technical context and architecture |
| `milestones.yaml` | `implementation/` | Milestone sequence and estimates |
| `timeline.yaml` | `delivery/` | Timeline estimates and dates |

## Process

### Step 1: Determine Base Directory and Scan for Required Artifacts

If no directory parameter was provided, check if `requirements/business-requirements.yaml` exists in the current directory.

- If found, use current directory as `base_directory`
- If not found, prompt: "Where are your planning artifacts located?" and wait for user response

Once `base_directory` is determined, scan for required files in standard locations. Display status:

```
## Developer Summary — Dependency Check

Scanning for required artifacts...

 ✓  requirements/business-requirements.yaml
 ✓  requirements/technical-requirements.yaml
 ✓  implementation/milestones.yaml
 ✗  delivery/timeline.yaml

3 of 4 required files found.
```

**Legend:** ✓ found · ✗ missing

### Step 2: Handle Missing Files

If any required files are missing, ask:

> "Missing required files: timeline.yaml
>
> Options:
> 1. **Continue with partial data** — Generate summary with available information (missing sections will be marked as [Not Available])
> 2. **Exit** — Complete missing artifacts first (run /delivery-timeline to generate timeline.yaml)
>
> What would you like to do?"

Wait for user response:
- If user chooses **1 (Continue)**: Proceed with available data, mark missing sections clearly
- If user chooses **2 (Exit)**: Display which skills to run and exit gracefully

### Step 3: Load and Parse Artifacts

Read all available files and extract:

**From business-requirements.yaml:**
- Project name and description
- Core features and capabilities
- Key deliverables

**From technical-requirements.yaml:**
- Technology stack
- Architectural patterns
- Key technical components

**From milestones.yaml:**
- Milestone sequence (m0, m1, m2, etc.)
- Milestone names and descriptions
- Dependencies between milestones
- Estimated duration per milestone

**From timeline.yaml (if available):**
- Total project duration
- Target completion date
- Timeline workback schedule

### Step 4: Generate Developer Summary

Create `summaries/developer-summary.md`.

The output document includes: header (timestamp, project name), `Overview` (3-5 sentence synthesis), `Deliverables` (grouped by category), `Milestones & Timeline` (M0, M1... with duration, dependencies, key deliverable), and `Summary` (total milestones, estimated duration, target completion).

See **[references/output-spec.md](references/output-spec.md)** for the complete document specification with section structure and formatting rules.

See **[references/example.md](references/example.md)** for a full example.

### Step 5: Handle Missing Data Gracefully

When required files are missing, insert clear placeholders:

```markdown
## Milestones & Timeline

[Not Available - `milestones.yaml` not found. Run `/implementation-planner` to generate milestones.]
```

Or for partial data:

```markdown
## Summary

**Total Milestones:** 4
**Estimated Total Duration:** 6 weeks (estimated from milestones)
**Target Completion:** [Not Available - run `/delivery-timeline` to set production deploy date]
```

### Step 6: Confirmation

After generating the summary, display:

```
## Developer Summary Generated ✓

**Location:** summaries/developer-summary.md
**Size:** [file size]

Summary includes:
  ✓ Project overview
  ✓ Deliverables breakdown
  ✓ Milestone roadmap
  [Missing data: timeline completion date - run /delivery-timeline]

The summary is ready for developer onboarding and reference.
```

## Deliverables Extraction Logic

### Identifying Deliverables

Parse the following sources to build the deliverables list:

**From business-requirements.yaml:**
- `functional_requirements` → User-facing features
- `features` or `capabilities` → High-level capabilities
- `scope.in_scope` → Explicitly included items

**From technical-requirements.yaml:**
- `architecture.components` → Technical components
- `technology_stack` → Infrastructure items (databases, APIs, services)
- `data_model.entities` → Domain entities/models
- `apis.endpoints` → API endpoints if listed
- `integration_points` → External integrations

### Categorization Rules

Group deliverables into logical categories based on type:

- **API Endpoints** - REST/GraphQL endpoints, webhooks
- **Domain Handlers** - Business logic handlers, command processors
- **UI Components** - Pages, views, components (if applicable)
- **Data Models** - Entities, schemas, database tables
- **Infrastructure** - Databases, message queues, auth systems
- **Integrations** - External service connections
- **Background Jobs** - Scheduled tasks, workers
- **Configuration** - Environment setup, deployment configs

Use the most relevant categories based on what's present in the requirements. Don't force categories that don't apply.

## Overview Generation Logic

### Crafting the Overview Paragraph

Synthesize information from multiple sources to create a concise, informative overview:

**Elements to include (in order):**
1. **What** - The system/feature being built (1 sentence)
2. **Why** - The problem it solves or value it provides (1 sentence)
3. **How (high-level)** - The approach or key capability (1 sentence, optional)

**Source fields to use:**
- `business-requirements.yaml`:
  - `description` or `overview`
  - `business_goals.primary_goal`
  - `success_criteria`
- `technical-requirements.yaml`:
  - `solution_overview`
  - `architecture.approach`

**Template:**
> "[System Name] is a [type of system] that [primary function]. It addresses [problem] by [solution approach], enabling [key benefit/outcome]. The system will [key technical approach or differentiator]."

**Example:**
> "The Sherpy CLI is a structured planning tool for AI-assisted software development. It addresses requirement drift and planning gaps by conducting guided interviews and generating comprehensive implementation plans with task-level detail. The system enforces best practices like task sizing, TDD requirements, and style anchors throughout the planning process."

### Keep it Concise

- Maximum 5 sentences
- No bullet points in the overview
- Focus on business value, not implementation details
- Avoid jargon unless it's domain-specific and necessary

## Milestone Roadmap Logic

### Extracting Milestone Information

For each milestone in `milestones.yaml`, extract:

**Required fields:**
- `id` - Milestone identifier (m0, m1, etc.)
- `name` - Milestone title
- `description` - What the milestone delivers
- `estimated_duration` - Time estimate
- `dependencies` - Which milestones must complete first

**Formatting:**
- Display milestones in sequence (m0 → m1 → m2...)
- Show dependencies clearly
- Highlight the "key deliverable" from the first line of the description or the most important success criterion

**Example extraction:**
```yaml
# From milestones.yaml:
milestones:
  - id: m1
    name: API Foundation
    description: |
      Build core REST API with authentication and authorization.
      Includes user management endpoints and JWT token handling.
    dependencies: [m0]
    estimated_duration: 2 weeks
    success_criteria:
      - All auth endpoints functional
      - JWT tokens properly validated
```

**Renders as:**
```markdown
### M1: API Foundation
**Duration:** 2 weeks
**Dependencies:** M0
**Key Deliverable:** Core REST API with authentication and authorization
```

### Timeline Calculation

If `timeline.yaml` is available:
- Use `total_duration` field
- Use `production_deploy_date` for target completion
- Show the calculated project dates

If only `milestones.yaml` is available:
- Sum all `estimated_duration` values
- Convert to appropriate unit (days/weeks)
- Note that this is an estimate without QA/PR time

If neither is available:
- Mark as "TBD" with instruction to run appropriate skill

## Error Handling

### File Not Found

If a required file doesn't exist in the expected location:
- Check alternative common locations (root directory as fallback)
- Display clear error with exact path tried
- Suggest which Sherpy skill generates that file

### Invalid YAML

If a file exists but can't be parsed:
- Display parsing error
- Show the file path and line number if available
- Suggest checking file format or regenerating

### Missing Required Fields

If a file is missing expected fields:
- Use sensible defaults or mark as "[Not Specified]"
- Continue generating summary with available data
- Note missing fields in the confirmation output

## Output Location

Always output to: `{base_directory}/summaries/developer-summary.md`

If the directory doesn't exist, create it:
```bash
mkdir -p {base_directory}/summaries
```

## Integration with Sherpy Flow

This skill is designed to be called as **Step 10** in `/sherpy-flow`. When invoked by sherpy-flow, it receives `base_directory` as a parameter. It should:
- Run after all planning artifacts are complete
- Auto-discover files from the organized folder structure within `base_directory`
- Not fail if optional files (like timeline) are missing
- Generate the summary without user interaction when all files are present

## Examples

See **[references/example.md](references/example.md)** for a complete sample developer summary.

## Related Skills

- `/executive-summary` - Generate executive summary for stakeholders
- `/sherpy-flow` - Full planning workflow (includes this skill at the end)
- `/implementation-planner` - Generates the milestones.yaml used by this skill
- `/delivery-timeline` - Generates the timeline.yaml used by this skill
