---
name: vault-metadata
description: |
  Canonical frontmatter schema reference for all PARA types in the Teslasoft Obsidian vault.
  Defines shared base fields, per-type required/optional/auto-managed schemas, consumer field maps,
  auto-managed field ownership, and Dataview query patterns.
  Single source of truth for all metadata conventions — templates, panels, MCP tools, and Drone
  collectors validate against these definitions.
  Keywords: frontmatter, metadata, schema, PARA, canonical, status, type, horizon, Dataview,
  query, repoPath, consumer map, auto-managed, lifecycle panel, FrontmatterManager, assigned_team,
  spec file, team file, context-packet, prompt, policy, enforcement, domain, session_date, branch,
  policy_refs, design
triggers:
  - frontmatter schema
  - metadata values
  - status values
  - type values
  - horizon format
  - dataview query
  - write a dataview query
  - repository path
  - repoPath
  - metadata guidelines
  - canonical schema
  - PARA frontmatter
  - consumer field map
  - auto-managed fields
  - assigned_team
  - team file
  - spec file
  - context-packet
  - prompt schema
  - enforcement values
  - domain field
  - session_date
  - policy_refs
  - design schema
  - token_threshold
  - context budget
  - warn urgent emergency
negative_triggers:
  - create a note
  - PARA structure
  - use template
  - apply template
  - archive note
version: 3.7.0
author: Christian Kusmanow / Junie
last_updated: 2026-06-17
---

# Vault Metadata — Canonical Frontmatter Schema Reference

Single source of truth for all PARA frontmatter schemas in the Teslasoft Obsidian vault. All consumers — lifecycle panels, FrontmatterManager, Dataview dashboards, Drone collectors, vault-mcp tools, vault-hooks — validate against these definitions.

## When to Use

- Defining or validating frontmatter fields for any PARA note type
- Checking valid status/type/horizon values
- Writing or debugging Dataview queries
- Understanding which consumers read/write each field
- Working with repository path (`repoPath`) fields

## When NOT to Use

- Creating notes or understanding PARA structure (use `vault-notes`)
- Looking up template sections and Templater syntax (use `vault-templates`)

---

## Quick Start

1. Identify the PARA type of the note (`type` field or folder path)
2. Look up the canonical schema in Section 2 for that type
3. Check field classification: Required / Important / Optional / Auto-managed
4. For valid values, see Section 3 (types) and Section 4 (status values)
5. For Dataview queries, see Section 9 for patterns

**Checkpoint**: The note's frontmatter contains all Required fields and uses canonical values from this skill.

> **Wikilink format:** Always `"[[filename]]"` (filename-only). Never `"[[folder/filename]]"` unless basename is ambiguous. See vault-notes skill for full convention.

---

## 1. Shared Base Fields

Fields used across multiple PARA types. Every PARA note SHOULD have these unless explicitly excluded in the per-type schema.

| Field | Classification | Type | Values / Format | Consumers |
|-------|---------------|------|-----------------|-----------|
| `type` | **Required** | string | See Section 3 | All Dataview dashboards, FrontmatterManager, para-indexer, para-configs, rc-watcher |
| `status` | **Required** | string | Per-type values in Section 4 | All Dataview dashboards, FrontmatterManager, all lifecycle panels, inbox-integrate |
| `created` | **Important** | string | `YYYY-MM-DD` | Templates, manual reference |
| `tags` | Optional | array | `[]` | Dataview queries, rc-watcher SEMANTIC_FIELDS |
| `domain` | Optional | string | Free-form (see below) | rc-watcher SEMANTIC_FIELDS, future validation library, domain-driven workflow routing |
| `actors` | Optional | array | Flow-array of role/agent IDs (`[architect, developer, vault-maintainer]`) | `actor-resolver.js` (CQRS hook) — see §13 |
| `last_activity` | Auto-managed | string | `YYYY-MM-DD` | inbox-lifecycle.js, lifecycle panels, inbox-integrate |
| `checkpoint_count` | Auto-managed | integer | `0` (incremented) | inbox-lifecycle.js |
| `last_commit` | Auto-managed | string | Git commit hash | inbox-lifecycle.js |
| `applies_policies` | Optional | array | `[LR-VOP-001, ...]` | VCA (P67) policy aggregation |
| `relevant_tools` | Optional | array | `[Read, Write, ...]` | VCA (P67) tool-chain context |
| `process_chain` | Optional | string | "Pattern Name" | VCA (P67) workflow routing |
| `related_skills` | Optional | array | `[vault-metadata, ...]` | VCA (P67) skill-context injection |
| `enrichments_disabled` | Optional | array | `[test_cli_help, ...]` | HET (P66) opt-out |
| `vca_disabled` | Optional | array | `[policy_aggregation, ...]` | VCA (P67) opt-out |
| `token_threshold` | Optional | object | `{warn: 70, urgent: 85, emergency: 95}` (% of model context) | Context-injection hooks (P30-W4 inject-token-warning) — see §14 |

**Classification legend:**
- **Required** — Must be present; consumers break without it
- **Important** — Panels use it; should be present but consumers handle absence gracefully
- **Optional** — Useful but not load-bearing
- **Auto-managed** — Written by code; humans should not edit

**`domain` field:** Cross-cutting Optional field applicable to any PARA type. Enables domain-specific CI-001 workflow routing and specialized execution tiers. Common values: `governance`, `operations`, `git`, `orchestration`, `infrastructure`, `quality`, `documentation`, `ux`, `ai`, `engineering`. The field is free-form — new domains can be added without schema changes. Indexed by rc-watcher SEMANTIC_FIELDS for semantic search.

**`actors` field:** Cross-cutting Optional field on inbox items (§2.1) and team-spec files (§2.9). Declares the **roster of roles or agents authorized to write** for this work item or team scope under CQRS-001 enforcement on `project/P##-*` branches. Distinct from `assigned_role` / `assigned_roles` (ownership/triage intent) — see §13 for the full distinction matrix, canonical on-disk form, accepted-on-read fallbacks, resolution lookup chain, and round-trip caveat. Defined by [[CQRS-002-actors-field|CQRS-002]] (Phase 1 ADR, S242).

**`token_threshold` field:** Cross-cutting Optional object that defines the percentage thresholds at which context-injection hooks emit warnings about agent context-window consumption. Resolves through a five-level precedence chain (inbox-item → project-master → agent profile → role profile → global default). Canonical default is `{warn: 70, urgent: 85, emergency: 95}`. See §14 for full schema, precedence, and partial-override semantics. Consumed by P30-W4 `inject-token-warning` hook and forward-compatible with the INJ-001 context-injection policy.

---

## 2. Canonical Schemas per PARA Type

### 2.1 Inbox (Work Item — Model B, CI-001)

The vault has TWO inbox models: (A) GTD quick-capture and (B) CI-001 phased work items. The lifecycle panel serves Model B. Model A items are processed via GTD triage. See Section 2.1b for Model A.

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: inbox                        # Always 'inbox'
status: pending                    # pending | active | blocked | done
project: "[[P##-Project-Name]]"           # Must reference a 20_Projects/ entry

