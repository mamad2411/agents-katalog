---
name: sdd-arch
description: 'Create or update the shared architecture document — select tech stack, define API patterns, establish naming conventions, map project structure, and record architectural decisions with rationale. Use when designing system architecture, making technical decisions, or updating the architecture doc. Do not use for implementing features, writing PRDs, or designing UX.'
---

Create or update the shared architecture document at `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md`.
This is a **shared project document** — not tied to any specific change. It defines HOW the system is built and serves as context for all future changes.

**Output**: `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md`

**Template**: Use `assets/architecture.md` as the document structure.

**Prerequisites**: `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` should exist. If not, ask user for a prd or suggest to "Create the PRD"


> [!IMPORTANT]
> This skill is designed to be used with the **sdd-team:sdd-architect.agent** agent.
> Switch to it in the agent selector before invoking this skill for the full interactive experience.
> If you are already using **sdd-team:sdd-architect.agent**, proceed with the workflow below.

---

## Entry point

1. **Check if architecture doc already exists**

   Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` or any file provided by the user. If it exists:
   - Summarize current content to the user.
   - Ask: "Do you want to **revise** the existing architecture or **start fresh**? Skip this question if you detect from existing document or user input.
   - If revise → follow **Edit Architecture Workflow** below.
   - If fresh → follow **Architecture Workflow** below.

2. **Context gathering** (always)
   - Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` if it exists — primary requirements baseline.
   - Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md` if it exists — UX implications.
   - Read any additional files provided by the user (e.g., `project-context.md`, `AGENTS.md`) for technical preferences or constraints.
   - Read project-level docs (README, package.json, `AGENTS.md`, etc.).
   - Ask the user for additional context if needed.

---

## Architecture Workflow

Collaborative, step-by-step creation of architecture decisions that ensure consistent implementation.

### Step 1 — Context gathering

1. If no docs were found, ask: _"Any PRD, UX specs, research docs, or project context files to load?"_
2. Read all provided files fully.
3. **If no PRD is available:** gather requirements directly from the user via chat. Ask about: project goals, target users, core features, technical constraints, NFRs (performance, security, scale), and existing tech preferences. Use the answers as the requirements baseline.
4. Look for existing technical preferences in `project-context.md`, `AGENTS.md`, etc.
5. Confirm gathered context with user before proceeding.

Output: `✅ Context loaded — ready to architect.`

### Step 2 — Project context analysis

Analyze loaded documents for architectural implications:

1. **Requirements analysis:** Extract FRs, NFRs (performance, security, compliance), technical constraints.
2. **Scale assessment:** Real-time needs, multi-tenancy, regulatory, integration complexity, data volume.
3. **UX implications** (if UX spec provided): component complexity, animations, real-time updates, offline needs, accessibility level.

Present analysis back to user for validation — core functionality summary, critical NFRs, scale indicators, cross-cutting concerns. Ask: _"Does this match your understanding?"_

### Step 3 — Starter template evaluation

1. Check project context for existing tech preferences (languages, frameworks, databases, platforms).
2. Ask about remaining preferences: team experience, deployment targets, integrations.
3. Research current starter / scaffolding options for the project type.
4. For each viable option, analyze: tech decisions it makes, patterns it establishes, dev experience features.
5. Present options with trade-offs (adapt depth to user skill level). Get user's choice.
6. Document: chosen starter, inherited tech decisions, CLI commands to scaffold.

### Step 4 — Core architectural decisions

Facilitate decisions across these categories (skip what's already decided by starter/preferences):

- **Data architecture:** database, modeling approach, validation, migrations, caching
- **Auth & security:** authentication method, authorization patterns, encryption, API security
- **API & communication:** design patterns (REST/GraphQL), error handling standards, rate limiting
- **Frontend** (if applicable): state management, component architecture, routing, performance
- **Infrastructure:** hosting, CI/CD, environment config, monitoring, scaling

For each decision: present options with trade-offs, get user input, verify current versions, record choice with rationale.

> **Decision record format** (for each item in `architecture.md`):
> ```
> | Decision | Choice | Rationale |
> |---|---|---|
> | Database | PostgreSQL (Supabase) | Team familiarity, built-in auth, real-time subscriptions |
> | Auth | Supabase Auth (JWT) | Free tier, social providers, row-level security |
> | API style | REST + tRPC | Type-safe client, auto-generated TS types |
> ```

### Step 5 — Implementation patterns & consistency rules

Define patterns to prevent implementation conflicts:

- **Naming:** database tables/columns, API endpoints, files, components, variables
- **Structure:** test locations, component organization, utilities, config files
- **Formats:** API response wrappers, error structures, date formats, JSON field casing
- **Communication:** event naming, state update patterns, logging formats
- **Processes:** error handling, loading states, retry logic, validation timing

For each area: present options, get user decision, document the chosen convention.

### Step 6 — Project structure & boundaries

1. Map requirements/epics to architectural components.
2. Generate complete project directory tree (real files and folders — no generic placeholders).
3. Define integration boundaries: API boundaries, component boundaries, data access patterns.
4. Present structure, get user confirmation.

### Step 7 — Validation

Run coherence checks on the complete architecture:

- **Decision compatibility:** all tech choices work together, versions compatible, no contradictions.
- **Requirements coverage:** every FR/NFR has architectural support.
- **Implementation readiness:** decisions complete enough for agents to implement consistently.
- **Gap analysis:** identify critical / important / nice-to-have gaps.

Present findings. Resolve critical issues with user before completing.

### Step 8 — Completion

1. Save final `architecture.md` to `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` using the template structure.
2. Present a **completion recap in chat**: decisions made, patterns defined, structure finalized, gaps found.

---

## Edit Architecture Workflow

Structured improvement of an existing architecture document.

### Step 1 — Discovery

1. Load `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` completely.
2. Ask: _"What would you like to change?"_ Examples:
   - Update technology choices (new framework version, different database, etc.)
   - Add missing architectural decisions or patterns
   - Refine project structure or boundaries
   - Incorporate new requirements from updated PRD/UX specs
   - Fix inconsistencies or gaps identified during implementation
3. If user provides updated spec files (PRD, UX, epics), load them fully to understand the delta.

### Step 2 — Impact analysis & change plan

1. Read the entire architecture document thoroughly.
2. Analyze requested changes for ripple effects:
   - **Decision compatibility:** does the change conflict with existing decisions?
   - **Pattern impact:** do naming conventions, error handling, or other patterns need updating?
   - **Structure impact:** does the project directory tree need changes?
   - **Downstream effects:** will this break existing implementations or require migration?
3. Build change plan: section-by-section list of what needs updating, priority (Critical/High/Medium/Low), estimated ripple effects.
4. Present change plan to user. Get approval before proceeding.

### Step 3 — Apply edits

1. Follow approved change plan systematically, section by section.
2. For each change: load current section → apply modification → verify consistency with rest of document.
3. **Verify current technology versions** for any tech stack changes — never trust hardcoded versions.
4. Ensure cross-references remain valid (if a pattern changes, update all sections that reference it).
5. Show progress after each major section update.
6. Final coherence check: re-run Step 7 of the Architecture Workflow on the updated document.

### Step 4 — Completion

1. Apply all edits directly to `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md`.
2. Present a **completion recap**: sections modified, decisions changed, new patterns/conventions, consistency check results.

---

## Tracker Update

After saving `architecture.md`, follow the **`sdd-tracker` skill** — update `shared.architecture` and changelog (only if architecture was revised, not for new documents).

---

## Guardrails

{SKILL_ASSETS_NOTICE}
- **Adopt Architect's persona** — from: `agents/architect.agent.md`
- **Never modify PRD or UX docs** — output goes into `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` only.
- **Always validate with user** before recording architectural decisions.
- **Verify technology versions** — never trust hardcoded versions.
- **No time estimates.**
