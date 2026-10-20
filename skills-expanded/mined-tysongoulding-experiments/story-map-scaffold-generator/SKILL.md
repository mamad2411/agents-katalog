---
name: story-map-scaffold-generator
description: >
  Generates a complete, populated UAT story map folder structure for a new application repository from first principles. Use this skill whenever someone wants to bootstrap a story map, scaffold UAT test files, create role-based workflow test scripts, generate happy-path test scripts, or set up a UAT execution framework for an application. Trigger whenever the user mentions: story map, UAT scaffold, test scaffold, happy path generation, UAT agent setup, UAT run sheet, role-based test coverage, or wants to prepare an application for UAT testing. Also use when the user wants to discover application roles and routes and turn them into structured test documentation. This skill is essential any time the phrase "story map" or "UAT scaffold" appears — even casually.
---

# Story Map Scaffold Generator

## Purpose

Bootstrap a complete, populated story map for a new application by discovering its roles, workflows, routes, and scope from the project source code and documentation — then generating every required file so that the existing UAT agent and status-reset agent prompts can be run immediately on the result.

The agent must:
1. Discover the application structure (roles, routes, workflows, feature areas) from the codebase or supplied documentation
2. Build the full folder tree under a `story-map/` directory at the target location
3. Populate every file with real, grounded content — no placeholder-only stubs
4. Produce output that is immediately ready for invocation by `story-map-playwright-mcp-uat-agent.prompt.md`

---

## Bundled Reference Implementations

This skill ships battle-tested reference files under `references/` (proven across real multi-role, multi-portal UAT cycles). Use them as the concrete starting point instead of writing files from scratch — adapt names and values to the target application, but keep the underlying policies intact unless the target app genuinely doesn't need them:

- **`references/uat-agent-reference.prompt.md`** — full reference implementation for `story-map/prompts/story-map-playwright-mcp-uat-agent.prompt.md`. Includes hardened policies proven across real UAT cycles: setup-source retry before blocking, reset-aware resume, blackbox data-tagging and cleanup tracking, console-error gating, and an optional scope-ceiling filter pattern for phased/milestone-based delivery.
- **`references/status-reset-agent-reference.prompt.md`** — already-generic reference implementation for `story-map/prompts/story-map-status-reset-agent.prompt.md`. Can be copied with minimal changes.
- **`references/happy-path-template.md`** — use verbatim as `story-map/shared/happy-path-template.md`.
- **`references/edge-case-template.md`** — use verbatim as `story-map/shared/edge-case-template.md`.
- **`references/tag-matrix-template.md`** — reusable Rules of Use / Tag Sequence Guidance for `story-map/prompts/uat-tagging-field-matrix.md`; populate the Workflow Matrix table fresh for the discovered roles/workflows.

---

## Required Inputs (gather before writing any files)

Before generating content, the agent must have answers to the following. Ask the user if any are unclear.

| Input | Description |
|---|---|
| **Target folder** | Where to create `story-map/` (e.g. `story-map`) |
| **Application base URL** | Local or test environment URL to use in UAT (e.g. `http://localhost:3000`) |
| **UAT cycle name** | Short identifier for the first run sheet (e.g. `UAT-Initial-2026-04`) |
| **Start / End Dates** | First UAT cycle date range for the run sheet |
| **Test Lead** | Name of the person owning UAT execution |
| **Codebase or doc sources** | Where to discover roles and routes — can be one or more of: route config files, README, OpenAPI spec, navigation components, sidebar/menu files, existing test specs. Provide paths. |
| **Scope reference** | Any known scope document, milestone list, or progress tracker that establishes what is in-scope vs deferred vs not-approved for this cycle. Provide path or paste content. |

---

## Discovery Phase (run before authoring any files)

### Step 1 — Identify Roles

Search the codebase for all distinct user roles or portal types:
- Look in: route config files, auth/permission files, navigation menu components, sidebar components, README, API controllers, ACL/role enums
- Produce a **Roles List**: named roles with brief descriptions and their primary dashboard entry route

Common patterns to search for:
```
*routes*.ts, *routes*.js, *router*.ts, *navigation*.vue, sidebar*.vue, *permissions*.ts, role*.ts, *ACL*, *dashboard*, *portal*
```

### Step 2 — Identify Workflows per Role

For each role, identify 1–6 distinct end-user workflows:
- A workflow is a complete, named user journey with a clear start and end state (e.g. "Submit Registration Form", "Approve Change Request", "Submit Vendor Proposal")
- Look in: route files, page/view component names, test spec descriptions, README feature lists, business requirements
- Each workflow should be testable end-to-end through the UI

Assign a short folder-safe workflow ID using kebab-case, prefixed `wf-`:
```
wf-registration-form, wf-change-request, wf-change-approval, wf-vendor-proposal, etc.
```