# ── IMPORTANT ────────────────────────────────────────────
priority: normal                   # urgent-important | important | urgent | normal
execution_mode: parallel-session   # parallel-session | single-session | async
assigned_role: "[[.claude/roles/developer/SKILL|Developer]]"  # Valid role from roles.index.yaml
assigned_team: "[[P58-Team]]"      # Link to P{id}-Team.md
phase: collect                     # collect | analyze | implement | verify | integrate | archive
created: "YYYY-MM-DD"
# ── OPTIONAL ─────────────────────────────────────────────
depends_on: slug                   # Dependency slug (other work item)
tags: []
policy_refs: []
actors: [architect, developer, vault-maintainer]  # CQRS write-authorization roster (§13, CQRS-002)
boot_tier: standalone              # Dashboard override (standalone | team | fleet)
working_set: "P58,P59"            # Dashboard override — comma-separated project IDs
session_date: "YYYY-MM-DD HH:mm"  # Session-notes variant only (see 2.1c)
branch: project/P##-name          # Session-notes variant only (see 2.1c)
auto_pilot_disabled: "false"       # CLAP (P68) opt-out
priority_weight: 1.0              # CLAP (P68) priority weighting
token_threshold:                   # Inbox-item override (most specific in precedence — see §14)
  warn: 70
  urgent: 85
  emergency: 95

# ── AUTO-MANAGED ─────────────────────────────────────────
last_activity: "YYYY-MM-DD"          # inbox-lifecycle.js
checkpoint_count: 0                # inbox-lifecycle.js
last_commit: abc1234               # inbox-lifecycle.js
dispatched_to: .worktrees/...      # Set when dispatched to worktree
completed_session: S###            # Set on completion
completed_date: "YYYY-MM-DD"         # Set on completion
commits: "hash1,hash2"            # Filled on completion
blocked: "true"                     # Toggled by panel
gate_status: null                  # PASS | WARN | BLOCK
phase_advanced_at: "ISO"           # CLAP (P68) advancement timestamp
phase_advanced_by: agent-id        # CLAP (P68) advancer ID
phase_blocked_by: "reason"         # CLAP (P68) blocking reason
phase_dispatch_in_flight: agent-id # CLAP (P68) idempotency lock
```

### 2.1b Inbox (GTD Quick-Capture — Model A)

```yaml
captured: "YYYY-MM-DD HH:mm"         # Capture timestamp
processed: false                    # true when triaged
tags: [inbox]                       # Always includes 'inbox'
```

Model A items have NO `type` field. The absence of `type: inbox` distinguishes Model A from Model B.

### 2.1c Inbox (Session Notes — Model B variant)

Session notes are Model B inbox items that record what happened in a work session. They use the full Model B schema plus two additional Optional fields:

```yaml
# ── Extends Model B (Section 2.1) ──────────────────────
session_date: "2026-03-20 14:30"   # Session timestamp (YYYY-MM-DD HH:mm)
branch: project/P58-w14            # Git branch for this session's work
```

**Distinction from Model A:** Session notes always have `type: inbox` (Model B). Model A GTD captures use `captured`/`processed` fields and have NO `type` field. The session-notes-rubric Gate 1.2 validates `type: inbox` — this applies to session notes (Model B), not to Model A GTD captures.

### 2.2 Goal

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: goal
status: active                     # planning | active | reviewing | completed | partial
horizon: "YYYY-QN"                   # e.g., 2026-Q1

# ── IMPORTANT ────────────────────────────────────────────
created: "YYYY-MM-DD"
# ── STRUCTURED (widget + user) ───────────────────────────
key_results:                       # Structured KR array
  - id: kr1
    label: "KR description"
    project: P##                   # Linked project ID
    target: 100                    # Target percentage
    progress: 0                    # Auto-updated from project status

# ── OPTIONAL ─────────────────────────────────────────────
tags: []

# ── AUTO-MANAGED ─────────────────────────────────────────
completed_date: "YYYY-MM-DD"         # Set when status → completed
```

### 2.3 Project

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: project
status: active                     # planning | active | on-hold | completed
goal: ["[[G-YYYY-QN ...]]"]        # Array of wikilinks to parent goals

# ── IMPORTANT ────────────────────────────────────────────
project: "[[P##-Project-Name]]"          # Canonical project ID field
created: "YYYY-MM-DD"
repoPath: path/to/repo             # External code location (Windows absolute path)

# ── OPTIONAL ─────────────────────────────────────────────
tags: []
priority: important                # urgent-important | important | urgent | normal
title: "Human-readable title"
policy_refs: []                    # Array of policy IDs (e.g., [HAW-001, CI-001])
session_namespace: P##             # Per-project session-counter namespace (e.g. P72). See §7.7
project_slug: project-slug         # Customer/project slug (e.g. falke-tek). Pairs with session_namespace

# ── AUTO-MANAGED ─────────────────────────────────────────
last_activity: "YYYY-MM-DD"          # Updated by panel/agent
```

> **`session_namespace` + `project_slug` (Optional, paired):** the declarative selector that
> activates a per-project session counter for the project's sessions. `session_namespace` is the
> P## project id used as the commit-scope / telemetry qualifier (e.g. `P72`); `project_slug` is the
> customer/project slug under `projects/` (e.g. `falke-tek`). Set both only on project notes whose
> sessions use a per-project counter — absent on every other project (those keep the global vault
> counter). Read by `resolveSessionNamespace` + `pnpm session:open` (see §7.7). Live example: the
> P72 falke-tek project note carries both.

### 2.4 Area

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: area

# ── IMPORTANT ────────────────────────────────────────────
status: active                     # active | hibernating
created: "YYYY-MM-DD"
# ── OPTIONAL ─────────────────────────────────────────────
projects: []                       # Array of wikilinks
resources: []                      # Array of wikilinks
tags: []

# ── AUTO-MANAGED ─────────────────────────────────────────
last_reviewed: "YYYY-MM-DD"          # AreaLifecyclePanel
review_cycle: monthly              # monthly | quarterly | manual
hibernated: false                  # AreaLifecyclePanel
```

### 2.5 Resource

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: resource

# ── IMPORTANT ────────────────────────────────────────────
category: AI                       # AI | Engineering | IoT | Hosting | Protocols | CMS | ECM | etc.

# ── OPTIONAL ─────────────────────────────────────────────
repoPath: path/to/repo             # External code location
created: "YYYY-MM-DD"
status: active                     # active (optional for resources)
tags: []

# ── AUTO-MANAGED ─────────────────────────────────────────
last_verified: "YYYY-MM-DD"          # ResourceLifecyclePanel
depth: reference                   # reference | deep-dive
outdated: false                    # ResourceLifecyclePanel
```

### 2.6 Collaboration

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: collaboration
status: active                     # planning | active | paused | completed
partner: Name

# ── IMPORTANT ────────────────────────────────────────────
created: "YYYY-MM-DD"
related_projects: [P44, P35]       # Array of project IDs

# ── OPTIONAL ─────────────────────────────────────────────
patreonURL: https://...
contactEmail: email@...
tags: []

# ── AUTO-MANAGED ─────────────────────────────────────────
last_activity: "YYYY-MM-DD"          # CollabLifecyclePanel
next_meeting: "YYYY-MM-DD"           # CollabLifecyclePanel
```

