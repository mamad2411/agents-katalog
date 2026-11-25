---
name: init
description: Initialize Circle framework for the current project. Creates output directories in home folder (zero project footprint). Checks and installs optional dependencies. Run once per project.
---

# Circle Init

Initialize the Circle-METHOD framework for the current project. All outputs are stored externally in the home directory — nothing is added to the project repository.

## Soul

Read and apply `../../resources/soul.md` before continuing.

## Process

### 0. Inspect optional integrations

Inspect the integrations exposed by the current host and check local binaries with `command -v`. Circle has no required external dependency.

If Linear, Notion, or another integration would materially help, explain why and offer it through the host plugin manager. Never install or connect an integration without the user's explicit confirmation. Record any project-specific preferences in `~/.circle/projects/$PROJECT_NAME/config.yaml`.

### 1. Detect project name

Derive from current directory: `basename "$PWD" | tr '[:upper:]' '[:lower:]'`

### 2. Detect domain

Analyze files in the current directory:
- **software**: if common project markers exist (e.g., `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `*.xcodeproj`, `Makefile`, `CMakeLists.txt`, `Gemfile`, `build.gradle`)
- **business**: if `business-plan.md`, `market-analysis.md`, or `strategy.md` exists
- **personal**: if `goals.md`, `journal.md`, or `habits/` folder exists
- **general**: default if no domain indicator found

### 3. Migrate legacy state and create output structure

Zero footprint — all in home directory:
```bash
PROJECT_NAME=$(basename "$PWD" | tr '[:upper:]' '[:lower:]')
BASE=~/.circle/projects/$PROJECT_NAME

mkdir -p $BASE/output/{scope,arch,impl,qa,e2e,security,ux,refine,facilitate,docs,pr-review,triage}
mkdir -p $BASE/output/sessions
mkdir -p $BASE/shards/{requirements,architecture,tasks}
mkdir -p $BASE/shards/sessions
mkdir -p $BASE/workspace
```

### 4. Create or migrate session state

Check if `~/.circle/projects/$PROJECT_NAME/output/session-state.json` already exists.

**If it does NOT exist** — create a fresh v2 file:
```json
{
  "version": 2,
  "project": "<project-name>",
  "domain": "<detected-domain>",
  "updated": "<ISO-8601 timestamp>",
  "sessions": {}
}
```

**If it exists** — check the `version` field:
- If `version` is `2`: already migrated, skip.
- If `version` is absent or `1`: run **v1 → v2 migration**:

**Migration algorithm** (must be idempotent):
1. Copy the file to `session-state.v1-backup.json` (safety net)
2. Read the existing `workflow` object from root
3. If `workflow.type` is `"none"` or the `workflow` object is empty:
   - Write v2 with empty `sessions: {}`
4. Else (active or completed workflow exists):
   - Generate session ID: `{project}-001`
   - Create a session entry by moving `workflow` fields into it
   - Add `type` from `workflow.type`, `created` from root `created`, `updated` from root `updated`
   - Move root `artifacts` array into the session entry
5. Set `version: 2` at root
6. Remove root fields: `phase`, `workflow`, `artifacts`, `created`
7. Write back to `session-state.json`

**If the file is not valid JSON**: warn the user and offer to back up and create a fresh v2 file.

### 5. Check for project config

- If `~/.circle/projects/$PROJECT_NAME/config.yaml` exists, report it
- If not, search for a config template in the repo:
  - Check: `docs/circle/config.yaml`, `Docs/circle/config.yaml`, `.circle/config.yaml`
  - If found: copy it to `~/.circle/projects/$PROJECT_NAME/config.yaml` and report:
    ```
    Found project Circle config template at <path>. Copied to ~/.circle/projects/<project>/config.yaml
    ```
  - If not found: suggest: "Create `~/.circle/projects/$PROJECT_NAME/config.yaml` for project-specific customization."

### 6. Confirm

```
Circle initialized for: <project-name>
Domain: <detected-domain>
Output: ~/.circle/projects/<project-name>/output/

Optional integrations:
  <summary of available integrations>
  Add or connect integrations through the host plugin manager after user confirmation.

Available roles:
  circle:scope       - Scope Clarifier (requirements, work items)
  circle:arch        - Architecture Owner (design, ADRs, trade-offs)
  circle:impl        - Implementer (implementation, code review)
  circle:qa          - Quality Guardian (test strategy, QA)
  circle:e2e         - E2E Author (end-to-end tests in the E2E suite)
  circle:ux          - Experience Designer (UI/UX design)
  circle:refine      - Refiner (prioritization, roadmap)
  circle:facilitate  - Facilitator (cycle planning, coordination)
  circle:security    - Security Guardian (audits, threat modeling)
  circle:docs        - Documentation Steward (doc generation)

Review:
  circle:pr-review - Multi-agent PR code review with AGENTS.md or CLAUDE.md compliance
  circle:triage      - Triage PR review comments

Orchestrators:
  circle:greenfield - Full workflow (analysis → QA)
  circle:cycle      - Cycle planning ceremony (Shape Up)

Utilities:
  circle:validate-prd     - Validate PRD quality (8 checks)
  circle:tdd              - TDD red-green-refactor cycle
  circle:shard            - Split large documents into shards
  circle:skills-discovery - Discover and install external skills (security-gated)
  circle:council          - Pressure-test a hard decision (5 lenses + chairman)
  circle:status           - Project status dashboard
  circle:init             - Project initialization (already done)

Start with: circle:scope to gather requirements, or circle:greenfield for the full workflow.
```
