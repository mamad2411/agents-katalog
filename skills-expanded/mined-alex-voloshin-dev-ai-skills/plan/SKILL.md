---
name: plan
description: Plan feature implementation across services and roles — parse requirements, understand project architecture (`ARCHITECTURE.md`, `AGENTS.md`), decompose into work packages per service/role, estimate complexity, produce an actionable implementation plan. Part of the umbrella feature workflow. Includes mandatory multi-reviewer feedback loop with product-manager, solution-architect, and system-architect.
context: fork
argument-hint: [PRD or feature brief path]
---

# Feature Plan

Plan a feature implementation by understanding the project architecture, decomposing work into service-level and role-level packages, and producing an actionable plan. This is the **planning phase** — no code is written here. Output feeds into `feature-dev` skill for execution.

## 1. Receive Feature Requirements

Gather the feature specification from the user:

- **Accepted formats**: PRD, ARD, design doc, implementation plan, ticket/issue, verbal description
- Read every provided document thoroughly
- Extract and organize:
  - **Goal**: What the feature does (1–2 sentences)
  - **Requirements**: Functional (what it does) and non-functional (performance, security, compliance)
  - **Acceptance criteria**: How to verify the feature works
  - **Constraints**: Deadlines, compatibility, dependencies on other teams/services
  - **Out of scope**: What this feature explicitly does NOT cover

If the specification is ambiguous or incomplete — ask before proceeding. Do not assume missing requirements.

## 2. Understand Project Architecture

Read and internalize the project's structure to plan correctly:

### 2a. Read Architecture Documentation

Read the following files (if they exist):

1. **`ARCHITECTURE.md`** — system overview, component boundaries, data flow, service map
2. **`AGENTS.md`** (root) — tech stack declaration, project structure, conventions
3. **Subdirectory `AGENTS.md` files** — per-service/module context and stack info

**Extract**:
- Service/module boundaries (monolith modules, microservices, frontend/backend split)
- Tech stack per service (language, framework, database, messaging)
- Communication patterns (REST, gRPC, events, shared DB)
- Data flow relevant to the feature
- Deployment topology (monorepo vs polyrepo, shared vs independent deploys)

### 2b. Scan Project Structure

If documentation is incomplete or absent, scan the filesystem:

```
// turbo
ls -la (or dir for Windows)
```

Look for:
- **Monorepo signals**: `packages/`, `services/`, `apps/`, root `package.json` with workspaces, Nx/Turborepo config
- **Polyrepo signals**: Single service, one `AGENTS.md`, one tech stack
- **Infrastructure**: `terraform/`, `infra/`, `k8s/`, `helm/`, `docker-compose.yml`
- **Dependency files**: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `*.csproj` per service

### 2c. Build Service Map

Create a map of services/modules the feature touches:

```
## Service Map

| Service/Module | Tech Stack | Role | Affected by Feature |
|---|---|---|---|
| [name] | [lang + framework] | `role-id` | [yes/no — how] |
| [name] | [lang + framework] | `role-id` | [yes/no — how] |
| infrastructure | Terraform / K8s | `devops-engineer` role | [yes/no — how] |
```

## 3. Decompose into Work Packages

Break the feature into **work packages** — each package is a self-contained unit of work scoped to one service/module and one role.

### 3a. Identify Work Streams

Group changes by responsibility:

| Work Stream | Role | Scope |
|---|---|---|
| **Frontend** | `frontend-engineer` role | UI components, pages, client-side logic, API integration |
| **Backend API** | `java-engineer` role / `python-engineer` role | Endpoints, business logic, data access, validation |
| **Data Layer** | `db-engineer` role | Database schema, migrations, queries, indexing, optimization |
| **Infrastructure** | `devops-engineer` role | Terraform, Docker, K8s, config, secrets |
| **Cloud Architecture** | `cloud-architect` role | Cloud platform design, landing zones, networking, cost optimization |
| **CI/CD Architecture** | `devops-architect` role | Pipeline design, deployment strategy, GitHub org governance, platform engineering |
| **ML / Data** | `ml-engineer` role | Models, pipelines, feature engineering. For LLM/RAG/agent features also consult `context-engineering` skill |
| **Data Pipelines** | `data-engineer` role | ETL/ELT, data warehousing, Spark, dbt, Airflow |
| **Mobile** | `mobile-engineer` role | React Native, Flutter, iOS, Android apps |
| **Marketing Content** | `marketing-strategist` role | Positioning, messaging, GTM, landing pages |
| **Architecture** | `system-architect` role | System design, ARCHITECTURE.md, component boundaries, tech selection |
| **Cross-cutting** | `software-engineer` role | Shared libraries, contracts, API specs |

Only include work streams that the feature actually requires. Do not add empty streams.

### 3b. Define Work Packages

For each work stream, create ordered work packages:

```
### [Work Stream]: [Service Name] — `role-id`

#### WP-[N]: [Title]
- **Description**: What to implement
- **Files**: Expected files to create/modify
- **Dependencies**: Which WPs must complete first
- **Acceptance criteria**: How to verify this WP is done
- **Complexity**: S (hours) / M (day) / L (days) / XL (week+)
```

**Rules for decomposition**:
- Each WP is independently testable
- WPs within a stream are ordered by dependency (foundations first)
- Cross-service dependencies are explicitly marked
- Database migrations always come before code that uses them
- API contracts defined before consumer implementation

### 3c. Define Integration Points