### 2.7 Research / Science

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: research
status: active                     # exploring | active | blocked | parked | concluded | integrated

# ── IMPORTANT ────────────────────────────────────────────
category: Architecture             # Free-form category
created: "YYYY-MM-DD"
related_projects: []               # Array of project IDs

# ── OPTIONAL ─────────────────────────────────────────────
tags: []

# ── AUTO-MANAGED ─────────────────────────────────────────
concluded_date: "YYYY-MM-DD"         # ScienceLifecyclePanel
blocked: "false"                     # ScienceLifecyclePanel
parked: false                      # ScienceLifecyclePanel
derived_project_suggested: false   # ScienceLifecyclePanel
```

### 2.8 Skill (Vault `70_Skills/` only)

This schema is for vault personal skill notes in `70_Skills/`. Agent SDL skills (`.claude/skills/`) use a different schema with `version`, `triggers`, `negative_triggers`.

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: skill
level: expert                      # novice | developing | proficient | expert | master

# ── IMPORTANT ────────────────────────────────────────────
created: "YYYY-MM-DD"
# ── OPTIONAL ─────────────────────────────────────────────
related_areas: []                  # Wikilinks to 30_Areas/
related_goals: []                  # Wikilinks to 10_Goals/
tags: []

# ── AUTO-MANAGED ─────────────────────────────────────────
last_practiced: "YYYY-MM-DD"         # SkillLifecyclePanel
```

### 2.9 Additional Types

#### ADR (Architecture Decision Record)

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: adr
status: accepted                   # proposed | accepted | deprecated | superseded

# ── IMPORTANT ────────────────────────────────────────────
date: "YYYY-MM-DD"                   # Decision date
project: "[[P##-Project-Name]]"    # Related project

# ── OPTIONAL ─────────────────────────────────────────────
session: S###
tags: []
```

**Location:** `40_Resources/architecture/`

#### Project Master

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: project-master
project: "[[P##-Project-Name]]"
status: active                     # active | completed

# ── OPTIONAL ─────────────────────────────────────────────
token_threshold:                   # Project-default override (level 2 in precedence — see §14)
  warn: 70
  urgent: 85
  emergency: 95

# ── AUTO-MANAGED ─────────────────────────────────────────
created: "YYYY-MM-DD"
last_activity: "YYYY-MM-DD"
checkpoint_count: 0
last_commit: hash
phase: collect                     # collect | analyze | implement | verify | integrate | archive
blocked: "false"
priority: normal                   # urgent-important | important | urgent | normal
tags: []
```

**Location:** `00_Inbox/P{N}-{Name}/P{N}-Master.md`
**Links to:** `P{N}-Team.md` (if team execution is planned)

#### Team File

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: project-team
project: "[[P##-Project-Name]]"
status: active                     # active | completed

# ── IMPORTANT ────────────────────────────────────────────
created: "YYYY-MM-DD"
phase_roles:                       # Per-phase role assignments (overrides defaults)
  collect: investigator            # Who runs the COLLECT phase
  analyze: planner                 # Who runs the ANALYZE phase
  implement: developer             # Who runs the IMPLEMENT phase
  verify: verification-collector   # Who runs the VERIFY phase
  integrate: orchestrator          # Who runs the INTEGRATE phase

# ── OPTIONAL ─────────────────────────────────────────────
actors: [architect, developer, vault-maintainer]  # CQRS roster — canonical roster source for child inbox items (§13, CQRS-002)
```

**Location:** `00_Inbox/P{N}-{Name}/P{N}-Team.md`
**Purpose:** Defines team composition and execution modes for a project's work items.
**Referenced by:** Inbox work items via `assigned_team` frontmatter field.

**`phase_roles` field:** Maps each CI-001 phase to the role responsible for executing it. When no `*.team.md` exists or `phase_roles` is absent, the following defaults apply:

| Phase | Default Role |
|-------|-------------|
| `collect` | investigator |
| `analyze` | planner |
| `implement` | developer |
| `verify` | verification-collector |
| `integrate` | orchestrator |

The team lookup chain resolves phase-role assignments in priority order:
1. `*.spec.md` (most specific)
2. Work item inbox item
3. Parent inbox item
4. Inbox Master (`P{N}-Master.md`)
5. Project note (least specific)

**Required content sections:**

1. **Team Roster** — Agent roles with model tier and responsibilities per phase
2. **Phase-Team Mapping** — Which team mode (solo, pair, fleet) applies to each CI-001 phase
3. **Work Item Type Routing** — Rules for assigning work item types to agents/teams
4. **Execution Widgets** — DataviewJS and/or Service-Monitor code blocks showing active executions, completions, and gate counts

#### Design

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: design
status: draft                      # draft | approved | complete

# ── IMPORTANT ────────────────────────────────────────────
project: "[[P##-Project-Name]]"    # Related project ID or wikilink
created: "YYYY-MM-DD"
# ── OPTIONAL ─────────────────────────────────────────────
session: S###                      # Session that produced this design
author: role-name                  # Author role
tags: []
policy_refs: []                    # Array of policy IDs (e.g., [HAW-001, CI-001])
```

**Location:** `00_Inbox/P{N}-{Name}/`, `coordination/designs/`, `docs/plans/`

#### Idea

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: idea
status: active                     # active | processed | archived

# ── OPTIONAL ─────────────────────────────────────────────
project: P##
priority: normal                   # P1 | P2 | P3 | normal
created: "YYYY-MM-DD"
source: "where the idea came from"
tags: []
```

**Location:** `00_Inbox/`

#### Policy

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: policy
policy_id: SKL-001                 # Format: [A-Z]{2,}-\d{3}
version: "1.0"                     # Policy version (string)
status: active                     # active | deprecated | draft
enforcement: BLOCK                 # BLOCK | WARN | ADVISORY

# ── IMPORTANT ────────────────────────────────────────────
title: "Skill Reference Integrity" # Human-readable policy title
created: "YYYY-MM-DD"
# ── OPTIONAL ─────────────────────────────────────────────
scope: [agents]                    # Array of scope identifiers
applies_to: [all-roles]            # Array of target roles/systems
target_roles: [developer, architect] # Roles that MUST know this policy (compliance tests)
domain: quality                    # governance | operations | git | orchestration | infrastructure | quality | documentation
updated: "YYYY-MM-DD"               # Last update date (use `updated`, not `last_updated`)
tags: []
```

**Location:** `coordination/policies/`
**Enforcement values:**
- `BLOCK` — Violation prevents the action from completing (hard gate)
- `WARN` — Violation emits a warning but action proceeds (soft gate)
- `ADVISORY` — Guidance only, no enforcement mechanism

