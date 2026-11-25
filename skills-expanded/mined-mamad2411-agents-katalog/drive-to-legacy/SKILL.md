---
name: drive-to-legacy
description: Use when exploring, studying, or porting an unfamiliar legacy codebase. Triggers when the user says "explore this project", "understand this code", "I need to port this", "how does this app work", "document this codebase", "study this code", or any request to deeply understand an existing project they did not write. Also triggers when onboarding to a new repo or preparing migration/rewrite plans.
effort: max
---

# Drive to Legacy - Systematic Legacy Code Exploration

## Overview

A 6-phase systematic approach to fully understand an unfamiliar codebase, producing a comprehensive architecture document with mermaid diagrams that both humans and AI can use for porting, migration, or onboarding.

**Core principle:** Explore wide before deep. Map the full territory first, then drill into each layer. Every finding goes into a living ARCHITECTURE.md with diagrams.

## When to Use

- Onboarding to an unfamiliar codebase
- Preparing to port or rewrite an application
- Documenting a legacy system that lacks documentation
- Studying code you need to maintain but did not write
- Any "how does this work?" question about a full project

**When NOT to use:**
- Small bug fixes in code you already understand
- Greenfield projects (no legacy to explore)
- Single-file scripts or utilities

## The 6 Phases

Follow these phases in order. Each phase builds on the previous. Use parallel Explore agents where possible to speed up discovery.

### Phase 1: User Stories

**Goal:** Describe WHAT the app does from the user's perspective. This comes first because it answers "why does this app exist?" — the context that makes all technical details meaningful.

1. Read `package.json` / `README.md` to understand the app's purpose
2. Read entry points and main container components to identify the UI flow
3. Walk through component render methods to find every user action
4. Trace each action to its handler and side effects
5. Note conditional paths (different behavior for different roles or data states)

**Write to ARCHITECTURE.md:**
- Section: "User Stories" with one subsection per story
- Each story: user story statement + mermaid `sequenceDiagram` showing the interaction

**Template per story:**
```markdown
### US-XX: Story Title

AS A [role]
I WANT TO [action]
SO THAT [outcome]

(mermaid sequence diagram)
```

### Phase 2: Project Identity and Component Map

**Goal:** Know the tech stack, file layout, and component tree.

1. Read build config (`vite.config.ts`, `webpack.config.js`, `tsconfig.json`, etc.)
2. List the top-level directory structure
3. Glob for all source files to see the shape: `**/*.tsx`, `**/*.ts`, `**/*.vue`, etc.
4. Read each main component/module entry point (not every file, just the key ones)
5. Trace the component hierarchy from root down
6. Identify reusable/shared components vs. page-specific ones

**Write to ARCHITECTURE.md:**
- Section: "What This App Does" (3 sentences max)
- Section: "Tech Stack and Key Dependencies" (bullet list)
- Section: "File-to-Responsibility Map" (tree with one-line descriptions)
- Section: "Component Hierarchy" (mermaid `graph TD` diagram)
- Section: "State Management Overview" (mermaid diagram showing where state lives)

### Phase 3: Data Model

**Goal:** Understand every entity, type, and relationship.

1. Read all type/interface/model files
2. Read the service/API layer to find all entities referenced
3. Map relationships between entities (foreign keys, lookups, joins)
4. Identify choice/enum fields and their values

**Capture:**
- Every TypeScript interface / database model / API schema
- Entity relationships (one-to-many, many-to-many)
- Key constants and magic numbers with their meanings

**Write to ARCHITECTURE.md:**
- Section: "CRM/Database Entity Relationship Diagram" (mermaid `erDiagram` with field lists)
- Section: "Key Constants and Option Set Values" (table)

### Phase 4: Business Logic

**Goal:** Extract every rule, validation, cascade, and conditional behavior.

This is the deepest phase. Read line by line through:
1. **Form validation rules** - what is required, when, why
2. **Field cascade logic** - selecting A resets B, populates C
3. **Conditional rendering** - what shows/hides and when
4. **Data transformation** - how input maps to output on save
5. **Silent fallbacks** - what happens when data is missing (nullability chains)

**Write to ARCHITECTURE.md:**
- Section: "Business Logic and Rules" with subsections for each rule domain
- Use mermaid `flowchart TD` for decision trees
- Use tables for validation rules and field mappings
- Include a "Nullability and Silent Fallbacks" table (what can be undefined and what happens)
- Include an "Auto-Population Rules" section (what triggers auto-fill of which fields)

### Phase 5: API Reference

**Goal:** Document every data query with exact parameters, filters, joins, and purpose.

**CRITICAL RULE: Every API endpoint MUST have a Why row.** The Why explains the business reason the data is needed - not just "fetches X from Y" but why the application cannot function without this call. Without Why, a developer porting the code cannot tell which APIs are essential vs. nice-to-have, or what would break if the API were removed or changed.

For each service method / API call:
1. Read the exact query (SQL, FetchXml, OData, GraphQL, REST URL)
2. Document parameters, entity, joins, filters
3. Note when it is called and by which component
4. **Explain WHY it exists** (business purpose, not just technical description)