For features spanning multiple services, explicitly document:

<integration_points>
- **API contracts**: Request/response schemas for new or modified endpoints
- **Events/messages**: New event types, payload schemas, producers, consumers
- **Shared types**: DTOs, enums, or constants shared across services
- **Database changes**: Schema migrations, new tables/columns, index requirements
- **Configuration**: New env vars, feature flags, secrets needed
</integration_points>

## 4. Dependency Graph

Visualize the execution order:

```
## Dependency Graph

WP-1: [DB migration]
  └─► WP-2: [Backend API]
        ├─► WP-3: [Frontend integration]
        └─► WP-4: [Infrastructure/config]
WP-5: [Tests] ← depends on WP-2, WP-3
```

Identify:
- **Critical path**: Longest chain of dependent WPs — determines minimum timeline
- **Parallelizable**: WPs that can be worked on simultaneously by different roles
- **Blockers**: External dependencies (other teams, third-party APIs, approvals)

## 5. Risk Assessment

Evaluate risks for each work stream:

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| [risk description] | High/Med/Low | High/Med/Low | [mitigation strategy] |

**Common risks to evaluate**:
- Breaking changes to existing APIs (backward compatibility)
- Database migration on large tables (performance, downtime)
- Cross-service coordination (deployment order matters)
- New dependencies or services (operational complexity)
- Security implications (new auth flows, data exposure)

## 6. Present the Plan

Compile the full plan and present to the user:

```
# Feature Plan: [Feature Name]

## Goal
[1–2 sentences]

## Architecture Impact
- Services affected: [list]
- New services: [if any]
- Database changes: [yes/no — summary]
- Infrastructure changes: [yes/no — summary]

## Work Packages

### Stream 1: [name] — `role-id`
| WP | Title | Complexity | Dependencies | Status |
|----|-------|------------|--------------|--------|
| WP-1 | [title] | M | — | planned |
| WP-2 | [title] | S | WP-1 | planned |

### Stream 2: [name] — `role-id`
| WP | Title | Complexity | Dependencies | Status |
|----|-------|------------|--------------|--------|
| WP-3 | [title] | L | WP-1 | planned |

## Critical Path
WP-1 → WP-2 → WP-5 (estimated: [timeframe])

## Risks
[table from Step 5]

## Next Step
Run `feature-dev` skill per work package, applying the designated role.
```

Wait for user approval. The user may reorder, split, merge, or remove work packages.

## 7. Multi-Reviewer Feedback Loop

The Feature Plan MUST pass a mandatory multi-reviewer cycle before handoff. Do not update `FEATURES.md` or hand off to the `feature-dev` skill until every reviewer returns `approved`.

### Reviewer Panel

Apply each role below in sequence, treating each as an independent reviewer with its own pass over the plan:

- `product-manager` role — scope alignment with the PRD, WP coverage of acceptance criteria, risk coverage, correct prioritization, missing requirements
- `solution-architect` role — end-to-end design coherence, integration points, API contracts, cross-service coordination, tech stack fit per WP, non-functional requirements coverage
- `system-architect` role — system boundaries, component topology, data flow, `ARCHITECTURE.md` consistency, scalability and deployment implications of the WP decomposition

### Cycle

1. For each role, produce a findings report: Critical (must fix), Major (should fix, justify if waived), Minor (optional), plus an explicit verdict: `approved` / `approved-with-changes` / `rejected`. Keep reports separate per role
2. Collect all three reports before editing
3. Apply all actionable findings to the plan (re-scope WPs, adjust dependencies, add missing streams, revise complexity). Resolve conflicts with priority Critical > Major > Minor; on ties, system-architect > solution-architect > product-manager. Record waivers with a one-line rationale
4. Re-run the same three reviewer passes against the updated plan
5. Loop until every reviewer returns `approved` with zero remaining critical/major findings

Termination: pass when all three are `approved`. On divergence (findings not shrinking, mutually exclusive asks) — pause and ask the user to arbitrate. Max 5 cycles before escalation.

Record the review history at the bottom of the plan as a `## Review History` section listing each cycle's reviewer verdicts and open issue counts.

## 8. Update FEATURES.md

After the plan is approved, **apply `product-manager` role** and update `FEATURES.md`:

1. If `FEATURES.md` does not exist — create it at the project root
2. Add or update the feature entry with status `planned`
3. If the feature has a PRD or spec — save it in `features/` directory and link from `FEATURES.md`

## 9. Handoff to Implementation

After approval, guide execution:

- **Sequential** (single developer): Execute WPs in dependency order using `feature-dev` skill for each
- **Parallel** (multiple developers/sessions): Assign independent WPs to separate sessions, each applying the appropriate role
- Track WP status: `planned` → `in_progress` → `done`
- Update the plan if scope changes during implementation

## Integration

- **Input**: PRD, ARD, design doc, or user request
- **Preceded by**: `product` skill (produces PRD), `architecture` skill (produces ARD, design docs, API contracts, engineering estimates)
- **Followed by**: `feature-dev` skill (implementation per work package)
- **Roles**: `product-manager` role (requirements; Step 7 reviewer), `solution-architect` role + `system-architect` role (architecture; Step 7 reviewers), `cloud-architect` role (cloud platform), `devops-architect` role (CI/CD architecture), stack-specific roles (work packages)
- **Skills**: `context-engineering` skill (context pipeline design, RAG, memory, agent harness — for AI/LLM feature work packages)