#### Archive

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: archive
originalType: project              # The original PARA type before archival

# ── IMPORTANT ────────────────────────────────────────────
archivedDate: YYYY-MM-DD           # When the item was archived
originalLocation: 20_Projects/     # Original folder path

# ── OPTIONAL ─────────────────────────────────────────────
tags: [archived]
```

**Location:** `90_Archive/` (mirrored subfolder structure)

#### Context Packet

```yaml
# ── REQUIRED ─────────────────────────────────────────────
type: context-packet
work_item_id: P25-W15-DRONE-API-WIRING   # Matches inbox item slug
status: pending                    # pending | active | completed

# ── IMPORTANT ────────────────────────────────────────────
inbox_ref: 00_Inbox/P25-Harness-Telemetry/p25-w15.md  # Path to source inbox item
worktree_path: .worktrees/p25-w15/ # Worktree directory
branch: work/p25-w15              # Git branch
assigned_role: "[[developer]]"                    # Assigned role
created: YYYY-MM-DDTHH:mm:ss.sssZ # ISO 8601 timestamp

# ── OPTIONAL ─────────────────────────────────────────────
autonomy_level: 1                  # 0 | 1 | 2
session_id: S###                   # Session that consumed this packet
```

**Location:** `coordination/context-packets/`
**Purpose:** Provides pre-loaded context for worktree-dispatched agents. Generated by `context_packet_generate` MCP tool.

#### Prompt

```yaml
# ── REQUIRED ─────────────────────────────────────────────
purpose: recovery                  # Category: recovery | generation | analysis | triage
description: |
  Brief description of what this prompt accomplishes.

# ── IMPORTANT ────────────────────────────────────────────
agent: "[[.claude/agents/orchestrator|Orchestrator]]"                # Target agent role
created: "YYYY-MM-DD"
# ── OPTIONAL ─────────────────────────────────────────────
skills: [/skill-name]              # Skills the prompt requires
tools: [tool-name]                 # Tools the prompt uses
review: |                          # Review instructions
  Optional review guidance.
```

**Location:** `00_Inbox/.prompts/`, `00_Inbox/s{{N}}/`, `.prompts/`
**Purpose:** Reusable agent prompt templates. Template: `.obsidian/templates/Prompt.md`

---

## 3. Type Values

| Type | Folder |
|------|--------|
| `goal` | `10_Goals/` |
| `project` | `20_Projects/` |
| `area` | `30_Areas/` |
| `resource` | `40_Resources/` |
| `adr` | `40_Resources/architecture/` |
| `collaboration` | `50_Collab/` |
| `research` | `60_Science/` |
| `skill` | `70_Skills/` |
| `inbox` | `00_Inbox/` |
| `project-master` | `00_Inbox/P{N}-{Name}/` |
| `project-team` | `00_Inbox/P{N}-{Name}/` |
| `design` | `00_Inbox/P{N}-{Name}/`, `coordination/designs/`, `docs/plans/` |
| `idea` | `00_Inbox/` |
| `archive` | `90_Archive/` |
| `policy` | `coordination/policies/` |
| `context-packet` | `coordination/context-packets/` |
| `prompt` | `00_Inbox/.prompts/`, `.prompts/`, `00_Inbox/s{{N}}/` |

---

## 4. Status Values per Type

### Goals
- `planning` — Not yet started
- `active` — Currently pursuing
- `reviewing` — Under review
- `completed` — Achieved
- `partial` — Partially achieved

### Projects
- `planning` — Not yet started
- `active` — Currently working on
- `on-hold` — Paused temporarily
- `completed` — Finished

### Areas
- `active` — Ongoing responsibility
- `hibernating` — Temporarily inactive

### Resources
- `active` — Current and maintained (optional field)

### Collaborations
- `planning` — Being discussed
- `active` — Ongoing partnership
- `paused` — Temporarily inactive
- `completed` — Concluded

### Research (Science)
- `exploring` — Initial investigation
- `active` — Active research
- `blocked` — Blocked on dependency
- `parked` — Intentionally paused
- `concluded` — Research complete
- `integrated` — Findings absorbed into project

### Skills
- No `status` field — use `level` for progression

### Inbox (Model B)
- `pending` — Not yet started
- `active` — In progress
- `blocked` — Waiting on dependency
- `done` — Completed

### ADR
- `proposed` — Under discussion
- `accepted` — Decision made
- `deprecated` — No longer valid
- `superseded` — Replaced by another ADR

### Policy
- `draft` — Under development
- `active` — Currently enforced
- `deprecated` — No longer enforced

### Context Packet
- `pending` — Generated but not yet consumed
- `active` — Being used by an agent session
- `completed` — Session finished

### Design
- `draft` — Under development
- `approved` — Design accepted for implementation
- `complete` — Design finalized

### Idea
- `active` — Under consideration
- `processed` — Triaged and acted upon
- `archived` — No longer relevant

---

## 5. Horizon Values (Goals only)

**Format:** `YYYY-QN` (e.g., `2026-Q1`, `2026-Q2`)

Used in Goals frontmatter and Dataview queries to filter by quarter.

---

## 6. Repository Path Integration

**Purpose:** Bridge between vault and external code repositories

**Pattern:** Absolute Windows paths in `repoPath` frontmatter field

**Common Base Paths:**
- `D:\TeamProjects\Teslasoft\` — Teslasoft projects
- `D:\TeamProjects\AwesomeNodes\` — AwesomeNodes projects
- `D:\TeamProjects\GT-SWEATLORDS\` — Gaming community projects

**When Working with Projects:**
1. Check if `repoPath` exists in frontmatter
2. Reference it when discussing code/implementation
3. Never modify paths without explicit confirmation
4. Suggest adding `repoPath` if project has external repo

---

## 7. Consumer Field Map

### 7.1 Lifecycle Panels (harness-telemetry)

| Panel | Reads | Writes |
|-------|-------|--------|
| InboxLifecyclePanel | `project`, `assigned_role`, `assigned_team`, `phase`, `status`, `priority`, `execution_mode`, `gate_status`, `blocked`, `dispatched_to`, `last_activity`, `depends_on` | `phase`, `status`, `blocked` |
| GoalLifecyclePanel | `horizon`, `area`, `status`, `key_results`, `title` | `status`, `completed_date` |
| ProjectLifecyclePanel | `horizon`, `status`, `goal`, `last_activity`, `total_work_items`, `completed_work_items`, `project` | `status` |
| AreaLifecyclePanel | `status`, `last_reviewed`, `review_cycle`, `projects`, `resources`, `hibernated` | `last_reviewed`, `hibernated`, `status` |
| ResourceLifecyclePanel | `category`, `depth`, `source`, `status`, `outdated`, `last_verified` | `last_verified`, `outdated` |
| CollabLifecyclePanel | `partner`, `status`, `last_activity`, `next_meeting`, `related_projects`, `activity_log` | `activity_log` |
| ScienceLifecyclePanel | `status`, `derived_project_suggested`, `related_projects`, `parked`, `findings` | `findings`, `parked`, `status`, `derived_project_suggested` |
| SkillLifecyclePanel | `level`, `last_practiced`, `category`, `related_areas`, `related_goals` | `progress_log` |

### 7.2 Dataview Dashboards

| Dashboard | Load-Bearing Fields |
|-----------|-------------------|
| 00-Vault-Status-Dashboard | `type`, `status`, `horizon`, `goal`, `level` |
| Project-Progress-Dashboard | `type`, `status`, `goal` |
| Policy-Status-Dashboard | `type`, `status`, `policy_id` |
| Agent-Activity-Dashboard | `type`, `status` |

### 7.3 Drone Collectors

| Collector | Fields Read |
|-----------|-------------|
| para-indexer.js | `type`, `status` |
| para-enricher.js | `type`, `status` |
| housekeeping-collector.js | `project`, `type`, `status`, `hk_id`, `category`, `risk_level` |
| scanner-handler.js | `project` |

### 7.4 vault-mcp Tools

| Tool | Fields Used |
|------|-------------|
| para-configs.ts | `type`, `status`, `goal`, `horizon`, `level`, `category`, `partner`, `projects[]`, `resources[]` |
| inbox-integrate.ts | `status`, `last_activity`, `completed_session`, `completed_date`, `commits`, `project` |
| vault_frontmatter | All fields (generic read/write) |
| vault_search_similar_frontmatter | `SEMANTIC_FIELDS` from rc-watcher |

### 7.5 rc-watcher SEMANTIC_FIELDS

```
type, status, tags, project, goal, area, title, domain, phase, priority, category
```

### 7.6 vault-hooks (inbox-lifecycle.js)

| Handler | Fields Written |
|---------|---------------|
| `handleEnterProject()` | `last_activity`, `checkpoint_count` |
| `handleLeaveProject()` | `last_activity` |
| `handleCheckpoint()` | `checkpoint_count`, `last_activity` |
| `handleCollabSave()` | `last_commit`, `checkpoint_count`, `last_activity` |
| `handleSessionClose()` | `last_activity` |

### 7.7 Per-Project Session Counter (session_namespace + project_slug)

| Consumer | Fields Read | Purpose |
|----------|-------------|---------|
| `resolveSessionNamespace` (vault-mcp `src/lib/session-namespace.ts`) | `session_namespace`, `project_slug` | Resolve the active session's namespace + counter path from the project-note frontmatter (precedence: call param > frontmatter > env) |
| `pnpm session:open` (invoked by fleet-hub Phase 1a `/fleet init` + `/fleet resume`) | `session_namespace`, `project_slug` | Derive the `--namespace` / `--slug` flags; increment the per-project counter once at open (resume adds `--resume`, no increment) |

**What they route:** the per-project session counter at `projects/<project_slug>/.session/session-counter.json`
(gitignored, local runtime state) and the per-project CHR buckets `s{n}` / `s{n}-{r}` under
`projects/<project_slug>/agent-state/sessions/`. A project with no `session_namespace` uses the
global vault counter (the `## Current Session (S###)` heading) — unchanged.