**The Why row must answer:** "What business goal does this query serve? What breaks or becomes impossible without it?"

**Good Why examples:**
- "Populates dropdown options so the form can render selectable choices. These are CRM choice-column labels, not hardcoded."
- "Finds the pre-defined stock item (inventory lane) for a customer + make between POL/POD ports. Links cargo to inventory forecasting."
- "Determines which other schedules can carry cargo onward. Same vessel for Cross, different vessel for Transshipment."

**Bad Why examples:**
- "Fetches data from the database" (too vague, says nothing about business purpose)
- "Called when user clicks save" (that's When, not Why)
- "Returns a list of records" (describes what, not why)

**Write to ARCHITECTURE.md:**
- Section: "API Reference" with one subsection per endpoint
- Each endpoint gets a properties table with **Why always after When**:

| Property | Value |
|----------|-------|
| **Called by** | Component or function name |
| **API method** | The actual call pattern |
| **Entity** | Table/endpoint queried |
| **Parameters** | Input values |
| **When** | Trigger condition |
| **Why** | Business reason this data is needed |

- Include the exact query (SQL/FetchXml/GraphQL) in a code block
- Include a mermaid join diagram for complex multi-table queries
- End with an "API Call Map by User Action" (mermaid flowchart showing which APIs fire on which user action)

**Also document inline queries** - queries defined inside components (not just in the service layer). These are easy to miss.

### Phase 6: Build and Deploy

**Goal:** Know how to run, build, and ship.

1. Read build scripts and CI/CD config
2. Read deployment scripts or docs
3. Note environment-specific configs

**Write to ARCHITECTURE.md:**
- Section: "Build and Deploy Pipeline" (mermaid `graph TD` from dev to production)
- Section: "LookupFieldInput / Reusable Components" (document non-obvious reusable patterns)

## ARCHITECTURE.md Structure

The final document should follow this reading order (user stories first — they answer "why does this app exist?" and make everything else meaningful):

```
# Project Name - Architecture Reference

> One-paragraph summary

## Table of Contents (clickable anchor links)

(overview Mermaid diagram here — the convention's mandatory document thumbnail)

## Part 1: User Stories
  - One subsection per story with sequence diagrams

## Part 2: Overview and Project Structure
  - What This App Does
  - Tech Stack and Key Dependencies
  - File-to-Responsibility Map
  - Key Constants and Option Set Values
  - Component Hierarchy (diagram)
  - Entity Relationship Diagram
  - State Management Overview (diagram)

## Part 3: Application Flow
  - Bootstrap / initialization sequence
  - Main user flows as sequence diagrams
  - Save / submit flow

## Part 4: Business Logic and Rules
  - Subsection per rule domain with flowcharts
  - Validation rules
  - Cascade logic
  - Conditional rendering rules
  - Auto-population rules
  - Nullability and silent fallbacks

## Part 5: Data Model and Field Mapping
  - TypeScript-to-database field mapping (diagram)
  - Conditional field mapping rules

## Part 6: API Reference
  - Overview of query patterns used
  - One subsection per endpoint (properties table + exact query + why)
  - Inline component queries
  - API call map by user action (diagram)

## Part 7: Technical Components
  - Reusable components worth understanding
  - Build and deploy pipeline
```

## Rules for the Architecture Document

1. **Clickable TOC** - every section linked with anchor. Avoid `&`, `--`, `/`, `*`, `()` in headings (they break anchor generation).
2. **Mermaid diagrams everywhere** - sequence diagrams for flows, flowcharts for logic, ER diagrams for data, graph TD for hierarchies. This implements the marketplace diagram convention (`references/diagram-convention.md`) — including its mandatory overview diagram at the top of the document.
3. **Every API table must have a Why row** - business purpose, not just technical trigger.
4. **Tables for scannable data** - validation rules, field mappings, constants, nullability.
5. **No speculation** - only document what you read in the code. If behavior is unclear, note it as unclear.
6. **Horizontal rules (`---`) between Parts** for visual separation.

## Parallel Exploration Strategy

Use multiple Explore agents in parallel to speed up Phase 1-3:

```
Agent 1: Read entry points, config, types, UI flows → Phase 1 + Phase 2
Agent 2: Read all types, service layer, entity references → Phase 3
Agent 3: Read service layer, extract all queries → Phase 5
```

Then do Phase 4 (business logic) sequentially — it requires understanding from all previous phases.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting with business logic before understanding structure | Follow phases in order. Phase 1-3 first. |
| Missing inline queries in components | Grep for query patterns in component files, not just service files |
| Writing "what" without "why" in API docs | Every API endpoint MUST have a Why row explaining the business reason, not just technical description. "Fetches data" is not a Why. |
| Why row says "fetches X" or "returns Y" | That describes What, not Why. Ask: "What breaks without this call? What business goal does it serve?" |
| Headings with special characters breaking TOC | Use only alphanumeric, spaces, and hyphens in headings |
| Enormous single-pass exploration | Use parallel agents. Split by concern. |
| Documenting only the happy path | Include error handling, fallbacks, and nullability chains |
| Skipping the user stories | User stories provide the "why" context that makes technical docs useful |