### Step 3 — Map Routes

Collect all frontend routes for each role:
- Look in: Vue router config, React Router config, Next.js pages folder, Angular routing modules
- Group routes by role/portal they belong to
- Note parameterized routes (`:id`, `:itemId`, etc.)

### Step 4 — Determine Scope

Using the supplied scope document or progress tracker:
- Classify each workflow as: `IN-SCOPE`, `DEFERRED`, or `NOT-APPROVED`
- Record the evidence source for each classification
- If no scope document is available, default all discovered workflows to `IN-SCOPE` and note that scope review is pending

### Step 5 — Map Setup Dependencies

For each `IN-SCOPE` workflow, determine:
- What prerequisite data must already exist for the happy path to run?
- Which other workflow creates that data?
- Can setup be achieved entirely via the UI?

---

## File Authoring Phase

Once discovery is complete, generate files in this order. Do not skip any file.

### A. Root Files

#### `story-map/00-index.md`
Master index linking all files. Must include:
- Purpose statement
- Document Map (linking all generated files)
- Prompt Invocation section (how to run the UAT agent and reset agent)
- Roles list with links to `roles/[role]/index.md`
- Execution Model description (3-file workflow pattern)
- Validation Standard (required fields for each happy-path.md)

Use this structure:
```markdown
# [Application Name] UAT Story Map

Purpose: role-first UAT map with workflow-level happy paths and separate edge-case companions.

## Document Map
...

## Prompt Invocation (Quick Start)
...

## Roles (Primary Axis)
...

## Execution Model
Each workflow has three files:
- `summary.md` (executive summary)
- `happy-path.md` (manual test steps with URL, inputs, expected outcomes)
- `edge-cases.md` (separate to avoid bloat)

## Validation Standard
Each `happy-path.md` must include:
- Scope tag
- Preconditions
- Entry URL
- Field/input checklist
- Step-by-step actions with expected results
- Evidence capture notes
- Email/notification validation via email logs only
```

#### `story-map/01-scope-decisions.md`
Scope decision matrix. Must include:
- Table with columns: Area | Status | Scope Tag | Evidence Source
- One row per discovered workflow, populated from Step 4 of discovery
- Rules for Story Map Authoring section
- Open Reconciliation Queue section (empty or pre-populated from known conflicts)

If the target application's delivery is organized into phases/milestones (e.g. delivery phases, release trains, sprint groupings), add a phase-tag column and a Phase Reference table mapping each phase to its portals/modules and workflows — see the optional scope-ceiling filter pattern in `references/uat-agent-reference.prompt.md`. Skip this entirely for applications without a meaningful phase structure.

#### `story-map/02-uat-run-sheet.md`
Master execution tracker. Must include:
- Run Metadata (cycle name, environment URL, start/end dates, test lead from inputs)
- Status Legend
- Workflow Execution Tracker table — one row per `IN-SCOPE` workflow containing:
  - Role, Workflow, Scope, UAT Auth Role, Happy Path file link, Edge Cases file link
  - Setup Source Workflow, Bootstrap Required (Yes/No)
  - Case IDs (EC-01..N, SEC-01, VAL-01..N as applicable)
  - Happy Status, Edge Status (both `NOT-RUN`)
  - Owner, Evidence Folder path, Notes
- Recommended Execution Order (derived from setup dependency chain)
- Day-by-Day Plan (group workflows into logical days)
- Reset and Re-Run Guidance

#### `story-map/.env`
DB connection settings stub. Content:
```
# UAT Database Connection Settings
# Fill in before running status-reset agent or schema capture
UAT_DB_CONNECTION_STRING=
UAT_DB_PROVIDER=
UAT_DB_DEFAULT_SCHEMA=

# UAT Role Credentials
# One username/password pair per discovered role
# (substitute the actual discovered role names in place of <ROLE>)
UAT_ROLE_<ROLE>_USERNAME=
UAT_ROLE_<ROLE>_PASSWORD=
```

This file will hold real credentials once filled in — treat it like any other secrets file (gitignored, never committed, never echoed back in chat).

#### `story-map/lessons-learned-in-running-story-map.md`
Empty initial file. Content:
```markdown
# Lessons Learned in Running Story Map UAT

This file is maintained by the UAT agent during execution runs.
Do not store raw passwords, tokens, or secrets here.

## Entry Format

Each entry must include:
- Timestamp
- UAT_RUN_ID
- Role/Workflow
- Scenario ID (if available)
- Lesson / observation
- Recommended action

## Entries

(No entries yet — will be populated by UAT agent during first run)
```

---

### B. Shared Files