---

## 8. Auto-Managed Field Ownership

Complete registry of fields written by code, not humans.

| Field | Owner | Types |
|-------|-------|-------|
| `last_activity` | inbox-lifecycle.js | inbox, project-master |
| `checkpoint_count` | inbox-lifecycle.js | inbox, project-master |
| `last_commit` | inbox-lifecycle.js | inbox, project-master |
| `completed_session` | inbox-integrate.ts | inbox |
| `completed_date` | inbox-integrate.ts / GoalLifecyclePanel | inbox, goal |
| `commits` | inbox-integrate.ts | inbox |
| `dispatched_to` | orchestrator | inbox |
| `blocked` | InboxLifecyclePanel / ScienceLifecyclePanel | inbox, research |
| `gate_status` | InboxLifecyclePanel | inbox |
| `phase` | InboxLifecyclePanel | inbox |
| `last_reviewed` | AreaLifecyclePanel | area |
| `review_cycle` | AreaLifecyclePanel | area |
| `hibernated` | AreaLifecyclePanel | area |
| `last_verified` | ResourceLifecyclePanel | resource |
| `depth` | ResourceLifecyclePanel | resource |
| `outdated` | ResourceLifecyclePanel | resource |
| `last_practiced` | SkillLifecyclePanel | skill |
| `concluded_date` | ScienceLifecyclePanel | research |
| `parked` | ScienceLifecyclePanel | research |
| `derived_project_suggested` | ScienceLifecyclePanel | research |
| `activity_log` | CollabLifecyclePanel | collaboration |
| `next_meeting` | CollabLifecyclePanel | collaboration |

---

## 9. Dataview Query Patterns

### Active Projects
```dataview
LIST FROM "20_Projects"
WHERE type = "project" AND status = "active"
SORT file.mtime desc
```

### Goals by Quarter
```dataview
LIST FROM "10_Goals"
WHERE horizon = "2026-Q1"
SORT file.name
```

### Resources by Category
```dataview
TABLE type, repoPath
FROM "40_Resources"
WHERE type = "resource"
```

### Active Inbox Items by Project
```dataview
TABLE status, priority, phase, assigned_role
FROM "00_Inbox"
WHERE type = "inbox" AND status != "done"
SORT priority ASC
```

### Skills by Level
```dataview
TABLE level, last_practiced
FROM "70_Skills"
WHERE type = "skill"
SORT level ASC
```

### Custom Patterns

- `FROM "folder"` — Scope to PARA folder
- `WHERE type = "value"` — Filter by note type
- `WHERE status = "value"` — Filter by status
- `SORT file.mtime desc` — Sort by last modified
- `TABLE field1, field2` — Tabular output with specific fields

---

## 10. Impact on Operations

Metadata changes can break:
- **Dashboard queries** — Dashboards use Dataview filtered by `type` and `status`
- **Goal-Project links** — Changing `goal` field breaks relationship chain
- **Backlinks** — Removing `[[]]` links breaks Obsidian's backlink graph
- **Dataview views** — Changing `type` values will exclude notes from filtered views
- **Lifecycle panels** — Panels read specific field names; renaming breaks rendering
- **Drone collectors** — para-indexer and housekeeping-collector read `type`, `status`, `project`
- **vault-mcp tools** — para-configs and inbox-integrate read/write specific fields

Always check `vault-notes` Common Tasks for safe modification workflows.

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| Unknown `type` value in frontmatter | Check Section 3 Type Values — may be a discovered type (adr, project-master, idea) or an error |
| Field not in canonical schema | Check Section 7 Consumer Field Map — may be a legacy alias read by panels with fallback |
| Dataview query returns no results | Verify `type` value matches exactly (case-sensitive); check folder scope in `FROM` clause |
| Auto-managed field has stale value | Do not edit manually — the owning system (Section 8) will update it on next trigger event |
| Conflicting field names across consumers | Canonical names are in Section 2 per-type schemas; aliases exist in panels for backward compatibility |

---

## Security & Permissions

- **Required tools**: Read (for schema lookup)
- **Confirmations**: Metadata changes can break dashboards and panels — verify impact (Section 10) before modifying `type` or `status` fields
- **Trust model**:
  - Instructions: trusted
  - User input: trusted (vault owner)
  - External content: not applicable (local vault only)
- **Forbidden**: Never modify `type` or `status` values to non-canonical values listed in Sections 3-4

---

## 11. File Conventions

### 11.1 Spec Files (`*.spec.md`)

**Purpose:** Formalized project specifications that define scope, phases, quality gates, and acceptance criteria. Specs are the contract between planning and execution.

**Naming:** `P##-ProjectName.spec.md` (e.g., `P56-Vault-Frontmatter-Maintenance.spec.md`)

**Location:** `20_Projects/`

**When to create:**
- At project inception or when scope is formally defined
- When a project has multiple phases requiring explicit acceptance criteria
- When multiple agents/roles will execute against a shared specification

**Frontmatter:**

```yaml
---
type: spec
status: active                     # active | completed | superseded
project: "[[P56-Vault-Frontmatter-Maintenance]]"
created: "YYYY-MM-DD"
tags: []
---
```

**Required sections:** Objective, Scope, Phases (with quality gates), Acceptance Criteria

### 11.2 Team Files (`*.team.md`)

**Purpose:** Define team composition and execution modes for a project's work items. Replaces the older `P{id}-Team.md` naming convention — team files can be attached to ANY PARA file, not just projects.

**Naming:** `P##-Team.md` (project-scoped) or `{ParentName}-Team.md` (general)

**Location:** `00_Inbox/P{N}-{Name}/` (project-scoped) or alongside the parent PARA file

**When to create:**
- When a project requires multi-agent execution
- When different CI-001 phases need different team configurations
- When work items within a project use different execution modes

**Frontmatter:**

```yaml
---
type: project-team
project: "[[P##-Project-Name]]"
status: active                     # active | completed
created: "YYYY-MM-DD"
---
```

**Required sections:**
1. **Team Roster** — Agent roles with model tier and responsibilities per phase
2. **Phase-Team Mapping** — Which team mode (solo, pair, fleet) applies to each CI-001 phase
3. **Work Item Type Routing** — Rules for assigning work item types to agents/teams
4. **Execution Widgets** — DataviewJS and/or Service-Monitor code blocks (optional)

**Referenced by:** Inbox work items via `assigned_team: "[[P##-Team]]"` frontmatter field

---

## 12. Schema Ownership & Consumer Handoff

vault-metadata is the **single source of truth** (SSOT) for all PARA frontmatter schemas. Other skills and tools are **consumers** that reference vault-metadata, not co-owners.

**Ownership boundaries:**

| Concern | Owner | Consumers |
|---------|-------|-----------|
| Field definitions (names, types, valid values) | vault-metadata | All |
| Document generation methodology | doc-specialist | — |
| Template sections and Templater syntax | vault-templates | — |
| Note operations (create, archive, link) | vault-notes | — |
| Code-level field parsing | FrontmatterManager, para-configs.ts | — |
| Semantic indexing fields | rc-watcher SEMANTIC_FIELDS | — |

**Consumer contract:** When consumers (doc-specialist rubrics, vault-notes, vault-templates) reference frontmatter fields, they should point to vault-metadata as the authority rather than hardcoding field definitions inline. If a consumer needs fields not in vault-metadata, the field should be added to vault-metadata first.

---

## 13. Actors Field — CQRS Authorization Roster

The `actors` field is the **canonical CQRS write-authorization roster** for an inbox item or team-spec file. It is read by `.claude/roles/hooks/pre-tool-use/actor-resolver.js` at commit time on `project/P##-*` branches and matched against the resolved agent identity. Defined by [[CQRS-002-actors-field|CQRS-002]] (S242 Phase 1 ADR).

> **Scope:** This section is the SSOT for `actors` field semantics. Tool-side enforcement (`actor-resolver.js`, `cqrs-enforce-hook.js`) may evolve in P53 Phase 3+; this section governs author-facing canonical form, distinction from adjacent fields, and resolution lookup order regardless of hook implementation details.

### 13.1 Distinction from Adjacent Fields (CQRS-002 D1)

Four adjacent frontmatter fields each play a distinct role. Confusion between them is the most common authoring error.

| Field | Purpose | Who reads it | Example |
|-------|---------|--------------|---------|
| `actors` | **CQRS authorization roster** — who MAY write | `actor-resolver.js` via `cqrs-enforce-hook.js` | `[architect, developer, vault-maintainer]` |
| `assigned_role` | Ownership / triage — who SHOULD drive this | Dashboards, lifecycle panels, spawn routing | `"[[.claude/roles/developer/SKILL\|Developer]]"` |
| `assigned_roles` | Plural variant of `assigned_role` | Same as above | `[architect, developer]` |
| `role` / `assigned_team` | Team pointer — references a `*.team.md` | Spawn composition, dashboards | `"[[P53-Team]]"` |

**Mental model:** `assigned_role` is "who **should** drive this work item." `actors` is "who is **permitted** to commit on the work item's branch." OR-gate resolution (D3 below) means in practice an authorized author satisfies either field; declaring `actors` explicitly is the recommended pattern for multi-role work items, while a single-author item may rely on `assigned_role` alone.

### 13.2 Canonical On-Disk Form (CQRS-002 D2)

**Write exactly this shape:**

```yaml
actors: [architect, developer, vault-maintainer]
```

**Rules:**

1. YAML flow-array syntax (`[...]`) — bracket-bounded, comma-separated.
2. Bare identifiers — no wiki-link brackets (`[[...]]`), no quotes, no path prefixes.
3. Lowercase, kebab-case, matching the canonical role or agent ID exactly.
4. Single-line flow form only (no multi-line block array). Authors needing many entries should declare `actors` on the parent `*.team.md` instead.

**Two valid entry shapes per item:**

- **Role name** — any role from `.claude/roles/roles.index.yaml`: `architect`, `developer`, `vault-maintainer`, `housekeeper`, `team-builder`, etc. Matches every agent inheriting that role.
- **Agent ID** — any `p{N}-{role}` instance or persistent agent name from `.claude/agents/*.md`: `p53-architect`, `p53-developer`, `orchestrator-hub`. Matches only that specific agent.

### 13.3 Accepted-on-Read Forms (CQRS-002 D2 — Backward Compatibility)

The H1-fixed `actor-resolver.js` (P53 Phase 3) parses these forms identically:

| Shape | Example | Status |
|-------|---------|--------|
| Flow array (canonical) | `actors: [architect, developer]` | Preferred — write this |
| Plain CSV | `actors: architect, developer` | Accepted — used by P35 legacy items |
| Wiki-link CSV | `actors: "[[architect, developer]]"` | Accepted — S241 workaround |
| Pipe-aliased role wikilink | `actors: "[[.claude/roles/architect/SKILL\|Architect]]"` | Accepted (single role) — used by `assigned_role` shape |