#### `story-map/shared/route-url-map.md`
Comprehensive route reference. Must include:
- Base URL from inputs
- Grouped sections per role
- All routes discovered in Step 3
- Parameterized route notation (e.g. `/:id`, `/:itemId`)
- Notes on any routes that require special auth or feature flags

#### `story-map/shared/uat-bootstrap-setup.md`
Setup dependency map. Must include:
- Policy section (UI-only, hybrid reuse, data manifest tagging)
- Setup Source Matrix table — one row per workflow with dependent data
  - Columns: Target Workflow | Required Data State | Setup Source Workflow (UI) | Fallback Rule
- Bootstrap Execution Order (numbered list respecting dependency chain)
- Setup Failure Handling rules
- Reset Recovery Contract
- Data Tagging format: `[[UAT|<RUN_ID>|<SCENARIO_ID>|<ENTITY>|<SEQ>]]`

#### `story-map/shared/happy-path-template.md`
Copy `references/happy-path-template.md` from this skill verbatim — do not modify it.

#### `story-map/shared/edge-case-template.md`
Copy `references/edge-case-template.md` from this skill verbatim — do not modify it.

---

### C. Per-Role Files

For each discovered role, create `story-map/roles/[role-id]/`:

#### `story-map/roles/[role-id]/index.md`
Role overview. Must include:
- Role name and executive summary (1–3 sentences)
- In-Scope Workflows list
- Workflow Links (linking to summary.md, happy-path.md, edge-cases.md for each)
- Core Routes (subset of route map for this role)
- Scope Guardrails (notable restrictions for this UAT cycle)

---

### D. Per-Workflow Files

For each workflow of each role, create `story-map/roles/[role-id]/[wf-id]/`:

#### `story-map/roles/[role-id]/[wf-id]/summary.md`
Executive summary. Must include:
- Role and workflow name
- Scope Tag
- 3–5 sentences describing business purpose and outcome
- Key actors (who initiates, who is affected)
- Downstream effects on other roles/workflows
- Scope guardrails or known limitations

#### `story-map/roles/[role-id]/[wf-id]/happy-path.md`
Primary test script. Follow `shared/happy-path-template.md` structure. Must be fully populated with:
- Real entry URL from route map
- Concrete field checklist with example input values derived from the application domain
- Step-by-step actions table (minimum 3 meaningful steps, maximum 10)
- Expected result for each step
- Evidence capture notation (Screenshot / Network tab / Email log)
- Email validation table (if workflow sends notifications)
- Traceability to task IDs or business rules when known

**Quality bar:** A tester with no prior knowledge of the application must be able to execute this script without asking questions.

#### `story-map/roles/[role-id]/[wf-id]/edge-cases.md`
Secondary test script. Follow `shared/edge-case-template.md` structure. Must include:
- 2–4 EC rows (realistic boundary/error scenarios, not invented)
- At least 1 SEC row (permission or auth boundary — e.g. wrong role attempting the action)
- At least 1 VAL row (invalid input with expected validation message)
- Failure Triage guidance

---

### E. Status Scaffold Files

#### `story-map/status/status.md`
Initialize to `NOT-RUN` state. Must include:
- Header with cycle name and timestamp
- `Current Failures (Active)` section — empty placeholder row
- Task Tracker table seeded from `02-uat-run-sheet.md`:
  - One Happy Path row and one Edge Cases row per workflow
  - Columns: Task | Role/Workflow | Current Status | Notes | Failure Link
  - IN-SCOPE tasks → `NOT-RUN`
  - DEFERRED tasks → `DEFERRED`

#### `story-map/status/data-manifest.md`
Initialize empty. Must include:
- Header and purpose
- Data Manifest table with columns:
  - Run ID | Scenario ID | Role/Workflow | Entity Type | Unique Tag | Where Created | Cleanup Method | Cleanup Status | Notes
- Empty placeholder row

#### `story-map/status/schema.md`
Initialize as pending scaffold. Content:
```markdown
# Story Map UAT Schema Snapshot

Captured: (pending — will be populated at first UAT agent startup)
Source: application database metadata (read-only) — provider determined during discovery

## Tables

(Pending capture — UAT agent will populate this from the database during first run using .env connection settings)
```

#### `story-map/status/failures/FAILURE-TEMPLATE.md`
Failure record template. Content:
```markdown
# Failure Record: [SHORT TITLE]

- Failure ID: FAIL-[NNN]
- Run ID:
- Role/Workflow:
- Scenario Type: Happy Path | Edge Case
- Step #:
- Observed Behavior:
- Expected Behavior:
- Console Errors: (paste or describe)
- Screenshots: (link or embed)
- Root Cause Hypothesis:
- Severity: Blocker | Major | Minor
- Status: Open | Resolved | Deferred
- Resolution Notes:
```

---