**Not accepted:** multi-line block arrays (`actors:\n  - architect\n  - developer`). Authors who need many entries should move the roster to the parent `*.team.md`.

### 13.4 Round-Trip Caveat (CQRS-002 D2b — Interim Until P56 Phase 4)

**Live runtime evidence (S242):** the Obsidian harness-telemetry plugin's `processFrontMatter` converts canonical flow-arrays `tags: [a, b, c]` into quoted scalars `tags: "[a, b, c]"` on every lifecycle write. Until P56 Phase 4 ships a targeted-field patcher (FMM-001 implementation), authors of items that will be touched by `inbox-lifecycle.js` should be aware:

- **Plain canonical form `actors: [a, b, c]`** is round-trip-stable for read (the H1 fix accepts the corrupted quoted form), but the on-disk shape will silently degrade to `actors: "[a, b, c]"` after the first lifecycle event. Hook resolution still works.
- **Wiki-link CSV form `actors: "[[a, b, c]]"`** is the **interim canonical form** for items expected to receive lifecycle writes. It is round-trip-stable mechanistically (same js-yaml quoting heuristic that preserves the corrupted plain-quoted form). Phase 5 VERIFY of P53 includes a wiki-link-CSV regression gate to catch any future Obsidian version drift.
- **Static items (policies, ADRs, specs)** that do NOT receive lifecycle writes can use the plain canonical form `actors: [a, b, c]` without concern.

After P56 Phase 4 lands, the targeted-field patcher will preserve any source style, and the plain canonical form becomes universally safe. AYML-001 (joint policy with P56) governs the full discipline.

### 13.5 Resolution Lookup Chain (CQRS-002 D6)

When the CQRS hook resolves the `allowedActors` set for a write, it walks this chain (most-specific to least-specific) and unions all hits:

1. **Inbox item's own `actors`** — the work item file being written, if it has `actors:`.
2. **Parent `*.team.md` `actors`** — the team spec referenced by the inbox item's `assigned_team`, or the project-default team.
3. **Parent `P{ID}-Master.md` `actors`** — the project-master tracker for the inbox item's `project`.
4. **Legacy `assigned_role` + `assigned_roles`** on the inbox item itself — fallback for items not yet migrated to `actors`.

This chain matches the LR-TEAM-001 team-spec lookup order (spec → work-item → inbox-item → inbox-master → project).

### 13.6 OR-Gate Resolution Semantics (CQRS-002 D3)

The four lookup-chain hits union into one `allowedActors` set. An incoming agent is authorized if **any one of**:

- The agent's ID matches an entry, OR
- The agent's role matches an entry, OR
- Any role in the agent's `stacked_roles` matches an entry.

Items with no `actors` declaration still grant write access to whoever appears in `assigned_role(s)` — no regression for legacy items.

### 13.7 Authoring Guidance

**For single-role work items:** declaring `assigned_role` alone is sufficient (legacy fallback applies). Adding `actors` is optional but documents intent explicitly.

**For multi-role work items (architect + developer + vault-maintainer pairings):** declare `actors` explicitly on the inbox item OR on the parent `*.team.md`. Prefer the team-spec when the same roster applies to many items in the project.

**For team-spec files (`*.team.md`):** always declare `actors` as the canonical roster. Child inbox items may override or extend.

**For master tracker files (`P{ID}-Master.md`):** declare `actors` as the project-default roster. This unblocks bookkeeper writes (vault-maintainer) on any project branch even when the working inbox item lacks `actors`.

### 13.8 Cross-References

- [[CQRS-002-actors-field|CQRS-002]] — Phase 1 ADR (S242). Authoritative source for D1-D10 decisions, identity-fix design (H2 layered), label-collision resolution (D9), Phase 2-6 handoff notes.
- [[CQRS-001-write-isolation|CQRS-001]] §C — parent write-isolation policy. The former CQRS-002 queue label is absorbed into CQRS-001-C per D9 (Phase 3 string change, not yet shipped).
- AYML-001 (Phase 2 joint policy with P56) — vault-wide YAML handling discipline; declares per-runtime parser allowlist and targeted-patcher contract for lifecycle writes.
- FMM-001 (P56 Phase 2 ADR) — frontmatter serialization contract; ships the targeted-field patcher in Phase 4 that resolves D2b's interim caveat.
- `.claude/roles/hooks/pre-tool-use/actor-resolver.js` — module implementing D1-D4, D6-D8 (after Phase 3 lands).

---

## 14. Token Threshold Schema (`token_threshold`)

The `token_threshold` field defines the **percentage thresholds of an agent's model context-window** at which context-injection hooks (P30-W4 `inject-token-warning` and downstream consumers) emit warnings. It is a cross-cutting Optional field — declarable on inbox items, project-master trackers, agent profiles, role profiles, and as a global default — that resolves through a five-level precedence chain.

### 14.1 Canonical Schema

```yaml
token_threshold:
  warn: 70       # int 0-100, percentage of model context limit
  urgent: 85    # int 0-100
  emergency: 95 # int 0-100
```

**Rules:**

1. YAML mapping with three integer keys: `warn`, `urgent`, `emergency`.
2. Each value is an integer in `[0, 100]` representing a percentage of the agent's model context window (resolved from `.claude/models.yaml`).
3. Ordering invariant: `warn ≤ urgent ≤ emergency`. Hooks that detect a violation log a WARN and fall back to the next-precedence-level value for the offending key.
4. Block-style mapping (`key: value` on separate lines) is canonical. Flow style (`{warn: 70, urgent: 85, emergency: 95}`) is accepted on read but not preferred — block form survives YAML round-trip without quoting drift.
5. Partial overrides are allowed — see §14.4.

### 14.2 Where to Set

The field can be declared at any of five levels. The canonical home depends on scope.

| Level | Location | Use when |
|-------|----------|----------|
| **Inbox item** (most specific) | `00_Inbox/P{XX}-Pipeline/p{XX}-w{N}-*.md` frontmatter | This particular work item is unusually long-running or context-heavy and needs different thresholds than its project peers. |
| **Project master** | `00_Inbox/P{XX}-Pipeline/P{XX}-Master.md` frontmatter | All work items in this project should share thresholds different from the agent / role default (e.g., research-heavy projects raise `warn` to 80). |
| **Agent profile** | `.claude/agents/{name}.md` frontmatter | A specific agent (e.g., `worker-coordinator` with known tool-output bloat) needs lower thresholds than its role default. |
| **Role profile** | `.claude/roles/{name}/profile.yaml` | All agents inheriting a role share thresholds (e.g., `architect` role at 75/85/95 because architectural reasoning is bursty). |
| **Global default** (least specific) | Hardcoded in `inject-token-warning` hook | Vault-wide fallback — `{warn: 70, urgent: 85, emergency: 95}`. |

**Note:** team-spec files (`*.team.md`, §2.9) are NOT a precedence level for `token_threshold`. Token usage is per-agent, not per-team; thresholds attach to agent identity (role / agent / project assignment), not to team membership.

### 14.3 Precedence Resolution

Hooks resolve the effective `token_threshold` for an agent at runtime by walking from most-specific to least-specific and **first-hit-per-key wins**:

1. The agent's currently-claimed inbox item's `token_threshold` (from the work order)
2. The inbox item's project-master `token_threshold`
3. The agent's `.claude/agents/{name}.md` frontmatter `token_threshold`
4. The agent's role's `profile.yaml` `token_threshold`
5. Hardcoded default `{warn: 70, urgent: 85, emergency: 95}`

Resolution is **per-key**, not per-object — see §14.4. This matches the team-spec lookup pattern in §13.5 (Actors Field) and the `phase_roles` lookup pattern in §2.9 (Team File).

### 14.4 Partial Overrides

A declaration MAY include only the keys it wants to override. Missing keys fall through to the next precedence level for that key alone.

**Example — agent profile lowers only `warn`:**

```yaml
# .claude/agents/worker-coordinator.md
token_threshold:
  warn: 60   # earlier warning because tool-output bloat is well-known
  # urgent + emergency inherit from role / global
```

At runtime the resolved threshold for a `worker-coordinator` agent (no inbox-item or project-master override) becomes `{warn: 60, urgent: 85, emergency: 95}`.

**Validation:** if a partial override produces an out-of-order tuple (e.g., agent sets `warn: 90` while a project-master sets `urgent: 85`), the hook logs a WARN and demotes the offending key to the next-lower-precedence value that preserves ordering. Hard `BLOCK` is reserved for invalid types (non-integer, out of `[0, 100]`).

### 14.5 Where Token Limits Come From

The percentages in `token_threshold` are applied to each agent's **model context limit**, not to a fixed token count. Model context limits are the single source of truth in `.claude/models.yaml` (per LR-MDL-002). The hook reads the agent's resolved model and computes:

```
effective_limit = model.context_tokens
warn_at         = effective_limit * (token_threshold.warn / 100)
urgent_at       = effective_limit * (token_threshold.urgent / 100)
emergency_at    = effective_limit * (token_threshold.emergency / 100)
```

This means the same `token_threshold: {warn: 70, ...}` produces different absolute warn-at-token-counts for opus (1M ctx) vs. sonnet (200k ctx) vs. haiku — exactly the desired behavior.

### 14.6 Authoring Guidance

**For most work items:** do not declare `token_threshold`. Rely on the role profile or global default. Adding the field everywhere creates noise and dilutes the signal of intentional overrides.

**Declare on the inbox item** when this specific work item is known to consume context atypically (large semantic searches, broad codebase exploration, tool-output bloat).

**Declare on the project master** when the project itself has a different "shape" than its host role (e.g., a documentation project run by `developer` agents wants higher `warn` because reasoning passes are short).

**Declare on the agent profile** when one agent variant differs from its peers (e.g., `worker-coordinator` historically over-consumed; thresholds tuned lower based on observed S247 telemetry).

**Declare on the role profile** when the role itself has a characteristic context-consumption pattern (e.g., `architect` role values longer reasoning chains and tolerates higher `warn`).

**Avoid declaring at multiple levels for the same item** unless you intentionally want partial-override resolution (§14.4). When in doubt, pick the most-specific level that captures the intent and let lower levels remain silent.

### 14.7 Cross-References

- `00_Inbox/P30-Continuous-Improvement-Loop/p30-w4-inject-token-warning-hook.md` — implementation work item (S247 task #23).
- INJ-001 (forthcoming policy at P30-W2 Phase 5) — context-injection policy that mirrors this schema for hook-side enforcement.
- LR-MDL-002 — model SSOT at `.claude/models.yaml` (provides per-model `context_tokens`).
- P25-W20 (cartographer) — token-consumption telemetry that informs threshold tuning.

---

## Cross-References

- **Note types and operations**: Invoke `vault-notes` for PARA structure and common tasks
- **Template specifications**: Invoke `vault-templates` for full template key fields and sections
- **Process inbox prompt**: `00_Inbox/.prompts/process-inbox.prompt.md`
- **Doc-specialist rubrics**: `.claude/roles/doc-specialist/rubrics/` — validate against vault-metadata schemas

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 3.6.0
last_updated: "2026-04-29"
source: P56-W1 canonical schema definitions + P56-W4 gap resolution + P30-W2/W4 context-injection
change_surface: Per-type schemas, consumer maps, auto-managed field ownership, file conventions
extension_points: New PARA types (add to Section 2), new consumers (add to Section 7), new conventions (add to Section 11)
changelog:
  - "1.0.0: Initial extraction from CLAUDE.md"
  - "2.0.0: P56-W1 canonical PARA frontmatter definitions — 8 PARA types + 4 additional types, assigned_role + assigned_team fields, Team File spec, consumer field map, auto-managed field ownership, Dataview query patterns"
  - "2.1.0: P56-W4 gap resolution — session_date + branch (inbox session-notes variant), title + updated + domain + enforcement values (policy schema), context-packet + prompt type schemas, *.spec.md + *.team.md conventions, schema ownership model (Section 12), policy/context-packet/idea status values (Section 4)"
  - "2.2.0: P56-W4 amendment — phase_roles schema for team files (default role matrix + lookup chain), domain elevated to cross-cutting Optional field (workflow routing, execution tiers)"
  - "3.1.0: Add policy_refs Optional field to type:project schema, add type:design schema (14 existing notes), register design in Type Values and Status Values"
  - "3.2.0: Add target_roles Optional field to policy schema — compliance testing infrastructure (S216 policy audit)"
  - "3.4.0: P53 Phase 2 SKILL-UPDATE (S243) — add actors field as cross-cutting Optional field (§1 + §2.1 inbox + §2.9 team-file), add §13 Actors Field — CQRS Authorization Roster (D1 distinction matrix + D2 canonical flow-array + D2b round-trip caveat + D3 OR-gate + D6 lookup chain + authoring guidance). Per CQRS-002 ADR (S242 P53 Phase 1)."
  - "3.5.0: S244 Critical Cross-Cutting Blockers fix — add enrichments_disabled (P66), vca_disabled + applies_policies + relevant_tools + process_chain + related_skills (P67), phase_advanced_at + phase_advanced_by + phase_blocked_by + auto_pilot_disabled + priority_weight + phase_dispatch_in_flight (P68). Collapse canonical_phase into phase. Add 'archive' value to phase enum."
  - "3.6.0: S247 — token_threshold cross-cutting Optional field (warn/urgent/emergency percentages) added to §1 Shared Base Fields, §2.1 Inbox, §2.9 Project Master. New §14 Token Threshold Schema with 5-level precedence chain (inbox-item > project-master > agent profile > role profile > global default), partial-override semantics, model-context resolution via .claude/models.yaml. Consumers: P30-W4 inject-token-warning hook + INJ-001 policy (forthcoming P30-W2 Phase 5)."
```