### F. Prompts Files

The following files must be generated into `story-map/prompts/` so the UAT agent and reset agent can be invoked immediately.

#### `story-map/prompts/story-map-playwright-mcp-uat-agent.prompt.md`
Adapt from **`references/uat-agent-reference.prompt.md`** (bundled with this skill), substituting application-specific values (application name, environment URL, role list, workflow file paths, role credential variable names). Keep its hardened policies (setup-source retry, reset-aware resume, blackbox data-tagging/cleanup, console-error gating) unless they genuinely don't apply. Drop the optional scope-ceiling filter section entirely if the target application has no phase/milestone structure. Must include:
- Agent frontmatter block
- Purpose and required tooling
- Source of truth file references (pointing to generated files)
- Default run mode (`happy-only`) and mode override options
- State and resume model (status folder behavior, temp workspace rule)
- Lessons learned memory contract
- Startup sequence (bootstrap checks, schema capture, status initialization)
- Task execution loop (announce → execute → report → log)
- Pass/fail/blocked rules
- Failure artifact creation rules
- Evidence capture rules
- Console inspection requirement
- Final summary report format

#### `story-map/prompts/story-map-status-reset-agent.prompt.md`
Adapt from **`references/status-reset-agent-reference.prompt.md`** (bundled with this skill) — it is already application-agnostic, so only the frontmatter `description` and any file paths need adjusting. Must include:
- Agent frontmatter block
- Purpose (two reset modes: `soft-reset` default, `hard-reset` with confirmation)
- Artifacts list (pointing to generated files)
- Data management contract for `data-manifest.md`
- Schema handling rules
- Safety rules
- Initialization rules for new `status.md` (seed from `02-uat-run-sheet.md`)

#### `story-map/prompts/uat-tagging-field-matrix.md`
Start from **`references/tag-matrix-template.md`** (bundled with this skill) for the Purpose, Rules of Use, and Tag Sequence Guidance sections, then populate the Workflow Matrix table fresh for every discovered role/workflow. Must include:
- Tag format: `[[UAT|<RUN_ID>|<SCENARIO_ID>|<ENTITY>|<SEQ>]]`
- Allowed fields per entity type (where to embed tags after creating records via UI)
- Instructions for the UAT agent on when and where to add tags
- Examples for each entity type present in the application

---

## Output Validation Checklist

Before declaring the scaffold complete, verify:

- [ ] Every `IN-SCOPE` workflow has `summary.md`, `happy-path.md`, and `edge-cases.md`
- [ ] Every `DEFERRED` workflow has at least `summary.md` with scope tag and reason
- [ ] `02-uat-run-sheet.md` has one row per workflow (no missing roles)
- [ ] `shared/uat-bootstrap-setup.md` matrix matches the dependency chain from discovery
- [ ] `shared/route-url-map.md` lists all routes discovered in Step 3
- [ ] `status/status.md` is seeded to `NOT-RUN` for all `IN-SCOPE` tasks
- [ ] `prompts/story-map-playwright-mcp-uat-agent.prompt.md` references all generated file paths correctly
- [ ] `prompts/story-map-status-reset-agent.prompt.md` references all generated file paths correctly
- [ ] `00-index.md` document map links to every generated file
- [ ] `.env` stub exists
- [ ] `lessons-learned-in-running-story-map.md` initial file exists

---

## Quality Standards

### Grounding Rule
Every file must be grounded in the actual discovered application. Do not generate generic or lorem-ipsum content. Specifically:
- Route URLs must be real routes from the codebase
- Field names must match actual UI labels or `data-testid` values where discoverable
- Evidence capture steps must reference real pages (e.g. actual log pages, not generic notes)
- Scope tags must trace to the supplied scope document or clearly note "Scope review pending"

### Executable First
The happy-path.md files are the single most important output. A tester must be able to run them without asking follow-up questions. Prioritize completeness of steps, URLs, and expected results over brevity.

### Setup Chain Integrity
The bootstrap setup matrix must be internally consistent. If workflow B depends on workflow A's output, then workflow A must appear earlier in the bootstrap execution order and as the setup-source for workflow B.

### No Orphan Files
Every generated file must be linked from at least one other file (usually `00-index.md` and the relevant `roles/[role]/index.md`).

---

## Execution Instructions for the Agent

1. **Ask for required inputs** if any are missing (see Required Inputs table above)
2. **Run discovery** (Steps 1–5) and present a summary table of discovered roles and workflows; confirm with the user before writing files
3. **Write files in order**: root files → shared files → per-role files → per-workflow files → status scaffold → prompts
4. **Report progress** after each group of files is written
5. **Run output validation checklist** and fix any gaps
6. **Present final summary**: total files created, folder tree, how to invoke the UAT agent
